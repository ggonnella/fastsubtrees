from fastsubtrees import logger, tqdm

NCBI_DUMP_SEP = "\t|\t"
NCBI_DUMP_TAXID_COL = 0
NCBI_DUMP_PARENT_COL = 1

def element_parent_ids(inputfile, separator = '\t',
                       element_id_column = 0, parent_id_column = 1,
                       comment_pfx = "#", ncbi_preset = False):
  """
  Reads a tabular file and yield (element_id, parent_id) pairs.

  Args:
    inputfile: tabular file to read
    separator: separator (default: tab)
    element_id_column: column index of the element ID (default: 0)
    parent_id_column: column index of the parent ID (default: 1)
    comment_pfx: prefix of lines to be skipped (default: '#')
    ncbi_preset: use NCBI dump preset (default: False)
  """
  logger.info(f"Reading data from file \"{inputfile}\" ...")
  if ncbi_preset:
    separator = NCBI_DUMP_SEP
    element_id_column = NCBI_DUMP_TAXID_COL
    parent_id_column = NCBI_DUMP_PARENT_COL
  with open(inputfile) as file:
    for line in tqdm(file):
      if comment_pfx and line.startswith(comment_pfx):
        continue
      fields = line.rstrip().split(separator)
      element = int(fields[element_id_column])
      parent = int(fields[parent_id_column])
      yield element, parent
