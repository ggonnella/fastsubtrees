# Command line interface

The command line interface of ``fastsubtrees`` consists in a set of scripts
that can be used to construct and modify a tree, add attributes to nodes,
and query a subtree.

## Tree construction

The script `bin/fastsubtrees-construct` constructs the tree representation
from a tabular file.

This script requires two parameters along with an optional parameter:
- `outfname`: Name of the file to store the tree in
- `idsmod`: A python module that defines the function ``element_parent_ids()``,
optionally taking arguments (``<idsmod_data>``) and yielding pairs
of IDs for all tree nodes ``(element_id, parent_id)``. For the root node,
the ``parent_id`` must be the same as the ``element_id``.
- `idsmod_data`: This is an optional parameter. It consists of a list
of arguments that have to be passed to the ``element_parent_ids()``
function of **idsmod**. By default they are passed as positional arguments.
To pass keyword arguments, the syntax **key=value** and the option **--keyargs**
has to be used.

## Modifying an existing tree representation

### Adding a subtree

The script `bin/fastsubtrees-add-subtree` adds a node or multiple nodes
to the already existing tree. Either a single node in the form of
a leaf node or multiple nodes as an internal node can be added in this case.

It must be noted that once a user has generated attribute files as mentioned in the following section,
it is important to pass a file containing the path of the attribute files with `--attrs` option,
so that the attribute files could also be updated with the new subtree values.

The user needs to provide two parameters as input along
with an optional parameter to run this script:
- `tree`: File containing the tree that has to be updated.
- `idsmod`: A python module that defines the function ``element_parent_ids()``,
   which optionally takes arguments (``<idsmod_data>``) and which yields pairs
   of IDs for all nodes ``(element_id, parent_id)`` of the subtree to be added.
- `idsmod_data`: This is an optional parameter. It consists of a list
   Of arguments that have to be passed to the ``element_parent_ids()``
   Function of **idsmod**. By default they are passed as positional arguments.
   To pass keyword arguments, the syntax **key=value** and the option
   **--keyargs** has to be used.

### Deleting a subtree

The script `bin/fastsubtrees-delete-subtree` will delete a node from the
exiting tree representation. If the specified node is a leaf node, then only
that node it is deleted. If it is an internal node, then the entire subtree is
also deleted, i.e. the set of all the descendants of the specified node.

When a node is deleted from a subtree, the attribute values corresponding to that node must
also be deleted. In order to do that, the user must pass a file containing the path of the attribute files with `--attrs` option,
so that the attribute files could also be updated such that the existing attribute values for the deleted
node could also be deleted.

The following parameters are used for the script:
- `nodeid`: ID of a leaf node to be deleted, or of an internal node, i.e.
   the subtree root of the subtree to be deleted
- `tree`: File containing the tree

## Defining an attribute

### Generating attribute files

The script`bin/fastsubtrees-attributes-construct` constructs a file containing
the values of a specified attribute for the nodes of the tree. Not all nodes
will necessarily have an attribute value associated with them. Attribute values
can be integers, floats or strings.

In order to generate attribute files, the user has to provide four input
parameters along with an optional input parameter to run this script:
- `outfile`: Name of the file to store the generated attributes in
- `tree`: File containing the tree that has to be updated.
- `attrmod`: A python module that defines a function ``attribute_values()``
   which may take arguments (``<attrmod_data>``) and returns pairs
   ``(element_id, attribute_value)`` for each node to which an attribute value
   exists.
- `attrmod_data`: This is an optional parameter. It consists of a list of
  arguments to be passed to the ``attribute_values()`` function of the module
  specified as **attrmod**. By default they are passed as positional arguments.
  To pass keyword arguments, the syntax **key=value** and the option
  **--keyargs** has to be used.

## Subtree queries

### Querying node identifiers

The script `bin/fastsubtrees-query` loads a tree representation from file
and performs a subtree IDs query to return a list of IDs of the subtree under a
given node.

To run this script, two parameters are required:
- `tree`: File containing the tree. It is the output of
  **fastsubtrees-construct** (eventually modified by other scripts).
- `subtreeroot`: ID of the root of the subtree for which the IDs
                 have to be queried

## Querying attribute values

The script `bin/fastsubtrees-attributes-query` outputs the values of a given
attribute in a subtree under a given node.

Three parameters are mandatory to run this script:
- `tree`: File containing the tree. It is the output of
  **fastsubtrees-construct** (eventually modified by other scripts).
- `subtreeroot`: ID of the root of the subtree for which the values
                 have to be queried
- `attributefile`: File containing the attribute data for an attribute
                   as output by **fastsubtrees-attributes-construct**.
