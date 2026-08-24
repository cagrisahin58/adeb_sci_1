#!/usr/bin/env python3
"""B2 gerileme karsilastirmasi: yeni a2 ciktisi eski artefakti bozdu mu?"""
import json
import sys
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

DEGISMEMELI = ["raw", "target_correct", "both_correct"]
ALANLAR = ["CNN_to_ViT", "ViT_to_CNN", "diff_CNNtoViT_minus_ViTtoCNN"]

hata, satir = [], []
for d in DIZINLER:
    eski = json.loads((ROOT / d / "a2_transfer_protocols.json").read_text())
    yeni = json.loads((YENI / d.replace("/", "_")).with_suffix(".json").read_text())

    for p in DEGISMEMELI:
        for a in ALANLAR:
            ev = eski["protocols"][p][a]
            yv = yeni["protocols"][p][a]
            ev = ev if not isinstance(ev, dict) else ev["rate"]
            yv = yv if not isinstance(yv, dict) else yv["rate"]
            if ev != yv:
                hata.append(f"{d} {p}.{a}: eski {ev} != yeni {yv}")

    # gevsek varyant eski successful_source ile BIREBIR tutmali
    for a in ALANLAR:
        ev = eski["protocols"]["successful_source"][a]
        yv = yeni["protocols"]["successful_source_loose"][a]
        ev = ev if not isinstance(ev, dict) else ev["rate"]
        yv = yv if not isinstance(yv, dict) else yv["rate"]
        if ev != yv:
            hata.append(f"{d} gevsek.{a}: eski_ss {ev} != yeni_gevsek {yv}")

    # eslesmis analiz (both_correct) hic degismemeli
    for k in ("n_common", "diff_pp", "signflip_permutation_p"):
        if eski["both_correct_paired"][k] != yeni["both_correct_paired"][k]:
            hata.append(f"{d} paired.{k}: {eski['both_correct_paired'][k]} != "
                        f"{yeni['both_correct_paired'][k]}")

    satir.append((d,
                  eski["protocols"]["successful_source"]["diff_CNNtoViT_minus_ViTtoCNN"],
                  yeni["protocols"]["successful_source"]["diff_CNNtoViT_minus_ViTtoCNN"]))

print(f"{'cift':<40}{'SS gevsek(eski)':>18}{'SS siki(yeni)':>16}{'fark':>9}")
for d, e, y in satir:
    print(f"{d:<40}{e:>+18.2f}{y:>+16.2f}{y - e:>+9.2f}")

print()
if hata:
    print("GERILEME VAR -- degismemesi gerekenler degisti:", *hata, sep="\n  ")
    sys.exit(1)
print("GERILEME YOK: raw / target_correct / both_correct ve eslesmis analiz BIREBIR ayni;")
print("gevsek varyant eski successful_source ile BIREBIR tutuyor.")
