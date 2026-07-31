#!/bin/bash
# C1 ikinci analiz dalgasi (dergi metni icin):
#   a5  : t-SNE nicellestirmesi
#   stat: istatistiksel dogrulama (saldiri-baslatma rastgeleligi)
#   C3  : WRN dahil 3x3 transfer matrisi
# Idempotent; her adim kendi guard dosyasina bakar.
set -uo pipefail
cd /workspace || exit 1
mkdir -p logs results/c1_a5 results/c1_statval results/c1_c3
LOG=logs/c1_wave2.log
log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

log "=============== C1-DALGA2 BASLANGIC ==============="

for p in 1 2 3; do
  case $p in
    1) RS=1001; VS=2001 ;;
    2) RS=1002; VS=2002 ;;
    3) RS=1003; VS=2003 ;;
  esac
  RNET="models/c1/resnet18_s${RS}/resnet18/adv/adversarial_training/best.pth"
  VIT="models/c1/vit_tiny_s${VS}/vit_tiny/adv/adversarial_training/best.pth"

  guard="results/c1_a5/pair${p}/a5_tsne_quant.json"
  if [ -e "$guard" ]; then
    log "SKIP  C1_a5_pair${p}"
  else
    log "START C1_a5_pair${p}"
    if A5_RESNET="$RNET" A5_VIT="$VIT" A5_OUT_DIR="/workspace/results/c1_a5/pair${p}" \
       python experiments/rev2/a5_tsne_quant.py >>"logs/C1_a5_pair${p}.log" 2>&1 && [ -e "$guard" ]; then
      log "DONE  C1_a5_pair${p}"
    else
      log "FAIL  C1_a5_pair${p} (logs/C1_a5_pair${p}.log)"
      exit 1
    fi
  fi
done

guard="results/c1_statval/statistical_validation.json"
if [ -e "$guard" ]; then
  log "SKIP  C1_statval"
else
  log "START C1_statval"
  if STATVAL_OUT_DIR="results/c1_statval" \
     python scripts/c1_statval_rerun.py >>logs/C1_statval.log 2>&1 && [ -e "$guard" ]; then
    log "DONE  C1_statval"
  else
    log "FAIL  C1_statval (logs/C1_statval.log)"
    exit 1
  fi
fi

guard="results/c1_c3/pair3/transfer_matrix.json"
if [ -e "$guard" ]; then
  log "SKIP  C1_c3"
else
  log "START C1_c3"
  if python experiments/c1_c3_transfer_matrix.py --pairs 1 2 3 --n-samples 10000 --seed 42 \
      >>logs/C1_c3.log 2>&1 && [ -e "$guard" ]; then
    log "DONE  C1_c3"
  else
    log "FAIL  C1_c3 (logs/C1_c3.log)"
    exit 1
  fi
fi

log "=============== C1-DALGA2 TAMAM ==============="
