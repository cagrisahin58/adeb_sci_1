# -*- coding: utf-8 -*-
"""SAHTE ciktisinda gercek C1 modellerinin B2 nicelikleri (K-a q, K-b rho_V) gorunuyor mu?"""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
S = json.load(open("results/q1/konsey_sahte_2x2_sinama.json", encoding="utf-8"))
print("ust anahtarlar:", list(S))
b2 = S.get("b2", {})
print("b2 ust:", list(b2))
bb = b2.get("b2", {})
print("hucreler:", bb.get("hucreler"), "ciftler:", bb.get("tohum_ciftleri"))
print("panel:", b2.get("panel"))
F = bb.get("F_B2", {})
ka = F.get("K-a", {})
print("K-a q:", ka.get("q"), "D:", ka.get("D"))
kb = F.get("K-b", {})
print("K-b degerler:", kb.get("degerler"), "ort:", kb.get("ort"), "ci90:", kb.get("ci90"))
print("karar:", F.get("karar"))
ty = json.load(open("results/q1/_konsey_sahte/sahte_hucre_tablosu.json", encoding="utf-8"))
print("sahte tablo V-scr/C1-R32 uyeleri:", {a: v["hucre"] for a, v in ty["modeller"].items() if v["hucre"] in ("V-scr", "C1-R32")})
print("sahte b2_tohum_ciftleri:", ty.get("b2_tohum_ciftleri"))
print("esleme:", json.dumps(ty.get("dizin_takma_ad_esleme"), ensure_ascii=False)[:800])
