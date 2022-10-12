#!/bin/bash

#
# Benchmark the construction and query of the attribute files
# associated with a tree.
#

if [ $# -ne 1 ]; then
    echo "Usage: $0 <tree>"
    echo "where <tree> is the name of a fastsubtrees tree file constructed"
    echo "with fastsubtrees-construct from a NCBI taxonomy dump"
    exit 1
fi
TREE=$1

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
FST_DIR=$SCRIPT_DIR/..
FST_DATA_DIR=$FST_DIR/data
FST_MOD_DIR=$FST_DIR/fastsubtrees/ids_modules

source $SCRIPT_DIR/benchmarks_params.sh
OUTFILE=${OUTFILE_PFX}_attr.tsv
rm -f $OUTFILE
mkdir -p $OUTDIR

declare -A attr_col
attr_col[genome_size]=2
attr_col[GC_content]=3

declare -A attr_dt
attr_dt[genome_size]=int
attr_dt[GC_content]=float

for attr in genome_size GC_content; do
  for ((i=0; i<$NREPEATS; i++)); do
    STEP="construct-$attr"
    /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
      fastsubtrees attribute $TREE $attr \
        $FST_MOD_DIR/attr_from_tabular_file.py --datatype ${attr_dt[$attr]} \
            filename=$FST_DATA_DIR/accession_taxid_attribute.tsv.gz \
            id_col=1 attr_col=${attr_col[$attr]}
  done

  for ((i=0; i<$NREPEATS; i++)); do
    STEP="query-$attr"
    for ROOT in $NODES; do
      echo "Step $STEP from node $ROOT, iteration $i..."
      /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
        fastsubtrees query -N -a --stats $TREE $ROOT $attr > \
        $OUTDIR/attr_values.$attr.$ROOT
    done
  done
done
