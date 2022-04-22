# NtMirror

NtMirror is a tool for creating and keeping up-to-date a local
mirror of the NCBI Taxonomy database

## Requirements

The software is distributed as a Python 3 package.
The file ``requirements.txt`` lists the required pip modules
(installable using ``pip -r requirements.txt``).

A relational database management system (RDBMS) is required.
NtMirror has been developed and tested using MariaDB as RDBMS.
However, it can be probably used with any RDBMS supported by SqlAlchemy.

Optionally, on MariaDB, the database data loading is performed using the
``mysql`` library and not using SqlAlchemy, since the loading is faster.

## Usage manual

For more information on the use of the software, see the
[user manual](https://github.com/ggonnella/ntmirror/blob/main/docs/user_manual.md).
