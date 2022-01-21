"""
Common arguments from scripts
"""

from schema import Or, Optional, Schema

args_doc = """\
  --verbose, -v  be verbose
  --version, -V  show script version
  --help, -h     show this help message"""

_schema = {Optional("--verbose"): Or(None, True, False),
           Optional(str): object}

def validate(args, *dicts):
  s = _schema.copy()
  for d in dicts:
    s.update(d)
  return Schema(s).validate(args)
