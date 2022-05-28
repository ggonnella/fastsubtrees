# setup loguru by disabling it, as expected for libraries
from loguru import logger
logger.disable(__name__)
import sys

def enable_logger(level):
  logger.remove()
  logger.enable("fastsubtrees")
  msgformat_prefix="<green><dim>{time:YYYY-MM-DD HH:mm:ss}</></>"
  msgformat_content="<level><normal>{level.name}: {message}</></>"
  logger.add(sys.stderr, format=f"{msgformat_prefix} {msgformat_content}",
             level=level)

# create a flag to enable/disable progress bar; disable it by default;
# the method tqdm will respect this flag and behave like tqdm.tqdm;
import tqdm as tqdm_module   # type: ignore
PROGRESS_ENABLED=False       # default value
tqdm = lambda *args, **kargs: \
    tqdm_module.tqdm(*args, **{**{"disable": not PROGRESS_ENABLED}, **kargs})

from fastsubtrees.error import *
from fastsubtrees.tree import Tree
from fastsubtrees.attribute import *
