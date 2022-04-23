# NtMirror User Manual

NtMirror downloads the NCBI taxonomy database dump.

After download it creates a timestamp file, so that the next time the download
is repeated only if a newer version is available.

The dump files are then decompressed and loaded into a local database.

## CLI

### Database dump download

To download the dump files, use the ``ntmirror-download`` script. Thereby the
output directory is passed as CLI argument. If it does not exist, it is
created.

The dump files archive is decompressed after download and deleted.

If the option ``--exitcode`` is used, then the exit code of the script is 100
if no newer version of the dump files was found, and thus nothing was
downloaded. Otherwise the exit code is always 0 (or 1 on error).

### Loading into the database

The script ``ntmirror-dbload`` is used to load the dump files into the
database. It takes as arguments the database username, its password, the
database name and the path to the connection socket as arguments, followed by
the directory where the dump files are located.

If the database tables do not exist, they are created.
If dump files are found, they are loaded into the database and deleted.
If no dump file is found, then nothing is done.

The exit code of the script is 0 on success and 1 if an error occurs. If the
option ``--exitcode`` is used, and no dump file is found, the exit code of the
script is 100 (instead of 0).

## API

### Database dump download

To download the dump files, use the Downloader class:
```
from ntmirror import Downloader
d = Downloader(output_directory_name)
has_downloaded = d.run()
```

The output directory is created if it does not exist. The dump files archive is
decompressed and the archive deleted, except if the option ``decompress=False``
is used.

The return value of ``run()`` is ``True`` if a dump file was downloaded,
``False`` if no newer version was available.

### Loading into the database

To create the database tables, a SqlAlchemy connection object is necessary.
This is passed to the ``dbschema.create(connection)`` method, which creates the
tables, if they do not exist yet.

To upload the dump files into the database, there are two options. If MariaDB
or MySQL is used, then the module ``dbloader_mysql`` can be used. This uses the
MySQLdb package and is faster. Otherwise, the ``dbloader_sqlalchemy`` module
can be used. The database must implement a ``LOAD DATA LOCAL INFILE`` SQL
command.

Both modules provide a ``load_all()`` function, to which the path of the
directory containing the dump files is passed. If no dump files are found,
nothing happens. Otherwise, the dump files are loaded into the database. The
function returns an array of tuples ``(filepfx, filepath)`` for each dump file
which was loaded into the database.

The ``dbloader_sqlalchemy`` version of ``load_all()`` takes two arguments: the
dump file directory and a SqlAlchemy connection object.

The ``dbloader_mysql`` version of ``load_all()`` takes as arguments the dump
file directory, the database hostname, database username, its password, the
database name and the path to the connection socket.
