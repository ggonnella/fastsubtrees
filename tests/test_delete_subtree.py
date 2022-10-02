import pytest
from fastsubtrees.ids_modules.ids_from_tabular_file import element_parent_ids
from fastsubtrees import Tree, error

def test_delete_node_small_tree(testdata,
                                results_delete_subtree_small_tree_id_1):
  construction_infname = testdata('small_tree.tsv')
  construction_generator = element_parent_ids(construction_infname)
  tree = Tree.construct(construction_generator)
  tree.delete_node(3)
  subtree_ids = tree.subtree_ids(1)
  assert subtree_ids == results_delete_subtree_small_tree_id_1

def test_delete_node_medium_tree(testdata,
                                 results_delete_subtree_medium_tree_id_78):
  construction_infname = testdata('medium_tree.tsv')
  construction_generator = element_parent_ids(construction_infname)
  tree = Tree.construct(construction_generator)
  tree.delete_node(78)
  subtree_ids = tree.subtree_ids(46)
  assert subtree_ids == results_delete_subtree_medium_tree_id_78

def test_delete_node_err_not_exist(testdata):
  construction_infname = testdata('small_tree.tsv')
  construction_generator = element_parent_ids(construction_infname)
  tree = Tree.construct(construction_generator)
  with pytest.raises(error.NodeNotFoundError):
    tree.delete_node(99)
