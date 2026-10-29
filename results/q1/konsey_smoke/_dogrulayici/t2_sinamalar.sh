#!/bin/bash
# Tur 2: kucuk sinamalar (konteynerde /workspace'ten).
cd /workspace
echo "=== 1. --skip-existing --cache-adv olmadan reddedilmeli"
python experiments/c1_c3_transfer_matrix.py --dataset cifar10 --n-samples 10 --seed 42 \
  --model ViT_Tiny_AT_s2001:vit_tiny:models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth \
  --rb-model Wong2020Fast --skip-existing --out-dir /tmp/t2_skip_red 2>&1 | tail -2
echo "rc=${PIPESTATUS[0]}; klasor olustu mu: $([ -d /tmp/t2_skip_red ] && echo EVET || echo HAYIR)"
echo "=== 2. adversarial_trainer ve denetim betigi derleniyor mu"
python -m py_compile src/training/adversarial_trainer.py scripts/konsey_b3_denetim.py scripts/konsey_b6_maskeleme.py experiments/c1_c3_transfer_matrix.py && echo derleme_tamam
bash -n scripts/konsey_b3_kuyruk.sh && echo bash_sozdizimi_tamam
echo "=== 3. B6 maskeleme betigi smoke (V_IN_smoke: AA n=50, matris_ekle n=200)"
python scripts/konsey_b6_maskeleme.py --aa-dizini results/q1/konsey_smoke/aa \
  --matris-dizini results/q1/konsey_smoke/matris_ekle --n 50 \
  --cikti results/q1/konsey_smoke/b6_maskeleme_smoke.json
echo "rc=$?"
echo "=== 4. B6 betigi, AA'dan uzun n istenince hata vermeli"
python scripts/konsey_b6_maskeleme.py --aa-dizini results/q1/konsey_smoke/aa \
  --matris-dizini results/q1/konsey_smoke/matris_ekle --n 1000 \
  --cikti /tmp/t2_b6_uzun.json; echo "rc=$?"
echo "=== 5. kuyruk --dry-run (gercek pilot)"
bash scripts/konsey_b3_kuyruk.sh --dry-run --pilot results/q1/konsey_pilot_zaman.json > results/q1/konsey_smoke/kuyruk_dry_run.txt
echo "rc=$?; satir: $(wc -l < results/q1/konsey_smoke/kuyruk_dry_run.txt)"
