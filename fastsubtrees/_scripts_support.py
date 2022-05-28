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
