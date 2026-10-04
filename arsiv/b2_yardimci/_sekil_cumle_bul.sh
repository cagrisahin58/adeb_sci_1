#!/usr/bin/env bash
# Sekil basliklari ve ilgili cumleler (EN/TR) -- 4. parti yamasi icin kesif
cd /home/firat/projects/adeb_sci_1 || exit 1
E=paper/manuscript/sections/04_experiments.tex
T=paper/manuscript_tr/sections/04_deneyler.tex
echo '=== EN captions'
grep -n -E '^\\caption\{(PGD-10 robust accuracy|Distribution of per-sample|Input-gradient magnitude|CLS-token attention|Per-layer entropy)' "$E" | cut -c1-600
echo '=== TR captions'
grep -n -E '^\\caption\{' "$T" | grep -E 'PGD-10 gürbüz|gradyan|dikkat|entropi|Gradyan' | cut -c1-600
echo '=== EN cumleler'
grep -n -o -E '[^.]*near 4\.9 nats[^.]*\.' "$E"
grep -n -o -E '[^.]*lie on top of each other[^.]*\.' "$E"
grep -n -o -E '[^.]*later layers move more[^.]*\.' "$E"
grep -n -o -E 'Figure~\\ref\{fig:gradient_analysis\}[^.]*\.' "$E"
grep -n -o -E 'Figure~\\ref\{fig:gradient_heatmap\}[^.]*\.' "$E"
echo '=== TR cumleler'
grep -n -o -E '[^.]*4[,{}]+9 nat[^.]*\.' "$T"
grep -n -o -E '[^.]*üst üste[^.]*\.' "$T"
grep -n -o -E '[^.]*daha çok (kaymakta|hareket)[^.]*\.' "$T"
grep -n -o -E 'Şekil~\\ref\{fig:gradient_analysis\}[^.]*\.' "$T"
grep -n -o -E 'Şekil~\\ref\{fig:gradient_heatmap\}[^.]*\.' "$T"
grep -n -o -E 'Şekil~\\ref\{fig:attention_layers\}[^.]*\.' "$T"
echo '=== REF entropi'
awk '/^## Dikkat entropisi/,/^## Epsilon/' results/C1_REFERANS_FOYU.md | head -30
