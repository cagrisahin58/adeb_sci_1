#!/usr/bin/env bash
# Council-round study overview: counts from data -> pdflatex (WSL) -> PNG preview -> kanit update.
set -u
KOK=/home/firat/projects/adeb_sci_1
cd "$KOK" || exit 1
docker exec -w /workspace adeb_eval python -B paper/figures/konsey/fig_study_overview_veri.py || exit 1
cd "$KOK/paper/figures/konsey" || exit 1
pdflatex -interaction=nonstopmode -halt-on-error fig_study_overview.tex > fig_study_overview_derle.log 2>&1
kod=$?
echo "pdflatex exit=$kod"
grep -E '^!|Overfull|Undefined' fig_study_overview.log | head -10
grep -o 'Output written on.*' fig_study_overview.log | tail -1
rm -f fig_study_overview.aux
[ "$kod" -eq 0 ] || exit 1
cd "$KOK" || exit 1
docker exec -w /workspace adeb_eval python scripts/pdf2png.py paper/figures/konsey/fig_study_overview.pdf paper/figures/konsey/fig_study_overview.png 300
docker exec -w /workspace adeb_eval python -B paper/figures/konsey/fig_study_overview_veri.py --cikti-ekle
