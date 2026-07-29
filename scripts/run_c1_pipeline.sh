#!/bin/bash
# =============================================================================
# rev2 C1 PIPELINE: mimari basina 3 tam kosum (clean pretrain + AT) + full eval
#   ResNet seeds: 1001 1002 1003   |   ViT seeds: 2001 2002 2003
#   Ortak SABIT val bolmesi: data/val_split_indices.json (leak fix — clean
#   pretraining de ayni ornekleri egitimden cikarir; secim val uzerinden)
# Idempotent: artefakti olan adim atlanir. Devam: ayni komut.
#   docker exec adeb_eval bash /workspace/scripts/run_c1_pipeline.sh
# Sure kayitlari: TIMING.md (adim baslangic/bitis + saniye)
# =============================================================================
set -uo pipefail
cd /workspace
LOG=logs/c1_pipeline.log
TIMING=TIMING.md
mkdir -p logs results/c1_seeds
log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }
tstamp() { date +%s; }

run_step() {
    local name="$1" artifact="$2"; shift 2
    if [ -e "$artifact" ]; then log "SKIP  $name (artefakt var)"; return 0; fi
    log "START $name"
    local t0; t0=$(tstamp)
    if "$@" >> "logs/${name}.log" 2>&1; then
        local dt=$(( $(tstamp) - t0 ))
        log "DONE  $name (${dt}s)"
        echo "| $name | ${dt}s | $(date '+%F %T') |" >> "$TIMING"
    else
        log "FAIL  $name (logs/${name}.log)"; exit 1
    fi
}

log "=============== C1-PIPELINE BASLANGIC ==============="
[ -f "$TIMING" ] || { echo "# TIMING — rev2 C1 (RTX 5090, paylasimli GPU)"; echo; echo "| Adim | Sure | Bitis |"; echo "|---|---|---|"; } >> "$TIMING"

# --- 0) Sabit val bolmesi ----------------------------------------------------
run_step C1_val_split "data/val_split_indices.json" \
    python experiments/rev2/make_val_split.py

# --- 1) Kosum ciftleri -------------------------------------------------------
for i in 1 2 3; do
    RSEED=$((1000 + i)); VSEED=$((2000 + i))

    # ResNet: clean pretrain (200 epoch, SGD lr 0.1) -> AT fine-tune (100, lr 1e-3)
    run_step "C1_clean_resnet_${RSEED}" "models/c1/resnet18_s${RSEED}/resnet18/clean/best.pth" \
        python -m cli.main train clean -m resnet18 -e 200 --lr 0.1 -b 128 \
            --seed "$RSEED" --val-indices data/val_split_indices.json \
            -o "models/c1/resnet18_s${RSEED}"
    run_step "C1_at_resnet_${RSEED}" "models/c1/resnet18_s${RSEED}/resnet18/adv/adversarial_training/best.pth" \
        python -m cli.main train adversarial -m resnet18 -d adversarial_training \
            -p "models/c1/resnet18_s${RSEED}/resnet18/clean/best.pth" \
            -e 100 --lr 0.001 -b 128 --patience 20 \
            --seed "$RSEED" --val-indices data/val_split_indices.json \
            -o "models/c1/resnet18_s${RSEED}"

    # ViT: clean pretrain (200 epoch, AdamW lr 1e-3) -> AT fine-tune (100, lr 1e-3, b 64)
    run_step "C1_clean_vit_${VSEED}" "models/c1/vit_tiny_s${VSEED}/vit_tiny/clean/best.pth" \
        python -m cli.main train clean -m vit_tiny -e 200 --lr 0.001 -b 128 \
            --seed "$VSEED" --val-indices data/val_split_indices.json \
            -o "models/c1/vit_tiny_s${VSEED}"
    run_step "C1_at_vit_${VSEED}" "models/c1/vit_tiny_s${VSEED}/vit_tiny/adv/adversarial_training/best.pth" \
        python -m cli.main train adversarial -m vit_tiny -d adversarial_training \
            -p "models/c1/vit_tiny_s${VSEED}/vit_tiny/clean/best.pth" \
            -e 100 --lr 0.001 -b 64 --patience 20 \
            --seed "$VSEED" --val-indices data/val_split_indices.json \
            -o "models/c1/vit_tiny_s${VSEED}"

    # Full-test PGD-10 (per-sample) — her iki model
    run_step "C1_pgd_resnet_${RSEED}" "results/c1_seeds/pair${i}/pgd_summary_resnet18_s${RSEED}.json" \
        python scripts/c1_pgd_eval.py --model-type resnet18 \
            --ckpt "models/c1/resnet18_s${RSEED}/resnet18/adv/adversarial_training/best.pth" \
            --out "results/c1_seeds/pair${i}" --tag "resnet18_s${RSEED}"
    run_step "C1_pgd_vit_${VSEED}" "results/c1_seeds/pair${i}/pgd_summary_vit_tiny_s${VSEED}.json" \
        python scripts/c1_pgd_eval.py --model-type vit_tiny \
            --ckpt "models/c1/vit_tiny_s${VSEED}/vit_tiny/adv/adversarial_training/best.pth" \
            --out "results/c1_seeds/pair${i}" --tag "vit_tiny_s${VSEED}"

    # Full-test AutoAttack (per-sample, chunked) — cift olarak
    run_step "C1_aa_pair${i}" "results/c1_seeds/pair${i}/autoattack_summary.json" \
        python experiments/run_autoattack_run2.py --n-samples 10000 --seed 42 \
            --resnet-path "models/c1/resnet18_s${RSEED}/resnet18/adv/adversarial_training/best.pth" \
            --vit-path "models/c1/vit_tiny_s${VSEED}/vit_tiny/adv/adversarial_training/best.pth" \
            --output-dir "results/c1_seeds/pair${i}"
done

log "=============== C1-PIPELINE TAMAM ==============="
