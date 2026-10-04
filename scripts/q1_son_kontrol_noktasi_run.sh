#!/usr/bin/env bash
# Faz 2.3 (LeCun plani, 2026-10-04): SON kontrol noktasi (adv/.../last.pth) ile uc ciftte 3x3 transfer
# matrisi (ornek bazinda kayit); referans RobustBench Gowal WRN-28-10 (C1 ile ayni). Secim kuralinin
# asimetriye etkisi: best.pth (C1) ile last.pth karsilastirilacak.
# Konteynerde arka planda: docker exec -d -w /workspace adeb_eval bash scripts/q1_son_kontrol_noktasi_run.sh
set -u
cd /workspace || exit 1
LOG=logs/q1_son_kontrol_noktasi.log
mkdir -p logs
{
echo "BASLADI $(date -u +%FT%TZ)"
for p in 1 2 3; do
    rs=$((1000 + p)); vs=$((2000 + p))
    out="results/q1/son_kontrol_noktasi/pair${p}"
    echo "== pair${p} -> ${out}"
    python experiments/c1_c3_transfer_matrix.py --dataset cifar10 --n-samples 10000 --seed 42 \
        --model "ResNet18_AT:resnet18:models/c1/resnet18_s${rs}/resnet18/adv/adversarial_training/last.pth" \
        --model "ViT_Tiny_AT:vit_tiny:models/c1/vit_tiny_s${vs}/vit_tiny/adv/adversarial_training/last.pth" \
        --out-dir "$out"
done
echo "BITTI $(date -u +%FT%TZ)"
} >> "$LOG" 2>&1
