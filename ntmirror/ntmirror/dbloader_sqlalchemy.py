#
# (c) 2020-2022 Giorgio Gonnella, University of Goettingen, Germany
#
"""
Loads the data into the database using SqlAlchemy
"""

from pathlib import Path
from .dbloader_sqlwriter import load_data_sql
from .dbschema import FILE2CLASS
from sqlalchemy import text

def load_data(datafile, dbmodel, connection):
  tablename = dbmodel.__tablename__
  columns = dbmodel.file_column_names()
  for line in load_data_sql(datafile, tablename, columns):
    connection.execute(text(line))

def load_all(dumpdir, connection):
  for filepfx, klass in FILE2CLASS.items():
    filepath = Path(dumpdir) / f"{filepfx}.dmp"
    if filepath.exists():
      load_data(filepath, klass, connection)
