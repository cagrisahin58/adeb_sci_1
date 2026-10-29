#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Yeniden kosulan masa ve sahte sinama ciktilarini depodakilerle karsilastirir.
Zaman damgasi ve yol alanlari disarida birakilir."""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
K = "/home/firat/projects/adeb_sci_1/"
D = K + "raporlar/konsey_2026-10-29/_dondurma_denetimi/"
ATLA = {"uretildi_utc", "sure_s", "hucre_tablosu", "sahte_hucre_tablosu", "cikti", "girdi_sha256", "kaynaklar"}


def duz(o, yol="", out=None):
    if out is None:
        out = {}
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ATLA:
                continue
            duz(v, yol + "." + k if yol else k, out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            duz(v, yol + "." + str(i), out)
    else:
        out[yol] = o
    return out


def karsilastir(a_yol, b_yol, etiket):
    try:
        a = duz(json.load(open(a_yol, encoding="utf-8")))
        b = duz(json.load(open(b_yol, encoding="utf-8")))
    except Exception as e:
        print(etiket, "OKUNAMADI", e)
        return
    ortak = set(a) & set(b)
    farkli = []
    en_buyuk = 0.0
    for k in sorted(ortak):
        x, y = a[k], b[k]
        if isinstance(x, (int, float)) and isinstance(y, (int, float)) and not isinstance(x, bool):
            d = abs(float(x) - float(y))
            if d != d:  # nan
                continue
            en_buyuk = max(en_buyuk, d)
            if d > 1e-9:
                farkli.append((k, x, y))
        elif x != y:
            if isinstance(x, str) and ("/workspace" in x or "dondurma_denetimi" in x or "kok/" in x):
                continue
            farkli.append((k, x, y))
    print(f"{etiket}: anahtar a={len(a)} b={len(b)} ortak={len(ortak)} yalniz_a={len(set(a)-set(b))} "
          f"yalniz_b={len(set(b)-set(a))} farkli={len(farkli)} en_buyuk_sayisal_fark={en_buyuk:.3e}")
    for f in farkli[:12]:
        print("   ", str(f)[:220])
    for k in sorted(set(a) ^ set(b))[:6]:
        print("    yalniz bir tarafta:", k)


m = json.load(open(D + "d9_ayrisim_masa.json", encoding="utf-8"))
print("masa regresyon.gecti =", m["regresyon"]["gecti"], " karsilastirilan =", m["regresyon"]["karsilastirilan"],
      " en_buyuk_mutlak_fark =", m["regresyon"]["en_buyuk_mutlak_fark"],
      " eksik =", len(m["regresyon"]["sentezde_olup_yenide_olmayan"]))
print("masa meta betik_sha256 =", m["meta"]["betik_sha256"], " hucre_tablosu_sha256 =", m["meta"]["hucre_tablosu_sha256"])
karsilastir(K + "results/q1/konsey_masa/konsey_ayrisim_masa.json", D + "d9_ayrisim_masa.json", "konsey_ayrisim_masa")
karsilastir(K + "results/q1/konsey_sahte_2x2_sinama.json", D + "kok/results/q1/konsey_sahte_2x2_sinama.json", "sahte_2x2")
for f in ["sahte_b2.json", "sahte_b2_kc.json", "sahte_b4.json", "sahte_b5.json",
          "sahte_b4_maskeleme_SAHTE_V_IN_a.json", "sahte_b4_maskeleme_ViT_Tiny_AT_s2003.json"]:
    karsilastir(K + "results/q1/_konsey_sahte/" + f, D + "kok/results/q1/_konsey_sahte/" + f, f)
s = json.load(open(D + "kok/results/q1/konsey_sahte_2x2_sinama.json", encoding="utf-8"))
print("sahte ust anahtarlar:", list(s.keys()))
bs = s.get("birim_sinamalari")
if isinstance(bs, dict):
    gecmeyen = [k for k, v in bs.items() if isinstance(v, dict) and v.get("gecti") is False]
    print("birim sinamalari:", len(bs), "gecmeyen:", gecmeyen)
for k in ("gecti", "tum_gecti", "ozet"):
    if k in s:
        print(k, "=", str(s[k])[:400])
