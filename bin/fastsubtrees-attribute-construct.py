#!/usr/bin/env python3
"""
Creates individual json files for all the attributes
present in the database

Usage:
  fastsubtrees-attribute-construct.py [options] <outputfile> <subtreeroot> <attributesfile> <pythonmodule>

Arguments:
  <outputfile>      Output of fastsubtrees-construct
  <subtreeroot>     ID of the root of the Tree
  <attributesfile>  File containing a list of all atrributes present in the database
  <pythonmodule>    Some module for python which defines the function for getting the attribute values
                    called get_attributes_list

Options:
  --quiet      be quiet
  --debug      print debug messages
"""
import json
from docopt import docopt
from fastsubtrees import Tree, _scripts_support
import importlib
from pathlib import Path

def main():
    modulename = Path(args["<pythonmodule>"]).stem
    spec = importlib.util.spec_from_file_location(modulename, args["<pythonmodule>"])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    attr = m.Attributes()
    file = open(args["<attributesfile>"])
    data = json.load(file)
    for d in data:
        result = attr.get_attribute_list(args["<outputfile>"], args["<subtreeroot>"], d)
        attr.create_json_file(str(d), result)


if __name__ == "__main__":
    args = docopt(__doc__, version="0.1")
    _scripts_support.setup_verbosity(args)
    main()
