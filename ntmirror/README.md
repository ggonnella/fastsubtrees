# NtMirror

NtMirror is a tool for creating and keeping up-to-date a local
mirror of the NCBI Taxonomy database.

## Requirements

The software is distributed as a Python 3 package.

An installation by pip is only possible, if the ``mariadb``
module is installed (which requires installation of MariaDB
and its C and Python connectors).

## CLI

### Loading into the database

The script ``ntmirror-dbload`` is used to load the dump files into the
database. It takes as arguments the database username, its password, the
database name and the path to the connection socket, followed by
the directory where the dump files are located.

If the database tables do not exist, they are created.
If dump files are found, they are loaded into the database and deleted.
If no dump file is found, then nothing is done.

The exit code of the script is 0 on success and 1 if an error occurs. If the
option ``--exitcode`` is used, and no dump file is found, the exit code of the
script is 100 (instead of 0).

### Subtree search using hierarchical SQL

To list the IDs of a subtree of the NCBI taxonomy tree, the
``ntmirror-extract-subtree`` script can be used.
It takes as arguments the database username, its password, the
database name and the path to the connection socket, followed by
the subtree root ID.

### Example usage

The following example uses the ``ntdownload`` package to download the
dumps and loads them into the database and extracts a subtree
using ``ntmirror``.

```
ntdownload ntdumpsdir
ntmirror-dbload myuser mypass mydb /path/to/db.socket ntdumpsdir
ntmirror-extract-subtree myser mypass mydb /path/to/db.socket 562
```

## API

### Database setup

To create the database tables, a SqlAlchemy connection object is necessary.
This is passed to the ``dbschema.create(connection)`` method, which creates the
tables, if they do not exist yet.

### Loading the data using MariaDB

In MariaDB, the database data loading is performed using the
``mysql`` library and not using SqlAlchemy, since the loading is faster.

The ``dbloader_mysql.load_all(ntdumpsdir)``
function is used, to which the path of the
directory containing the dump files is passed,
followed by the database hostname, database username, its password, the
database name and the path to the connection socket.

If no dump files are found,
nothing happens. Otherwise, the dump files are loaded into the database. The
function returns an array of tuples ``(filepfx, filepath)`` for each dump file
which was loaded into the database.

### Example usage

The following example uses the ``ntdownload`` package to download the
dumps and loads them into the database and extracts a subtree
using ``ntmirror``.

```
from ntdownload import Downloader
from ntmirror import dbschema, dbloader_mysql

# this assumes that the SqlAchemy connection is available
dbschema.create(connection)

d = Downloader("ntdumpsdir")
d.run()
dbloader_mysql.load_all("ntdumpsdir", dbhostname, dbusername, dbpassword,
                        path_to_db_socket)
```

### Loading the data using another RDBMS

Database data loading using SqlAlchemy was also implemented,
so that the package can be used with other RDBMS,
although it is slower than using the ``dbloader_mysql`` module.

To upload the dump files into the database the ``dbloader_sqlalchemy`` module
can be used. The database must implement a ``LOAD DATA LOCAL INFILE`` SQL
command.
The ``dbloader_sqlalchemy`` version of ``load_all()`` takes two arguments: the
dump file directory and a SqlAlchemy connection object.


