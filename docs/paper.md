# Statement of need

Tree representations are commonly used in different informatics application
fields to represent hierarchical information. For example, in Bioinformatics,
trees are often used to represent the phylogenetic relation of taxa. A related
application is in taxonomy, where trees are used for representing the
hierarchical classification of living organisms, which, in modern times, is
based on their phylogenetic relations.

The NCBI taxonomy (REF) tree is an example of taxonomic tree representation. It
consists of xxx nodes (as of xxx), each represented by a positive integer node
identifier. Biologically relevant information, e.g. genome sequence
statistics, can be mapped to the tree nodes. It is then interesting to extract
subtrees, under different nodes of the tree (subtree roots). e.g. for comparing
value distributions in different taxonomic groups.

The efficiency of the subtree extraction operation depends on the
implementation used for the data representation of the tree. When using a
database, e.g. the tables provided by NCBI as dump files, a subtree can be
extracted using a SQL hierarchical query. However, this can be quite slow in
practice.

A more efficient solution in terms of running time is to represent the tree
information in memory. For this solution to be scalable to large trees, some
care must be taken. First, the tree information must be stored in a compact
manner. Furthermore, an index is necessary, in order to find the subtree root
in constant time.

# Main features

Here we present _fastsubtrees_, a Python package, which allows to store tree
information using a compact representation, suitable for the fast extraction of
any subtree. It can be installed using ``pip install fastsubtrees``. Its
functionality can be used through either executable scripts or an API, which
can be employed from other Python programs. Manuals are provided for both
kind of interfaces.

The first step to use _fastsubtrees_ is to generate the file containing the
tree representation. For this step, the user must provide a generator function
yielding pairs of node numbers (parent and child node), describing the tree, in
any order. Each node must be represented by a unique positive ID. The IDs space
must be compact, i.e. the numbers are not necessarily all consecutive, bu the
largest node ID (_idmax_) should not be much larger than the total number of
nodes, because the memory consumption is in O(idmax). If this condition is not
met, the existing node labels must be mapped to a compact set of positive
integers. The generator function mechanism allows using the library for
constructing trees from any source (e.g. from tabular files, or from database
tables). Examples of generator functions are provided.

After the tree representation has been created or loaded from file, it can be
used for finding any node in constant time and extracting the subtree under
that node in time proportional to the output subtree size. To achieve this, in
the tree representation the node numbers and the subtree sizes under each node
are stored in depth-first traversal order. Furthermore, an index table is
provided which gives the ordinal position of each node in the depth-first
representation.

The tree representation is dynamic, i.e. it is possible to add and remove
subtrees. The subtree adding is achieved by finding the insertion position
in the depth-first representation and adding there the subtree, and
correcting accordingly the node positions in the index table. The subtree
removing is achieved by marking the corresponding nodes as deleted.

Along with numerical node identifiers, additional information can be stored for
each node, by defining any number of optional node attributes. These can be any
numerical or string information (including e.g. the original node labels, if
they were not a compact set of positive integers). Any desired numbers of
attributes can be used. For each attribute defined in a tree, a file is
created, where the attribute values are stored. The attributes are stored in
the same depth-first traversal order as the nodes in the tree representation,
so that the list of attribute values for an entire subtree can be queried
efficiently.

# Extracting NCBI taxonomy subtrees

Although the _fastsubtrees_ library can be applied to any tree, it was developed
with the main purpose of extracting subtrees of the NCBI taxonomy tree.

Dump files containing the tree information can be obtained from the NCBI FTP
site (XXX). To facilitate obtaining the dump file and keeping the local copy
up-to-date, a Python package _ntmirror_ (XXX) was developed, which allows to
download the latest copy of the taxonomy database, if needed, and optionally
load the information into a local database.

The tree contains 2949637 nodes as of May 28, 2022. The generation of the tree
representation from the dump files required (in average)
23 minutes and 35 seconds.


