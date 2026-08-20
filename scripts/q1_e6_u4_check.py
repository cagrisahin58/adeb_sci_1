#!/usr/bin/env python3
"""E6 kural U4 saglamasi: temiz dogruluk SALDIRIDAN BAGIMSIZDIR.

Ayni checkpoint L(infinity) ve L2 degerlendirmelerinde AYNI temiz dogrulugu
vermelidir. Vermiyorsa bir yukleme/on-isleme hatasi vardir ve E6 analizi
DURDURULMALIDIR (E6_ON_KAYIT.md §3 U4).

Bu bir sonuc uretmez; bir SAGLAMA TESTIDIR. Cikis kodu 0 = gecti, 1 = kaldi.
"""
import json
import sys
from pathlib import Path

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
L2DIR = ROOT / "results/q1/cifar10_l2"
TOLERANS = 0.005  # yuzde puan; ayni ckpt + ayni test kumesi -> tam esit olmali

c1 = json.loads((ROOT / "results/c1_seeds/c1_seed_summary.json").read_text(encoding="utf-8"))
linf = {}
for p in c1["pairs"]:
    linf[("resnet18", p["resnet_seed"])] = p["resnet"]["clean"]
    linf[("vit_tiny", p["vit_seed"])] = p["vit"]["clean"]

satirlar, kalan, bulunan = [], 0, 0
for (arch, seed), c_linf in sorted(linf.items()):
    f = L2DIR / f"{arch}_s{seed}" / f"pgd_summary_{arch}.json"
    if not f.exists():
        satirlar.append(f"{arch:9s} s{seed}  L2 ciktisi YOK ({f.name}) -- atlandi")
        continue
    bulunan += 1
    d = json.loads(f.read_text(encoding="utf-8"))
    c_l2 = d.get("clean_acc")
    fark = abs(c_l2 - c_linf)
    ok = fark <= TOLERANS
    if not ok:
        kalan += 1
    satirlar.append(f"{arch:9s} s{seed}  Linf={c_linf:.2f}  L2={c_l2:.2f}  "
                    f"fark={fark:.4f}  {'GECTI' if ok else 'KALDI'}")

print("U4 SAGLAMASI -- temiz dogruluk saldiridan bagimsiz mi?")
print("-" * 64)
for s in satirlar:
    print(" ", s)
print("-" * 64)
if bulunan == 0:
    print("HENUZ L2 CIKTISI YOK -- saglama kosulamadi (hata degil).")
    sys.exit(0)
if kalan:
    print(f"KALDI: {kalan}/{bulunan}. Temiz dogruluk ayni ckpt'te DEGISEMEZ.")
    print("Olasi sebep: farkli normalizasyon, farkli test altkumesi veya yanlis ckpt.")
    print("E6 analizi DURDURULMALI (U4).")
    sys.exit(1)
print(f"GECTI: {bulunan}/{bulunan} model, temiz dogruluk ozdes.")
sys.exit(0)
