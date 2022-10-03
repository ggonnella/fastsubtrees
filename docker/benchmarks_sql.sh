#!/bin/bash

NREPEATS=3
OUTFILE=benchmarks_sql.tsv

rm -f $OUTFILE
for ((i=0; i<$NREPEATS; i++)); do
  STEP="dbload"
  ROOT=""
  echo "Step $STEP, iteration $i..."
  /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
    ntmirror-dbload --testmode --reset \
      myuser mypass ntmirror_test /run/mysqld/mysqld.sock ntdumpdir
done
for ((i=0; i<$NREPEATS; i++)); do
  STEP="extract"
  for ROOT in 511145 83333 562 561 543 91347 1236 1224 2; do
    echo "Step $STEP from node $ROOT, iteration $i..."
    /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
      ntmirror-extract-subtree \
        myuser mypass ntmirror_test /run/mysqld/mysqld.sock $ROOT > \
        ntmirror.subtree.$ROOT
  done
done

