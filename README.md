Fastsubtrees is a Python library and a set of scripts, for handling fairly
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

# Node identifiers

Each node must be represented by a unique positive ID. The IDs must not
necessarily be all consecutive (i.e. some "holes" may be present), but the
largest node ID (_idmax_) should not be much larger than the total number of
nodes, because the memory consumption is in O(idmax).

The NCBI taxonomy tree, for example, fullfills the conditions stated above.

However, the library can be used on any other tree. For this, if the IDs are
non-numerical, contain zero or negative numbers, or the ID space is not compact,
they must be first mapped to different IDs.

# Attributes

Besides a numerical node identifier, for each node of the tree additional
information can be stored in form of _attributes_.  Any number of attributes
can be created.  Each node can contain a single value or a set of values for an
attribute, but there is no requirement that all nodes have values for an
attribute.

For each attribute defined in a tree, a file is created, where the attribute
values are stored. The attributes are also stored in deep-first traversal
order, so that the list of attribute values for an entire subtree can be
queried efficiently.

# Tree construction

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

# CLI and API

Command line scripts are provided, which allow to perform all implemented
operations: construct a tree, add and delete leaf nodes
and subtrees, perform a subtree query, add attribute information.

The scripts are designed to be very flexible: e.g. the data source for
tree construction, or for obtaining attribute values, can be freely
defined by the user and passed to the scripts as Python code
and configuration data. Modules for the most common cases (database,
tabular file) are provided.

The scripts are described in the document ``docs/cli.md``.
Alternatively, the library functionality can be also directly accessed using
the API, which are documented in ``docs/api.md`.

