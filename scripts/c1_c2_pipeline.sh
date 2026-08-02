#!/bin/bash
# C2: TGR transfer saldirisi, her tohum cifti ayri surecte (bellek guvenligi).
set -uo pipefail
cd /workspace || exit 1
mkdir -p logs results/c1_c2
LOG=logs/c1_c2.log
log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

log "=============== C1-C2 BASLANGIC ==============="
for p in 1 2 3; do
  guard="results/c1_c2/pair${p}/tgr_summary.json"
  if [ -e "$guard" ]; then
    log "SKIP  C1_c2_pair${p}"
    continue
  fi
  log "START C1_c2_pair${p}"
  if python experiments/c1_c2_tgr.py --pairs "$p" --n-samples 10000 --seed 42 \
      >>"logs/C1_c2_pair${p}.log" 2>&1 && [ -e "$guard" ]; then
    log "DONE  C1_c2_pair${p}"
  else
    log "FAIL  C1_c2_pair${p} (logs/C1_c2_pair${p}.log)"
    exit 1
  fi
done
log "=============== C1-C2 TAMAM ==============="
