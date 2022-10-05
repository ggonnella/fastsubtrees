#!/bin/bash
#
# Benchmarks the construction of the tree data files for fastsubtrees
#

NREPEATS=3
OUTFILE=benchmarks_construct.tsv

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
