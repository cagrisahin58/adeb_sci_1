# Salt okur: dondurulmus betik ciktisinin b2.model_tablosu alanini olcek basina tablo olarak basar.
# Kullanim: python3 -I _ek_rapor_model_tablosu.py <json> [olcek=yari_log]
import json
import math
import sys

sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(sys.argv[1], encoding="utf-8"))
olcek = sys.argv[2] if len(sys.argv) > 2 else "yari_log"
mt = d["b2"]["model_tablosu"]
print(f"olcek={olcek}  (w = exp(omega) yuzde, yalniz log olceklerde)")
for m, v in mt.items():
    e = v.get(olcek, {})
    om = e.get("omega")
    w = math.exp(om) if (om is not None and "log" in olcek and "logit" not in olcek) else None
    print(f"{m:40s} sigma={e.get('sigma')!s:24s} rho={e.get('rho')!s:24s} S={e.get('S')!s:22s} omega={om!s:22s} w%={w if w is None else round(w, 4)} panel_n={e.get('panel_n')}")
