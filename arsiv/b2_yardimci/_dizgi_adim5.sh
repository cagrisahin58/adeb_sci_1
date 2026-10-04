#!/usr/bin/env bash
# 2026-10-04 dizgi adim 5: TR yamalarini uygula, foy protokol bolumu, tablo kaynaklari.
cd /home/firat/projects/adeb_sci_1 || exit 1
echo '=== metin1 yeniden'
python3 arsiv/b2_yardimci/_lecun_metin1.py | grep -v ZATEN
echo '=== REF protokol x ayar (151-201)'
sed -n '151,201p' results/C1_REFERANS_FOYU.md
echo '=== refs: tab:svhn_protocols / tab:l2_results (EN, TR)'
grep -n -o -E '.{80}tab:(svhn_protocols|l2_results)\}.{40}' paper/manuscript/sections/*.tex paper/manuscript_tr/sections/*.tex | grep -v 'label{' | cut -c1-220
echo '=== EN Tablo 6 (222-240)'
sed -n '222,240p' paper/manuscript/sections/04_experiments.tex | cut -c1-240
echo '=== TR Tablo 6'
grep -n -B3 -A14 'label{tab:svhn_protocols}' paper/manuscript_tr/sections/04_deneyler.tex | cut -c1-240
echo '=== EN Tablo 8 satirlari (300-308)'
sed -n '300,310p' paper/manuscript/sections/04_experiments.tex | cut -c1-200
echo '=== TR Tablo 8'
grep -n -A12 'label{tab:gradient}' paper/manuscript_tr/sections/04_deneyler.tex | cut -c1-200
echo '=== EN Tablo 9 (322-340)'
grep -n -A12 'label{tab:spatial}' paper/manuscript/sections/04_experiments.tex | cut -c1-200
echo '=== TR Tablo 9'
grep -n -A12 'label{tab:spatial}' paper/manuscript_tr/sections/04_deneyler.tex | cut -c1-200
echo '=== EN Tablo 10 govde'
grep -n -A24 'label{tab:feature_degradation}' paper/manuscript/sections/04_experiments.tex | sed -n '1,30p' | cut -c1-160
echo '=== TR Tablo 10 govde'
grep -n -A24 'label{tab:feature_degradation}' paper/manuscript_tr/sections/04_deneyler.tex | sed -n '1,30p' | cut -c1-160
echo '=== 04:303 isaretli kosinus cumlesi (EN/TR)'
grep -n -o -E '.{60}0\.0014.{40}' paper/manuscript/sections/04_experiments.tex | head -3
grep -n -o -E '.{60}0\{,\}0014.{40}' paper/manuscript_tr/sections/04_deneyler.tex | head -3
echo '=== layer4.0 metinde'
grep -n -o -E 'layer[0-9]\.[0-9]' paper/manuscript/sections/04_experiments.tex paper/manuscript/sections/05_discussion.tex | sort | uniq -c | head
