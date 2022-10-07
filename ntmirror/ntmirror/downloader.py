#
# (c) 2020-2022 Giorgio Gonnella, University of Goettingen, Germany
#

"""
Downloads the NCBI taxonomy dump, if it is newer than the timestamp flag file
"""

import sh
import os

class Downloader():
  PROTOCOL1 = "ftp://"
  PROTOCOL2 = "https://"
  REMOTE = "ftp.ncbi.nih.gov/pub/taxonomy"
  DUMPFILENAME = "taxdump.tar.gz"
  TESTFILENAME = "taxdump_readme.txt"
  TIMESTAMP = "timestamp"

  def __init__(self, outdir):
    self.outdir = outdir
    os.makedirs(self.outdir, exist_ok=True)
    self.testmode = False

  def set_testmode(self):
    self.DUMPFILENAME = self.TESTFILENAME
    self.testmode = True

  def run(self, decompress=True):
    remotefile = self.REMOTE + "/" + self.DUMPFILENAME
    localfile = self.outdir + "/" + self.DUMPFILENAME
    timestampfile = self.outdir + "/" + self.TIMESTAMP
    args = ["-o", localfile, "-w", "%{size_download}", "-R"]
    if os.path.exists(timestampfile):
      args += ["-z", timestampfile]
    try:
      ret = sh.curl(self.PROTOCOL1 + remotefile, *args)
    except sh.ErrorReturnCode:
      ret = sh.curl(self.PROTOCOL2 + remotefile, *args)
    downloaded = int(ret.rstrip())
    if downloaded > 0:
      if decompress and not self.testmode:
        sh.tar("-xzf", localfile, "-C", self.outdir)
        os.unlink(localfile)
      sh.touch(timestampfile)
      return True
    else:
      return False
