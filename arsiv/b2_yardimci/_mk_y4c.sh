#!/bin/bash
cd /home/firat/projects/adeb_sci_1
F=results/C1_REFERANS_FOYU.md
grep -n "^## \|^### M" "$F" | awk -F: '$1>1300' | cut -c1-120
echo ---
grep -n "Potansiyel payi" "$F" | cut -c1-80
grep -n "^| K-b" "$F" | cut -c1-60
grep -n "Anahtar cift" "$F" | cut -c1-80
