# NtSubtree package

from pathlib import Path
from platformdirs import PlatformDirs

__version__="1.0"
__appname__="NtSubtree"
__author__="ggonnella"

NCBI_DUMP_SEP = "\t|\t"

NCBI_NODES_DUMP_FILENAME = "nodes.dmp"
NCBI_NODES_DUMP_TAXID_COL = 0
NCBI_NODES_DUMP_PARENT_COL = 1

NCBI_NAMES_DUMP_FILENAME = "names.dmp"
NCBI_NAMES_DUMP_TAXID_COL = 0
NCBI_NAMES_DUMP_NAME_COL = 1
NCBI_NAMES_DUMP_CLASS_COL = 3
NCBI_NAMES_DUMP_CLASS_SCIENTIFIC = "scientific name"

APPDATADIR = Path(PlatformDirs(__appname__, __author__, \
                              version=__version__).user_data_dir)
NTDUMPSDIR = APPDATADIR / "ntdumps"
TREEFILE = str(APPDATADIR / "nt.tree")
