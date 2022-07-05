import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

def element_parent_ids(socket, user, password, database,
                       driver="mysql+mysqldb", hostname="localhost",
                       port=3306, table = "nt_nodes",
                       element_id_column = "tax_id",
                       parent_id_column = "parent_tax_id",
                       echo = False):
  """
  Reads from a database table and yield (element_id, parent_id) pairs.

  Args:
    socket: database connection socket file
    user: database user
    password: password of database user
    database: name of the database to connect to
    driver: database driver (default: mysql+mysqldb)
    hostname: hostname of the database server (default: localhost)
    port: port of the database server (default: 3306)
    table: name of table to read from (default: nt_nodes)
    element_id_column: table column containing element ids (default: tax_id)
    parent_id_column: column containing parent ids (default: parent_tax_id)
    echo: if True, print SQL queries to stdout (default: False)
  """
  url = URL.create(drivername=driver, username=user, password=password,
                   database=database, host=hostname, port=port,
                   query={"unix_socket":socket})
  engine = create_engine(url, echo=echo)
  session = sessionmaker(bind=engine)()
  sql = text(f"SELECT {element_id_column}, {parent_id_column} FROM {table}")
  connection = self.engine.connect()
  for result in connection.execute(sql).fetchall():
    yield result[0], result[1]
