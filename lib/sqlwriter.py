import importlib
import os
from typing import Union, List, Dict, Any

def _fixed_data_from_file(fixed_data_fn):
  result = {}
  with open(fixed_data_fn) as f:
    for line in f:
      elems = line.rstrip().split("\t")
      result[elems[0]] = elems[1]
  return result

def _column_names_from_dbschema(filename, tablename):
  assert(os.path.exists(filename))
  spec = importlib.util.spec_from_file_location("dbschema", filename)
  assert(spec)
  dbschema = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(dbschema)
  klass = dbschema.tablename2class[tablename]
  return klass.file_column_names()

def n_header_lines(filename: str, pfx: str = "#") -> int:
  """Number of header lines, identified by a given prefix

  Args:
    filename: data of the table file
    pfx:      header lines prefix, defaults to "#"

  Returns:
    0 if pfx is empty, otherwise number of initial lines starting with pfx
  """
  result = 0
  if not pfx:
    return 0
  with open(filename) as f:
    for line in f:
      if line.startswith(pfx):
        result += 1
      else:
        return result

def load_data_sql(datafile: str, tablename: str, columns: Union[List[str], str],
                  skipfields: List[int] = [],
                  fixed_data: Union[None, str, Dict[str, Any]] = None,
                  ignore: Union[bool, None] = False,
                  dropkeys: Union[bool, None] = False,
                  ncbidmp: Union[bool, None] = False,
                  headerpfx: str = "#") -> List[str]:
  """Create SQL script for bulk data loading.

  Args:
    datafile: filename, tsv or ncbidmp format (if ncbidmp=True)
    tablename: table where to insert
    columns: either a list of strings (column names) or a python module filename
             which provides: tablename2class[<tablename>].file_column_names()
             returning a list of strings (column names)
    skipfields = fields of the file to be ignored (1-based field numbers)
    fixed_data (optional): data which must be added to each column
             either a string (filename of tsv with lines:
             column_name <TAB> value) or a dict column_name => value
    ignore (optional): use IGNORE on repeated primary key instead of REPLACE
    dropkeys (optional): drop non-unique indices before inserting,
             recompute them after inserting
    ncbidmp (optional): datafile is in NCBI dmp format
    headerpfx (optional): skip any initial line in the file starting
                          with this prefix; use empty string to disable

  Returns:
    list of SQL statements
  """
  result = []
  result.append("SET foreign_key_checks = 0;")
  if dropkeys:
    result.append(f"ALTER TABLE {tablename} DISABLE KEYS;")
  sql = f"LOAD DATA LOCAL INFILE '{datafile}' "
  sql += "IGNORE " if ignore else "REPLACE "
  sql += f"INTO TABLE {tablename} "
  if ncbidmp:
    sql += r"FIELDS TERMINATED BY '\t|\t' "
    sql += r"LINES TERMINATED BY '\t|\n' "
  if isinstance(columns, str):
    columns = _column_names_from_dbschema(columns, tablename)
  if skipfields:
    for n in sorted(skipfields):
      columns.insert(n-1, "@dummy")
  sql +="("+",".join(columns)+") "
  if fixed_data:
    if isinstance(fixed_data, str):
      fixed_data = _fixed_data_from_file(fixed_data)
    setelems = [f"{k} = %({k})s" for k in fixed_data.keys()]
    sql += "SET "+", ".join(setelems) + " "
  if headerpfx:
    n_skip = n_header_lines(datafile, headerpfx)
    if n_skip:
      sql += f"IGNORE {n_skip} LINES "
  sql += ";"
  result.append(sql)
  if dropkeys:
    result.append(f"ALTER TABLE {tablename} ENABLE KEYS;")
  result.append("SET foreign_key_checks = 1;")
  return result
