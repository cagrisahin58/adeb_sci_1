#!/bin/bash
# C1-pipeline izleyici: yeni log satirlarini yayar; TAMAM/FAIL/oturum-kaybinda cikar.
cd /home/firat/projects/adeb_sci_1 || { echo "cd basarisiz"; exit 1; }
last=0
while true; do
  n=$(wc -l < logs/c1_pipeline.log 2>/dev/null)
  n=${n:-0}
  if [ "$n" -gt "$last" ]; then
    tail -n +"$((last+1))" logs/c1_pipeline.log | grep -E "START|DONE|FAIL|SKIP|TAMAM|BASLANGIC"
    last="$n"
  fi
  grep -q "C1-PIPELINE TAMAM" logs/c1_pipeline.log 2>/dev/null && exit 0
  grep -q "FAIL" logs/c1_pipeline.log 2>/dev/null && exit 1
  tmux has-session -t c1pipe 2>/dev/null || { echo "UYARI: c1pipe tmux oturumu kayboldu (TAMAM gorulmedi)"; exit 1; }
  sleep 300
done
