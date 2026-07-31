#!/bin/bash
# Bildiri sayfalarini PNG'ye cevirip host'a kopyalar: bash scripts/copy_bildiri_pages.sh 1 3 5 6
cd /home/firat/projects/adeb_sci_1 || exit 1
docker exec -w /workspace adeb_eval python scripts/render_bildiri_pages.py "$@" >/dev/null || exit 1
for p in "$@"; do
  docker cp "adeb_eval:/tmp/bildiri_page${p}.png" "$HOME/bp${p}.png" || exit 1
  echo "$HOME/bp${p}.png"
done
