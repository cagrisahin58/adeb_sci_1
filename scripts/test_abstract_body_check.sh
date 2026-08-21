#!/usr/bin/env bash
# check_abstract_body.py GERCEKTEN yakaliyor mu? (F1 dersi: gecen bir kontrol,
# yakaladigini kanitlamaz.) Gecici kopyada oze SAHTE bir sayi enjekte edilir.
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

cp -r paper "$TMP/paper"
cp scripts/check_abstract_body.py "$TMP/chk.py"
sed -i "s|^ROOT = .*|ROOT = Path(\"$TMP\")|" "$TMP/chk.py"
grep -n '^ROOT = ' "$TMP/chk.py"

echo
echo "=== 0) BOZULMAMIS kopya -> GECMELI ==="
python3 "$TMP/chk.py" | tail -2

echo
echo "=== 1) oze GOVDEDE OLMAYAN sayi enjekte -> KALMALI ==="
python3 - "$TMP/paper/manuscript/main.tex" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1]); t = p.read_text(encoding="utf-8")
assert "a 3.3-fold spread" in t
p.write_text(t.replace("a 3.3-fold spread",
                       "a 3.3-fold spread, with a headline value of 77.31 points", 1),
             encoding="utf-8")
PY
python3 "$TMP/chk.py" | tail -4

echo
echo "=== 2) YUVARLAMA farki (13.6 vs 13.58) -> yanlis alarm VERMEMELI ==="
python3 - "$TMP/paper/manuscript/main.tex" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1]); t = p.read_text(encoding="utf-8")
p.write_text(t.replace(", with a headline value of 77.31 points", "", 1), encoding="utf-8")
PY
python3 "$TMP/chk.py" | tail -2
echo
echo "NOT: gercek depoya DOKUNULMADI."
