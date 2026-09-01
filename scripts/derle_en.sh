#!/usr/bin/env bash
# Ingilizce makaleyi IEEE Access sinifiyla derler.
# ieeeaccess.cls ve font dosyalari paper/manuscript/ieeeaccess/ altinda;
# TEXINPUTS/BSTINPUTS bunlari gorunur kilar (sondaki ':' varsayilan yolu ekler).
set -u
cd /home/firat/projects/adeb_sci_1/paper/manuscript || exit 1
export TEXINPUTS="/home/firat/projects/adeb_sci_1/paper/manuscript/ieeeaccess//:"
export BSTINPUTS="/home/firat/projects/adeb_sci_1/paper/manuscript/ieeeaccess//:"
export TEXFONTS="/home/firat/projects/adeb_sci_1/paper/manuscript/ieeeaccess//:"
latexmk -pdf -interaction=nonstopmode main.tex > /tmp/derle_en.log 2>&1
kod=$?
grep -o 'Output written on.*' main.log | tail -1
printf 'hata      : %s\n' "$(grep -c '^!' main.log)"
printf 'tanimsiz  : %s\n' "$(grep -ci 'undefined' main.log)"
printf 'Overfull  : %s\n' "$(grep -c 'Overfull ..hbox' main.log)"
exit $kod
