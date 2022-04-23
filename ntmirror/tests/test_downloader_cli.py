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

@pytest.mark.script_launch_mode('subprocess')
def test_first_download(testout, script, script_runner):
  outdir=testout("first_download")
  sh.rm(outdir, "-rf")
  args = [outdir, "--exitcode"]
  if not USE_REAL_FILE:
    args.append("--testmode")
  ret = script_runner.run(script("ntmirror-download"), *args)
  assert ret.returncode == 0
  if not USE_REAL_FILE:
    assert os.path.exists(outdir/Downloader.TESTFILENAME)
  assert os.path.exists(outdir/Downloader.TIMESTAMP)

@pytest.mark.script_launch_mode('subprocess')
def test_no_newer_version(testout, script, script_runner):
  outdir=testout("no_newer_version")
  sh.rm(outdir, "-rf")
  sh.mkdir(outdir, "-p")
  sh.touch(outdir/Downloader.TIMESTAMP)
  future = time.time() + 3600
  os.utime(outdir/Downloader.TIMESTAMP, (future, future))
  args = [outdir, "--exitcode", "--testmode"]
  ret = script_runner.run(script("ntmirror-download"), *args)
  assert ret.returncode == 100
  assert not os.path.exists(outdir/Downloader.TESTFILENAME)

@pytest.mark.script_launch_mode('subprocess')
def test_newer_version(testout, script, script_runner):
  outdir=testout("newer_version")
  sh.rm(outdir, "-rf")
  args = [outdir, "--exitcode", "--testmode"]
  ret = script_runner.run(script("ntmirror-download"), *args)
  assert ret.returncode == 0
  mtime = os.stat(outdir/Downloader.TESTFILENAME).st_mtime
  before_last_version = mtime - 18000
  os.utime(outdir/Downloader.TIMESTAMP, \
           (before_last_version, before_last_version))
  os.unlink(outdir/Downloader.TESTFILENAME)
  assert not os.path.exists(outdir/Downloader.TESTFILENAME)
  ret = script_runner.run(script("ntmirror-download"), *args)
  assert ret.returncode == 0
  assert os.path.exists(outdir/Downloader.TESTFILENAME)

