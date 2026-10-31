#!/bin/bash
# Salt okur: ImageNetV2 klasor ve dosya sayilari (ek §5.1 denetimi) ve manifest sinif basina sayim.
cd /home/firat/projects/adeb_sci_1/data/imagenetv2/imagenetv2-matched-frequency-format-val
echo "klasor: $(ls | wc -l)"
for d in */; do ls "$d" | wc -l; done | sort | uniq -c
cd /home/firat/projects/adeb_sci_1
python3 -I -c "
import json,collections
d=json.load(open('results/q1/konsey_b8_imagenetv2/denetim/imagenetv2_manifest.json'))
c=collections.Counter(x['etiket'] for x in d['dosyalar'])
print('sinif', len(c), 'sinif basina', sorted(set(c.values())))
"
