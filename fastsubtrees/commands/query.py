#!/usr/bin/env python3
"""
List IDs and/or attributes of a subtree under a given node.

Usage:
  fastsubtrees query [options] <tree> <subtreeroot> [<attribute>...]

Arguments:
  tree         tree representation file
               (output of fastsubtrees construct)
  subtreeroot  ID of the subtree root
               (use 'root' for the root of the tree)
  attribute    Attributes to be printed for each node

Options:
  -s, --stats            show subtree statistics
  -a, --attributes-only  do not print node IDs (only attributes)
  -m, --missing          print None for missing attributes in -a mode
  -H, --no-header        do not print header line
  -S, --separator SEP    use SEP as separator [default: \t]
  -p, --parents          show parents of nodes
  -z, --subtree-sizes    show size of subtree under each nodes
                         (including nodes marked as deleted!)
  -o, --only             show only selected node, not the subtree
  -q, --quiet            disable log messages
  -d, --debug            print debug information
  -h, --help             show this help message and exit
  -V, --version          show program's version number and exit
"""

from fastsubtrees import Tree, logger

def check_attribute_args(args):
  attrnames = args["<attribute>"]
  if attrnames:
    logger.debug("Attributes to be printed: {}".format(", ".join(attrnames)))
  else:
    logger.debug("Printing only IDs, no attributes")
    if args["--attributes-only"]:
      logger.error("Cannot use --attributes-only without attributes")
      exit(1)
  if args["--attributes-only"]:
    logger.debug("Printing only attributes, no IDs")
    if args["--missing"]:
      logger.debug("Showing None for nodes without attribute values")
    else:
      logger.debug("Hiding nodes without attribute values")
  else:
    args["--missing"] = True
  return attrnames

def show_header(args, attrnames):
  if not args["--no-header"]:
    header_data = []
    if not args["--attributes-only"]:
      header_data.append("node_id")
    if args["--parents"]:
      header_data.append("parent")
    if args["--subtree-sizes"]:
      header_data.append("subtree_size")
    header_data.extend(attrnames)
    print("# "+args["--separator"].join(header_data))

def show_data(args, subtree_info, attrnames):
  n_nodes = 0
  for i, node_id in enumerate(subtree_info["node_id"]):
    if args["--only"] and node_id != int(args["<subtreeroot>"]):
      continue
    if node_id == Tree.UNDEF:
      continue
    n_nodes += 1
    if not args["--missing"] and \
        all([subtree_info[attrname][i] is None for attrname in attrnames]):
      continue
    line_data = []
    if not args["--attributes-only"]:
      line_data.append(str(node_id))
    if args["--parents"]:
      line_data.append(str(subtree_info["parent"][i]))
    if args["--subtree-sizes"]:
      line_data.append(str(subtree_info["subtree_size"][i]))
    for attrname in attrnames:
      value = subtree_info[attrname][i]
      if isinstance(value, list):
        line_data.append(", ".join([str(v) for v in value]))
      else:
        line_data.append(str(value))
    print(args["--separator"].join(line_data))
  if args["--stats"]:
    logger.info("Number of nodes in subtree: {}".format(n_nodes))

def run_query(args, tree):
  if args["<subtreeroot>"] == "root":
    subtree_root = tree.root_id
  else:
    subtree_root = int(args["<subtreeroot>"])
  logger.debug(f"Extracting subtree under node '{subtree_root}'")
  attrnames = check_attribute_args(args)
  if not tree.check_has_attributes(attrnames):
    exit(1)
  subtree_info = tree.subtree_info(subtree_root, attrnames,
      args["--subtree-sizes"], args["--parents"], args["--stats"])
  show_header(args, attrnames)
  show_data(args, subtree_info, attrnames)

def main(args):
  logger.debug("Loading tree from file '{}'".format(args['<tree>']))
  tree = Tree.from_file(args["<tree>"])
  run_query(args, tree)
