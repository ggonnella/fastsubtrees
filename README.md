# Fastsubtrees

Fastsubtrees is a Python library and a command line script, for handling fairly
large trees (in the order of magnitude of millions nodes), in particular
allowing the fast extraction of any subtree.

The main application domain of fastsubtrees is working with the NCBI taxonomy
tree, however the code is implemented in a generic way, so that other
applications are possible.

For achieving an efficient running time and memory use, the nodes of the tree
are represented compactly in deep-first traversal order.
Subtrees are then extracted in O(s) time, where s is the size of the extracted
subtree (i.e. not depending on the size of the whole tree).

The tree representation can be saved to file, so that it must be not be
re-computed each time. It is dynamical, i.e. after a tree has been created,
it can be modified, by adding a new leaf node,
or an entire subtree under an existing node. Also, existing leaf nodes or
entire subtrees can be deleted.

Along with numerical node identifiers, additional
information can be stored for each node, by defining any number of optional
node attributes.

## Node identifiers

Each node must be represented by a unique positive ID. The IDs must not
necessarily be all consecutive (i.e. some "holes" may be present), but the
largest node ID (_idmax_) should not be much larger than the total number of
nodes, because the memory consumption is in _O(idmax)_.

The NCBI taxonomy tree, for example, fullfills the conditions stated above.

However, the library can be used on any other tree. For this, if the IDs are
non-numerical, contain zero or negative numbers, or the ID space is not compact,
they must be first mapped to different IDs.

## Attributes

Besides a numerical node identifier, for each node of the tree additional
information can be stored in form of _attributes_.  Any number of attributes
can be created.  Each node can contain a single value or a set of values for an
attribute, but there is no requirement that all nodes have values for an
attribute.

For each attribute defined in a tree, a file is created, where the attribute
values are stored. The attributes are also stored in deep-first traversal
order, so that the list of attribute values for an entire subtree can be
queried efficiently.

## Tree construction

For the construction of the tree a data source for the tree node identifiers
must be provided. For each node, the data source must provide the ID of the node
itself and of its parent. No particular order of the data is
required, i.e. a child node information may be provided before or after its
parent node.
The data source can be e.g. a database table or a tabular file
(or anything else).

The same interface is used when adding a new subtree
(with the difference, in the current implementation, that in this case
child nodes must be provided after their parent node).

## Working with the library

### Installation

The package can be installed using ``pip install fastsubtrees``.

### Docker

To try or test the package, it is possible to use ``fastsubtrees``
by employing the Docker image defined in ``Dockerfile``.
This does not require any external database installation and configuration.

```
# create a Docker image
docker build --tag "fastsubtrees" .

# create a container and run it
docker run -p 8050:8050 --detach --name fastsubtreesC fastsubtrees
# or, if it was already created and stopped, restart it using:
# docker start fastsubtreesC

# run the tests
docker exec fastsubtreesC tests

# run the benchmarks, skipping repeating tree creation
docker exec fastsubtreesC benchmarks

# run all benchmarks, including tree creation
docker exec fastsubtreesC benchmarks --all

# run the example application
docker exec fastsubtreesC start-example-app
# now open it in the browser at https://0.0.0.0:8050
```

### Tests

To run the test suite, you can use ``pytest`` (or ``make tests``).
The tests include tests of ``fastsubtrees`` and of the sub-package ``ntmirror``.
The latter are partly dependent on a database installation and configuration
which must be given in ``ntmirror/tests/config.yaml``;
database-dependent tests are skipped if this configuration file is not provided.

The entire test suite can be also run from the Docker container,
without further configuration, see above the _Docker_ section.

### Benchmarks

Benchmarks can be run using the shell scripts provided under ``benchmarks``.
These require data, which is downloaded from NCBI taxonomy and
some pre-computed example data which is provided in the ``data`` subdirectory
(genome sizes and GC content).

The benchmarks can be convienently run from the Docker container, without
requiring a database installation and setup, see above the _Docker_ section.

The ```_all``` version also benchmarks the construction of the representation
of the NCBI taxonomy tree and requires about 40-70 minutes to complete,
depending on the system.

### Command line interface

The command line tool ``fastsubtrees`` allows constructing a tree, modifying it
(by adding and deleting leaf nodes or subtrees), adding attributes,
and performing a subtree query (listing IDs or attribute values in a subtree).

The scripts are designed to be very flexible: e.g. the data source for
tree construction, or for obtaining attribute values, can be freely
defined by the user and passed to the scripts as Python code
and configuration data. Modules for the most common cases (database,
tabular file) are provided.

The command line interface is further described in the
[CLI manual](https://github.com/ggonnella/fastsubtrees/blob/main/docs/cli.md).

#### CLI example: NCBI taxonomy tree

This is an example of the basic operations using the NCBI taxonomy tree:
```
# download the NCBI taxonomy database dumps
ntmirror-download ntdumps
# construct the fastsubtrees tree data structure
fastsubtrees construct nt.tree --ntdump ntdumps
# query the IDs under node 562
faststubrees query nt.tree 562
```

The following adds attributes
from the example data (GC content and genome size of Bacterial genomes)
stored in the repository:

```
# add a genome size attribute from a tabular file
# the IDs are in column 1, the values in column 2 of the table
fastsubtrees attribute nt.tree genome_size --tab \
  data/accession_taxid_attribute.tsv.gz 1 2

# add a GC content attribute from a tabular file
# the IDs are in column 1, the values in column 3 of the table
fastsubtrees attribute nt.tree GC_content --tab \
  data/accession_taxid_attribute.tsv.gz 1 3
```

Once the attributes are created, their values in any subtree can be
easily queried:
```
# query the genome size values under node 562
fastsubtrees query nt.tree 562 genome_size GC_content
```

#### Adding the taxa names

Taxa names can be displayed alongside the taxa ID, by storing them
as an attribute. To extract the names from the NCBI taxonomy database
dumps, the _ntdownload_ package provides a ``ntnames`` command:

```
# extract the names from the dump files
ntnames ntdumps > names.tsv
# create the attribute file
fastsubtrees attribute nt.tree taxname --tab names.tsv
# query ID, taxa names and genome sizes in a subtree
fastsubtrees query nt.tree 562 taxname genome_size
```

#### CLI example with generic data

Fastsubtrees is not only usable with the NCBI taxonomy tree. The following
example constructs a tree with example data included with the repository
loading it from a tabular file.

```
# construct the tree, using a tabular file as data source
fastsubtrees construct small.tree --tab tests/testdata/small_tree.tsv
```

The data source can be differet: for example also a differently
formatted tabular file or a database table. For these cases, a Python
module is passed, which yields the tree data, as described in the
CLI manual.

### API

The library functionality can be also directly accessed in Python code using
the API, which is documented in the
[API manual](https://github.com/ggonnella/fastsubtrees/blob/main/docs/api.md).

## Subpackages

### ntmirror

When working with the NCBI taxonomy database, a local copy of the NCBI taxonomy
dump can be obtained and kept up-to-date using the _ntmirror_ package, which
is located in the directory ``ntmirror``. It is a Python package, which can
be installed using ``pip``, separately from _fastsubtrees_.

Besides downloading the dump, when needed, the package also allows to load
the NCBI taxonomy database in a local SQL database, and to extract subtrees
from it using hierarchical SQL queries.

Please refer to the user manual of _ntmirror_ located under ``ntmirror/docs``
for more information.

### Genomes Attributes Viewer

An interactive web application based on ``fastsubtrees`` was developed using
_dash_. It allows to graphically display the distribution of values of
attributes in subtrees of the NCBI taxonomic tree.

It can be installed and started locally (see below) or using the Docker image of
_fastsubtrees_ (see above in the _Docker_ section).

For more information see also the ``genomes-attributes-viewer/README.md`` file.

#### Local installation and startup

To application can be installed using ``pip install genomes_attributes_viewer``
or from the ``genomes_attributes_viewer`` directory of the _fastsubtrees_
repository.

To start the application, use the ``genomes-attributes-viewer``.
The first time this command is run, the application data are downloaded and
prepared, taking about 20 minutes to complete. Startup on subsequent
starts does not require these operations and is thus very fast.

## Community guidelines

Contributions to the software are welcome. Please clone this repository
and send a pull request on Github, to let the changes be integrated in
the original repository.

In case of bugs and issues, please report them through the Github Issues page
of the repository.
