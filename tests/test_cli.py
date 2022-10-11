#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#
import pytest
import sh
import time
import os

@pytest.mark.script_launch_mode('subprocess')
def test_construct(testout, testdata, ids_modules, script, script_runner):
  args = ["construct", testout("small_tree.tree"),
          ids_modules("ids_from_tabular_file.py"), testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert os.path.exists(testout("small_tree.tree"))
  # add an attribute
  args = ["attr", "construct", testout("small_tree.tree"), 'attrX',
          ids_modules("attr_from_tabular_file.py"),
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert os.path.exists(testout("small_tree.tree.attrX.attr"))

@pytest.mark.script_launch_mode('subprocess')
def test_construct_tab(testout, testdata, ids_modules, script, script_runner):
  args = ["construct", testout("small_tree.tree"), "--tab",
          testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert os.path.exists(testout("small_tree.tree"))

@pytest.mark.script_launch_mode('subprocess')
def test_query(testout, testdata, ids_modules, script, script_runner,
               results_query_small_tree_id_8,
               results_query_small_tree_id_8_attrX):
  # construct the tree
  args = ["construct", testout("small_tree.tree"),
          ids_modules("ids_from_tabular_file.py"), testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  # add an attribute
  args = ["attr", "construct", testout("small_tree.tree"), 'attrX',
          ids_modules("attr_from_tabular_file.py"),
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  # query the constructed tree
  args = ["query", testout("small_tree.tree"), "8"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "".join(f"{x}\n" for x in results_query_small_tree_id_8)
  # query the attribute
  args = ["attr", "query", testout("small_tree.tree"), "attrX", "8"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout.strip() == str(results_query_small_tree_id_8_attrX)

@pytest.mark.script_launch_mode('subprocess')
def test_edit(testout, testdata, ids_modules, script, script_runner,
              results_query_small_tree_id_8,
              results_query_small_tree_id_8_add_subtree1,
              results_query_small_tree_id_8_add_subtree2,
              results_query_small_tree_id_8_attrX_after_add,
              results_query_small_tree_id_8_attrX_after_add2):
  # construct the tree
  args = ["construct", testout("small_tree.tree"),
          ids_modules("ids_from_tabular_file.py"), testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  # add an attribute
  args = ["attr", "construct", testout("small_tree.tree"), 'attrX',
          ids_modules("attr_from_tabular_file.py"),
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  # add a leaf
  args = ["add", testout("small_tree.tree"),
          ids_modules("ids_from_tabular_file.py"),
          testdata("small_tree_add_subtree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  args = ["query", testout("small_tree.tree"), "8"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "".join(f"{x}\n" for x in
      results_query_small_tree_id_8_add_subtree1)
  # add a more complicated subtree
  args = ["add", testout("small_tree.tree"),
          ids_modules("ids_from_tabular_file.py"),
          testdata("small_tree_add_subtree2.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  args = ["query", testout("small_tree.tree"), "8"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "".join(f"{x}\n" for x in
      results_query_small_tree_id_8_add_subtree2)
  # attribute query before changing it
  args = ["attr", "query", testout("small_tree.tree"), "attrX", "8"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout.strip() == \
    str(results_query_small_tree_id_8_attrX_after_add)
  # add attribute values
  args = ["attr", "add", testout("small_tree.tree"), 'attrX',
          ids_modules("attr_from_tabular_file.py"),
          testdata("small_tree_attrX_add.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # attribute query after changing it
  args = ["attr", "query", testout("small_tree.tree"), "attrX", "8"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout.strip() == \
    str(results_query_small_tree_id_8_attrX_after_add2)
  # delete added values from the tree
  args = ["delete", testout("small_tree.tree"), "10"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  args = ["query", testout("small_tree.tree"), "8"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "".join(f"{x}\n" for x in
      results_query_small_tree_id_8_add_subtree1)
  args = ["delete", testout("small_tree.tree"), "6"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  args = ["query", testout("small_tree.tree"), "8"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "".join(f"{x}\n" for x in
      results_query_small_tree_id_8)

