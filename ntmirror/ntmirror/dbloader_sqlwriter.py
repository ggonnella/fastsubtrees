#
# (c) 2020-2022 Giorgio Gonnella, University of Goettingen, Germany
#
"""
SQL statements for loading the data into the database
"""

def _load_data_sql(datafile, tablename, columns):
  """Create SQL script for bulk loading NCBI Taxonomy dump data.

  Non-unique indices are dropped before loading and recomputed afterwards.
  IGNORE is used to handle eventually repeated primary keys.

  Args:
    datafile: NCBI taxonomy dump file
    tablename: table where to insert the data
    columns: table column names in the order of the data in the file

  Returns:
    list of SQL statements
  """
  result = []
  result.append("SET foreign_key_checks = 0;")
  result.append(f"ALTER TABLE {tablename} DISABLE KEYS;")
  sql = f"LOAD DATA LOCAL INFILE '{datafile}' "
  sql += "IGNORE "
  sql += f"INTO TABLE {tablename} "
  sql += r"FIELDS TERMINATED BY '\t|\t' "
  sql += r"LINES TERMINATED BY '\t|\n' "
  sql +="("+",".join(columns)+") "
  result.append(sql)
  result.append(f"ALTER TABLE {tablename} ENABLE KEYS;")
  result.append("SET foreign_key_checks = 1;")
  return result
