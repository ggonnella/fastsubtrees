#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#
import pytest
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

@pytest.mark.script_launch_mode('subprocess')
def test_first_download(testout, script, script_runner):
  outdir=testout("first_download")
  sh.rm("-rf", outdir)
  args = [outdir, "--exitcode"]
  if not USE_REAL_FILE:
    args.append("--testmode")
  ret = script_runner.run(script("ntdownload"), *args)
  assert ret.returncode == 0
  assert os.path.exists(outdir/Downloader.TIMESTAMP)
  assert os.path.exists(outdir/CONTAINED_FILENAME)

@pytest.mark.script_launch_mode('subprocess')
def test_no_newer_version(testout, script, script_runner):
  outdir=testout("no_newer_version")
  sh.rm("-rf", outdir)
  sh.mkdir("-p", outdir)
  sh.touch(outdir/Downloader.TIMESTAMP)
  future = time.time() + 3600
  os.utime(outdir/Downloader.TIMESTAMP, (future, future))
  args = [outdir, "--exitcode", "--testmode"]
  ret = script_runner.run(script("ntdownload"), *args)
  assert ret.returncode == 100
  assert not os.path.exists(outdir/CONTAINED_FILENAME)

@pytest.mark.script_launch_mode('subprocess')
def test_newer_version(testout, script, script_runner):
  outdir=testout("newer_version")
  sh.rm("-rf", outdir)
  args = [outdir, "--exitcode", "--testmode"]
  ret = script_runner.run(script("ntdownload"), *args)
  assert ret.returncode == 0
  mtime = os.stat(outdir/Downloader.TESTFILENAME).st_mtime
  before_last_version = mtime - 18000
  os.utime(outdir/Downloader.TIMESTAMP, \
           (before_last_version, before_last_version))
  os.unlink(outdir/CONTAINED_FILENAME)
  assert not os.path.exists(outdir/CONTAINED_FILENAME)
  ret = script_runner.run(script("ntdownload"), *args)
  assert ret.returncode == 0
  assert os.path.exists(outdir/CONTAINED_FILENAME)

@pytest.mark.script_launch_mode('subprocess')
def test_no_unpack(testout, script, script_runner):
  outdir=testout("no_upack")
  sh.rm("-rf", outdir)
  args = [outdir, "--exitcode", "--no-unpack"]
  if not USE_REAL_FILE:
    args.append("--testmode")
  ret = script_runner.run(script("ntdownload"), *args)
  assert ret.returncode == 0
  assert os.path.exists(outdir/Downloader.TIMESTAMP)
  assert os.path.exists(outdir/ARCHIVE_FILENAME)

@pytest.mark.script_launch_mode('subprocess')
def test_force_https(testout, script, script_runner):
  outdir=testout("no_upack")
  sh.rm("-rf", outdir)
  args = [outdir, "--exitcode", "--force-https"]
  if not USE_REAL_FILE:
    args.append("--testmode")
  ret = script_runner.run(script("ntdownload"), *args)
  assert ret.returncode == 0
  assert os.path.exists(outdir/Downloader.TIMESTAMP)
  assert os.path.exists(outdir/CONTAINED_FILENAME)

@pytest.mark.script_launch_mode('subprocess')
def test_exception2(testout, script, script_runner):
  outdir=testout("exception2")
  sh.rm("-rf", outdir)
  args = [str(outdir), "--protocol", "fake"]
  if not USE_REAL_FILE:
    args.append("--testmode")
  ret = script_runner.run(script("ntdownload"), *args)
  assert ret.returncode == 1
  assert "ERROR" in ret.stderr
  assert not os.path.exists(outdir/Downloader.TIMESTAMP)
  assert not os.path.exists(outdir/CONTAINED_FILENAME)


