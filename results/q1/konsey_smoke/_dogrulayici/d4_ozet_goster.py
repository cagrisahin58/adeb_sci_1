import json
from pathlib import Path

d = json.loads(Path("results/q1/konsey_smoke/_dogrulayici/d4_bayraklar.json").read_text())
for k in d["kuyruk"]:
    if k["etiket"] in ("temiz", "AT") and k["komut"].find("s2101") + k["komut"].find("s1201") + k["komut"].find("s1301") > -3:
        print(k["etiket"], json.dumps(k.get("ozet"), ensure_ascii=False))
print("--- kuyruk etiketleri:", [(k["etiket"], k["durum"]) for k in d["kuyruk"]][:8])
for r in d["runbook"]:
    o = dict(r.get("ozet") or {})
    for a in ("model", "rb_model", "sources", "matris_dizini"):
        if isinstance(o.get(a), list):
            o[a] = f"{len(o[a])} oge"
    print(r["komut_basi"], r["arguman_sayisi"], r["durum"], json.dumps(o, ensure_ascii=False))
