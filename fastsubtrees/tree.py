"""
Computation of the information necessary for the subtree query
"""

import struct
import array
import sys
from collections import defaultdict
from typing import List, Union, Iterator, Tuple, Dict, Any
import json
import glob
from pathlib import Path
from fastsubtrees import logger, tqdm, error
from fastsubtrees.ids_modules import ids_from_tabular_file

class Tree():

  def __init__(self):
    self.subtree_sizes = array.array("Q")
    self.coords = array.array("Q")
    self.treedata = array.array("Q")
    self.parents = array.array("Q")
    self.root_id = None
    self.filename = None

  UNDEF = sys.maxsize
  DELETED = sys.maxsize - 1

  def __compute_parents(self, generator):
    self.parents = array.array("Q")
    assert (self.root_id is None)
    for elem, parent in generator:
      if elem == self.root_id:
        raise error.ConstructionError( \
          f"Node {elem} had already been added as root, cannot " + \
          f"add it again with parent {parent}")
      if elem <= 0:
        raise error.ConstructionError( \
          f"The node IDs must be > 0, found: {elem}")
      if parent <= 0:
        raise error.ConstructionError( \
          f"The node IDs must be > 0, found: {parent}")
      n_missing = elem + 1 - len(self.parents)
      if n_missing > 0:
        for i in range(n_missing):
          self.parents.append(Tree.UNDEF)
      if self.parents[elem] != Tree.UNDEF:
        raise error.ConstructionError( \
          f"Node {elem} had already been added with parent " + \
          f"{self.parents[elem]}, cannot add it again with " + \
          f"parent {parent}")
      if parent != elem:
        self.parents[elem] = parent
      elif self.root_id is None:
        self.root_id = elem
      else:
        raise error.ConstructionError( \
          f"The tree already has a root node {self.root_id}, " + \
          f"cannot add a second root node {elem}")
    if self.root_id is None:
      raise error.ConstructionError( \
        "The tree does not have any root node")

  def __compute_subtree_sizes(self):
    self.subtree_sizes = array.array('Q', [0] * len(self.parents))
    for elem, parent in tqdm(enumerate(self.parents)):
      while parent != Tree.UNDEF:
        if parent >= len(self.parents):
          raise error.ConstructionError( \
            f"The node {elem} has parent {parent}, " + \
            f"which is not in the tree")
        self.subtree_sizes[parent] += 1
        if parent == self.root_id:
          break
        else:
          grandparent = self.parents[parent]
          if grandparent == Tree.UNDEF:
            raise error.ConstructionError( \
              f"The parent of node {elem} is {parent}, " + \
              f"but this is not correctly connected to the tree")
          elem = parent
          parent = grandparent

  def __compute_treedata(self):
    treesize = self.subtree_sizes[self.root_id] + 1
    self.treedata = array.array("Q", [0] * (treesize + 1))
    self.coords = array.array("Q", [0] * len(self.parents))
    self.treedata[1] = self.root_id
    self.coords[self.root_id] = 1
    for i in tqdm(range(len(self.parents))):
      if self.parents[i] != Tree.UNDEF:
        path = [i]
        parent = self.parents[i]
        while parent != self.root_id:
          path.append(parent)
          parent = self.parents[parent]
        for node in reversed(path):
          if not self.coords[node]:
            pos = self.coords[self.parents[node]] + 1
            while True:
              treedatanode = self.treedata[pos]
              if treedatanode == 0:
                break
              else:
                pos += (self.subtree_sizes[treedatanode] + 1)
            self.coords[node] = pos
            self.treedata[pos] = node

  @classmethod
  def construct(cls, generator: Iterator[Tuple[int, int]]):
    """
    Construct a tree from a generator that yields tuples of the form
    (node, parent).
    """
    self = cls()
    logger.info("Constructing temporary parents table...")
    self.__compute_parents(generator)
    logger.info("Constructing subtree sizes table...")
    self.__compute_subtree_sizes()
    logger.info("Constructing tree data and index...")
    self.__compute_treedata()
    logger.success("Tree data structure constructed")
    return self

  @classmethod
  def construct_from_tabular(cls, filename: Union[str, Path],
                             separator: str = "\t", elem_field_num: int = 0,
                             parent_field_num: int = 1):
    """
    Construct a tree from a tabular file.
    """
    generator = ids_from_tabular_file(filename, separator,
        elem_field_num, parent_field_num)
    return cls.construct(generator)

  @classmethod
  def construct_from_ncbi_dump(cls, filename: Union[str, Path]):
    """
    Constructs a tree from a NCBI taxonomy dump nodes file.
    """
    generator = ids_from_tabular_file(filename, ncbi_preset=True)
    return cls.construct(generator)

  def to_file(self, outfname: Union[str, Path]):
    """
    Save the tree to file.
    """
    self.filename = Path(outfname)
    with open(outfname, "wb") as f:
      f.write(struct.pack("QQQ", len(self.subtree_sizes), len(self.treedata),
                                 len(self.parents)))
      self.subtree_sizes.tofile(f)
      self.coords.tofile(f)
      self.treedata.tofile(f)
      self.parents.tofile(f)
    logger.info(f"Tree written to file \"{outfname}\"")

  @classmethod
  def from_file(cls, filename: Union[str, Path]):
    """
    Load a tree from a file.
    """
    self = cls()
    with open(filename, "rb") as f:
      idxsize, nelems, nparents = struct.unpack("QQQ", f.read(24))
      self.subtree_sizes.fromfile(f, idxsize)
      self.coords.fromfile(f, idxsize)
      self.treedata.fromfile(f, nelems)
      self.parents.fromfile(f, nparents)
      self.root_id = self.treedata[1]
    logger.debug(f"Tree loaded from file \"{filename}\"")
    self.filename = filename
    return self

  def __check_node_number(self, node):
    if node <= 0 or node > len(self.coords) - 1:
      raise error.NodeNotFoundError(f"Node ID '{node}' does not exist.")

  def get_parent(self, node: int) -> int:
    """
    Returns the parent ID of the given node.
    """
    self.__check_node_number(node)
    if node == self.root_id or node == self.DELETED or node == self.UNDEF:
      return node
    else:
      return self.parents[node]

  def get_subtree_size(self, node: int) -> int:
    """
    Returns the number of nodes in the subtree rooted at the given node.
    """
    self.__check_node_number(node)
    if node == self.DELETED or node == self.UNDEF:
      return 0
    return self.subtree_sizes[node] + 1

  def get_treedata_coord(self, node: int) -> int:
    """
    Returns the position of the given node in the treedata array.
    """
    self.__check_node_number(node)
    return self.coords[node]

  def get_subtree_data(self, subtree_root: int) -> array.array:
    """
    Returns the treedata array for the subtree rooted at the given node.

    This includes nodes marked as deleted.
    """
    self.__check_node_number(subtree_root)
    pos = self.get_treedata_coord(subtree_root)
    if pos > 0:
      subtree_size = self.get_subtree_size(subtree_root)
      return self.treedata[pos:pos + subtree_size]
    else:
      return array.array("Q")

  def subtree_ids(self, subtree_root: int) -> array.array:
    """
    Returns the IDs of the nodes in the subtree rooted at the given node.
    """
    self.__check_node_number(subtree_root)
    result = array.array("Q")
    for node_id in self.get_subtree_data(subtree_root):
      if (node_id != self.DELETED and node_id != self.UNDEF):
        result.append(node_id)
    return result

  NONELINE = 'null\n'

  def __edit_attribute_values(self, edit_script, attrfilenames):
    for attrfilename in attrfilenames:
      with open(attrfilename, 'r') as f:
        lines = f.readlines()
      for op in edit_script:
        if op[0] == "insert":
          lines.insert(op[1]-1, Tree.NONELINE)
        elif op[0] == "copy":
          lines[op[1]-1] = lines[op[2]-1]
        elif op[0] == "delete":
          lines[op[1]-1] = Tree.NONELINE
      with open(attrfilename, 'w') as f:
        f.writelines(lines)

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
      if node_number <= 0:
        raise error.ConstructionError(\
            f"The node IDs must be > 0, found: {node_number}")
      elif parent <= 0:
        raise error.ConstructionError(\
            f"The node parent IDs must be > 0, found: {parent}")
      if node_number < len(self.parents):
        if node_number == self.root_id:
          if skip_existing:
            if node_number != parent:
              raise error.ConstructionError(\
                  f'Node {node_number} / parent {parent} already exists '+\
                  f'as the root node')
            continue
          else:
            raise error.ConstructionError(\
                f"The root node {node_number} already exists")
        if self.parents[node_number] != Tree.UNDEF and \
              self.treedata[self.coords[node_number]] != Tree.DELETED:
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
    self.__edit_attribute_values(edit_script, attrfilenames)
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
    assert(self.coords[parent] > 0)
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
      self.parents.extend([Tree.UNDEF] * n_to_append)
      self.subtree_sizes.extend([0] * n_to_append)
    self.coords[node_number] = inspos
    self.parents[node_number] = parent
    self.subtree_sizes[node_number] = 0
    p = self.parents[node_number]
    while p != Tree.UNDEF:
      self.subtree_sizes[p] += 1
      p = self.parents[p]
    #logger.info(f"Inserted node {node_number} with parent {parent} at position {inspos}")
    if list_added is not None:
      list_added.append(node_number)

  def __move_subtree(self, subtree_root, new_parent, edit_script):
    subtree_size = self.subtree_sizes[subtree_root] + 1
    assert(self.coords[new_parent] > 0)
    inspos = self.coords[new_parent] + 1
    for i in range(subtree_size):
      self.treedata.insert(inspos, Tree.UNDEF)
      edit_script.append(("insert", inspos))
    n_existing = len(self.coords)
    for i in range(n_existing):
      if self.coords[i] >= inspos:
        self.coords[i] += subtree_size
    oldpos = self.coords[subtree_root]
    for i in range(subtree_size):
      nodenum = self.treedata[oldpos + i]
      self.treedata[inspos + i] = nodenum
      if nodenum != Tree.UNDEF and nodenum != Tree.DELETED:
        self.coords[nodenum] = inspos + i
        edit_script.append(("copy", oldpos + i, inspos + i))
      self.treedata[oldpos + i] = Tree.DELETED
      edit_script.append(("delete", oldpos + i))
    self.parents[subtree_root] = new_parent
    p = new_parent
    while p != Tree.UNDEF:
      self.subtree_sizes[p] += subtree_size
      p = self.parents[p]

  def __delete_subtree(self, node_number, attrfilenames=[],
                     list_deleted = None, edit_script = None):
    try:
      coord = self.coords[node_number]
    except IndexError:
      raise error.NodeNotFoundError(\
          f"The node ID does not exist: {node_number}")
    n_deleted = 0
    subtree_size = self.subtree_sizes[node_number]
    if edit_script is None:
      edit_script = []
    for i in range(subtree_size + 1):
      delpos = coord + i
      if self.treedata[delpos] != Tree.DELETED:
        deleted = self.treedata[delpos]
        self.treedata[delpos] = Tree.DELETED
        edit_script.append(("delete", delpos))
        n_deleted += 1
        if list_deleted is not None:
          list_deleted.append(deleted)
        #logger.info(f"Deleted node {deleted} at position {delpos}")
    self.__edit_attribute_values(edit_script, attrfilenames)
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
    __check_node_number(subtree_root)
    if subtree_root == self.root_id:
      raise error.ConstructionError("The root node cannot be moved")
    __check_node_number(new_parent)
    if self.get_parent(subtree_root) == new_parent:
      return
    edit_script = []
    self.__move_subtree(subtree_root, new_parent, edit_script)
    attrfilenames = self.__get_attrfilenames()
    self.__edit_attribute_values(edit_script, attrfilenames)

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
    self.__edit_attribute_values(edit_script, attrfiles)
    return n_added, n_deleted, n_moved

  ATTR_EXT = "attr"

  def set_filename(self, filename: Union[str, Path]):
    """
    Sets the filename of the tree.

    The filename is used to compute the name of the files where
    attribute values are stored.

    The filename is automatically set when the tree is loaded from a file
    or saved to a file.
    """
    self.filename = Path(filename)

  @staticmethod
  def compute_attribute_filename(treefilename, attribute):
    return Path(f"{treefilename}.{attribute}.{Tree.ATTR_EXT}")

  @staticmethod
  def existing_attribute_filenames(treefilename: Union[str, Path]) \
      -> Dict[str, Path]:
    treefilename = str(treefilename)
    result = {}
    globpattern = treefilename + ".*." + Tree.ATTR_EXT
    for file in glob.glob(globpattern):
      attribute = file[len(treefilename)+1:-(len(Tree.ATTR_EXT))-1]
      result[attribute] = Path(file)
    return result

  def destroy_all_attributes(self):
    """
    Destroys all attribute values associated with the tree.
    """
    self.__check_filename_set()
    for filename in self.existing_attribute_filenames(self.filename).values():
      logger.info("Removing obsolete attribute file {}".format(filename))
      filename.unlink()

  def __check_filename_set(self):
    if self.filename is None:
      raise RuntimeError("The tree filename is not set")

  def attribute_filename(self, attribute) -> Path:
    """
    Returns the filename where the attribute values are stored.
    """
    self.__check_filename_set()
    return self.compute_attribute_filename(self.filename, attribute)

  def list_attributes(self) -> List[str]:
    """
    Returns a list of the attribute names.
    """
    self.__check_filename_set()
    return list(self.existing_attribute_filenames(self.filename).keys())

  def has_attribute(self, attribute):
    attrfilename = self.attribute_filename(attribute)
    return attrfilename.exists()

  def __check_has_attribute(self, attribute):
    if not self.has_attribute(attribute):
      attrfilename = self.attribute_filename(attribute)
      raise RuntimeError(f"Attribute '{attribute}' does not exist "+\
          "(file '{attrfilename}' does not exist)")

  def destroy_attribute(self, attribute: str):
    """
    Destroys the attribute values associated with the given attribute.
    """
    self.__check_filename_set()
    self.__check_has_attribute(attribute)
    filename = self.attribute_filename(attribute)
    logger.info("Removing obsolete attribute file {}".format(filename))
    filename.unlink()

  def subtree_attribute_data(self, subtree_root, attribute):
    self.__check_filename_set()
    self.__check_has_attribute(attribute)
    subtree_size = self.get_subtree_size(subtree_root)
    coord = self.get_treedata_coord(subtree_root) - 1
    attrfilename = self.attribute_filename(attribute)
    line_no = 0
    result = []
    with open(attrfilename, 'r') as f:
      for line in f:
        if line_no in range(coord, coord + subtree_size):
          result.append(json.loads(line.rstrip()))
        line_no += 1
    return result

  def save_attribute_values(self, attribute, attrvalues):
    self.__check_filename_set()
    attrfname = self.attribute_filename(attribute)
    with open(attrfname, "w") as outfile:
      for element_id in self.get_subtree_data(self.root_id):
        if element_id == self.DELETED:
          attribute = None
        else:
          attribute = attrvalues.get(element_id, None)
        outfile.write(json.dumps(attribute) + "\n")
    logger.debug("Saved attribute values to file '{}'...".format(attrfname))

  def check_has_attributes(self, attributes):
    self.__check_filename_set()
    for attribute in attributes:
      attrfname = self.attribute_filename(attribute)
      if not attrfname.exists():
        logger.error("Attribute '{}' not found".format(attribute))
        return False
    return True

  def query_attributes(self, subtree_root: int, attributes: List[str],
                       show_stats: bool = False) -> Dict[str, List[Any]]:
    """
    Returns attribute values for the given subtree, for multiple
    attributes, as a dictionary in the form {'attribute_name': [values]}.
    """
    result = {}
    for attrname in attributes:
      logger.debug("Loading attribute '{}' values".format(attrname))
      result[attrname] = self.subtree_attribute_data(subtree_root, attrname)
      if show_stats:
        filtered = [a for a in result[attrname] if a is not None]
        flattened = [e for sl in filtered for e in sl]
        logger.info("Number of nodes with attribute '{}': {}".\
            format(attrname, len(filtered)))
        logger.info("Number of values of attribute '{}': {}".\
            format(attrname, len(flattened)))
    return result

  def subtree_info(self, subtree_root: int, attributes: List[str] = [],
                   include_subtree_sizes: bool = False,
                   include_parents: bool = False,
                   show_stats: bool = False,
                   node_id_key = "node_id",
                   subtree_size_key = "subtree_size",
                   parent_key = "parent") -> Dict[str, List[Any]]:
    result = {}
    node_ids = self.get_subtree_data(subtree_root)
    result[node_id_key] = node_ids
    if include_subtree_sizes:
      result[subtree_size_key] = []
      for node_id in node_ids:
        result[subtree_size_key].append(self.get_subtree_size(node_id))
    if include_parents:
      result[parent_key] = []
      for node_id in node_ids:
        result[parent_key].append(self.get_parent(node_id))
    if attributes:
      attr_values = self.query_attributes(subtree_root, attributes, show_stats)
      for attrname in attributes:
        result[attrname] = attr_values[attrname]
    return result

  def load_attribute_values(self, attribute):
    self.__check_filename_set()
    self.__check_has_attribute(attribute)
    i = 0
    fname = self.attribute_filename(attribute)
    all_ids = self.get_subtree_data(self.root_id)
    existing = {}
    with open(fname, "r") as f:
      for line in f:
        data = json.loads(line.rstrip())
        existing[all_ids[i]] = data
        i += 1
    return existing
