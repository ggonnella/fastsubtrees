#!/usr/bin/env python3
"""
Update an existing tree representation

update mode (default):
  Given a source of IDs, it will remove from an existing tree all subtrees which
  are not in the source of IDs and add all subtrees which are in the source of
  IDs but not in the tree.

add mode:
  Given a source of IDs, it will add all nodes to the tree.

delete mode:
  Delete all listed nodes from the tree and all subtrees under them.

Notes:
- Any added node must be attached to an existing node in the tree or
  to a node added before that in the IDs source.
- Changing the parents of tree nodes is not supported.
- If existing node are included in the source of IDs, they will be ignored
  in update mode and the script will exit with an error in add mode.
- Deleted nodes cannot be added again.
- Attribute files are updated automatically.

Usage:
  fastsubtrees update [options] <tree> --tab <tabfile> [<idsmod_data>...]
  fastsubtrees update [options] <tree> <idsmod> [<idsmod_data>...]
  fastsubtrees update [options] <tree> --delete <subtree_root>...

Using a tabular file as source of IDs:

  To use a tabular file <tabfile> as source of IDs, use the --tab option.
  The file shall contain lines in the form "node_id <TAB> parent_id".

  Optional arguments after <tabfile> are given in this order
  or passed as key=value:
    - separator: separator (default: tab)
    - element_id_column: column index of the element ID (default: 0)
    - parent_id_column: column index of the parent ID (default: 1)
    - comment_pfx: prefix of lines to be skipped (default: '#')

Using a IDs source module:

  The <idsmod> argument is the path to a Python module.
  The module must have a function named element_parent_ids which yields
  tuples (node_id, parent_id).

  The <idsmod_data> arguments are passed to the element_parent_ids function.
  If they contain a = sign, they are interpreted as keyword arguments.

Options:
  --add        only add nodes, do not delete nodes
  --delete     delete specified nodes and subtrees under them
  --tab        use a tabular file as source of input data;
               shorthand for using the idsmod module
               fastsubtrees/ids_modules/ids_from_tabular_file.py
  --quiet      disable log messages
  --debug      print debug information
  --changes    print the changes made to the tree
  --help       show this help message and exit
  --version    show program's version number and exit
"""

import importlib
from docopt import docopt
from pathlib import Path
from fastsubtrees import Tree, logger, _scripts_support, VERSION, attribute

def main(args):
  logger.debug("Loading tree from file '{}'".format(args['<tree>']))
  tree = Tree.from_file(args["<tree>"])
  attrfiles = attribute.attrfiles(args["<tree>"]).values()
  n_deleted = 0
  deleted_nodes = list() if args["--changes"] else None
  added_nodes = list() if args["--changes"] else None
  if attrfiles:
    logger.debug("Attribute files to be updated: '{}'".\
        format("', '".join(attrfiles)))
  if args["--delete"]:
    for n in args["<subtree_root>"]:
      n_deleted += tree.delete_subtree(int(n), attrfiles,
          list_deleted=deleted_nodes)
  else:
    if args["--tab"]:
      import fastsubtrees.ids_modules.ids_from_tabular_file as m
      args["<idsmod_data>"] = [args["<tabfile>"]] + args["<idsmod_data>"]
    else:
      m = _scripts_support.get_module(args["<idsmod>"], "element_parent_ids")
    posargs, keyargs = _scripts_support.get_fn_args(True, args["<idsmod_data>"])
    generator = m.element_parent_ids(*posargs, **keyargs)
    if args["--add"]:
      n_added = tree.add_nodes(generator, attrfiles)
    else:
      n_added, n_deleted = tree.update(self, generator, attrfiles,
          list_added=added_nodes, list_deleted=deleted_nodes)
  if not args["--delete"]:
    logger.info("Number of nodes added: {}".format(n_added))
    if args["--changes"] and n_added:
      logger.info("IDs of added nodes: " + ", ".join(\
          [str(n) for n in added_nodes]))
  if not args["--add"]:
    logger.info("Number of nodes deleted: {}".format(n_deleted))
    if args["--changes"] and n_deleted:
      logger.info("IDs of deleted nodes: " + ", ".join(\
          [str(n) for n in deleted_nodes]))
  tree.to_file(args["<tree>"])

if __name__ == "__main__":
  args = docopt(__doc__, version=VERSION)
  _scripts_support.setup_verbosity(args)
  main(args)
