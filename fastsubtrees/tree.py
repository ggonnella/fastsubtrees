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

    @staticmethod
    def __from_csv(filename, separator, elem_field_num, parent_field_num):
        logger.info(f"Reading data from file \"{filename}\" ...")
        with open(filename) as f:
            for line in tqdm(f):
                fields = line.rstrip().split(separator)
                elem = int(fields[elem_field_num])
                parent = int(fields[parent_field_num])
                yield elem, parent

    def __compute_parents(self, generator):
        self.parents = array.array("Q")
        for elem, parent in generator:
            if elem <= 0:
                raise error.ConstructionError(\
                    f"The node IDs must be > 0, found: {elem}")
            if parent <= 0:
                raise error.ConstructionError(\
                    f"The node IDs must be > 0, found: {parent}")
            n_missing = elem + 1 - len(self.parents)
            if n_missing > 0:
                for i in range(n_missing):
                    self.parents.append(Tree.UNDEF)
            if parent != elem:
                self.parents[elem] = parent
            else:
                self.root_id = elem

    def __compute_subtree_sizes(self):
        self.subtree_sizes = array.array('Q', [0] * len(self.parents))
        for parent in tqdm(self.parents):
            elem = parent
            while elem != Tree.UNDEF:
                self.subtree_sizes[elem] += 1
                elem = self.parents[elem]

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
                            self.treedatanode = self.treedata[pos]
                            if self.treedatanode == 0:
                                break
                            else:
                                pos += (self.subtree_sizes[self.treedatanode] + 1)
                        self.coords[node] = pos
                        self.treedata[pos] = node

    @classmethod
    def construct(cls, generator):
        self = cls()
        logger.info("Constructing temporary parents table...")
        try:
            self.__compute_parents(generator)
        except UnboundLocalError:
            raise error.RootNotFoundError("Root does not exist for the given tree")
        logger.info("Constructing subtree sizes table...")
        try:
            self.__compute_subtree_sizes()
        except IndexError:
            raise error.ParentNotFoundError("The parent node does not exist for the given child node")
        logger.info("Constructing tree data and index...")
        try:
            self.__compute_treedata()
        except IndexError:
            raise error.MultipleRootNodeError("Cannot have multiple root nodes")
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
            f.write(struct.pack("QQQ", len(self.subtree_sizes), len(self.treedata), len(self.parents)))
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
            subtree_data, pos, subtree_size, subtree_parents = self.query_subtree(subtree_root)
        except ValueError:
            raise error.NodeNotFoundError(f"The node ID does not exist, found: {subtree_root}")
        new_subtree_ids = array.array("Q")
        for data in subtree_data:
            if data != Tree.UNDEF:
                new_subtree_ids.append(data)
        return new_subtree_ids

    def add_subtree(self, generator):
        for node_number, parent in generator:
            if node_number in self.treedata:
                raise error.NodeReplicationError('The node cannot have more than 1 parent')
            else:
                inspos = self.__prepare_node_insertion(node_number, parent)
                self.__get_coords(node_number, inspos, parent)
                self.__update_subtree_sizes(node_number)

    def __prepare_node_insertion(self, node_number, parent):
        try:
            inspos = self.coords[parent]+1
            self.treedata.insert(inspos, node_number)
            return inspos
        except IndexError:
            error.ParentNotFoundError('The parent node does not exist for the given child node')

    def __get_coords(self, node_number, inspos, parent):
        if node_number < len(self.coords):
            try:
                self.coords[node_number] = inspos
            except TypeError:
                raise error.NodeNotFoundError(f'The node ID does not exist')
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

    def delete_node(self, node_number):
        elements = self.subtree_ids(node_number)
        coord = self.coords[node_number]
        subtree_size = self.subtree_sizes[node_number]
        for i in range(subtree_size+1):
            self.treedata[coord+i] = Tree.UNDEF
        for element in elements:
            self.coords[element] = Tree.UNDEF
