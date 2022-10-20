#!/usr/bin/env python3
"""
Create or edit a tree representation

Usage:
  fastsubtrees tree <treefile> [--new|--update|--reset|--add] <tabfile> [options]
  fastsubtrees tree <treefile> [--new|--update|--reset|--add] --module M [<args>...] [options]
  fastsubtrees tree <treefile> --delete <subtree_root>... [options]

Actions:
  -N, --new      (default) create a new tree from the given IDs source
  -U, --update   update an existing tree to reflect the given IDs source;
                 the tree and the attribute files are edited
  -R, --reset    reset an existing tree to reflect the given IDs source;
                 the tree is created from scratch; attributes are dumped and reloaded
  -A, --add      add new nodes to an existing tree
  -D, --delete   remove leaves or subtrees from an existing tree

Tabular file input:
  <tabfile>            tabular file containing IDs of the nodes and their parents
  -n, --ncbi           the tabular file is in NCBI taxonomy dump format
  -s, --separator S    separator in the tabular file (default: tab)
  -e, --elementscol E  column with the IDs of the elements (1-based, default: 1)
  -p, --parentscol P   column with the IDs of the parents (1-based, default: 2)
  -c, --commentchar C  lines starting with this character are ignored (default: #)

Module input:
  -m, --module M  select file <M> as a Python module defining a function
                  yielding IDs of elements and parents
  <args>...       arguments to be passed to the function;
                  if they contain a '=', they are passed as keyword arguments
  -F, --fn FN     name of the function to be called (default: element_parent_ids)
  -K, --nokeys    disable interpreting '=' in <args> as keyword arguments separator

Further options:
  -f, --force        overwrite the output file if it exists (action --new)
  -C, --changes      verbosily report changes made to the tree
  -q, --quiet        disable log messages
  -d, --debug        print debug information
  -h, --help         show this help message and exit
  -V, --version      show program's version number and exit
  -t, --processes N  number of processes to use (default: 1)
""" # noqa

from pathlib import Path
from fastsubtrees import Tree, logger
from fastsubtrees.commands import _support

def get_generator(args):
  fn = "element_parent_ids"
  if args["--module"]:
    if args["--ncbi"]:
      logger.warning("The --ncbi option is ignored when using --module")
    if args["--fn"]:
      fn = args["--fn"]
    logger.debug("Using function {} from module {} as a source of IDs".\
        format(fn, args["--module"]))
    m = _support.get_module(args["--module"], fn)
    posargs, keyargs = \
        _support.get_fn_args(not args["--nokeys"], args["<args>"])
  else:
    if args["--fn"]:
      logger.warning("Argument --fn ignored when not using --module")
    import fastsubtrees.ids_modules.ids_from_tabular_file as m
    logger.debug("Using tabular file {} as a source of IDs".\
        format(args["<tabfile>"]))
    posargs = [args["<tabfile>"]]
    if args["--ncbi"]:
      if args["--separator"] or args["--elementscol"] \
          or args["--parentscol"] or args["--commentchar"]:
        logger.warning("The --ncbi option overrides the following options: " +\
            "--separator, --elementscol, --parentscol, --commentchar")
      keyargs = {"ncbi_preset": True, "comment_pfx": "#"}
    else:
      keyargs = {"separator": "\t", "element_id_column": 0,
                 "parent_id_column": 1, "comment_pfx": "#"}
      if args["--separator"]:
        keyargs["separator"] = args["--separator"]
      if args["--elementscol"]:
        keyargs["element_id_column"] = int(args["--elementscol"]) - 1
      if args["--parentscol"]:
        keyargs["parent_id_column"] = int(args["--parentscol"]) - 1
      if args["--commentchar"]:
        keyargs["comment_pfx"] = args["--commentchar"]
  return getattr(m, fn)(*posargs, **keyargs)

DEFAULT_ACTION = "new"

def get_action(args):
  actions = \
      [a for a in ["new", "update", "reset", "add", "delete"] if args["--" + a]]
  assert len(actions) <= 1
  if len(actions) == 0:
    return DEFAULT_ACTION
  elif len(actions) == 1:
    return actions[0]

def report_changes(n_changes, changes, report=[]):
  for c in report:
    logger.info("Number of nodes {}: {}".format(c, n_changes[c]))
    if n_changes[c] > 0 and changes[c] is not None:
      logger.info(f"IDs of {c} nodes: " + ", ".join(\
          [str(n) for n in changes[c]]))

def main(args):
  action = get_action(args)
  if action != "delete":
    generator = get_generator(args)
  if action == "new":
    logger.debug("Creating new tree")
    if Path(args["<treefile>"]).exists() and not args["--force"]:
      logger.error("File {} already exists".format(args["<treefile>"]))
      exit(1)
    if not args["--processes"]:
      args["--processes"] = 1
    else:
      args["--processes"] = int(args["--processes"])
    tree = Tree.construct(generator, args["--processes"])
    tree.set_filename(args["<treefile>"])
    tree.destroy_all_attributes()
  else:
    if not Path(args["<treefile>"]).exists():
      msg = "Tree file {} does not exist".format(args["<treefile>"])
      logger.error(msg)
      exit(1)
    logger.debug("Loading tree from file '{}'".format(args['<treefile>']))
    tree = Tree.from_file(args["<treefile>"])
    n_changes = {"added": 0, "moved": 0, "deleted": 0}
    if args["--changes"]:
      changes = {"added": [], "moved": [], "deleted": []}
    else:
      changes = {"added": None, "moved": None, "deleted": None}
    if action == "delete":
      for n in args["<subtree_root>"]:
        n_changes["deleted"] += tree.delete_subtree(int(n),
            list_deleted=changes["deleted"])
      report_changes(n_changes, changes, ["deleted"])
    elif action == "add":
      n_changes["added"] = tree.add_nodes(generator,
          list_added=changes["added"])
      report_changes(n_changes, changes, ["added"])
    elif action == "update":
      n_changes["added"], n_changes["deleted"], n_changes["moved"] = \
          tree.update(generator,
              list_added=changes["added"], list_deleted=changes["deleted"],
              list_moved=changes["moved"])
      report_changes(n_changes, changes, ["added", "deleted", "moved"])
    elif action == "reset":
      tree.reset(generator)
  tree.to_file(args["<treefile>"])
