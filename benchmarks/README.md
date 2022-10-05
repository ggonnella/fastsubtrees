The benchmark scripts in this directory allow to reproduce the benchmarks
presented in the paper. The easiest way to run the scripts is by installing the
Docker image of fastsubtrees and running "make benchmarks".

Scripts:

|------------------------|-----------------------------------------------------|
| ``benchmarks_sql.sh``  | loads NCBI taxonomy data into the database and runs
|                        | a set of subtree queries using recursive SQL, as
|                        | implemented in the ntmirror-extract-subtree script;
|                        | it requires a MariaDB server running
|                        |
|------------------------|-----------------------------------------------------|
|                        |
| ``benchmarks_fst.sh``  | constructs a fastsubtrees tree using NCBI taxonomy
|                        | data and runs a set of subtree queries, using the
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
|------------------------|-----------------------------------------------------|
