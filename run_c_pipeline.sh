#!/bin/bash
# =============================================================================
# C-MADDELERI PIPELINE'I (2026-07-10 paneli, kullanici onayli GPU kosulari)
# Idempotent: artefakti olan adim atlanir. Kesinti sonrasi ayni komutla devam:
#   docker exec adeb_eval bash /workspace/run_c_pipeline.sh
# C23 (>=3 egitim seed'i) BILEREK kapsam disi (en pahali; metin onsuz yazildi).
# =============================================================================
set -uo pipefail
cd /workspace
mkdir -p logs results/c_addenda

MASTER_LOG=logs/c_pipeline.log
log() { echo "[$(date '+%F %T')] $*" | tee -a "$MASTER_LOG"; }

run_step() {
    local name="$1"; local guard="$2"; shift 2
    if [ -e "$guard" ]; then log "SKIP  $name"; return 0; fi
    log "START $name"
    if "$@" >> "logs/${name}.log" 2>&1 && [ -e "$guard" ]; then
        log "DONE  $name"
    else
        log "FAIL  $name (logs/${name}.log)"; exit 1
    fi
}

EPS8=0.03137254901960784
EPS2=0.00784313725490196
EPS4=0.01568627450980392
EPS16=0.06274509803921569
R3NET=models/resnet18/adv/at_run3/resnet18/adv/adversarial_training/best.pth
V3IT=models/vit_tiny/adv/at_run3/vit_tiny/adv/adversarial_training/best.pth

log "=============== C-PIPELINE BASLANGIC ==============="

# --- C21 + C20 + C22 (run_c_addenda kendi icinde idempotent) -----------------
run_step C_addenda "results/c_addenda/mifgsm_transfer.json" \
    python -u experiments/run_c_addenda.py

# --- C19: clean-model kosullu transfer matrisi --------------------------------
run_step C19_clean_transfer "results/transfer_analysis_clean/transfer_summary.json" \
    python -u experiments/run_all_analyses_run2.py --only transfer \
        --n-samples 10000 --seed 42 \
        --resnet-path models/resnet18/clean/best.pth \
        --vit-path models/vit_tiny/clean/best.pth \
        --transfer-output-dir results/transfer_analysis_clean

# --- C24: Tablo 1 + eps-sweep hucrelerinin SEED'LI yeniden uretimi -------------
run_step C24_eval_resnet_at "results/final_eval_seeded/resnet18_at/resnet18_robustness_results.csv" \
    python -m cli.main evaluate robustness -m "$R3NET" -t resnet18 \
        -a fgsm -a pgd -e $EPS8 --seed 42 -o results/final_eval_seeded/resnet18_at
run_step C24_eval_vit_at "results/final_eval_seeded/vit_tiny_at/vit_tiny_robustness_results.csv" \
    python -m cli.main evaluate robustness -m "$V3IT" -t vit_tiny \
        -a fgsm -a pgd -e $EPS8 --seed 42 -o results/final_eval_seeded/vit_tiny_at
run_step C24_eval_resnet_clean "results/final_eval_seeded/resnet18_clean/resnet18_robustness_results.csv" \
    python -m cli.main evaluate robustness -m models/resnet18/clean/best.pth -t resnet18 \
        -a fgsm -a pgd -e $EPS8 --seed 42 -o results/final_eval_seeded/resnet18_clean
run_step C24_eval_vit_clean "results/final_eval_seeded/vit_tiny_clean/vit_tiny_robustness_results.csv" \
    python -m cli.main evaluate robustness -m models/vit_tiny/clean/best.pth -t vit_tiny \
        -a fgsm -a pgd -e $EPS8 --seed 42 -o results/final_eval_seeded/vit_tiny_clean
run_step C24_sweep_resnet "results/epsilon_sweep_seeded/resnet18/resnet18_robustness_results.csv" \
    python -m cli.main evaluate robustness -m "$R3NET" -t resnet18 \
        -a pgd -e $EPS2 -e $EPS4 -e $EPS8 -e $EPS16 --seed 42 \
        -o results/epsilon_sweep_seeded/resnet18
run_step C24_sweep_vit "results/epsilon_sweep_seeded/vit_tiny/vit_tiny_robustness_results.csv" \
    python -m cli.main evaluate robustness -m "$V3IT" -t vit_tiny \
        -a pgd -e $EPS2 -e $EPS4 -e $EPS8 -e $EPS16 --seed 42 \
        -o results/epsilon_sweep_seeded/vit_tiny

log "=============== C-PIPELINE TAMAM ==============="
