#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Runbook'taki python komutlarini argparse ile ayristirir (calistirmadan).

Konteynerde /workspace altinda kosar. parse_args yamalanir: ayristirma bittiginde
Dur istisnasi atilir, boylece betigin govdesi hic calismaz.
"""
import argparse
import json
import re
import runpy
import shlex
import sys

sys.stdout.reconfigure(encoding="utf-8")
RB = "raporlar/konsey_2026-10-29/KONSEY_RUNBOOK.md"
HT = "raporlar/konsey_2026-10-29/hucre_tablosu.json"
metin = open(RB, encoding="utf-8").read()
tablo = json.load(open(HT, encoding="utf-8"))
adlar = set(tablo["modeller"])


class Dur(Exception):
    pass


_orig = argparse.ArgumentParser.parse_args


def _pa(self, args=None, namespace=None):
    ns = _orig(self, args, namespace)
    raise Dur(ns)


argparse.ArgumentParser.parse_args = _pa

# 1) M12, P7, S12 degiskenlerini runbook'tan cikar
degisken = {}
for ad in ["M12", "P7", "S12"]:
    m = re.search(ad + r'="(.*?)"\n', metin, re.S)
    degisken[ad] = m.group(1).replace("\\\n", " ") if m else ""
    print(ad, "uzunluk", len(degisken[ad]))

# 2) python komutlarini topla: kod bloklari + satir ici backtick
satirlar = metin.replace("\\\n", " ")
for ad, deger in degisken.items():
    satirlar = satirlar.replace("$" + ad, deger)
komutlar = []
for m in re.finditer(r"python (experiments/[\w_]+\.py|scripts/[\w_]+\.py)([^\n`\"]*)", satirlar):
    betik, kalan = m.group(1), m.group(2)
    # yonlendirme ve zincirleme oncesinde kes
    kalan = re.split(r"\s>\s|\s&&\s|\s2>&1|\s\|\s", kalan)[0]
    komutlar.append((betik, kalan.strip()))

print("toplam komut:", len(komutlar))
sonuc = []
for betik, kalan in komutlar:
    argv = shlex.split(kalan)
    kayit = {"betik": betik, "argv_bas": " ".join(argv)[:160]}
    sys.argv = [betik] + argv
    try:
        runpy.run_path(betik, run_name="__main__")
        kayit["durum"] = "AYRISTIRMA OLMADAN BITTI"
    except Dur as e:
        ns = vars(e.args[0])
        kayit["durum"] = "AYRISTI"
        # takma ad denetimi
        bilinmeyen = []
        for k in ("model",):
            for spec in ns.get(k) or []:
                takma = spec.split(":")[0]
                if takma not in adlar:
                    bilinmeyen.append(takma)
        for spec in ns.get("rb_model") or []:
            takma = spec.split(":")[-1]
            if takma not in adlar:
                bilinmeyen.append(takma)
        for takma in ns.get("sources") or []:
            if takma not in adlar:
                bilinmeyen.append(takma)
        for takma in ns.get("maskeleme_isaretli") or []:
            if takma not in adlar:
                bilinmeyen.append(takma)
        kayit["tablo_disi_takma"] = bilinmeyen
        kisa = {k: v for k, v in ns.items() if k not in ("model",)}
        kayit["ns"] = {k: (v if not isinstance(v, list) or len(v) < 8 else f"liste[{len(v)}]") for k, v in kisa.items()}
        if ns.get("model"):
            kayit["model_sayisi"] = len(ns["model"])
    except SystemExit as e:
        kayit["durum"] = f"ARGPARSE HATASI (SystemExit {e.code})"
    except Exception as e:
        kayit["durum"] = f"ISTISNA {type(e).__name__}: {e}"
    sonuc.append(kayit)
    print(json.dumps(kayit, ensure_ascii=False, default=str))

# 3) Takma ad sayisi
print("hucre_tablosu model sayisi:", len(adlar))
print("K5 beklenen 20:", len(adlar) == 20)
