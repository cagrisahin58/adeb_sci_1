# -*- coding: utf-8 -*-
"""Masa incelemesi (31.10.2026): hucre tablolarinin model alanlari ve mantel JSON model listeleri."""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
K = "raporlar/konsey_2026-10-29/"
for t in ("hucre_tablosu.json", "hucre_tablosu_b9.json", "hucre_tablosu_b8.json"):
    d = json.load(open(K + t, encoding="utf-8"))
    print("==", t, [k for k in d if k != "modeller"])
    for a, v in d["modeller"].items():
        print("  ", a, v)
for v in ("cifar10", "cifar100", "imagenetv2"):
    d = json.load(open(f"results/q1/konsey_b10_gradyan/mantel_{v}.json", encoding="utf-8"))
    print("==", v, d["modeller_ortak"], d.get("dislanan"), d["c_turu"], d["matris_dizinleri"])
    print({k: (s.get("istatistik"), s.get("p_tek")) for k, s in d["sinamalar"].items()})
a = json.load(open("results/q1/konsey_b10_gradyan/b10_aile.json", encoding="utf-8"))
print("== b10_aile keys", list(a.keys()))
print(json.dumps(a, ensure_ascii=False)[:3000])
