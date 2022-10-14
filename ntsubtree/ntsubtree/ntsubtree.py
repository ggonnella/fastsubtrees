import fastsubtrees
import fastsubtrees.ids_modules.ids_from_tabular_file as ids_from_tabular_file
from ntdownload import Downloader
from pathlib import Path

from .constants import \
   NCBI_NODES_DUMP_TAXID_COL, NCBI_NODES_DUMP_PARENT_COL, \
   NCBI_NAMES_DUMP_TAXID_COL, NCBI_NAMES_DUMP_NAME_COL, \
   NCBI_NAMES_DUMP_CLASS_COL, NCBI_NAMES_DUMP_CLASS_SCIENTIFIC, \
   NCBI_NAMES_DUMP_FILENAME, NCBI_NODES_DUMP_FILENAME, \
   NTDUMPSDIR, TREEFILE, NCBI_DUMP_SEP, APPDATADIR

def read_names():
  names_dump = NTDUMPSDIR / NCBI_NAMES_DUMP_FILENAME
  fastsubtrees.logger.info("Extracting taxonomic names")
  names = {}
  with open(names_dump, 'r') as f:
    for line in f:
      fields = line.split(NCBI_DUMP_SEP)
      if fields[NCBI_NAMES_DUMP_CLASS_COL].\
          startswith(NCBI_NAMES_DUMP_CLASS_SCIENTIFIC):
        names[int(fields[NCBI_NAMES_DUMP_TAXID_COL])] = \
                                  fields[NCBI_NAMES_DUMP_NAME_COL]
  return names

def n_lines(filename):
  n = 0
  with open(filename, 'r') as f:
    for _ in f:
      n += 1
  return n

def update(redownload=False, force=False):
  fastsubtrees.PROGRESS_ENABLED = True
  fastsubtrees.enable_logger("INFO")
  fastsubtrees.logger.info("Updating ntsubtree data (this may take a while)")
  fastsubtrees.logger.info("Data directory: {}".format(APPDATADIR))
  fastsubtrees.logger.info("Downloading NCBI taxonomy data...")
  NTDUMPSDIR.mkdir(parents=True, exist_ok=True)
  if redownload:
    for f in NTDUMPSDIR.glob("*"):
      f.unlink()
  updated = Downloader(str(NTDUMPSDIR)).run()
  if updated or force:
    fastsubtrees.logger.info("Updating taxonomy tree...")
    tree = fastsubtrees.Tree.from_file(TREEFILE)
    n_node_lines = n_lines(NTDUMPSDIR / NCBI_NODES_DUMP_FILENAME)
    fastsubtrees.logger.info("Number of nodes: {}".format(n_node_lines))
    generator = ids_from_tabular_file.element_parent_ids(\
        str(NTDUMPSDIR / NCBI_NODES_DUMP_FILENAME), separator=NCBI_DUMP_SEP,
        element_id_column=NCBI_NODES_DUMP_TAXID_COL,
        parent_id_column=NCBI_NODES_DUMP_PARENT_COL)
    if tree.has_attribute("taxname"):
      tree.destroy_attribute("taxname")
    n_added, n_deleted, n_moved = tree.update(generator, total=n_node_lines)
    tree.to_file(TREEFILE)
    tree.save_attribute_values(tree, "taxname", read_names())

def __auto_init():
  if not NTDUMPSDIR.exists():
    fastsubtrees.PROGRESS_ENABLED = True
    fastsubtrees.enable_logger("INFO")
    fastsubtrees.logger.info("Initializing ntsubtree data (this may take a while)")
    fastsubtrees.logger.info("Data directory: {}".format(APPDATADIR))
    fastsubtrees.logger.info("Downloading NCBI taxonomy data...")
    NTDUMPSDIR.mkdir(parents=True, exist_ok=True)
    Downloader(str(NTDUMPSDIR)).run()
    tree = fastsubtrees.Tree.construct_from_csv(\
        str(NTDUMPSDIR / NCBI_NODES_DUMP_FILENAME),
        NCBI_DUMP_SEP, NCBI_NODES_DUMP_TAXID_COL, NCBI_NODES_DUMP_PARENT_COL)
    tree.to_file(TREEFILE)
    ### tree = fastsubtrees.Tree.from_file(TREEFILE)
    names = read_names()
    outfname = tree.attrfilename("taxname")
    with open(outfname, "w") as outfile:
      attribute.write_attribute_values(tree, names, outfile)
