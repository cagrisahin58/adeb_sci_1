#!/bin/bash
# C1 kalan analizler: FGSM/PGD degerlendirme, epsilon taramasi, gradyan yapisi,
# blok bazli oznitelik kaymasi. Uc tohum cifti icin, idempotent.
# Kosum: docker exec -d -w /workspace adeb_eval bash scripts/c1_analyses_pipeline.sh
set -uo pipefail
cd /workspace || exit 1
mkdir -p logs results/c1_eval results/c1_sweep

LOG=logs/c1_analyses.log
log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

run_step() {
  local name="$1" guard="$2"; shift 2
  if [ -e "$guard" ]; then log "SKIP  $name"; return 0; fi
  log "START $name"
  if "$@" >>"logs/${name}.log" 2>&1 && [ -e "$guard" ]; then
    log "DONE  $name"
  else
    log "FAIL  $name (logs/${name}.log)"
    exit 1
  fi
}

EPS8=0.03137254901960784
EPS2=0.00784313725490196
EPS4=0.01568627450980392
EPS16=0.06274509803921569

log "=============== C1-ANALIZ BASLANGIC ==============="

for p in 1 2 3; do
  case $p in
    1) RS=1001; VS=2001 ;;
    2) RS=1002; VS=2002 ;;
    3) RS=1003; VS=2003 ;;
  esac
  RNET="models/c1/resnet18_s${RS}/resnet18/adv/adversarial_training/best.pth"
  VIT="models/c1/vit_tiny_s${VS}/vit_tiny/adv/adversarial_training/best.pth"

  run_step "C1_eval_resnet_p${p}" "results/c1_eval/pair${p}/resnet18/resnet18_robustness_results.csv" \
    python -m cli.main evaluate robustness -m "$RNET" -t resnet18 \
    -a fgsm -a pgd -e $EPS8 --seed 42 -o "results/c1_eval/pair${p}/resnet18"

  run_step "C1_eval_vit_p${p}" "results/c1_eval/pair${p}/vit_tiny/vit_tiny_robustness_results.csv" \
    python -m cli.main evaluate robustness -m "$VIT" -t vit_tiny \
    -a fgsm -a pgd -e $EPS8 --seed 42 -o "results/c1_eval/pair${p}/vit_tiny"

  run_step "C1_sweep_resnet_p${p}" "results/c1_sweep/pair${p}/resnet18/resnet18_robustness_results.csv" \
    python -m cli.main evaluate robustness -m "$RNET" -t resnet18 \
    -a pgd -e $EPS2 -e $EPS4 -e $EPS8 -e $EPS16 --seed 42 -o "results/c1_sweep/pair${p}/resnet18"

  run_step "C1_sweep_vit_p${p}" "results/c1_sweep/pair${p}/vit_tiny/vit_tiny_robustness_results.csv" \
    python -m cli.main evaluate robustness -m "$VIT" -t vit_tiny \
    -a pgd -e $EPS2 -e $EPS4 -e $EPS8 -e $EPS16 --seed 42 -o "results/c1_sweep/pair${p}/vit_tiny"
done

run_step C1_gradient "results/c1_gradient/pair3/gradient_summary.json" \
  python scripts/c1_analyses_rerun.py --only gradient --pairs 1 2 3

run_step C1_drift "results/c1_drift/pair3/attention_summary.json" \
  python scripts/c1_analyses_rerun.py --only drift --pairs 1 2 3

log "=============== C1-ANALIZ TAMAM ==============="
