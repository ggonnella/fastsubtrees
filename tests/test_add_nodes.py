import pytest
from fastsubtrees.ids_modules.ids_from_tabular_file import element_parent_ids
from fastsubtrees import Tree, error

def test_add_subtree_small_tree(testdata, results_add_subtree_small_subtree_1):
  construction_infname = testdata('small_tree.tsv')
  construction_generator = element_parent_ids(construction_infname)
  tree = Tree.construct(construction_generator)
  add_infname = testdata('small_tree_add_subtree.tsv')
  add_generator = element_parent_ids(add_infname)
  tree.add_nodes(add_generator)
  subtree_ids = tree.subtree_ids(1)
  assert subtree_ids == results_add_subtree_small_subtree_1

def test_add_subtree_medium_tree(testdata,
                                 results_add_subtree_medium_subtree_46):
  construction_infname = testdata('medium_tree.tsv')
  construction_generator = element_parent_ids(construction_infname)
  tree = Tree.construct(construction_generator)
  add_infname = testdata('medium_tree_add_subtree.tsv')
  add_generator = element_parent_ids(add_infname)
  tree.add_nodes(add_generator)
  subtree_ids = tree.subtree_ids(46)
  assert subtree_ids == results_add_subtree_medium_subtree_46

def test_add_subtree_err_repeated_node_ids(testdata):
  construction_infname = testdata('small_tree.tsv')
  construction_generator = element_parent_ids(construction_infname)
  tree = Tree.construct(construction_generator)
  add_infname = testdata('add_subtree_repeated_nodes.tsv')
  add_generator = element_parent_ids(add_infname)
  with pytest.raises(error.ConstructionError):
    tree.add_nodes(add_generator)

def test_add_subtree_err_parent_not_exists(testdata):
  construction_infname = testdata('small_tree.tsv')
  construction_generator = element_parent_ids(construction_infname)
  tree = Tree.construct(construction_generator)
  add_infname = testdata('add_subtree_parent_not_exist.tsv')
  add_generator = element_parent_ids(add_infname)
  with pytest.raises(error.ConstructionError):
    tree.add_nodes(add_generator)

def test_add_subtree_err_node0(testdata):
  construction_infname = testdata('small_tree.tsv')
  construction_generator = element_parent_ids(construction_infname)
  tree = Tree.construct(construction_generator)
  add_infname = testdata('construction_node0.tsv')
  add_generator = element_parent_ids(add_infname)
  with pytest.raises(error.ConstructionError):
    tree.add_nodes(add_generator)

def test_add_subtree_err_prev_deleted(testdata):
  construction_infname = testdata('small_tree.tsv')
  construction_generator = element_parent_ids(construction_infname)
  tree = Tree.construct(construction_generator)
  tree.delete_subtree(3)
  add_infname = testdata('add_already_deleted_node.tsv')
  add_generator = element_parent_ids(add_infname)
  with pytest.raises(error.DeletedNodeError):
    tree.add_nodes(add_generator)
