#!/bin/bash
# Ek icin foy satirlarini bul (Y3, 31.10.2026)
f=/home/firat/projects/adeb_sci_1/results/C1_REFERANS_FOYU.md
for k in "0.4928" "0.4561" "0.4046" "0.0378" "Moran" "0.9604" "0.8777" "0.0045" "0.0276" "4.613" "0.9895" "0.22" "0.48" "10.45" "0.656" "0.931" "0.974" "0.885" "0.802" "\-1.249" "0.527" "0.914" "0.762" "2.85" "2.62" "1.09 " "1.42" "0.67" "7.38" "0.32" "25 epok\|25 epoch\|secilen epok" "0.05 " "2.41" "28.3" "0.18;\|1.83" "2.83" "epsilon\|eps sup\|Epsilon" "57" "C2: TGR" "10.07" "0.0009" "0.036"; do
  echo "##### $k"
  grep -n -- "$k" "$f" | cut -c1-260 | head -6
done
