#!/bin/bash
cd /home/firat/projects/adeb_sci_1/paper/manuscript || exit 1
echo "--- undefined satirlari ---"
grep -ni 'undefined' main.log
echo "--- 04 ve sonrasi Overfull/Underfull ---"
bas=$(grep -n '(./sections/04_experiments.tex' main.log | head -1 | cut -d: -f1)
awk -v b="$bas" 'NR>=b && /Overfull|Underfull/ {print NR": "$0}' main.log | head -30
echo "--- multiply ---"
grep -n 'multiply' main.log
echo "--- LaTeX Warning ozet ---"
grep 'LaTeX Warning' main.log | sed 's/on page.*//' | sort | uniq -c | head -20
