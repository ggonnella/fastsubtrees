#!/bin/bash

NREPEATS=3
OUTFILE=benchmarks_attr.tsv

rm -f $OUTFILE

declare -A attr_col
attr_col[genome_size]=2
attr_col[GC_content]=3

for attr in genome_size GC_content; do
  for ((i=0; i<$NREPEATS; i++)); do
    STEP="construct-$attr"
    /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
      fastsubtrees-attributes-construct $attr.attr /ncbi-taxonomy.tree \
        /fastsubtrees/data/attribute_values.py --keyargs \
          filename=/fastsubtrees/data/accession_taxid_attribute.tsv.gz \
          taxid_col=1 attr_col=${attr_col[$attr]}
  done

  rm -f $OUTFILE
  for ((i=0; i<$NREPEATS; i++)); do
    STEP="query-$attr"
    for ROOT in 511145 83333 562 561 543 91347 1236 1224 2; do
    echo "Step $STEP from node $ROOT, iteration $i..."
    /usr/bin/time -f "$STEP\t$ROOT\t$i\t%U\t%S\t%e\t%M" -o $OUTFILE -a \
      fastsubtrees-attributes-query \
        /ncbi-taxonomy.tree $ROOT $attr.attr > \
      attr_values.$attr.$ROOT
    done
  done
done
