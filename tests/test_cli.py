#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#
import pytest
import sh
import time
import os
from pathlib import Path

@pytest.mark.script_launch_mode('subprocess')
def test_new_from_tabular(testout, testdata, script, script_runner):
  Path(testout("small_tree.tree")).unlink(missing_ok=True)
  args = ["tree", testout("small_tree.tree"), testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert os.path.exists(testout("small_tree.tree"))

@pytest.mark.script_launch_mode('subprocess')
def test_new_from_module(testout, testdata, ids_modules, script, script_runner):
  Path(testout("small_tree.tree")).unlink(missing_ok=True)
  args = ["tree", testout("small_tree.tree"), "--module",
          ids_modules("ids_from_tabular_file.py"), testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert os.path.exists(testout("small_tree.tree"))

@pytest.mark.script_launch_mode('subprocess')
def test_new_attribute_from_tabular(testout, testdata, script,
                                    script_runner, small_tree_file):
  Path(testout("small_tree.tree.attrX.attr")).unlink(missing_ok=True)
  args = ["attribute", small_tree_file, 'attrX',
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert os.path.exists(testout("small_tree.tree.attrX.attr"))

@pytest.mark.script_launch_mode('subprocess')
def test_new_attribute_from_module(testout, testdata, ids_modules, script,
                       script_runner, small_tree_file):
  Path(testout("small_tree.tree.attrX.attr")).unlink(missing_ok=True)
  args = ["attribute", small_tree_file, 'attrX',
          "--module", ids_modules("attr_from_tabular_file.py"),
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert os.path.exists(testout("small_tree.tree.attrX.attr"))

@pytest.mark.script_launch_mode('subprocess')
def test_query(testout, testdata, script, script_runner,
               results_query_small_tree_id_8,
               results_query_small_tree_id_8_attrX,
               small_tree_file):
  Path(testout("small_tree.tree.attrX.attr")).unlink(missing_ok=True)
  # add an attribute
  args = ["attribute", small_tree_file, 'attrX',
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  # query the constructed tree
  args = ["query", small_tree_file, "8", "-N"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "".join(f"{x}\n" for x in results_query_small_tree_id_8)
  # query the attribute
  args = ["query", small_tree_file, "8", "attrX", "-a", "-N"]
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
  Path(testout("small_tree.tree")).unlink(missing_ok=True)
  Path(testout("small_tree.tree.attrX.attr")).unlink(missing_ok=True)
  # construct the tree
  args = ["tree", testout("small_tree.tree"), testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  # add an attribute
  args = ["attribute", testout("small_tree.tree"), 'attrX',
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  # add a leaf
  args = ["tree", "--add", testout("small_tree.tree"),
          testdata("small_tree_add_subtree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  args = ["query", testout("small_tree.tree"), "8", "-N"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "".join(f"{x}\n" for x in
      results_query_small_tree_id_8_add_subtree1)
  # add a more complicated subtree
  args = ["tree", "--add", testout("small_tree.tree"),
          testdata("small_tree_add_subtree2.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  args = ["query", testout("small_tree.tree"), "8", "-N"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "".join(f"{x}\n" for x in
      results_query_small_tree_id_8_add_subtree2)
  # attribute query before changing it
  args = ["query", testout("small_tree.tree"), "8", "attrX", "-a", "-N", "-n"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout.strip() == \
    str(results_query_small_tree_id_8_attrX_after_add)
  # add attribute values
  args = ["attribute", "--add", testout("small_tree.tree"), 'attrX',
          testdata("small_tree_attrX_add.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # attribute query after changing it
  args = ["query", testout("small_tree.tree"), "8", "attrX", "-a", "-N", "-n"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout.strip() == \
    str(results_query_small_tree_id_8_attrX_after_add2)
  # delete added values from the tree
  args = ["tree", "--delete", testout("small_tree.tree"), "10"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  args = ["query", testout("small_tree.tree"), "8", "-N"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "".join(f"{x}\n" for x in
      results_query_small_tree_id_8_add_subtree1)
  args = ["tree", "--delete", testout("small_tree.tree"), "6"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  args = ["query", testout("small_tree.tree"), "8", "-N"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "".join(f"{x}\n" for x in
      results_query_small_tree_id_8)

