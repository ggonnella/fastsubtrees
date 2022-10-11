#!/usr/bin/env python3
"""
Construct a tree data structure for fast subtrees queries.

The tree information is obtained in one of these ways:

- simplified mode for NCBI taxonomy:
  by using the NCBI taxonomy dump files and the --ntdump option

- tabular file mode:
  by using the --tab option and a TAB-separated tabular file as input,
  with two columns: the first one contains
  the element ID, the second one contains the parent ID.

- generic mode:
  by using the specified Python module "idsmod" (see below)
  and passing the specified positional or keyword arguments
  (if --keyargs is used)

Usage:
  fastsubtrees construct [options] <outfname> <idsmod> [<idsmod_data>...]
  fastsubtrees construct [options] <outfname> --ntdump <ntdumpdir>
  fastsubtrees construct [options] <outfname> --tab <tabfile>

Common arguments:
  outfname     desired name for the output file

Arguments for NCBI taxonomy simplified mode:
  ntdumpdir    directory containing NCBI taxonomy dump files

Arguments for tabular file mode:
  tabfile      tabular file containing the tree information in two columns
               (element ID <TAB> parent ID)

Arguments for generic mode:
  idsmod       Python module defining a function element_parent_ids()
               which may take arguments (<idsmod_data>) and yield pairs
               of IDs for all tree nodes (element_id, parent_id).
               For the root node, the parent_id shall be equal to the
               element_id.
  idsmod_data  [optional] arguments to be passed to the element_parent_ids()
               function of the module specified as <idsmod>; to pass keyword
               arguments, use the syntax "key=value" and the option --keyargs

Options:
  --ntdump     use the NCBI taxonomy simplified mode (see above)
               to construct the tree from NCBI taxonomuy dump files
  --tab        use the tabular file mode (see above) to construct the tree
               from a TAB-separated tabular file
  --keyargs    split the arguments specified in <idsmod_data> into
               keywords and values by splitting on the first instance of '=';
               arguments which do not contain '=' are passed as positional,
               before any keyword argument
  --keepattr   keep existing attribute files (if any) for the output file
  --quiet      disable log messages
  --debug      print debug information
  --help       show this help message and exit
  --version    show program's version number and exit
"""

NCBI_DUMP_SEP = "\t|\t"
NCBI_DUMP_TAXID_COL = 0
NCBI_DUMP_PARENT_COL = 1

import importlib
from docopt import docopt
from pathlib import Path
from fastsubtrees import Tree, logger, _scripts_support, VERSION, attribute

def main(args):
  if args['--ntdump']:
    filename = Path(args['<ntdumpdir>']) / 'nodes.dmp'
    logger.info(f'Constructing tree from NCBI taxonomy dump file {filename}')
    tree = Tree.construct_from_csv(str(filename), NCBI_DUMP_SEP,
                      NCBI_DUMP_TAXID_COL, NCBI_DUMP_PARENT_COL)
  elif args['--tab']:
    filename = Path(args['<tabfile>'])
    logger.info(f'Constructing tree from tabular file {filename}')
    tree = Tree.construct_from_csv(str(filename), "\t", 0, 1)
  else:
    m = _scripts_support.get_module(args['<idsmod>'], 'element_parent_ids')
    logger.info("Constructing tree using IDs yielded by the generator...")
    posargs, keyargs = _scripts_support.get_fn_args(\
                          args["--keyargs"], args["<idsmod_data>"])
    tree = Tree.construct(m.element_parent_ids(*posargs, **keyargs))
  logger.success("Tree constructed")
  tree.to_file(args["<outfname>"])
  if not args["--keepattr"]:
    for fname in attribute.attrfiles(args["<outfname>"]).values():
      logger.info("Removing obsolete attribute file %s", fname)
      Path(fname).unlink()

if __name__ == "__main__":
  args = docopt(__doc__, version=VERSION)
  _scripts_support.setup_verbosity(args)
  main(args)