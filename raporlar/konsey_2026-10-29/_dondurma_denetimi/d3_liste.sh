#!/bin/bash
cd /home/firat/projects/adeb_sci_1/results/q1 || exit 1
OUT=/home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29/_dondurma_denetimi/d3_dosyalar.txt
{
echo "=== konsey_smoke (adv_onbellek* haric, ilk iki duzey dizinler + dosyalar) ==="
find konsey_smoke -path '*adv_onbellek*' -prune -o -path '*d7_onbellek' -prune -o -type f -printf '%TY-%Tm-%Td %TH:%TM %s %p\n' | sort -k3
echo "=== konsey_smoke onbellek dizinleri ==="
find konsey_smoke -type d \( -name 'adv_onbellek*' -o -name 'd7_onbellek' \) -printf '%p\n'
echo "=== konsey_masa ==="
find konsey_masa -type f -printf '%TY-%Tm-%Td %TH:%TM %s %p\n' | sort -k3
echo "=== _konsey_sahte ==="
find _konsey_sahte -type f -printf '%TY-%Tm-%Td %TH:%TM %s %p\n' | sort -k3
echo "=== konsey_sahte_2x2_sinama.json ve diger konsey_* ==="
ls -la --time-style=+'%Y-%m-%d %H:%M' konsey_* 2>/dev/null
echo "=== results/q1 altinda konsey adli baska ogeler ==="
ls -d *konsey* 2>/dev/null
echo "=== taslagin ilk yaziminin ve diger dosyalarin zamanlari ==="
stat -c '%y %n' /home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29/ON_KAYIT_TASLAGI.md /home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29/KONSEY_PLANI.md
} > "$OUT" 2>&1
wc -l "$OUT"
