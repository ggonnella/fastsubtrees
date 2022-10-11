#!/usr/bin/env python3
"""
Delete values of an attribute for specific nodes

Usage:
  fastsubtrees attr delete [options] <tree> <attribute> <node>...

Arguments:
  tree          fastsubtrees tree representation file,
                e.g. output by fastsubtrees-construct
  attribute     name of the attribute
  node          node IDs to delete attribute values for

Options:
  --quiet        disable log messages
  --debug        print debug information
  --help         show this help message and exit
  --version      show program's version number and exit
  --all          remove the attribute for all nodes
"""

from docopt import docopt
from fastsubtrees import _scripts_support, logger, Tree, attribute, VERSION
from collections import defaultdict
from pathlib import Path

def main(args):
  outfname = attribute.attrfilename(args["<tree>"], args["<attribute>"])
  if args['--all']:
    Path(outfname).unlink(missing_ok=True)
    logger.success("Deleted attribute file %s", outfname)
  else:
    logger.debug("Loading tree from file '{}'".format(args['<tree>']))
    tree = Tree.from_file(args["<tree>"])
    logger.debug("Reading existing attribute values from file '{}'".\
        format(outfname))
    attrvalues = attribute.read_attribute_values(tree, outfname)
    for k in args["<node>"]:
      k = int(k)
      if k not in attrvalues:
        logger.warning("Node '{}' not found in the tree".format(k))
      else:
        del attrvalues[k]
    with open(outfname, "w") as outfile:
      attribute.write_attribute_values(tree, attrvalues, outfile)
    logger.success("Attribute values rewritten to file '{}'".\
        format(outfname))

if __name__ == "__main__":
  args = docopt(__doc__, version=VERSION)
  _scripts_support.setup_verbosity(args)
  main(args)
