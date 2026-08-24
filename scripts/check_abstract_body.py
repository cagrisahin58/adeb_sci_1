#!/usr/bin/env python3
"""OZ ile GOVDE tutarliligi: ozdeki her sayinin govdede karsiligi var mi?

NEDEN. Bu projede AYNI kusur sinifi IKI KEZ cikti:
  · IS-1: r=0,997 govdede nitelenmis, MANSETTE nitelenmemis
  · IS-2: E1/E2 govdeye yazilmis, OZDE hic anilmamis
Ikisi de "oz ile govde ayri yasiyor" hatasidir ve hakemin ilk gorecegi seydir.

BU BETIK: ozdeki (main.tex \\begin{abstract}...\\end{abstract}) her SAYIYI
ayiklar ve govde bolumlerinde ariar. Bulunmayanı raporlar.

Yanlis alarmi azaltan kurallar:
  · yil benzeri sayilar (1900-2100) ve tek haneli sayilar atlanir
  · eps gosterimleri (8/255 gibi) atlanir
  · TR/EN ondalik normalizasyonu verify_manuscript_numbers.py ile AYNI

Cikis kodu 0 = tutarli, 1 = ozde govdede olmayan sayi var.
"""
import re
import sys
from pathlib import Path

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"

DILLER = {
    "EN": ("paper/manuscript", ["sections/01_introduction.tex", "sections/02_related_work.tex",
                                "sections/03_methodology.tex", "sections/04_experiments.tex",
                                "sections/05_discussion.tex", "sections/06_conclusion.tex"]),
    "TR": ("paper/manuscript_tr", ["sections/01_giris.tex", "sections/02_ilgili_calismalar.tex",
                                   "sections/03_yontem.tex", "sections/04_deneyler.tex",
                                   "sections/05_tartisma.tex", "sections/06_sonuc.tex"]),
}


def norm_en(t):
    return t.replace("{,}", "").replace(",", "")


def norm_tr(t):
    t = re.sub(r"(?<=\d)\.(?=\d{3}(?!\d))", "", t)
    t = t.replace("{,}", ".")
    return re.sub(r"(?<=\d),(?=\d)", ".", t)


def oz_metni(base):
    m = (ROOT / base / "main.tex").read_text(encoding="utf-8")
    a = re.search(r"\\begin\{abstract\}(.+?)\\end\{abstract\}", m, re.DOTALL)
    if a:
        return a.group(1)
    # IEEEtran bazen \begin{IEEEkeywords} oncesi duz metin kullanir
    a = re.search(r"\\maketitle(.+?)\\begin\{IEEE", m, re.DOTALL)
    return a.group(1) if a else ""


SAYI = re.compile(r"\d+\.\d+|\d+")
ATLA_DESEN = re.compile(r"\d+\s*/\s*255")          # eps gosterimi


def sayilari_ayikla(metin):
    metin = ATLA_DESEN.sub(" ", metin)
    out = []
    for s in SAYI.findall(metin):
        if "." not in s:
            v = int(s)
            if v < 10 or 1900 <= v <= 2100:
                continue                            # tek hane ve yil benzeri
        out.append(s)
    return sorted(set(out), key=lambda x: (len(x), x), reverse=True)


kalan = 0
OZETLER = {}
for dil, (base, dosyalar) in DILLER.items():
    norm = norm_en if dil == "EN" else norm_tr
    oz = norm(oz_metni(base))
    govde = norm("\n".join((ROOT / base / f).read_text(encoding="utf-8")
                           for f in dosyalar if (ROOT / base / f).exists()))
    sayilar = sayilari_ayikla(oz)
    # YUVARLAMAYA DUYARLI ESLESME. Ozetlerde yuvarlamak NORMALDIR (bu makalenin
    # ozu zaten "4,4-14,6" diyor). Kontrolun isi, ozde gecen bir sayinin
    # govdede HIC KARSILIGI OLMAMASINI yakalamaktir; "13,6 vs 13,58" gibi
    # yuvarlama farkini hata saymak yanlis alarmdir.
    govde_sayilari = [float(x) for x in SAYI.findall(govde)]

    def govdede_var(s):
        if s in govde:
            return True
        try:
            v = float(s)
        except ValueError:
            return False
        nd = len(s.split(".")[1]) if "." in s else 0
        return any(round(b, nd) == v for b in govde_sayilari)

    OZETLER[dil] = oz
    eksik = [s for s in sayilar if not govdede_var(s)]
    print(f"=== {dil} === ozde {len(sayilar)} sayi, govdede bulunmayan {len(eksik)}")
    for s in eksik:
        # baglami goster
        m = re.search(r".{45}" + re.escape(s) + r".{45}", oz)
        print(f"   EKSIK {s:>10s}   ...{m.group(0).strip() if m else ''}...")
    kalan += len(eksik)

# --- OZET UZUNLUGU (IEEE Access siniri 250 kelime) ---
UZUNLUK_ESIGI = 280
print("-" * 66)
for dil, oz in OZETLER.items():
    k = len(oz.split())
    durum = "OK" if k <= UZUNLUK_ESIGI else "UZUN"
    print(f"=== {dil} === ozet uzunlugu {k} kelime (esik {UZUNLUK_ESIGI})  {durum}")
    if k > UZUNLUK_ESIGI:
        kalan += 1

print("-" * 66)
if kalan:
    print(f"SONUC: KALDI -- ozde gecip govdede bulunmayan {kalan} sayi var.")
    print("Oz ile govde AYRI YASIYOR demektir; bu kusur bu projede iki kez cikti.")
    sys.exit(1)
print("SONUC: GECTI -- ozdeki her sayinin govdede karsiligi var.")
sys.exit(0)
