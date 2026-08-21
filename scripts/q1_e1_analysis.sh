#!/usr/bin/env bash
# Q1 transfer analiz zinciri — E1 (CIFAR-100) ve E7 (SVHN) icin ORTAK.
#
# NEDEN AYRI BETIK: q1_pipeline.sh yalniz egitim + PGD degerlendirmesi kosar;
# transfer matrisi ve protokol analizi pipeline'da YOKTUR. Ara denetim bunu
# "unutulma riski gercek" olarak isaretledi. Bu betik zinciri tek komuta indirir.
#
# Kosum:
#   bash scripts/q1_e1_analysis.sh                      # varsayilan: cifar100, 3 cift
#   bash scripts/q1_e1_analysis.sh --dataset svhn       # E7-kisa: svhn, 2 cift
#   PAIRS="1" bash scripts/q1_e1_analysis.sh            # tek cift
#
# Uretilenler (DS = veri kumesi):
#   results/q1/${DS}/transfer/pairN/per_sample_*.npz + transfer_matrix.json
#   results/q1/${DS}/transfer/pairN/a2_transfer_protocols.json
#   results/q1/${DS}/transfer/pairN/a2b_class_balance_${DS}.json
#   results/q1/${DS}/transfer/${SUMMARY_NAME}            (tohum toplulastirmasi)
set -u

cd "$(dirname "$0")/.." || exit 1

# --- veri kumesi parametresi (eskiden DS=cifar100 SABITTI) ---
DS="${DS:-cifar100}"
while [ $# -gt 0 ]; do
    case "$1" in
        --dataset) DS="$2"; shift 2 ;;
        --dataset=*) DS="${1#*=}"; shift ;;
        *) echo "Bilinmeyen arguman: $1"; exit 1 ;;
    esac
done

# Rapor basligi/dosya adi da veri kumesine gore: CIFAR-100 ciktisi "C1"
# basligiyla ureiliyordu ve KARANTINA kurali acisindan karistirma riskiydi.
case "$DS" in
    cifar100)
        DEF_PAIRS="1 2 3"; DEF_SUMMARY="e1_transfer_summary.json"
        DEF_TITLE="E1 Transfer Protokolleri - CIFAR-100, 3 Tohum"
        DEF_MD="E1_TRANSFER_RAPORU.md"
        DEF_DESC="Ayni istatistik kodu (a2_transfer_protocols.py), E1 (CIFAR-100) kontrol noktalarina uygulandi. Her satir 3 tohum ortalamasi +- std." ;;
    svhn)
        DEF_PAIRS="1 2";   DEF_SUMMARY="e7_transfer_summary.json"
        DEF_TITLE="E7 Transfer Protokolleri - SVHN, 2 Tohum"
        DEF_MD="E7_TRANSFER_RAPORU.md"
        DEF_DESC="Ayni istatistik kodu (a2_transfer_protocols.py), E7 (SVHN, kisa surum) kontrol noktalarina uygulandi. Her satir 2 tohum ortalamasi +- std. UCUNCU MIMARI YOKTUR (2x2 matris)." ;;
    cifar10)
        DEF_PAIRS="1 2 3"; DEF_SUMMARY="c1_transfer_summary.json"
        DEF_TITLE="C1 Transfer Protokolleri - 3 Tohum"
        DEF_MD="C1_TRANSFER_RAPORU.md"
        DEF_DESC="Ayni istatistik kodu (a2_transfer_protocols.py), C1 sizinti-duzeltmeli kontrol noktalarina uygulandi. Her satir 3 tohum ortalamasi +- std." ;;
    *) echo "HATA: desteklenmeyen veri kumesi '$DS' (cifar10|cifar100|svhn)"; exit 1 ;;
esac

PAIRS="${PAIRS:-$DEF_PAIRS}"
SUMMARY_NAME="${SUMMARY_NAME:-$DEF_SUMMARY}"
OUT_ROOT="results/q1/${DS}/transfer"
DEX=(docker exec -w /workspace adeb_eval)

log() { echo "[$(date '+%F %T')] $*"; }

# --- Tam test kumesi: veri kumesinden OKUNUR, sabitlenmez ---
# CIFAR 10.000 iken SVHN 26.032'dir. Sabit 10.000 kullanmak SVHN'de sessizce
# test kumesinin %38'ini kullanmak olurdu; makalenin "tam test kumesi" iddiasi
# uc veri kumesinde de gecerli kalmali.
N_SAMPLES="$("${DEX[@]}" python -c "from src.data.datasets import DATASETS; print(DATASETS['${DS}']['n_test'])" 2>/dev/null | tr -d '\r')"
case "$N_SAMPLES" in
    ''|*[!0-9]*) echo "HATA: ${DS} icin n_test okunamadi ('${N_SAMPLES}')"; exit 1 ;;
esac
log "Veri kumesi=${DS}  ciftler='${PAIRS}'  tam test kumesi=${N_SAMPLES}"

# --- 0. On kontrol: ilgili KOSUMLAR BITMIS mi? ---
# DIKKAT: best.pth varligina BAKILMAZ -- egitim suruyorken de best.pth vardir
# (ilk epoktan itibaren yazilir) ve yari egitilmis modelle analiz kosmak sessiz
# bir bilim hatasidir. Bitmisligin kaniti pgd_summary_*.json'dur: o dosya yalniz
# egitim tamamlanip PGD degerlendirmesi kosunca uretilir. (K6)
missing=0
for i in $PAIRS; do
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
    echo "HATA: ${DS} kosumlari bitmemis. Once q1_pipeline.sh tamamlansin."
    echo "      (best.pth VARLIGI bitmislik kaniti DEGILDIR -- egitim sirasinda da vardir.)"
    exit 1
fi

# --- 0b. Referans (ucuncu) mimari: VAR MI, YOK MU -- SESSIZ GECILMEZ ---
# c1_c3_transfer_matrix.py yalniz cifar10/cifar100'de RobustBench referansini
# OTOMATIK ekler (has_rb kurali). SVHN'de eklemez; matris 2x2 cikar.
# Bu, E7-KISA icin KUSUR DEGIL, ON-KAYITLI TASARIMDIR:
#   Q1_ARASTIRMA_RAPORU §E7 -> "Kisa surum: 2 mimari x 2 tohum ... ~11 sa"
#   (referans yalniz TAM surumde: "+ DenseNet-121 referans ~5-6 sa")
# Ama fark SESSIZ kalmamalidir: 2x2 matris veri-kumesi-ICI karistirici
# korelasyonunu (B.4 madde 3) KURAMAZ; SVHN'in E3'e katkisi yorunge
# checkpointleri ve iki dusuk-hata capasidir. Ekrana ve JSON'a yazilir.
case "$DS" in
    cifar10|cifar100) REF_DURUM="otomatik-robustbench (3x3)" ;;
    *)                REF_DURUM="YOK (2x2)" ;;
esac
if [ "$REF_DURUM" = "YOK (2x2)" ]; then
    echo
    echo "UYARI -- UCUNCU MIMARI YOK: ${DS} icin transfer matrisi 2x2'dir."
    echo "  Ne kaybediliyor: veri-kumesi-ICI 'ham-kosullu sapma ~ hedefin temiz"
    echo "  hatasi' korelasyonu (iki nokta uzerinden kurulamaz)."
    echo "  Ne korunuyor  : 4 protokol yayilimi, sinif bilesimi kontrolu ve"
    echo "  E3 icin dusuk-hata capalari (yorunge checkpointleri + iki hedef)."
    echo "  Bu, K-01'de onaylanan KISA surumun tasarimidir; referans istenirse"
    echo "  --model ile ELLE verilmelidir (ek egitim maliyeti ~5-6 GPU-saat)."
    echo
fi

# --- 1. CUDA sert kontrolu (C1'de sessiz CPU dususu yasandi) ---
if ! "${DEX[@]}" python -c "import torch,sys; sys.exit(0 if torch.cuda.is_available() else 1)"; then
    echo "HATA: CUDA yok. Sessiz CPU dususune izin verilmiyor."
    exit 1
fi

for i in $PAIRS; do
    d="${OUT_ROOT}/pair${i}"
    mkdir -p "$d"

    # --- 2. Transfer matrisi (ornek-bazli maskeler) ---
    # Model adlari a2/a2b betiklerinin bekledigi adlarla AYNI olmak ZORUNDA.
    if [ -f "$d/transfer_matrix.json" ]; then
        log "SKIP transfer matrisi pair${i} (zaten var)"
    else
        log "START transfer matrisi pair${i} (n=${N_SAMPLES})"
        "${DEX[@]}" python experiments/c1_c3_transfer_matrix.py \
            --dataset "$DS" --n-samples "$N_SAMPLES" --seed 42 \
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

    # --- 4. Sinif bilesimi kontrolu (E7 icin yazildi; her veri kumesinde kosulur) ---
    # SVHN DENGESIZDIR (sinif paylari 0,0636-0,1892; dengesizlik 2,98x).
    # CIFAR'da bilesim etkisi asimetrinin %1-19'u cikti; SVHN'de BUYUMESI
    # beklenir ve buyurse RAPORLANIR (K8).
    log "START sinif bilesimi pair${i}"
    "${DEX[@]}" env A2B_IN_DIR="$d" A2B_DATASET="$DS" \
        A2B_OUT="$d/a2b_class_balance_${DS}.json" \
        python experiments/rev2/a2b_class_balance.py \
        || { echo "FAIL a2b pair${i}"; exit 1; }
    log "DONE pair${i}"
done

# --- 5. Tohum toplulastirma (C1 ile AYNI kod, yalniz girdi koku farkli) ---
if [ "$PAIRS" = "$DEF_PAIRS" ]; then
    log "START toplulastirma"
    "${DEX[@]}" env AGG_IN_DIR="$OUT_ROOT" AGG_OLD="" \
        AGG_OUT_NAME="$SUMMARY_NAME" \
        AGG_TITLE="$DEF_TITLE" AGG_MD_NAME="$DEF_MD" AGG_DESC="$DEF_DESC" \
        AGG_PAIRS="$PAIRS" \
        python scripts/c1_transfer_aggregate.py \
        || { echo "FAIL toplulastirma"; exit 1; }
    log "DONE toplulastirma -> ${OUT_ROOT}/${SUMMARY_NAME}"

    # --- 6. On-kestirim sinamasi: YALNIZ on-kayitli veri kumesinde ---
    # K5: veri gorulduk ten sonra YENI esik kurulmaz. B.4 madde 1 yalniz
    # CIFAR-100 icin on-kayitlidir; SVHN icin boyle bir on-kestirim YOKTUR,
    # bu yuzden SVHN'de yayilim yalnizca RAPOR EDILIR, hukum verilmez.
    if [ "$DS" = "cifar100" ]; then
        echo
        echo "=== B.4 madde 1 ON-KESTIRIM SINAMASI ==="
        echo "On-kayit: CIFAR-100 protokol yayilimi CIFAR-10'un 10,45 puanindan BUYUK olmali."
        "${DEX[@]}" python -c "
import json
d = json.load(open('${OUT_ROOT}/${SUMMARY_NAME}'))
s = d.get('protocol_spread_pp', {})
print('CIFAR-100 yayilim :', s)
m = s.get('mean')
if m is None:
    print('HUKUM: yayilim alani yok, elle kontrol gerek')
else:
    print('CIFAR-10 referans : 10.45')
    print('HUKUM:', 'ON-KESTIRIM DOGRULANDI' if m > 10.45 else 'ON-KESTIRIM KARSILANMADI -> E1 tezi desteklemiyor olarak raporlanir (B.4)')
"
    else
        echo
        echo "=== ${DS^^} PROTOKOL YAYILIMI (on-kestirim YOK, yalniz rapor) ==="
        echo "K5: veri gorulduk ten sonra esik kurulmaz; asagidaki sayi hukumsuz raporlanir."
        "${DEX[@]}" python -c "
import json
d = json.load(open('${OUT_ROOT}/${SUMMARY_NAME}'))
print('${DS} yayilim :', d.get('protocol_spread_pp', {}))
print('karsilastirma icin: CIFAR-10 = 10.45 · CIFAR-100 = 13.58 (hukum YOK)')
"
    fi
fi

echo
echo "=== UCUNCU MIMARI DURUMU: ${REF_DURUM} ==="
if [ "$REF_DURUM" = "YOK (2x2)" ]; then
    echo "${DS} icin veri-kumesi-ICI karistirici korelasyonu (B.4 madde 3)"
    echo "KURULAMAZ. Bu, K-01 kisa surum tasariminin bilinen ve KABUL EDILEN"
    echo "sinirlamasidir; makaleye boyle yazilir."
else
    echo "c1_c3_transfer_matrix.py RobustBench referansini otomatik ekledi."
    echo "Ilk kosumda indirme olur; kesilirse .part dosyasi kalir ve SILINMELIDIR"
    echo "(models/robustbench_zoo/${DS}/Linf/*.part)."
fi
