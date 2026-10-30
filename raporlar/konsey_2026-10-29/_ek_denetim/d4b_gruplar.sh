#!/bin/bash
cd /home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29
awk -F'\t' '{g=($2 ~ /imagenet\//)?"IN":(($2 ~ /cifar100/)?"C100":"arsiv"); s[g]+=$1; if ($2 ~ /Wong2020Fast|Chen2021LTD|Cui2023/) y[g]+=$1} END {for (g in s) printf "%s toplam %.1f MB, yedeksiz %.1f MB, MiB %.1f\n", g, s[g]/1e6, (s[g]-y[g])/1e6, s[g]/1048576}' _ek_denetim/d4_boyutlar.tsv
echo "== KONSEY_PLANI §13 =="
awk 'NR>=210' KONSEY_PLANI.md
echo "== sure kestirimi ozet =="
python3 -c "import json; d=json.load(open('_ek_sure_kestirimi.json')); print(json.dumps({k:v for k,v in d.items() if not isinstance(v,(list,dict))}, ensure_ascii=False, indent=0)[:3000]); print(list(d.keys()))"
