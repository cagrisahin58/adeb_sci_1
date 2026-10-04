#!/usr/bin/env bash
# ieeeaccess.cls yazi tipi kurulumu kesfi (2026-10-04, LeCun paneli B5/R1)
cd /home/firat/projects/adeb_sci_1/paper/manuscript || exit 1
echo '=== cls 50-95'
sed -n '50,95p' ieeeaccess.cls
echo '=== font dosyalari'
ls *.tfm *.pfb *.map *.fd 2>/dev/null | tr '\n' ' '; echo
ls ieeeaccess 2>/dev/null | head -40 | tr '\n' ' '; echo
echo '=== map yukleme / DeclareFont'
grep -n -i -E 'pdfmapfile|mapfile|\.map|DeclareFontFamily|DeclareFontShape|DeclareFontSubstitution' ieeeaccess.cls | head -20
echo '=== volume'
grep -n -i -E 'volume|\\vol\b|\\year' ieeeaccess.cls | head -8
echo '=== log font uyarilari'
grep -n -i 'Font shape' main.log | head -8
echo '=== sahin bib'
grep -n -A8 'sahin2026behavioral' references.bib | head -12
echo '=== caption icinde {,} (math) sayisi'
grep -c '{,}' sections/04_experiments.tex
grep -n -o -E '\\caption\{[^$]*\$[^$]*\{,\}[^$]*\$' sections/*.tex | cut -c1-110 | head
echo '=== url paketi'
grep -n -E 'usepackage\{(url|xurl|hyperref)' main.tex ieeeaccess.cls | head
