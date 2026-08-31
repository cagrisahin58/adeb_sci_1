#!/usr/bin/env python3
"""Is akisi ciktisindan uc hukmu ve eylem planlarini okur."""
import io
import json
import sys

F = ("/mnt/c/Users/cagri/AppData/Local/Temp/claude/"
     "--wsl-localhost-Ubuntu-22-04-home-firat-projects-adeb-sci-1/"
     "0d0fab82-c6b8-472d-a420-d8ffb5857ab2/tasks/w19whqcku.output")

_raw = json.load(io.open(F, encoding="utf-8"))
d = _raw.get("result") or _raw.get("hukumler") and _raw or _raw
if "hukumler" not in d:
    for _k in ("result", "output", "value", "data"):
        if isinstance(_raw.get(_k), dict) and "hukumler" in _raw[_k]:
            d = _raw[_k]; break
    else:
        print("ust anahtarlar:", list(_raw.keys())); raise SystemExit(1)
kip = sys.argv[1] if len(sys.argv) > 1 else "ozet"

for h in d["hukumler"]:
    print("=" * 74)
    print(h["alan"])
    print("HUKUM:", h["hukum"])
    eb = h.get("engelleyici_bulgular", [])
    ib = h.get("ikincil_bulgular", [])
    rd = h.get("reddedilen_iddialar", [])
    ep = h.get("eylem_plani", [])
    print(f"engelleyici {len(eb)} · ikincil {len(ib)} · reddedilen {len(rd)} · plan {len(ep)}")

    if kip in ("ozet", "engelleyici"):
        print("\n-- ENGELLEYICI --")
        for b in eb:
            print(f"  * {b['baslik']}")
            if kip == "engelleyici":
                print(f"      neden: {b.get('neden_engelleyici','')[:400]}")
                print(f"      eylem: {b.get('eylem','')[:400]}")
    if kip in ("ozet", "plan"):
        print("\n-- EYLEM PLANI --")
        for a in sorted(ep, key=lambda x: x.get("sira", 99)):
            print(f"  {a.get('sira')}. [{a.get('kim','?')}] {a['is'][:170]}")
            if kip == "plan":
                print(f"      neden: {a.get('neden','')[:260]}")
                print(f"      efor : {a.get('tahmini_efor','')} | bagimlilik: {a.get('bagimlilik','-')}")
    if kip == "ikincil":
        print("\n-- IKINCIL --")
        for b in ib:
            print(f"  * {b['baslik']}\n      -> {b.get('eylem','')[:260]}")
    if kip == "reddedilen":
        print("\n-- REDDEDILEN IDDIALAR --")
        for r in rd:
            print(f"  * {r[:300]}")
    if kip == "gerekce":
        print("\nGEREKCE:\n" + h.get("gerekce", ""))
    print()
