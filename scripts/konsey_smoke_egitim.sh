#!/bin/bash
# Konsey B1 smoke: 200 iterasyonluk temiz egitim (CLI yolu), IN baslatma ile
# rastgele baslatma ayni ayarla (AdamW lr 1e-4, b 128, sabit val bolmesi).
# Her cagri tek kosu; kullanim (konteynerde, /workspace):
#   bash scripts/konsey_smoke_egitim.sh <etiket> <tip> <init>
# Cikti: models/q1/konsey_smoke/<etiket>/, log results/q1/konsey_smoke/egitim_<etiket>.log
set -uo pipefail
cd /workspace
TAG="$1"; MT="$2"; INIT="$3"
LOG="results/q1/konsey_smoke/egitim_${TAG}.log"
mkdir -p results/q1/konsey_smoke
python -m cli.main train clean -m "$MT" --init-weights "$INIT" --optimizer adamw \
    -e 1 --lr 0.0001 -b 128 --seed 2101 --val-indices data/val_split_indices.json \
    --max-train-batches 200 -o "models/q1/konsey_smoke/${TAG}" 2>&1 \
    | tr '\r' '\n' | grep -v -E "it/s\]|s/it\]|^\s*$" > "$LOG"
tail -5 "$LOG"
