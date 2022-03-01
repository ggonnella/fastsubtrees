"""
Computation of the information necessary for the subtree query
"""

import struct
import array
import sys
from fastsubtrees import logger, tqdm

class Tree():

    def __init__(self):
        self.subtree_sizes = array.array("Q")
        self.coords = array.array("Q")
        self.treedata = array.array("Q")
        self.parents = array.array("Q")
        self.root_id = None
        self.MAX_SIZE = sys.maxsize

    @staticmethod
    def __from_csv(filename, separator, elem_field_num, parent_field_num):
        logger.info(f"Reading data from file \"{filename}\" ...")
        with open(filename) as f:
            for line in tqdm(f):
                fields = line.rstrip().split(separator)
                elem = int(fields[elem_field_num])
                parent = int(fields[parent_field_num])
                yield elem, parent

    @staticmethod
    def __compute_parents(self, generator):
        results = array.array("Q")
        for elem, parent in generator:
            if elem <= 0:
                raise fastsubtrees.Error(f"The node IDs must be > 0, found: {elem}")
            if parent <= 0:
                raise fastsubtrees.Error(f"The node IDs must be > 0, found: {parent}")
            n_missing = elem + 1 - len(results)
            if n_missing > 0:
                for i in range(n_missing):
                    results.append(self.MAX_SIZE)
            if parent != elem:
                results[elem] = parent
            else:
                root_id = elem
        return results, root_id

    @staticmethod
    def __compute_subtree_sizes(self, parents):
        results = array.array('Q', [0] * len(parents))
        for parent in tqdm(parents):
            elem = parent
            while elem != self.MAX_SIZE:
                results[elem] += 1
                elem = parents[elem]
        return results

    @staticmethod
    def __compute_treedata(self, parents, subtree_sizes, root_id):
        treesize = subtree_sizes[root_id] + 1
        treedata = array.array("Q", [0] * (treesize + 1))
        coords = array.array("Q", [0] * len(parents))
        treedata[1] = root_id
        coords[root_id] = 1
        for i in tqdm(range(len(parents))):
            if parents[i] != self.MAX_SIZE:
                path = [i]
                parent = parents[i]
                while parent != root_id:
                    path.append(parent)
                    parent = parents[parent]
                for node in reversed(path):
                    if not coords[node]:
                        pos = coords[parents[node]] + 1
                        while True:
                            treedatanode = treedata[pos]
                            if treedatanode == 0:
                                break
                            else:
                                pos += (subtree_sizes[treedatanode] + 1)
                        coords[node] = pos
                        treedata[pos] = node
        return treedata, coords

    @classmethod
    def construct(cls, generator):
        self = cls()
        logger.info("Constructing temporary parents table...")
        self.parents, self.root_id = cls.__compute_parents(self, generator)
        logger.info("Constructing subtree sizes table...")
        self.subtree_sizes = cls.__compute_subtree_sizes(self, self.parents)
        logger.info("Constructing tree data and index...")
        self.treedata, self.coords = \
            cls.__compute_treedata(self, self.parents, self.subtree_sizes, self.root_id)
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
        return self.treedata[pos:pos + subtree_size + 1], pos, subtree_size, subtree_parents

    def subtree_ids(self, subtree_root):
        subtree_data, pos, subtree_size = self.query_subtree(subtree_root)
        return subtree_data
