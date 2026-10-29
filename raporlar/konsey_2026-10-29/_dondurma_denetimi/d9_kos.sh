#!/bin/bash
# Konteynerde (/workspace) kosar. Masa regresyonu ve sahte sinamayi, depodaki
# islenecek dosyalara dokunmadan yeniden kosar.
set -u
cd /workspace || exit 1
D=raporlar/konsey_2026-10-29/_dondurma_denetimi
S=$D/kok
rm -rf "$S"
mkdir -p "$S/experiments" "$S/results/q1/_konsey_sahte" "$S/raporlar/konsey_2026-10-29"
cp experiments/q1_konsey_ayrisim.py experiments/q1_konsey_sahte_sinama.py "$S/experiments/"
cp raporlar/konsey_2026-10-29/hucre_tablosu.json "$S/raporlar/konsey_2026-10-29/"
cp results/q1/konsey_sentez_r_tau_masa.json "$S/results/q1/"
mkdir -p "$S/results/q1"
ln -s /workspace/results/c1_c3 "$S/results/c1_c3"
ln -s /workspace/results/q1/son_kontrol_noktasi "$S/results/q1/son_kontrol_noktasi"
ln -s /workspace/results/q1/havuz_cifar10 "$S/results/q1/havuz_cifar10"
ln -s /workspace/src "$S/src"
ln -s /workspace/data "$S/data"
echo "kopya ozetleri:"; sha256sum "$S/experiments/q1_konsey_ayrisim.py" "$S/raporlar/konsey_2026-10-29/hucre_tablosu.json"

echo "=== 1. masa regresyonu ==="
T0=$(date +%s.%N)
timeout 120 python experiments/q1_konsey_ayrisim.py --mod masa \
  --matris-dizini results/q1/havuz_cifar10 \
  --matris-dizini results/c1_c3/pair1 --matris-dizini results/c1_c3/pair2 --matris-dizini results/c1_c3/pair3 \
  --matris-dizini results/q1/son_kontrol_noktasi/pair1 --matris-dizini results/q1/son_kontrol_noktasi/pair2 --matris-dizini results/q1/son_kontrol_noktasi/pair3 \
  --matris-dizini results/q1/cifar100/transfer/pair1 --matris-dizini results/q1/cifar100/transfer/pair2 --matris-dizini results/q1/cifar100/transfer/pair3 \
  --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu.json \
  --cikti $D/d9_ayrisim_masa.json
echo "cikis: $? sure: $(echo "$(date +%s.%N) - $T0" | bc)"

echo "=== 2. sahte sinama (gecici kokte) ==="
T0=$(date +%s.%N)
( cd "$S" && timeout 200 python experiments/q1_konsey_sahte_sinama.py )
echo "cikis: $? sure: $(echo "$(date +%s.%N) - $T0" | bc)"
ls -la "$S/results/q1/" "$S/results/q1/_konsey_sahte/"
