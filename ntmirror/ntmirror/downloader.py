#!/usr/bin/env python3
"""
Downloads the NCBI taxonomy dump, if it is newer than the timestamp flag file
"""

import sh
import os

class Downloader():
  REMOTE = "ftp://ftp.ncbi.nih.gov/pub/taxonomy"
  DUMPFILENAME = "taxdump.tar.gz"
  TIMESTAMP = "timestamp"

  def __init__(self, outdir):
    self.outdir = outdir

  def run(decompress=True):
    remotefile = self.REMOTE + "/" + self.DUMPFILENAME
    localfile = self.outdir + "/" + self.DUMPFILENAME
    timestamp = outdir + "/" + self.TIMESTAMP
    args = [remotefile, "-o", localfile]
    if os.path.exists(timestamp):
      args.append("-z", timestamp)
    sh.curl(*args)
    sh.touch(timestamp)
    if decompress:
      sh.tar("xvf", localfile, "-C", self.outdir)
