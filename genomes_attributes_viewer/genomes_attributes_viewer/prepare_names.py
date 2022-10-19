from loguru import logger
import os
import json
from tqdm import tqdm
import genomes_attributes_viewer as gav

NAMESFILE = "names.dmp"
NAMES_ID_COLUMN = 0
NAME_COLUMN = 1
NAMETYPE_COLUMN = 3

def scientific_names(workdir, force):
  logger.info("Looking for scientific names list...")
  outfilename = os.path.join(workdir, gav.SCIENTIFIC_NAMES)
  if force:
    logger.info("Force updating, since upstream data was updated")
  else:
    logger.info(f"Expected location: {outfilename}")
  if not os.path.exists(outfilename) or force:
    logger.info("Generating scientific names list...")
    names = []
    ntdumps = os.path.join(workdir, gav.NTDUMPSDIR)
    infilename = os.path.join(ntdumps, NAMESFILE)
    with open(infilename) as f:
      for line in tqdm(f, f"Reading scientific names from {NAMESFILE}"):
        elems = line.split(gav.NCBI_SEP)
        if elems[NAMETYPE_COLUMN] == "scientific name\t|\n":
          option = {'label': elems[NAME_COLUMN] + \
                    ' (taxid: ' + str(elems[NAMES_ID_COLUMN]) + ')', \
                    'value': elems[NAME_COLUMN] + \
                    ' (' + str(elems[NAMES_ID_COLUMN])}
          names.append(option)
          option = {}
    with open(outfilename, 'w+') as file:
      file.write(json.dumps(names))
    return True
  else:
    logger.info("Scientific names list found")
    return False

