#
# (c) 2020-2022 Giorgio Gonnella, University of Goettingen, Germany
#
"""
Loads the data into the database
"""

import MySQLdb

def connect_and_execute(host, user, passwd, db, unix_socket, statements):
  db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db,
                       unix_socket=unix_socket, use_unicode=True)
  cursor = db.cursor()
  for statement in statements:
    cursor.execute(statement)
  cursor.close()
  db.commit()

def load_data_sql(datafile, tablename, columns):
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

def load_data(host, user, passwd, db, unix_socket, datafile, dbmodel):
  tablename = dbmodel.__tablename__
  columns = dbmodel.file_column_names()
  connect_and_execute(host, user, passwd, db, unix_socket,
                      load_data_sql(datafile, tablename, columns))

from pathlib import Path

FILE2CLASS = {
  'names': NtName,
  'gencode': NtGencode,
  'merged': NtMerged,
  'division': NtDivision,
  'delnodes': NtDelnode,
  'citations': NtCitation,
  'nodes': NtNode,
}

def load_all(host, user, passwd, db, unix_socket, dumpdir):
  for filepfx, klass in FILE2CLASS.items():
    filepath = Path(dumpdir) / f"{filepfx}.dmp"
    if filepath.exists():
      load_data(host, user, passwd, db, unix_socket, filepath,
                FILE2CLASS[filepfx])
