#!/usr/bin/env bash
# MUHAFIZ SINAMASI: bildiri denetimi gercekten YAKALIYOR mu?
# Hic kalmamis bir muhafiz degersizdir. Yontem: gecici kopyada BOZ,
# denetimi kopyada kos, KALDI demesini bekle.
#
# UC KOL:
#   metin kolu    (1-3) : bildiriyi boz  -> MANUSCRIPT_ROOT
#   artefakt kolu (4-5) : artefakti boz  -> GATE_ROOT
# Artefakt kolu 2026-08-25'te eklendi: o gune kadar otoriter degerler betige
# SABIT yaziliydi, yani kapi korudugu sayinin kopyasini tasiyordu ve artefakt
# degistiginde kaymayi goremiyordu (olculdu: ust sinir 14,60 -> 19,37 oldu,
# kapi yine GECTI dedi). Eski oz-sinama bunu YAKALAYAMAZDI cunku yalniz
# bildiriyi bozuyordu.
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
cp -r paper "$TMP/paper"
B="$TMP/paper/bildiri/bildiri.tex"

echo "=== 0) BOZULMAMIS kopya -> GECMELI ==="
MANUSCRIPT_ROOT="$TMP" python3 scripts/bildiri_tutarlilik.py 2>&1 | tail -2

echo
echo "=== 1) ESKIMIS sayi: AutoAttack 37,93 -> 36,0 (run2 karantina degeri) ==="
sed -i 's/37\.93\$\\pm\$0\.14/36.00$\\pm$0.14/' "$B"
MANUSCRIPT_ROOT="$TMP" python3 scripts/bildiri_tutarlilik.py 2>&1 | grep -E "AA ResNet|SONUC"
sed -i 's/36\.00\$\\pm\$0\.14/37.93$\\pm$0.14/' "$B"

echo
echo "=== 2) YUVARLAMA farki: Hoyer 0,493 -> 0,4928 -> yanlis alarm VERMEMELI ==="
sed -i 's/Hoyer 0\.493/Hoyer 0.4928/' "$B"
MANUSCRIPT_ROOT="$TMP" python3 scripts/bildiri_tutarlilik.py 2>&1 | grep -E "SONUC"
sed -i 's/Hoyer 0\.4928/Hoyer 0.493/' "$B"

echo
echo "=== 3) SINIRLAMA cumlesi silinsin, yon iddiasi kalsin -> KALMALI ==="
sed -i 's/preliminary results on one dataset and one model pair/results on our data/' "$B"
MANUSCRIPT_ROOT="$TMP" python3 scripts/bildiri_tutarlilik.py 2>&1 | grep -E "tek veri kumesi|SONUC"
sed -i 's/results on our data/preliminary results on one dataset and one model pair/' "$B"

# --------------------------------------------------------------------------
# ARTEFAKT KOLU: bildiri DOGRU, artefakt kayiyor. Kapi bunu gormek zorunda.
# --------------------------------------------------------------------------
ART="$TMP/artefakt"
mkdir -p "$ART/results/c1_seeds" "$ART/results/c1_transfer"
cp results/c1_seeds/c1_seed_summary.json     "$ART/results/c1_seeds/"
cp results/c1_transfer/c1_transfer_summary.json "$ART/results/c1_transfer/"
cp results/c1_behavior_summary.json          "$ART/results/"

echo
echo "=== 4) ARTEFAKT kaydi: basarili-kaynak farki +19,37 -> +14,60 (eski gevsek deger) ==="
python3 - "$ART" <<'PY'
import json, sys
from pathlib import Path
f = Path(sys.argv[1]) / "results/c1_transfer/c1_transfer_summary.json"
d = json.loads(f.read_text(encoding="utf-8"))
d["protocols"]["successful_source"]["diff"]["mean"] = 14.60
f.write_text(json.dumps(d, indent=1), encoding="utf-8")
PY
GATE_ROOT="$ART" MANUSCRIPT_ROOT="." python3 scripts/bildiri_tutarlilik.py 2>&1 \
    | grep -E "protokol ust sinir|protokol kat|SONUC"
cp results/c1_transfer/c1_transfer_summary.json "$ART/results/c1_transfer/"

echo
echo "=== 5) ARTEFAKT kaydi: AutoAttack ResNet 37,93 -> 36,00 ==="
python3 - "$ART" <<'PY'
import json, sys
from pathlib import Path
f = Path(sys.argv[1]) / "results/c1_seeds/c1_seed_summary.json"
d = json.loads(f.read_text(encoding="utf-8"))
d["aggregate"]["resnet"]["aa"]["mean"] = 36.00
f.write_text(json.dumps(d, indent=1), encoding="utf-8")
PY
GATE_ROOT="$ART" MANUSCRIPT_ROOT="." python3 scripts/bildiri_tutarlilik.py 2>&1 \
    | grep -E "AA ResNet|SONUC"

echo
echo "=== 6) EKSIK artefakt -> SESSIZ GECMEMELI ==="
rm -f "$ART/results/c1_behavior_summary.json"
GATE_ROOT="$ART" MANUSCRIPT_ROOT="." python3 scripts/bildiri_tutarlilik.py 2>&1 | tail -1

echo
echo "NOT: gercek depoya DOKUNULMADI; tum degisiklikler gecici kopyada."
