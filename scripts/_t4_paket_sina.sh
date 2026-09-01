#!/usr/bin/env bash
# Teslim paketindeki EN kaynagi, depodan BAGIMSIZ olarak derleniyor mu?
# (Editor/hakem elinde yalnizca paket olacak.)
set -u
PAKET=$(ls -d /home/firat/projects/adeb_sci_1/teslim/TESLIM_*/ 2>/dev/null | tail -1)
[ -n "$PAKET" ] || { echo "paket yok"; exit 1; }
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
cp -r "$PAKET/02_MAKALE_EN/kaynak/." "$T/"
cd "$T" || exit 1
# figurler paket icinde 'final/' altinda; main.tex ../figures/final bekliyor
mkdir -p ../figures && cp -r final ../figures/final 2>/dev/null || true
latexmk -pdf -interaction=nonstopmode main.tex > /dev/null 2>&1
echo "paket icinden derleme:"
grep -o 'Output written on.*' main.log 2>/dev/null | tail -1 | sed 's/^/  /'
printf '  hata     : %s\n' "$(grep -c '^!' main.log 2>/dev/null || echo '?')"
printf '  tanimsiz : %s\n' "$(grep -c 'Reference.*undefined\|Citation.*undefined' main.log 2>/dev/null || echo '?')"
