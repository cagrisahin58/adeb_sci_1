#!/usr/bin/env bash
# A kolunu B2 duzeltmeleriyle yeniden kosar -> results/q1/e3_akolu_v2
#
# Iki duzeltme birden tasinir:
#   (1) successful_source artik SIKI tanim (beyaz kutu basarisi),
#   (2) her kontrol noktasi (yorunge, epok)'a bagli KENDI tohumunu alir.
# Gevsek varyant da kaydedilir (gerileme kontrolu icin).
#
# Kapsayicida ara sira UCX teardown segfault'u goruluyor; surucu mevcut
# dosyalari atladigi icin tekrar kosmak kaldigi yerden devam eder.
set -u
cd "$(dirname "$0")/.." || exit 1
OUT=results/q1/e3_akolu_v2

for deneme in 1 2 3 4; do
    echo "=== DENEME $deneme ==="
    E3A_OUT="$OUT" bash scripts/q1_e3_akolu_run.sh 10
    n=$(ls "$OUT"/*.json 2>/dev/null | wc -l)
    echo "=== deneme $deneme sonunda nokta: $n ==="
    if [ "$n" -ge 116 ]; then
        echo "TAMAM: $n nokta"
        exit 0
    fi
done
echo "UYARI: 4 denemeden sonra hala eksik ($n / 116)"
