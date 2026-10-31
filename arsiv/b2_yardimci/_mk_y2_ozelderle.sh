#!/bin/bash
# Y2: depoya dokunmadan ozel kopyada derleme (eszamanli derlemelerden etkilenmemek icin)
export PATH="$HOME/.local/bin:$PATH"
D=/tmp/y2_derle
rm -rf "$D"; mkdir -p "$D/paper"
cp -r /home/firat/projects/adeb_sci_1/paper/manuscript "$D/paper/manuscript"
cp -r /home/firat/projects/adeb_sci_1/paper/figures "$D/paper/figures" 2>/dev/null
cd "$D/paper/manuscript" || exit 1
rm -f main.aux main.bbl main.blg main.fdb_latexmk main.fls main.log main.out main.toc
latexmk -pdf -interaction=nonstopmode main.tex > /tmp/y2_lm.log 2>&1
echo "LATEXMK_EXIT=$?"
echo "hata: $(grep -c '^! ' main.log)"
grep -n -A3 '^! ' main.log | head -20
echo "tanimsiz gonderme: $(grep -c 'LaTeX Warning: Reference' main.log)"
grep 'LaTeX Warning: Reference' main.log | head
echo "tanimsiz atif: $(grep -c 'LaTeX Warning: Citation' main.log)"
grep 'LaTeX Warning: Citation' main.log | head
echo "cift etiket: $(grep -c 'multiply defined' main.log)"
grep 'multiply defined' main.log | head
echo "bibtex uyarilari:"; grep -i 'warning' main.blg | head
pdfinfo main.pdf 2>/dev/null | grep Pages
grep -o '(./sections/[^ )]*' main.log | sort | uniq -c
