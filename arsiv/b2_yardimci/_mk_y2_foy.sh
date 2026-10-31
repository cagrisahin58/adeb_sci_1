#!/bin/bash
# Kullanim: bash _mk_y2_foy.sh 1437,1445 1450,1458 ...
F=/home/firat/projects/adeb_sci_1/results/C1_REFERANS_FOYU.md
for r in "$@"; do
  echo "==== $r"
  a=${r%,*}; b=${r#*,}
  awk -v a="$a" -v b="$b" 'NR>=a && NR<=b {printf "%d: %s\n", NR, substr($0,1,420)}' "$F"
done
