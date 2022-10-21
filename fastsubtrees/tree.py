"""
Computation of the information necessary for the subtree query
"""

import struct
import array
import sys
from typing import Union, Iterator, Tuple
from pathlib import Path
from fastsubtrees import logger, tqdm, error
from fastsubtrees.ids_modules import ids_from_tabular_file
from multiprocessing.pool import Pool
from .attribute import TreeAttributes
from .query import SubtreeQuery
from .edit import TreeEditor

class Tree(TreeAttributes, SubtreeQuery, TreeEditor):
  """
  Representation of a tree, which allows fast subtree queries.

  For constructing an object of this class, you can use one of the
  following methods:
  - from_file(cls, filename: Union[str, Path]): load a tree from a fastsubtrees
    tree file, where it was previously saved with the to_file method.
  - construct(cls, generator: Iterator[Tuple[int, int]]): construct a tree
    from a generator of (node, parent) pairs.
  - construct_from_tabular(cls, filename: Union[str, Path],
                           separator: str = "\t", elem_field_num: int = 0,
                          parent_field_num: int = 1, n_processes: int = 1):
    construct a tree from a tabular file, where each line contains the
    node ID and its parent ID, separated by the separator character.
    The elem_field_num and parent_field_num parameters specify the (0-based)
    column numbers of the node and parent IDs, respectively.
  - construct_from_ncbi_dump(cls, filename: Union[str, Path]): construct a
    tree from a NCBI taxonomy dump file; this is specialized version
    of the construct_from_tabular method, where the separator and field
    numbers are set to the values used in the NCBI taxonomy dump files.

  The tree can be saved to a file with the to_file() method.
  """

  def __init__(self):
    # treedata contains:
    #  dummy value, so that treedata[coords[missing]] == UNDEF
    #  |      ROOT_COORD == 1
    #  |      |     node ids in depth-first order
    #  |      |     |                            deleted nodes
    #  |      |     |                            |
    # [UNDEF, root, child1, child2, child3, ..., UNDEF, ...]
    self.treedata = array.array("Q")

    # coords contains:
    #
    #  pos (>0) in treedata of i-th node
    #  |    pos (>0) of root in treedata is ROOT_COORD == 1
    #  |    |       i-th node not contained in the tree, points to UNDEF
    #  |    |       |       deleted nodes: not changed, but now point to UNDEFs
    #  |    |       |       |
    # [pos, 1, ..., 0, ..., pos, ...]
    self.coords = array.array("Q")

    # subtree_sizes contains:
    #
    #  size of i-th subtree, including node itself
    #  |     rootID is handled as every other
    #  |     |                    i-th node not contained in the tree
    #  |     |                    |       deleted nodes: not changed (*)
    #  |     |                    |       |
    # [size, treesize, size, ..., 0, ..., size, ]
    # (*) not changed because the corresponding data is still in treedata
    self.subtree_sizes = None

    # parents contains:
    #
    #  parent of i-th node
    #  |       rootID: rootID itself, special case
    #  |       |                  i-th node not contained in the tree
    #  |       |                  |           deleted nodes: not changed (*)
    #  |       |                  |           |
    # [parent, rootID, size, ..., UNDEF, ..., size, ]
    # (*) not changed because the corresponding data is still in treedata
    self.parents = None

    self.root_id = None
    self.filename = None

  def _reset_data(self):
    """
    This method prepares for the reset operation.
    It does not change the associated filename, if any.
    """
    self.treedata = array.array("Q")
    self.coords = array.array("Q")
    self.subtree_sizes = None
    self.parents = None
    self.root_id = None

  UNDEF = sys.maxsize

  def _compute_parents(self, generator):
    """
    Copy the parents ID from the generator, after some checks;
    parent IDs can still be invalid in two ways:
    - parent_ID < 0 or parent_ID > max_node_ID
    - parent_ID is a "missing" node
    """
    logger.info("Constructing temporary parents table...")
    self.parents = array.array("Q")
    assert (self.root_id is None)
    for elem, parent in generator:
      if elem < 0:
        raise error.ConstructionError( \
          f"The node IDs must be >= 0, found: {elem}")
      if parent < 0:
        raise error.ConstructionError( \
          f"The node IDs must be >= 0, found: {parent}")
      if elem == self.root_id:
        raise error.ConstructionError( \
          f"Node {elem} had already been added as root, cannot " + \
          f"add it again with parent {parent}")
      n_missing = elem + 1 - len(self.parents)
      if n_missing > 0:
        for i in range(n_missing):
          self.parents.append(Tree.UNDEF)
      elif self.parents[elem] != Tree.UNDEF:
        raise error.ConstructionError( \
          f"Node '{elem}' had already been added with parent " + \
          f"'{self.parents[elem]}', cannot add it again with " + \
          f"parent {parent}")
      if elem == parent:
        if self.root_id is None:
          self.root_id = elem
        else:
          raise error.ConstructionError( \
            f"The tree already has a root node {self.root_id}, " + \
            f"cannot add a second root node {elem}")
      self.parents[elem] = parent
    if self.root_id is None:
      raise error.ConstructionError( \
        "The tree does not have any root node")

  def max_node_id(self) -> int:
    """
    Return the maximum node ID in the tree
    (after __compute_parents has been called).
    """
    assert (self.parents is not None)
    return len(self.parents) - 1

  def _validate_parents(self):
    logger.info("Validating the parents table data...")
    for elem, parent in tqdm(enumerate(self.parents), \
                             total=self.max_node_id()+1):
      if parent == Tree.UNDEF or parent == elem:
        continue
      if parent >= len(self.parents):
        raise error.ConstructionError(\
          f"The node '{elem}' has parent '{parent}', "+\
          "which is not in the tree")
      grandparent = self.parents[parent]
      if (grandparent == Tree.UNDEF):
        raise error.ConstructionError(\
          f"The node '{parent}' has parent '{grandparent}', "+\
          "which is not in the tree")

  def _compute_subtree_sizes_partial(self, start, end, max_node_id, undef,
                                     parents_array_readonly):
    subtree_sizes = array.array("Q", [0] * (max_node_id + 1))
    for elem in range(start, end):
      parent = parents_array_readonly[elem]
      if parent == undef:
        continue
      subtree_sizes[elem] += 1
      while parent != elem:
        subtree_sizes[parent] += 1
        grandparent = parents_array_readonly[parent]
        elem = parent
        parent = grandparent
    return subtree_sizes

  def _parallel_compute_subtree_sizes(self, n_processes):
    logger.info("Constructing subtree sizes table "+\
        f"using {n_processes} processes...")
    self.subtree_sizes = array.array("Q", [0] * (self.max_node_id() + 1))
    results = []
    with Pool(n_processes) as pool:
      for i in range(n_processes):
        start = i * (self.max_node_id()+1) // n_processes
        end = (i + 1) * (self.max_node_id()+1) // n_processes
        logger.info(f"Process {i} computes subtree sizes"+\
            f" for nodes {start} to {end}...")
        results.append(pool.apply_async(
          self._compute_subtree_sizes_partial,
          (start, end, self.max_node_id(), Tree.UNDEF, self.parents)))
      pool.close()
      pool.join()
    for i in range(self.max_node_id() + 1):
      self.subtree_sizes[i] = sum([r.get()[i] for r in results])

  def _compute_subtree_sizes(self):
    logger.info("Constructing subtree sizes table...")
    self.subtree_sizes = array.array('Q', [0] * (self.max_node_id()+1))
    for elem, parent in tqdm(enumerate(self.parents), \
                             total=self.max_node_id()+1):
      if parent == Tree.UNDEF:
        continue
      self.subtree_sizes[elem] += 1
      while parent != elem:
        self.subtree_sizes[parent] += 1
        grandparent = self.parents[parent]
        elem = parent
        parent = grandparent

  def get_treesize(self) -> int:
    """
    Returns the number of nodes in the tree.
    """
    assert self.subtree_sizes is not None
    return self.subtree_sizes[self.root_id]

  ROOT_COORD=1

  def _compute_treedata_and_coords(self):
    self.treedata = array.array("Q", [Tree.UNDEF] * (self.get_treesize() + 1))
    self.coords = array.array("Q", [0] * (self.max_node_id() + 1))
    self.treedata[self.ROOT_COORD] = self.root_id
    self.coords[self.root_id] = self.ROOT_COORD
    logger.info("Computing depth-first tree traversal order...")
    for elem in tqdm(range(self.max_node_id() + 1)):
      if elem == self.root_id:
        continue
      if self.parents[elem] == Tree.UNDEF:
        continue
      stack = []
      while elem != self.root_id and not self.coords[elem]:
        stack.append(elem)
        elem = self.parents[elem]
      while stack:
        elem = stack.pop()
        pos = self.coords[self.parents[elem]] + 1
        self.coords[elem] = pos
        self.treedata[pos] = elem
        self.coords[self.parents[elem]] += self.subtree_sizes[elem]
    logger.info("Finalize index of nodes positions in depth-first traversal...")
    for elem in tqdm(range(self.max_node_id() + 1)):
      if self.parents[elem] == Tree.UNDEF:
        continue
      self.coords[elem] -= (self.subtree_sizes[elem] - 1)

  @classmethod
  def construct(cls, generator: Iterator[Tuple[int, int]], n_processes: int = 1):
    """
    Construct a tree from a generator that yields tuples of the form
    (node, parent).
    """
    self = cls()
    self._compute_parents(generator)
    self._validate_parents()
    if n_processes > 1:
      self._parallel_compute_subtree_sizes(n_processes)
    else:
      self._compute_subtree_sizes()
    self._compute_treedata_and_coords()
    logger.success("Tree data structure constructed")
    return self

  @classmethod
  def construct_from_tabular(cls, filename: Union[str, Path],
                             separator: str = "\t", elem_field_num: int = 0,
                             parent_field_num: int = 1, n_processes: int = 1):
    """
    Construct a tree from a tabular file.
    """
    generator = ids_from_tabular_file.element_parent_ids(filename, separator,
        elem_field_num, parent_field_num)
    return cls.construct(generator, n_processes)

  @classmethod
  def construct_from_ncbi_dump(cls, filename: Union[str, Path],
                               n_processes: int = 1):
    """
    Constructs a tree from a NCBI taxonomy dump nodes file.
    """
    generator = ids_from_tabular_file.element_parent_ids(filename,
        ncbi_preset=True)
    return cls.construct(generator, n_processes)

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
      self.subtree_sizes = array.array("Q")
      self.subtree_sizes.fromfile(f, idxsize)
      self.coords.fromfile(f, idxsize)
      self.treedata.fromfile(f, nelems)
      self.parents = array.array("Q")
      self.parents.fromfile(f, nparents)
      self.root_id = self.treedata[1]
    logger.debug(f"Tree loaded from file \"{filename}\"")
    self.filename = filename
    return self

  def _check_node_number(self, node):
    if node < 0 or node > len(self.coords) - 1:
      raise error.NodeNotFoundError(f"Node ID '{node}' does not exist.")

  def get_parent(self, node: int) -> int:
    """
    Returns the parent ID of the given node.
    """
    self._check_node_number(node)
    return self.parents[node]

  def set_filename(self, filename: Union[str, Path]):
    """
    Sets the filename of the tree.

    The filename is used to compute the name of the files where
    attribute values are stored.

    The filename is automatically set when the tree is loaded from a file
    or saved to a file.
    """
    self.filename = Path(filename)

  def _check_filename_set(self):
    if self.filename is None:
      raise error.FilenameNotSetError("The tree filename is not set")

