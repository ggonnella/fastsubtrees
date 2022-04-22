#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#

from ntmirror import dbschema

def test_database_creation_and_dropping(connection):
  dbschema.create(connection)
  dbschema.drop(connection)

