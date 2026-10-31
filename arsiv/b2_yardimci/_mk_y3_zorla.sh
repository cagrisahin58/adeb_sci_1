#!/bin/bash
# Y3: latexmk'i zorla yeniden kostur (eszamanli derlemenin bozdugu aux icin)
export PATH="$HOME/.local/bin:$PATH"
cd /home/firat/projects/adeb_sci_1/paper/manuscript || exit 1
export TEXINPUTS="/home/firat/projects/adeb_sci_1/paper/manuscript/ieeeaccess//:"
export BSTINPUTS="/home/firat/projects/adeb_sci_1/paper/manuscript/ieeeaccess//:"
export TEXFONTS="/home/firat/projects/adeb_sci_1/paper/manuscript/ieeeaccess//:"
latexmk -g -pdf -interaction=nonstopmode main.tex > /tmp/y3_zorla.log 2>&1
echo "latexmk cikis: $?"
ls -la --time-style=+%H:%M:%S main.aux main.pdf
grep -o 'Output written on.*' main.log | tail -1
printf 'hata      : %s\n' "$(grep -c '^!' main.log)"
printf 'ref tanimsiz: %s\n' "$(grep -c 'Reference.*undefined' main.log)"
printf 'atif tanimsiz: %s\n' "$(grep -c 'Citation.*undefined' main.log)"
printf 'cift etiket: %s\n' "$(grep -c 'multiply' main.log)"
grep -n '^!' main.log | head
grep 'Reference.*undefined' main.log | sed "s/.*Reference .\([^']*\).*/\1/" | sort -u | tr '\n' ' '
echo
