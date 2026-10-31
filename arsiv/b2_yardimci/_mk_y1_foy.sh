#!/bin/bash
# Y1 (makale yazari, devam kipi): foy satirlarini yazdirir. Salt okur.
F=/home/firat/projects/adeb_sci_1/results/C1_REFERANS_FOYU.md
for n in "$@"; do
  printf '[%s] %s\n' "$n" "$(sed -n "${n}p" "$F" | cut -c1-300)"
done
