#!/usr/bin/env bash
# B2 duzeltmesinin GPU GEREKTIRMEYEN yeniden uretim zinciri.
#
# Sirasiyla: a2 (dort veri kumesi) -> sinif bilesimi -> tohum toplulastirmalari
# -> B kolu noktalari. A kolu (GPU) ayri kosar; E3 uydurmalari o bittikten
# sonra calistirilir.
set -eu
cd "$(dirname "$0")/.." || exit 1
DEX=(docker exec -w /workspace adeb_eval)
log() { echo "[$(date '+%T')] $*"; }

# ---------------------------------------------------------------- 1. a2
log "=== a2: dort protokol + gevsek tani ==="
for p in 1 2 3; do
    "${DEX[@]}" env A2_IN_DIR="results/c1_transfer/pair$p" \
        A2_OUT="/workspace/results/c1_transfer/pair$p/a2_transfer_protocols.json" \
        python -B experiments/rev2/a2_transfer_protocols.py > /dev/null
    log "  c10 pair$p"
done
for p in 1 2 3; do
    d="results/q1/cifar100/transfer/pair$p"
    "${DEX[@]}" env A2_IN_DIR="$d" A2_OUT="/workspace/$d/a2_transfer_protocols.json" \
        python -B experiments/rev2/a2_transfer_protocols.py > /dev/null
    "${DEX[@]}" env A2B_IN_DIR="$d" A2B_DATASET="cifar100" \
        A2B_OUT="/workspace/$d/a2b_class_balance_cifar100.json" \
        python -B experiments/rev2/a2b_class_balance.py > /dev/null
    log "  c100 pair$p"
done
for p in 1 2; do
    d="results/q1/svhn/transfer/pair$p"
    "${DEX[@]}" env A2_IN_DIR="$d" A2_OUT="/workspace/$d/a2_transfer_protocols.json" \
        python -B experiments/rev2/a2_transfer_protocols.py > /dev/null
    "${DEX[@]}" env A2B_IN_DIR="$d" A2B_DATASET="svhn" \
        A2B_OUT="/workspace/$d/a2b_class_balance_svhn.json" \
        python -B experiments/rev2/a2b_class_balance.py > /dev/null
    log "  svhn pair$p"
done
for p in 1 2 3; do
    d="results/q1/cifar10_l2/transfer/pair$p"
    "${DEX[@]}" env A2_IN_DIR="$d" A2_OUT="/workspace/$d/a2_transfer_protocols.json" \
        python -B experiments/rev2/a2_transfer_protocols.py > /dev/null
    log "  l2 pair$p"
done

# ------------------------------------------------------- 2. toplulastirmalar
log "=== tohum toplulastirmalari ==="
"${DEX[@]}" env AGG_IN_DIR="results/c1_transfer" AGG_PAIRS="1 2 3" \
    python -B scripts/c1_transfer_aggregate.py > /dev/null
log "  c10 -> c1_transfer_summary.json"

"${DEX[@]}" env AGG_IN_DIR="results/q1/cifar100/transfer" AGG_OLD="" \
    AGG_OUT_NAME="e1_transfer_summary.json" \
    AGG_TITLE="E1 Transfer Protokolleri - CIFAR-100, 3 Tohum" \
    AGG_MD_NAME="E1_TRANSFER_RAPORU.md" \
    AGG_DESC="Ayni istatistik kodu (a2_transfer_protocols.py), E1 (CIFAR-100) kontrol noktalarina uygulandi. Her satir 3 tohum ortalamasi +- std." \
    AGG_PAIRS="1 2 3" python -B scripts/c1_transfer_aggregate.py > /dev/null
log "  c100 -> e1_transfer_summary.json"

"${DEX[@]}" env AGG_IN_DIR="results/q1/svhn/transfer" AGG_OLD="" \
    AGG_OUT_NAME="e7_transfer_summary.json" \
    AGG_TITLE="E7 Transfer Protokolleri - SVHN, 2 Tohum" \
    AGG_MD_NAME="E7_TRANSFER_RAPORU.md" \
    AGG_DESC="Ayni istatistik kodu (a2_transfer_protocols.py), E7 (SVHN, kisa surum) kontrol noktalarina uygulandi. Her satir 2 tohum ortalamasi +- std. UCUNCU MIMARI YOKTUR (2x2 matris)." \
    AGG_PAIRS="1 2" python -B scripts/c1_transfer_aggregate.py > /dev/null
log "  svhn -> e7_transfer_summary.json"

"${DEX[@]}" env AGG_IN_DIR="results/q1/cifar10_l2/transfer" AGG_OLD="" \
    AGG_OUT_NAME="e6_l2_transfer_summary.json" \
    AGG_TITLE="E6 Transfer Protokolleri - CIFAR-10, L2 tehdit modeli, 3 Tohum" \
    AGG_MD_NAME="E6_L2_TRANSFER_RAPORU.md" \
    AGG_DESC="Ayni istatistik kodu (a2_transfer_protocols.py), C1 kontrol noktalarina L2 BUTCESI (eps=0,5) altinda uygulandi. Her satir 3 tohum ortalamasi +- std. DIKKAT: modeller L-infinity ile EGITILMISTIR; bu sayilar L2-EGITILMIS referanslarla KARSILASTIRILAMAZ (E6_ON_KAYIT §0)." \
    AGG_PAIRS="1 2 3" python -B scripts/c1_transfer_aggregate.py > /dev/null
log "  l2 -> e6_l2_transfer_summary.json"

# --------------------------------------------------------- 3. B kolu noktalari
log "=== B kolu noktalari ==="
"${DEX[@]}" python -B scripts/q1_e3_bkolu.py --out-dir results/q1/e3_points | tail -3
"${DEX[@]}" python -B scripts/q1_e3_bkolu_c10_wrn.py | tail -3

log "=== GPU'SUZ ZINCIR TAMAM ==="
