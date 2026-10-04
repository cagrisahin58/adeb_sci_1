#!/usr/bin/env bash
# 2026-10-04 dizgi adim 4: TikZ sema -> final/, kalan yamalar, EN+TR derleme, dizgi denetimi, kapilar.
cd /home/firat/projects/adeb_sci_1 || exit 1
echo '=== TikZ sema'
bash paper/figures/overview/derle.sh 2>&1 | grep -v -E 'kpsewhich|YOK' | tail -4
mkdir -p paper/figures/arsiv
[ -f paper/figures/final/fig_study_overview.png ] && git mv -f paper/figures/final/fig_study_overview.png paper/figures/arsiv/fig_study_overview_ai_2026-09-29.png 2>/dev/null || mv -f paper/figures/final/fig_study_overview.png paper/figures/arsiv/fig_study_overview_ai_2026-09-29.png 2>/dev/null
cp paper/figures/overview/fig_study_overview.pdf paper/figures/final/fig_study_overview.pdf
cp paper/figures/overview/fig_study_overview.png paper/figures/final/fig_study_overview.png
ls -la paper/figures/final/fig_study_overview.* paper/figures/arsiv/fig_study_overview_ai_2026-09-29.png
echo '=== yamalar'
python3 arsiv/b2_yardimci/_lecun_metin1.py | grep -v ZATEN
python3 arsiv/b2_yardimci/_lecun_metin2.py | grep -v ZATEN
echo '=== EN derle'
bash scripts/derle_en.sh
grep -n -A3 '^!' paper/manuscript/main.log | head -8
echo '=== TR derle'
( cd paper/manuscript_tr && latexmk -pdf -interaction=nonstopmode main.tex > /tmp/derle_tr.log 2>&1; grep -o 'Output written on.*' main.log | tail -1; echo "hata=$(grep -c '^!' main.log) tanimsiz=$(grep -ci 'undefined' main.log)" )
echo '=== dizgi denetimi (EN)'
docker exec -w /workspace adeb_eval python scripts/check_pdf_typeset.py paper/manuscript/main.pdf paper/manuscript/main.log --ayrinti 2>&1 | tail -14
echo '=== kapilar'
timeout 580 bash scripts/kapilar.sh 2>&1 | tail -11
