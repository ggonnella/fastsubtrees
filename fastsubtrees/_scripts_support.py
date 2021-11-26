import os
import sys
import fastsubtrees

msgformat_prefix="<green><dim>{time:YYYY-MM-DD HH:mm:ss}</></>"
msgformat_content="<level><normal>{level.name}: {message}</></>"

def setup_verbosity(args):
  fastsubtrees.logger.remove()
  if args["--quiet"]:
    fastsubtrees.PROGRESS_ENABLED = False
  else:
    fastsubtrees.PROGRESS_ENABLED = True
    fastsubtrees.logger.enable("fastsubtrees")
    if args["--debug"]:
      level = "DEBUG"
    else:
      level = "INFO"
    fastsubtrees.logger.add(sys.stderr,
        format=f"{msgformat_prefix} {msgformat_content}",
               level=level)
