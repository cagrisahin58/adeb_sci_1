#!/usr/bin/env bash
# 2026-10-04 dizgi adim 7: sekil basliklari, EN+TR derleme, dokuz kapi, render.
cd /home/firat/projects/adeb_sci_1 || exit 1
echo '=== metin4'
python3 arsiv/b2_yardimci/_lecun_metin4.py || exit 1
echo '=== EN derle'
bash scripts/derle_en.sh
grep -n -A3 '^!' paper/manuscript/main.log | head -6
echo '=== TR derle'
( cd paper/manuscript_tr && latexmk -pdf -interaction=nonstopmode main.tex > /tmp/derle_tr.log 2>&1; grep -o 'Output written on.*' main.log | tail -1; echo "hata=$(grep -c '^!' main.log) tanimsiz=$(grep -ci 'undefined' main.log)"; grep -n -A3 '^!' main.log | head -6 )
echo '=== kapilar'
timeout 580 bash scripts/kapilar.sh 2>&1 | tail -12
echo '=== render'
docker exec -w /workspace adeb_eval python scripts/render_sayfalar.py /workspace/teslim/render_2026-10-04c 2>&1 | tail -1
grep -E 'fig:' teslim/render_2026-10-04c/INDEKS.md
