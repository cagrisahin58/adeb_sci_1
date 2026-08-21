#!/usr/bin/env bash
# MUHAFIZ SINAMASI: bildiri denetimi gercekten YAKALIYOR mu?
# Hic kalmamis bir muhafiz degersizdir. Yontem: gecici kopyada bildiriyi
# BOZ, denetimi kopyada kos, KALDI demesini bekle.
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
cp -r paper "$TMP/paper"
export MANUSCRIPT_ROOT="$TMP"
B="$TMP/paper/bildiri/bildiri.tex"

echo "=== 0) BOZULMAMIS kopya -> GECMELI ==="
python3 scripts/bildiri_tutarlilik.py 2>&1 | tail -2

echo
echo "=== 1) ESKIMIS sayi: AutoAttack 37,93 -> 36,0 (run2 karantina degeri) ==="
sed -i 's/37\.93\$\\pm\$0\.14/36.00$\\pm$0.14/' "$B"
python3 scripts/bildiri_tutarlilik.py 2>&1 | grep -E "AA ResNet|SONUC"
sed -i 's/36\.00\$\\pm\$0\.14/37.93$\\pm$0.14/' "$B"

echo
echo "=== 2) YUVARLAMA farki: Hoyer 0,493 -> 0,4928 -> yanlis alarm VERMEMELI ==="
sed -i 's/Hoyer 0\.493/Hoyer 0.4928/' "$B"
python3 scripts/bildiri_tutarlilik.py 2>&1 | grep -E "SONUC"
sed -i 's/Hoyer 0\.4928/Hoyer 0.493/' "$B"

echo
echo "=== 3) SINIRLAMA cumlesi silinsin, yon iddiasi kalsin -> KALMALI ==="
sed -i 's/preliminary results on one dataset and one model pair/results on our data/' "$B"
python3 scripts/bildiri_tutarlilik.py 2>&1 | grep -E "tek veri kumesi|SONUC"

echo
echo "NOT: gercek depoya DOKUNULMADI; tum degisiklikler gecici kopyada."
