#!/bin/bash
# Y1: foyun bolum basliklarini satir numarasiyla listeler. Salt okur.
F=/home/firat/projects/adeb_sci_1/results/C1_REFERANS_FOYU.md
grep -n '^#' "$F" | awk -F: '($1>=1 && $1<=420) || $1>=1430'
