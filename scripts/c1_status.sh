#!/bin/bash
# C1 durum ozeti: seed bazli PGD/AA sonuclarini basar.
cd /workspace || exit 1
for f in results/c1_seeds/pair*/pgd_summary_*.json results/c1_seeds/pair*/autoattack_summary.json; do
  [ -f "$f" ] || continue
  echo "== $f"
  cat "$f"
  echo
done
