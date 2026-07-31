#!/bin/bash
# C1 transfer boru hatti: ornek-bazli transfer npz'leri + protokol istatistikleri
# (raw / target-correct / both-correct / successful-source), her tohum cifti icin.
# Konteyner icinde kosar: docker exec -w /workspace adeb_eval bash scripts/c1_transfer_pipeline.sh
set -u
cd /workspace || exit 1
LOG=logs/c1_transfer.log
mkdir -p logs results/c1_transfer

stamp() { date "+%Y-%m-%d %H:%M:%S"; }
say() { echo "[$(stamp)] $*" | tee -a "$LOG"; }

say "BASLANGIC C1 transfer"

if [ ! -f results/c1_transfer/pair3/per_sample_ViT_Tiny_AT_to_ResNet18_AT.npz ]; then
  say "START c1_transfer_rerun"
  if python scripts/c1_transfer_rerun.py --pairs 1 2 3 --n-samples 10000 --seed 42 >>logs/c1_transfer_rerun.log 2>&1; then
    say "DONE  c1_transfer_rerun"
  else
    say "FAIL  c1_transfer_rerun (bkz logs/c1_transfer_rerun.log)"
    exit 1
  fi
else
  say "SKIP  c1_transfer_rerun (ciktilar mevcut)"
fi

for p in 1 2 3; do
  say "START a2_protocols_pair$p"
  if A2_IN_DIR="results/c1_transfer/pair$p" \
     A2_OUT="/workspace/results/c1_transfer/pair$p/a2_transfer_protocols.json" \
     python experiments/rev2/a2_transfer_protocols.py >>logs/c1_transfer_a2_pair$p.log 2>&1; then
    say "DONE  a2_protocols_pair$p"
  else
    say "FAIL  a2_protocols_pair$p (bkz logs/c1_transfer_a2_pair$p.log)"
    exit 1
  fi
done

say "=============== C1-TRANSFER TAMAM ==============="
