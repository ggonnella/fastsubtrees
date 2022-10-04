#!/usr/bin/env python3
import os
from loguru import logger
from tqdm import tqdm
from ntmirror import Downloader
import fastsubtrees
import json
import gzip

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
ATTR_INPUTFILE="accession_taxid_attribute.tsv.gz"
ATTRIBUTES = ['genome_size', 'GC_content']
TAXID_COLUMN = 1
GENOME_SIZE_COLUMN = 2
GC_CONTENT_COLUMN = 3

def elements_parents_ids(ntdumps):
  filename = os.path.join(ntdumps, NODESFILE)
  with open(filename) as f:
    for line in f:
      elems = line.split(SEPARATOR)
      yield int(elems[ELEM_COLUMN]), int(elems[PARENT_COLUMN])

def scientific_names(ntdumps):
  names = []
  filename = os.path.join(ntdumps, NAMESFILE)
  with open(filename) as f:
    for line in tqdm(f, f"Reading scientific names from {NAMESFILE}"):
      elems = line.split(SEPARATOR)
      if elems[NAMETYPE_COLUMN] == "scientific name\t|\n":
        option = {'label': elems[NAME_COLUMN] + \
                  ' (taxid: ' + str(elems[NAMES_ID_COLUMN]) + ')', \
                  'value': elems[NAME_COLUMN] + \
                  ' (' + str(elems[NAMES_ID_COLUMN])}
        names.append(option)
        option = {}
  return names

def read_attr_input_file():
  result = dict()
  with gzip.open(f'{scriptdir}/{ATTR_INPUTFILE}', 'rt') as file:
    for line in file:
      elems = line.rstrip().split('\t')
      taxid = int(elems[TAXID_COLUMN])
      if taxid not in result:
        result[taxid] = (list(), list())
      result[taxid][GENOME_SIZE_COLUMN-2].append(int(elems[GENOME_SIZE_COLUMN]))
      result[taxid][GC_CONTENT_COLUMN-2].append(float(elems[GC_CONTENT_COLUMN]))
  return result

def generate_attribute_file():
  attrvalues = read_attr_input_file()
  for attribute in ATTRIBUTES:
    with open(f'{scriptdir}/{attribute}.attr', 'w') as outfile:
      tree = fastsubtrees.Tree.from_file(f'{scriptdir}/{TREEFILE}')
      aidx = ATTRIBUTES.index(attribute)-2
      for element_id in tree.subtree_ids(1):
        v = attrvalues.get(element_id, (None, None))[aidx]
        outfile.write(json.dumps(v) + "\n")
    logger.success(f"Attribute file generated: {attribute}.attr")

fastsubtrees.PROGRESS_ENABLED = True
fastsubtrees.enable_logger("INFO")

scriptdir = os.path.dirname(os.path.realpath(__file__))

logger.info(f"Looking for a NCBI taxonomy database dump...")
ntdumps = os.path.join(scriptdir, OUTDIR)
if not os.path.exists(ntdumps):
  d = Downloader(ntdumps)
  has_dwn = d.run()
  assert(has_dwn)
  logger.success(f"Download complete: {ntdumps}")
  tree = fastsubtrees.Tree.construct(elements_parents_ids(ntdumps))
  tree.to_file(os.path.join(scriptdir, TREEFILE))
else:
  logger.success(f"Local copy is up-to-date: {ntdumps}")

logger.info(f"Generating scientific names list...")
snames = scientific_names(ntdumps)
with open(os.path.join(scriptdir,'dictionary.txt'), 'w+') as file:
  file.write(json.dumps(snames))

logger.info(f"Generating attribute files...")
generate_attribute_file()
logger.success(f"Application setup is done, run using ./start.py")
