# -*- coding: utf-8 -*-
"""Masa incelemesi (31.10.2026): konsey_ek_masa ciktilarinin ozetini yazar (sayi uretmez, yalniz okur)."""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
for f in sys.argv[1:]:
    d = json.load(open(f, encoding="utf-8"))
    print("==", f, d["meta"]["betik_sha256"], "girdi", len(d["meta"]["girdi_sha256"]))
    for k, v in d.items():
        if k in ("meta", "tanim", "tanim_S10_3", "tanim_6_2_yeniden_uretim"):
            continue
        print(" ", k, json.dumps(v, ensure_ascii=False)[:2500])
