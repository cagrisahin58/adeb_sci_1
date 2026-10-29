#!/bin/bash
# Celisik dogrulayici, D3: matris betigi --attack mi ve --attack tgr (n=100),
# ardindan bagimsiz karsilastirma. Konteynerde /workspace'te.
set -euo pipefail
cd /workspace
D=results/q1/konsey_smoke/_dogrulayici
M1="ResNet18_AT_s1001:resnet18:models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth"
M2="ViT_Tiny_AT_s2001:vit_tiny:models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth"
rm -rf "$D/mi100" "$D/tgr100"
python experiments/c1_c3_transfer_matrix.py --model "$M1" --model "$M2" --n-samples 100 --seed 42 \
    --attack mi --out-dir "$D/mi100" 2>&1 | grep -v 'it/s'
python experiments/c1_c3_transfer_matrix.py --model "$M1" --model "$M2" --n-samples 100 --seed 42 \
    --attack tgr --out-dir "$D/tgr100" 2>&1 | grep -v 'it/s'
python "$D/d3_mi_tgr_bagimsiz.py" "$D/mi100" "$D/tgr100" "$D/d3_mi_tgr.json"
