#!/bin/bash
# Ikinci tur (dogrulayici duzeltmeleri) yeniden kosu: regresyon, sahte sinama, masa betiklerinin yeniden kosusu.
set -e
cd /workspace
D=""
for k in 1 2 3; do D="$D --matris-dizini results/c1_c3/pair$k"; done
for k in 1 2 3; do D="$D --matris-dizini results/q1/son_kontrol_noktasi/pair$k"; done
for k in 1 2 3; do D="$D --matris-dizini results/q1/cifar100/transfer/pair$k"; done
time python experiments/q1_konsey_ayrisim.py --mod masa --matris-dizini results/q1/havuz_cifar10 $D \
  --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu.json --cikti results/q1/konsey_masa/konsey_ayrisim_masa.json
time python experiments/q1_konsey_sahte_sinama.py
sha256sum experiments/q1_konsey_ayrisim.py raporlar/konsey_2026-10-29/hucre_tablosu.json
