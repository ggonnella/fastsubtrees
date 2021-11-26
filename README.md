This library stores tree information in a read-only data structure
which supports a fast query of the set of nodes in the subtree
under a specified node.

The tree has the following structure:
- each node is labeled by a unique positive integer ID
- the largest node label shall not be much larger than the number of IDs

If the IDs are non-numerical or contain zero or negative numbers
they must be first mapped to positive integers.

Using non-unique IDs leads to undefined behaviour.

The input is a table containing for each node the following two values
or an iterator which yields the two values:
  elemid:    ID of the current node
  parentid:  ID of the parent of the current node,
             or elemid if the current node is the root

The data structure can be stored to file and re-loaded from file.
