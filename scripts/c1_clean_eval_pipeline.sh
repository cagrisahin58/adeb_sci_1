#!/bin/bash
# C1 temiz (AT'siz) kontrol noktalarinin FGSM/PGD degerlendirmesi.
# Tablo I'in "AT yok" satirlari da 3 tohumdan gelsin diye.
set -uo pipefail
cd /workspace || exit 1
mkdir -p logs results/c1_eval_clean
LOG=logs/c1_analyses.log
log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

waited=0
while pgrep -f "c1_analyses_pipeline|c1_analyses_rerun|c1_addenda_rerun|c1_addenda_pipeline|a3_gradient_paired|c1_gradient_paired" >/dev/null 2>&1; do
  sleep 60
  waited=$((waited + 60))
  if [ "$waited" -gt 14400 ]; then
    log "FAIL  C1_clean_eval (onceki asamalar 4 saatte bitmedi)"
    exit 1
  fi
done

EPS8=0.03137254901960784
for p in 1 2 3; do
  case $p in
    1) RS=1001; VS=2001 ;;
    2) RS=1002; VS=2002 ;;
    3) RS=1003; VS=2003 ;;
  esac
  for spec in "resnet18:models/c1/resnet18_s${RS}/resnet18/clean/best.pth" \
              "vit_tiny:models/c1/vit_tiny_s${VS}/vit_tiny/clean/best.pth"; do
    mt="${spec%%:*}"
    mp="${spec#*:}"
    guard="results/c1_eval_clean/pair${p}/${mt}/${mt}_robustness_results.csv"
    if [ -e "$guard" ]; then
      log "SKIP  C1_cleaneval_${mt}_p${p}"
      continue
    fi
    log "START C1_cleaneval_${mt}_p${p}"
    if python -m cli.main evaluate robustness -m "$mp" -t "$mt" -a fgsm -a pgd -e $EPS8 \
        --seed 42 -o "results/c1_eval_clean/pair${p}/${mt}" \
        >>"logs/C1_cleaneval_${mt}_p${p}.log" 2>&1 && [ -e "$guard" ]; then
      log "DONE  C1_cleaneval_${mt}_p${p}"
    else
      log "FAIL  C1_cleaneval_${mt}_p${p}"
      exit 1
    fi
  done
done

log "=============== C1-CLEANEVAL TAMAM ==============="
