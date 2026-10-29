#!/bin/bash
# Celisik dogrulayici: --mod masa regresyonunun bagimsiz kosusu (29.10.2026)
set -e
cd /workspace
D=results/q1/konsey_masa/_dogrulayici
python experiments/q1_konsey_ayrisim.py --mod masa \
  --matris-dizini results/q1/havuz_cifar10 \
  --matris-dizini results/c1_c3/pair1 --matris-dizini results/c1_c3/pair2 --matris-dizini results/c1_c3/pair3 \
  --matris-dizini results/q1/son_kontrol_noktasi/pair1 --matris-dizini results/q1/son_kontrol_noktasi/pair2 --matris-dizini results/q1/son_kontrol_noktasi/pair3 \
  --matris-dizini results/q1/cifar100/transfer/pair1 --matris-dizini results/q1/cifar100/transfer/pair2 --matris-dizini results/q1/cifar100/transfer/pair3 \
  --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu.json \
  --cikti $D/dogrulayici_ayrisim_masa.json
