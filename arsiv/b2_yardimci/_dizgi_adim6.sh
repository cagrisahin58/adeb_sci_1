#!/usr/bin/env bash
# 2026-10-04 dizgi adim 6: 3. parti tablo yamalari, derleme, dizgi denetimi, kapilar.
cd /home/firat/projects/adeb_sci_1 || exit 1
echo '=== metin3'
python3 arsiv/b2_yardimci/_lecun_metin3.py || exit 1
echo '=== EN derle'
bash scripts/derle_en.sh
grep -n -A3 '^!' paper/manuscript/main.log | head -8
echo '=== TR derle'
( cd paper/manuscript_tr && latexmk -pdf -interaction=nonstopmode main.tex > /tmp/derle_tr.log 2>&1; grep -o 'Output written on.*' main.log | tail -1; echo "hata=$(grep -c '^!' main.log) tanimsiz=$(grep -ci 'undefined' main.log)"; grep -n -A3 '^!' main.log | head -6 )
echo '=== dizgi denetimi (EN)'
docker exec -w /workspace adeb_eval python scripts/check_pdf_typeset.py paper/manuscript/main.pdf paper/manuscript/main.log --ayrinti 2>&1 | tail -12
echo '=== kapilar'
timeout 580 bash scripts/kapilar.sh 2>&1 | tail -11
