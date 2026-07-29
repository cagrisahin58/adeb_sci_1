#!/bin/bash
# C-pipeline izleyici: yeni log satirlarini yayar; TAMAM/FAIL/oturum-kaybinda cikar.
cd /home/firat/projects/adeb_sci_1 || { echo "cd basarisiz"; exit 1; }
last=0
while true; do
  n=$(wc -l < logs/c_pipeline.log 2>/dev/null)
  n=${n:-0}
  if [ "$n" -gt "$last" ]; then
    tail -n +"$((last+1))" logs/c_pipeline.log
    last="$n"
  fi
  grep -q "C-PIPELINE TAMAM" logs/c_pipeline.log 2>/dev/null && exit 0
  grep -q "FAIL" logs/c_pipeline.log 2>/dev/null && exit 1
  tmux has-session -t cpipe 2>/dev/null || { echo "UYARI: cpipe tmux oturumu kayboldu (TAMAM gorulmedi)"; exit 1; }
  sleep 120
done
