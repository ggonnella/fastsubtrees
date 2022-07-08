# Library API

``Tree()`` is the main class of this package. An instance of the class
represents the tree information.

## Construction of the tree representation

To construct the tree representation, information about
the nodes of the tree and their parent node is required.

### Constructing from a tabular file

`Tree.construct_from_csv(filename, separator, elem_field_num, parent_field_num)`
allows the construction of a `Tree()` object from a tabular file.
Header or comment lines starting with a `#` are ignored
The `elem_field_num`
and `parent_field_num` parameters are 0-based field numbers of the fields
(columns) in the tabular file containing, respectively,
element IDs and the IDs of the element parents. Parents can be defined
before or after their children.

### Constructing from a different data source

For constructing the tree from a different data source (e.g. a database)
the `Tree.construct(generator)` class method can be used.
The
paremeter shall be a generator, which yields pairs of values, that
are the ID of each node and the corresponding parent node ID.
Parents can be defined before or after their children.

## Saving and loading from file

The tree representations can be stored to file using the instance method
`tree.to_file(filename)` and re-loaded from such a file using
the class method `Tree.from_file(filename)`.

## Modifying an existing tree representation

A tree representation (constructed from an input source or loaded from
a file) can be modified, by adding or deleting leaf nodes or entire subtrees.

### Adding nodes

For adding a leaf node, the `tree.add_node(parent, node_number)`
method can be used.
Thereby `parent` is the identifier of the node to which to add a new leaf
and `node_number` is the identifier of the leaf.

For adding a subtree, the `tree.add_subtree(generator)` method is used.
The paremeter shall be a generator, which yields pairs of values, that
are the ID of each node and the corresponding parent node ID. In the current
implementation, the first yielded pair must be the root of the new subtree
and parent nodes in the subtree must be defined before their children.

### Removing nodes

For removing a node, the `tree.delete_node(node_number)` function is used.
If the provided ID is for a leaf tree, then only that node is removed.
If it is an internal node, the node, and the entire subtree under it
are removed.

In order to implement this operation more efficiently, removed nodes remain
stored in the representation, but are flagged as removed and not output
by subtree queries. Removed node IDs shall therefore not be used anymore
in subsequent node or subtree adding operations.

## Defining an attribute

At first from `Tree.from_file(tree)` the tree is loaded and then a dictionary
is created using `module_name.attribute_values(attribute_name, database_connection_data)`. This
dictionary contains the taxonomy id of the organisms along with their
attribute values. These are finally saved into an output file with the extension `.attr`.

## Subtree queries

### List of IDs of a subtree

The list of IDs of a subtree whose root is node `n` is obtained using the
instance method: `tree.subtree_ids(n)`.

The return value is an instance of `array` containing unsigned long long
values (it can be used as a Python list for most purposes, and converted to
a list if needed).

### List of values of an attribute for a subtree
For a given node `n`, the list of its attribute values can be obtained
using the method `attribute.get_attribute_list(tree, n, attribute_file)`.

The return value is again an instance of `array` containing unsigned long long
values (it can be used as a Python list for most purposes, and converted to
a list if needed).

## Verbosity

For slow operations, such as constructing a new tree, optional progress bars
(based on the tqdm libary) can be displayed. They are enabled by setting
`fastsubtrees.PROGRESS_ENABLED` to `True` (by default the value is `False`).

The output verbosity can be controlled by setting the log level.
By default the logger is disabled.
Log messages can be activated by using `fastsubtrees.enable_logger("INFO")`.
For debugging, additional messages can be displayed by using
`fastsubtrees.enable_logger("DEBUG")`.
