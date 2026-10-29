"""Celisik dogrulayici, D2: iki matris klasorunu hucre ve ornek duzeyinde
karsilastirir (B1'in konsey_smoke_karsilastir.py betiginden bagimsiz yazildi).

Kullanim: python d2_karsilastir.py KLASOR_A KLASOR_B CIKTI_JSON
"""
import json
import sys
from pathlib import Path

import numpy as np

a, b, cikti = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
ja = json.loads((a / "transfer_matrix.json").read_text())
jb = json.loads((b / "transfer_matrix.json").read_text())
sonuc = {"A": str(a), "B": str(b)}
sonuc["json_anahtarlari_A"] = sorted(ja)
sonuc["json_anahtarlari_B"] = sorted(jb)
sonuc["json_anahtar_kumesi_ayni"] = sorted(ja) == sorted(jb)
ortak = sorted(set(ja) & set(jb) - {"results"})
sonuc["ust_alan_farklari"] = {k: [ja[k], jb[k]] for k in ortak if ja[k] != jb[k]}
sonuc["hucre_sayisi"] = [len(ja["results"]), len(jb["results"])]
hf = {}
for k in sorted(set(ja["results"]) | set(jb["results"])):
    if ja["results"].get(k) != jb["results"].get(k):
        hf[k] = [ja["results"].get(k), jb["results"].get(k)]
sonuc["hucre_deger_farklari"] = hf
na = sorted(p.name for p in a.glob("per_sample_*.npz"))
nb = sorted(p.name for p in b.glob("per_sample_*.npz"))
sonuc["npz_sayisi"] = [len(na), len(nb)]
sonuc["npz_adlari_ayni"] = na == nb
dizi_fark = {}
toplam_dizi = 0
for n in sorted(set(na) & set(nb)):
    da, db = np.load(a / n), np.load(b / n)
    if sorted(da.files) != sorted(db.files):
        dizi_fark[n] = {"dosya_alanlari": [sorted(da.files), sorted(db.files)]}
        continue
    for f in da.files:
        toplam_dizi += 1
        if not np.array_equal(da[f], db[f]):
            dizi_fark.setdefault(n, {})[f] = int((da[f] != db[f]).sum())
sonuc["karsilastirilan_dizi"] = toplam_dizi
sonuc["dizi_farklari"] = dizi_fark
sonuc["BIREBIR"] = (not hf and not dizi_fark and na == nb and len(na) > 0
                    and not sonuc["ust_alan_farklari"] and sonuc["json_anahtar_kumesi_ayni"])
cikti.write_text(json.dumps(sonuc, indent=1, ensure_ascii=False))
print(json.dumps(sonuc, indent=1, ensure_ascii=False))
