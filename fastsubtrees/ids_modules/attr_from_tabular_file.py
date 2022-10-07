"""
Yield attribute values from a tabular file, optionally gzipped.
"""

import gzip

def attribute_values(filename, id_col=0, attr_col=1, separator = "\t",
                     comment_pfx = "#"):
  id_col = int(id_col)
  attr_col = int(attr_col)
  with open(filename, 'rb') as f:
    is_gzipped = f.read(2) == b'\x1f\x8b'
  f = gzip.open(filename, 'rt') if is_gzipped else open(filename, 'r')
  for line in f:
    line = line.rstrip()
    if line.startswith(comment_pfx):
      continue
    fields = line.split(separator)
    id = fields[id_col]
    attr = fields[attr_col]
    yield id, attr
  f.close()
