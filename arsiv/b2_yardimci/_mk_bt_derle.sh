#!/usr/bin/env bash
# Butunlestirici: temiz derleme + sayim. Kullanim: bash _mk_bt_derle.sh [temiz]
cd /home/firat/projects/adeb_sci_1/paper/manuscript || exit 1
export PATH=/home/firat/.local/bin:$PATH
if [ "${1:-}" = "temiz" ]; then
  rm -f main.aux main.bbl main.blg main.fdb_latexmk main.fls main.out
fi
bash /home/firat/projects/adeb_sci_1/scripts/derle_en.sh
echo "derle_en rc=$?"
python3 -c "import pypdf;print('sayfa', len(pypdf.PdfReader('main.pdf').pages))"
echo "--- uyarilar"
grep -n 'Overfull\|undefined\|multiply\|Underfull .hbox (badness 10000) in paragraph' main.log | head -40
grep -n '^!' main.log | head
echo "--- bibtex"
grep -i 'warning\|error' main.blg | head
