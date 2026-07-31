#!/bin/bash
# C1 c_addenda koşusu (C20 ResNet kayma profili, C21 temiz gradyan, C22 MI-FGSM).
# c1_analyses_pipeline.sh bittikten sonra kosulur (GPU'yu paylasmamak icin).
set -uo pipefail
cd /workspace || exit 1
mkdir -p logs results/c1_addenda
LOG=logs/c1_analyses.log
log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

# Onceki asama bitene kadar bekle (en fazla 2 saat)
waited=0
while pgrep -f "c1_analyses_pipeline|c1_analyses_rerun" >/dev/null 2>&1; do
  sleep 60
  waited=$((waited + 60))
  if [ "$waited" -gt 7200 ]; then
    log "FAIL  C1_addenda (onceki asama 2 saatte bitmedi)"
    exit 1
  fi
done

if [ -e results/c1_addenda/pair3/mifgsm_transfer.json ]; then
  log "SKIP  C1_addenda"
else
  log "START C1_addenda"
  if python scripts/c1_addenda_rerun.py --pairs 1 2 3 >>logs/C1_addenda.log 2>&1 \
    && [ -e results/c1_addenda/pair3/mifgsm_transfer.json ]; then
    log "DONE  C1_addenda"
  else
    log "FAIL  C1_addenda (logs/C1_addenda.log)"
    exit 1
  fi
fi

log "=============== C1-ADDENDA TAMAM ==============="
