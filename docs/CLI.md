# Command line interface

The command line interface of the library consists in a script ``fastsubtrees``
that can be used to construct and modify a tree, add attributes to nodes, and
query subtree IDs and attribute values.

The list of subcommands is displayed using ``fastsubtrees --help``.
Using ``--help`` after a subcommand (e.g. ``fastsubtrees tree --help``
displays the syntax and details of the subcommand.

The following subcommands are available:
```
  tree         Create or modify a tree.
  attribute    Create, modify or remove an attribute.
  query        List node IDs and/or attributes in a subtree.
```

## Tree construction

The subcommand ``fastsubtrees tree`` is used to construct the tree
representation, from data consisting in node IDs and the corresponding parent
IDs. The data can be obtained from a tabular file, or from a different data
source.

### Construction from a tabular file

If the IDs of the elements and their parents are contained in a tabular
file, the filename is given as an argument to ``fastsubtrees tree``, e.g.:
```
fastsubtrees tree my.tree
```

Details of the format can be specified using options. The separator
is specified using ``--separator`` (default: tab), the columns containing
the IDs using ``--elementscol`` and ``--parentscol`` (as
1-based column numbers, default: 1 and 2), and the prefix of comment/header
lines using ``--commentchar`` (default: #).

When using ``nodes.dmp`` from
the NCBI taxonomy tree dump, the preset ``--ncbi`` can be used.
Example:
```
fastsubtrees my.tree --ncbi ntdumpsdir/nodes.dmp
```

### Generalized tree construction

In the generalized tree construction mode, using the option ``--module``,
the path to a Python module is passed. The module defines a function, yielding
the node and parent IDs. The default function name is ``element_parent_ids``
and can be changed using the option ``--fn``.

All positional arguments given to the script are passed to the function.
If they contain a `=`, they are passed as keyword arguments (unless
the option ``--nokeys`` is used).
Examples:
```
fastsubtrees tree my.tree --module my_module.py a b c
fastsubtrees tree my.tree --module my_module.py k1=v1 k2=v=2 x --fn myfn
fastsubtrees tree my.tree --module my_module.py k1=v1 k2=v=2 x --nokeys
```

This is the called function in the tree cases:
```
element_parent_ids("a", "b", "c")
myfn("x", k1="v1", k2="v=2")
element_parent_ids("k1=v1", "k2=v=2", "x")
```

A module implementing the described interface for reading
from a tabular file is provided
under ``fastsubtrees/ids_modules/ids_from_tabular_file.py``.

## Modifying an existing tree representation

Existing tree representations can be modified using ``fastsubtrees tree``
with the options ``--update``, ``--add``  or ``--delete``.

### Updating or resetting a tree

If the option ``--update`` or ``--reset`` is provided, the tree is modified so
to reflect the given source of IDs of elements and their parents (tabular file
or Python function). The result is a tree, which is functionally equivalent to
a new tree, constructed with the same data source.

The difference between the two is that ``--update`` edits the existing tree and
attribute data, while ``--reset`` recomputes the tree data from scratch, after
dumping the attribute values and reconstructing the attribute files with the
dumped values afterwards.

The common advantage of using ``--update`` or ``--reset`` is that the attribute
files are not lost.
Generally the reset operation performs better, since tree creation is fast.
The update operation can be faster, if the tree is large and is only slightly
modified.

### Adding leaf nodes or new subtrees

If the option ``--add`` is used, new elements are added to an existing tree.
The elements must not yet be present in the tree and they must all be connected
to a node already present in the tree or added in the same operation.

### Removing leaf nodes or subtrees

If the option ``--delete`` is used, all remaining positional arguments of the
script are IDs of nodes. If a node is a leaf node, it is removed from the tree.
If it is an internal node, the entire subtree under that node is removed.

### Attributes when editing a tree

If attribute have been defined, as described in the following section,
the attribute files are automatically detected and modified too,
when adding or deleting nodes.

If nodes have been added by ``--add`` or ``--update``,
new attribute values for those nodes
can be added using ``fastsubtrees attribute --add``, as explained below.

## Tree attributes

The tree can contain further information, except the IDs, in the form of
attributes. Attribute values can be integers, floats or strings.
Not all nodes will necessarily have an attribute value associated
with them. Some nodes can contain multiple values for an attribute.
Attributes are managed by the subcommand ``fastsubtrees attribute``.

### Adding an attribute

To create a new attribute, a source of attribute values is
passed to ``fastsubtrees attribute``. Similar to the tree construction case,
the source can be a tabular file, or a Python module, specifiying a function
yielding node IDs and attribute values.
The same node ID can appear multiple times, in which case the
attribute values will all be stored, as a list.

By default, attribute values are stored as strings. The option
``--type f`` can be used to apply a function ``f()`` to each attribute
value. The function can be either from the standard library (e.g.
``int`` or ``float``, or, if ``--module`` is used, from that module.

#### Attribute values from a tabular file

To create an attribute from a tabular file, the filename is passed, e.g.
```
fastsubtrees attribute my.tree myattr value.tsv
```
Also in this case the format options can be used, for changing separator,
comment character and specifying the columns containing the ID of the
nodes (``--elementscol``) and attribute values (``--valuescol``).

#### Generalized source of attribute values

As a generalized attribute values source, the path to a Python module
is passed, using the option ``--module``. The module
defines a function, yielding
tuples ``(node_ID, attribute_value)``.
The default function name is ``attribute_values``
and can be changed using the option ``--fn``.

All positional arguments given to the script are passed to the function.
If they contain a `=`, they are passed as keyword arguments (unless
the option ``--nokeys`` is used).
Examples:
```
fastsubtrees attribute my.tree myattr --module my_module.py a b c
fastsubtrees attribute my.tree myattr --module my_module.py k1=v1 k2=v=2 x --fn myfn
fastsubtrees attribute my.tree myattr --module my_module.py k1=v1 k2=v=2 x --nokeys
```

This is the called function in the tree cases:
```
attribute_values("a", "b", "c")
myfn("x", k1="v1", k2="v=2")
attribute_values("k1=v1", "k2=v=2", "x")
```

An example module implementing the described interface is provided
under ``fastsubtrees/ids_modules/attrs_from_tabular_file.py``.

### Listing defined attributes

To list the attributes that have been created, use ``fastsubtrees attribute``
with the option ``--list``.

### Editing attribute values

To add new values for an attribute, ``fastsubtrees attribute`` with the option
``--add`` is used. New values of the attributes for a node are appended to the
existing ones. If the existing ones shall be replaced by the new ones, use the
option ``--replace`` instead of ``--add``.

To remove the values of an attribute for a list of given nodes,
use ``fastsubtrees attribute --delete`` specifying the nodes.
To remove an attribute completely, use ``fastsubtrees attribute --delete``
without specifying any node.

## Subtree queries

The subcommand ``fastsubtrees query`` loads a tree representation from file
and performs a subtree query to return a list of node IDs and/or attributes
of the subtree under a given node.

To run the query, two parameters are required:
- `tree`: File containing the tree.
- `subtreeroot`: ID of the root of the subtree for which the IDs
                 have to be queried

For query the values of an attribute in a subtree, the attribute names
are passed as further arguments, after the subtree root argument.
The output is tabular and a header line is output, which summarizes the content
of each column.

To hide the node IDs when attributes are printed, use the option
``--attributes-only``. In this case, only nodes for which
some attribute value exists are shown, unless the option ``--missing``
is used.
