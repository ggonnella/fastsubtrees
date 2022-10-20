import fastsubtrees
from ntdownload import Downloader
from pathlib import Path
from shutil import rmtree

from .constants import \
   NCBI_NAMES_DUMP_TAXID_COL, NCBI_NAMES_DUMP_NAME_COL, \
   NCBI_NAMES_DUMP_CLASS_COL, NCBI_NAMES_DUMP_CLASS_SCIENTIFIC, \
   NCBI_NAMES_DUMP_FILENAME, NCBI_NODES_DUMP_FILENAME, \
   NTDUMPSDIR, TREEFILE, NCBI_DUMP_SEP, APPDATADIR

def yield_names():
  names_dump = NTDUMPSDIR / NCBI_NAMES_DUMP_FILENAME
  fastsubtrees.logger.info("Source of scientific names: {}".format(names_dump))
  with open(names_dump, 'r') as f:
    for line in f:
      fields = line.split(NCBI_DUMP_SEP)
      if fields[NCBI_NAMES_DUMP_CLASS_COL].\
          startswith(NCBI_NAMES_DUMP_CLASS_SCIENTIFIC):
        yield int(fields[NCBI_NAMES_DUMP_TAXID_COL]), \
                                  fields[NCBI_NAMES_DUMP_NAME_COL]

def read_names():
  result = {}
  for taxid, name in yield_names():
    result[taxid] = name
  return result

def n_lines(filename):
  n = 0
  with open(filename, 'r') as f:
    for _ in f:
      n += 1
  return n

names_index = None

def search_name(query, reindex=False):
  global names_index
  if not names_index or reindex:
    fastsubtrees.logger.info("Building scientific names index")
    names_index = {}
    for taxid, name in yield_names():
      names_index[name] = taxid
  return names_index.get(query, None)

def update(force_download=False, force_construct=False):
  """
  Download updated NCBI taxonomy data using _ntdownload_, if any.
  If the new data was found, update the taxonomy tree using _fastsubtrees_.
  """
  fastsubtrees.PROGRESS_ENABLED = True
  fastsubtrees.enable_logger("INFO")
  fastsubtrees.logger.info("Updating ntsubtree data...")
  fastsubtrees.logger.info("Data directory: {}".format(APPDATADIR))
  fastsubtrees.logger.info("Looking for updated NCBI taxonomy data...")
  NTDUMPSDIR.mkdir(parents=True, exist_ok=True)
  if force_download:
    for f in NTDUMPSDIR.glob("*"):
      f.unlink()
  updated = Downloader(str(NTDUMPSDIR)).run()
  if updated or force_construct:
    fastsubtrees.logger.info("Updating taxonomy tree...")
    tree = fastsubtrees.Tree.from_file(TREEFILE)
    filename = str(NTDUMPSDIR / NCBI_NODES_DUMP_FILENAME)
    n_node_lines = n_lines(filename)
    fastsubtrees.logger.info("Number of nodes: {}".format(n_node_lines))
    tree.reset_from_ncbi_dump(filename, total=n_node_lines)
    fastsubtrees.logger.info("Updating taxonomy names...")
    tree.to_file(TREEFILE)
    if tree.has_attribute("taxname"):
      tree.replace_attribute_values("taxname", read_names())
    else:
      tree.create_attribute("taxname", yield_names())
    global names_index
    names_index = None
  else:
    fastsubtrees.logger.info("No tree update needed.")

def cleanup():
  if APPDATADIR.exists():
    for path in Path(APPDATADIR).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)

def setup():
  """
  Download the NCBI taxonomy data using _ntdownload_ and construct
  the taxonomy tree using _fastsubtrees_.
  """
  fastsubtrees.PROGRESS_ENABLED = True
  fastsubtrees.enable_logger("INFO")
  fastsubtrees.logger.info("Initializing ntsubtree data...")
  fastsubtrees.logger.info("Data directory: {}".format(APPDATADIR))
  fastsubtrees.logger.info("Downloading NCBI taxonomy data...")
  cleanup()
  NTDUMPSDIR.mkdir(parents=True)
  Downloader(str(NTDUMPSDIR)).run()
  inputfn = str(NTDUMPSDIR / NCBI_NODES_DUMP_FILENAME)
  tree = fastsubtrees.Tree.construct_from_ncbi_dump(inputfn)
  tree.to_file(TREEFILE)
  fastsubtrees.logger.info("Loading taxonomy names...")
  tree.create_attribute("taxname", yield_names())

def __auto_setup():
  """
  Automatically download NCBI taxonomy data and construct the taxonomy tree
  if not found at the expected location.
  """
  if not NTDUMPSDIR.exists():
    setup()

def get_tree():
  """
  Return the taxonomy tree.
  """
  __auto_setup()
  return fastsubtrees.Tree.from_file(TREEFILE)
