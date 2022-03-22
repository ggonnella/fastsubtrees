from array import array

from pytesting.generate_parent_element_id import ElementParentIdGenerator
from fastsubtrees import Tree
from pathlib import Path

class TestClass:
    def test_fastsubtrees_construct(self, subtree_id):
        # elemparentid = ElementParentIdGenerator('./pytesting/config.yaml')
        # generator = elemparentid.get_element_parent_id()
        # tree = Tree.construct(generator)
        # outfname = Path('./pytesting/nodes.tree')
        # tree.to_file(outfname)
        new_tree = Tree.from_file('./pytesting/nodes.tree')
        subtree_ids = new_tree.subtree_ids(int(subtree_id))
        test_tree = Tree.from_file('./data/nodes.tree')
        test_subtree_ids = test_tree.subtree_ids(int(subtree_id))
        assert subtree_ids == test_subtree_ids


    def test_fastsubtrees_query(self, subtree_id):
        tree = Tree.from_file('./data/nodes.tree')
        subtree_ids = tree.subtree_ids(int(subtree_id))
        assert subtree_ids == array('Q', [2242, 33003, 33004, 33005, 64091, 478009, 2597657])


    def test_fastsubtrees_add_subtree(self, parent, node_number):
        create_tree = Tree.construct_from_csv('./testdata/small_tree.tsv', '\t', 0, 1)
        outfname = Path('./pytesting/smalltree').with_suffix(".tree")
        create_tree.to_file(outfname)
        tree = Tree()
        tree.add_node('./pytesting/smalltree.tree', int(parent), int(node_number))
        new_tree = Tree.from_file('./pytesting/smalltree.tree')
        subtree_ids = new_tree.subtree_ids(1)
        assert subtree_ids == array('Q', [1, 2, 8, 6, 3, 7, 9, 4, 5])


    def test_fastsubtrees_delete_node(self, delete_node_number):
        tree = Tree()
        tree.delete_node('./pytesting/smalltree.tree', int(delete_node_number))
        new_tree = Tree.from_file('./pytesting/smalltree.tree')
        subtree_ids = new_tree.subtree_ids(1)
        assert subtree_ids == array('Q', [1, 2, 8, 3, 7, 9, 4, 5])
