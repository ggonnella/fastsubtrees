#!/usr/bin/env python3
"""
Manage attribute values for trees.

Usage:
  fastsubtrees attribute <treefile> [--new|--add|--replace] <attribute> <tabfile> [options]
  fastsubtrees attribute <treefile> [--new|--add|--replace] <attribute> --module M [<args>...] [options]
  fastsubtrees attribute <treefile> --delete <attribute> [<node_id>...] [options]
  fastsubtrees attribute <treefile> --list [options]

Actions:
  -N, --new        (default) create a new attribute
  -A, --add        add further values to an existing attribute
  -R, --replace    replace some values of an existing attribute
  -D, --delete     delete an attribute or attribute values
  -L, --list       list defined attributes

Tabular file input:
  <tabfile>        tabular file with node IDs and attribute values
  -s, --separator S    separator in the tabular file (default: tab)
  -e, --elementscol E  column with the IDs of the elements (1-based, default: 1)
  -v, --valuescol P    column with the attribute values (1-based, default: 2)
  -c, --commentchar C  lines starting with this character are ignored (default: #)

Module input:
  -m, --module M  select file <M> as a Python module defining a function
                  yielding element IDs and attribute values
  <args>...       arguments to be passed to the function;
                  if they contain a '=', they are passed as keyword arguments
  -F, --fn FN     name of the function to be called (default: attribute_values)
  -K, --nokeys    disable interpreting '=' in <args> as keyword arguments separator

Conversion of attribute values:
  -t, --type T   function to apply to the attribute values; either from the
                 standard library or defined in the specified --module M

Further options:
  -S, --strict   exit with an error if a node ID is not found in the tree
                 (default: ignore lines with non-existing node IDs)
  -q, --quiet    disable log messages
  -d, --debug    print debug information
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit
""" # noqa

from fastsubtrees import logger, Tree
from fastsubtrees.commands import _support

def get_generator_and_casting_fn(args):
  fn = "attribute_values"
  if args["--module"]:
    if args["--fn"]:
      fn = args["--fn"]
    logger.debug("Using function "+\
        "{} from module {} as a source of attribute values".format(\
          fn, args["--module"]))
    m = _support.get_module(args["--module"], fn)
    posargs, keyargs = \
        _support.get_fn_args(not args["--nokeys"], args["<args>"])
    casting_fn = \
        _support.get_datatype_casting_fn(args["--type"], m, args["--module"])
  else:
    if args["--fn"]:
      logger.warning("Argument --fn ignored when not using --module")
    import fastsubtrees.ids_modules.attr_from_tabular_file as m
    logger.debug("Using tabular file {} as a source of attribute values".\
        format(args["<tabfile>"]))
    posargs = [args["<tabfile>"]]
    keyargs = {"separator": "\t",
               "id_col": 0,
               "attr_col": 1,
               "comment_pfx": "#"}
    if args["--separator"]:
      keyargs["separator"] = args["--separator"]
    if args["--elementscol"]:
      keyargs["id_col"] = int(args["--elementscol"]) - 1
    if args["--valuescol"]:
      keyargs["attr_col"] = int(args["--valuescol"]) - 1
    if args["--commentchar"]:
      keyargs["comment_pfx"] = args["--commentchar"]
    casting_fn = _support.get_datatype_casting_fn(args["--type"], None, None)
  return getattr(m, fn)(*posargs, **keyargs), casting_fn

DEFAULT_ACTION = "new"

def get_action(args):
  actions = \
      [a for a in ["new", "add", "replace", "delete", "list"] if args["--" + a]]
  assert len(actions) <= 1
  if len(actions) == 0:
    action = DEFAULT_ACTION
  elif len(actions) == 1:
    action = actions[0]
  return action

def manage_attribute(args, tree):
  action = get_action(args)
  if action in ["new", "add", "replace"]:
    generator, casting_fn = get_generator_and_casting_fn(args)
    new_attrvalues = Tree.prepare_attribute_values(generator, casting_fn)
  if action == "new":
    tree.save_attribute_values(args["<attribute>"], new_attrvalues)
  elif action == "add":
    tree.append_attribute_values(args["<attribute>"], new_attrvalues,
                                 args["--strict"])
  elif action == "replace":
    tree.replace_attribute_values(args["<attribute>"], new_attrvalues,
                                  args["--strict"])
  elif action == "delete":
    if not args["<node_id>"]:
      tree.destroy_attribute(args["<attribute>"])
    else:
      tree.delete_attribute_values(args["<attribute>"], args["<node_id>"],
                                 args["--strict"])
  elif action == "list":
    for attr in tree.list_attributes():
      print(attr)

def main(args):
  logger.debug("Loading tree from file '{}'".format(args['<treefile>']))
  tree = Tree.from_file(args["<treefile>"])
  manage_attribute(args, tree)
