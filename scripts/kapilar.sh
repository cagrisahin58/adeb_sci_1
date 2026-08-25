#!/usr/bin/env bash
# ALTI KAPI tek komutta. Her biri kendi hukmunu basar; sonda toplam.
#
#   1 verify_manuscript_numbers.py  tasiyici sayilar <-> artefaktlar (iki dil)
#   2 check_manuscript_claims.py    muhafizli iddialar + A kolu kokeni
#   3 check_abstract_body.py        oz <-> govde + ozet uzunlugu
#   4 q1_tr_decimal_check.py        TR matematik kipinde ciplak ondalik virgul
#   5 bildiri_tutarlilik.py         bildiri <-> ARTEFAKTLAR
#   6 check_en_tr_mirror.py         EN/TR yapisal ayna
set -u
cd "$(dirname "$0")/.." || exit 1
DEX=(docker exec -w /workspace adeb_eval python)

KAPILAR=(
  "verify_manuscript_numbers.py:sayilar"
  "check_manuscript_claims.py:iddialar"
  "check_abstract_body.py:ozet"
  "q1_tr_decimal_check.py:TR ondalik"
  "bildiri_tutarlilik.py:bildiri"
  "check_en_tr_mirror.py:EN/TR ayna"
)

kalan=0
for k in "${KAPILAR[@]}"; do
    betik="${k%%:*}"; ad="${k##*:}"
    if "${DEX[@]}" "scripts/$betik" > /tmp/kapi.log 2>&1; then
        printf "%-14s GECTI   %s\n" "$ad" "$(grep -m1 'SONUC\|TEMIZ' /tmp/kapi.log | cut -c1-70)"
    else
        printf "%-14s KALDI   %s\n" "$ad" "$(grep -m1 'SONUC\|KALDI' /tmp/kapi.log | cut -c1-70)"
        kalan=$((kalan + 1))
    fi
done

echo "----------------------------------------------------------------------"
if [ "$kalan" -eq 0 ]; then
    echo "ALTI KAPI DA GECTI"
else
    echo "KALAN KAPI: $kalan"
fi
exit "$kalan"
