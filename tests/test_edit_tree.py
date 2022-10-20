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

def test_add_subtree_negative_parent(testdata):
  construction_infname = testdata('small_tree.tsv')
  construction_generator = element_parent_ids(construction_infname)
  tree = Tree.construct(construction_generator)
  add_infname = testdata('negative_parent.tsv')
  add_generator = element_parent_ids(add_infname)
  with pytest.raises(error.ConstructionError):
    tree.add_nodes(add_generator)

def test_add_subtree_negative_node(testdata):
  construction_infname = testdata('small_tree.tsv')
  construction_generator = element_parent_ids(construction_infname)
  tree = Tree.construct(construction_generator)
  add_infname = testdata('negative_node.tsv')
  add_generator = element_parent_ids(add_infname)
  with pytest.raises(error.ConstructionError):
    tree.add_nodes(add_generator)

def test_add_subtree_prev_deleted(testdata):
  construction_infname = testdata('small_tree.tsv')
  construction_generator = element_parent_ids(construction_infname)
  tree = Tree.construct(construction_generator)
  tree.delete_subtree(3)
  add_infname = testdata('add_already_deleted_node.tsv')
  add_generator = element_parent_ids(add_infname)
  tree.add_nodes(add_generator)

def test_delete_node_small_tree(testdata,
                                results_delete_subtree_small_tree_id_1):
  construction_infname = testdata('small_tree.tsv')
  construction_generator = element_parent_ids(construction_infname)
  tree = Tree.construct(construction_generator)
  tree.delete_subtree(3)
  subtree_ids = tree.subtree_ids(1)
  assert subtree_ids == results_delete_subtree_small_tree_id_1

def test_delete_node_medium_tree(testdata,
                                 results_delete_subtree_medium_tree_id_78):
  construction_infname = testdata('medium_tree.tsv')
  construction_generator = element_parent_ids(construction_infname)
  tree = Tree.construct(construction_generator)
  tree.delete_subtree(78)
  subtree_ids = tree.subtree_ids(46)
  assert subtree_ids == results_delete_subtree_medium_tree_id_78

def test_delete_node_err_not_exist(testdata):
  construction_infname = testdata('small_tree.tsv')
  construction_generator = element_parent_ids(construction_infname)
  tree = Tree.construct(construction_generator)
  with pytest.raises(error.NodeNotFoundError):
    tree.delete_subtree(99)

def assert_identical_subtrees(tree1, tree2):
  for node in set(tree1.subtree_ids(tree1.root_id)):
    assert set(tree1.subtree_ids(node)) == set(tree2.subtree_ids(node))

def assert_identical_attributes(tree1, tree2):
  attrnames1 = set(tree1.list_attributes())
  attrnames2 = set(tree2.list_attributes())
  assert attrnames1 == attrnames2
  for attrname in attrnames1:
    attrvalues1 = tree1.load_attribute_values(attrname)
    attrvalues2 = tree2.load_attribute_values(attrname)
    assert attrvalues1 == attrvalues2

def test_update_tree(testdata, testout):
  tree = Tree.construct_from_tabular(testdata('small_tree.tsv'))
  tree.to_file(testout('small_tree.tree'))
  tree.destroy_all_attributes()
  tree.create_attribute_from_tabular("attrX", testdata("small_tree_attrX.tsv"))
  tree.create_attribute_from_tabular("attrX2", testdata("small_tree_attrX.tsv"))
  tree.update_from_tabular(testdata('small_tree.update.tsv'))
  with open(testdata("small_tree.updated.query.root.parents.results")) as f:
    expected_results = \
        [int(line.split("\t")[0]) for line in f if line[0] != "#"]
  assert list(tree.subtree_ids(tree.root_id)) == expected_results
  t2 = Tree.construct_from_tabular(testdata('small_tree.update.tsv'))
  t2.to_file(testout('small_tree2.tree'))
  t2.destroy_all_attributes()
  t2.create_attribute_from_tabular("attrX", testdata("small_tree_attrX.tsv"))
  t2.create_attribute_from_tabular("attrX2", testdata("small_tree_attrX.tsv"))
  assert_identical_subtrees(tree, t2)
  assert_identical_attributes(tree, t2)
  # update deleting everything except root
  tree.update_from_tabular(testdata('small_tree.rootonly.tsv'))
  assert list(tree.subtree_ids(tree.root_id)) == [1]
  t2 = Tree.construct_from_tabular(testdata('small_tree.rootonly.tsv'))
  t2.to_file(testout('small_tree2.tree'))
  t2.destroy_all_attributes()
  t2.create_attribute_from_tabular("attrX", testdata("small_tree_attrX.tsv"))
  t2.create_attribute_from_tabular("attrX2", testdata("small_tree_attrX.tsv"))
  assert_identical_subtrees(tree, t2)
  assert_identical_attributes(tree, t2)
  # update_from_ncbi_dump
  tree = Tree.construct_from_ncbi_dump(testdata('small_ncbi.tsv'))
  tree.to_file(testout('small_ncbi.tree'))
  tree.destroy_all_attributes()
  tree.create_attribute_from_tabular("attrX", testdata("small_tree_attrX.tsv"))
  tree.create_attribute_from_tabular("attrX2", testdata("small_tree_attrX.tsv"))
  tree.update_from_ncbi_dump(testdata("small_ncbi.update.tsv"))
  with open(testdata("small_ncbi.updated.query.root.parents.results")) as f:
    expected_results = \
        [int(line.split("\t")[0]) for line in f if line[0] != "#"]
  assert list(tree.subtree_ids(tree.root_id)) == expected_results
  t2 = Tree.construct_from_ncbi_dump(testdata('small_ncbi.update.tsv'))
  t2.to_file(testout('small_ncbi2.tree'))
  t2.destroy_all_attributes()
  t2.create_attribute_from_tabular("attrX", testdata("small_tree_attrX.tsv"))
  t2.create_attribute_from_tabular("attrX2", testdata("small_tree_attrX.tsv"))
  assert_identical_subtrees(tree, t2)
  assert_identical_attributes(tree, t2)

def test_reset_tree(testdata, testout):
  tree = Tree.construct_from_tabular(testdata('small_tree.tsv'))
  tree.to_file(testout('small_tree.tree'))
  tree.destroy_all_attributes()
  tree.create_attribute_from_tabular("attrX", testdata("small_tree_attrX.tsv"))
  tree.create_attribute_from_tabular("attrX2", testdata("small_tree_attrX.tsv"))
  tree.reset_from_tabular(testdata('small_tree.update.tsv'))
  with open(testdata("small_tree.updated.query.root.parents.results")) as f:
    expected_results = \
        [int(line.split("\t")[0]) for line in f if line[0] != "#"]
  assert set(tree.subtree_ids(tree.root_id)) == set(expected_results)
  t2 = Tree.construct_from_tabular(testdata('small_tree.update.tsv'))
  t2.to_file(testout('small_tree2.tree'))
  t2.destroy_all_attributes()
  t2.create_attribute_from_tabular("attrX", testdata("small_tree_attrX.tsv"))
  t2.create_attribute_from_tabular("attrX2", testdata("small_tree_attrX.tsv"))
  assert_identical_subtrees(tree, t2)
  assert_identical_attributes(tree, t2)
  # reset to only root
  tree.reset_from_tabular(testdata('small_tree.rootonly.tsv'))
  assert list(tree.subtree_ids(tree.root_id)) == [1]
  t2 = Tree.construct_from_tabular(testdata('small_tree.rootonly.tsv'))
  t2.to_file(testout('small_tree_rootonly.tree'))
  t2.destroy_all_attributes()
  t2.create_attribute_from_tabular("attrX", testdata("small_tree_attrX.tsv"))
  t2.create_attribute_from_tabular("attrX2", testdata("small_tree_attrX.tsv"))
  assert_identical_subtrees(tree, t2)
  assert_identical_attributes(tree, t2)
  # reset_from_ncbi_dump
  tree = Tree.construct_from_ncbi_dump(testdata('small_ncbi.tsv'))
  tree.set_filename(testout('small_ncbi.tree'))
  tree.destroy_all_attributes()
  tree.create_attribute_from_tabular("attrX", testdata("small_tree_attrX.tsv"))
  tree.create_attribute_from_tabular("attrX2", testdata("small_tree_attrX.tsv"))
  tree.reset_from_ncbi_dump(testdata("small_ncbi.update.tsv"))
  with open(testdata("small_ncbi.updated.query.root.parents.results")) as f:
    expected_results = \
        [int(line.split("\t")[0]) for line in f if line[0] != "#"]
  assert set(tree.subtree_ids(tree.root_id)) == set(expected_results)
  t2 = Tree.construct_from_ncbi_dump(testdata('small_ncbi.update.tsv'))
  t2.to_file(testout('small_ncbi2.tree'))
  t2.destroy_all_attributes()
  t2.create_attribute_from_tabular("attrX", testdata("small_tree_attrX.tsv"))
  t2.create_attribute_from_tabular("attrX2", testdata("small_tree_attrX.tsv"))
  assert_identical_subtrees(tree, t2)
  assert_identical_attributes(tree, t2)

def test_move_subtree(testdata, testout):
  tree = Tree.construct_from_tabular(testdata('small_tree.tsv'))
  tree.set_filename(testout("small_tree.tree"))
  tree.destroy_all_attributes()
  tree.create_attribute_from_tabular("attrX", testdata("small_tree_attrX.tsv"))
  tree.create_attribute_from_tabular(\
      "attrX", testdata("small_tree_attrX.tsv"), force=True)
  with pytest.raises(error.ConstructionError):
    tree.move_subtree(tree.root_id, 2)
  with pytest.raises(error.NodeNotFoundError):
    tree.move_subtree(2, -1)
  with pytest.raises(error.NodeNotFoundError):
    tree.move_subtree(-2, 1)
  tree.move_subtree(2, tree.get_parent(2))
  tree.move_subtree(2, 8)
  with pytest.raises(error.ConstructionError):
    tree.move_subtree(3, 7)
