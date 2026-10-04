#!/usr/bin/env bash
# Genel bakis TikZ seklini derler ve PNG onizleme uretir.
set -u
cd /home/firat/projects/adeb_sci_1/paper/figures/overview || exit 1
for s in tikz.sty standalone.cls lmodern.sty; do printf '%-16s %s\n' "$s" "$(kpsewhich "$s" || echo YOK)"; done
latexmk -pdf -interaction=nonstopmode fig_study_overview.tex > derle.log 2>&1
kod=$?
echo "latexmk exit=$kod"
grep -E '^!|Overfull|Undefined' fig_study_overview.log | head -10
grep -o 'Output written on.*' fig_study_overview.log | tail -1
cd /home/firat/projects/adeb_sci_1 || exit 1
docker exec -w /workspace adeb_eval python scripts/pdf2png.py paper/figures/overview/fig_study_overview.pdf paper/figures/overview/fig_study_overview.png 200
echo "--- Type3 kontrolu"
docker exec -w /workspace adeb_eval python -c "import fitz; d=fitz.open('paper/figures/overview/fig_study_overview.pdf'); print(sorted({f[3] for f in d[0].get_fonts()}))"
nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader 2>/dev/null || echo "nvidia-smi yok"
