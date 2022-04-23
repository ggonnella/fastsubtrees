#
# (c) 2022, Giorgio Gonnella, University of Goettingen, Germany
#

from schema import Or, Optional, Schema
from loguru import logger
import sys

ARGS_DOC = """\
  --verbose, -v    be verbose
  --version, -V    show script version
  --help, -h       show this help message"""

ARGS_SCHEMA = {Optional("--verbose", default=None): Or(None, True, False),
                                                    Optional(str): object}

def validate(args, *dicts):
  s = ARGS_SCHEMA.copy()
  for d in dicts:
    s.update(d)
  return Schema(s).validate(args)

def setup_logger(verbose):
  logger.remove()
  logger.add(sys.stderr, colorize=sys.stdout.isatty(),
             format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "+\
                    "<level>{level}</level> | {message}",
             level="INFO" if verbose else "WARNING")
  return logger
