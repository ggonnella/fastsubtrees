#!/bin/bash

#
# Benchmarks recursive SQL based subtree extraction
#

NREPEATS=3
OUTFILE=benchmarks_attr.tsv

if [ $# -ne 4 ]; then
    echo "Usage: $0 <dbuser> <dbpass> <dbname> <dbsock>"
    echo "where <dbuser> is the database user name, <dbpass> is the"
    echo "database password, <dbname> is the database name, and <dbsock>"
    echo "is the database socket."
    exit 1
fi
DBUSER=$1
DBPASS=$2
DBNAME=$3
DBSOCK=$4

rm -f $OUTFILE
mkdir -p results

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
FST_DIR=$SCRIPT_DIR/..
FST_DATA_DIR=$FST_DIR/data

for ((i=0; i<$NREPEATS; i++)); do
  STEP="dbload"
  ROOT=""
  echo "Step $STEP, iteration $i..."
  /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
    ntmirror-dbload --testmode --reset \
      $DBUSER $DBPASS $DBNAME $DBSOCK ntdumpdir
done
for ((i=0; i<$NREPEATS; i++)); do
  STEP="extract"
  for ROOT in 511145 83333 562 561 543 91347 1236 1224 2; do
    echo "Step $STEP from node $ROOT, iteration $i..."
    /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
      ntmirror-extract-subtree \
        $DBUSER $DBPASS $DBNAME $DBSOCK $ROOT > \
        results/ntmirror.subtree.$ROOT
  done
done
