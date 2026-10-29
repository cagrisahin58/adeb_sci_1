#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ON_KAYIT_2026-10-29.md ve KONSEY_PLANI.md §12 uslup denetimi: uzun tire, paragraf basi koyu etiket,
birinci tekil kisi."""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
K = "/home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29/"


def denetle(ad, satirlar, bas=1):
    print("==", ad)
    for i, s in enumerate(satirlar, bas):
        if "—" in s:
            print(f"  UZUN TIRE satir {i}: ...{s[max(0, s.find(chr(0x2014)) - 60):s.find(chr(0x2014)) + 40]}...")
        if "–" in s:
            j = s.find("–")
            print(f"  EN TIRE (bilgi) satir {i}: ...{s[max(0, j - 30):j + 30]}...")
        if re.match(r"^\s*(\d+\.\s+|-\s+)?(\*\*|__)[^*]{1,60}(\*\*|__)", s):
            print(f"  KOYU BAS satir {i}: {s[:100]}")
        if re.match(r"^\s*(\d+\.\s+|-\s+)?\*[^*\s][^*]{0,40}\*[.:]", s):
            print(f"  ITALIK ETIKET satir {i}: {s[:100]}")
        for kalip in [r"\bben\b", r"\bbence\b", r"\bbenim\b", r"\byaptım\b", r"\bbuldum\b", r"\bdüşünüyorum\b",
                      r"\bönerim\b", r"\bönerdim\b", r"\bgördüm\b", r"\bhesapladım\b", r"\bdondurdum\b",
                      r"\bekledim\b", r"\beklendim\b", r"\byazdım\b", r"\bkontrol ettim\b"]:
            for m in re.finditer(kalip, s, re.I):
                print(f"  1. TEKIL satir {i}: ...{s[max(0, m.start() - 40):m.end() + 40]}...")
        # -dım/-dim/-tım/-tim fiil sonu (kaba)
        for m in re.finditer(r"\b\w{3,}(d|t)(ı|i|u|ü)m\b", s):
            w = m.group(0)
            if w.lower() not in {"bilim", "dönüm", "ölçüm", "çözüm", "bölüm", "tutum", "durum", "türüm", "itim",
                                 "eğitim", "üretim", "iletim", "yönetim", "kestirim", "sürdürüm", "giderim",
                                 "işletim", "değişim", "yönelim", "bileşim", "dağıtım", "yatırım", "denetim",
                                 "ayrışım", "karışım", "yetişim", "biçim", "kesim", "geçim", "seçim", "yitim",
                                 "üstüm", "tüketim", "tanıtım", "kurtarım", "uyarım", "anlatım", "aktarım",
                                 "artım", "yaptırım", "katılım", "dışlanım", "kapsam", "yazım", "çekim"}:
                print(f"  -DIM? satir {i}: {w}")


ok = open(K + "ON_KAYIT_2026-10-29.md", encoding="utf-8").read().split("\n")
denetle("ON_KAYIT_2026-10-29.md", ok)
pl = open(K + "KONSEY_PLANI.md", encoding="utf-8").read().split("\n")
bas = next(i for i, s in enumerate(pl) if s.startswith("## 12."))
denetle("KONSEY_PLANI.md §12", pl[bas:], bas + 1)
denetle("KONSEY_PLANI.md satir 112 (5(2))", pl[111:112], 112)
