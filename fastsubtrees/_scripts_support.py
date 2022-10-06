import os
import sys
import fastsubtrees

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
  logger.debug("Loading Python module '{}'".format(fname))
  modulename = Path(fname).stem
  spec = importlib.util.spec_from_file_location(modulename, fname)
  m = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(m)
  if not m.__dict__.get(function):
    raise ValueError("The specified Python module {} does not define a "
                     "function {}()".format(fname, function))
  logger.success("Module loaded, function {}() found".format(function))
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
    logger.debug(f"Positional arguments passed to the function: {posargs}")
  if keyargs:
    logger.debug(f"Keyword arguments passed to the function: {keyargs}")
  return posargs, keyargs

def get_datatype_casting_fn(value, m, mfilename):
  if not value:
    logger.debug("Using str for datatype casting (default)")
    cast = str
  else:
    try:
      cast = eval(value)
      logger.debug(f"Using function '{value}()' for datatype casting")
    except NameError:
      if m.__dict__.get(value):
        cast = m.__dict__[value]
        logger.debug("Using function {}() from module {} for datatype casting".\
            format(value, mfilename))
      else:
        raise ValueError("Invalid datatype casting function '{}'".\
            format(value))
    return cast

def find_attribute_files(treefile):
  # find all files whose path starts with treefile and end with .attrs
  treefile = Path(treefile)
  treefile_dir = treefile.parent
  treefile_prefix = treefile.stem
  files = [f for f in treefile_dir.iterdir() if f.stem.startswith(treefile_prefix)]
  # filter out files that are not attribute files
  files = [f for f in files if f.suffix in [".csv", ".tsv", ".txt"]]
  return files

