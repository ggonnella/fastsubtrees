from contextlib import contextmanager
import MySQLdb

def connect(args, **kwargs):
  return MySQLdb.connect(host="localhost",
                         user=args["<dbuser>"],
                         passwd=args["<dbpass>"],
                         db=args["<dbname>"],
                         unix_socket=args["<dbsocket>"],
                         use_unicode=True,
                         **kwargs)

@contextmanager
def cursor_from(args):
  db = connect(args)
  cursor = db.cursor()
  try:
    yield cursor
  finally:
    cursor.close()
  db.commit()

def connect_and_execute(args, statements):
  with cursor_from(args) as c:
    for statement in statements:
      c.execute(statement)
