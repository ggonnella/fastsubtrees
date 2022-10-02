import pytest
from fastsubtrees.ids_modules.ids_from_tabular_file import element_parent_ids
from fastsubtrees import Tree, error

def test_query_small_tree(testdata, results_query_small_tree_id_1,
                          results_query_small_tree_id_8):
  infname = testdata('small_tree.tsv')
  generator = element_parent_ids(infname)
  tree = Tree.construct(generator)
  subtree_1_ids = tree.subtree_ids(1)
  assert subtree_1_ids == results_query_small_tree_id_1
  subtree_8_ids = tree.subtree_ids(8)
  assert subtree_8_ids == results_query_small_tree_id_8

def test_query_medium_tree(testdata, results_query_medium_tree_id_1,
                           results_query_medium_tree_id_8,
                           results_query_medium_tree_id_566):
  infname = testdata('medium_tree.tsv')
  generator = element_parent_ids(infname)
  tree = Tree.construct(generator)
  subtree_1_ids = tree.subtree_ids(1)
  assert subtree_1_ids == results_query_medium_tree_id_1
  subtree_8_ids = tree.subtree_ids(8)
  assert subtree_8_ids == results_query_medium_tree_id_8
  subtree_566_ids = tree.subtree_ids(566)
  assert subtree_566_ids == results_query_medium_tree_id_566

def test_query_node_not_exist(testdata):
  infname = testdata('small_tree.tsv')
  generator = element_parent_ids(infname)
  tree = Tree.construct(generator)
  with pytest.raises(error.NodeNotFoundError):
      tree.subtree_ids(87)
