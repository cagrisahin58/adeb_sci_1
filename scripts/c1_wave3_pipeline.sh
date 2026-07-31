#!/bin/bash
# C1 ucuncu analiz dalgasi: C4 (n=1000 oznitelik/attention) + C5 (mekansal lokalite).
# Dalga 2 bitene kadar bekler.
set -uo pipefail
cd /workspace || exit 1
mkdir -p logs results/c1_c4 results/c1_c5
LOG=logs/c1_wave3.log
log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

waited=0
while pgrep -f "c1_wave2|a5_tsne|c1_statval|c1_c3_transfer" >/dev/null 2>&1; do
  sleep 60
  waited=$((waited + 60))
  if [ "$waited" -gt 14400 ]; then
    log "FAIL  C1_wave3 (dalga2 4 saatte bitmedi)"
    exit 1
  fi
done

log "=============== C1-DALGA3 BASLANGIC ==============="

guard="results/c1_c5/pair3/c5_spatial.json"
if [ -e "$guard" ]; then
  log "SKIP  C1_c5"
else
  log "START C1_c5"
  if python experiments/c1_c5_spatial_locality.py --pairs 1 2 3 --n-samples 500 --seed 42 \
      >>logs/C1_c5.log 2>&1 && [ -e "$guard" ]; then
    log "DONE  C1_c5"
  else
    log "FAIL  C1_c5 (logs/C1_c5.log)"
    exit 1
  fi
fi

guard="results/c1_c4/pair3/c4_summary.json"
if [ -e "$guard" ]; then
  log "SKIP  C1_c4"
else
  log "START C1_c4"
  if python experiments/c1_c4_attention_features.py --pairs 1 2 3 --n-samples 1000 --seed 42 \
      >>logs/C1_c4.log 2>&1 && [ -e "$guard" ]; then
    log "DONE  C1_c4"
  else
    log "FAIL  C1_c4 (logs/C1_c4.log)"
    exit 1
  fi
fi

log "=============== C1-DALGA3 TAMAM ==============="
