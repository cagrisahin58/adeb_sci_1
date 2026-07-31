#!/bin/bash
# C1 zincirinin son asamasini (temiz model degerlendirmesi) bekler.
# Zincir: addenda -> a3 (eslesmis gradyan) -> temiz eval.
LOGF=/home/firat/projects/adeb_sci_1/logs/c1_analyses.log
last=$(wc -l < "$LOGF")
while true; do
  n=$(wc -l < "$LOGF")
  n=${n:-0}
  if [ "$n" -gt "$last" ]; then
    tail -n +"$((last + 1))" "$LOGF" | grep -E "START|DONE|FAIL|SKIP|TAMAM"
    last="$n"
  fi
  grep -q "C1-CLEANEVAL TAMAM" "$LOGF" 2>/dev/null && exit 0
  tail -n 1 "$LOGF" 2>/dev/null | grep -q "FAIL" && exit 1
  if ! docker exec adeb_eval pgrep -f "c1_addenda|c1_gradient_paired|c1_clean_eval|a3_gradient" >/dev/null 2>&1; then
    echo "UYARI: C1 zincir sureci yok ve CLEANEVAL TAMAM gorunmuyor"
    exit 1
  fi
  sleep 60
done
