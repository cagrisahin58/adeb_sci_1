#!/usr/bin/env bash
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
cp -r paper "$TMP/paper"
cp scripts/check_abstract_body.py "$TMP/chk.py"
sed -i "s|^ROOT = .*|ROOT = Path(\"$TMP\")|" "$TMP/chk.py"

python3 - "$TMP/paper/manuscript/main.tex" <<'PY'
import pathlib
import re
import sys
p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", t, re.S)
govde = m.group(1)
t = t[:m.start(1)] + govde + " " + govde.strip() + t[m.end(1):]
p.write_text(t, encoding="utf-8")
PY

echo "===== KAPI TAM CIKTISI ====="
python3 "$TMP/chk.py"
