#!/usr/bin/env python3
"""
List the values of a specified attribute in a specified subtree

Usage:
  fastsubtrees attr query [options] <tree> <attribute> <subtreeroot>

Arguments:
  tree           fastsubtrees-construct output
  attribute      name of the attribute
  subtreeroot    ID of the subtree root

Options:
  --quiet      disable log messages
  --ids        show node IDs alongside the attribute values
               (output format: node_id <TAB> attribute_value)
  --nones      do not filter out None values in the output
  --counts     count the number of nodes with attributes and of attribute values
  --debug      print debug information
  --help       show this help message and exit
  --version    show program's version number and exit
"""
from docopt import docopt
from fastsubtrees import Tree, logger, _scripts_support, VERSION, attribute

def main(args):
  logger.debug("Loading tree from file '{}'".format(args['<tree>']))
  tree = Tree.from_file(args["<tree>"])
  subtree_root = int(args["<subtreeroot>"])
  attributefile = attribute.attrfilename(args["<tree>"], args["<attribute>"])
  logger.debug("Loading attribute '{}' values from file '{}'".\
      format(args["<attribute>"], attributefile))
  attribute_list = attribute.get_attribute_list(tree, subtree_root, \
      attributefile)
  if args["--counts"]:
    filtered = [a for a in attribute_list if a is not None]
    if args["--counts"]:
      count = len(filtered)
      logger.info("Number of nodes with attributes: {}".format(count))
      flattened = [e for sl in filtered for e in sl]
      count = len(flattened)
      logger.info("Number of attribute values: {}".format(count))
  node_ids = tree.subtree_ids(subtree_root) if args["--ids"] else None
  for i, result in enumerate(attribute_list):
    if result is None and not args["--nones"]:
      continue
    if isinstance(result, list):
      attrstr = ", ".join(str(r) for r in result)
    else:
      attrstr = str(result)
    if node_ids:
      node_id = node_ids[i]
      print("{}\t{}".format(node_id, attrstr))
    else:
      print(attrstr)

if __name__ == "__main__":
  args = docopt(__doc__, version=VERSION)
  _scripts_support.setup_verbosity(args)
  main(args)
