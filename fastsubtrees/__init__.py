# setup loguru by disabling it, as expected for libraries
from loguru import logger
logger.disable(__name__)

# create a flag to enable/disable progress bar; disable it by default;
# the method tqdm will respect this flag and behave like tqdm.tqdm;
import tqdm as tqdm_module   # type: ignore
PROGRESS_ENABLED=False       # default value
tqdm = lambda *args, **kargs: \
    tqdm_module.tqdm(*args, **{**{"disable": not PROGRESS_ENABLED}, **kargs})

from fastsubtrees.error import *
from fastsubtrees.tree import Tree

