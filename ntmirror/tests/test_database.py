#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#

from ntmirror import dbschema
from ntmirror import dbloader_mysql
from ntmirror import dbloader_sqlalchemy
from sqlalchemy.orm import Session

def test_db_creation_and_dropping(connection):
  dbschema.create(connection)
  dbschema.drop(connection)

def test_db_data_loading_mysql(connection, testdatadir, mysql_connection_data):
  dbschema.drop(connection)
  dbschema.create(connection)
  dbloader_mysql.load_all(str(testdatadir), *mysql_connection_data)
  session = Session(connection)
  for klass in dbschema.DB_MODEL_CLASSES:
    assert session.query(klass).count() == 10
  session.close()

def test_db_data_loading_sqlalchemy(connection, testdatadir):
  dbschema.drop(connection)
  dbschema.create(connection)
  dbloader_sqlalchemy.load_all(str(testdatadir), connection)
  session = Session(connection)
  for klass in dbschema.DB_MODEL_CLASSES:
    assert session.query(klass).count() == 10
  session.close()
