#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#
from ntdownload import yield_scientific_names_from_dump

def test_names(testdata_dir):
  names = list(yield_scientific_names_from_dump(testdata_dir))
  assert names == [(1, 'root'), (2, 'Bacteria')]
