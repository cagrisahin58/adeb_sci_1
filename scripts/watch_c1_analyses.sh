#!/bin/bash
# C1 kalan-analiz izleyicisi: logs/c1_analyses.log.
LOGF=/home/firat/projects/adeb_sci_1/logs/c1_analyses.log
last=0
while true; do
  if [ -f "$LOGF" ]; then n=$(wc -l < "$LOGF"); else n=0; fi
  n=${n:-0}
  if [ "$n" -gt "$last" ]; then
    tail -n +"$((last + 1))" "$LOGF" | grep -E "START|DONE|FAIL|SKIP|TAMAM|BASLANGIC"
    last="$n"
  fi
  grep -q "C1-ANALIZ TAMAM" "$LOGF" 2>/dev/null && exit 0
  tail -n 1 "$LOGF" 2>/dev/null | grep -q "FAIL" && exit 1
  if ! docker exec adeb_eval pgrep -f "c1_analyses|c1_analyses_rerun|cli.main" >/dev/null 2>&1; then
    echo "UYARI: konteynerde C1 analiz sureci yok ve TAMAM gorunmuyor"
    exit 1
  fi
  sleep 60
done
