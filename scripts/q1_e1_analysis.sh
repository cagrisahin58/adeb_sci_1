#!/usr/bin/env bash
# E1 (CIFAR-100) analiz zinciri — E1'in BIRINCIL ciktisi.
#
# NEDEN AYRI BETIK: q1_pipeline.sh yalniz egitim + PGD degerlendirmesi kosar;
# transfer matrisi ve protokol analizi pipeline'da YOKTUR. Ara denetim bunu
# "unutulma riski gercek" olarak isaretledi. Bu betik zinciri tek komuta indirir.
#
# Kosum (E1 TAMAMEN bittikten sonra):
#   bash scripts/q1_e1_analysis.sh
# Tek cift icin:
#   PAIRS="1" bash scripts/q1_e1_analysis.sh
#
# Uretilenler:
#   results/q1/cifar100/transfer/pairN/per_sample_*.npz + transfer_matrix.json
#   results/q1/cifar100/transfer/pairN/a2_transfer_protocols.json
#   results/q1/cifar100/transfer/pairN/a2b_class_balance_cifar100.json
#   results/q1/cifar100/transfer/e1_transfer_summary.json   (3 tohum toplulastirma)
set -u

cd "$(dirname "$0")/.." || exit 1
DS=cifar100
PAIRS="${PAIRS:-1 2 3}"
OUT_ROOT="results/q1/${DS}/transfer"
DEX=(docker exec -w /workspace adeb_eval)

log() { echo "[$(date '+%F %T')] $*"; }

# --- 0. On kontrol: alti KOSUM DA BITMIS mi? ---
# DIKKAT: best.pth varligina BAKILMAZ -- egitim suruyorken de best.pth vardir
# (ilk epoktan itibaren yazilir) ve yari egitilmis modelle analiz kosmak sessiz
# bir bilim hatasidir. Bitmisligin kaniti pgd_summary_*.json'dur: o dosya yalniz
# egitim tamamlanip PGD degerlendirmesi kosunca uretilir.
missing=0
for i in 1 2 3; do
    for spec in "resnet18:s100${i}" "vit_tiny:s200${i}"; do
        arch="${spec%%:*}"; sfx="${spec##*:}"
        done_marker="results/q1/${DS}/${arch}_${sfx}/pgd_summary_${arch}.json"
        if [ ! -f "$done_marker" ]; then
            echo "BITMEMIS: ${arch} ${sfx} (yok: $done_marker)"
            missing=1
        fi
    done
done
if [ "$missing" = 1 ]; then
    echo
    echo "HATA: E1 kosumlari bitmemis. Once q1_pipeline.sh (STAGE=e1) tamamlansin."
    echo "      (best.pth VARLIGI bitmislik kaniti DEGILDIR -- egitim sirasinda da vardir.)"
    exit 1
fi

# --- 1. CUDA sert kontrolu (C1'de sessiz CPU dususu yasandi) ---
if ! "${DEX[@]}" python -c "import torch,sys; sys.exit(0 if torch.cuda.is_available() else 1)"; then
    echo "HATA: CUDA yok. Sessiz CPU dususune izin verilmiyor."
    exit 1
fi

for i in $PAIRS; do
    d="${OUT_ROOT}/pair${i}"
    mkdir -p "$d"

    # --- 2. Transfer matrisi (2x2, ornek-bazli maskeler) ---
    # Model adlari a2/a2b betiklerinin bekledigi adlarla AYNI olmak ZORUNDA.
    if [ -f "$d/transfer_matrix.json" ]; then
        log "SKIP transfer matrisi pair${i} (zaten var)"
    else
        log "START transfer matrisi pair${i}"
        "${DEX[@]}" python experiments/c1_c3_transfer_matrix.py \
            --dataset "$DS" --n-samples 10000 --seed 42 \
            --model "ResNet18_AT:resnet18:models/q1/${DS}/resnet18_s100${i}/resnet18/adv/adversarial_training/best.pth" \
            --model "ViT_Tiny_AT:vit_tiny:models/q1/${DS}/vit_tiny_s200${i}/vit_tiny/adv/adversarial_training/best.pth" \
            --out-dir "$d" || { echo "FAIL transfer pair${i}"; exit 1; }
        log "DONE transfer matrisi pair${i}"
    fi

    # --- 3. Dort protokol + bootstrap/permutasyon (veri kumesinden bagimsiz kod) ---
    log "START protokoller pair${i}"
    "${DEX[@]}" env A2_IN_DIR="$d" A2_OUT="$d/a2_transfer_protocols.json" \
        python experiments/rev2/a2_transfer_protocols.py \
        || { echo "FAIL a2 pair${i}"; exit 1; }

    # --- 4. Sinif bilesimi kontrolu (E7 icin yazildi; CIFAR-100'de de kosulur) ---
    log "START sinif bilesimi pair${i}"
    "${DEX[@]}" env A2B_IN_DIR="$d" A2B_DATASET="$DS" \
        A2B_OUT="$d/a2b_class_balance_${DS}.json" \
        python experiments/rev2/a2b_class_balance.py \
        || { echo "FAIL a2b pair${i}"; exit 1; }
    log "DONE pair${i}"
done

# --- 5. Uc tohum toplulastirma (C1 ile AYNI kod, yalniz girdi koku farkli) ---
if [ "$PAIRS" = "1 2 3" ]; then
    log "START toplulastirma"
    "${DEX[@]}" env AGG_IN_DIR="$OUT_ROOT" AGG_OLD="" \
        AGG_OUT_NAME="e1_transfer_summary.json" \
        python scripts/c1_transfer_aggregate.py \
        || { echo "FAIL toplulastirma"; exit 1; }
    log "DONE toplulastirma -> ${OUT_ROOT}/e1_transfer_summary.json"

    echo
    echo "=== B.4 madde 1 ON-KESTIRIM SINAMASI ==="
    echo "On-kayit: CIFAR-100 protokol yayilimi CIFAR-10'un 10,45 puanindan BUYUK olmali."
    "${DEX[@]}" python -c "
import json
d = json.load(open('${OUT_ROOT}/e1_transfer_summary.json'))
s = d.get('protocol_spread_pp', {})
print('CIFAR-100 yayilim :', s)
m = s.get('mean')
if m is None:
    print('HUKUM: yayilim alani yok, elle kontrol gerek')
else:
    print('CIFAR-10 referans : 10.45')
    print('HUKUM:', 'ON-KESTIRIM DOGRULANDI' if m > 10.45 else 'ON-KESTIRIM KARSILANMADI -> E1 tezi desteklemiyor olarak raporlanir (B.4)')
"
fi

echo
echo "NOT (3x3 karistirici matrisi): c1_c3_transfer_matrix.py, dataset cifar10/cifar100"
echo "ise WRN-28-10 referansini OTOMATIK ekler (has_rb kurali) ve gerekirse"
echo "RobustBench'ten indirir -- yani matris 2x2 degil 3x3 uretilir ve B.4 madde 3"
echo "(ham-kosullu sapma ~ hedefin temiz hatasi, CIFAR-10'da r=0,997) CIFAR-100'de"
echo "de sinanabilir. Ilk kosumda indirme olur; kesilirse .part dosyasi kalir ve"
echo "SILINMELIDIR (models/robustbench_zoo/cifar100/Linf/*.part)."
