#!/bin/bash
# KONTEYNER ICINDE calisir: yarim ViT-2001 AT'yi --resume ile tamamla,
# sonra idempotent pipeline'a devam et. (Host'tan degil docker exec ile cagrilir;
# log dosyalari root sahipli oldugundan yazma yetkisi ancak boyle saglanir.)
set -uo pipefail
cd /workspace
LOG=logs/c1_pipeline.log
log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

if [ ! -e "models/c1/vit_tiny_s2001/.at_complete" ]; then
    log "RESUME C1_at_vit_2001 (kesinti kurtarmasi, --resume)"
    if python -m cli.main train adversarial -m vit_tiny \
        -d adversarial_training \
        -p "models/c1/vit_tiny_s2001/vit_tiny/clean/best.pth" \
        -e 100 --lr 0.001 -b 64 --patience 20 \
        --seed 2001 --val-indices data/val_split_indices.json \
        -o "models/c1/vit_tiny_s2001" --resume >> logs/C1_at_vit_2001.log 2>&1; then
        touch "models/c1/vit_tiny_s2001/.at_complete"
        log "DONE  C1_at_vit_2001 (resume ile tamamlandi)"
    else
        log "FAIL  C1_at_vit_2001 (resume)"; exit 1
    fi
else
    log "SKIP  C1_at_vit_2001 (resume tamamlanmis)"
fi

exec bash /workspace/scripts/run_c1_pipeline.sh
