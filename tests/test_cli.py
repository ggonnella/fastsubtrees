#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#
import pytest
import os
from pathlib import Path

@pytest.mark.script_launch_mode('subprocess')
def test_not_existing_subcommand(script, script_runner):
  ret = script_runner.run(script("fastsubtrees"), "not-existing")
  assert ret.returncode == 1

@pytest.mark.script_launch_mode('subprocess')
def test_new_from_tabular(testout, testdata, script, script_runner):
  Path(testout("small_tree.tree")).unlink(missing_ok=True)
  args = ["tree", testout("small_tree.tree"), testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert os.path.exists(testout("small_tree.tree"))
  # setting format options
  args = ["tree", testout("small_tree.tree"), testdata("small_tree.tsv"),
       "--separator", "\t", "--commentchar", "#", "--elementscol", "1",
       "--parentscol", "2"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  args.append("--force")
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert os.path.exists(testout("small_tree.tree"))
  args.extend(["--processes", "1"])
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert os.path.exists(testout("small_tree.tree"))

@pytest.mark.script_launch_mode('subprocess')
def test_update(testout, testdata, script, script_runner):
  Path(testout("small_tree.tree")).unlink(missing_ok=True)
  args = ["tree", testout("small_tree.tree"), testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  # updating the tree with itself
  args = ["tree", testout("small_tree.tree"), "--update",
      testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # really updating now
  args = ["tree", testout("small_tree.tree"), "--update", "--changes",
      testdata("small_tree.update.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  with open(testdata("small_tree.updated.query.root.parents.results")) as f:
    expected_results = f.read()
  args = ["query", testout("small_tree.tree"), "root", "--parents"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == expected_results
  args = ["query", testout("small_tree.tree"), "root", "--subtree-sizes"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # updating to just the root
  args = ["tree", testout("small_tree.tree"), "--update",
      testdata("just_root.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # try to set root node as internal
  args = ["tree", testout("small_tree.tree"), "--update",
      testdata("same_node_root_and_not.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  # add to tree which does not exist
  args = ["tree", testout("not_existing.tree"), "--add",
      testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  # negative parent
  args = ["tree", testout("small_tree.tree"), "--add",
      testdata("negative_parent.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  args = ["tree", testout("small_tree.tree"), "--update",
      testdata("negative_parent.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr

@pytest.mark.script_launch_mode('subprocess')
def test_reset(testout, testdata, script, script_runner):
  Path(testout("small_tree.tree")).unlink(missing_ok=True)
  args = ["tree", testout("small_tree.tree"), testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  # updating the tree with itself
  args = ["tree", testout("small_tree.tree"), "--reset",
      testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # really updating now
  args = ["tree", testout("small_tree.tree"), "--reset",
      testdata("small_tree.update.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  with open(testdata("small_tree.updated.query.root.parents.results")) as f:
    expected_results = f.read()
  args = ["query", testout("small_tree.tree"), "root", "--parents"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert set(ret.stdout.split("\n")) == set(expected_results.split("\n"))
  args = ["query", testout("small_tree.tree"), "root", "--subtree-sizes"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # updating to just the root
  args = ["tree", testout("small_tree.tree"), "--reset",
      testdata("just_root.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # try to set root node as internal
  args = ["tree", testout("small_tree.tree"), "--reset",
      testdata("same_node_root_and_not.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr

@pytest.mark.script_launch_mode('subprocess')
def test_new_from_nodes_dmp(testout, testdata, script, script_runner):
  Path(testout("small_ncbi.tree")).unlink(missing_ok=True)
  args = ["tree", testout("small_ncbi.tree"), testdata("small_ncbi.tsv"),
          "--ncbi"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert os.path.exists(testout("small_ncbi.tree"))
  # setting format options results to a warning
  args = ["tree", testout("small_tree.ncbi"), testdata("small_ncbi.tsv"),
       "--ncbi", "--separator", "\t", "--commentchar", "#",
       "--elementscol", "1", "--parentscol", "2", "--force"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert "WARNING" in ret.stderr

def ids_wrapper(filename, a, b=None):
  assert (a == "A")
  assert (b == "B=B")
  import fastsubtrees.ids_modules.ids_from_tabular_file as iftf
  return iftf.element_parent_ids(filename)

def ids_wrapper2(filename, a, b=None):
  assert (a == "b=B=B")
  assert (b == "A")
  import fastsubtrees.ids_modules.ids_from_tabular_file as iftf
  return iftf.element_parent_ids(filename)

@pytest.mark.script_launch_mode('subprocess')
def test_new_from_module(testout, testdata, ids_modules, script, script_runner):
  Path(testout("small_tree.tree")).unlink(missing_ok=True)
  args = ["tree", testout("small_tree.tree"), "--module",
          ids_modules("ids_from_tabular_file.py"), testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert os.path.exists(testout("small_tree.tree"))
  # ncbi is ignored when using module
  Path(testout("small_tree.tree")).unlink(missing_ok=True)
  args = ["tree", testout("small_tree.tree"), "--force", "--ncbi", "--module",
          ids_modules("ids_from_tabular_file.py"), testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert "WARNING" in ret.stderr
  # using --fn
  args = ["tree", testout("small_tree.tree"), "--force", "--fn", "ids_wrapper",
      "--module", __file__, testdata("small_tree.tsv"), "b=B=B", "A"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # using --nokeys
  args = ["tree", testout("small_tree.tree"), "--force", "--fn", "ids_wrapper2",
      "--module", __file__, testdata("small_tree.tsv"), "b=B=B", "A",
      "--nokeys"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # --fn is ignored with a warning if --module is not used
  args = ["tree", testout("small_tree.tree"), "--force", "--fn", "ids_wrapper",
      testdata("small_tree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert "WARNING" in ret.stderr

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
  args = ["query", small_tree_file, "8", "-H"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "".join(f"{x}\n" for x in results_query_small_tree_id_8)
  # query the attribute
  args = ["query", small_tree_file, "8", "attrX", "-a", "-H"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout.strip() == str(results_query_small_tree_id_8_attrX)
  # error, --attributes-only without attributes
  args = ["query", small_tree_file, "8", "-a", "-H"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  # query from root, --stats
  args = ["query", small_tree_file, "root", "attrX", "-a", "-H", "--stats"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  with open(testdata("small_tree_attrX.query_root.a.H.results")) as f:
    assert ret.stdout.strip() == f.read().strip()
  assert "Number of nodes in subtree: 8" in ret.stderr

def attribute_values_wrapper(filename, a, b=None):
  assert (a == "A")
  assert (b == "B=B")
  import fastsubtrees.ids_modules.attr_from_tabular_file as aftf
  return aftf.attribute_values(filename)

def attribute_values_wrapperB(filename, a, b=None):
  assert (a == "b=B=B")
  assert (b == "A")
  import fastsubtrees.ids_modules.attr_from_tabular_file as aftf
  return aftf.attribute_values(filename)

def add_10_percent(x):
  return "{:.1f}".format(float(x)*1.1)

@pytest.mark.script_launch_mode('subprocess')
def test_attribute_failures_and_warnings(testout, testdata, ids_modules, script,
    script_runner, small_tree_file):
  # tree file does not exist
  args = ["attribute", "does_not_exist.tree", 'attrY', "--add",
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  # module does not exist
  args = ["attribute", small_tree_file, 'attrX', "--module", "not_existing.py",
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  # modules does not define the function
  args = ["attribute", small_tree_file, 'attrX', "--fn", "not_existing_fn",
          "--module", ids_modules("ids_from_tabular_file.py"),
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  # modules cannot be loaded
  args = ["attribute", small_tree_file, 'attrX',
          "--module", testdata("small_tree_attrX.tsv"),
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  # using --fn without --module, produces a warning, but no error
  args = ["attribute", small_tree_file, 'attrX', "--fn", "attribute_values",
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert "WARNING" in ret.stderr
  # attribute file not existing
  args = ["attribute", small_tree_file, 'attrY', "--add",
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  # delete non-existing node, no --strict, no error
  args = ["attribute", small_tree_file, 'attrX', "--delete", "100"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # delete non-existing node, error when --strict
  args = ["attribute", small_tree_file, 'attrX', "--delete", "100", "--strict"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  # add non-existing node, no --strict, no error
  args = ["attribute", small_tree_file, 'attrX', "--add", \
      testdata("small_tree_attrX_add.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # add non-existing node, error when --strict
  args = ["attribute", small_tree_file, 'attrX', "--add", \
      testdata("small_tree_attrX_add.tsv"), "--strict"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  # replace non-existing node, no --strict, no error
  args = ["attribute", small_tree_file, 'attrX', "--replace", \
      testdata("small_tree_attrX_add.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # replace non-existing node, error when --strict
  args = ["attribute", small_tree_file, 'attrX', "--replace", \
      testdata("small_tree_attrX_add.tsv"), "--strict"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  # non-existing casting function from module
  args = ["attribute", small_tree_file, 'attrX', "--type", "not_existing_fn",
          "--module", ids_modules("ids_from_tabular_file.py"),
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  # non-existing casting function from standard library
  args = ["attribute", small_tree_file, 'attrX', "--type", "not_existing_fn",
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr

@pytest.mark.script_launch_mode('subprocess')
def test_attribute_edit_and_query(testout, testdata, script,
                                  script_runner, small_tree_file):
  args = ["attribute", small_tree_file, 'attrX',
          testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # add existing node, no error, values are appended
  args = ["attribute", small_tree_file, 'attrX', "--add", \
      testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # query after adding existing node
  args = ["query", small_tree_file, "9", "attrX", "-a", "-H"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout.strip() == "I, I"
  # query with all extra information and header, --separator
  args = ["query", small_tree_file, "9", "attrX", "--parents",
      "--subtree-sizes"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "# node_id\tparent\tsubtree_size\tattrX\n"+\
                       "9\t3\t1\tI, I\n"
  # query with --separator
  args = ["query", small_tree_file, "9", "attrX", "--separator", ";"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "# node_id;attrX\n"+\
                       "9;I, I\n"
  # replace
  args = ["attribute", small_tree_file, 'attrX', "--replace", \
      testdata("small_tree_attrX.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # query after replace
  args = ["query", small_tree_file, "9", "attrX", "-a", "-H"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout.strip() == "I"
  # query after replace, node with multiple values, --only option
  args = ["query", small_tree_file, "3", "attrX", "-a", "-H", "-o"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout.strip() == "C, c"
  # delete; --quiet option
  args = ["attribute", small_tree_file, 'attrX', "--delete", "9", "--quiet"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # query after adding existing node, --debug option
  args = ["query", small_tree_file, "9", "attrX", "-a", "-H", "--debug"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout.strip() == ""
  # query with --missing
  args = ["query", small_tree_file, "9", "attrX", "-a", "-H", "--missing"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout.strip() == "None"
  # create int attribute
  args = ["attribute", small_tree_file, 'attrI', \
      testdata("small_tree_attrI.tsv"), '--type', 'int']
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # query int attribute
  args = ["query", small_tree_file, "9", "attrI", "-a", "-H"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout.strip() == "900"
  # create custom type attribute
  args = ["attribute", small_tree_file, 'attrJ',
          "--module", __file__, "--fn", "attribute_values_wrapper",
          testdata("small_tree_attrI.tsv"), "b=B=B", "A",
          "--type", "add_10_percent"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # query custom type attribute
  args = ["query", small_tree_file, "9", "attrJ", "-a", "-H"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout.strip() == "990.0"
  # list attributes
  args = ["attribute", small_tree_file, "--list"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert set(ret.stdout.strip().split()) == set(["attrI", "attrJ", "attrX"])

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
  # add an attribute, use the format options to test them
  args = ["attribute", testout("small_tree.tree"), 'attrX',
          testdata("small_tree_attrX.tsv"), "--separator", "\t",
          "--elementscol", "1", "--valuescol", "2", "--commentchar", "#"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  # add a leaf
  args = ["tree", "--add", testout("small_tree.tree"),
          testdata("small_tree_add_subtree.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  args = ["query", testout("small_tree.tree"), "8", "-H"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # add a more complicated subtree
  args = ["tree", "--add", testout("small_tree.tree"),
          testdata("small_tree_add_subtree2.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  args = ["query", testout("small_tree.tree"), "8", "-H"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "".join(f"{x}\n" for x in
      results_query_small_tree_id_8_add_subtree2)
  # add failing, since nodes are repeated, failing at the root
  args = ["tree", "--add", testout("small_tree.tree"),
      testdata("just_root.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  # add failing, since nodes are repeated, failing at other node
  args = ["tree", "--add", testout("small_tree.tree"),
      testdata("small_tree.shuffled.tsv")]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  # attribute query before changing it
  args = ["query", testout("small_tree.tree"), "8", "attrX", "-a", "-H", "-m"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout.strip() == \
    str(results_query_small_tree_id_8_attrX_after_add)
  # add attribute values (this time test the --module and --fn option)
  args = ["attribute", "--add", testout("small_tree.tree"), 'attrX',
          "--module", __file__, "--fn", "attribute_values_wrapper",
          testdata("small_tree_attrX_add.tsv"), "b=B=B", "A"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # add attribute values (use --nokeys)
  args = ["attribute", "--replace", testout("small_tree.tree"), 'attrX',
          "--module", __file__, "--fn", "attribute_values_wrapperB",
          "--nokeys", testdata("small_tree_attrX_add.tsv"), "b=B=B", "A"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # attribute query after changing it
  args = ["query", testout("small_tree.tree"), "8", "attrX", "-a", "-H", "-m"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout.strip() == \
    str(results_query_small_tree_id_8_attrX_after_add2)
  # delete added values from the tree
  args = ["tree", "--delete", testout("small_tree.tree"), "10"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  args = ["query", testout("small_tree.tree"), "8", "-H"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "".join(f"{x}\n" for x in
      results_query_small_tree_id_8_add_subtree1)
  args = ["tree", "--delete", testout("small_tree.tree"), "6"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  args = ["query", testout("small_tree.tree"), "8", "-H"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  assert ret.stdout == "".join(f"{x}\n" for x in
      results_query_small_tree_id_8)
  # delete all values of attrX
  args = ["attribute", "--delete", testout("small_tree.tree"), 'attrX']
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 0
  # attribute query after deleting it
  args = ["query", testout("small_tree.tree"), "8", "attrX", "-a", "-H", "-m"]
  ret = script_runner.run(script("fastsubtrees"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr

