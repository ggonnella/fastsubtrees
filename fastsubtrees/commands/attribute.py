#!/usr/bin/env python3
"""
Manage attribute values for trees.

creation mode (default):
  Given a source of attribute values, it will create a new attribute file
  for the given tree, replacing any existing file.

add mode (--add option):
  Given a source of attribute values, it will add further values to the
  attribute file for the given tree. If a node already has values for
  the attribute, the new values will be appended to the existing one.

replace mode (--replace option):
  Given a source of attribute values, it will set values to the
  attribute file for the given tree. If a node already has values for
  the attribute, the new values will replace the existing one.

delete mode (--delete option):
  Delete the attribute file for the given tree, or, if one or more
  node IDs are given, delete the attribute values for those nodes.

Usage:
  fastsubtrees attribute [options] <tree> <attribute> --tab <tabfile> [<attrmod_data>...]
  fastsubtrees attribute [options] <tree> <attribute> <attrmod> [<attrmod_data>...]
  fastsubtrees attribute [options] <tree> <attribute> --delete [<node_id>...]

Using a tabular file as source of attribute values:

  To use a tabular file <tabfile> as source of IDs, use the --tab option.
  The file shall contain lines in the form "node_id <TAB> parent_id".

  Optional arguments after <tabfile> are given in this order
  or passed as key=value:
    - id_col: column index of the element ID (default: 0)
    - attr_col: column index of the attribute value (default: 1)
    - separator: separator (default: tab)
    - comment_pfx: prefix of lines to be skipped (default: '#')

Using an attribute values source module:

  The <attrmod> argument is the path to a Python module.
  The module must have a function named attribute_values which yields
  tuples (node_id, attribute_value).

  The <attrmod_data> arguments are passed to the attribute_values function.
  If they contain a = sign, they are interpreted as keyword arguments.

Options:
  --replace      replace attribute values in an existing file
  --add          add new attribute values to an existing file
  --strict       exit with an error if a node ID is not found in the tree
  --delete       delete attribute values from an existing file
  --tab          use a tabular file as source of input data;
                 shorthand for using the module
                 fastsubtrees/ids_modules/attr_from_tabular_file.py
  --quiet        disable log messages
  --debug        print debug information
  --help         show this help message and exit
  --version      show program's version number and exit
  --datatype DT  function to apply to the attribute values before writing
                 them to the output file; <DT> must be a valid Python function;
                 the function can optionally be defined in the module specified
                 by <attrmod> [default: str]
"""

from docopt import docopt
from fastsubtrees import _scripts_support, logger, Tree, attribute, VERSION
from collections import defaultdict
from pathlib import Path

def read_attribute_values(m, posargs, keyargs, cast):
  result = defaultdict(list)
  for k, v in m.attribute_values(*posargs, **keyargs):
    result[int(k)].append(cast(v))
  return result

def write_attribute_file(args, attrvalues):
  logger.debug("Loading tree from file '{}'".format(args['<tree>']))
  tree = Tree.from_file(args["<tree>"])
  outfname = attribute.attrfilename(args["<tree>"], args["<attribute>"])
  if args["--add"] or args["--replace"] or args["--delete"]:
    existing = attribute.read_attribute_values(tree, outfname)
    if args["--add"] or args["--replace"]:
      replaced = set()
      for k in attrvalues:
        if k not in existing:
          if args["--strict"]:
            raise ValueError("Node {} does not exist".format(k))
          else:
            continue
        elif existing[k] is None or (k not in replaced and args["--replace"]):
          existing[k] = attrvalues[k]
          replaced.add(k)
        else:
          existing[k].extend(attrvalues[k])
    else:
      for k in args["<node_id>"]:
        k = int(k)
        if k not in existing:
          logger.warning("Node '{}' not found in the tree".format(k))
        else:
          del existing[k]
    attrvalues = existing
  logger.debug("Writing attribute values to file '{}'...".format(outfname))
  with open(outfname, "w") as outfile:
    attribute.write_attribute_values(tree, attrvalues, outfile)

def main(args):
  if args["--delete"]:
    if args['<node_id>']:
      write_attribute_file(args, [])
    else:
      outfname = attribute.attrfilename(args["<tree>"], args["<attribute>"])
      Path(outfname).unlink(missing_ok=True)
      logger.info("Deleted attribute file %s", outfname)
  else:
    if args["--tab"]:
      import fastsubtrees.ids_modules.attr_from_tabular_file as m
      args["<attrmod_data>"] = [args["<tabfile>"]] + args["<attrmod_data>"]
    else:
      m = _scripts_support.get_module(args["<attrmod>"], "attribute_values")
    posargs, keyargs = _scripts_support.get_fn_args(\
       True, args["<attrmod_data>"])
    cast = _scripts_support.get_datatype_casting_fn(args["--datatype"], m, \
                                                    args["<attrmod>"])
    attrvalues = read_attribute_values(m, posargs, keyargs, cast)
    write_attribute_file(args, attrvalues)

if __name__ == "__main__":
  args = docopt(__doc__, version=VERSION)
  _scripts_support.setup_verbosity(args)
  main(args)
