from pathlib import Path

NCBI_DUMP_SEP = "\t|\t"
NCBI_NAMES_DUMP_FILENAME = "names.dmp"
NCBI_NAMES_DUMP_TAXID_COL = 0
NCBI_NAMES_DUMP_NAME_COL = 1
NCBI_NAMES_DUMP_CLASS_COL = 3
NCBI_NAMES_DUMP_CLASS_SCIENTIFIC = "scientific name"

def yield_scientific_names_from_dump(dumpsdir):
  names_file = Path(dumpsdir) / NCBI_NAMES_DUMP_FILENAME
  with open(names_file, 'r') as f:
    for line in f:
      fields = line.split(NCBI_DUMP_SEP)
      if fields[NCBI_NAMES_DUMP_CLASS_COL].\
          startswith(NCBI_NAMES_DUMP_CLASS_SCIENTIFIC):
        yield int(fields[NCBI_NAMES_DUMP_TAXID_COL]), \
              fields[NCBI_NAMES_DUMP_NAME_COL]
