#!/bin/bash
cd /home/firat/projects/adeb_sci_1
F=results/C1_REFERANS_FOYU.md
sed -n '1698,1730p' "$F" | cut -c1-330
echo "=== P3"
sed -n '13,28p' raporlar/konsey_2026-10-29/01_oneri_P3_kuram_olcum.md
echo "=== 13_b10"
head -40 raporlar/konsey_2026-10-29/13_b10_r18_r50_denetimi.md | cut -c1-400
echo "=== labels"
cd paper/manuscript
grep -ho '\\label{[^}]*}' main.tex sections/*.tex | sort | uniq -c | awk '$1>1'
for l in subsec:scale subsec:attack_side subsec:gradcos subsec:imagenet app:behavior subsec:pair_decomposition prop:identifiability eq:raw_identity eq:general_identity prop:hscale subsec:transfer app:selection subsec:twobytwo subsec:robustness subsec:computational subsec:limitations subsec:implications; do
  n=$(grep -c "\\\\label{$l}" main.tex sections/*.tex | awk -F: '{s+=$2} END{print s}')
  echo "$l $n"
done
echo "=== who refs my labels"
grep -n "subsec:findings\|subsec:prior\|subsec:implications\|subsec:limitations\|subsec:future\|subsec:computational\|sec:discussion" main.tex sections/*.tex | grep -v "label{" | cut -c1-160
