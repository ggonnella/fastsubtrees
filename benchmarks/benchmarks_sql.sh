#!/bin/bash

#
# Benchmarks recursive SQL based subtree extraction
#

if [ $# -ne 5 ]; then
    echo "Usage: $0 <dbuser> <dbpass> <dbname> <dbsock> <ntdumpsdir>"
    echo "where:"
    echo "  <dbuser> is the database user name"
    echo "  <dbpass> is the database password"
    echo "  <dbname> is the database name"
    echo "  <dbsock> is the database socket file"
    echo "  <ntdumpsdir> is a directory containing NCBI taxonomy dump files"
    exit 1
fi
DBUSER=$1
DBPASS=$2
DBNAME=$3
DBSOCK=$4
NTDUMPSDIR=$5

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
FST_DIR=$SCRIPT_DIR/..
FST_DATA_DIR=$FST_DIR/data

source $SCRIPT_DIR/benchmarks_params.sh
OUTFILE=${OUTFILE_PFX}_sql.tsv
rm -f $OUTFILE
mkdir -p $OUTDIR

for ((i=0; i<$NREPEATS; i++)); do
  STEP="dbload"
  ROOT=""
  echo "Step $STEP, iteration $i..."
  /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
    ntmirror-dbload --testmode --reset \
      $DBUSER $DBPASS $DBNAME $DBSOCK $NTDUMPSDIR
done
for ((i=0; i<$NREPEATS; i++)); do
  STEP="extract"
  for ROOT in $NODES; do
    echo "Step $STEP from node $ROOT, iteration $i..."
    /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
      ntmirror-extract-subtree \
        $DBUSER $DBPASS $DBNAME $DBSOCK $ROOT > \
        $OUTDIR/ntmirror.subtree.$ROOT
  done
done
