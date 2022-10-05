"""
Yield attribute values read from the accession_taxid_attribute table
"""

import gzip

def attribute_values(filename, taxid_col, attr_col):
  taxid_col = int(taxid_col)
  attr_col = int(attr_col)
  with gzip.open(filename, 'rt') as f:
    for line in f:
      line = line.rstrip()
      if line.startswith('#'):
        continue
      fields = line.split('\t')
      taxid = fields[taxid_col]
      attr = fields[attr_col]
      yield taxid, attr
