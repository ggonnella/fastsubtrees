# NtDownload

NtDownload is a tool for downloading and keeping up-to-date a local
version of the NCBI Taxonomy database dump files

After download it creates a timestamp file, so that the next time the download
is repeated only if a newer version is available.

## Installation

The software is distributed as a Python 3 package and can be installed
using ``pip install ntdownload``.

## Command line interface

To download the dump files, use the ``ntdownload`` script. Thereby the
output directory is passed as CLI argument. If it does not exist, it is
created.

The dump files archive is decompressed after download and deleted.

If the option ``--exitcode`` is used, then the exit code of the script is 100
if no newer version of the dump files was found, and thus nothing was
downloaded. Otherwise the exit code is always 0 (or 1 on error).

## API

To download the dump files, use the Downloader class:
```
from ntdownload import Downloader
d = Downloader(output_directory_name)
has_downloaded = d.run()
```

The output directory is created if it does not exist. The dump files archive is
decompressed and the archive deleted, except if the option ``decompress=False``
is used.

The return value of ``run()`` is ``True`` if a dump file was downloaded,
``False`` if no newer version was available.

## ntnames

The script ``ntnames`` is provided, which, after download using ``ntdownload``
can be used for creating a list of taxonomy IDs and scientific names,
which can be used as attribute source file for fastsubtrees.

## Test suite

The test suite is run using ``pytest``.
