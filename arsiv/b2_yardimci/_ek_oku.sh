#!/bin/bash
cd /home/firat/projects/adeb_sci_1
for f in results/q1/ek_regresyon/gpu_n200/karsilastirma_*.json; do echo "== $f"; cat "$f"; echo; done
echo "== manifest ust alanlar"
python3 -c "
import json; m=json.load(open('results/q1/konsey_b8_imagenetv2/denetim/imagenetv2_manifest.json'))
print({k:(v if not isinstance(v,(list,dict)) else type(v).__name__+'['+str(len(v))+']') for k,v in m.items()})
"
echo "== b8_denetim.log kuyruk"
tail -25 results/q1/ek_loglar/b8_denetim.log
echo "== sha256"
sha256sum results/q1/konsey_b8_imagenetv2/denetim/onisleme_denetimi.json results/q1/konsey_b8_imagenetv2/denetim/imagenetv2_manifest.json experiments/q1_ek_transfer_matrix.py
echo "== sapma kaydi Ek B8-B10 bolumu kuyrugu"
grep -n 'Ek B8' results/q1_research/ONKAYIT_SAPMALAR.md
tail -15 results/q1_research/ONKAYIT_SAPMALAR.md
