#!/bin/bash
# Kullanim: bash _mk_foy_satir.sh 196,200 210,232 ...
f=/home/firat/projects/adeb_sci_1/results/C1_REFERANS_FOYU.md
for r in "$@"; do
  echo "=== $r"
  sed -n "${r}p" "$f" | cut -c1-700
done
