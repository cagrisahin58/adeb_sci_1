#!/usr/bin/env python3
"""Tur 4 ayrisimi: acikliklari HAM artefakt degerlerinden hesaplar.

Tur 3'te 5,30/5,80 yazmistim cunku yuvarlanmis tablo degerlerinden
turetmistim; dogrusu 5,31/5,79 idi. Ayni hatayi tekrarlamamak icin
CIFAR-100 ve SVHN artik-acikliklari da ham degerlerden gelir.

Tur 4 cercevesi (ONAYLANDI): koşulsuz oran eksen noktasidir.
    yayilim = (ham - hedef_dogru)  +  (basarili_kaynak - ham)
            =   OZDESLIK TERIMI    +   FARKLI ESTIMAND
ve hedef_dogru <-> her_ikisi_dogru, duzeltme SONRASI kalan ARTIK takdirdir.
"""
import json
from pathlib import Path

ROOT = Path("/workspace")


def protokoller(yol, etiket):
    d = json.loads((ROOT / yol).read_text(encoding="utf-8"))

    def ara(o):
        if isinstance(o, dict):
            if "protocols" in o:
                return o["protocols"]
            for v in o.values():
                r = ara(v)
                if r:
                    return r
        return None

    pr = ara(d)
    if pr is None:
        print(f"  {etiket}: 'protocols' yok -> {list(d.keys())[:8]}")
        return None

    def deg(k):
        v = pr.get(k)
        if isinstance(v, dict):
            for a in ("diff", "asimetri", "asymmetry", "fark"):
                if a in v:
                    w = v[a]
                    return w["mean"] if isinstance(w, dict) else w
            if "mean" in v:
                return v["mean"]
        return v

    return {k: deg(k) for k in
            ("raw", "target_correct", "both_correct", "successful_source")}


print("=" * 68)
print("TUR 4 AYRISIMI (ham artefakt degerleri)")
print("=" * 68)

for etiket, yol in (
        ("CIFAR-10", "results/c1_transfer/c1_transfer_summary.json"),
        ("CIFAR-100", "results/q1/cifar100/transfer/e1_transfer_summary.json"),
        ("SVHN", "results/q1/svhn/transfer/e7_transfer_summary.json")):
    P = protokoller(yol, etiket)
    if not P or any(v is None for v in P.values()):
        print(f"\n{etiket}: eksik -> {P}")
        continue
    ozdeslik = P["raw"] - P["target_correct"]
    estimand = P["successful_source"] - P["raw"]
    artik = P["both_correct"] - P["target_correct"]
    yayilim = max(P.values()) - min(P.values())
    print(f"\n{etiket}")
    print(f"  ham {P['raw']:.4f} · hedef-dogru {P['target_correct']:.4f} · "
          f"her-ikisi {P['both_correct']:.4f} · basarili-kaynak {P['successful_source']:.4f}")
    print(f"  OZDESLIK TERIMI (ham - hedef-dogru) = {ozdeslik:7.4f}  -> {ozdeslik:.2f}")
    print(f"  FARKLI ESTIMAND (bas.kaynak - ham)  = {estimand:7.4f}  -> {estimand:.2f}")
    print(f"  ARTIK TAKDIR   (her-ikisi - hedef)  = {artik:7.4f}  -> {artik:.2f}")
    print(f"  toplam ozdeslik+estimand            = {ozdeslik + estimand:7.4f}")
    print(f"  gozlenen yayilim (max-min)          = {yayilim:7.4f}  -> {yayilim:.2f}")
    if abs((ozdeslik + estimand) - yayilim) > 0.005:
        print("  NOT: ham, uc protokol arasinda DEGIL -> iki-parcali bolumleme"
              " bu veri kumesinde tam degil; metinde belirtilmeli.")
