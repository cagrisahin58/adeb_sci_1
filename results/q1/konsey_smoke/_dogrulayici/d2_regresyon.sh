#!/bin/bash
# Celisik dogrulayici, D2: degisiklik oncesi (HEAD 4972738) ve sonrasi matris
# kodu, iki C1 modeli, n=200, varsayilan bayraklar. Konteyner icinde /workspace'te.
set -euo pipefail
cd /workspace
D=results/q1/konsey_smoke/_dogrulayici
M1="ResNet18_AT_s1001:resnet18:models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth"
M2="ViT_Tiny_AT_s2001:vit_tiny:models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth"
rm -rf "$D/reg_eski" "$D/reg_yeni"
echo "== ESKI (HEAD) kod: $D/eski_kod/experiments/c1_c3_transfer_matrix.py"
python "$D/d2_calistir.py" "$D/eski_kod/experiments/c1_c3_transfer_matrix.py" \
    --model "$M1" --model "$M2" --n-samples 200 --seed 42 --out-dir "$D/reg_eski"
echo "== YENI (calisma agaci) kod: experiments/c1_c3_transfer_matrix.py"
python "$D/d2_calistir.py" experiments/c1_c3_transfer_matrix.py \
    --model "$M1" --model "$M2" --n-samples 200 --seed 42 --out-dir "$D/reg_yeni"
python "$D/d2_karsilastir.py" "$D/reg_eski" "$D/reg_yeni" "$D/d2_regresyon_karsilastirma.json"
