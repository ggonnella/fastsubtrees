#!/bin/bash
#
# Benchmarks the subtree query using fastsubtrees
#

NREPEATS=3
OUTFILE=benchmarks_fst.tsv

if [ $# -ne 1 ]; then
    echo "Usage: $0 <tree>"
    echo "where <tree> is the name of a fastsubtrees tree file constructed"
    echo "with fastsubtrees-construct from a NCBI taxonomy dump"
    exit 1
fi
TREE=$1

rm -f $OUTFILE
mkdir -p results

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
FST_DIR=$SCRIPT_DIR/..

for ((i=0; i<$NREPEATS; i++)); do
  STEP="extract"
  for ROOT in 511145 83333 562 561 543 91347 1236 1224 2; do
    echo "Step $STEP from node $ROOT, iteration $i..."
    /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
      fastsubtrees-query $TREE $ROOT > \
        results/fastsubtrees.subtree.$ROOT
  done
done

