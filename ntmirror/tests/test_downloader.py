#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#
import pytest
import sh
import time
import os
from ntmirror import Downloader

def test_first_download(testout):
  # test download from NCBI taxonomy when no timestamp file exists
  sh.rm(testout("first_download"), "-rf")
  sh.mkdir(testout("first_download"), "-p")
  downloader = Downloader(str(testout("first_download")))
  downloader.DUMPFILENAME = "taxdump_readme.txt"
  was_downloaded = downloader.run(decompress=False)
  assert(was_downloaded)
  assert(os.path.exists(testout("first_download")/downloader.DUMPFILENAME))
  assert(os.path.exists(testout("first_download/timestamp")))

def test_no_newer_version(testout):
  sh.rm(testout("no_newer_version"), "-rf")
  sh.mkdir(testout("no_newer_version"), "-p")
  sh.touch(testout("no_newer_version/timestamp"))
  os.utime(testout("no_newer_version/timestamp"), \
           (time.time() + 1800, time.time() + 1800))
  downloader = Downloader(str(testout("no_newer_version")))
  downloader.DUMPFILENAME = "taxdump_readme.txt"
  was_downloaded = downloader.run(decompress=False)
  assert(not was_downloaded)
  assert(not os.path.exists(testout("no_newer_version")/\
                                    downloader.DUMPFILENAME))

def test_newer_version(testout):
  sh.rm(testout("newer_version"), "-rf")
  sh.mkdir(testout("newer_version"), "-p")
  downloader = Downloader(str(testout("newer_version")))
  downloader.DUMPFILENAME = "taxdump_readme.txt"
  downloader.run(decompress=False)
  stinfo = os.stat(testout("newer_version")/downloader.DUMPFILENAME)
  mtime = stinfo.st_mtime
  os.utime(testout("newer_version/timestamp"), \
           (mtime - 18000, mtime - 18000))
  os.unlink(testout("newer_version")/downloader.DUMPFILENAME)
  assert(not os.path.exists(testout("newer_version")/downloader.DUMPFILENAME))
  was_downloaded = downloader.run(decompress=False)
  assert(was_downloaded)
  assert(os.path.exists(testout("newer_version")/downloader.DUMPFILENAME))

