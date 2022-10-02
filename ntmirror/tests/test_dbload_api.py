#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#
import pytest
from ntmirror import dbschema
from ntmirror import dbloader_mysql
from ntmirror import dbloader_sqlalchemy
from sqlalchemy.orm import Session

NODBMSG="Database configuration invalid or configuration file not provided"

def test_dbload_api_mysql(connection, testdatadir, mysql_connection_data):
  if connection is None:
    pytest.skip(NODBMSG)
  else:
    dbschema.drop(connection)
    dbschema.create(connection)
    dbloader_mysql.load_all(str(testdatadir), *mysql_connection_data)
    session = Session(connection)
    for klass in dbschema.DB_MODEL_CLASSES:
      assert session.query(klass).count() == 10
    session.close()

def test_dbload_api_sqlalchemy(connection, testdatadir):
  if connection is None:
    pytest.skip(NODBMSG)
  else:
    dbschema.drop(connection)
    dbschema.create(connection)
    dbloader_sqlalchemy.load_all(str(testdatadir), connection)
    session = Session(connection)
    for klass in dbschema.DB_MODEL_CLASSES:
      assert session.query(klass).count() == 10
    session.close()
