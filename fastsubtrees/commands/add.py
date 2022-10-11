#!/usr/bin/env python3
"""
Add a subtree to an existing tree representation

The subtree may consist of a single leaf node, or of an internal node
to be attached to the existing tree and the subtree under that internal node.

To add multiple leaves or subtrees under different nodes of an existing tree,
call this script separately for each subtree.

Usage:
  fastsubtrees add [options] <tree> <idsmod> [<idsmod_data>...]
  fastsubtrees add [options] <tree> --tab <tabfile> [<idsmod_data>...]

Arguments:
  tree         File containing the tree data
  idsmod       Python module defining a function element_parent_ids()
               which may take arguments (<idsmod_data>) and yield pairs
               (element_id, parent_id) for all nodes of the subtree to add.
  tabfile      If the --tab option is used, the module
               fastsubtrees/ids_modules/ids_from_tabular_file.py is used;
               the tabfile argument in this case is the path to the tabular
               file containing the attribute values.
  idsmod_data  [optional] arguments to be passed to the element_parent_ids()
               function of the module specified as <idsmod>; to pass keyword
               arguments, use the syntax "key=value" and the option --keyargs

Options:
  --tab        use a tabular file as source of input data;
               shorthand for using the idsmod module
               fastsubtrees/ids_modules/ids_from_tabular_file.py
  --keyargs    split the arguments specified in <idsmod_data> into
               keywords and values by splitting on the first instance of '=';
               arguments which do not contain '=' are passed as positional,
               before any keyword argument
  --quiet      disable log messages
  --debug      print debug information
  --help       show this help message and exit
  --version    show program's version number and exit
"""

import importlib
from docopt import docopt
from pathlib import Path
from fastsubtrees import Tree, logger, _scripts_support, VERSION, attribute

def main(args):
  if args["--tab"]:
    import fastsubtrees.ids_modules.ids_from_tabular_file as m
    args["<idsmod_data>"] = [args["<tabfile>"]] + args["<idsmod_data>"]
  else:
    m = _scripts_support.get_module(args["<idsmod>"], "element_parent_ids")
  logger.info("Adding subtree using IDs yielded by the generator...")
  posargs, keyargs = _scripts_support.get_fn_args(args["--keyargs"],
                                                  args["<idsmod_data>"])
  logger.debug("Loading tree from file '{}'".format(args['<tree>']))
  tree = Tree.from_file(args["<tree>"])
  logger.debug("Successfully loaded tree from file '{}'".format(args['<tree>']))
  attrfiles = attribute.attrfiles(args["<tree>"]).values()
  logger.debug("Modifying attribute files: '{}'".format("', '".join(attrfiles)))
  generator = m.element_parent_ids(*posargs, **keyargs)
  tree.add_subtree(generator, attrfiles)
  logger.success("Subtree added to the existing tree")
  tree.to_file(args["<tree>"])

if __name__ == "__main__":
  args = docopt(__doc__, version=VERSION)
  _scripts_support.setup_verbosity(args)
  main(args)