import pytest

from fastsubtrees.data_source_modules.get_element_parent_tsv \
    import ElementParentIdGenerator
from fastsubtrees import Tree, error
from pathlib import Path
from tests.reference_results import *
import os

class TestClass:
    def test_fastsubtrees_construct_smalltree(self):
        elemparentid = ElementParentIdGenerator('./tests/testdata/small_tree.tsv')
        generator = elemparentid.get_element_parent_id()
        tree = Tree.construct(generator)
        outfname = Path('./tests/small_tree.tree')
        tree.to_file(outfname)
        new_tree = Tree.from_file('./tests/small_tree.tree')
        subtree_ids = new_tree.subtree_ids(int(1))
        test_tree = Tree.from_file('./tests/testdata/small_tree.tree')
        test_subtree_ids = test_tree.subtree_ids(int(1))
        assert subtree_ids == test_subtree_ids

    def test_fastsubtrees_construct_middletree(self):
        elemparentid = ElementParentIdGenerator('./tests/testdata/middle_tree.tsv')
        generator = elemparentid.get_element_parent_id()
        tree = Tree.construct(generator)
        outfname = Path('./tests/middle_tree.tree')
        tree.to_file(outfname)
        new_tree = Tree.from_file('./tests/middle_tree.tree')
        subtree_ids = new_tree.subtree_ids(int(1))
        test_tree = Tree.from_file('./tests/testdata/middle_tree.tree')
        test_subtree_ids = test_tree.subtree_ids(int(1))
        assert subtree_ids == test_subtree_ids

    def test_construction_with_node_0(self):
        elemparentid = ElementParentIdGenerator('./tests/testdata/construction_node0.tsv')
        generator = elemparentid.get_element_parent_id()
        with pytest.raises(error.ConstructionError):
            Tree.construct(generator)

    def test_construction_repeated_node_ids(self):
        elemparentid = ElementParentIdGenerator('./tests/testdata/repeated_nodes.tsv')
        generator = elemparentid.get_element_parent_id()
        with pytest.raises(error.ConstructionError):
            Tree.construct(generator)

    def test_construction_no_root_node(self):
        elemparentid = ElementParentIdGenerator('./tests/testdata/no_root_node.tsv')
        generator = elemparentid.get_element_parent_id()
        with pytest.raises(error.ConstructionError):
            Tree.construct(generator)

    def test_construction_multiple_root_nodes(self):
        elemparentid = ElementParentIdGenerator('./tests/testdata/multiple_root_nodes.tsv')
        generator = elemparentid.get_element_parent_id()
        with pytest.raises(error.ConstructionError):
            Tree.construct(generator)

    def test_construction_parent_not_exist(self):
        elemparentid = ElementParentIdGenerator('./tests/testdata/parent_not_exist.tsv')
        generator = elemparentid.get_element_parent_id()
        with pytest.raises(error.ConstructionError):
            Tree.construct(generator)

    def test_fastsubtrees_query_smalltree(self):
        # use subtree_ids 1, 8 and change the id in variable results_query_smalltree_id_*
        tree = Tree.from_file('./tests/small_tree.tree')
        subtree_ids = tree.subtree_ids(1)
        assert subtree_ids == results_query_smalltree_id_1

    def test_fastsubtrees_query_middletree(self):
        # use subtree_ids 1, 8, 566 and change the id in variable results_query_middletree_id_*
        tree = Tree.from_file('./tests/middle_tree.tree')
        subtree_ids = tree.subtree_ids(1)
        assert subtree_ids == results_query_middletree_id_1

    def test_query_node_not_exist(self):
        tree = Tree.from_file('./tests/small_tree.tree')
        with pytest.raises(error.NodeNotFoundError):
            tree.subtree_ids(87)

    def test_fastsubtrees_add_subtree_smalltree(self):
        create_tree = Tree.construct_from_csv('./tests/testdata/small_tree.tsv', '\t', 0, 1)
        outfname = Path('./tests/small_tree').with_suffix(".tree")
        create_tree.to_file(outfname)
        tree = Tree.from_file('./tests/small_tree.tree')
        elemparentid = ElementParentIdGenerator('./tests/testdata/smalltree_add_subtree.tsv')
        generator = elemparentid.get_element_parent_id()
        tree.add_subtree(generator)
        tree.to_file('./tests/small_tree.tree')
        new_tree = Tree.from_file('./tests/small_tree.tree')
        subtree_ids = new_tree.subtree_ids(1)
        os.remove('./tests/small_tree.tree')
        assert subtree_ids == results_add_subtree_smalltree_id_1


    def test_fastsubtrees_add_subtree_middletree(self):
        create_tree = Tree.construct_from_csv('./tests/testdata/middle_tree.tsv', '\t', 0, 1)
        outfname = Path('./tests/middle_tree').with_suffix(".tree")
        create_tree.to_file(outfname)
        tree = Tree.from_file('./tests/middle_tree.tree')
        elemparentid = ElementParentIdGenerator('./tests/testdata/middletree_add_subtree.tsv')
        generator = elemparentid.get_element_parent_id()
        tree.add_subtree(generator)
        tree.to_file('./tests/middle_tree.tree')
        new_tree = Tree.from_file('./tests/middle_tree.tree')
        subtree_ids = new_tree.subtree_ids(46)
        os.remove('./tests/middle_tree.tree')
        assert subtree_ids == results_add_subtree_middletree_id_46

    def test_add_subtree_repeated_node_ids(self):
        create_tree = Tree.construct_from_csv('./tests/testdata/small_tree.tsv', '\t', 0, 1)
        outfname = Path('./tests/small_tree_repeated_node_id').with_suffix(".tree")
        create_tree.to_file(outfname)
        tree = Tree.from_file('./tests/small_tree_repeated_node_id.tree')
        elemparentid = ElementParentIdGenerator('./tests/testdata/add_subtree_repeated_nodes.tsv')
        generator = elemparentid.get_element_parent_id()
        with pytest.raises(error.ConstructionError):
            tree.add_subtree(generator)
            os.remove('./tests/small_tree_repeated_node_id.tree')

    def test_add_subtree_parent_not_exist(self):
        create_tree = Tree.construct_from_csv('./tests/testdata/small_tree.tsv', '\t', 0, 1)
        outfname = Path('./tests/small_tree_repeated_node_id').with_suffix(".tree")
        create_tree.to_file(outfname)
        tree = Tree.from_file('./tests/small_tree_repeated_node_id.tree')
        elemparentid = ElementParentIdGenerator('./tests/testdata/add_subtree_parent_not_exist.tsv')
        generator = elemparentid.get_element_parent_id()
        with pytest.raises(error.ConstructionError):
            tree.add_subtree(generator)
            os.remove('./tests/small_tree_repeated_node_id.tree')

    def test_add_subtree_node0(self):
        create_tree = Tree.construct_from_csv('./tests/testdata/small_tree.tsv', '\t', 0, 1)
        outfname = Path('./tests/small_tree_repeated_node_id').with_suffix(".tree")
        create_tree.to_file(outfname)
        tree = Tree.from_file('./tests/small_tree_repeated_node_id.tree')
        elemparentid = ElementParentIdGenerator('./tests/testdata/construction_node0.tsv')
        generator = elemparentid.get_element_parent_id()
        with pytest.raises(error.ConstructionError):
            tree.add_subtree(generator)
            os.remove('./tests/small_tree_repeated_node_id.tree')

    def test_add_already_deleted_node(self):
        create_tree = Tree.construct_from_csv('./tests/testdata/small_tree.tsv', '\t', 0, 1)
        outfname = Path('./tests/add_already_deleted_node').with_suffix(".tree")
        create_tree.to_file(outfname)
        tree = Tree.from_file('./tests/git.tree')
        tree.delete_node(3)
        new_tree = Tree.from_file('./tests/add_already_deleted_node.tree')
        elemparentid = ElementParentIdGenerator('./tests/testdata/add_already_deleted_node.tsv')
        generator = elemparentid.get_element_parent_id()
        with pytest.raises(error.DeletedNodeError):
            new_tree.add_subtree(generator)
            os.remove('./tests/add_already_deleted_node.tree')


    def test_fastsubtrees_delete_node_smalltree(self):
        create_tree = Tree.construct_from_csv('./tests/testdata/small_tree.tsv', '\t', 0, 1)
        outfname = Path('./tests/small_tree').with_suffix(".tree")
        create_tree.to_file(outfname)
        tree = Tree.from_file('./tests/small_tree.tree')
        tree.delete_node(3)
        tree.to_file('./tests/small_tree.tree')
        new_tree = Tree.from_file('./tests/small_tree.tree')
        subtree_ids = new_tree.subtree_ids(1)
        os.remove('./tests/small_tree.tree')
        assert subtree_ids == results_delete_subtree_smalltree_id_1


    def test_fastsubtrees_delete_node_middletree(self):
        create_tree = Tree.construct_from_csv('./tests/testdata/middle_tree.tsv', '\t', 0, 1)
        outfname = Path('./tests/middle_tree').with_suffix(".tree")
        create_tree.to_file(outfname)
        tree = Tree.from_file('./tests/middle_tree.tree')
        tree.delete_node(78)
        tree.to_file('./tests/middle_tree.tree')
        new_tree = Tree.from_file('./tests/middle_tree.tree')
        subtree_ids = new_tree.subtree_ids(46)
        os.remove('./tests/middle_tree.tree')
        assert subtree_ids == results_delete_subtree_middletree_id_78

    def test_delete_node_not_exist(self):
        create_tree = Tree.construct_from_csv('./tests/testdata/small_tree.tsv', '\t', 0, 1)
        outfname = Path('./tests/small_tree').with_suffix(".tree")
        create_tree.to_file(outfname)
        tree = Tree.from_file('./tests/small_tree.tree')
        with pytest.raises(error.NodeNotFoundError):
            tree.delete_node(99)
            os.remove('./tests/small_tree.tree')
