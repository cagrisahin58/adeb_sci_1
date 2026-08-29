#!/usr/bin/env bash
# BIR SAYFA dusurmek icin ne kadar metin cikarmak gerekiyor? Deneyle olcer.
# Gecici bir kopyada Bolum 4'un sonundan N kelime cikarip derler.
# GERCEK DEPOYA DOKUNMAZ.
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
cp -r paper/manuscript "$T/m"
cp -r paper/figures "$T/figures"

olc() {  # $1 = cikarilacak kelime sayisi
    rm -rf "$T/deneme"
    cp -r "$T/m" "$T/deneme"
    python3 - "$T/deneme/sections/04_experiments.tex" "$1" <<'PY'
import pathlib
import sys
p = pathlib.Path(sys.argv[1])
hedef = int(sys.argv[2])
satirlar = p.read_text(encoding="utf-8").splitlines()
kalan = hedef
for i in range(len(satirlar) - 1, -1, -1):
    s = satirlar[i].strip()
    if len(s) < 200 or s.startswith(("\\", "%")):
        continue
    k = s.split()
    if len(k) <= kalan:
        kalan -= len(k)
        satirlar[i] = "% (deney: kaldirildi)"
    else:
        satirlar[i] = " ".join(k[:len(k) - kalan])
        kalan = 0
    if kalan <= 0:
        break
p.write_text("\n".join(satirlar), encoding="utf-8")
PY
    (cd "$T/deneme" && latexmk -pdf -interaction=nonstopmode main.tex > /dev/null 2>&1)
    n=$(grep -o 'Output written on.*(\([0-9]*\) pages' "$T/deneme/main.log" \
        | grep -o '([0-9]* pages' | grep -o '[0-9]*')
    echo "  cikarilan ${1} kelime -> ${n} sayfa"
}

echo "=== SAYFA DENEYI ==="
for n in 40 80 120; do
    olc "$n"
done
