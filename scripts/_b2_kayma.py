#!/usr/bin/env python3
"""Akis ayrimindan sonra RASTGELE niceliklerin kaymasini raporlar.

Belirlenimci nicelikler (oranlar, paydalar, fark) zaten birebir tutuyor.
Burada yalniz Monte Carlo nicelikleri: bootstrap GA'lari, permutasyon p,
TOST p. Amac: makalede ALINTILANAN basamakta bir sey degisiyor mu.
"""
import json
from pathlib import Path

ROOT = Path("/workspace")
YENI = ROOT / "results/q1/_b2_gerileme"
DIZINLER = [
    "results/c1_transfer/pair1", "results/c1_transfer/pair2", "results/c1_transfer/pair3",
    "results/q1/cifar100/transfer/pair1", "results/q1/cifar100/transfer/pair2",
    "results/q1/cifar100/transfer/pair3",
    "results/q1/svhn/transfer/pair1", "results/q1/svhn/transfer/pair2",
    "results/q1/cifar10_l2/transfer/pair1", "results/q1/cifar10_l2/transfer/pair2",
    "results/q1/cifar10_l2/transfer/pair3",
]

print(f"{'cift':<38}{'esli GA (eski)':>22}{'esli GA (yeni)':>22}{'kayma':>16}")
en_buyuk = 0.0
for d in DIZINLER:
    e = json.loads((ROOT / d / "a2_transfer_protocols.json").read_text())["both_correct_paired"]
    y = json.loads((YENI / d.replace("/", "_")).with_suffix(".json").read_text())["both_correct_paired"]
    ea, eb = e["paired_bootstrap_ci95_pp"]
    ya, yb = y["paired_bootstrap_ci95_pp"]
    k = max(abs(ya - ea), abs(yb - eb))
    en_buyuk = max(en_buyuk, k)
    print(f"{d:<38}[{ea:>7.2f},{eb:>7.2f}]   [{ya:>7.2f},{yb:>7.2f}]{k:>16.3f}")

print(f"\nen buyuk GA kaymasi: {en_buyuk:.3f} puan")

print(f"\n{'cift':<38}{'perm p eski':>14}{'perm p yeni':>14}   TOST(esdeger mi) eski -> yeni")
for d in DIZINLER:
    e = json.loads((ROOT / d / "a2_transfer_protocols.json").read_text())["both_correct_paired"]
    y = json.loads((YENI / d.replace("/", "_")).with_suffix(".json").read_text())["both_correct_paired"]
    te = [e["tost_sensitivity"][m]["equivalent_at_0.05"] for m in ("margin_1pp", "margin_2pp", "margin_3pp")]
    ty = [y["tost_sensitivity"][m]["equivalent_at_0.05"] for m in ("margin_1pp", "margin_2pp", "margin_3pp")]
    bayrak = "" if te == ty else "   <<< TOST HUKMU DEGISTI"
    print(f"{d:<38}{e['signflip_permutation_p']:>14.5f}{y['signflip_permutation_p']:>14.5f}   {te} -> {ty}{bayrak}")

# toplulastirilmis SVHN degeri (makalede alintilanan)
sv = [json.loads((YENI / f"results_q1_svhn_transfer_pair{i}.json").read_text())["both_correct_paired"]
      for i in (1, 2)]
sv_eski = [json.loads((ROOT / f"results/q1/svhn/transfer/pair{i}/a2_transfer_protocols.json").read_text())["both_correct_paired"]
           for i in (1, 2)]
print(f"\nSVHN perm p (max, makalede 0,105 yaziyor): "
      f"eski {max(s['signflip_permutation_p'] for s in sv_eski):.5f} -> "
      f"yeni {max(s['signflip_permutation_p'] for s in sv):.5f}")
