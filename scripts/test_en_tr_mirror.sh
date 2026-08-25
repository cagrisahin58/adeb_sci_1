#!/usr/bin/env bash
# MUHAFIZ SINAMASI: ayna kapisi gercekten YAKALIYOR mu?
# Hic kalmamis bir muhafiz degersizdir. Gecici kopyada bir dilden ogeler
# silinir, kapinin KALDIGI dogrulanir.
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
cp -r paper "$TMP/paper"
export MANUSCRIPT_ROOT="$TMP"
TRD="$TMP/paper/manuscript_tr/sections"
END="$TMP/paper/manuscript/sections"

echo "=== 0) BOZULMAMIS kopya -> GECMELI ==="
python3 scripts/check_en_tr_mirror.py | tail -2

echo
echo "=== 1) TR'den bir DENKLEM silinsin -> KALMALI ==="
python3 - "$TRD/03_yontem.tex" <<'PY'
import pathlib
import re
import sys
p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
yeni, n = re.subn(r"\\begin\{equation\}.*?\\end\{equation\}\n", "", t, count=1, flags=re.S)
if n != 1:
    sys.exit("SINAMA HATASI: denklem silinemedi -- kol KOSULMADI")
p.write_text(yeni, encoding="utf-8")
PY
python3 scripts/check_en_tr_mirror.py | grep -E "denklem.*AYRISMA|SONUC" | head -3
cp paper/manuscript_tr/sections/03_yontem.tex "$TRD/03_yontem.tex"

echo
echo "=== 2) EN'den bir PARAGRAF silinsin -> KALMALI ==="
python3 - "$END/05_discussion.tex" <<'PY'
import pathlib
import sys
p = pathlib.Path(sys.argv[1])
satirlar = p.read_text(encoding="utf-8").split("\n")
for i, s in enumerate(satirlar):
    if len(s.strip()) > 200 and not s.strip().startswith("\\") and not s.strip().startswith("%"):
        del satirlar[i]
        break
else:
    sys.exit("SINAMA HATASI: paragraf bulunamadi -- kol KOSULMADI")
p.write_text("\n".join(satirlar), encoding="utf-8")
PY
python3 scripts/check_en_tr_mirror.py | grep -E "paragraf.*AYRISMA|SONUC" | head -3
cp paper/manuscript/sections/05_discussion.tex "$END/05_discussion.tex"

echo
echo "=== 3) TR'den bir AD OBEGI basligi silinsin -> KALMALI ==="
sed -i '0,/\\paragraph{/{s/\\paragraph{/% silindi {/}' "$TRD/04_deneyler.tex" 2>/dev/null || true
python3 - "$TRD/03_yontem.tex" <<'PY'
import pathlib
import sys
p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
if "\\paragraph{" not in t:
    sys.exit("SINAMA HATASI: ad obegi yok -- kol KOSULMADI")
p.write_text(t.replace("\\paragraph{", "% KALDIRILDI{", 1), encoding="utf-8")
PY
python3 scripts/check_en_tr_mirror.py | grep -E "ad obegi.*AYRISMA|SONUC" | head -3

echo
echo "=== 4) EKSIK dosya -> SESSIZ GECMEMELI ==="
rm -f "$TRD/06_sonuc.tex"
python3 scripts/check_en_tr_mirror.py 2>&1 | tail -1

echo
echo "NOT: gercek depoya DOKUNULMADI; tum degisiklikler gecici kopyada."
