#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#

from ntmirror import dbschema
from ntmirror import dbloader
from sqlalchemy.orm import Session

def test_database_creation_and_dropping(connection):
  dbschema.create(connection)
  dbschema.drop(connection)

def test_database_data_loading(connection, testdatadir, mysql_connection_data):
  dbschema.drop(connection)
  dbschema.create(connection)
  dbloader.load_all(str(testdatadir), *mysql_connection_data)
  session = Session(connection)
  for klass in dbschema.DB_MODEL_CLASSES:
    assert session.query(klass).count() == 10
  session.close()
