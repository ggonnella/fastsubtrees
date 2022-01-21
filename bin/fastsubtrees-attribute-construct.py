#!/usr/bin/env python3
"""
Return the list of IDs of the subtree of a tree
previously constructed and stored to file by this library

Usage:
  fastsubtrees-attribute-construct [options] <inputfile> <subtree_root> <attributesfile>

Arguments:
  <inputfile>       Output of fastsubtrees-construct
  <subtree_root>    ID of the subtree root
  <attributesfile>  Name of all the attribute values whose value is to be found

Options:
  --quiet      be quiet
  --debug      print debug messages
"""
import json

from docopt import docopt
from fastsubtrees import Tree, _scripts_support, Attributes


def main():
    attr = Attributes()
    # result = attr.get_attribute_list(args["<inputfile>"], args["<subtree_root>"], args["<attributesfile>"])
    # print(result)
    file = open(args["<attributesfile>"])
    data = json.load(file)
    for d in data:
        result = attr.get_attribute_list(args["<inputfile>"], args["<subtree_root>"], d)
        # attr.create_json_file(args["<attribute>"], result)


if __name__ == "__main__":
    args = docopt(__doc__, version="0.1")
    _scripts_support.setup_verbosity(args)
    main()
