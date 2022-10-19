from loguru import logger
import os
from ntdownload import Downloader
import fastsubtrees
import genomes_attributes_viewer as gav
import genomes_attributes_viewer.prepare_names as prepare_names
import genomes_attributes_viewer.prepare_attributes as prepare_attributes
import fastsubtrees.ids_modules.ids_from_tabular_file as ids_from_tabular_file

fastsubtrees.PROGRESS_ENABLED = True
fastsubtrees.enable_logger("INFO")

NODESFILE = "nodes.dmp"
ELEM_COLUMN = 0
PARENT_COLUMN = 1

def prepare_ncbi_dumps(workdir, force):
  logger.info("Looking for NCBI taxonomy data...")
  ntdumps = os.path.join(workdir, gav.NTDUMPSDIR)
  if force:
    logger.info("Force updating")
  else:
    logger.info(f"Expected location: {ntdumps}")
  if not os.path.exists(ntdumps) or force:
    d = Downloader(ntdumps)
    has_dwn = d.run()
    assert has_dwn
    return True
  else:
    logger.success("NCBI taxonomy data found")
    return False

def prepare_tree(workdir, force):
  logger.info("Looking for fastsubtrees tree file...")
  treefile = os.path.join(workdir, gav.TREEFILE)
  ntdumps = os.path.join(workdir, gav.NTDUMPSDIR)
  if force:
    logger.info("Force updating, since upstream data was updated")
  else:
    logger.info(f"Expected location: {treefile}")
  if not os.path.exists(treefile) or force:
    tree = fastsubtrees.Tree.construct(ids_from_tabular_file.element_parent_ids(
        os.path.join(ntdumps, NODESFILE),
        separator=gav.NCBI_SEP, element_id_column=ELEM_COLUMN,
        parent_id_column=PARENT_COLUMN))
    tree.to_file(treefile)
    return True
  else:
    logger.success("Tree file found")
    return False

def prepare_first_run(workdir, force=False):
  force = prepare_ncbi_dumps(workdir, force)
  prepare_names.scientific_names(workdir, force)
  force = prepare_tree(workdir, force)
  prepare_attributes.generate_attribute_files(workdir, force)
