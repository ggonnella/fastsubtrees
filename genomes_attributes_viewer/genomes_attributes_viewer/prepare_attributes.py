from loguru import logger
import os
import json
import gzip
import fastsubtrees
from collections import defaultdict
import importlib.resources
import genomes_attributes_viewer as gav

TAXID_COLUMN = 1
GENOME_SIZE_COLUMN = 2
GC_CONTENT_COLUMN = 3
ATTR_INPUTFILE="accession_taxid_attribute.tsv.gz"

def read_attr_input_file(workdir):
  result = {"genome_size": defaultdict(list), "GC_content": defaultdict(list)}
  parentdir = os.path.dirname(__file__)
  attr_inputfile = os.path.join(parentdir, 'data', ATTR_INPUTFILE)
  with gzip.open(attr_inputfile, 'rt') as file:
    for line in file:
      elems = line.rstrip().split('\t')
      taxid = int(elems[TAXID_COLUMN])
      result["genome_size"][taxid].append(int(elems[GENOME_SIZE_COLUMN]))
      result["GC_content"][taxid].append(float(elems[GC_CONTENT_COLUMN]))
  return result

def generate_attribute_files(workdir, force):
  logger.info(f"Looking for attribute files...")
  file_not_found = False
  if force:
    logger.info(f"Force updating, since upstream data was updated")
  else:
    for attribute in gav.ATTRIBUTES:
      outfilename = fastsubtrees.Tree.compute_attrfilename(f'{workdir}/{gav.TREEFILE}',
                                                        attribute)

      logger.info(f"Expected location: {outfilename}")
      if not os.path.exists(outfilename):
        file_not_found = True
        break
  if file_not_found or force:
    logger.info(f"Generating attribute files...")
    attrvalues = read_attr_input_file(workdir)
    tree = fastsubtrees.Tree.from_file(f'{workdir}/{gav.TREEFILE}')
    for attribute in gav.ATTRIBUTES:
      tree.save_attribute_values(tree, attribute, attrvalues[attribute])
      logger.success(f"Attribute file for '{attribute}' generated")
    return True
  else:
    logger.success(f"Attribute files found")
    return False

