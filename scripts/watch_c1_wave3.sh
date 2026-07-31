#!/bin/bash
# C1 ucuncu analiz dalgasi izleyicisi (C5 + C4).
LOGF=/home/firat/projects/adeb_sci_1/logs/c1_wave3.log
last=0
while true; do
  if [ -f "$LOGF" ]; then n=$(wc -l < "$LOGF"); else n=0; fi
  n=${n:-0}
  if [ "$n" -gt "$last" ]; then
    tail -n +"$((last + 1))" "$LOGF" | grep -E "START|DONE|FAIL|SKIP|TAMAM"
    last="$n"
  fi
  grep -q "C1-DALGA3 TAMAM" "$LOGF" 2>/dev/null && exit 0
  tail -n 1 "$LOGF" 2>/dev/null | grep -q "FAIL" && exit 1
  if ! docker exec adeb_eval pgrep -f "c1_wave3|c1_c4_attention|c1_c5_spatial" >/dev/null 2>&1; then
    echo "UYARI: C1 dalga3 sureci yok ve TAMAM gorunmuyor"
    exit 1
  fi
  sleep 90
done
