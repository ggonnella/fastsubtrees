import sys
import fastsubtrees
from pathlib import Path
import importlib.util

def setup_verbosity(args):
  if args["--quiet"]:
    fastsubtrees.PROGRESS_ENABLED = False
    fastsubtrees.logger.remove()
  else:
    fastsubtrees.PROGRESS_ENABLED = True
    if args["--debug"]:
      level = "DEBUG"
    else:
      level = "INFO"
    fastsubtrees.enable_logger(level)

def get_module(fname, function):
  fastsubtrees.logger.debug("Loading Python module '{}'".format(fname))
  modulename = Path(fname).stem
  if not Path(fname).exists():
    fastsubtrees.logger.error(\
        "The specified Python module '{}' does not exist".format(fname))
    sys.exit(1)
  spec = importlib.util.spec_from_file_location(modulename, fname)
  if spec is None:
    fastsubtrees.logger.error(\
        "The specified Python module {} cannot be loaded".format(fname))
    sys.exit(1)
  m = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(m)
  if not m.__dict__.get(function):
    fastsubtrees.logger.error(\
        "The specified Python module {} does not define a function {}()".\
          format(fname, function))
    sys.exit(1)
  fastsubtrees.logger.success("Module loaded, function {}() found".\
      format(function))
  return m

def get_fn_args(has_keyargs, values):
  if has_keyargs:
    keyargs = {k: v for k, v in \
               [a.split("=", 1) for a in values if "=" in a]}
    posargs = [a for a in values if "=" not in a]
  else:
    keyargs = {}
    posargs = values
  if posargs:
    fastsubtrees.logger.debug(\
        f"Positional arguments passed to the function: {posargs}")
  if keyargs:
    fastsubtrees.logger.debug(\
        f"Keyword arguments passed to the function: {keyargs}")
  return posargs, keyargs

def get_datatype_casting_fn(value, m, mfilename):
  if not value:
    fastsubtrees.logger.debug("Using str for datatype casting (default)")
    cast = str
  else:
    try:
      cast = eval(value)
      fastsubtrees.logger.debug(\
          f"Using function '{value}()' for datatype casting")
    except NameError:
      if m and m.__dict__.get(value):
        cast = m.__dict__[value]
        fastsubtrees.logger.debug(\
            "Using function {}() from module {} for datatype casting".\
              format(value, mfilename))
      else:
        fastsubtrees.logger.error("Invalid datatype casting function '{}'".\
            format(value))
        sys.exit(1)
  return cast

