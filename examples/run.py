#!/usr/bin/env python3
import os
from loguru import logger
from ntmirror import Downloader
import fastsubtrees

# constants
OUTDIR = "ntdumps"
NODESFILE = "nodes.dmp"
ELEM_COLUMN = 0
PARENT_COLUMN = 1
NAMESFILE = "names.dmp"
NAMES_ID_COLUMN = 0
NAME_COLUMN = 1
NAMETYPE_COLUMN = 3
SEPARATOR = "\t|\t"
TREEFILE = "nt.tree"

fastsubtrees.PROGRESS_ENABLED = True
fastsubtrees.enable_logger("INFO")

scriptdir = os.path.dirname(os.path.realpath(__file__))
ntdumps = os.path.join(scriptdir, OUTDIR)
logger.info(f"Checking for NCBI taxonomy dumps...")
d = Downloader(ntdumps)
has_dwn = d.run()
if has_dwn:
  logger.success(f"Download complete: {ntdumps}")
else:
  logger.success(f"Local copy is up-to-date: {ntdumps}")

def elements_parents_ids(ntdumps):
  filename = os.path.join(ntdumps, NODESFILE)
  with open(filename) as f:
    for line in f:
      elems = line.split(SEPARATOR)
      yield int(elems[ELEM_COLUMN]), int(elems[PARENT_COLUMN])

if has_dwn:
  tree = fastsubtrees.Tree.construct(elements_parents_ids(ntdumps))
  fullpath_treefile = os.path.join(scriptdir, TREEFILE)
  tree.to_file(fullpath_treefile)

def scientific_names(ntdumps):
  names = {}
  filename = os.path.join(ntdumps, NAMESFILE)
  with open(filename) as f:
    for line in f:
      elems = line.split(SEPARATOR)
      if elems[NAMETYPE_COLUMN] == "scientific name":
        names[int(elems[NAMES_ID_COLUMN])] = elems[NAME_COLUMN]
  return names


