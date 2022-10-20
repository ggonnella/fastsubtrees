from loguru import logger
import os
import fastsubtrees
import genomes_attributes_viewer as gav

TAXID_COLUMN = 1
ATTR_COLUMN = {}
ATTR_COLUMN["genome_size"] = 2
ATTR_COLUMN["GC_content"] = 3
ATTR_CAST = {}
ATTR_CAST["genome_size"] = int
ATTR_CAST["GC_content"] = float
ATTR_INPUTFILE="accession_taxid_attribute.tsv.gz"

def generate_attribute_files(workdir, force):
  logger.info("Looking for attribute files...")
  tree = fastsubtrees.Tree.from_file(f'{workdir}/{gav.TREEFILE}')
  parentdir = os.path.dirname(__file__)
  attr_inputfile = os.path.join(parentdir, 'data', ATTR_INPUTFILE)
  if force:
    logger.info("Force updating, since upstream data was updated")
  for attribute in gav.ATTRIBUTES:
    if tree.has_attribute(attribute) and not force:
      logger.info(f"Attribute '{attribute}' found")
    else:
      if force and tree.has_attribute(attribute):
        tree.destroy_attribute(attribute)
      tree.create_attribute_from_tabular(attribute, attr_inputfile,
          elem_field_num=TAXID_COLUMN, attr_field_num=ATTR_COLUMN[attribute],
          casting_fn=ATTR_CAST[attribute])
      logger.success(f"Attribute '{attribute}' added to tree")
