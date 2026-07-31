#!/bin/bash
# C1 eslesmis gradyan istatistikleri (a3): her tohum cifti icin ayni kod,
# per-sample Hoyer/Gini/rel-threshold + Wilcoxon/Holm + tum-cift alignment.
# Onceki C1 asamalari bitene kadar bekler.
set -uo pipefail
cd /workspace || exit 1
mkdir -p logs results/c1_a3
LOG=logs/c1_analyses.log
log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

waited=0
while pgrep -f "c1_analyses_pipeline|c1_analyses_rerun|c1_addenda_rerun|c1_addenda_pipeline" >/dev/null 2>&1; do
  sleep 60
  waited=$((waited + 60))
  if [ "$waited" -gt 10800 ]; then
    log "FAIL  C1_a3 (onceki asamalar 3 saatte bitmedi)"
    exit 1
  fi
done

for p in 1 2 3; do
  case $p in
    1) RS=1001; VS=2001 ;;
    2) RS=1002; VS=2002 ;;
    3) RS=1003; VS=2003 ;;
  esac
  guard="results/c1_a3/pair${p}/a3_gradient_paired.json"
  if [ -e "$guard" ]; then
    log "SKIP  C1_a3_pair${p}"
    continue
  fi
  log "START C1_a3_pair${p}"
  if A3_RESNET="models/c1/resnet18_s${RS}/resnet18/adv/adversarial_training/best.pth" \
     A3_VIT="models/c1/vit_tiny_s${VS}/vit_tiny/adv/adversarial_training/best.pth" \
     A3_OUT_DIR="/workspace/results/c1_a3/pair${p}" \
     python experiments/rev2/a3_gradient_paired.py >>"logs/C1_a3_pair${p}.log" 2>&1 && [ -e "$guard" ]; then
    log "DONE  C1_a3_pair${p}"
  else
    log "FAIL  C1_a3_pair${p} (logs/C1_a3_pair${p}.log)"
    exit 1
  fi
done

log "=============== C1-A3 TAMAM ==============="
