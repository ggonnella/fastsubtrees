#!/usr/bin/env python3
"""
List IDs and/or attributes of a subtree under a given node.

Usage:
  fastsubtrees query [options] <tree> <subtreeroot> [<attribute>...]

Arguments:
  tree         tree representation file
               (output of fastsubtrees construct)
  subtreeroot  ID of the subtree root
  attribute    Attributes to be printed for each node

Options:
  -q, --quiet            disable log messages
  -d, --debug            print debug information
  -s, --stats            show subtree statistics
  -a, --attributes-only  do not print node IDs (only attributes)
  -n, --show-none        print None for missing attributes in -a mode
  -N, --no-header        do not print header line
  -s, --separator SEP    use SEP as separator [default: \t]
  -h, --help             show this help message and exit
  -V, --version          show program's version number and exit
"""

import os
from docopt import docopt
from fastsubtrees import Tree, logger, _scripts_support, VERSION, attribute

def check_attribute_args(args):
  attrnames = args["<attribute>"]
  if attrnames:
    logger.debug("Attributes to be printed: {}".format(", ".join(attrnames)))
  else:
    logger.debug("Printing only IDs, no attributes")
    if args["--attributes-only"]:
      logger.error("Cannot use --attributes-only without attributes")
      exit(1)
  if args["--attributes-only"]:
    logger.debug("Printing only attributes, no IDs")
    if args["--show-none"]:
      logger.debug("Showing None for nodes without attribute values")
    else:
      logger.debug("Hiding nodes without attribute values")
  else:
    args["--show-none"] = True
  return attrnames

def get_attribute_values(attrnames, tree, subtree_root, args):
  attr_values = {}
  for attrname in attrnames:
    attributefile = attribute.attrfilename(args["<tree>"], attrname)
    if not os.path.isfile(attributefile):
      logger.error("Attribute '{}' not found".format(attrname))
      exit(1)
    logger.debug("Loading attribute '{}' values from file '{}'".\
        format(attrname, attributefile))
    attr_values[attrname] = attribute.get_attribute_list(tree, subtree_root, \
        attributefile)
    if args["--stats"]:
      filtered = [a for a in attr_values[attrname] if a is not None]
      flattened = [e for sl in filtered for e in sl]
      logger.info("Number of nodes with attribute '{}': {}".\
          format(attrname, len(filtered)))
      logger.info("Number of values of attribute '{}': {}".\
          format(attrname, len(flattened)))
  return attr_values

def show_header(attrnames, attributes_only):
  header_data = []
  if not attributes_only:
    header_data.append("node_id")
  header_data.extend(attrnames)
  print("# "+"\t".join(header_data))

def show_results(args, node_ids, attr_values, attrnames):
  if not args["--separator"]:
    args["--separator"] = "\t"
  for i, node_id in enumerate(node_ids):
    if not args["--show-none"] and \
        all([attr_values[attrname][i] is None for attrname in attrnames]):
      continue
    line_data = []
    if not args["--attributes-only"]:
      line_data.append(str(node_id))
    for attrname in attrnames:
      value = attr_values[attrname][i]
      if isinstance(value, list):
        line_data.append(", ".join([str(v) for v in value]))
      else:
        line_data.append(str(value))
    print(args["--separator"].join(line_data))

def main(args):
  logger.debug("Loading tree from file '{}'".format(args['<tree>']))
  tree = Tree.from_file(args["<tree>"])
  subtree_root = int(args["<subtreeroot>"])
  logger.debug(f"Extracting subtree under node '{subtree_root}'")
  attrnames = check_attribute_args(args)
  node_ids = tree.subtree_ids(subtree_root)
  if args["--stats"]:
    logger.info("Number of nodes in subtree: {}".format(len(node_ids)))
  attr_values = get_attribute_values(attrnames, tree, subtree_root, args)
  if not args["--no-header"]:
    show_header(attrnames, args["--attributes-only"])
  show_results(args, node_ids, attr_values, attrnames)

if __name__ == "__main__":
  args = docopt(__doc__, version=VERSION)
  _scripts_support.setup_verbosity(args)
  main(args)
