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
# 2026-10-31: eski desen 'Overfull ..hbox' iki karakter bekliyordu, gunlukte tek ters bolu var
# ('Overfull \hbox'); hic eslesmiyor ve her zaman 0 basiyordu. Toplam, compile_check.sh'nin
# 'Overfull' sayimiyla aynidir (gunlukte yalniz \hbox ve \vbox satirlari Overfull tasir).
printf 'Overfull  : %s (hbox %s, vbox %s)\n' "$(grep -c 'Overfull \\[hv]box' main.log)" \
    "$(grep -c 'Overfull \\hbox' main.log)" "$(grep -c 'Overfull \\vbox' main.log)"
exit $kod
