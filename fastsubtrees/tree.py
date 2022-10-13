"""
Computation of the information necessary for the subtree query
"""

import struct
import array
import sys
from collections import defaultdict
from fastsubtrees import logger, tqdm, error

class Tree():

  def __init__(self):
    self.subtree_sizes = array.array("Q")
    self.coords = array.array("Q")
    self.treedata = array.array("Q")
    self.parents = array.array("Q")
    self.root_id = None

  UNDEF = sys.maxsize
  DELETED = sys.maxsize - 1

  @staticmethod
  def __from_csv(filename, separator, elem_field_num, parent_field_num):
    logger.info(f"Reading data from file \"{filename}\" ...")
    with open(filename) as f:
      for line in tqdm(f):
        if line[0] == "#":
          continue
        fields = line.rstrip().split(separator)
        elem = int(fields[elem_field_num])
        parent = int(fields[parent_field_num])
        yield elem, parent

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
  def construct(cls, generator):
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
  def construct_from_csv(cls, filename, separator,
               elem_field_num, parent_field_num):
    generator = cls.__from_csv(filename, separator,
                   elem_field_num, parent_field_num)
    return cls.construct(generator)

  def to_file(self, outfname):
    logger.debug(f"Writing tree to file \"{outfname}\" ...")
    with open(outfname, "wb") as f:
      f.write(struct.pack("QQQ", len(self.subtree_sizes), len(self.treedata),
                                 len(self.parents)))
      self.subtree_sizes.tofile(f)
      self.coords.tofile(f)
      self.treedata.tofile(f)
      self.parents.tofile(f)
    logger.info(f"Tree written to file \"{outfname}\"")
    return self.treedata

  @classmethod
  def from_file(cls, filename):
    self = cls()
    logger.debug(f"Loading tree from file \"{filename}\" ...")
    with open(filename, "rb") as f:
      idxsize, nelems, nparents = struct.unpack("QQQ", f.read(24))
      self.subtree_sizes.fromfile(f, idxsize)
      self.coords.fromfile(f, idxsize)
      self.treedata.fromfile(f, nelems)
      self.parents.fromfile(f, nparents)
      self.root_id = self.treedata[1]
    logger.debug(f"Tree loaded from file \"{filename}\"")
    return self

  def get_parent(self, node):
    if node == self.root_id or node == self.DELETED or node == self.UNDEF:
      return node
    else:
      return self.parents[node]

  def get_subtree_size(self, node):
    if node == self.DELETED or node == self.UNDEF:
      return 0
    return self.subtree_sizes[node] + 1

  def query_subtree(self, subtree_root):
    if subtree_root <= 0 or subtree_root > len(self.coords) - 1:
      logger.info(f"Node {subtree_root} not in tree => subtree is empty")
      return []
    pos = self.coords[subtree_root]
    logger.debug(f"Coordinate of node {subtree_root}: {pos}")
    if pos == 0:
      return []
    subtree_size = self.subtree_sizes[subtree_root]
    subtree_parents = self.parents[subtree_root]
    logger.debug(\
        f"Subtree under node {subtree_root} has size {subtree_size + 1} "+\
        "(including deleted nodes, if any)")
    return self.treedata[pos:pos + subtree_size + 1], pos, \
         subtree_size, subtree_parents

  def subtree_ids(self, subtree_root, include_deleted=False):
    try:
      subtree_data, pos, subtree_size, subtree_parents = \
          self.query_subtree(subtree_root)
    except ValueError:
      raise error.NodeNotFoundError(\
          f"The node ID does not exist, found: {subtree_root}")
    new_subtree_ids = array.array("Q")
    for data in subtree_data:
      if data != Tree.UNDEF and (data != Tree.DELETED or include_deleted):
        new_subtree_ids.append(data)
    return new_subtree_ids

  def add_nodes(self, generator, attrfilenames=[], skip_existing=False,
                  rm_existing_set=None, list_added=None, total=None,
                  edit_script=None):
    n_added = 0
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
            del pending[node]
    if len(pending) > 0:
      raise error.ConstructionError(\
          "Impossible operations because the node parents " + \
          f"were not present in the tree: {pending}")
    self.__edit_attribute_values(edit_script, attrfilenames)
    return n_added

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

  def delete_subtree(self, node_number, attrfilenames=[],
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

  def update(self, generator, attrfiles, list_added=None, list_deleted=None,
             total=None):
    edit_script = []
    deleted = set(self.subtree_ids(self.root_id))
    n_added = self.add_nodes(generator, skip_existing=True,
        rm_existing_set=deleted, list_added=list_added, total=total,
        edit_script=edit_script)
    parents_of_deleted = {n: self.get_parent(n) for n in deleted}
    n_deleted = 0
    for n in deleted:
      if parents_of_deleted[n] in deleted:
        continue
      n_deleted += self.delete_subtree(n, list_deleted=list_deleted,
          edit_script=edit_script)
    self.__edit_attribute_values(edit_script, attrfiles)
    return n_added, n_deleted

  NONELINE = 'null\n'

  def __edit_attribute_values(self, edit_script, attrfilenames):
    print(edit_script)
    for attrfilename in attrfilenames:
      with open(attrfilename, 'r') as f:
        lines = f.readlines()
      print(lines)
      for op in edit_script:
        if op[0] == "insert":
          lines.insert(op[1]-1, Tree.NONELINE)
        elif op[0] == "copy":
          lines[op[1]-1] = lines[op[2]-1]
        elif op[0] == "delete":
          lines[op[1]-1] = Tree.NONELINE
      with open(attrfilename, 'w') as f:
        f.writelines(lines)

