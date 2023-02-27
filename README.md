# Fastsubtrees

[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](https://opensource.org/licenses/ISC)
[![Latest Github tag](https://img.shields.io/github/v/tag/ggonnella/fastsubtrees)](https://github.com/ggonnella/fastsubtrees/tags)
[![ReadTheDocs](https://readthedocs.org/projects/pip/badge/?version=stable)](https://fastsubtrees.readthedocs.io/)
[![PyPI](https://img.shields.io/pypi/v/fastsubtrees)](https://pypi.org/project/fastsubtrees/)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.04755/status.svg)](https://doi.org/10.21105/joss.04755)

_Fastsubtrees_ is a Python library and a command line script, for handling fairly
large trees (in the order of magnitude of millions nodes), in particular
allowing the fast extraction of any subtree.
The main application domain of _fastsubtrees_ is working with the NCBI taxonomy
tree, however the code is implemented in a generic way, so that other
applications are possible.

The library functionality can be accessed both from inside Python code
and from the provided command line tool ``fastsubtrees``.

## Introduction

For the use of _fastsubtrees_, nodes must be uniquely identified by non-negative IDs.
Furthermore, the space of the IDs must be compact (i.e. the maximum ID should not be
much larger than the number of IDs).

The first step when using _fastsubtrees_ is to construct a tree representation.
The operation requires a source of IDs of elements and their parents, which can be
a tabular file, or any Python function yielding the IDs.

This operation just takes a few seconds, for a tree with million nodes, such as the NCBI taxonomy tree.
It must be done only once, if a tree does not change, since the resulting data
is stored to file.

The IDs of the NCBI taxonomy tree fullfill the conditions stated above. However, the library
can be used for any tree. A way to use the library with IDs which do not fullfill the conditions,
it to map them to an ID space which does, and store the original IDs as an attribute.

Besides the IDs, a tree can contain further information, e.g. integers, floats or other
data, here called attributes, associated to the nodes. Each node can contain zero, one or more values
for an attribute. To add values for an attribute, a tabular file or another data
source (a Python function) is selected.

The data for any subtree can then be easily and efficently queried; thereby the node IDs and/other
selected attributes can be retrieved.

The tree representation is dynamic, i.e. both the tree topology and the attribute values can be
edited and changed.

## Working with the library

### Installation

The package can be installed using ``pip install fastsubtrees``.

### Command line interface

The command line tool ``fastsubtrees`` allows constructing and modifying a tree
(subcommand ``tree``), adding and editing attributes (subcommand ``attribute``)
and performing a subtree query (subcommand ``query``).

The command line interface is further described in the
[CLI manual](https://github.com/ggonnella/fastsubtrees/blob/main/docs/cli.md).

#### CLI example: working with the NCBI taxonomy tree

The example below uses the ``fastsubtrees`` command, as well as the ``ntdownload`` library
(installed as a dependency, by ``pip``) for obtaining the NCBI taxonomy data.

```
ntdownload ntdumps                                     # download NCBI taxonomy data
fastsubtrees tree nt.tree --ncbi ntdumps/nodes.dmp -f  # create the tree
fastsubtrees query nt.tree 562                         # query node 562

# attributes
ATTRTAB=data/accession_taxid_attribute.tsv.gz          # data file
TAXID=2; GENOME_SIZE=3; GC_CONTENT=4                   # column numbers, 1-based

fastsubtrees attribute nt.tree genome_size $ATTRTAB -e $TAXID -v $GENOME_SIZE -t int
fastsubtrees attribute nt.tree GC_content $ATTRTAB -e $TAXID -v $GC_CONTENT -t float

fastsubtrees query nt.tree 562 genome_size GC_content  # query including attributes

# taxonomy names
ntnames ntdumps >| names.tsv                           # prepare data from names dump
fastsubtrees attribute nt.tree taxname names.tsv       # add names as attribute
fastsubtrees query nt.tree 562 taxname genome_size     # query including taxa names
```

#### Using NtSubtree

The package ``ntsubtree`` (installable by ``pip``) simplifies working with the NCBI taxonomy even more.
Tree and the taxonomic names tables are automatically created and stored in a central location.

```
# first run after installing automatically downloads and constructs the tree

ntsubtree query 562               # taxonomic names displayed alongside the IDs
ntsubtree query -n "Escherichia"  # Query by taxonomic name

# attributes
ATTRTAB=data/accession_taxid_attribute.tsv.gz          # data file
TAXID=2; GENOME_SIZE=3; GC_CONTENT=4                   # column numbers

ntsubtree attribute genome_size $ATTRTAB -e $TAXID -v $GENOME_SIZE
ntsubtree attribute GC_content $ATTRTAB -e $TAXID -v $GC_CONTENT
ntsubtree query -n "Escherichia" genome_size GC_content

# check if a newer version of the taxonomy data is available
# and update the tree if necessary, keeping the attribute values:
ntsubtree update
```

### API

The library functionality can be also directly accessed in Python code using
the API, which is documented in the
[API manual](https://github.com/ggonnella/fastsubtrees/blob/main/docs/api.md).

#### API example: working with the NCBI taxonomy tree

The example below uses the ``fastsubtrees`` command, as well as the ``ntdownload`` library
(installed as a dependency, by ``pip``) for obtaining the NCBI taxonomy data.

```python
# download the NCBI taxonomy data
from ntdownload import Downloader
d = Downloader("ntdumpsdir")
has_downloaded = d.run()

from fastsubtrees import Tree
infile = "ntdumpsdir/nodes.dmp"
tree = Tree.construct_from_ncbi_dump(infile)     # create the tree
results = tree.subtree_ids(562)                   # retrieve subtree IDs

attrtab="data/accession_taxid_attribute.tsv.gz"         # data file
taxid_col=1; genome_size_col=2; gc_content_col=3        # column numbers, 0-based

tree.to_file("nt.tree")
tree.create_attribute_from_tabular("genome_size", attrtab, elem_field_num=taxid_col,
                                   attr_field_num=genome_size_col, casting_fn=int)
tree.create_attribute_from_tabular("GC_content", attrtab, elem_field_num=taxid_col,
                                   attr_field_num=gc_content_col, casting_fn=float)
results = tree.subtree_info(562, ["genome_size", "GC_content"])

# taxonomy names
from ntdownload import yield_scientific_names_from_dump as generator
tree.create_attribute("taxname", generator("ntdumpsdir"))
results = tree.subtree_info(562, ["taxname", "genome_size"])
```

#### Using NtSubtree

The package ``ntsubtree`` (installable by ``pip``) simplifies working with the NCBI taxonomy even more.
Tree and the taxonomic names tables are automatically created and stored in a central location.
The first time the library is included these operations are done automatically.

```python
import ntsubtree

tree = ntsubtree.get_tree()
results = tree.subtree_ids(562)

taxid = ntsubtree.search_name("Escherichia")
results = tree.subtree_info(taxid, ["taxname"])

attrtab="data/accession_taxid_attribute.tsv.gz"         # data file
taxid_col=1; genome_size_col=2; gc_content_col=3        # column numbers, 0-based

tree.create_attribute_from_tabular("genome_size", attrtab, elem_field_num=taxid_col,
                                   attr_field_num=genome_size_col, casting_fn=int)
tree.create_attribute_from_tabular("GC_content", attrtab, elem_field_num=taxid_col,
                                   attr_field_num=gc_content_col, casting_fn=float)
results = tree.subtree_info(562, ["genome_size", "GC_content"])

# check if a newer version of the taxonomy data is available
# and update the tree if necessary, keeping the attribute values:
ntsubtree.update()
```

### Docker

To try or test the package, it is possible to use ``fastsubtrees``
by employing the Docker image defined in ``Dockerfile``.
This does not require any external database installation and configuration.

<details>
    <summary>Example of the Docker command line:</summary>

```
# create a Docker image
docker build --tag "fastsubtrees" .

# create a container and run it
docker run -p 8050:8050 --detach --name fastsubtreesC fastsubtrees
# or, if it was already created and stopped, restart it using:
# docker start fastsubtreesC

# run the tests
docker exec fastsubtreesC tests

# run benchmarks
docker exec fastsubtreesC benchmarks

# run the example application
docker exec fastsubtreesC start-example-app
# now open it in the browser at https://0.0.0.0:8050
```
</details>
  
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

### Example application: Genome attributes viewer

An interactive web application based on ``fastsubtrees`` was developed using
_dash_. It allows to graphically display the distribution of values of
attributes in subtrees of the NCBI taxonomic tree.
It is a separate Python package, which can
be installed using ``pip``, and depends on _fastsubtrees_.

It can also be installed using the Docker image of
_fastsubtrees_ (see above in the _Docker_ section).

For more information see also the ``genomes-attributes-viewer/README.md`` file.

#### Local installation and startup

To application can be installed using ``pip install genomes_attributes_viewer``
or from the ``genomes_attributes_viewer`` directory of the _fastsubtrees_
repository.

To start the application, use the ``genomes-attributes-viewer``.
The first time this command is run, the application data are downloaded and
prepared, taking a few seconds. Startup on subsequent
starts does not require these operations and is thus faster.

### Other subpackages

#### NtSubtree

NtSubtree is a library which automatically downloads the NCBI taxonomy
dump and constructs the ``fastsubtrees`` data for it. It allows to easily
keep the data up-to-date. It is a separate Python package, which can
be installed using ``pip``, and depends on _fastsubtrees_.

The ``query`` command of the NtSubtree CLI tool automatically
display also taxonomic names, alongside the IDs in query and allow to
perform queries by taxonomic name.

For more information see also the ``ntsubtree/README.md`` file.

#### ntdownload

When working with the NCBI taxonomy database, a local copy of the NCBI taxonomy
dump can be obtained and kept up-to-date using the _ntdownload_ package, which
is located in the directory ``ntdownload``. It is a separate
Python package, which can be installed using ``pip``, independently
from _fastsubtrees_.

Please refer to the user manual of _ntdownload_ located under ``ntdownload/README.md``
for more information.

#### ntmirror

A downloaded NCBI taxonomy database dump can be loaded to
a local SQL database, using the package _ntmirror_, which is located
in the directory ``ntmirror``.
It is a separate Python package, which can
be installed using ``pip``, independently from _fastsubtrees_.

It contains also a script to extract subtrees
from the local database mirror using hierarchical SQL queries.

Please refer to the user manual of _ntmirror_ located under ``ntmirror/README.md``
for more information.

### Internals

For achieving an efficient running time and memory use, the nodes of the tree
are represented compactly in deep-first traversal order.
Subtrees are then extracted in O(s) time, where s is the size of the extracted
subtree (i.e. not depending on the size of the whole tree).

The IDs must not
necessarily be all consecutive (i.e. some "holes" may be present), but the
largest node ID (_idmax_) should not be much larger than the total number of
nodes, because the memory consumption is in _O(idmax)_.

For each attribute defined in a tree, a file is created, where the attribute
values are stored. The attributes are also stored in the same deep-first traversal
order as the tree IDs.

#### Tree construction algorithm

The tree construction algorithm used here is the following,
where the input data consists of 2-tuples ``(element_id, parent_id)``
and the maximum node ID m is not much larger than the number of IDs n.

1. iteration over the input data to construct a table _P_ of parents by ID,
i.e. ``P[element_id]=parent_id`` if ``element_id`` is in the tree,
and ``P[element_id]=UNDEF`` if not, where UNDEF is a special value.
This requires _O(n)_ steps
for reading the IDs and _O(m)_ steps for writing either the ID or the _UNDEF_
value to _P_; since _m>=n_, the total time is in _O(m)_.
2. iteration over table _P_ to construct a table _S_ of subtree sizes
by ID; for each element the tree is climbed to the root, to add the
element to the counts of each ancestor. This
operation requires _O(n*d)_ time, where _d_ is the height of the node,
which is in average case much lower than _m_ and _d=m_ is the worst case.
3. iteration over each node ID to construct the list _D_, consisting of the depth first order of
the nodes, and the table _C_ of the coordinates of all nodes in the tree data, by id.
For this operation, first the root is added to _D_ and _C_, then
for each other node _x_ in _P_, the tree is climbed and nodes added to a stack until the next not-yet-added
ancestor is found. The position where to add it this node is computed by the next
free position in the subtree of its parent (which must have been already added,
by definition, thus the next free position in its subtree is known). After this,
the next stack element is added, until _x_ is added.
Although this operation also requires climbing the tree, it takes in total _O(n)_ time,
since each node is added only once.

#### Parallelizing the tree construction

Currently the slowest step of the construction, detailed in the previous
section, is the second, i.e. the computation of _S_.
Since each node must be count in the subtree size of all its ancestors,
there is no easy way to reduce the time from _O(n*h)_.

To parallelize this step, one divides the parents table into _t_ slices,
and assign each to a different sub-process (not thread, because of the GIL).
Each sub-process would then count the subtree sizes in the slice only.
A version implemented with a shared table and a lock was too slow,
since access to the table was concurrent among the sub-processes.
In the current version, instead, each sub-process makes a own subtree sizes
_S'_ table. The sub-processes _S'_ tables are summed up after completion for
obtaining the _S_ table.

This option can be activated in the CLI using the ``--processes P`` option,
or in the API setting the ``nprocesses`` argument of ``Tree.construct`` and
related methods. Benchmarks show that the parallel version did not significantly
improve the performance on constructing the NCBI taxonomy tree, likely
because of the overhead of process starting, array _S'_ initialization
and summing up of all _S'_ to _S_ after completion.

## Community guidelines

Contributions to the software are welcome. Please clone this repository
and send a pull request on Github, to let the changes be integrated in
the original repository.

In case of bugs and issues, please report them through the Github Issues page
of the repository.

## Documentation

The complete documentation of Fastsubtrees is available on ReadTheDocs
at https://fastsubtrees.readthedocs.io/ in website and
[PDF format](https://fastsubtrees.readthedocs.io/_/downloads/en/latest/pdf/).

## Licence

All code of Fastsubtrees is released under the ISC license.
(see LICENSE file).
It is functionally equivalent to a two-term BSD copyright with
language removed that is made unnecessary by the Berne convention.
See http://openbsd.org/policy.html for more information on copyrights.

## Acknowledgements
This software has been originally created in context of the DFG project GO 3192/1-1
“Automated characterization of microbial genomes and metagenomes by collection and verification of association rules”.
The funders had no role in study design, data collection and analysis.
