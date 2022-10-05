The benchmark scripts in this directory allow to reproduce the benchmarks
presented in the paper.

The easiest way to run the scripts is by installing the
Docker image of fastsubtrees and running ``make benchmarks`` (all benchmarks
except tree file construction) or ``make benchmarks_all`` (all benchmarks).

# Scripts

|------------------------|-----------------------------------------------------|
|                        |
| ``benchmarks_sql.sh``  | loads NCBI taxonomy data into the database and runs
|                        | a set of subtree queries using recursive SQL, as
|                        | implemented in the ntmirror-extract-subtree script;
|                        | it requires a MariaDB server running
|                        |
|------------------------------|-----------------------------------------------|
|                              |
| ``benchmarks_construct.sh``  | constructs a fastsubtrees tree using NCBI
|                              | taxonomy using the fastsubtrees-construct
|                              | script
|                              |
|------------------------------|-----------------------------------------------|
|                        |
| ``benchmarks_fst.sh``  | runs a set of subtree queries, using the
|                        | fastsubtrees library, as implemented in the
|                        | fastsubtrees-query script
|                        |
|------------------------|-----------------------------------------------------|
|                        |
| ``benchmarks_attr.sh`` | creates fastsubtrees attribute files for the data
|                        | stored in the "data" subdirectory of the
|                        | fastsubtrees repository and runs a set of attribute
|                        | queries for subtrees, using the fastsubtrees
|                        | library, as implemented in the
|                        | fastsubtrees-attributes-query script
|                        |
|------------------------|-----------------------------------------------------|
