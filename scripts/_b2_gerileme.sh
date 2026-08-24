#!/usr/bin/env bash
# B2 GERILEME KONTROLU -- hicbir mevcut artefakti EZMEZ.
#
# Yamalanmis a2'yi, mevcut dort veri kumesinin her ciftinde GECICI bir cikti
# dosyasina kosar. Sonra karsilastirir:
#   yeni.raw                       == eski.raw                 (birebir)
#   yeni.target_correct            == eski.target_correct      (birebir)
#   yeni.both_correct              == eski.both_correct        (birebir)
#   yeni.successful_source_loose   == eski.successful_source   (birebir)
#   yeni.successful_source         =  YENI deger (siki tanim)
set -u
cd "$(dirname "$0")/.." || exit 1
DEX=(docker exec -w /workspace adeb_eval)

DIZINLER=(
  results/c1_transfer/pair1 results/c1_transfer/pair2 results/c1_transfer/pair3
  results/q1/cifar100/transfer/pair1 results/q1/cifar100/transfer/pair2 results/q1/cifar100/transfer/pair3
  results/q1/svhn/transfer/pair1 results/q1/svhn/transfer/pair2
  results/q1/cifar10_l2/transfer/pair1 results/q1/cifar10_l2/transfer/pair2 results/q1/cifar10_l2/transfer/pair3
)

mkdir -p results/q1/_b2_gerileme
for d in "${DIZINLER[@]}"; do
  ad=$(echo "$d" | tr '/' '_')
  echo "== $d"
  "${DEX[@]}" env A2_IN_DIR="$d" \
      A2_OUT="/workspace/results/q1/_b2_gerileme/${ad}.json" \
      python -B experiments/rev2/a2_transfer_protocols.py >/dev/null \
    || { echo "  FAIL $d"; exit 1; }
done
echo
echo "yeni ciktilar: results/q1/_b2_gerileme/"
