#!/bin/bash
# C4'u her tohum cifti icin AYRI surecte kosar (tek surecte arka arkaya model
# yuklerken segfault aliyorduk). Idempotent.
set -uo pipefail
cd /workspace || exit 1
mkdir -p logs results/c1_c4
LOG=logs/c1_wave3.log
log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

for p in 1 2 3; do
  guard="results/c1_c4/pair${p}/c4_summary.json"
  if [ -e "$guard" ]; then
    log "SKIP  C1_c4_pair${p}"
    continue
  fi
  log "START C1_c4_pair${p}"
  if python experiments/c1_c4_attention_features.py --pairs "$p" --n-samples 1000 --seed 42 \
      >>"logs/C1_c4_pair${p}.log" 2>&1 && [ -e "$guard" ]; then
    log "DONE  C1_c4_pair${p}"
  else
    log "FAIL  C1_c4_pair${p} (logs/C1_c4_pair${p}.log)"
    exit 1
  fi
done

log "=============== C1-C4 TAMAM ==============="
