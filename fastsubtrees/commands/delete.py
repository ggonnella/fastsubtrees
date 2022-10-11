#!/usr/bin/env python3
"""
Parse a given tabular file and delete a given node
from the the tree

Usage:
  fastsubtrees delete [options] <tree> <nodeid>

Arguments:
  tree        File containing the tree data
  nodeid      ID of the node that has to be deleted

Options:
  --quiet      disable log messages
  --debug      print debug information
  --help       show this help message and exit
  --version    show program's version number and exit
"""

from docopt import docopt
from fastsubtrees import Tree, logger, _scripts_support, VERSION, attribute

def main(args):
  logger.debug("Loading tree from file '{}'".format(args['<tree>']))
  tree = Tree.from_file(args["<tree>"])
  logger.debug("Successfully loaded tree from file '{}'".format(args['<tree>']))
  attrfiles = attribute.attrfiles(args["<tree>"]).values()
  logger.debug("Modifying attribute files: '{}'".format("', '".join(attrfiles)))
  tree.delete_node(int(args["<nodeid>"]), attrfiles)
  logger.success("Node deleted successfully")
  tree.to_file(args["<tree>"])

if __name__ == "__main__":
  args = docopt(__doc__, version=VERSION)
  _scripts_support.setup_verbosity(args)
  main(args)
