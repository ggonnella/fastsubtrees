# Command line interface

The command line interface of the library consists in a script ``fastsubtrees``
that can be used to construct and modify a tree, add attributes to nodes, and
query subtree IDs and attribute values.

The list of subcommands is displayed using ``fastsubtrees --help``.
Using ``--help`` after a subcommand (e.g. ``fastsubtrees construct --help``
displays the syntax and details of the subcommand.

The following subcommands are available:
```
  construct         Construct the tree data structure and save it to file
  update            Update an existing tree data structure
  attribute         Create, update or delete node attributes
  query             List node IDs and/or attributes in the subtree under a node
```

## Tree construction

The subcommand ``fastsubtrees construct`` constructs the tree representation
from a tabular file.

The script has different modes of use, depending on the input format,
as described in the following subsections.

Common to all modes of use is the first parameter, which is the output file
name, containing the tree data, used for the subsequent queries.

### NCBI taxonomy tree construction

For constructing the NCBI taxonomy tree, the directory containing ``nodes.dmp``
is specified, after using the ``--ntdump`` option.
Example:
```
fastsubtrees-construct my.tree --ntdump ntdumpsdir
```

### Using a tabular file

If the input data is contained in a TAB-separated input file, with two
columns, the elements IDs in the first column, and the parent IDs in the second
column, then the ``--tab`` option can be used:

Example:
```
fastsubtrees-construct my.tree --tab elems_and_parents.tsv
```

If the separator is not TAB, or the column order is different, use the generic
tree construction mode described below,
passing the ``ids_from_tabular_file.py`` module.

### Generic tree construction mode

In the generic mode, the next parameter of ``fastsubtrees construct``
is the name of a Python module. This must define a function called
``element_parent_ids()``, which yields pairs of IDs ``(element_id, parent_id)``.
Examples of this functions, obtaining the ID data from a database table or
from a tabular file are given in the modules in the
``fastsubtrees.ids_modules`` namespace modules.

The ``element_parent_ids()`` function usually needs parameters. These
can be passed either as positional or as keyword parameters. To pass them
as positional parameters, they are just used as further arguments,
after the module name.
To define them as keyword parameters, the
use the form ``key=value``.

Examples:
```
fastsubtrees construct my.tree my_module.py a b c
fastsubtrees construct my.tree my_module.py k1=v1 k2=v=2 x
```

In the first example, the function in ``my_module.py`` is called as
``element_parent_ids("a", "b", "c")``, in the second as
``element_parent_ids("x", k1="v1", k2="v=2")``.

Some modules implementing the described interface are provided
under ``fastsubtrees/ids_modules``. In particular, ``ids_from_database.py``
provides an interface for reading the tree data from a database table,
and ``ids_from_tabular_file.py`` from a tabular input file.

## Modifying an existing tree representation

### Updating a tree

It is possible to modify a tree, by updating the representation, given
a source of node and parent IDs, similar to the one for the tree creation.
For this the command ``fastsubtrees update`` is used.
Any node not yielded in the source will be deleted, and new nodes
will be added.

### Adding nodes

It is also possible to add nodes using a source which only specifies
the new nodes to add, but not the existing ones. This is done by using
``fastsubtrees update`` with the option ``--add``.

### Delete nodes

To delete leaf nodes or an internal nodes and entire subtree under them,
the ``fastsubtrees update`` command is used with the option ``--delete``
by listing the leaf nodes to delete and/or the roots of subtrees
to delete.

### Attributes when editing a tree

If attribute have been defined, as described in the following section,
the attribute files are automatically detected and modified too,
when adding or deleting nodes.

If nodes have been added, new attribute values for those nodes
can be added using ``fastsubtrees attribute --add``, as explained below.

## Tree attributes

The tree can contain further information, except the IDs, in the form of
attributes. Attribute values can be integers, floats or strings.
Not all nodes will necessarily have an attribute value associated
with them. Some nodes can contain multiple values for an attribute.

### Adding an attribute

The command `fastsubtrees attribute` constructs a file containing
the values of a specified attribute for the nodes of the tree.

In order to generate attribute files, the user has to
provide the following parameters:
- `tree`: File containing the tree that has to be updated.
- `attribute`: Name of the attribute; attribute names are not allowed
               to contain spaces or commas
- `attrmod`: Path to a python module that defines a function
  ``attribute_values()`` which may take arguments (``<attrmod_data>``) and
  returns pairs ``(element_id, attribute_value)`` for each node to which an
  attribute value exists.
- `attrmod_data`: This is an optional parameter. It consists of a list of
  arguments to be passed to the ``attribute_values()`` function of the module
  specified as **attrmod**.
  To pass keyword arguments, the syntax **key=value** is used.

A module using the described ``attrmod`` interface for adding attributes
from tabular files is provided under ``fastsubtrees/ids_modules`` and
can be selected by the shorthand option ``--tab``:
```
fastsubtrees attribute my.tree myattribute --tab tabularfile.tsv
```
By default, the IDs are supposed to be in column 0, the attribute values in
column 1 and the columns to be tab-separated; different values can be
provided as keyword arguments, e.g.:
```
fastsubtrees attribute my.tree myattribute --tab tabularfile.tsv \
   id_col=2 attr_col=10 separator=';'
```

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
some attribute value exists are shown, unless the option ``--show-none``
is used.
