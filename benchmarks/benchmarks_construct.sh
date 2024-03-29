#!/bin/bash
#
# Benchmarks the construction of the tree data files for fastsubtrees
#

if [ $# -ne 2 ]; then
    echo "Usage: $0 <tree> <ntdumpsdir>"
    echo "where <ntdumpsdir> is the directory containing the NCBI taxonomy"
    echo "dump files to be used for the tree construction"
    exit 1
fi
TREE=$1
NTDUMPSDIR=$2

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
FST_DIR=$SCRIPT_DIR/..
FST_IDS_MODULES_DIR=$FST_DIR/fastsubtrees/ids_modules

source $SCRIPT_DIR/benchmarks_params.sh
OUTFILE=${OUTFILE_PFX}_construct.tsv
rm -f $OUTFILE

for ((i=0; i<$NREPEATS; i++)); do
  STEP="construct"
  ROOT=""
  echo "Step $STEP, iteration $i..."
  rm -f nt.tree
  /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
    fastsubtrees tree --force $TREE \
                      --ncbi $NTDUMPSDIR/nodes.dmp
done
