#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#
import pytest
from ntmirror import dbschema
from sqlalchemy.orm import Session

NODBMSG="Database configuration invalid or configuration file not provided"

@pytest.mark.script_launch_mode('subprocess')
def test_dbload_cli_mysql(connection, script, testdatadir,
                          connection_args, script_runner):
  if connection is None:
    pytest.skip(NODBMSG)
  else:
    dbschema.drop(connection)
    args = connection_args + [testdatadir, "--exitcode", "--dbecho", "--verbose",
                                           "--testmode"]
    ret = script_runner.run(script("ntmirror-dbload"), *args)
    assert ret.returncode == 0
    session = Session(connection)
    for klass in dbschema.DB_MODEL_CLASSES:
      assert session.query(klass).count() == 10
    session.close()

@pytest.mark.script_launch_mode('subprocess')
def test_dbload_cli_sqlalchemy(connection, script, testdatadir,
                               connection_args, script_runner):
  if connection is None:
    pytest.skip(NODBMSG)
  else:
    dbschema.drop(connection)
    args = connection_args + [testdatadir, "--exitcode", "--sqlalchemy",
                                           "--dbecho", "--verbose", "--testmode"]
    ret = script_runner.run(script("ntmirror-dbload"), *args)
    session = Session(connection)
    for klass in dbschema.DB_MODEL_CLASSES:
      assert session.query(klass).count() == 10
    session.close()
