from fastsubtrees.get_element_parent_tsv import getElementParentIdFromTSV
from fastsubtrees import Tree
from pathlib import Path
from pytesting.reference_results import *

class TestClass:
    def test_fastsubtrees_construct_smalltree(self):
        elemparentid = getElementParentIdFromTSV('./testdata/small_tree.tsv')
        generator = elemparentid.getElementParentTSV()
        tree = Tree.construct(generator)
        outfname = Path('./pytesting/small_tree.tree')
        tree.to_file(outfname)
        new_tree = Tree.from_file('./pytesting/small_tree.tree')
        subtree_ids = new_tree.subtree_ids(int(1))
        test_tree = Tree.from_file('./testdata/small_tree.tree')
        test_subtree_ids = test_tree.subtree_ids(int(1))
        assert subtree_ids == test_subtree_ids

    def test_fastsubtrees_construct_middletree(self):
        elemparentid = getElementParentIdFromTSV('./testdata/middle_tree.tsv')
        generator = elemparentid.getElementParentTSV()
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

