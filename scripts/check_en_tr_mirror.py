#!/usr/bin/env python3
"""ALTINCI KAPI: Ingilizce ve Turkce surumler gercekten AYNA mi?

NEDEN VAR. Mevcut bes kapinin hepsi SAYILARI ya da belirli IFADELERI
denetliyor. Hicbiri YAPIYI denetlemiyordu. 2026-08-25'te bu bosluk iki
GERCEK kusur sakladigi olculdu:

  1. Turkce Yontem bolumunde "Oznitelik Bozunmasi Metrikleri" basligi,
     iki denklemi ve tanimlariyla birlikte HIC YOKTU -- oysa Turkce Bolum 4
     ayni metrikleri kullaniyor ve raporluyordu.
  2. Ingilizce Tartisma bolumunde Mahmood ve ark.'nin TERS yonlu bulgusuyla
     yuzlesen paragraf HIC YOKTU; Turkce surumde vardi. Gonderilecek surum
     Ingilizce oldugu icin bu, gonderilen metnin eksigiydi.

Ikisi de sayi tasimadigi icin sayi kapisi (137/137) gormedi; ikisi de
muhafizli bir ifade olmadigi icin iddia kapisi da gormedi.

OLCUT. Her bolum ciftinde: alt bolum / alt-alt bolum / tablo / sekil /
denklem / paragraf sayilari ESIT olmalidir. Paragraf esigi (200 karakter)
tablo hucrelerini ve kisa komut satirlarini eler.

Cikis kodu: ayrisma varsa 1, yoksa 0.
"""
import os
import re
import sys
from pathlib import Path

_kok = os.environ.get("MANUSCRIPT_ROOT")
ROOT = Path(_kok) if _kok else (
    Path("/workspace") if Path("/workspace/results").is_dir()
    else Path(__file__).resolve().parents[1])

EN_DIR = ROOT / "paper/manuscript/sections"
TR_DIR = ROOT / "paper/manuscript_tr/sections"

CIFTLER = [
    ("01_introduction.tex", "01_giris.tex"),
    ("02_related_work.tex", "02_ilgili_calismalar.tex"),
    ("03_methodology.tex", "03_yontem.tex"),
    ("04_experiments.tex", "04_deneyler.tex"),
    ("05_discussion.tex", "05_tartisma.tex"),
    ("06_conclusion.tex", "06_sonuc.tex"),
]

PARAGRAF_ESIGI = 200


def olc(p):
    if not p.exists():
        sys.exit(f"KAPI HATASI: {p} yok; denetim yapilmadi.")
    t = p.read_text(encoding="utf-8")
    if not t.strip():
        sys.exit(f"KAPI HATASI: {p} bos; denetim yapilmadi.")
    paragraf = [s for s in t.split("\n")
                if len(s.strip()) > PARAGRAF_ESIGI
                and not s.strip().startswith("\\")
                and not s.strip().startswith("%")]
    return {
        "alt bolum": len(re.findall(r"\\subsection\{", t)),
        "alt-alt bolum": len(re.findall(r"\\subsubsection\{", t)),
        "ad obegi": len(re.findall(r"\\paragraph\{", t)),
        "tablo": len(re.findall(r"\\begin\{table", t)),
        "sekil": len(re.findall(r"\\begin\{figure", t)),
        "denklem": len(re.findall(r"\\begin\{equation", t)),
        "paragraf": len(paragraf),
    }


print(f"{'bolum':26s}{'olcut':16s}{'EN':>5s}{'TR':>5s}  durum")
print("-" * 62)
ayrisma = []
for en_ad, tr_ad in CIFTLER:
    e, t = olc(EN_DIR / en_ad), olc(TR_DIR / tr_ad)
    for k in e:
        esit = e[k] == t[k]
        if not esit:
            ayrisma.append(f"{en_ad} / {tr_ad} :: {k}: EN {e[k]}, TR {t[k]}")
        print(f"{en_ad:26s}{k:16s}{e[k]:>5d}{t[k]:>5d}  "
              f"{'' if esit else 'AYRISMA'}")
    print()

if ayrisma:
    print("SONUC: KALDI -- iki surum AYNA DEGIL:")
    for a in ayrisma:
        print("  -", a)
    print("Bir dilde yapilip otekinde unutulan degisiklik iki surumu sessizce")
    print("ayirir; bu kusur bu projede uc kez cikti.")
    sys.exit(1)
print("SONUC: GECTI -- iki surumun bolum agaci, kayan nesneleri, denklemleri")
print("ve paragraf sayilari birebir tutuyor.")
sys.exit(0)
