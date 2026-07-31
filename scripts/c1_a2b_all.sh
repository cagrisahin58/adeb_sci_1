#!/bin/bash
# C1 dislayici-altkume (mekanizma) sayilari: her tohum cifti icin.
cd /workspace || exit 1
for p in 1 2 3; do
  echo "===== cift $p ====="
  A2B_IN_DIR="results/c1_transfer/pair$p" \
  A2B_OUT="/workspace/results/c1_transfer/pair$p/a2b_exclusive_subsets.json" \
    python experiments/rev2/a2b_exclusive_subsets.py || exit 1
done
