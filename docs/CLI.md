# Command line interface

## Tree Construction
### Constructing a Tree
The script `bin/fastsubtrees-construct` constructs the tree representation
from a tabular file. 

This script requires two parameters along with an optional parameter:
- `outfname`: Name of the file to store the tree in
- `idsmod`: A python module that defines the function element_parent_ids() and
which will take arguments (<idsmod_data>) and yield pairs
of IDs for all tree nodes (element_id, parent_id). The parent_id
should be the same as the element_id for the root node. 
- `idsmod_data`: This is an optional parameter. It will take
the set of arguments that have to be passed to element_parent_ids()
function of **idsmod**. To pass the arguments,
the syntax **key=value** and the option **--keyargs**
has to be used.

## Modifying an existing Tree Representation
### Adding a subtree
The script `bin/fastsubtrees-add-subtree` adds a node or multiple nodes
to the already existing tree. Either a single node in the form of
a leaf node or multiple nodes as an internal node 
can be added in this case.

The user needs to provide two parameters as input along 
with an optional parameter to run this script:
- `tree`: File containing the tree that has to be updated.
- `idsmod`: A python module that defines the function element_parent_ids() and
which will take arguments (<idsmod_data>) and yield pairs
of IDs for all tree nodes (element_id, parent_id). 
- `idsmod_data`: This is an optional parameter. It will take
the set of arguments that have to be passed to element_parent_ids()
function of **idsmod**. To pass the arguments,
the syntax **key=value** and the option **--keyargs**
has to be used.


### Deleting a subtree 
The script `bin/fastsubtrees-delete-subtree` will delete a node from the
exiting tree representation. One can delete the leaf node
or if in case an internal node is deleted then all its 
children are also deleted. 

To delete a node from the tree, one must pass the following two parameters while running this script:
- `nodeid`: ID of the node that has to be deleted
- `tree`: File containing the tree

## Defining an attribute
### Generating attribute files
The script`bin/fastsubtrees-attributes-construct` constructs an attribute file
for the existing attributes in the database. 

It has to be noted that not all nodes will have an attribute value associated with them. 

The attribute value can either be an int, float or string.

In order to generate attribute files, the user has to provide four inputs along with 
an optional input to run this script:
- `outfile`: Name of the file to store the generated attributes in
- `tree`: File containing the tree that has to be updated.
- `attribute`: Name of the attribute
- `attrmod`: A python module that defines a function attribute_values()
which may take arguments (<attrmod_data>) and returns pairs
(element_id, attribute_value) for each node to which an attribute value exists.
- `attrmod_data`: This is an optional parameter. This will take
the set of arguments to be passed to the attribute_values()
function of the module specified as **attrmod**. To pass keyword
arguments, use the syntax **"key=value"** and the option **--keyargs**.


## Subtree Queries
### Querying a Tree
The script `bin/fastsubtrees-query` loads a tree representation from file
and performs a subtree IDs query to return a list of 
ids of a subtree under a given node.

To run this script, two parameters are required:
- `tree`: File containing the tree. It is the output of 
**fastsubtrees-construct**
- `subtreeroot`: ID of the node for which the tree has to be queried

## Querying attribute files
The script `bin/fastsubtrees-attributes-query` will return the attribute values
for a passed attribute name.   

Three parameters are essential to run this script:
- `tree`: File containing the tree. It is the output of 
**fastsubtrees-construct**
- `subtreeroot`: ID of the node for which the tree has to be queried
- `attributefile`: This is a file containing the attribute data for an attribute
as output by fastsubtrees-attributes-construct.
