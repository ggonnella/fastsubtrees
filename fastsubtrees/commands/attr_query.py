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
  --nones      do not filter out None values in the output
  --counts     count the number of nodes with attributes and of attribute values
  --debug      print debug information
  --help       show this help message and exit
  --version    show program's version number and exit
"""
from docopt import docopt
from fastsubtrees import Tree, logger, _scripts_support, VERSION, attribute

def print_results(results):
  for result in results:
    if isinstance(result, list):
      print(", ".join(str(r) for r in result))
    else:
      print(result)

def main(args):
  logger.debug("Loading tree from file '{}'".format(args['<tree>']))
  tree = Tree.from_file(args["<tree>"])
  subtree_root = int(args["<subtreeroot>"])
  attributefile = attribute.attrfilename(args["<tree>"], args["<attribute>"])
  logger.debug("Loading attribute '{}' values from file '{}'".\
      format(args["<attribute>"], attributefile))
  attribute_list = attribute.get_attribute_list(tree, subtree_root, \
      attributefile)
  filtered = None
  if (not args["--nones"]) or args["--counts"]:
    filtered = [a for a in attribute_list if a is not None]
    if args["--counts"]:
      count = len(filtered)
      logger.info("Number of nodes with attributes: {}".format(count))
      flattened = [e for sl in filtered for e in sl]
      count = len(flattened)
      logger.info("Number of attribute values: {}".format(count))
  if args["--nones"]:
    print_results(attribute_list)
  else:
    print_results(filtered)

if __name__ == "__main__":
  args = docopt(__doc__, version=VERSION)
  _scripts_support.setup_verbosity(args)
  main(args)
