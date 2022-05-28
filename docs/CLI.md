# Command line interface

## Constructing a Tree

The script `bin/fastsubtrees-construct` constructs the tree representation
from a tabular file. 

This script requires two parameters:
- `pymodule`: A python module which defines the function get_element_parent_id 
for yielding the element and parent ids
- `outputfilename`: Name of the file to store the tree in

## Querying a Tree
The script `bin/fastsubtrees-query` loads a tree representation from file
and performs a subtree IDs query.

To run this script, two parameters are required:
- `nodefile`: File containing the tree. It is the output of 
**fastsubtrees-construct**
- `subtreeroot`: ID of the node for which the tree has to be queried

## Adding a subtree
The script `bin/fastsubtrees-add-subtree` adds a node or multiple nodes
to the already existing tree.

The user needs to provide three parameters as input so as to run this script:
- `pymodule`: A python module which defines the function get_element_parent_id 
for yielding the element and parent ids
- `inputfile`: TSV file containing parents followed by children
- `nodefile`: File containing the tree that has to be updated.

## Deleting a subtree 
The script `bin/fastsubtrees-delete-subtree` will delete a node from the
exiting tree representation.

To delete a node from the tree, one must pass the following two attributes while running this script:
- `nodeid`: ID of the node that has to be deleted
- `nodefile`: File containing the tree

## Generating attribute files
The script`bin/fastsubtrees-attributes-construct` constructs an attribute file
for the existing attributes in the database.

In order to generate attribute files, the user has to provide five inputs to run this script:
- `nodefile`: File containing the tree that has to be updated.
- `subtreeroot`: ID of the node for which the attribute has to be generated.
- `attribute`: Name of the attribute 
- `pymodule`: A python module which defines the function get_attribute_list for getting the attribute values
- `outputfile`: Name of the file to store the generated attributes in

## Querying attribute files
The script `bin/fastsubtrees-attributes-query` will return the attribute values
for a passed attribute name.   

Three parameters are essential to run this script:
- `nodefile`: File containing the tree. It is the output of 
**fastsubtrees-construct**
- `subtreeroot`: ID of the node for which the tree has to be queried
- `attributefile`: 
