# -*- coding: utf-8 -*-
"""Masa incelemesi (31.10.2026): dondurulmus B2/B9 ciktilarinin yapisini okur; sayi uretmez."""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
for f in sys.argv[1:]:
    print("==", f)
    d = json.load(open(f, encoding="utf-8"))
    print(list(d.keys()))
    m = d.get("meta", {})
    print(json.dumps(m, ensure_ascii=False)[:1500])
    b = d.get("b2")
    if b:
        F = b["F_B2"]
        print("hucreler", b["hucreler"], "ciftler", b["tohum_ciftleri"])
        ka = F["K-a"]
        print("KA", {k: ka[k] for k in ka if k != "sinama"})
        print("KAsin", ka["sinama"])
        print("KB", F["K-b"])
        print("KC", F["K-c"])
        print("p", F["p_ham"], F["p_holm"], F["karar"])
        print("duy006", F["duyarlilik_delta_0.06"])
        print("panel", d.get("panel"))
        print("veri", {k: v for k, v in d["veri"].items() if k != "girdi_sha256"})
        print("n girdi", len(d["veri"].get("girdi_sha256", {})))
    else:
        print(json.dumps(d, ensure_ascii=False)[:2500])
