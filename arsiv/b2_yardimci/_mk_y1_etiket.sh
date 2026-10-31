#!/bin/bash
# Y1: kendi dosyalarimdaki \cite anahtarlarinin .bib'de, \ref hedeflerinin
# herhangi bir .tex'te tanimli olup olmadigini denetler. Salt okur.
cd /home/firat/projects/adeb_sci_1/paper/manuscript || exit 1
MY="main.tex sections/01_introduction.tex sections/06_conclusion.tex"
echo "== cite =="
grep -ohE '\\cite\{[^}]*\}' $MY | sed 's/\\cite{//; s/}//' | tr ',' '\n' | sed 's/ //g' | sort -u | while read k; do
  if grep -qE "@[a-zA-Z]+\{$k," references.bib; then echo "OK  $k"; else echo "YOK $k"; fi
done
echo "== ref =="
grep -ohE '\\(ref|eqref)\{[^}]*\}' $MY | sed -E 's/\\(ref|eqref)\{//; s/}//' | sort -u | while read k; do
  c=$(grep -ho "\\\\label{$k}" main.tex sections/*.tex | wc -l)
  echo "$c  $k"
done
echo "== my labels =="
grep -ohE '\\label\{[^}]*\}' $MY
