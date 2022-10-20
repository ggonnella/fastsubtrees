"""
Editing operations for fastsubtrees.Tree objects.
"""

from collections import defaultdict
from typing import List, Union, Iterator, Tuple
from pathlib import Path
from fastsubtrees import logger, tqdm, error
from fastsubtrees.ids_modules import ids_from_tabular_file

class TreeEditor():

  def __add_or_move_nodes(self, generator, attrfilenames=[],
      skip_existing=False, rm_existing_set=None, list_added=None,
      list_moved=None, total=None, edit_script=None):
    n_added = 0
    n_moved = 0
    pending = defaultdict(list)
    logger.info("Tree root: " + str(self.root_id))
    if edit_script is None:
      edit_script = []
    for node_number, parent in tqdm(generator, total=total):
      if rm_existing_set is not None:
        rm_existing_set.discard(node_number)
      if node_number < 0:
        raise error.ConstructionError(\
            f"The node IDs must be >= 0, found: {node_number}")
      elif parent < 0:
        raise error.ConstructionError(\
            f"The node parent IDs must be >= 0, found: {parent}")
      if node_number < len(self.parents):
        if node_number == self.root_id:
          if skip_existing:
            if node_number == parent:
              continue
            else:
              raise error.ConstructionError(\
                  f'Node {node_number} / parent {parent} already exists '+\
                  'as the root node')
          else:
            raise error.ConstructionError(\
                f"The root node {node_number} already exists")
        if self.parents[node_number] != self.UNDEF and \
              self.treedata[self.coords[node_number]] != self.UNDEF:
          if skip_existing:
            if self.parents[node_number] != parent:
              if parent >= len(self.parents) or self.coords[parent] == 0:
                pending[parent].append(('move', node_number))
              else:
                self.__move_subtree(node_number, parent, edit_script)
                n_moved += 1
                if list_moved is not None:
                  list_moved.append(node_number)
            continue
          else:
            if self.parents[node_number] != parent:
              raise error.ConstructionError(\
                f"Node {node_number} / parent {parent} already exists "+\
                f"with a different parent ({self.parents[node_number]})")
            else:
              raise error.ConstructionError(\
                f"Node {node_number} / parent {parent} already exists")
      if parent >= len(self.parents) or self.coords[parent] == 0:
        pending[parent].append(("insert", node_number))
      else:
        self.__insert_node(node_number, parent, edit_script, list_added)
        n_added += 1
        stack = [node_number]
        while stack:
          node = stack.pop()
          if node in pending:
            for child in pending[node]:
              if child[0] == "insert":
                self.__insert_node(child[1], node, edit_script, list_added)
                n_added += 1
                stack.append(child[1])
              elif child[0] == "move":
                self.__move_subtree(child[1], node, edit_script)
                n_moved += 1
                if list_moved is not None:
                  list_moved.append(child[1])
            del pending[node]
    if len(pending) > 0:
      raise error.ConstructionError(\
          "Impossible operations because the node parents " + \
          f"were not present in the tree: {pending}")
    self._edit_attribute_values(edit_script, attrfilenames)
    return n_added, n_moved

  def __insert_node(self, node_number, parent, edit_script, list_added):
    # the idea for the insertion is the following
    # - in treedata, the insertion position is after the parent
    # - thus coords must be updated, adding 1 to all the coords >= inspos
    # - if the node_number is larger than the current max_node_number then
    #   parents/coords and subtree_sizes must be extended
    # - the parents/coords/subtree_sizes values for the node must be set
    #   (to parent/inspos/0)
    # - subtree_sizes must be updated, adding 1 to all ancestors of node_number
    assert self.coords[parent] > 0
    inspos = self.coords[parent] + 1
    n_existing = len(self.coords)
    for i in range(n_existing):
      if self.coords[i] >= inspos:
        self.coords[i] += 1
    self.treedata.insert(inspos, node_number)
    edit_script.append(("insert", inspos))
    n_to_append = node_number + 1 - n_existing
    if n_to_append > 0:
      self.coords.extend([0] * n_to_append)
      self.parents.extend([self.UNDEF] * n_to_append)
      self.subtree_sizes.extend([0] * n_to_append)
    self.coords[node_number] = inspos
    self.parents[node_number] = parent
    self.subtree_sizes[node_number] = 1
    if list_added is not None:
      list_added.append(node_number)
    p = self.parents[node_number]
    while p != node_number:
      assert p != self.UNDEF
      self.subtree_sizes[p] += 1
      node_number = p
      p = self.parents[node_number]

  def __move_subtree(self, subtree_root, new_parent, edit_script):
    subtree_size = self.subtree_sizes[subtree_root]
    assert self.coords[new_parent] > 0
    inspos = self.coords[new_parent] + 1
    for i in range(subtree_size):
      self.treedata.insert(inspos, self.UNDEF)
      edit_script.append(("insert", inspos))
    n_existing = len(self.coords)
    for i in range(n_existing):
      if self.coords[i] >= inspos:
        self.coords[i] += subtree_size
    oldpos = self.coords[subtree_root]
    for i in range(subtree_size):
      nodenum = self.treedata[oldpos + i]
      self.treedata[inspos + i] = nodenum
      if nodenum != self.UNDEF:
        self.coords[nodenum] = inspos + i
        edit_script.append(("copy", oldpos + i, inspos + i))
      self.treedata[oldpos + i] = self.UNDEF
      edit_script.append(("delete", oldpos + i))
    self.parents[subtree_root] = new_parent
    p = new_parent
    while True:
      self.subtree_sizes[p] += subtree_size
      gp = self.parents[p]
      if gp == p:
        break
      p = gp

  def __delete_subtree(self, node_number, attrfilenames=[],
                     list_deleted = None, edit_script = None):
    try:
      coord = self.coords[node_number]
    except IndexError:
      raise error.NodeNotFoundError(\
          f"The node ID does not exist: {node_number}")
    n_deleted = 0
    if edit_script is None:
      edit_script = []
    subtree_size = self.subtree_sizes[node_number]
    for i in range(subtree_size):
      delpos = coord + i
      if self.treedata[delpos] != self.UNDEF:
        deleted = self.treedata[delpos]
        self.treedata[delpos] = self.UNDEF
        edit_script.append(("delete", delpos))
        n_deleted += 1
        if list_deleted is not None:
          list_deleted.append(deleted)
        # logger.info(f"Deleted node {deleted} at position {delpos}")
    self._edit_attribute_values(edit_script, attrfilenames)
    return n_deleted

  def __get_attrfilenames(self):
    if self.filename:
      attrfilenames = self.existing_attribute_filenames(self.filename).values()
      if attrfilenames:
        logger.debug("Attribute files to be updated: '{}'".\
            format("', '".join([str(x) for x in attrfilenames])))
      else:
        logger.debug("No attribute files to be updated")
    else:
      logger.debug("Attribute files will not be updated because the tree " +\
          "filename is not set")
      attrfilenames = []
    return attrfilenames

  def move_subtree(self, subtree_root: int, new_parent: int):
    """
    Moves a subtree to a different point in the tree.
    If the tree filename is set and attributes exist, then the attribute values
    are moved to reflect the new node positions.
    """
    self._check_node_number(subtree_root)
    if subtree_root == self.root_id:
      raise error.ConstructionError("The root node cannot be moved")
    self._check_node_number(new_parent)
    if self.get_parent(subtree_root) == new_parent:
      return
    if new_parent in self.subtree_ids(subtree_root):
      raise error.ConstructionError(\
          "A node cannot be moved to be a descendant of itself")
    edit_script = []
    self.__move_subtree(subtree_root, new_parent, edit_script)
    attrfilenames = self.__get_attrfilenames()
    self._edit_attribute_values(edit_script, attrfilenames)

  def delete_subtree(self, subtree_root: int,
      list_deleted: Union[None, List[int]] = None) -> int:
    """
    Deletes the subtree rooted at node, and returns the number of deleted nodes.
    If the tree filename is set and attributes exist, then the attribute values
    are deleted from the corresponding nodes.

    If list_deleted is not None, then the list is filled with the node numbers
    of the deleted nodes.

    Returns the number of deleted nodes.
    """
    attrfilenames = self.__get_attrfilenames()
    return self.__delete_subtree(subtree_root, attrfilenames, list_deleted)

  def add_nodes(self, generator: Iterator[Tuple[int, int]],
                list_added: Union[None, List[int]] = None,
                total: Union[None, int] = None) -> int:
    """
    Add the nodes yielded by the generator to the tree.
    The generator must yield tuples of the form (node_number, parent_number).

    The nodes must be not yet present in the tree, and the parent must be
    present or added in the same call to add_nodes.

    If the tree filename is set and attributes exist, then empty attribute
    values are added for the added nodes.

    If list_added is not None, then the list is filled with the node numbers
    of the added nodes.

    If total is provided, then it is used to display a progress bar.
    It should be set to the total number of tuples yielded by the generator.

    Returns the number of added nodes.
    """
    attrfilenames = self.__get_attrfilenames()
    n_added, _ = self.__add_or_move_nodes(generator, attrfilenames,
        list_added=list_added, total=total)
    return n_added

  def update(self, generator: Iterator[Tuple[int, int]],
             list_added: Union[None, List[int]] = None,
             list_deleted: Union[None, List[int]] = None,
             list_moved: Union[None, List[int]] = None,
             total: Union[None, int] = None) -> Tuple[int, int, int]:
    """
    Updates the tree with the nodes in the generator.
    The generator must yield tuples of the form (node_number, parent_number).

    If the tree filename is set and attributes exist, then the attribute
    values are updated for the corresponding nodes.

    If list_added, list_deleted, list_moved are not None, then the lists are
    filled with the node numbers of the added nodes, deleted nodes, and moved
    nodes, respectively.

    If total is provided, then it is used to display a progress bar.
    It should be set to the total number of tuples yielded by the generator.

    Returns a tuple (n_added, n_deleted, n_moved).
    """
    edit_script = []
    attrfilenames = self.__get_attrfilenames()
    deleted = set(self.subtree_ids(self.root_id))
    n_added, n_moved = self.__add_or_move_nodes(generator, skip_existing=True,
        rm_existing_set=deleted, list_added=list_added, list_moved=list_moved,
        total=total, edit_script=edit_script)
    parents_of_deleted = {n: self.get_parent(n) for n in deleted}
    n_deleted = 0
    for n in deleted:
      if parents_of_deleted[n] in deleted:
        continue
      n_deleted += self.__delete_subtree(n, list_deleted=list_deleted,
          edit_script=edit_script)
    self._edit_attribute_values(edit_script, attrfilenames)
    return n_added, n_deleted, n_moved

  def update_from_tabular(self, filename: Union[str, Path],
                             separator: str = "\t", elem_field_num: int = 0,
                             parent_field_num: int = 1,
                             list_added: Union[None, List[int]] = None,
                             list_deleted: Union[None, List[int]] = None,
                             list_moved: Union[None, List[int]] = None,
                             total: Union[None, int] = None)\
                               -> Tuple[int, int, int]:
    generator = ids_from_tabular_file.element_parent_ids(filename, separator,
        elem_field_num, parent_field_num)
    return self.update(generator, list_added=list_added,
        list_deleted=list_deleted, list_moved=list_moved, total=total)

  def update_from_ncbi_dump(self, filename: Union[str, Path],
                            list_added: Union[None, List[int]] = None,
                            list_deleted: Union[None, List[int]] = None,
                            list_moved: Union[None, List[int]] = None,
                            total: Union[None, int] = None)\
                              -> Tuple[int, int, int]:
    generator = ids_from_tabular_file.element_parent_ids(filename,
        ncbi_preset=True)
    return self.update(generator, list_added=list_added,
        list_deleted=list_deleted, list_moved=list_moved, total=total)

  def reset(self, generator: Iterator[Tuple[int, int]],
            total: Union[None, int] = None):
    """
    Resets the tree with the nodes in the generator.
    The generator must yield tuples of the form (node_number, parent_number).

    If the tree filename is set and attributes exist, then the attribute
    values are updated for the corresponding nodes.

    If total is provided, then it is used to display a progress bar.
    It should be set to the total number of tuples yielded by the generator.
    """
    self._check_filename_set()
    attrnames = self.list_attributes()
    for attrname in attrnames:
      self.dump_attribute_values(attrname)
    self._reset_data()
    self._compute_parents(generator)
    self._compute_subtree_sizes()
    self._compute_treedata_and_coords()
    for attrname in attrnames:
      self.create_attribute_from_dump(attrname)

  def reset_from_tabular(self, filename: Union[str, Path],
                         separator: str = "\t", elem_field_num: int = 0,
                         parent_field_num: int = 1,
                         total: Union[None, int] = None):
    generator = ids_from_tabular_file.element_parent_ids(filename, separator,
        elem_field_num, parent_field_num)
    self.reset(generator, total=total)

  def reset_from_ncbi_dump(self, filename: Union[str, Path],
                           total: Union[None, int] = None):
    generator = ids_from_tabular_file.element_parent_ids(filename,
        ncbi_preset=True)
    self.reset(generator, total=total)
