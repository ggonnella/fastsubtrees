"""
Computation of the information necessary for the subtree query
"""

import struct
import array
import sys
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
    logger.debug(f"Writing to file \"{outfname}\" ...")
    with open(outfname, "wb") as f:
      f.write(struct.pack("QQQ", len(self.subtree_sizes), len(self.treedata),
                                 len(self.parents)))
      self.subtree_sizes.tofile(f)
      self.coords.tofile(f)
      self.treedata.tofile(f)
      self.parents.tofile(f)
    logger.success(f"Tree written to file \"{outfname}\"")
    return self.treedata

  @classmethod
  def from_file(cls, filename):
    self = cls()
    logger.debug(f"Reading from file \"{filename}\" ...")
    with open(filename, "rb") as f:
      idxsize, nelems, nparents = struct.unpack("QQQ", f.read(24))
      self.subtree_sizes.fromfile(f, idxsize)
      self.coords.fromfile(f, idxsize)
      self.treedata.fromfile(f, nelems)
      self.parents.fromfile(f, nparents)
      self.root_id = self.treedata[1]
    logger.success(f"Tree loaded from file \"{filename}\"")
    return self

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
    logger.info(f"Subtree of node {subtree_root} has size {subtree_size + 1}")
    return self.treedata[pos:pos + subtree_size + 1], pos, \
         subtree_size, subtree_parents

  def subtree_ids(self, subtree_root):
    try:
      subtree_data, pos, subtree_size, subtree_parents = \
          self.query_subtree(subtree_root)
    except ValueError:
      raise error.NodeNotFoundError(\
          f"The node ID does not exist, found: {subtree_root}")
    new_subtree_ids = array.array("Q")
    for data in subtree_data:
      if data != Tree.UNDEF and data != Tree.DELETED:
        new_subtree_ids.append(data)
    return new_subtree_ids

  def add_subtree(self, generator, attributefilenames=[]):
    for node_number, parent in generator:
      if node_number <= 0:
        raise error.ConstructionError(\
            f"The node IDs must be > 0, found: {node_number}")
      elif parent <= 0:
        raise error.ConstructionError(\
            f"The node IDs must be > 0, found: {parent}")
      else:
        if node_number < len(self.parents):
          if self.treedata[self.coords[node_number]] == Tree.DELETED:
            raise error.DeletedNodeError(\
                f'Node {node_number} was already deleted once. ' + \
                'Cannot add the same node again')
          else:
            if self.parents[node_number] != Tree.UNDEF:
              raise error.ConstructionError(\
                f"Node {node_number} had already been added with parent " + \
                f"{self.parents[node_number]}, cannot add it again with " + \
                f"parent {parent}")
            else:
              inspos = self.__prepare_node_insertion(node_number, parent)
              if attributefilenames:
                self.__insert_none_in_attribute_list(inspos, attributefilenames)
              self.__insert_node(node_number, inspos, parent)
              self.__update_subtree_sizes(node_number)
        else:
          inspos = self.__prepare_node_insertion(node_number, parent)
          if attributefilenames:
            self.__insert_none_in_attribute_list(inspos, attributefilenames)
          self.__insert_node(node_number, inspos, parent)
          self.__update_subtree_sizes(node_number)

  def __prepare_node_insertion(self, node_number, parent):
    try:
      inspos = self.coords[parent] + 1
      self.treedata.insert(inspos, node_number)
      return inspos
    except IndexError:
      raise error.ConstructionError(\
          f"The node {node_number} has parent {parent}, " + \
          f"which is not in the tree")

  def __insert_node(self, node_number, inspos, parent):
    if node_number < len(self.coords):
      try:
        self.coords[node_number] = inspos
      except TypeError:
        raise error.NodeNotFoundError(\
            f'The node ID {node_number} does not exist')
      self.parents[node_number] = parent
      for i in range(len(self.coords)):
        if i != node_number:
          if self.coords[i] >= inspos:
            self.coords[i] += 1
    else:
      len_coords = len(self.coords)
      diff = node_number - len_coords
      for i in range(diff):
        self.coords.insert(len_coords + i, 0)
        # subtree_size of 0 would mean 1, if so we would need to use an
        # undef value
        self.subtree_sizes.insert(len_coords + i, 0)
        self.parents.insert(len_coords + i, Tree.UNDEF)
      self.coords.insert(node_number, inspos)
      self.subtree_sizes.insert(node_number, 1)
      self.parents.insert(node_number, parent)
      for i in range(len_coords):
        if self.coords[i] >= inspos:
          self.coords[i] += 1

  def __update_subtree_sizes(self, node_number):
    p = self.parents[node_number]
    while p != Tree.UNDEF:
      self.subtree_sizes[p] += 1
      p = self.parents[p]

  def delete_node(self, node_number, attributefilenames=[]):
    elements = self.subtree_ids(node_number)
    coord = self.coords[node_number]
    subtree_size = self.subtree_sizes[node_number]
    for i in range(subtree_size + 1):
      self.treedata[coord + i] = Tree.DELETED
      self.__delete_node_in_attribute_list(coord + i, attributefilenames)
    # for element in elements:
    #   self.coords[element] = Tree.UNDEF
    #   self.parents[element] = Tree.UNDEF

  def __insert_none_in_attribute_list(self, inspos, attributefilenames):
    for filename in attributefilenames:
      with open(f'{filename}.attr', 'r+') as file:
        contents = file.readlines()
        contents.insert(inspos-1, 'null' + "\n")
        file.seek(0)
        file.writelines(contents)

  def __delete_node_in_attribute_list(self, pos, attributefilenames):
    for filename in attributefilenames:
      with open(f'{filename}.attr', 'r+') as file:
        contents = file.readlines()
        contents[pos-1] = str(Tree.DELETED) + "\n"
        file.seek(0)
        file.writelines(contents)
