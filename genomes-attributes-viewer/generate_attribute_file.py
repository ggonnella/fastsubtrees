import json
import gzip
import os

import fastsubtrees

TAXID_COLUMN = 1
GENOME_SIZE_COLUMN = 2
GC_CONTENT_COLUMN = 3
attributes = ['genome_size', 'GC_content']

scriptdir = os.path.dirname(os.path.realpath(__file__))

INPUTFILE="accession_taxid_attribute.tsv.gz"
TREEFILE="nt.tree"

def read_input_file():
  result = dict()
  with gzip.open(f'{scriptdir}/{INPUTFILE}', 'rt') as file:
    for line in file:
      elems = line.rstrip().split('\t')
      taxid = int(elems[TAXID_COLUMN])
      if taxid not in result:
        result[taxid] = (list(), list())
      result[taxid][GENOME_SIZE_COLUMN-2].append(int(elems[GENOME_SIZE_COLUMN]))
      result[taxid][GC_CONTENT_COLUMN-2].append(float(elems[GC_CONTENT_COLUMN]))
  return result

def generate_attribute_file():
  attrvalues = read_input_file()
  for attribute in attributes:
    with open(f'{scriptdir}/{attribute}.attr', 'w') as outfile:
      tree = fastsubtrees.Tree.from_file(f'{scriptdir}/{TREEFILE}')
      aidx = attributes.index(attribute)-2
      for element_id in tree.subtree_ids(1):
        v = attrvalues.get(element_id, (None, None))[aidx]
        outfile.write(json.dumps(v) + "\n")

generate_attribute_file()
