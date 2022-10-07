# Command line interface

The command line interface of ``fastsubtrees`` consists in a set of scripts
that can be used to construct and modify a tree, add attributes to nodes,
and query a subtree.

## Tree construction

The script ``fastsubtrees-construct`` constructs the tree representation
from a tabular file.

The script has two modes of use, one generic and one specific for the
NCBI taxonomy tree dumps (for which the library was originally designed).
Common to both modes is the first parameter, which is the output file name,
containing the tree data, used for the subsequent queries.

### NCBI taxonomy construction mode

For constructing the NCBI taxonomy tree, the directory containing ``nodes.dmp``
is specified, after using the ``--ntdump`` option.
Example:
```
fastsubtrees-construct my.tree --ntdump ntdumpsdir
```

### Generic tree construction mode

In the generic mode, the next parameter of the ``fastsubtrees-construct``
script is the name of a Python module. This must define a function called
``element_parent_ids()``, which yields pairs of IDs ``(element_id, parent_id)``.
Examples of this functions, obtaining the ID data from a database table or
from a tabular file are given in the modules in the
``fastsubtrees.ids_modules`` namespace modules.

The ``element_parent_ids()`` function usually needs parameters. These
can be passed either as positional or as keyword parameters. To pass them
as positional parameters, they are just used as further arguments of the
script, after the module name. To define them as keyword parameters, the
``--keyargs`` option is used, and all further arguments in the form
``key=value`` (i.e. where at least one = is present), are parsed and
passed as keywords parameters.

Examples:
```
fastsubtrees-construct my.tree my_module.py a b c
fastsubtrees-construct my.tree my_module.py --keyargs k1=v1 k2=v=2 x
```

In the first example, the function in ``my_module.py`` is called as
``element_parent_ids("a", "b", "c")``, in the second as
``element_parent_ids("x", k1="v1", k2="v=2")``.

Some modules implementing the described interface are provided
under ``fastsubtrees/ids_modules``. In particular, ``ids_from_database.py``
provides an interface for reading the tree data from a database table,
and ``ids_from_tabular_file.py`` from a tabular input file.

## Modifying an existing tree representation

### Adding a subtree

The script `fastsubtrees-add-subtree` adds one or multiple nodes to an already
existing tree. The interface is identical to the generic tree construction
interface of ``fastsubtrees-construct`` (see above), i.e. the following
arguments are passed to the script:
- `tree`: File containing the tree that has to be updated.
- `idsmod`: A Python module that defines the function ``element_parent_ids()``,
   which optionally takes arguments (``<idsmod_data>``) and which yields pairs
   of IDs for all nodes ``(element_id, parent_id)`` of the subtree to be added.
- `idsmod_data` (optional): list of arguments to be passed to
  ``element_parent_ids()``. By default they are passed as positional arguments.
  To pass keyword arguments, using the syntax ``key=value``, use the option
  ``--keyargs``.

### Deleting a subtree

The script `fastsubtrees-delete-subtree` is used to delete one or multiple
nodes from an exiting tree representation. If the specified node is a leaf
node, then only that node it is deleted. If it is an internal node, then the
entire subtree is also deleted, i.e. the set of all the descendants of the
specified node.

The following parameters are used for the script:
- `nodeid`: ID of a leaf node to be deleted, or of an internal node, i.e.
   the subtree root of the subtree to be deleted
- `tree`: File containing the tree

## Tree attributes

The tree can contain further information, except the IDs, in the form of
attributes. Attribute values can be integers, floats or strings.
Not all nodes will necessarily have an attribute value associated
with them. Some nodes can contain multiple values for an attribute.

### Adding an attribute

The script `fastsubtrees-attr-construct` constructs a file containing
the values of a specified attribute for the nodes of the tree.

In order to generate attribute files, the user has to provide four input
parameters along with an optional input parameter to run this script:
- `tree`: File containing the tree that has to be updated.
- `attribute`: Name of the attribute
- `attrmod`: A python module that defines a function ``attribute_values()``
   which may take arguments (``<attrmod_data>``) and returns pairs
   ``(element_id, attribute_value)`` for each node to which an attribute value
   exists.
- `attrmod_data`: This is an optional parameter. It consists of a list of
  arguments to be passed to the ``attribute_values()`` function of the module
  specified as **attrmod**. By default they are passed as positional arguments.
  To pass keyword arguments, the syntax **key=value** and the option
  **--keyargs** has to be used.

A module using the described ``attrmod`` interface for adding attributes
from tabular files is provided under ``fastsubtrees/ids_modules`` and
can be used as follows:
```
fastsubtrees-attr-construct my.tree myattribute \
   fastsubtrees/ids_modules/attr_from_tabular_file.py tabularfile.tsv
```
By default, the IDs are supposed to be in column 0, the attribute values in
column 1 and the columns to be tab-separated; different values can be
provided as keyword arguments, e.g.:
```
fastsubtrees-attr-construct my.tree myattribute \
   fastsubtrees/ids_modules/attr_from_tabular_file.py tabularfile.tsv
   --keyargs id_col=2 attr_col=10 separator=';'
```

### Attributes when editing a tree

If attribute have been defined, as described in the following section,
the attribute files are automatically detected and modified too,
when adding or deleting a subtree.

When adding a subtree, the attribute will initially have an empty value (None)
for each of the additional nodes. In order to add attribute values for the new
nodes, the script ``fastsubtrees-attr-add`` is employed. This must be called
for each of the attributes for which values shall be added, and uses the same
interface as the ``fastsubtrees-attr-construct`` script (see above).

### Editing attribute values

To add new values for an attribute, use the ``fastsubtrees-attr-add`` script.
The script uses the same
interface as the ``fastsubtrees-attr-construct`` script (see above).

By default, the new values of the attributes for a node are added to the
existing ones. If the existing ones shall be replaced by the new ones,
use the option ``--replace``.

To remove the values of an attribute for a list of given nodes,
use the ``fastsubtrees-attr-delete`` script.

### Removing an attribute

To remove an attribute, use the ``fastsubtrees-attr-delete`` script
with the option ``--all``.

## Subtree queries

### Querying node identifiers

The script `fastsubtrees-query` loads a tree representation from file
and performs a subtree IDs query to return a list of IDs of the subtree under a
given node.

To run this script, two parameters are required:
- `tree`: File containing the tree. It is the output of
  **fastsubtrees-construct** (eventually modified by other scripts).
- `subtreeroot`: ID of the root of the subtree for which the IDs
                 have to be queried

## Querying attribute values

The script `fastsubtrees-attr-query` outputs the values of a given
attribute in a subtree under a given node.

Three parameters are mandatory to run this script:
- `tree`: File containing the tree. It is the output of
  **fastsubtrees-construct** (eventually modified by other scripts).
- `attribute`: Name of the attribute to query
- `subtreeroot`: ID of the root of the subtree for which the values
                 have to be queried
