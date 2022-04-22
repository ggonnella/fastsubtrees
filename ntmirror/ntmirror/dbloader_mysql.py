#
# (c) 2020-2022 Giorgio Gonnella, University of Goettingen, Germany
#
"""
Loads the data into the database using the mysql module
"""

import MySQLdb
from pathlib import Path
from .dbloader_sqlwriter import load_data_sql
from .dbschema import FILE2CLASS

def connect_and_execute(host, user, passwd, db, unix_socket, statements):
  db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db,
                       unix_socket=unix_socket, use_unicode=True)
  cursor = db.cursor()
  for statement in statements:
    cursor.execute(statement)
  cursor.close()
  db.commit()

def load_data(datafile, dbmodel, host, user, passwd, db, unix_socket):
  tablename = dbmodel.__tablename__
  columns = dbmodel.file_column_names()
  connect_and_execute(host, user, passwd, db, unix_socket,
                      load_data_sql(datafile, tablename, columns))

def load_all(dumpdir, host, user, passwd, db, unix_socket):
  for filepfx, klass in FILE2CLASS.items():
    filepath = Path(dumpdir) / f"{filepfx}.dmp"
    if filepath.exists():
      load_data(filepath, klass, host, user, passwd, db, unix_socket)
