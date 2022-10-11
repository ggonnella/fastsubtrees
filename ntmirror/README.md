# NtMirror

NtMirror is a tool for creating and keeping up-to-date a local
mirror of the NCBI Taxonomy database.

## Requirements

The software is distributed as a Python 3 package.

An installation by pip is only possible, if the ``mariadb``
module is installed (which requires installation of MariaDB
and its C and Python connectors).

In MariaDB, the database data loading is performed using the
``mysql`` library and not using SqlAlchemy, since the loading is faster.

## Adapting to other RDBMS

NtMirror has been developed and tested using MariaDB as RDBMS.
However, database data loading using SqlAlchemy was also implemented,
so that the software can be used or easily adapted to
other RDBMS supported by SqlAlchemy.

## Usage manual

