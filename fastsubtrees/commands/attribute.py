#!/usr/bin/env python3
"""
Manage attribute values for trees.

Usage:
  fastsubtrees attribute <treefile> [--new|--add|--replace] <attribute> <tabfile> [options]
  fastsubtrees attribute <treefile> [--new|--add|--replace] <attribute> --module M [<args>...] [options]
  fastsubtrees attribute <treefile> --delete <attribute> [<node_id>...] [options]

Actions:
  --new        (default) create a new attribute
  --add        add further values to an existing attribute
  --replace    replace some values of an existing attribute
  --delete     delete an attribute or attribute values

Tabular file input:
  <tabfile>        tabular file with node IDs and attribute values
  --separator S    separator in the tabular file (default: tab)
  --elementscol E  column with the IDs of the elements (1-based, default: 1)
  --valuescol P    column with the attribute values (1-based, default: 2)
  --commentchar C  lines starting with this character are ignored (default: #)

Module input:
  --module M  select file <M> as a Python module defining a function
              yielding element IDs and attribute values
  <args>...   arguments to be passed to the function;
              if they contain a '=', they are passed as keyword arguments
  --fn FN     name of the function to be called (default: attribute_values)

Conversion of attribute values:
  --datatype DT  function to apply to the attribute values; either from the
                 standard library or defined in the specified --module M

Further options:
  --strict       exit with an error if a node ID is not found in the tree
                 (default: ignore lines with non-existing node IDs)
  --quiet        disable log messages
  --debug        print debug information
  --help         show this help message and exit
  --version      show program's version number and exit
"""

from docopt import docopt
from fastsubtrees import _scripts_support, logger, Tree, attribute, VERSION
from collections import defaultdict
from pathlib import Path

def get_generator_and_casting_fn(args):
  fn = "attribute_values"
  if args["--module"]:
    if args["--fn"]:
      fn = args["--fn"]
    logger.debug("Using function "+\
        "{} from module {} as a source of attribute values".format(\
          fn, args["--module"]))
    m = _scripts_support.get_module(args["--module"], fn)
    posargs, keyargs = _scripts_support.get_fn_args(True, args["<args>"])
    casting_fn = _scripts_support.get_datatype_casting_fn(args["--datatype"], \
                                                          m, args["--module"])
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
    casting_fn = _scripts_support.get_datatype_casting_fn(args["--datatype"], \
                                                          None, None)
  return getattr(m, fn)(*posargs, **keyargs), casting_fn

DEFAULT_ACTION = "new"

def get_action(args, attrfname):
  actions = [a for a in ["new", "add", "replace", "delete"] if args["--" + a]]
  if len(actions) == 0:
    action = DEFAULT_ACTION
  elif len(actions) == 1:
    action = actions[0]
  else:
    msg = "Only one of actions --new, --add, --replace, --delete can be used"
    logger.error(msg)
    exit(1)
  if not attrfname.exists():
    if action != "new":
      msg = "Attribute file {} does not exist".format(attrfname)
      logger.error(msg)
      exit(1)
  return action

def delete_from_existing(node_ids, existing, strict):
  for k in node_ids:
    k = int(k)
    if k in existing:
      del existing[k]
    elif args["--strict"]:
      logger.error(f"Node '{k}' not found in the tree")
      exit(1)

def add_to_existing(new_attrvalues, existing, strict):
  for k in new_attrvalues:
    if k in existing:
      if existing[k] is None:
        existing[k] = new_attrvalues[k]
      else:
        existing[k].extend(new_attrvalues[k])
    elif strict:
      logger.error(f"Node '{k}' not found in the tree")
      exit(1)

def replace_in_existing(new_attrvalues, existing, strict):
  replaced = set()
  for k in new_attrvalues:
    if k in existing:
      if existing[k] is None or (k not in replaced and args["--replace"]):
        existing[k] = new_attrvalues[k]
        replaced.add(k)
      else:
        existing[k].extend(new_attrvalues[k])
    elif strict:
      logger.error(f"Node '{k}' not found in the tree")
      exit(1)

def main(args):
  if not Path(args["<treefile>"]).exists():
    msg = "Tree file {} does not exist".format(args["<treefile>"])
    logger.error(msg)
    exit(1)
  attrfname = \
      Path(attribute.attrfilename(args["<treefile>"], args["<attribute>"]))
  action = get_action(args, attrfname)
  if action == "delete":
    if not args["<node_id>"]:
      attrfname.unlink(missing_ok=True)
      logger.info(f"Deleted attribute file {attrfname}")
      exit(0)
  else:
    generator, casting_fn = get_generator_and_casting_fn(args)
    new_attrvalues = defaultdict(list)
    for k, v in generator:
      new_attrvalues[int(k)].append(casting_fn(v))
  logger.debug("Loading tree from file '{}'".format(args['<treefile>']))
  tree = Tree.from_file(args["<treefile>"])
  if action != "new":
    existing = attribute.read_attribute_values(tree, attrfname)
    if action == "delete":
      delete_from_existing(args["<node_id>"], existing, args["--strict"])
    elif action == "add":
      add_to_existing(new_attrvalues, existing, args["--strict"])
    elif action == "replace":
      replace_in_existing(new_attrvalues, existing, args["--strict"])
    new_attrvalues = existing
  logger.debug("Writing attribute values to file '{}'...".format(attrfname))
  with open(attrfname, "w") as outfile:
    attribute.write_attribute_values(tree, new_attrvalues, outfile)

if __name__ == "__main__":
  args = docopt(__doc__, version=VERSION)
  _scripts_support.setup_verbosity(args)
  main(args)
