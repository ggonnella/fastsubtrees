#!/bin/bash

NREPEATS=3
OUTFILE=benchmarks_sql.tsv

rm -f $OUTFILE
for ((i=0; i<$NREPEATS; i++)); do
    STEP="dbload"
    VAR=""
    echo "Step $STEP, iteration $i..."
    /usr/bin/time -f "$STEP\t$VAR\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
      ntmirror-dbload --testmode --reset \
        myuser mypass ntmirror_test /run/mysqld/mysqld.sock ntdumpdir
done

