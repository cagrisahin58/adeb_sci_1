#!/usr/bin/env bash
# 2026-10-04 dizgi adim 3: derleme hatasi, TR 41. satir, Tablo 3 yeniden yapilandirma yamasi.
cd /home/firat/projects/adeb_sci_1 || exit 1
echo '=== derleme hatasi'
grep -n -A6 '^!' paper/manuscript/main.log | head -30
echo '=== tanimsiz'
grep -n -i 'undefined' paper/manuscript/main.log | head -5
echo '=== times shape bilgi (ilk 4)'
grep -n 'T1/times' paper/manuscript/main.log | head -4
echo '=== TR 41'
sed -n '41p' paper/manuscript_tr/sections/04_deneyler.tex | grep -o -E '.{70}10\^\{-84\}.{90}'
echo '=== Tablo 3 yamasi'
python3 arsiv/b2_yardimci/_lecun_metin2.py
