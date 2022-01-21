"""
Helper methods for working with the database
"""

from sqlalchemy.engine.url import URL
import os
from collections import defaultdict
from schema import And

args_doc = """\
  dbuser:       database user to use
  dbpass:       password of the database user
  dbname:       database name
  dbsocket:     connection socket file"""

args_usage="<dbuser> <dbpass> <dbname> <dbsocket>"

args_schema = {"<dbuser>": And(str, len),
               "<dbpass>": And(str, len),
               "<dbname>": And(str, len),
               "<dbsocket>": And(str, len, os.path.exists)}

snake_args = {"config": ["<dbuser>", "<dbpass>", "<dbname>"],
              "input": ["<dbsocket>"]}

DB_DRIVER="mysql+mysqldb"
DB_HOST="localhost"

def _connstr(u,p,d,s):
  if not(s):
    raise RuntimeError("DB unix socket not provided")
  elif not os.path.exists(s):
    raise RuntimeError(f"DB unix socket does not exist: {s}")
  elif not(u):
    raise RuntimeError("Database user name not provided")
  elif not(p):
    raise RuntimeError(f"Database password for user '{u}' not provided")
  elif not(d):
    raise RuntimeError("Database name not provided")
  return URL.create(drivername=DB_DRIVER, username=u, password=p,
                    database=d, host=DB_HOST, query={"unix_socket":s})

ARGSKEYS = ["<dbuser>", "<dbpass>", "<dbname>", "<dbsocket>"]

def connstr_from(args) -> str:
  """
  MySQL/MariaDB connection string based on the values of the args '<dbuser>',
  '<dbpass>', '<dbname>' and '<dbsocket>'
  """
  return _connstr(*[args.get(k) for k in ARGSKEYS])

def connstr_env(varname) -> str:
  """
  Create a connection string from an env variable consisting of
  dbuser dbpass dbname and dbsocket, space-separated
  """
  return _connstr(*os.environ[varname].split(" "))

def args_from_env(varname):
  """
  Creates an args variable for running the main() function
  of a script, using the db connection data from an env variable
  """
  return defaultdict(lambda:None,
      {k:v for k, v in zip(ARGSKEYS, os.environ[varname].split(" "))})
