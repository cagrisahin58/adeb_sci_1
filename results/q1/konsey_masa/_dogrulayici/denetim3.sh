#!/bin/bash
cd /home/firat/projects/adeb_sci_1
echo "=== pilot ve smoke dosyalari"
ls -la --time-style=+%H:%M results/q1/konsey_pilot_zaman*.json 2>&1
ls -laR --time-style=+%H:%M models/q1/konsey_smoke 2>&1 | head -30
echo "=== pilot icerik anahtarlari (dogruluk var mi)"
for f in results/q1/konsey_pilot_zaman*.json; do
  echo "--- $f"
  grep -o -i -E '"[a-z_]*(acc|dogruluk|robust|pgd|fool|yanilt)[a-z_]*" *: *[-0-9.]+' "$f" | head -10
done
echo "=== etkilesim_simetri_masa anahtarlari"
python3 -c "import json;d=json.load(open('results/q1/etkilesim_simetri_masa.json'));print(list(d)[:20])"
echo "=== smoke loglari"
ls -la --time-style=+%H:%M logs/ 2>/dev/null | grep -i -E 'konsey|smoke|pilot' | head
