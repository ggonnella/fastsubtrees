# Library API

``Tree()`` is the main class of this package.

## Construction of the tree representation

To construct the tree representation, information about
the nodes of the tree and their parent node is required.

`Tree.construct_from_csv(filename, separator, elem_field_num, parent_field_num)`
allows to construct the `Tree()` object from a tabular file, with no header,
fields separated by `separator` and the 0-based numbers of the nodes
their parents in the fields specified by `elem_field_num` and
`parent_field_num`.

Alternatively, an iterator or generator can be passed to
`Tree.construct(generator)` which should yield pairs of values
(ID of each node and the corresponding parent node ID).

## Saving and loading from file

The tree representations can be stored to file using the instance method
`tree.to_file(filename)` and re-loaded from such a file using
the class method `Tree.from_file(filename)`.

## List of IDs of a subtree

The list of IDs of a subtree whose root is node `n` is obtained using the
instance method: `tree.subtree_ids(n)`.

The return value is an instance of `array` containing unsigned long long
values (it can be used as a Python list for most purposes, and converted to
a list if needed).

## Verbosity

The progress bars are enabled by setting `fastsubtrees.PROGRESS_ENABLED`
to `True` (by default the value is `False`).
The log messages can be activated by using `fastsubtrees.enable_logger("INFO")`
and the debug messages by `fastsubtrees.enable_logger("DEBUG")`
(by default the logger is disabled).
