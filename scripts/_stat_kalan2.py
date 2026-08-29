#!/usr/bin/env python3
"""S6 (A kolu kaldirac), S8 (L2 ucuncu ongoru entailment) ve yardimci sayilar."""
import json
from pathlib import Path

import numpy as np

ROOT = Path("/workspace")


def bas(s):
    print("\n" + "=" * 70 + f"\n{s}\n" + "=" * 70)


bas("S6/S7: iki kol fit dosyasi")
p = ROOT / "results/q1/e3_iki_kol_fit.json"
j = json.loads(p.read_text(encoding="utf-8"))


def ozet(o, yol="", d=0):
    if d > 3:
        return
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, list) and len(v) > 8:
                print(f"  {yol}.{k}: liste[{len(v)}]")
            else:
                ozet(v, f"{yol}.{k}" if yol else k, d + 1)
    else:
        print(f"  {yol} = {o}")


ozet(j)

bas("A kolu: SVHN payi ve kaldirac")
a = ROOT / "results/q1/e3_a_kolu.json"
for aday in ROOT.glob("results/q1/*a_kol*"):
    print("  dosya:", aday.name)
for aday in ROOT.glob("results/q1/e3_*.json"):
    print("  q1:", aday.name)

bas("S8: L2 ucuncu ongoru Denklem (1)'den turuyor mu?")
# Eger sapma = e*(1-r_cond) ise, sapmanin e'ye gore egimi (1 - r_cond)'dur.
# Yani egim +0.914 -> ortalama kosullu oran ~0.086. Bagimsiz bir sinama degil.
for ad, yol in (("L2", "results/q1/e5_l2_ozet.json"),
                ("Linf", "results/c1_transfer/c1_transfer_summary.json")):
    q = ROOT / yol
    print(f"  {ad}: {'VAR' if q.exists() else 'YOK'}  {yol}")
for aday in sorted(ROOT.glob("results/q1/*l2*")) + sorted(ROOT.glob("results/q1/*L2*")):
    print("  l2 artefakti:", aday.name)

bas("CIFAR-100 temiz dogruluk farki (05:21'deki '11 or 21' kontrolu)")
for aday in sorted(ROOT.glob("results/q1/*c100*")) + sorted(ROOT.glob("results/q1/*cifar100*")):
    print("  c100 artefakti:", aday.name)
