#!/bin/bash
# Rev2 dogrulama: derleme + uyari sayimlari + abstract kelime sayisi
export PATH="$HOME/.local/bin:$PATH"
cd "$HOME/projects/adeb_sci_1/paper/manuscript" || exit 1
latexmk -pdf -interaction=nonstopmode main.tex >/tmp/lm.log 2>&1
echo "LATEXMK_EXIT=$?"
echo "undefined_refs=$(grep -c 'undefined' main.log)"
echo "overfull=$(grep -c 'Overfull' main.log)"
grep "LaTeX Warning: Citation" main.log | head -3
echo "=== abstract kelime sayisi ==="
sed -n '/begin{abstract}/,/end{abstract}/p' main.tex | sed '1d;$d' | wc -w
echo "=== sayfa sayisi ==="
pdfinfo main.pdf 2>/dev/null | grep Pages
