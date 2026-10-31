#!/bin/bash
cd /home/firat/projects/adeb_sci_1
F=results/C1_REFERANS_FOYU.md
wc -l "$F"
for r in 14,22 645,652 1312,1318 1450,1500 1505,1513 1550,1556 1600,1607 1755,1760 1786,1797 1815,1820 1836,1840 1874,1880; do
  echo "--- $r"
  sed -n "${r}p" "$F" | cut -c1-280
done
