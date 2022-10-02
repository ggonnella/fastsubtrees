import pytest
from fastsubtrees.ids_modules.ids_from_tabular_file import element_parent_ids
from fastsubtrees import Tree, error

def test_construction_small(testdata, prebuilt):
  infname = testdata('small_tree.tsv')
  generator = element_parent_ids(infname)
  constructed_tree = Tree.construct(generator)
  constructed_subtree_ids = constructed_tree.subtree_ids(1)
  prebuilt_tree = Tree.from_file(prebuilt('small_tree.tree'))
  prebuilt_subtree_ids = prebuilt_tree.subtree_ids(1)
  assert constructed_subtree_ids == prebuilt_subtree_ids

def test_construction_medium(testdata, prebuilt):
  infname = testdata('medium_tree.tsv')
  generator = element_parent_ids(infname)
  constructed_tree = Tree.construct(generator)
  constructed_subtree_ids = constructed_tree.subtree_ids(1)
  prebuilt_tree = Tree.from_file(prebuilt('medium_tree.tree'))
  prebuilt_subtree_ids = prebuilt_tree.subtree_ids(1)
  assert constructed_subtree_ids == prebuilt_subtree_ids

def test_construction_err_node0(testdata):
  infname = testdata('construction_node0.tsv')
  generator = element_parent_ids(infname)
  with pytest.raises(error.ConstructionError):
    Tree.construct(generator)

def test_construction_err_repeated_ids(testdata):
  infname = testdata('repeated_nodes.tsv')
  generator = element_parent_ids(infname)
  with pytest.raises(error.ConstructionError):
    Tree.construct(generator)

def test_construction_err_no_root(testdata):
  infname = testdata('no_root_node.tsv')
  generator = element_parent_ids(infname)
  with pytest.raises(error.ConstructionError):
    Tree.construct(generator)

def test_construction_err_multiple_roots(testdata):
  infname = testdata('multiple_root_nodes.tsv')
  generator = element_parent_ids(infname)
  with pytest.raises(error.ConstructionError):
    Tree.construct(generator)

def test_construction_err_parent_not_exist(testdata):
  infname = testdata('parent_not_exist.tsv')
  generator = element_parent_ids(infname)
  with pytest.raises(error.ConstructionError):
    Tree.construct(generator)
