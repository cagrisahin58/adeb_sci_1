#!/bin/bash
# C1 izleyici v2: yeni log satirlarini yayar; TAMAM'da exit 0, SON satir FAIL ise
# exit 1. Canlilik tmux'a DEGIL konteyner icindeki surece bakar (tmux yalnizca
# goruntuleyicidir; olmesi pipeline'i etkilemez — zincir c1_resume_inner.sh ile
# konteyner icinde yasar). Eski logdaki tarihsel FAIL satirlari yok sayilir.
cd /home/firat/projects/adeb_sci_1 || { echo "cd basarisiz"; exit 1; }
last=0
while true; do
  n=$(wc -l < logs/c1_pipeline.log 2>/dev/null)
  n=${n:-0}
  if [ "$n" -gt "$last" ]; then
    tail -n +"$((last+1))" logs/c1_pipeline.log | grep -E "START|DONE|FAIL|SKIP|RESUME|TAMAM|BASLANGIC"
    last="$n"
  fi
  grep -q "C1-PIPELINE TAMAM" logs/c1_pipeline.log 2>/dev/null && exit 0
  tail -n 1 logs/c1_pipeline.log 2>/dev/null | grep -q "FAIL" && exit 1
  if ! docker exec adeb_eval bash -c "pgrep -f 'c1_resume_inner|run_c1_pipeline|cli.main|run_autoattack|c1_pgd_eval' >/dev/null" 2>/dev/null; then
    echo "UYARI: konteynerde C1 sureci gorunmuyor ve TAMAM yok — kontrol gerekli"
    exit 1
  fi
  sleep 180
done
