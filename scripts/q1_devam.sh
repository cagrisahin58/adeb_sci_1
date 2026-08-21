#!/usr/bin/env bash
# Q1 — GPU BOSALINCA KALAN HER SEYI SIRAYLA KOSAR.
#
# Kullanim (GPU bosken):
#     bash scripts/q1_devam.sh
# Tek asama:
#     bash scripts/q1_devam.sh e7        # (e7 | e7analiz | e3 | e6 | b8)
#
# Her asama IDEMPOTENTTIR: bitmis is atlanir, yarim kalan --resume ile surer.
# Kesilirse ayni komut kaldigi yerden devam eder.
#
# SIRA GEREKCESI:
#   e7      -> E3'un x ekseninde OLCULEN dusuk-hata boslugunu dolduran tek is
#   e7analiz-> E7'nin protokol/bilesim ciktilarini uretir
#   e3      -> tezin omurgasi; E7 noktalari A koluna girsin diye E7'den SONRA
#   e6      -> L2 tehdit modeli (bagimsiz, en sona alinabilir)
#   b8      -> CIFAR-100 secim bandini VEKIL yerine GERCEK TEST uzerinde olcer
set -u
cd "$(dirname "$0")/.." || exit 1
ASAMA="${1:-hepsi}"
log() { echo "[$(date '+%F %T')] === $* ==="; }

gpu_bos_mu() {
    local kullanilan
    kullanilan=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1)
    [ -z "$kullanilan" ] && { echo "UYARI: nvidia-smi okunamadi"; return 0; }
    echo "  GPU kullanimi: ${kullanilan} MiB"
    if [ "$kullanilan" -gt 20000 ]; then
        echo "  UYARI: GPU'da 20 GB'tan fazla dolu. Baska bir proje kosuyor olabilir."
        echo "  Yine de devam etmek icin: Q1_DEVAM_ZORLA=1"
        [ "${Q1_DEVAM_ZORLA:-0}" = "1" ] || return 1
    fi
    return 0
}

kos_e7() {
    log "E7 (SVHN) -- kaldigi yerden"
    # KOSELI PARANTEZ HILESI: duz 'q1_pipeline.sh' deseni pgrep'in KENDI
    # sarmalayicisini de eslestirir (bash -lc komut satirinda desen geciyor) ve
    # muhafiz HER ZAMAN "kosuyor" der -- E7 hic baslamazdi.
    if docker exec adeb_eval bash -lc 'pgrep -f "[q]1_pipeline.sh" >/dev/null'; then
        echo "  ZATEN KOSUYOR, yeni kosum baslatilmadi."
        return 0
    fi
    local bitmis
    bitmis=$(find models/q1/svhn -name TRAINING_COMPLETE 2>/dev/null | wc -l)
    echo "  bitmis egitim: ${bitmis}/8 (atlanacaklar)"
    # E7_FULL VERILMEZ (K-01 kisa surum) · --stratified EKLENMEZ (SVHN dengesiz)
    docker exec -d -e STAGE=e7 -w /workspace adeb_eval bash scripts/q1_pipeline.sh
    echo "  arka planda baslatildi. Izleme:  tail -f logs/q1_e7.log"
    echo "  BITTI isareti: logs/q1_e7.log icinde 'Q1-E7 TAMAM'"
}

kos_e7analiz() {
    log "E7 analiz zinciri (SVHN)"
    if ! grep -q 'Q1-E7 TAMAM' logs/q1_e7.log 2>/dev/null; then
        echo "  ATLANDI: E7 henuz bitmemis (logs/q1_e7.log icinde 'Q1-E7 TAMAM' yok)."
        echo "  (K6: best.pth varligi bitmislik kaniti DEGILDIR.)"
        return 1
    fi
    bash scripts/q1_e1_analysis.sh --dataset svhn
}

kos_e3() {
    log "E3 -- A kolu (B kolu zaten kosuldu)"
    bash scripts/q1_e3_run.sh
}

kos_e6() {
    log "E6 -- L2 tehdit modeli"
    bash scripts/q1_e6_l2.sh
}

kos_b8() {
    log "B.8 -- CIFAR-100 test egrisi (secim bandi GERCEK test uzerinde)"
    docker exec -w /workspace adeb_eval python -B scripts/q1_e2_test_curve.py \
        --dataset cifar100
}

if ! gpu_bos_mu; then
    echo "DURDURULDU: GPU mesgul."
    exit 1
fi

case "$ASAMA" in
    e7)        kos_e7 ;;
    e7analiz)  kos_e7analiz ;;
    e3)        kos_e3 ;;
    e6)        kos_e6 ;;
    b8)        kos_b8 ;;
    hepsi)
        # E7 arka planda kostugu icin zincirin kalani ONUN BITMESINI bekler;
        # bu yuzden "hepsi" E7'yi baslatir ve DURUR. E7 bitince tekrar cagirin.
        kos_e7
        echo
        echo "E7 arka planda kosuyor. Bittiginde (logs/q1_e7.log -> 'Q1-E7 TAMAM'):"
        echo "    bash scripts/q1_devam.sh e7analiz"
        echo "    bash scripts/q1_devam.sh e3"
        echo "    bash scripts/q1_devam.sh e6"
        echo "    bash scripts/q1_devam.sh b8"
        ;;
    *) echo "Bilinmeyen asama: $ASAMA (e7|e7analiz|e3|e6|b8|hepsi)"; exit 1 ;;
esac
