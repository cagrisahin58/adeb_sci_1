#!/bin/bash
# Y3 derleme ve uyari ozeti (konsey turu, 31.10.2026)
export PATH="$HOME/.local/bin:$PATH"
bash /home/firat/projects/adeb_sci_1/scripts/derle_en.sh
cd /home/firat/projects/adeb_sci_1/paper/manuscript || exit 1
echo "--- tanimsiz gonderme / cift etiket (atif haric) ---"
grep -n "Reference.*undefined\|multiply defined\|multiply-defined" main.log | head -40
echo "--- tanimsiz atif sayisi ---"
grep -c "Citation.*undefined" main.log
grep "Citation.*undefined" main.log | sed "s/.*Citation .\([^']*\).*/\1/" | sort -u | tr '\n' ' '
echo
echo "--- hatalar ---"
grep -n -A3 "^!" main.log | head -30
echo "--- overfull (sections) ---"
grep -n "Overfull" main.log | head -20
pdfinfo main.pdf 2>/dev/null | grep Pages
