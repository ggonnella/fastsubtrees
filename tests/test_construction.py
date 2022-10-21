import pytest
from fastsubtrees.ids_modules.ids_from_tabular_file import element_parent_ids
from fastsubtrees.ids_modules.attr_from_tabular_file import attribute_values
from fastsubtrees import Tree, error

def test_construction_small(testdata, prebuilt):
  infname = testdata('small_tree.tsv')
  generator = element_parent_ids(infname)
  constructed_tree = Tree.construct(generator)
  constructed_subtree_ids = constructed_tree.subtree_ids(1)
  prebuilt_tree = Tree.from_file(prebuilt('small_tree.tree'))
  prebuilt_subtree_ids = prebuilt_tree.subtree_ids(1)
  assert constructed_subtree_ids == prebuilt_subtree_ids

def test_construction_small_parallel(testdata, prebuilt):
  infname = testdata('small_tree.tsv')
  generator = element_parent_ids(infname)
  constructed_tree = Tree.construct(generator, 2)
  constructed_subtree_ids = constructed_tree.subtree_ids(1)
  prebuilt_tree = Tree.from_file(prebuilt('small_tree.tree'))
  prebuilt_subtree_ids = prebuilt_tree.subtree_ids(1)
  assert constructed_subtree_ids == prebuilt_subtree_ids

def test_construction_small_from_tabular(testdata, prebuilt):
  infname = testdata('small_tree.tsv')
  constructed_tree = Tree.construct_from_tabular(infname)
  assert constructed_tree.root_id == 1
  constructed_subtree_ids = constructed_tree.subtree_ids(1)
  prebuilt_tree = Tree.from_file(prebuilt('small_tree.tree'))
  prebuilt_subtree_ids = prebuilt_tree.subtree_ids(1)
  assert constructed_subtree_ids == prebuilt_subtree_ids

def test_construction_small_from_ncbi_dump(testdata):
  infname = testdata('small_ncbi.tsv')
  tree = Tree.construct_from_ncbi_dump(infname)
  subtree_ids = \
      list(tree.subtree_ids(tree.root_id))
  with open(testdata("small_ncbi_query_ids_root.results")) as f:
    expected_subtree_ids = [int(line.strip()) for line in f]
  assert subtree_ids == expected_subtree_ids

def test_attribute_construction(testdata, testout):
  tree = Tree.construct_from_tabular(testdata('small_tree.tsv'))
  infname = testdata('small_tree_attrX.tsv')
  with pytest.raises(error.FilenameNotSetError):
    tree.create_attribute("attrX", attribute_values(infname))
  tree.set_filename(testout('small_tree.tree'))
  tree.create_attribute("attrX", attribute_values(infname))
  # attribute exists already:
  with pytest.raises(error.AttributeCreationError):
    tree.create_attribute("attrX", attribute_values(infname))
  with pytest.raises(error.AttributeCreationError):
    tree.create_attribute_from_tabular("attrX", infname)
  assert Tree.compute_attribute_filename(testout('small_tree.tree'),
      "attrX").exists()
  tree.destroy_attribute("attrX")
  assert not Tree.compute_attribute_filename(testout('small_tree.tree'),
      "attrX").exists()
  with pytest.raises(error.AttributeNotFoundError):
    tree.destroy_attribute("attrX")
  tree.create_attribute("attrX", attribute_values(infname))
  tree.create_attribute("attrY", attribute_values(infname))
  assert Tree.compute_attribute_filename(testout('small_tree.tree'),
      "attrY").exists()
  assert set(tree.list_attributes()) == {"attrX", "attrY"}
  tree.destroy_all_attributes()
  assert not Tree.compute_attribute_filename(testout('small_tree.tree'),
      "attrX").exists()
  assert not Tree.compute_attribute_filename(testout('small_tree.tree'),
      "attrY").exists()
  assert tree.list_attributes() == []
  # delete a node, then setting the attribute does not really set it
  tree.create_attribute("attrX", attribute_values(infname))
  values = tree.load_attribute_values("attrX")
  assert values[9] == ["I"]
  tree.delete_subtree(9)
  values = tree.load_attribute_values("attrX")
  assert 9 not in values
  values[9] = ["I"]
  tree.save_attribute_values("attrX", values)
  values = tree.load_attribute_values("attrX")
  assert 9 not in values

def test_get_methods(testdata):
  infname = testdata('small_tree.tsv')
  tree = Tree.construct_from_tabular(infname)
  assert tree.get_parent(1) == 1
  assert tree.get_parent(8) == 1
  assert tree.get_subtree_size(1) == 8
  assert tree.get_subtree_size(8) == 6
  assert tree.get_parent(6) == Tree.UNDEF
  assert tree.get_subtree_size(6) == 0
  assert list(tree.get_subtree_data(6)) == []

def test_construction_medium(testdata, prebuilt):
  infname = testdata('medium_tree.tsv')
  generator = element_parent_ids(infname)
  constructed_tree = Tree.construct(generator)
  constructed_subtree_ids = constructed_tree.subtree_ids(1)
  prebuilt_tree = Tree.from_file(prebuilt('medium_tree.tree'))
  prebuilt_subtree_ids = prebuilt_tree.subtree_ids(1)
  assert constructed_subtree_ids == prebuilt_subtree_ids

def test_construction_node0(testdata):
  infname = testdata('construction_node0.tsv')
  tree = Tree.construct_from_tabular(infname)
  assert list(tree.subtree_ids(tree.root_id)) == [0, 1]

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

def test_construction_err_same_node_root_and_not(testdata):
  infname = testdata('same_node_root_and_not.tsv')
  generator = element_parent_ids(infname)
  with pytest.raises(error.ConstructionError):
    Tree.construct(generator)

def test_construction_err_negative(testdata):
  infname = testdata('negative_parent.tsv')
  generator = element_parent_ids(infname)
  with pytest.raises(error.ConstructionError):
    Tree.construct(generator)
  infname = testdata('negative_node.tsv')
  generator = element_parent_ids(infname)
  with pytest.raises(error.ConstructionError):
    Tree.construct(generator)

def test_construction_err_parent_not_exist(testdata):
  infname = testdata('parent_not_exist.tsv')
  generator = element_parent_ids(infname)
  with pytest.raises(error.ConstructionError):
    Tree.construct(generator)
  infname = testdata('parent_not_exist_small.tsv')
  generator = element_parent_ids(infname)
  with pytest.raises(error.ConstructionError):
    Tree.construct(generator)
