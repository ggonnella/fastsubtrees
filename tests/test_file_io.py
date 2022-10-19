import pytest
from fastsubtrees.ids_modules.ids_from_tabular_file import element_parent_ids
from fastsubtrees import Tree

def test_save_reload_small(testdata, testout):
  infname = testdata('small_tree.tsv')
  generator = element_parent_ids(infname)
  constructed_tree = Tree.construct(generator)
  constructed_subtree_ids = constructed_tree.subtree_ids(1)
  outfname = testout('small_tree.tree')
  constructed_tree.to_file(outfname)
  reloaded_tree = Tree.from_file(outfname)
  reloaded_subtree_ids = reloaded_tree.subtree_ids(1)
  assert constructed_subtree_ids == reloaded_subtree_ids

def test_save_reload_medium(testdata, testout):
  infname = testdata('medium_tree.tsv')
  generator = element_parent_ids(infname)
  constructed_tree = Tree.construct(generator)
  constructed_subtree_ids = constructed_tree.subtree_ids(1)
  outfname = testout('medium_tree.tree')
  constructed_tree.to_file(outfname)
  reloaded_tree = Tree.from_file(outfname)
  reloaded_subtree_ids = reloaded_tree.subtree_ids(1)
  assert constructed_subtree_ids == reloaded_subtree_ids

def test_err_nofile():
  with pytest.raises(FileNotFoundError):
    Tree.from_file('no_such_file.tree')
