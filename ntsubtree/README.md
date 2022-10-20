# NtSubtree

NtSubtree is a package based on Fastsubtrees which automatically
downloads and installs the NCBI taxonomy tree during setup,
and make it easier to work with taxonomy names.

## Installation

It can be installed using ``pip install ntsubtree`` and automatically
installs ``fastsubtrees`` on which it depends.

## CLI

The CLI tool ``ntsubtree`` is provided by the package.
The first time the tool is called from the command line, the package
data (NCBI taxonomy tree) is downloaded from NCBI, the fastsubtrees
tree data is constructed, as well as a table of taxonomy names.

If anything goes wrong during the automatic download and construction,
use ``ntsubtree update --cleanup`` to repeat the process.

After that, it is possible to update the data to the newest NCBI taxonomy
data, by running ``ntsubtree update``. This only re-downloads the data
and reconstruct the tree data, if newer data is available.
Furthermore, it conserves any attribute data which have been added to
the tree.

To add new attributes to the tree, ``ntsubtree attribute`` can be used.
The usage is identical to ``fastsubtrees attribute``, except that no
tree filename is passed.

To query the tree, the ``ntsubtree query`` command is used.
The usage is identical to ``fastsubtrees query``, except that no
tree filename is passed.

Taxonomic names are displayed automatically in the query results,
unless the option ``--no-taxname`` is used.
Furthermore, it is possible to query the tree by using a taxon name
instead of a taxon ID as a subtree root, using the option ``-n``.

### Example usage

```
ntsubtree query 562               # taxonomic names displayed alongside the IDs
ntsubtree query -n "Escherichia"  # Query by taxonomic name

ntsubtree attribute myattr values.tsv
ntsubtree query 562 myattr

ntsubtree update
```

## API

The first time that ntsubtree is imported, the package
data (NCBI taxonomy tree) is downloaded from NCBI, the fastsubtrees
tree data is constructed, as well as a table of taxonomy names.
This can be triggered by ``python -m ntsubtree``.

The ``ntsubtree.update()`` function can be used to check if new
taxonomy data is avalaible at NCBI and, if so, download it and update
the tree, without loosing existing attribute data.

Working with the tree is done using the _fastsubtrees_ package API.
The ``Tree`` object is obtained using ``get_tree()``.

Besides the IDs, the ``taxname`` attribute is automatically available.
Furthermore, the ``ntsubtree.search_name(query)`` function can be used
to retrieve a taxon ID to pass to the _fastsubtrees_ tree query methods.

### Example usage

```python
import ntsubtree

ids_in_subtree = ntsubtree.get_tree().subtree_ids(562)

taxid = ntsubtree.search_name("Escherichia")
subtree_info = tree.subtree_info(taxid, ["taxname"])

tree.create_attribute_from_tabular("myattr", "attr-tsv")
results = tree.subtree_info(562, ["taxname", "myattr"])

ntsubtree.update() # check for updates
```
