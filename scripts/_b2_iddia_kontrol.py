#!/usr/bin/env python3
"""Metinde korunan NITEL iddialari yeni sayilara karsi denetler.

Sayilar kapidan geciyor olabilir ama "her zaman", "hicbir", "en genis" gibi
NITEL iddialar sayi degisince sessizce yanlislanir. Kapilar bunlari gormez.
"""
import json
from itertools import combinations
from pathlib import Path

ROOT = Path("/workspace")
P4 = ["raw", "target_correct", "both_correct", "successful_source"]

d = json.loads((ROOT / "results/q1/e3_asimetri_fit.json").read_text(encoding="utf-8"))
ciftler = d["ciftler"]
print(f"B kolu: {len(ciftler)} cift\n")

# --- IDDIA 1: "en genis protokol cifti HER ZAMAN hedef-dogru vs basarili-kaynak"
hedef = ("target_correct", "successful_source")
sayac, ihlal = 0, []
for c in ciftler:
    a = c["asimetri"]
    genis = max(combinations(P4, 2), key=lambda pr: abs(a[pr[0]] - a[pr[1]]))
    if set(genis) == set(hedef):
        sayac += 1
    else:
        ihlal.append((c["kume"], genis, round(abs(a[genis[0]] - a[genis[1]]), 2)))
print(f"IDDIA 'en genis cift HER ZAMAN hedef-dogru vs basarili-kaynak':")
print(f"  {sayac}/{len(ciftler)} ciftte dogru")
if ihlal:
    print("  IHLALLER:")
    for k, g, v in ihlal:
        print(f"    {k}: {g[0]} vs {g[1]} ({v} puan)")
    print("  -> 'her zaman' YAZILAMAZ")
else:
    print("  -> 'her zaman' gecerli")

# --- IDDIA 2: basarili-kaynak kac ciftte UC (max veya min)
mn = sum(1 for c in ciftler if min(c["asimetri"], key=c["asimetri"].get) == "successful_source")
mx = sum(1 for c in ciftler if max(c["asimetri"], key=c["asimetri"].get) == "successful_source")
print(f"\nIDDIA 'SS {len(ciftler)} ciftin 12'sinde en kucuk, 4'unde en buyuk':")
print(f"  en kucuk {mn}, en buyuk {mx}, toplam uc {mn + mx}")

# --- IDDIA 3: her protokolun tohum-duzeyi sd'si 1,5 puanin altinda (CIFAR-10)
t = json.loads((ROOT / "results/c1_transfer/c1_transfer_summary.json").read_text(encoding="utf-8"))
print("\nIDDIA 'herhangi bir protokolun tohum sd'si 1,5 puanin altinda':")
enb = 0.0
for p in P4:
    s = t["protocols"][p]["diff"]["std"]
    enb = max(enb, s)
    print(f"  {p:20s} sd {s:.2f}")
print(f"  en buyuk {enb:.2f} -> {'gecerli' if enb < 1.5 else 'IHLAL'}")

# --- IDDIA 4: SVHN'de dort protokolun ikisi CNN, ikisi ViT lehine
e7 = json.loads((ROOT / "results/q1/svhn/transfer/e7_transfer_summary.json").read_text(encoding="utf-8"))
isaret = {p: e7["protocols"][p]["diff"]["mean"] for p in P4}
arti = [p for p, v in isaret.items() if v > 0]
print(f"\nIDDIA 'SVHN'de iki protokol CNN, iki protokol ViT lehine':")
print(f"  CNN lehine (+): {arti}")
print(f"  -> {'gecerli' if len(arti) == 2 else 'IHLAL'}")

# --- IDDIA 5: CIFAR-10 ve CIFAR-100'de yon 12/12 pozitif
for ad, yol in (("CIFAR-10", "results/c1_transfer/c1_transfer_summary.json"),
                ("CIFAR-100", "results/q1/cifar100/transfer/e1_transfer_summary.json"),
                ("L2", "results/q1/cifar10_l2/transfer/e6_l2_transfer_summary.json")):
    s = json.loads((ROOT / yol).read_text(encoding="utf-8"))
    v = [x for p in P4 for x in s["protocols"][p]["diff"]["values"]]
    print(f"\nIDDIA '{ad}: on iki olcumun tamami pozitif': "
          f"{sum(1 for x in v if x > 0)}/{len(v)}")
