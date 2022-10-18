#!/usr/bin/env python3
"""
List IDs and/or attributes of a subtree under a given node.

Usage:
  ntsubtree query [options] <subtreeroot> [<attribute>...]

Arguments:
  subtreeroot  ID of the subtree root
               (use 'root' for the root of the tree)
  attribute    Attributes to be printed for each node

Options:
  -n, --by-name          search for the subtree root by name
  -T, --no-taxname       do not print taxnames
  -s, --stats            show subtree statistics
  -a, --attributes-only  do not print taxa IDs (only attributes)
  -m, --missing          print None for missing attributes in -a mode
  -H, --no-header        do not print header line
  -S, --separator SEP    use SEP as separator [default: \t]
  -p, --parents          show taxa IDs of parents of nodes
  -z, --subtree-sizes    show size of subtree under each nodes
                         (including nodes marked as deleted!)
  -o, --only             show only selected node, not the subtree
  -q, --quiet            disable log messages
  -d, --debug            print debug information
  -h, --help             show this help message and exit
  -V, --version          show program's version number and exit
"""

from pathlib import Path
from fastsubtrees import logger
from fastsubtrees.commands.query import run_query
from ntsubtree import get_tree, setup
import ntsubtree.constants

def main(args):
  treefile = ntsubtree.constants.TREEFILE
  if not Path(treefile).exists():
    ntsubtree.setup()
  if args['--by-name']:
    args['<subtreeroot>'] = ntsubtree.search_name(args['<subtreeroot>'])
    if args['<subtreeroot>'] is None:
      logger.error("No node found with name '{}'".format(args['<subtreeroot>']))
      exit(1)
  tree = ntsubtree.get_tree()
  if not args['--no-taxname']:
    if "taxname" not in args["<attribute>"]:
      args["<attribute>"].insert(0, "taxname")
  run_query(args, tree)
