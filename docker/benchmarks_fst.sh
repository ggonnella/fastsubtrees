#!/bin/bash

NREPEATS=3
OUTFILE=benchmarks_fst.tsv

rm -f $OUTFILE
for ((i=0; i<$NREPEATS; i++)); do
  STEP="construct"
  ROOT=""
  echo "Step $STEP, iteration $i..."
  rm -f nt.tree
  /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
    fastsubtrees-construct nt.tree \
      /fastsubtrees/ids_modules/ids_from_tabular_file.py \
      --keyargs separator='\t|\t' inputfile=/ntdumpdir/nodes.dmp
done
for ((i=0; i<$NREPEATS; i++)); do
  STEP="extract"
  for ROOT in 511145 83333 562 561 543 91347 1236 1224 2; do
    echo "Step $STEP from node $ROOT, iteration $i..."
    /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
      fastsubtrees-query nt.tree $ROOT > \
        fastsubtrees.subtree.$ROOT
  done
done

