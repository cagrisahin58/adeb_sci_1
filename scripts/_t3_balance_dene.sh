#!/usr/bin/env bash
# \balance'in sayfa sayisina etkisini GECICI kopyada olcer. Depoya dokunmaz.
set -u
cd /home/firat/projects/adeb_sci_1/paper || exit 1
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
cp -r manuscript "$T/m"; cp -r figures "$T/figures"

olc() {
    (cd "$T/m" && latexmk -pdf -interaction=nonstopmode main.tex >/dev/null 2>&1)
    grep -o 'Output written on.*([0-9]* pages' "$T/m/main.log" | tail -1 \
        | grep -o '[0-9]* pages'
}

echo -n "  \\balance VAR   : "; olc
sed -i 's/^\\balance$/%\\balance/' "$T/m/main.tex"
(cd "$T/m" && latexmk -C >/dev/null 2>&1)
echo -n "  \\balance YOK   : "; olc
