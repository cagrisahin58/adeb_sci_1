#!/usr/bin/env python3
"""TUR 4 (A10): MLP alt-blok vs BLOK CIKISI derinlik profili.

Makale Bolum 4.7 sunlari soyluyordu:
  - ViT kaymasi 8-10. bloklar civarinda minimuma iniyor, cikisa toparliyor
  - CLS yolu yama-ortalamasindan yaklasik DORT kat uzaga kayiyor (0,9343 vs 0,9840)
  - "CLS siniflandiricinin okudugu seydir"
Ancak cos_cls YALNIZ .mlp alt-bloklari icin hesaplanmisti. Siniflandirici
son BLOK cikisinin CLS'ini okur. Bu betik iki seriyi yan yana koyar.
"""
import json
from pathlib import Path

import numpy as np

ROOT = Path("/workspace/results/c1_c4")


def seri(d, anahtar, ek=""):
    """blok indeksine gore sirali ortalama kosinus."""
    g = d["vit"].get(anahtar, {})
    if not g:
        return None
    out = {}
    for k, v in g.items():
        ad = k.replace(".mlp", "")
        if not ad.startswith("block"):
            continue
        out[int(ad[5:])] = v["mean"]
    return [out[i] for i in sorted(out)] if out else None


ciftler = []
for p in (1, 2, 3):
    f = ROOT / f"pair{p}/c4_summary.json"
    if f.exists():
        ciftler.append(json.loads(f.read_text(encoding="utf-8")))

print(f"{len(ciftler)} cift okundu\n")
ADLAR = [("cos_cls", "CLS @ MLP alt-blok  (ESKI, makaledeki)"),
         ("cos_block_cls", "CLS @ BLOK cikisi   (YENI, dogru tensor)"),
         ("cos_token_mean", "token-ort @ MLP"),
         ("cos_block_token_mean", "token-ort @ BLOK"),
         ("cos_block_output", "duzlestirilmis @ BLOK")]

seriler = {}
for anahtar, etiket in ADLAR:
    yig = [seri(d, anahtar) for d in ciftler]
    yig = [s for s in yig if s]
    if not yig:
        print(f"{etiket:42s} YOK")
        continue
    m = np.array(yig).mean(0)
    seriler[anahtar] = m
    imin = int(np.argmin(m))
    print(f"{etiket:42s} min blok {imin+1:2d}  deger {m[imin]:.4f}  "
          f"son blok {m[-1]:.4f}")

print("\n" + "=" * 72)
print("MAKALEDEKI IDDIALAR vs OLCUM")
print("=" * 72)
if "cos_cls" in seriler and "cos_block_cls" in seriler:
    a, b = seriler["cos_cls"], seriler["cos_block_cls"]
    print(f"  ESKI (MLP)  : min blok {int(np.argmin(a))+1}, deger {a.min():.4f}")
    print(f"  YENI (blok) : min blok {int(np.argmin(b))+1}, deger {b.min():.4f}")
    print(f"  Makale: 'minimum 8-10. bloklar civari' -> "
          f"{'TUTUYOR' if 8 <= int(np.argmin(b))+1 <= 10 else 'TUTMUYOR'} (yeni seride)")
if "cos_block_cls" in seriler and "cos_block_token_mean" in seriler:
    c, t = seriler["cos_block_cls"], seriler["cos_block_token_mean"]
    oran = (1 - c.min()) / (1 - t.min())
    print(f"\n  Blok cikisinda CLS/token-ort kayma orani: {oran:.2f} kat")
    print(f"    CLS min {c.min():.4f} · token-ort min {t.min():.4f}")
    print(f"  Makale (MLP'de olculmus): 4,1 kat (0,9343 vs 0,9840)")
if "cos_cls" in seriler and "cos_token_mean" in seriler:
    a, t = seriler["cos_cls"], seriler["cos_token_mean"]
    print(f"\n  MLP'de CLS/token-ort orani (eski): "
          f"{(1-a.min())/(1-t.min()):.2f} kat  "
          f"(CLS {a.min():.4f} · token-ort {t.min():.4f})")
