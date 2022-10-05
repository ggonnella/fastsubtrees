#!/bin/bash
#
# Benchmark the construction and query of the attribute files
# associated with a tree.
#

NREPEATS=3
OUTFILE=benchmarks_fst.tsv

if [ $# -ne 1 ]; then
    echo "Usage: $0 <ntdumpdir>"
    echo "where <ntdumpdir> is the directory containing the NCBI taxonomy"
    echo "dump files to be used for the tree construction"
    exit 1
fi
NTDUMPDIR=$1

rm -f $OUTFILE
mkdir -p results

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
FST_DIR=$SCRIPT_DIR/..
FST_IDS_MODULES_DIR=$FST_DIR/fastsubtrees/ids_modules

for ((i=0; i<$NREPEATS; i++)); do
  STEP="construct"
  ROOT=""
  echo "Step $STEP, iteration $i..."
  rm -f nt.tree
  /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
    fastsubtrees-construct nt.tree \
      $FST_IDS_MODULES_DIR/ids_from_tabular_file.py \
        --keyargs separator='	|	' inputfile=$NTDUMPDIR/nodes.dmp
done
for ((i=0; i<$NREPEATS; i++)); do
  STEP="extract"
  for ROOT in 511145 83333 562 561 543 91347 1236 1224 2; do
    echo "Step $STEP from node $ROOT, iteration $i..."
    /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
      fastsubtrees-query nt.tree $ROOT > \
        results/fastsubtrees.subtree.$ROOT
  done
done

