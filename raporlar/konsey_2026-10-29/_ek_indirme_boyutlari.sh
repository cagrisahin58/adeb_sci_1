#!/usr/bin/env bash
# 06_ek_deney_tasarim.md icin: fastai arsivlerinin boyutu (yalniz HTTP HEAD; indirme yok)
cd "$(dirname "$0")"
{
  echo "# uretildi $(date -u +%Y-%m-%dT%H:%M:%SZ); curl -sI (HEAD), indirme yapilmadi"
  for u in imagenette2-320 imagewoof2-320 imagenette-320 imagewoof-320; do
    printf '%s ' "$u"
    curl -sI --max-time 20 "https://s3.amazonaws.com/fast-ai-imageclas/$u.tgz" | grep -i -E 'content-length|^HTTP' | tr -d '\r' | tr '\n' ' '
    echo
  done
} > _ek_indirme_boyutlari.txt
