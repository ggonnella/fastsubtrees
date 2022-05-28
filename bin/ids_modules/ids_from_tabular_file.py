def element_parent_ids(inputfile, separator = '\t',
                       element_id_column = 0, parent_id_column = 1,
                       comment_pfx = "#"):
  """
  Reads a tabular file and yield (element_id, parent_id) pairs.

  Args:
    inputfile: tabular file to read
    separator: separator (default: tab)
    element_id_column: column index of the element ID (default: 0)
    parent_id_column: column index of the parent ID (default: 1)
    comment_pfx: prefix of lines to be skipped (default: '#')
  """
  with open(inputfile) as file:
    for line in file:
      if comment_pfx and line.startswith(comment_pfx):
        continue
      fields = line.rstrip().split(separator)
      element = int(fields[element_id_column])
      parent = int(fields[parent_id_column])
      yield element, parent
