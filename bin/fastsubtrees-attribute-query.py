#!/usr/bin/env python3
"""
Return the list of values for the given attribute for
a particular subtree

Usage:
  fastsubtrees-attribute-query.py [options] <outputfile> <subtree_root> <attributefile>

Arguments:
  <outputfile>    Output of fastsubtrees-construct
  <subtree_root>  ID of the subtree root
  <attributefile> Output of fastsubtrees-attribute-construct for a particular attribute

Options:
  --quiet      be quiet
  --debug      print debug messages
"""
import json
from docopt import docopt
from fastsubtrees import Tree, _scripts_support

def get_attribute_value(self, attributefile, subtree_size, position):
  file = open(attributefile)
  data = json.load(file)
  attribute_value_list = list()
  for i in range(position, (position + subtree_size)):
    attribute_value_list.append(data[i])
  return attribute_value_list

def main():
  tree = Tree.from_file(args["<outputfile>"])
  subtree_root = int(args["<subtree_root>"])
  treedata, position, subtree_size = tree.query_subtree(subtree_root)
  attribute_list = get_attribute_value(args["<attributefile>"], subtree_size+1, position-1)
  print(attribute_list)


if __name__ == "__main__":
  args = docopt(__doc__, version="0.1")
  _scripts_support.setup_verbosity(args)
  main()
