import json
from collections import defaultdict
import gzip

import fastsubtrees

TAXID_COLUMN = 1
GENOME_SIZE_COLUMN = 2
GC_CONTENT_COLUMN = 3
attributes = ['genome_size', 'GC_content']

def generate_attribute_file():
  with gzip.open('./accession_taxid_attribute.tsv.gz', 'r') as file:
    taxid_genome_dictionary = defaultdict(list)
    taxid_gccontent_dictionary = defaultdict(list)
    for line in file:
      elems = line.split('\t')
      taxid_genome_dictionary[int(elems[TAXID_COLUMN])].append(int(elems[GENOME_SIZE_COLUMN]))
      taxid_gccontent_dictionary[int(elems[TAXID_COLUMN])].append(float(elems[GC_CONTENT_COLUMN]))
  for attribute in attributes:
    with open(f'{attribute}.attr', 'w') as outfile:
      tree = fastsubtrees.Tree.from_file('./nt.tree')
      for element_id in tree.subtree_ids(1):
        attribute = taxid_genome_dictionary.get(element_id, None)
        outfile.write(json.dumps(attribute) + "\n")

generate_attribute_file()
