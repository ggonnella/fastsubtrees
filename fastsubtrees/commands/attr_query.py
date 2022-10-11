#!/usr/bin/env python3
"""
List the values of a specified attribute in a specified subtree

Usage:
  fastsubtrees attr query [options] <tree> <attribute> <subtreeroot>

Arguments:
  tree           fastsubtrees-construct output
  attribute      name of one or multiple attributes (comma separated);
                 if multiple attributes are specified, the values are
                 output separated by tabs
  subtreeroot    ID of the subtree root

Options:
  --quiet      disable log messages
  --ids        show node IDs alongside the attribute values
               (output format: node_id <TAB> attribute_value)
  --nones      do not filter out None values in the output
  --counts     count the number of nodes with attributes and of attribute values
  --debug      print debug information
  --help       show this help message and exit
  --version    show program's version number and exit
"""
from docopt import docopt
from fastsubtrees import Tree, logger, _scripts_support, VERSION, attribute

def main(args):
  logger.debug("Loading tree from file '{}'".format(args['<tree>']))
  tree = Tree.from_file(args["<tree>"])
  subtree_root = int(args["<subtreeroot>"])
  attribute_list = {}
  attrnames = args["<attribute>"].split(",")
  for attrname in attrnames:
    attributefile = attribute.attrfilename(args["<tree>"], attrname)
    logger.debug("Loading attribute '{}' values from file '{}'".\
        format(attrname, attributefile))
    attribute_list[attrname] = attribute.get_attribute_list(tree, subtree_root, \
        attributefile)
    if args["--counts"]:
      filtered = [a for a in attribute_list[attrname] if a is not None]
      flattened = [e for sl in filtered for e in sl]
      logger.info("Attribute '{}'".format(attrname))
      logger.info("Number of nodes with attributes: {}".format(len(filtered)))
      logger.info("Number of attribute values: {}".format(len(flattened)))
  node_ids = tree.subtree_ids(subtree_root) if args["--ids"] else None
  if node_ids or len(attrnames) > 1:
    header_data = []
    if node_ids:
      header_data.append("node_id")
    header_data.extend(attrnames)
    print("# "+"\t".join(header_data))
  for i, result0 in enumerate(attribute_list[attrnames[0]]):
    if result0 is None and not args["--nones"]:
      all_none = True
      for attrname in attrnames[1:]:
        if attribute_list[attrname][i] is not None:
          all_none = False
          break
      if all_none:
        continue
    line_data = []
    if node_ids:
      line_data.append(str(node_ids[i]))
    for attrname in attrnames:
      value = attribute_list[attrname][i]
      if isinstance(value, list):
        line_data.append(", ".join([str(v) for v in value]))
      else:
        line_data.append(str(value))
    print("\t".join(line_data))

if __name__ == "__main__":
  args = docopt(__doc__, version=VERSION)
  _scripts_support.setup_verbosity(args)
  main(args)
