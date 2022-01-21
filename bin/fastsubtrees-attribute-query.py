#!/usr/bin/env python3
"""
Return the list of IDs of the subtree of a tree
previously constructed and stored to file by this library

Usage:
  fastsubtrees-query [options] <inputfile> <subtree_root> <attributefile>

Arguments:
  <inputfile>     Output of fastsubtrees-construct
  <subtree_root>  ID of the subtree root
  <attributefile> Output of fastsubtrees-attribute-construct

Options:
  --quiet      be quiet
  --debug      print debug messages
"""

from docopt import docopt
from fastsubtrees import Tree, _scripts_support, Attributes

def main():
  tree = Tree.from_file(args["<inputfile>"])
  subtree_root = int(args["<subtree_root>"])
  treedata, position, subtree_size = tree.subtree_ids(subtree_root)
  attr = Attributes()
  al = attr.get_attribute_value(args["<attributefile>"], subtree_size+1, position-1)
  print(al)

if __name__ == "__main__":
  args = docopt(__doc__, version="0.1")
  _scripts_support.setup_verbosity(args)
  main()
