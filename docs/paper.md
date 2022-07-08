# Summary

Tree data structures are commonly used for representing hierarchical data. A
prominent example in bioinformatics is the taxonomic tree, representing the
biological classification of organisms, currently including millions of nodes.

An interesting operation for such trees is the extraction of the IDs and other
associated values for each node in a given subtree.
Here we present _fastsubtrees_, a Python package which provides a simple and
efficient way to perform this operation, by storing the tree data in a suitable
representation. The package provides a command line interface and a
application programming interface.

It was mainly developed for handling the NCBI taxonomy tree, although its
interface is generic, and can be applied to other trees as well. For working
with the NCBI taxonomy tree, a companion package is provided, named _ntmirror_,
which simplifies the task of keeping a local updated version of the NCBI
taxonomy data.

Finally, a web application, Genome Attribute Viewer, is provided,
which examplifies the use of the
software for extracting and comparing the distribution of values of attributes
(e.g. genome size and GC content) from any subtree of the NCBI taxonomy tree.

# Statement of need

Tree data structures are commonly used in different fields of computer science
to represent hierarchical information (Black, 1999). A prominent use case is in
philogenetics, where trees are used to represent the common ancestry of
organisms or macromolecules. Taxonomy, the hierarchical biological
classification of organisms, is based on their phylogenetic relationships, and
is thus representable as a tree.

The NCBI taxonomy (Schoch et al., 2020) database is a curated database of
all organisms for which sequences were deposited in public sequence databases.
The data is represented as a tree, which, as of July 2022, contains about
2.4 million nodes (https://www.ncbi.nlm.nih.gov/Taxonomy/taxonomyhome.html/index.cgi?chapter=statistics).
Each node, representing a taxon, is labeled by a positive integer and is associated
with one or multiple names for the organism (e.g.\ a scientific name
and multiple common names).

Given a taxonomic tree,
quantitative or qualitative data can be associated to taxa (e.g. sequence or
annotation statistics). Variables associated with tree nodes are
hereafter called attributes. Interesting applications of the taxonomic tree
are the investigation of the range of values of an attribute in a given subtree,
and the comparison of the value distributions in different subtrees.
This allows e.g. to identify uncommon values in some members of a taxon,
which in turn can be a primer for new biological hypotheses.
In order to enable such investigations of subtrees of
the taxonomic tree, the IDs of the subtree nodes, and the attributes
associated with those nodes, must be efficiently extracted.
However, no simple and efficient package offering this operation in Python
was available until now.

# The fastsubtrees Python package

Here we present the  _fastsubtrees_ Python package, which was developed
for storing tree information using a compact representation,
suitable for fast extraction of any subtree.
This package can be applied to any tree in which the nodes
are labeled by positive integers. I.e., although it was designed and
tested mainly for the NCBI taxonomy tree, it is not limited to it.

It can be installed using ``pip install fastsubtrees``. Its
functionality can be used through either executable scripts or an API, which
can be employed from other Python programs. Manuals are provided for both
kind of interfaces. A complete test suite based on _pytest_ is provided.

The first step to use _fastsubtrees_ is to generate the file containing the
tree representation. For this step, the user must provide a generator function
yielding pairs of node numbers (parent and child node), describing the tree, in
any order. Each node must be represented by a unique positive ID. The IDs space
must be compact, i.e. the numbers are not necessarily all consecutive, bu the
largest node ID (_idmax_) should not be much larger than the total number of
nodes, because the memory consumption is in O(idmax). If this condition is not
met, the existing node labels must be mapped to a compact set of positive
integers. The generator function mechanism allows using the library for
constructing trees from any source (e.g. from tabular files, or from database
tables). Examples of generator functions are provided.

After the tree representation has been created or loaded from file, it can be
used for finding any node in constant time and extracting the subtree under
that node in time proportional to the output subtree size. To achieve this, in
the tree representation the node numbers and the subtree sizes under each node
are stored in depth-first traversal order. Furthermore, an index table is
provided which gives the ordinal position of each node in the depth-first
representation.

The tree representation is dynamic, i.e. it is possible to add and remove
subtrees. The subtree adding is achieved by finding the insertion position
in the depth-first representation and adding there the subtree, and
correcting accordingly the node positions in the index table. The subtree
removing is achieved by marking the corresponding nodes as deleted.

Along with numerical node identifiers, additional information can be stored for
each node, by defining any number of optional node attributes. These can be any
numerical or string information (including e.g. the original node labels, if
they were not a compact set of positive integers). Any desired numbers of
attributes can be used. For each attribute defined in a tree, a file is
created, where the attribute values are stored. The attributes are stored in
the same depth-first traversal order as the nodes in the tree representation,
so that the list of attribute values for an entire subtree can be queried
efficiently.

# The ntmirror package

In order to apply the _fastsubtrees_ package to the NCBI taxonomy tree, the
NCBI taxonomy dump files must be obtained(
from the NCBI FTP website (https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/).
We developed a
package, named _ntmirror_, which automatically downloads (if needed) and keeps
up-to-date a local copy of the NCBI taxonomy dump files and can be combined
with _fastsubtrees_ for working on the NCBI taxonomy tree in Python.

Additionally the package offers the option to construct a relational database
for storing the NCBI tree and loads the dump data into it. This is not
necessary, if _fastsubtrees_ is used.

The package can be used by employing the provided command line scripts or from
inside Python code, using the provided API. Both interfaces are described
in the package user manual.
A complete test suite based on the `pytest` package is included. Testing
of the database loading feature requires the user to setup the database
management system and provide the connection data in a configuration file,
as described in the manual.

# Materials and Methods

## Benchmark system

Benchmarks were performed on a Linux server with Intel Xeon E7-4850 2.0 Ghz
CPU and 1 Tb RAM. Running times were measured as an average of 3 runs using
GNU time version 1.9.
(Free Software Foundation. GNU Time; 2018. Available from: https://www.gnu.org/software/time/.)
For the tests Python version 3.10.2 was used.
For comparative tests with SQL queries, MariaDB version 10.6.8 was used
a relational database management system.

## NCBI taxonomy tree

The NCBI taxonomy tree used for the tests was downloaded on May 28, 2022
from the NCBI FTP website (https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/) using
the _ntmirror_ package described above.
The tree contained 2949637 nodes as of May 28, 2022. The generation of the tree
representation of the NCBI taxonomy tree from the dump files
using the _fastsubtrees-construct_ script required
23 minutes and 35 seconds (average of 3 runs).

## Example attribute files

For providing an example of attributes to store alongside the tree IDs, we
computed the GC content and genome size of bacterial all assemblies downloaded
from the NCBI Refseq database (O'Leary et al, 2016) using Python scripts and
provided this data in a table in the source code repository
(``examples/accession_taxid_attribute.tsv.gz``). The table contains
values for 27967 genomes.

## Example subtrees

To select subtrees of different sizes for the benchmarks, we started from the
taxonomy ID of _Escherichia coli_ K12 MG1655 (511145) and climbed up the
taxonomy tree, including all parent nodes in the benchmarks, up to the Bacteria
node (TaxID 2), i.e. nodes 83333 (_Escherichia coli_ K12),
562 (_Escherichia coli_), 561 (_Escherichia_ genus), 543 (Enterobacteriaceae),
91347 (Enterobacterales), 1236 (Gammaproteobacteria) and 1224 (Proteobacteria).

# Results

## Comparison to hierarchical SQL queries

An alternative to the use of _fastsubtrees_ is to store the tree data in a SQL
database and extract subtrees using hierarchical SQL queries.
In order to compare the use of _fastsubtrees_ with such a solution,
we implemented a script, named _ncbi_taxonomy_db_extract_subtree.py_
running such queries on the NCBI taxonomy database reconstructed by
_ntmirror_ from the NCBI dump files. The script is based on SQLAlchemy
and was tested using MariaDB version as relational database management system.

Table 1 compares the running time and memory usage for _fastsubtrees-query_
script of the _fastsubtrees_ package with hierarchical SQL queries, as
implemented in the _ncbi_taxonomy_db_extract_subtree.py_ script of the
_ntmirror_ package.

## Extraction of attribute values for subtrees

We evaluated the time needed for the extraction of attributes in a given subtree,
by applying the _fastsubtrees-attributes-query_ script for
subtrees of different sizes, for extracting the GC content and genome size
data (provided in the _fastsubtrees_ source code repository
as a table in the _examples_ subdirectory).

The generation of the attribute files using the
_fastsubtrees-attributes-construct_ script required 29 seconds
(average of 3 runs).

Table 2 reports the running time and memory usage for the extraction
of the attribute values for different subtrees.

## Genome Attribute Viewer

To provide an example of usage of _fastsubtrees_ we implemented an interactive
web application based on the _dash_ library (version 2.0.0,
https://dash.plotly.com/).  The application allows displaying diagrams of the
value distribution of GC content and genome size values in any subtree of the
NCBI taxonomy tree (we actually included in the example only values for
bacterial genomes, see above).  Values for multiple subtrees can be compared.

# Author Contributions

Aman Modi: software development, test suite, example application,
documentation and benchmarks.

Giorgio Gonnella: funding acquisition, conceptualization,
software development, project supervision and manuscript redaction.

# Funding

Giorgio Gonnella has been supported by the DFG Grant GO 3192/1-1 ‘‘Automated
characterization of microbial genomes and metagenomes by collection and
verification of association rules’’. The funders had no role in study design,
data collection and analysis, decision to publish, or preparation of the
manuscript.

# References

Paul E. Black, CRC Press LLC,
 1999, "tree", in Dictionary of Algorithms and Data Structures [online],
  Paul E. Black, ed. 15 December 2017.
  Available from: https://www.nist.gov/dads/HTML/tree.html

Schoch CL, et al. NCBI Taxonomy: a comprehensive update on curation,
resources and tools. Database (Oxford). 2020: baaa062. [PubMed]

O'Leary NA, Wright MW, Brister JR, Ciufo S, Haddad D, McVeigh R, Rajput B, Robbertse B, Smith-White B, Ako-Adjei D, Astashyn A, Badretdin A, Bao Y, Blinkova O, Brover V, Chetvernin V, Choi J, Cox E, Ermolaeva O, Farrell CM, Goldfarb T, Gupta T, Haft D, Hatcher E, Hlavina W, Joardar VS, Kodali VK, Li W, Maglott D, Masterson P, McGarvey KM, Murphy MR, O'Neill K, Pujar S, Rangwala SH, Rausch D, Riddick LD, Schoch C, Shkeda A, Storz SS, Sun H, Thibaud-Nissen F, Tolstoy I, Tully RE, Vatsan AR, Wallin C, Webb D, Wu W, Landrum MJ, Kimchi A, Tatusova T, DiCuccio M, Kitts P, Murphy TD, Pruitt KD. Reference sequence (RefSeq) database at NCBI: current status, taxonomic expansion, and functional annotation. Nucleic Acids Res. 2016 Jan 4;44(D1):D733-45 PubMed PubMedCentral

