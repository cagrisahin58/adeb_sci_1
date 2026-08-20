#!/usr/bin/env bash
# E6 — L2 tehdit modeli (CIFAR-10 YALNIZ). Ön-kayıt: results/q1_research/E6_ON_KAYIT.md
#
# NE YAPAR: L∞ ile çekişmeli eğitilmiş C1 ana çiftini (3 tohum) L2 bütçesi
# altında ölçer. Aynı ağırlıklar, farklı ölçüm aleti.
#
# NE İDDİA ETMEZ: modellerin L2-gürbüz olduğunu. Çıkan mutlak sayılar
# RobustBench'in L2-EĞİTİLMİŞ girdileriyle KARŞILAŞTIRILAMAZ (E6_ON_KAYIT §0).
#
# Kosum (E7 BITTIKTEN SONRA):
#   bash scripts/q1_e6_l2.sh
# AA-L2'yi atlamak icin:
#   E6_SKIP_AA=1 bash scripts/q1_e6_l2.sh
set -u

cd "$(dirname "$0")/.." || exit 1
DEX=(docker exec -w /workspace adeb_eval)
OUT="results/q1/cifar10_l2"
log() { echo "[$(date '+%F %T')] $*"; }

# --- on-kayitli sabitler (E6_ON_KAYIT.md §1) -- DEGISTIRILMEZ ---
EPS_L2=0.5
ALPHA_L2=0.125          # 2,5 * eps / steps
STEPS_L2=10
N_PGD=10000             # tam test kumesi
N_AA=5000               # butce indirimi, BEYAN EDILMIS

# --- 0. GPU cakismasi muhafizi ---
# E7 (veya baska bir q1 kosumu) suruyorsa ikisi de yavaslar. Bilincli
# uzerine binmek icin E6_FORCE=1.
if "${DEX[@]}" bash -lc 'pgrep -f "q1_pipeline.sh" >/dev/null'; then
    if [ "${E6_FORCE:-0}" != "1" ]; then
        echo "DURDURULDU: q1_pipeline.sh kosuyor (buyuk olasilikla E7)."
        echo "  Iki GPU isini ust uste bindirmek ikisini de yavaslatir."
        echo "  E7 bitince tekrar calistirin, ya da bilerek E6_FORCE=1 verin."
        exit 1
    fi
    echo "UYARI: q1_pipeline.sh kosuyor ama E6_FORCE=1 verildi; devam ediliyor."
fi

# --- 1. On kosul: C1 modelleri ve C1 sonuclari var mi (K6) ---
missing=0
for i in 1 2 3; do
    for spec in "resnet18:100${i}" "vit_tiny:200${i}"; do
        arch="${spec%%:*}"; seed="${spec##*:}"
        ck="models/c1/${arch}_s${seed}/${arch}/adv/adversarial_training/best.pth"
        [ -f "$ck" ] || { echo "EKSIK MODEL: $ck"; missing=1; }
    done
done
# C1'in BITMIS oldugunun kaniti: toplulastirilmis sonuc dosyasi
[ -f results/c1_seeds/c1_seed_summary.json ] || {
    echo "EKSIK: results/c1_seeds/c1_seed_summary.json (C1 bitmislik kaniti)"; missing=1; }
if [ "$missing" = 1 ]; then
    echo; echo "HATA: E6 on kosullari saglanmadi."; exit 1
fi

# --- 2. CUDA sert kontrolu ---
if ! "${DEX[@]}" python -c "import torch,sys; sys.exit(0 if torch.cuda.is_available() else 1)"; then
    echo "HATA: CUDA yok. Sessiz CPU dususune izin verilmiyor."; exit 1
fi

mkdir -p "$OUT"
log "E6 basliyor -- L2, eps=${EPS_L2}, alpha=${ALPHA_L2}, steps=${STEPS_L2}"
log "  PGD-L2 n=${N_PGD} (tam test) · AA-L2 n=${N_AA} (beyan edilmis butce indirimi)"

# --- 3. PGD-L2 beyaz kutu degerlendirmesi (6 model) ---
for i in 1 2 3; do
    for spec in "resnet18:100${i}" "vit_tiny:200${i}"; do
        arch="${spec%%:*}"; seed="${spec##*:}"
        d="${OUT}/${arch}_s${seed}"
        if [ -f "${d}/pgd_summary_${arch}.json" ]; then
            log "SKIP PGD-L2 ${arch} s${seed}"; continue
        fi
        log "START PGD-L2 ${arch} s${seed}"
        "${DEX[@]}" python scripts/c1_pgd_eval.py \
            --model-type "$arch" --dataset cifar10 --norm l2 \
            --eps "$EPS_L2" --alpha "$ALPHA_L2" --steps "$STEPS_L2" --seed 42 \
            --ckpt "models/c1/${arch}_s${seed}/${arch}/adv/adversarial_training/best.pth" \
            --out "$d" || { echo "FAIL PGD-L2 ${arch} s${seed}"; exit 1; }
    done
done

# --- 4. L2 transfer matrisi + 4 protokol (cift basina) ---
for i in 1 2 3; do
    d="${OUT}/transfer/pair${i}"
    mkdir -p "$d"
    if [ -f "$d/transfer_matrix.json" ]; then
        log "SKIP L2 transfer matrisi pair${i}"
    else
        log "START L2 transfer matrisi pair${i}"
        "${DEX[@]}" python experiments/c1_c3_transfer_matrix.py \
            --dataset cifar10 --norm l2 --n-samples "$N_PGD" --seed 42 \
            --model "ResNet18_AT:resnet18:models/c1/resnet18_s100${i}/resnet18/adv/adversarial_training/best.pth" \
            --model "ViT_Tiny_AT:vit_tiny:models/c1/vit_tiny_s200${i}/vit_tiny/adv/adversarial_training/best.pth" \
            --out-dir "$d" || { echo "FAIL L2 transfer pair${i}"; exit 1; }
    fi
    log "START L2 protokoller pair${i}"
    "${DEX[@]}" env A2_IN_DIR="$d" A2_OUT="$d/a2_transfer_protocols.json" \
        python experiments/rev2/a2_transfer_protocols.py \
        || { echo "FAIL a2 pair${i}"; exit 1; }
done

# --- 5. Toplulastirma ---
log "START toplulastirma"
"${DEX[@]}" env AGG_IN_DIR="${OUT}/transfer" AGG_OLD="" \
    AGG_OUT_NAME="e6_l2_transfer_summary.json" \
    python scripts/c1_transfer_aggregate.py \
    || { echo "FAIL toplulastirma"; exit 1; }
log "DONE -> ${OUT}/transfer/e6_l2_transfer_summary.json"

# --- 6. AutoAttack-L2 (n=5000; U2: uretilemezse ATLAMA SESSIZ OLMAZ) ---
if [ "${E6_SKIP_AA:-0}" = "1" ]; then
    log "AA-L2 ATLANDI (E6_SKIP_AA=1) -- makalede 'AA-L2 kosulmadi' diye YAZILIR (U2)"
else
    for i in 1 2 3; do
        d="${OUT}/aa_pair${i}"
        if [ -f "${d}/autoattack_results.csv" ]; then log "SKIP AA-L2 pair${i}"; continue; fi
        log "START AA-L2 pair${i} (n=${N_AA})"
        "${DEX[@]}" python experiments/run_autoattack_run2.py \
            --dataset cifar10 --norm L2 --eps "$EPS_L2" --n-samples "$N_AA" --seed 42 \
            --output-dir "$d" \
            --model "ResNet18_AT:resnet18:models/c1/resnet18_s100${i}/resnet18/adv/adversarial_training/best.pth" \
            --model "ViT_Tiny_AT:vit_tiny:models/c1/vit_tiny_s200${i}/vit_tiny/adv/adversarial_training/best.pth" \
            || { echo "UYARI: AA-L2 pair${i} basarisiz -- U2 geregi RAPOR EDILIR, sessiz dusurulmez"; }
    done
fi

# --- 7. Saglama testi U4: temiz dogruluk saldiridan BAGIMSIZ olmali ---
log "U4 saglamasi: L2 kosumundaki temiz dogruluk, L infinity kosumundakiyle ayni mi?"
"${DEX[@]}" python scripts/q1_e6_u4_check.py || echo "UYARI: U4 saglamasi kosulamadi"

log "=============== Q1-E6 TAMAM ==============="
echo
echo "HATIRLATMA (E6_ON_KAYIT.md §0): bu sayilar L-infinity ile EGITILMIS"
echo "modellerin L2 altindaki olcumleridir; L2-EGITILMIS RobustBench"
echo "girdileriyle KARSILASTIRILAMAZ."
