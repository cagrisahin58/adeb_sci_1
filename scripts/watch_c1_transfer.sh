#!/bin/bash
# C1 transfer izleyicisi: konteyner icindeki logs/c1_transfer.log'u takip eder.
# TAMAM -> exit 0; SON satir FAIL -> exit 1; surec yoksa ve TAMAM yoksa uyarip cikar.
LOGF=/home/firat/projects/adeb_sci_1/logs/c1_transfer.log
last=0
while true; do
  if [ -f "$LOGF" ]; then
    n=$(wc -l < "$LOGF")
  else
    n=0
  fi
  n=${n:-0}
  if [ "$n" -gt "$last" ]; then
    tail -n +"$((last + 1))" "$LOGF" | grep -E "START|DONE|FAIL|SKIP|TAMAM|BASLANGIC"
    last="$n"
  fi
  grep -q "C1-TRANSFER TAMAM" "$LOGF" 2>/dev/null && exit 0
  tail -n 1 "$LOGF" 2>/dev/null | grep -q "FAIL" && exit 1
  if ! docker exec adeb_eval pgrep -f c1_transfer >/dev/null 2>&1; then
    echo "UYARI: konteynerde c1_transfer sureci yok ve TAMAM gorunmuyor"
    exit 1
  fi
  sleep 60
done
