---
title: 'Fastsubtrees: simple and efficient subtrees extractions in Python with applications to NCBI taxonomy'
tags:
- Python
- tree
- subtrees extraction
- bioinformatics
- taxonomy
authors:
- name: Aman Modi
  orcid: 0000-0002-9843-7133
  equal-contrib: true
  affiliation: "1"
- name: Giorgio Gonnella
  orcid: 0000-0003-3900-5397
  equal-contrib: true
  corresponding: true
  affiliation: "1, 2"
affiliations:
- name: Department of Bioinformatics (IMG), University of Göttingen, Göttingen, Germany
  index: 1
- name: Center for Bioinformatics (ZBH), University of Hamburg, Hamburg, Germany
  index: 2
date: 8 July 2022
bibliography: paper.bib
---

# Summary

Tree data structures are commonly used for representing hierarchical data. A
prominent example in bioinformatics are taxonomic trees, representing the
biological classification of organisms, currently containing millions of nodes.
An interesting operation for such trees is the extraction of the IDs and other
associated values for each node in a given subtree.
Here we present _fastsubtrees_, a Python package which provides a simple and
efficient way to perform this operation, by storing the tree data in a suitable
representation. The package provides a command line interface and a
application programming interface. While the software is written in a generic
way and can be applied to other trees as well, it is mainly aimed at working
with the NCBI taxonomy tree.

# Statement of need

Tree data structures are commonly used in different fields of computer science
to represent hierarchical information [@Black:1999]. In
phylogenetics, trees are used to represent the common ancestry of
organisms or macromolecules. Based on phylogenetics is the hierarchical
biological classification of organisms, which is also representable
as a tree. An example of this
is the NCBI taxonomy database [@Schoch:2020].

If the taxonomic tree
is annotated with data associated to taxa, hereafter called _attributes_
(e.g. sequence or annotation statistics), an interesting operation is the
extraction of distribution of values of an attribute in a given subtree, or
in multiple subtrees, which are compared to each other.
This allows for instance to identify uncommon values in some members of a taxon,
which in turn can be used in a primer for new biological hypotheses.

No Python package currently allows for a simple and efficient extraction of a
subtree, including data associated with the subtree nodes.
While software exists for visualizing data associated with phylogenetic
or taxonomic subtrees, e.g. AnnoTree [@Mendler:2019] and Treehouse
[@Steenwyk:2019], these are standalone software not simple
to integrate in other applications.

# The fastsubtrees Python package

Here we present the  _fastsubtrees_ Python package [@FastsubtreesRepo], which was developed
for storing tree information using a compact representation,
suitable for fast extraction of any subtree.
This package can be applied to any tree in which the nodes
are labeled by positive integers. I.e., although it was designed and
tested mainly for the NCBI taxonomy tree, it is not limited to it.

It can be installed using ``pip install fastsubtrees``.
The package functionality can be used
through either executable scripts or an API, which can be employed from other
Python programs. Manuals are provided for both kind of interfaces. A complete
test suite based on _pytest_ is provided. Running the complete tests, comparative
benchmarks and the example application (see below) requires a database
installation and setup; however, a Docker image is provided, which allows
to simply run benchmarks, tests and the example application without this hassle.

The first step when using _fastsubtrees_ is constructing its tree
representation and storing it to file. Any source can be used as input (e.g. tabular files, or
database tables) by defining a generation function (example are provided).
Besides the NCBI taxonomy tree, other trees can be represented using
_fastsubtrees_. For this, each node must be labeled by a unique positive ID.
Furthermore, the IDs space
must be compact, i.e. the numbers must not be necessarily all consecutive, but the
largest node ID (_idmax_) should not be much larger than the total number of
nodes, because the memory consumption is in _O(idmax)_.

In the tree representation, the node numbers and the subtree sizes under each
node are stored in depth-first traversal order.  Furthermore, an index table is
provided which gives the ordinal position of each node in the depth-first
representation.  Finally, any number of numerical or string attributes can be
associated to the nodes: these are stored in separate files, in the same order
as the node identifiers.  Thus, from the tree representation, any node and its
associated data can be found in constant time and the subtree under a node can
be output in time proportional to the subtree size. The representation is
dynamic, i.e. it is possible to add and remove subtrees.

# Subtree extraction benchmarks

Benchmarks were performed on a MacBook Pro 2021 with Apple M1 Pro CPU
and 32 Gb RAM. Running times were measured as an average of 3 runs using
GNU time version 1.9 [@GNUtime].
For the tests Python version 3.10.2 was used.
The tested version of fastsubtrees was 2.0.

The NCBI taxonomy tree used for the tests was downloaded on October 7, 2022
from the NCBI FTP website [@NCBI:FTP].
For downloading and keeping up-to-date a copy of the dump files using Python
we developed the _ntdownload_ package (located in the directory ``ntdownload``
of the source code repository, version 1.4)
[@NTDOWNLOAD] installable using ``pip install ntdownload``.
The tree contained 2447574 nodes. The generation of the tree
representation of the NCBI taxonomy tree from the dump files
using the _fastsubtrees construct_ command required
9 minutes and 23 seconds (average of 3 runs).

An alternative to the use of _fastsubtrees_ is to store the tree data in a SQL
database and extract subtrees using hierarchical SQL queries. We implemented
this solution in a package _ntmirror_: the dump data downloaded by _ntdownload_
is loaded into a MariaDB database (version 10.6.10)
and the script _ntmirror-extract-subtree_, based on
SQLAlchemy allows to extract a subtree using SQL.
The installation of _ntmirror_ using ``pip`` requires the installation
of MariaDB and its Python connector (_mariadb_ package).

To select subtrees of different sizes for the benchmarks, we started from the
taxonomy ID of _Escherichia coli_ K12 MG1655 (511145) and climbed up the
taxonomy tree, including all parent nodes in the benchmarks, up to the Bacteria
node (TaxID 2), i.e. nodes 83333 (_Escherichia coli_ K12),
562 (_Escherichia coli_), 561 (_Escherichia_ genus), 543 (Enterobacteriaceae),
91347 (Enterobacterales), 1236 (Gammaproteobacteria) and 1224 (Proteobacteria).
The running time and memory usage of _fastsubtree_ are compared with those for
hierarchical SQL queries in Table 1.

| Subtree root ID | Subtree size | SQL CPU time (s) | fastsubtrees CPU time (s) | SQL real time (s) | fastsubtrees real time (s) | SQL memory peak (MB) | fastsubtrees memory peak (MB) |
|-----------------|--------------|------------------|---------------------------|-------------------|----------------------------|----------------------|-------------------------------|
| 511145 | 1 | 0.29 | 0.18 | 1.58 | 0.19 | 41.3 | 153.6 |
| 83333 | 36 | 0.30 | 0.17 | 2.75 | 0.18 | 41.4 | 153.1 |
| 562 | 3381 | 0.30 | 0.18 | 4.86 | 0.18 | 48.1 | 153.1 |
| 561 | 4436 | 0.32 | 0.17 | 5.88 | 0.18 | 50.4 | 153.1 |
| 543 | 22750 | 0.48 | 0.19 | 35.43 | 0.19 | 89.1 | 153.1 |
| 91347 | 31609 | 0.60 | 0.19 | 37.16 | 0.19 | 106.3 | 153.1 |
| 1236 | 123300 | 1.56 | 0.23 | 60.22 | 0.23 | 294.8 | 153.1 |
| 1224 | 228153 | 2.67 | 0.27 | 89.33 | 0.28 | 511.8 | 153.1 |
| 2 | 535272 | 5.85 | 0.41 | 132.54 | 0.42 | 1142.0 | 153.1 |

As an example of attributes associated to tree nodes, we computed GC content and genome size for each bacterial
genome in the NCBI Refseq database [@Oleary:2015]. The results, available
in the repository, contain values for 27967 genomes.
The genome size attribute file generation using the
_fastsubtrees attribute_ command required 2.9 seconds.
Table 2 reports the running time and memory usage for the extraction
of the genome size attribute values for different subtrees.

| Subtree root ID | Subtree size | CPU time (s) | Real time (s) | Memory peak (MB) | N. nodes with values | N. values |
|-----------------|--------------|--------------|---------------|------------------|----------------------|-----------|
| 511145 | 1 | 0.49 | 0.50 | 153.1 | 1 | 9 |
| 83333 | 36 | 0.49 | 0.50 | 153.1 | 8 | 38 |
| 562 | 3381 | 0.54 | 0.55 | 153.4 | 165 | 2160 |
| 561 | 4436 | 0.53 | 0.53 | 153.5 | 174 | 2246 |
| 543 | 22750 | 0.54 | 0.55 | 153.5 | 839 | 5774 |
| 91347 | 31609 | 0.56 | 0.57 | 153.7 | 1150 | 6709 |
| 1236 | 123300 | 0.67 | 0.68 | 154.0 | 2830 | 11178 |
| 1224 | 228153 | 0.78 | 0.79 | 154.2 | 5099 | 16072 |
| 2 | 535272 | 1.11 | 1.12 | 155.3 | 10043 | 27515 |

Finally, to provide an example of usage of fastsubtrees we implemented an interactive
web application, Genomes Attributes Viewer, based on the _dash_ library version 2.0.0 [@Dash]
The application (in the subdirectory _genomes-attributes-viewer_ of the source
code repository) allows displaying diagrams of the
value distribution of GC content and genome size values in any subtree of the
NCBI taxonomy tree (we have included in the example only values for
bacterial genomes, see above). Attribute value distributions for multiple
subtrees can be thereby compared graphically.

# Author Contributions

Aman Modi: software development, test suite, example application,
documentation and benchmarks.

Giorgio Gonnella: funding acquisition, conceptualization,
software development, test suite, documentation, Docker image,
project supervision and manuscript redaction.

# Funding

Giorgio Gonnella has been supported by the DFG Grant GO 3192/1-1 ‘‘Automated
characterization of microbial genomes and metagenomes by collection and
verification of association rules’’. The funders had no role in study design,
data collection and analysis, decision to publish, or preparation of the
manuscript.

# Acknowledgements

The authors would like to thank Serena Lam (Department of Bioinformatics,
University of Göttingen) for language style suggestions and grammar corrections

# References
