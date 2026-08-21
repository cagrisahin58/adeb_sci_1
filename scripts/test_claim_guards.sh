#!/usr/bin/env bash
# MUHAFIZ SINAMASI: yeni E/F kontrolleri gercekten YAKALIYOR mu?
# Bir muhafiz, kirilmis metinde de GECTI diyorsa DEGERSIZDIR.
# Yontem: makaleyi gecici bir kopyaya al, iddiayi BOZ, denetimi kopyada kos.
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

cp -r paper "$TMP/paper"
cp scripts/check_manuscript_claims.py "$TMP/chk.py"
# Denetleyicinin koku gecici kopyaya baksin. Kaynak satirini sed ile yamamak
# kirilgandi (satir bicimi degisince sessizce islemez oluyordu); denetleyici
# artik bu degiskeni kendisi okuyor.
export MANUSCRIPT_ROOT="$TMP"
echo "MANUSCRIPT_ROOT=$MANUSCRIPT_ROOT"

echo
echo "=== 0) BOZULMAMIS kopya (hepsi GECMELI) ==="
python3 "$TMP/chk.py" 2>&1 | tail -2

echo
echo "=== 1) 'incomplete' silinsin -> F2 EN KALMALI ==="
sed -i 's/That account is incomplete/That account is fine/' "$TMP/paper/manuscript/sections/05_discussion.tex"
python3 "$TMP/chk.py" 2>&1 | grep -E 'F2. EN|TOPLAM'

echo
echo "=== 2) ozdeslik denklem etiketi silinsin -> E1 EN KALMALI ==="
sed -i 's/eq:raw_identity/eq:silindi/g' "$TMP/paper/manuscript/sections/04_experiments.tex"
python3 "$TMP/chk.py" 2>&1 | grep -E 'E1. EN|TOPLAM'

echo
echo "=== 3) ESKI korelasyon dili GERI GELSIN -> E3 EN KALMALI ==="
python3 - "$TMP/paper/manuscript/sections/04_experiments.tex" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text(encoding="utf-8")
t += ("\n\nThe deviation is almost perfectly explained by the clean error "
      "of the target.\n")
p.write_text(t, encoding="utf-8")
PY
python3 "$TMP/chk.py" 2>&1 | grep -E 'E3. EN|TOPLAM'

echo
echo "=== 4) ikinci surucu anilmasin -> F1 EN KALMALI ==="
sed -i 's/second and partly/quite another and partly/' "$TMP/paper/manuscript/sections/04_experiments.tex"
sed -i 's/adds a second driver/adds another effect/' "$TMP/paper/manuscript/sections/05_discussion.tex"
python3 "$TMP/chk.py" 2>&1 | grep -E 'F1. EN|TOPLAM'


echo
echo "=== 5) BAYAT KAPSAM geri gelsin -> G1/G2 EN KALMALI ==="
sed -i "s/covers three datasets and a single model pair/covers one dataset and one model pair/" \
  "$TMP/paper/manuscript/sections/06_conclusion.tex"
python3 "$TMP/chk.py" 2>&1 | grep -E "G1. EN|G2. EN|TOPLAM"
echo
echo "NOT: gercek depoya DOKUNULMADI; tum degisiklikler gecici kopyada."
