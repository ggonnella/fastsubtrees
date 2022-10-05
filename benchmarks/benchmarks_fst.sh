#!/bin/bash
#
# Benchmarks the subtree query using fastsubtrees
#

if [ $# -ne 1 ]; then
    echo "Usage: $0 <tree>"
    echo "where <tree> is the name of a fastsubtrees tree file constructed"
    echo "with fastsubtrees-construct from a NCBI taxonomy dump"
    exit 1
fi
TREE=$1

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $SCRIPT_DIR/benchmarks_params.sh
OUTFILE=${OUTFILE_PFX}_fst.tsv
rm -f $OUTFILE
mkdir -p $OUTDIR

for ((i=0; i<$NREPEATS; i++)); do
  STEP="extract"
  for ROOT in 511145 83333 562 561 543 91347 1236 1224 2; do
    echo "Step $STEP from node $ROOT, iteration $i..."
    /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
      fastsubtrees-query $TREE $ROOT > \
        $OUTDIR/fastsubtrees.subtree.$ROOT
  done
done

