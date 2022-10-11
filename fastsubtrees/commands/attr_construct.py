#!/usr/bin/env python3
"""
Creates files for a given attribute present in the database

Usage:
  fastsubtrees attr construct [options] <tree> <attribute> <attrmod> [<attrmod_data>...]
  fastsubtrees attr construct [options] <tree> <attribute> --tab <tabfile> [<attrmod_data>...]

Arguments:
  tree          fastsubtrees tree representation file,
                e.g. output by fastsubtrees-construct
  attribute     name of the attribute
  attrmod       Python module defining a function attribute_values()
                which may take arguments (<attrmod_data>) and returns pairs
                (element_id, attribute_value) for each node to which an
                attribute value exists.
  tabfile       If the --tab option is used, the module
                fastsubtrees/ids_modules/attr_from_tabular_file.py is used;
                the tabfile argument in this case is the path to the tabular
                file containing the attribute values.
  attrmod_data  [optional] arguments to be passed to the attribute_values()
                function of the module specified as <attrmod>; to pass keyword
                arguments, use the syntax "key=value" and the option --keyargs

Options:
  --keyargs      split the arguments specified in <idsmod_data> into
                 keywords and values by splitting on the first instance of '=';
                 arguments which do not contain '=' are passed as positional,
                 before any keyword argument
  --tab          use a tabular file as source of input data;
                 shorthand for using the module
                 fastsubtrees/ids_modules/attr_from_tabular_file.py
  --quiet        disable log messages
  --debug        print debug information
  --help         show this help message and exit
  --version      show program's version number and exit
  --datatype DT  function to apply to the attribute values before writing
                 them to the output file; <DT> must be a valid Python function;
                 the function can optionally be defined in the module specified
                 by <attrmod> [default: str]
"""

from docopt import docopt
from fastsubtrees import _scripts_support, logger, Tree, attribute, VERSION
from collections import defaultdict
from pathlib import Path

def read_attribute_values(m, posargs, keyargs, cast):
  result = defaultdict(list)
  for k, v in m.attribute_values(*posargs, **keyargs):
    result[int(k)].append(cast(v))
  return result

def write_attribute_file(args, attrvalues):
  logger.debug("Loading tree from file '{}'".format(args['<tree>']))
  tree = Tree.from_file(args["<tree>"])
  outfname = attribute.attrfilename(args["<tree>"], args["<attribute>"])
  logger.debug("Writing attribute values to file '{}'...".format(outfname))
  with open(outfname, "w") as outfile:
    attribute.write_attribute_values(tree, attrvalues, outfile)
  logger.success("Attribute values successfully written to file '{}'".\
      format(outfname))

def main(args):
  if args["--tab"]:
    import fastsubtrees.ids_modules.attr_from_tabular_file as m
    args["<attrmod_data>"] = [args["<tabfile>"]] + args["<attrmod_data>"]
  else:
    m = _scripts_support.get_module(args["<attrmod>"], "attribute_values")
  posargs, keyargs = _scripts_support.get_fn_args(\
                          args["--keyargs"], args["<attrmod_data>"])
  cast = _scripts_support.get_datatype_casting_fn(args["--datatype"], m, \
                                                  args["<attrmod>"])
  attrvalues = read_attribute_values(m, posargs, keyargs, cast)
  write_attribute_file(args, attrvalues)

if __name__ == "__main__":
  args = docopt(__doc__, version=VERSION)
  _scripts_support.setup_verbosity(args)
  main(args)