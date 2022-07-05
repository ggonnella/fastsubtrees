import pytest

from fastsubtrees.ids_modules.ids_from_tabular_file import element_parent_ids
from fastsubtrees import Tree, error
from pathlib import Path
from tests.reference_results import *
import os

class TestClass:
    def test_fastsubtrees_construct_smalltree(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/small_tree.tsv')
        generator = element_parent_ids(filename)
        tree = Tree.construct(generator)
        outfname = os.path.join(dir, 'small_tree.tree')
        tree.to_file(outfname)
        new_tree = Tree.from_file(outfname)
        subtree_ids = new_tree.subtree_ids(int(1))
        test_tree = Tree.from_file(os.path.join(dir, 'testdata/small_tree.tree'))
        test_subtree_ids = test_tree.subtree_ids(int(1))
        os.remove(outfname)
        assert subtree_ids == test_subtree_ids

    def test_fastsubtrees_construct_middletree(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/middle_tree.tsv')
        generator = element_parent_ids(filename)
        tree = Tree.construct(generator)
        outfname = os.path.join(dir, 'middle_tree.tree')
        tree.to_file(outfname)
        new_tree = Tree.from_file(outfname)
        subtree_ids = new_tree.subtree_ids(int(1))
        test_tree = Tree.from_file(os.path.join(dir, 'testdata/middle_tree.tree'))
        test_subtree_ids = test_tree.subtree_ids(int(1))
        os.remove(outfname)
        assert subtree_ids == test_subtree_ids

    def test_construction_with_node_0(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/construction_node0.tsv')
        generator = element_parent_ids(filename)
        with pytest.raises(error.ConstructionError):
            Tree.construct(generator)

    def test_construction_repeated_node_ids(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/repeated_nodes.tsv')
        generator = element_parent_ids(filename)
        with pytest.raises(error.ConstructionError):
            Tree.construct(generator)

    def test_construction_no_root_node(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/no_root_node.tsv')
        generator = element_parent_ids(filename)
        with pytest.raises(error.ConstructionError):
            Tree.construct(generator)

    def test_construction_multiple_root_nodes(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/multiple_root_nodes.tsv')
        generator = element_parent_ids(filename)
        with pytest.raises(error.ConstructionError):
            Tree.construct(generator)

    def test_construction_parent_not_exist(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/parent_not_exist.tsv')
        generator = element_parent_ids(filename)
        with pytest.raises(error.ConstructionError):
            Tree.construct(generator)

    def test_fastsubtrees_query_smalltree(self):
        # use subtree_ids 1, 8 and change the id in variable results_query_smalltree_id_*
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/small_tree.tsv')
        generator = element_parent_ids(filename)
        tree = Tree.construct(generator)
        outfname = os.path.join(dir, 'small_tree.tree')
        tree.to_file(outfname)
        tree = Tree.from_file(outfname)
        subtree_ids = tree.subtree_ids(1)
        assert subtree_ids == results_query_smalltree_id_1

    def test_fastsubtrees_query_middletree(self):
        # use subtree_ids 1, 8, 566 and change the id in variable results_query_middletree_id_*
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/middle_tree.tsv')
        generator = element_parent_ids(filename)
        tree = Tree.construct(generator)
        outfname = os.path.join(dir, 'middle_tree.tree')
        tree.to_file(outfname)
        tree = Tree.from_file(outfname)
        subtree_ids = tree.subtree_ids(1)
        assert subtree_ids == results_query_middletree_id_1

    def test_query_node_not_exist(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/small_tree.tsv')
        generator = element_parent_ids(filename)
        tree = Tree.construct(generator)
        outfname = os.path.join(dir, 'small_tree.tree')
        tree.to_file(outfname)
        tree = Tree.from_file(outfname)
        with pytest.raises(error.NodeNotFoundError):
            tree.subtree_ids(87)

    def test_fastsubtrees_add_subtree_smalltree(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/small_tree.tsv')
        create_tree = Tree.construct_from_csv(filename, '\t', 0, 1)
        outfname = os.path.join(dir, 'small_tree.tree')
        create_tree.to_file(outfname)
        tree = Tree.from_file(outfname)
        generator = element_parent_ids(os.path.join(dir, 'testdata/smalltree_add_subtree.tsv'))
        tree.add_subtree(generator)
        tree.to_file(outfname)
        new_tree = Tree.from_file(outfname)
        subtree_ids = new_tree.subtree_ids(1)
        os.remove(outfname)
        assert subtree_ids == results_add_subtree_smalltree_id_1

    def test_fastsubtrees_add_subtree_middletree(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/middle_tree.tsv')
        create_tree = Tree.construct_from_csv(filename, '\t', 0, 1)
        outfname = os.path.join(dir, 'middle_tree.tree')
        create_tree.to_file(outfname)
        tree = Tree.from_file(os.path.join(dir, 'middle_tree.tree'))
        generator = element_parent_ids(os.path.join(dir, 'testdata/middletree_add_subtree.tsv'))
        tree.add_subtree(generator)
        tree.to_file(outfname)
        new_tree = Tree.from_file(outfname)
        subtree_ids = new_tree.subtree_ids(46)
        os.remove(outfname)
        assert subtree_ids == results_add_subtree_middletree_id_46

    def test_add_subtree_repeated_node_ids(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/small_tree.tsv')
        create_tree = Tree.construct_from_csv(filename, '\t', 0, 1)
        outfname = os.path.join(dir, 'small_tree_repeated_node_id.tree')
        create_tree.to_file(outfname)
        tree = Tree.from_file(outfname)
        generator = element_parent_ids(os.path.join(dir, 'testdata/add_subtree_repeated_nodes.tsv'))
        with pytest.raises(error.ConstructionError):
            tree.add_subtree(generator)
            os.remove(outfname)

    def test_add_subtree_parent_not_exist(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/small_tree.tsv')
        create_tree = Tree.construct_from_csv(filename, '\t', 0, 1)
        outfname = os.path.join(dir, 'small_tree_parent_not_exist.tree')
        create_tree.to_file(outfname)
        tree = Tree.from_file(outfname)
        generator = element_parent_ids(os.path.join(dir, 'testdata/add_subtree_parent_not_exist.tsv'))
        with pytest.raises(error.ConstructionError):
            tree.add_subtree(generator)
            os.remove(outfname)

    def test_add_subtree_node0(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/small_tree.tsv')
        create_tree = Tree.construct_from_csv(filename, '\t', 0, 1)
        outfname = os.path.join(dir, 'small_tree_add_node0.tree')
        create_tree.to_file(outfname)
        tree = Tree.from_file(os.path.join(dir, 'small_tree_add_node0.tree'))
        generator = element_parent_ids(os.path.join(dir, 'testdata/construction_node0.tsv'))
        with pytest.raises(error.ConstructionError):
            tree.add_subtree(generator)
            os.remove(outfname)

    def test_add_already_deleted_node(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/small_tree.tsv')
        create_tree = Tree.construct_from_csv(filename, '\t', 0, 1)
        outfname = os.path.join(dir, 'add_already_deleted_node.tree')
        create_tree.to_file(outfname)
        tree = Tree.from_file(os.path.join(dir, 'add_already_deleted_node.tree'))
        tree.delete_node(3)
        tree.to_file(outfname)
        new_tree = Tree.from_file(outfname)
        generator = element_parent_ids(os.path.join(dir, 'testdata/add_already_deleted_node.tsv'))
        with pytest.raises(error.DeletedNodeError):
            new_tree.add_subtree(generator)
            os.remove(outfname)

    def test_fastsubtrees_delete_node_smalltree(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/small_tree.tsv')
        create_tree = Tree.construct_from_csv(filename, '\t', 0, 1)
        outfname = os.path.join(dir, 'small_tree.tree')
        create_tree.to_file(outfname)
        tree = Tree.from_file(os.path.join(dir, 'small_tree.tree'))
        tree.delete_node(3)
        tree.to_file(os.path.join(dir, 'small_tree.tree'))
        new_tree = Tree.from_file(os.path.join(dir, 'small_tree.tree'))
        subtree_ids = new_tree.subtree_ids(1)
        os.remove(os.path.join(dir, 'small_tree.tree'))
        assert subtree_ids == results_delete_subtree_smalltree_id_1

    def test_fastsubtrees_delete_node_middletree(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/middle_tree.tsv')
        create_tree = Tree.construct_from_csv(filename, '\t', 0, 1)
        outfname = os.path.join(dir, 'middle_tree.tree')
        create_tree.to_file(outfname)
        tree = Tree.from_file(os.path.join(dir, 'middle_tree.tree'))
        tree.delete_node(78)
        tree.to_file(os.path.join(dir, 'middle_tree.tree'))
        new_tree = Tree.from_file(os.path.join(dir, 'middle_tree.tree'))
        subtree_ids = new_tree.subtree_ids(46)
        os.remove(os.path.join(dir, 'middle_tree.tree'))
        assert subtree_ids == results_delete_subtree_middletree_id_78

    def test_delete_node_not_exist(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'testdata/small_tree.tsv')
        create_tree = Tree.construct_from_csv(filename, '\t', 0, 1)
        outfname = os.path.join(dir, 'small_tree.tree')
        create_tree.to_file(outfname)
        tree = Tree.from_file(os.path.join(dir, 'small_tree.tree'))
        with pytest.raises(error.NodeNotFoundError):
            tree.delete_node(99)
            os.remove(os.path.join(dir, 'small_tree.tree'))

