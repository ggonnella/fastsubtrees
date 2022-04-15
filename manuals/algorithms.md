This document briefly explains the algorithms and data structure used in the
implementation of the fastsubtrees library.

# Tree representation

- ``coords(nodeID)``:
    - ordinal number of each node in deep-first traversal order
      i.e. the position in the treedata(), see below
    - memory: ``O(max(nodeID))``; ``max(nodeID) * 8 bytes``
- ``subtree_sizes(nodeID)``:
    - length of the subtree under each node
    - memory: ``O(max(nodeID))``; ``max(nodeID) * 8 bytes``
- ``treedata(coord)``:
    - node IDs in deep-first traversal order
    - memory: ``O(n_nodes)``; ``(n_nodes+1) * 8 bytes``
- ``parents(nodeID)``:
    - ID of the parent of each node
    - memory: ``O(max(nodeID))``; ``max(nodeID) * 8 bytes``
    - not necessary for the subtree queries, but useful for tree editing

# Operations

- Tree construction:
- List the IDs of the subtree under a node:
   - ``treedata[coord(nodeID)..coord(nodeID)+subtree_sizes(nodeID)]``
   - running time:
       - ``coords(nodeID)`` and ``subtree_sizes(nodeID)``: O(1)
       - output: ``O(size(subtree))``
- Add a leaf node to an existing tree:
  - XXX
