#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#
import pytest
import sh
import time
import os
from ntmirror import Downloader

#
# By default, the test will be done downloading a smaller file
# (taxdump_readme.txt) instead of the dump file (taxdump.tar.gz).
#
# If the following variable is set to True, the test "test_first_download"
# will be done downloading the full dump file (and using the "decompress"
# option).
#
USE_REAL_FILE = False

def test_first_download(testout):
  outdir=testout("first_download")
  sh.rm(outdir, "-rf")
  downloader = Downloader(str(outdir))
  if not USE_REAL_FILE:
    downloader.set_testmode()
  was_downloaded = downloader.run()
  assert was_downloaded
  if not USE_REAL_FILE:
    assert os.path.exists(outdir/downloader.DUMPFILENAME)
  assert os.path.exists(outdir/downloader.TIMESTAMP)

def test_no_newer_version(testout):
  outdir=testout("no_newer_version")
  sh.rm(outdir, "-rf")
  sh.mkdir(outdir, "-p")
  sh.touch(outdir/Downloader.TIMESTAMP)
  future = time.time() + 3600
  os.utime(outdir/Downloader.TIMESTAMP, (future, future))
  downloader = Downloader(str(outdir))
  downloader.set_testmode()
  was_downloaded = downloader.run()
  assert not was_downloaded
  assert not os.path.exists(outdir/downloader.DUMPFILENAME)

def test_newer_version(testout):
  outdir=testout("newer_version")
  sh.rm(outdir, "-rf")
  downloader = Downloader(str(outdir))
  downloader.set_testmode()
  downloader.run()
  stinfo = os.stat(outdir/downloader.DUMPFILENAME)
  mtime = stinfo.st_mtime
  before_last_version = mtime - 18000
  os.utime(outdir/Downloader.TIMESTAMP, \
           (before_last_version, before_last_version))
  os.unlink(outdir/downloader.DUMPFILENAME)
  assert not os.path.exists(outdir/downloader.DUMPFILENAME)
  was_downloaded = downloader.run()
  assert was_downloaded
  assert os.path.exists(outdir/downloader.DUMPFILENAME)

