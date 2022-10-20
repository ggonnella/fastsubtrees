#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#
import sh
import time
import os
from ntdownload import Downloader

#
# By default, the test will be done downloading a smaller file
# (taxdump_readme.txt) instead of the dump file (taxdump.tar.gz).
#
# If the following variable is set to True, the test "test_first_download"
# will be done downloading the full dump file (and using the "decompress"
# option).
#
USE_REAL_FILE = False

if USE_REAL_FILE:
  CONTAINED_FILENAME = "README.md"
  ARCHIVE_FILENAME = Downloader.DUMPFILENAME
else:
  CONTAINED_FILENAME = Downloader.TESTFILENAME
  ARCHIVE_FILENAME = CONTAINED_FILENAME + Downloader.ARCHIVE_SUFFIX

def test_first_download(testout):
  outdir=testout("first_download")
  sh.rm("-rf", outdir)
  downloader = Downloader(outdir)
  if not USE_REAL_FILE:
    downloader.set_testmode()
  was_downloaded = downloader.run()
  assert was_downloaded
  assert os.path.exists(outdir/downloader.TIMESTAMP)
  assert os.path.exists(outdir/CONTAINED_FILENAME)

def test_no_newer_version(testout):
  outdir=testout("no_newer_version")
  sh.rm("-rf", outdir)
  sh.mkdir("-p", outdir)
  sh.touch(outdir/Downloader.TIMESTAMP)
  future = time.time() + 3600
  os.utime(outdir/Downloader.TIMESTAMP, (future, future))
  downloader = Downloader(outdir)
  downloader.set_testmode()
  was_downloaded = downloader.run()
  assert not was_downloaded
  assert not os.path.exists(outdir/CONTAINED_FILENAME)

def test_newer_version(testout):
  outdir=testout("newer_version")
  sh.rm("-rf", outdir)
  downloader = Downloader(outdir)
  downloader.set_testmode()
  downloader.run()
  stinfo = os.stat(outdir/downloader.DUMPFILENAME)
  mtime = stinfo.st_mtime
  before_last_version = mtime - 18000
  os.utime(outdir/Downloader.TIMESTAMP, \
           (before_last_version, before_last_version))
  os.unlink(outdir/CONTAINED_FILENAME)
  assert not os.path.exists(outdir/CONTAINED_FILENAME)
  was_downloaded = downloader.run()
  assert was_downloaded
  assert os.path.exists(outdir/CONTAINED_FILENAME)

def test_no_unpack(testout):
  outdir=testout("no_unpack")
  sh.rm("-rf", outdir)
  downloader = Downloader(outdir)
  if not USE_REAL_FILE:
    downloader.set_testmode()
  was_downloaded = downloader.run(unpack=False)
  assert was_downloaded
  assert os.path.exists(outdir/Downloader.TIMESTAMP)
  assert os.path.exists(outdir/ARCHIVE_FILENAME)

def test_force_https(testout):
  outdir=testout("force_https")
  sh.rm("-rf", outdir)
  downloader = Downloader(outdir)
  if not USE_REAL_FILE:
    downloader.set_testmode()
  was_downloaded = downloader.run(force_https=True)
  assert was_downloaded
  assert os.path.exists(outdir/Downloader.TIMESTAMP)
  assert os.path.exists(outdir/CONTAINED_FILENAME)

def test_fallback_https(testout):
  outdir=testout("fallback_https")
  sh.rm("-rf", outdir)
  downloader = Downloader(outdir)
  downloader.PROTOCOL1 = "fakeftp"
  if not USE_REAL_FILE:
    downloader.set_testmode()
  was_downloaded = downloader.run()
  assert was_downloaded
  assert os.path.exists(outdir/Downloader.TIMESTAMP)
  assert os.path.exists(outdir/CONTAINED_FILENAME)
