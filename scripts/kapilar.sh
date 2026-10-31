#!/usr/bin/env bash
# YEDI KAPI tek komutta. Her biri kendi hukmunu basar; sonda toplam.
#
#   1 verify_manuscript_numbers.py  tasiyici sayilar <-> artefaktlar (iki dil)
#   2 check_manuscript_claims.py    muhafizli iddialar + A kolu kokeni
#   3 check_abstract_body.py        oz <-> govde + ozet uzunlugu
#   4 q1_tr_decimal_check.py        TR matematik kipinde ciplak ondalik virgul
#   5 bildiri_tutarlilik.py         bildiri <-> ARTEFAKTLAR
#   6 check_en_tr_mirror.py         EN/TR yapisal ayna
#   7 gonderim_tutarlilik.py       kapak mektubu / one cikanlar / beyanlar
#                                  <-> makale basligi ve ARTEFAKTLAR
#   8 check_pdf_render.py          DERLENMIS PDF: ozet, anahtar kelimeler,
#                                  baslik, yazar bandi ve biyografi RENDER'da
#                                  var mi. (2026-09-29: ilk yedi kapi .tex
#                                  okur; ieeeaccess.cls ozeti bir ay boyunca
#                                  sessizce dusurmustu ve hepsi gecmisti.)
#                                  Sinamasi: scripts/test_pdf_render.sh
#   9 check_pdf_typeset.py         DERLENMIS PDF: govde Times mi, kalin ve
#                                  italik gomulu mu, satirlar sutun kenarini
#                                  asiyor mu, gunlukte 'T1/times undefined'
#                                  var mi. (2026-10-04: sinif 'times' ailesini
#                                  hic tanimlamiyordu; govde bir ay Computer
#                                  Modern'di, kalin/italik hic basilmadi, bes
#                                  tablo sutunu asti; sekiz kapi da gecmisti.)
#   0 test_verify_manuscript_numbers.py  ILK ADIM: sayi kapisinin oz-sinamasi (2026-10-31,
#                                  celisik dogrulayici Y3; ucuncu tur Y4). Gecici kopyada 19
#                                  sinamanin butun adaylarini bozar (isaret, takas, tek kopya,
#                                  tamsayi, A1-A3, B, KAYNAK-yalniz, GRUPSUZ, ters aralik, YON,
#                                  ozet rakam takasi, KAYNAK belgesi). Oz-sinama KALDI verirse
#                                  sayi kapisinin hukmu gecersizdir: zincir "OZ-SINAMA KALDI:
#                                  sayi kapisi hukmu gecersiz" basar ve HEMEN cikis 1 ile durur
#                                  (kalan kapilar kosulmaz).
set -u
cd "$(dirname "$0")/.." || exit 1
DEX=(docker exec -w /workspace adeb_eval python -B)

KAPILAR=(
  "test_verify_manuscript_numbers.py:oz-sinama"
  "verify_manuscript_numbers.py:sayilar"
  "check_manuscript_claims.py:iddialar"
  "check_abstract_body.py:ozet"
  "q1_tr_decimal_check.py:TR ondalik"
  "bildiri_tutarlilik.py:bildiri"
  "check_en_tr_mirror.py:EN/TR ayna"
  "gonderim_tutarlilik.py:gonderim"
  "check_pdf_render.py:PDF render"
  "check_pdf_typeset.py:PDF dizgi"
)

kalan=0
for k in "${KAPILAR[@]}"; do
    betik="${k%%:*}"; ad="${k##*:}"
    if "${DEX[@]}" "scripts/$betik" > /tmp/kapi.log 2>&1; then
        printf "%-14s GECTI   %s\n" "$ad" "$(grep -m1 'SONUC\|TEMIZ' /tmp/kapi.log | cut -c1-70)"
    else
        printf "%-14s KALDI   %s\n" "$ad" "$(grep -m1 'SONUC\|KALDI' /tmp/kapi.log | cut -c1-70)"
        kalan=$((kalan + 1))
        if [ "$betik" = "test_verify_manuscript_numbers.py" ]; then
            grep '^  KALDI' /tmp/kapi.log | cut -c1-120
            echo "OZ-SINAMA KALDI: sayi kapisi hukmu gecersiz"
            exit 1
        fi
    fi
done

echo "----------------------------------------------------------------------"
if [ "$kalan" -eq 0 ]; then
    echo "OZ-SINAMA VE DOKUZ KAPI GECTI"
else
    echo "KALAN KAPI: $kalan"
fi
exit "$kalan"
