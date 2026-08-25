#!/usr/bin/env python3
"""B2 sonrasi METNE yazilacak her sayiyi tek yerde basar."""
import json
from pathlib import Path

import numpy as np

ROOT = Path("/workspace")


def jl(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


def blok(ad, yol):
    t = jl(yol)
    print(f"\n===== {ad} =====")
    for p, v in t["protocols"].items():
        if p.endswith("_loose"):
            continue
        print(f"  {p:20s} {v['CNN_to_ViT']['mean']:6.2f}+/-{v['CNN_to_ViT']['std']:.2f}  "
              f"{v['ViT_to_CNN']['mean']:6.2f}+/-{v['ViT_to_CNN']['std']:.2f}  "
              f"fark {v['diff']['mean']:+6.2f}+/-{v['diff']['std']:.2f}  "
              f"n {v['n_cond_CNN_to_ViT']['mean']:.0f}/{v['n_cond_ViT_to_CNN']['mean']:.0f}")
    d = [t["protocols"][p]["diff"]["mean"] for p in
         ("raw", "target_correct", "both_correct", "successful_source")]
    print(f"  aralik {min(d):+.2f} .. {max(d):+.2f}   ort-aciklik {max(d)-min(d):.2f}   "
          f"kat {max(map(abs,d))/min(map(abs,d)):.2f}")
    print(f"  tohum-basina yayilim {t['protocol_spread_pp']['mean']:.2f}"
          f"+/-{t['protocol_spread_pp']['std']:.2f}")
    b = t["both_correct_paired"]
    print(f"  esli fark {b['diff_pp']['mean']:.2f}+/-{b['diff_pp']['std']:.2f}  "
          f"GA [{b['ci_low']['mean']:.2f}, {b['ci_high']['mean']:.2f}]  "
          f"perm p max {b['perm_p_max']:.5f}  TOST esdeger mi {b['tost_equivalent_any']}")


blok("CIFAR-10 Linf", "results/c1_transfer/c1_transfer_summary.json")
blok("CIFAR-100", "results/q1/cifar100/transfer/e1_transfer_summary.json")
blok("SVHN", "results/q1/svhn/transfer/e7_transfer_summary.json")
blok("CIFAR-10 L2", "results/q1/cifar10_l2/transfer/e6_l2_transfer_summary.json")

print("\n===== SURUCU AYRISTIRMA (B kolu, kayitli bilesim) =====")
s = jl("results/q1/e3_surucu_ayristirma.json")
for k in ("A_dort_protokol", "B_uc_protokol"):
    if k in s:
        v = s[k]
        print(f"  {k:18s} egim {v['egim']:+.4f}  r {v['pearson_r']:+.3f}  "
              f"GA [{v['egim_GA95'][0]:+.3f}, {v['egim_GA95'][1]:+.3f}]")
print("  uc olma sayilari:", json.dumps(s.get("uc_sayaci", {}), ensure_ascii=False))
cp = s.get("protokol_cifti_ortalama_aciklik", {})
for k, v in sorted(cp.items(), key=lambda kv: -kv[1]["ort_aciklik"])[:3]:
    print(f"  en genis cift {k:46s} {v['ort_aciklik']:.2f}")

print("\n===== SVHN DUYARLILIGI (B kolu bilesimi) =====")
a = jl("results/q1/e3_asimetri_fit.json")
asv = jl("results/q1/e3_asimetri_fit_svhnli.json")
for ad, d in (("kayitli (SVHN'siz)", a), ("SVHN dahil", asv)):
    print(f"  {ad:20s} n={len(d['ciftler'])} kume={len(set(c['kume'] for c in d['ciftler']))} "
          f"egim {d['fit']['egim']:+.4f}  GA [{d['fit']['egim_GA95'][0]:+.4f}, "
          f"{d['fit']['egim_GA95'][1]:+.4f}]")

print("\n===== VARYANS ORANI =====")
v = jl("results/q1/variance_ratio.json")
print("  ORAN_ACIKLIGI:", json.dumps(v["ORAN_ACIKLIGI"], ensure_ascii=False))
for ad, blk in v.items():
    if isinstance(blk, dict) and "degerler" in blk:
        print(f"  {ad}: {blk['degerler']}")

print("\n===== KACAK-ETKILI KARSILASTIRMA (rev2_blockA) =====")
r = jl("results/rev2_blockA/a2_transfer_protocols.json")["protocols"]
for p in ("raw", "target_correct", "both_correct", "successful_source"):
    print(f"  {p:20s} fark {r[p]['diff_CNNtoViT_minus_ViTtoCNN']:+.2f}")
print(f"  (gevsek varyant   fark {r['successful_source_loose']['diff_CNNtoViT_minus_ViTtoCNN']:+.2f})")
