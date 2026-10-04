#!/usr/bin/env bash
# 2026-10-04 dizgi adim 1: t1times.fd ile derle, yazi tipi/tasma denetimi, kesif grep'leri.
cd /home/firat/projects/adeb_sci_1 || exit 1
echo '=== sablondan .fd var mi (depo + teslim)'
find . -name '*.fd' -not -path './models/*' -not -path './logs/*' 2>/dev/null | head
echo '=== EN derle'
bash scripts/derle_en.sh
echo '=== times uyarisi'
grep -c "Font shape \`T1/times" paper/manuscript/main.log
echo '=== dizgi denetimi (konteyner)'
docker exec -w /workspace adeb_eval python scripts/check_pdf_typeset.py paper/manuscript/main.pdf paper/manuscript/main.log 2>&1 | tail -30
echo '=== sayfa sayisi'
grep -o 'Output written on.*' paper/manuscript/main.log | tail -1
echo '=== CIFAR kucuk resimler'
docker exec -w /workspace adeb_eval python paper/figures/overview/cifar_thumbs.py 2>&1 | tail -2
echo '=== kesif: etiketler ve cumleler'
grep -n 'label{subsec:' paper/manuscript/sections/04_experiments.tex | cut -c1-80
echo '--- REF 40-46'
sed -n '40,46p' results/C1_REFERANS_FOYU.md
echo '--- TGR config'
python3 -c "import json;d=json.load(open('results/c1_c2/pair1/tgr_summary.json'));print({k:v for k,v in d.items() if not isinstance(v,(dict,list))});print([k for k in d])" 2>&1 | head -5
echo '--- fig4 heatmap ortami (EN)'
grep -n -B3 -A3 'fig3_transfer_heatmap' paper/manuscript/sections/04_experiments.tex | cut -c1-100
grep -n 'fig:transfer_heatmap' paper/manuscript/sections/*.tex | cut -c1-160
echo '--- fig4 heatmap ortami (TR)'
grep -n -B3 -A3 'fig3_transfer_heatmap' paper/manuscript_tr/sections/04_deneyler.tex | cut -c1-100
grep -n 'fig:transfer_heatmap' paper/manuscript_tr/sections/*.tex | cut -c1-160
echo '--- 03:7 cumle'
grep -n 'without re-running any attack' paper/manuscript/sections/03_methodology.tex | cut -c1-60
grep -n 'yeniden koşmadan' paper/manuscript_tr/sections/03_yontem.tex | cut -c1-60
echo '--- McNemar 04:41'
grep -n -o -E 'p < 10\^\{-(84|120)\}[^)]*' paper/manuscript/sections/04_experiments.tex | head
grep -n -o -E 'p < 10\^\{-(84|120)\}[^)]*' paper/manuscript_tr/sections/04_deneyler.tex | head
echo '--- caption satirlarinda {,}'
grep -n -E '^\\caption' paper/manuscript/sections/04_experiments.tex | grep -o -E '^[0-9]+:.{0,0}' | tr -d ':' | while read -r n; do if sed -n "${n}p" paper/manuscript/sections/04_experiments.tex | grep -q '{,}'; then echo "satir $n: $(sed -n "${n}p" paper/manuscript/sections/04_experiments.tex | grep -o -E '.{0,30}\{,\}.{0,12}' | head -3 | tr '\n' '|')"; fi; done
