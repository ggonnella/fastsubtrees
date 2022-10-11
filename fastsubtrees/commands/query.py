#!/usr/bin/env python3
"""
List all IDs of a subtree under a given node.

It uses as input a tree representation constructed
by this library and stored to file (<tree>).

Usage:
  fastsubtrees query [options] <tree> <subtreeroot>

Arguments:
  tree         tree representation file
               (e.g. output of fastsubtrees-construct script)
  subtreeroot  ID of the subtree root

Options:
  --quiet      disable log messages
  --debug      print debug information
  --help       show this help message and exit
  --version    show program's version number and exit
"""

from docopt import docopt
from fastsubtrees import Tree, logger, _scripts_support, VERSION

def main(args):
  logger.debug(f"Loading tree file '{args['<tree>']}'")
  tree = Tree.from_file(args["<tree>"])
  logger.debug(f"Extracting subtree under node '{args['<subtreeroot>']}'")
  for node_id in tree.subtree_ids(int(args["<subtreeroot>"])):
    print(node_id)

if __name__ == "__main__":
  args = docopt(__doc__, version=VERSION)
  _scripts_support.setup_verbosity(args)
  main(args)