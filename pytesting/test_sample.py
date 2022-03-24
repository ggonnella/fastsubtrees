from fastsubtrees.get_element_parent_tsv import ElementParentIdGenerator
from fastsubtrees import Tree
from pathlib import Path
from pytesting.reference_results import *
import os

class TestClass:
    def test_fastsubtrees_construct_smalltree(self):
        elemparentid = ElementParentIdGenerator('./testdata/small_tree.tsv')
        generator = elemparentid.get_element_parent_id()
        tree = Tree.construct(generator)
        outfname = Path('./pytesting/small_tree.tree')
        tree.to_file(outfname)
        new_tree = Tree.from_file('./pytesting/small_tree.tree')
        subtree_ids = new_tree.subtree_ids(int(1))
        test_tree = Tree.from_file('./testdata/small_tree.tree')
        test_subtree_ids = test_tree.subtree_ids(int(1))
        assert subtree_ids == test_subtree_ids

    def test_fastsubtrees_construct_middletree(self):
        elemparentid = ElementParentIdGenerator('./testdata/middle_tree.tsv')
        generator = elemparentid.get_element_parent_id()
        tree = Tree.construct(generator)
        outfname = Path('./pytesting/middle_tree.tree')
        tree.to_file(outfname)
        new_tree = Tree.from_file('./pytesting/middle_tree.tree')
        subtree_ids = new_tree.subtree_ids(int(1))
        test_tree = Tree.from_file('./testdata/middle_tree.tree')
        test_subtree_ids = test_tree.subtree_ids(int(1))
        assert subtree_ids == test_subtree_ids


    def test_fastsubtrees_query_smalltree(self):
        # use subtree_ids 1, 8 and change the id in variable results_query_smalltree_id_*
        tree = Tree.from_file('./pytesting/small_tree.tree')
        subtree_ids = tree.subtree_ids(1)
        assert subtree_ids == results_query_smalltree_id_1


    def test_fastsubtrees_query_middletree(self):
        # use subtree_ids 1, 8, 566 and change the id in variable results_query_middletree_id_*
        tree = Tree.from_file('./pytesting/middle_tree.tree')
        subtree_ids = tree.subtree_ids(1)
        assert subtree_ids == results_query_middletree_id_1


    def test_fastsubtrees_add_subtree_smalltree(self):
        create_tree = Tree.construct_from_csv('./testdata/small_tree.tsv', '\t', 0, 1)
        outfname = Path('./pytesting/small_tree').with_suffix(".tree")
        create_tree.to_file(outfname)
        tree = Tree.from_file('./pytesting/small_tree.tree')
        elemparentid = ElementParentIdGenerator('./testdata/smalltree_add_subtree.tsv')
        generator = elemparentid.get_element_parent_id()
        tree.add_subtree(generator)
        tree.to_file('./pytesting/small_tree.tree')
        new_tree = Tree.from_file('./pytesting/small_tree.tree')
        subtree_ids = new_tree.subtree_ids(1)
        os.remove('./pytesting/small_tree.tree')
        assert subtree_ids == results_add_subtree_smalltree_id_1


    def test_fastsubtrees_add_subtree_middletree(self):
        create_tree = Tree.construct_from_csv('./testdata/middle_tree.tsv', '\t', 0, 1)
        outfname = Path('./pytesting/middle_tree').with_suffix(".tree")
        create_tree.to_file(outfname)
        tree = Tree.from_file('./pytesting/middle_tree.tree')
        elemparentid = ElementParentIdGenerator('./testdata/middletree_add_subtree.tsv')
        generator = elemparentid.get_element_parent_id()
        tree.add_subtree(generator)
        tree.to_file('./pytesting/middle_tree.tree')
        new_tree = Tree.from_file('./pytesting/middle_tree.tree')
        subtree_ids = new_tree.subtree_ids(46)
        os.remove('./pytesting/middle_tree.tree')
        assert subtree_ids == results_add_subtree_middletree_id_46


    def test_fastsubtrees_delete_node_smalltree(self):
        create_tree = Tree.construct_from_csv('./testdata/small_tree.tsv', '\t', 0, 1)
        outfname = Path('./pytesting/small_tree').with_suffix(".tree")
        create_tree.to_file(outfname)
        tree = Tree.from_file('./pytesting/small_tree.tree')
        tree.delete_node(3)
        tree.to_file('./pytesting/small_tree.tree')
        new_tree = Tree.from_file('./pytesting/small_tree.tree')
        subtree_ids = new_tree.subtree_ids(1)
        os.remove('./pytesting/small_tree.tree')
        assert subtree_ids == results_delete_subtree_smalltree_id_1


    def test_fastsubtrees_delete_node_middletree(self):
        create_tree = Tree.construct_from_csv('./testdata/middle_tree.tsv', '\t', 0, 1)
        outfname = Path('./pytesting/middle_tree').with_suffix(".tree")
        create_tree.to_file(outfname)
        tree = Tree.from_file('./pytesting/middle_tree.tree')
        tree.delete_node(78)
        tree.to_file('./pytesting/middle_tree.tree')
        new_tree = Tree.from_file('./pytesting/middle_tree.tree')
        subtree_ids = new_tree.subtree_ids(46)
        os.remove('./pytesting/middle_tree.tree')
        assert subtree_ids == results_delete_subtree_middletree_id_78