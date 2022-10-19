#!/usr/bin/env python3
"""
Manage attribute values for the NCBI taxonomy tree.

Usage:
  ntsubtree attribute [--new|--add|--replace] <attribute> <tabfile> [options]
  ntsubtree attribute [--new|--add|--replace] <attribute> --module M [<args>...] [options]
  ntsubtree attribute --delete <attribute> [<node_id>...] [options]
  ntsubtree attribute --list [options]

Actions:
  -N, --new        (default) create a new attribute
  -A, --add        add further values to an existing attribute
  -R, --replace    replace some values of an existing attribute
  -D, --delete     delete an attribute or attribute values
  -L, --list       list defined attributes

Tabular file input:
  <tabfile>        tabular file with node IDs and attribute values
  -s, --separator S    separator in the tabular file (default: tab)
  -e, --elementscol E  column with the IDs of the elements (1-based, default: 1)
  -v, --valuescol P    column with the attribute values (1-based, default: 2)
  -c, --commentchar C  lines starting with this character are ignored (default: #)

Module input:
  -m, --module M  select file <M> as a Python module defining a function
                  yielding element IDs and attribute values
  <args>...       arguments to be passed to the function;
                  if they contain a '=', they are passed as keyword arguments
  -F, --fn FN     name of the function to be called (default: attribute_values)
  -K, --nokeys    disable interpreting '=' in <args> as keyword arguments separator

Conversion of attribute values:
  -t, --type T   function to apply to the attribute values; either from the
                 standard library or defined in the specified --module M

Further options:
  -S, --strict   exit with an error if a node ID is not found in the tree
                 (default: ignore lines with non-existing node IDs)
  -q, --quiet    disable log messages
  -d, --debug    print debug information
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit
"""

from fastsubtrees.commands.attribute import manage_attribute
from pathlib import Path
import ntsubtree.constants

def main(args):
  treefile = ntsubtree.constants.TREEFILE
  if not Path(treefile).exists():
    ntsubtree.setup()
  tree = ntsubtree.get_tree()
  manage_attribute(args, tree)
