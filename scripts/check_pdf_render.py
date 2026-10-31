#!/usr/bin/env python3
"""SEKIZINCI KAPI: derlenmis PDF'in RENDER'ini denetler.

NEDEN. Yedi kapinin hepsi .tex okur. 2026-09-01'de makale ieeeaccess.cls'e
tasindi; o sinif ozeti ve anahtar kelimeleri \\maketitle'dan ONCE bekler.
Sira korunmayinca ikisini de SESSIZCE dusurdu: PDF bir ay boyunca OZETSIZ
kaldi, yedi kapi da gecti, paketten bagimsiz derleme de gecti (hata yok,
sadece icerik yok). "Gecen bir kontrol, yakaladigini kanitlamaz."

BU KAPI PDF METNINI okur ve sunlari ister:
  - ozetin ilk cumlesi ILK SAYFADA
  - "INDEX TERMS" ILK SAYFADA
  - baslik ILK SAYFADA
  - yazar bandinda kucuk harf dotless-i kalintisi YOK (\\uppercase tuzagi)
  - sayfa sayisi makul aralikta (kaza ile bos/yarim PDF yakalansin)
  - son sayfada biyografiler VAR (EOD sonrasi kesilme yakalansin)

Konteynerde calisir (PyMuPDF): docker exec -w /workspace adeb_eval python ...
Cikis 0 = GECTI, 1 = KALDI.
"""
import re
import sys
from pathlib import Path

try:
    import fitz
except ImportError:
    sys.exit("KAPI HATASI: PyMuPDF yok; konteynerde calistirin.")

ROOT = Path("/workspace") if Path("/workspace/paper").is_dir() else Path.home() / "projects/adeb_sci_1"
# Istege bagli 1. argüman: denetlenecek PDF (oz-sinama gecici PDF verir).
PDF = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "paper/manuscript/main.pdf"
TEX = ROOT / "paper/manuscript/main.tex"

if not PDF.exists():
    sys.exit(f"KAPI HATASI: {PDF} yok; once derleyin.")

# ozetin ilk cumlesini .tex'ten al (sabit metne bagimli olmasin)
tex = TEX.read_text(encoding="utf-8")
m = re.search(r"\\begin\{abstract\}\s*(.+?)[.]", tex, re.DOTALL)
if not m:
    sys.exit("KAPI HATASI: main.tex icinde ozet bulunamadi.")
ozet_ilk = re.sub(r"\s+", " ", m.group(1)).strip()
# PDF metninde satir sonlari/tireleme olabilir: ilk 6 kelimeyi ara
ozet_anahtar = " ".join(ozet_ilk.split()[:6])


def tex_baslik(metin):
    """main.tex'teki \\title{...} govdesi (dengeli parantez), LaTeX'ten arindirilmis duz metin.

    2026-10-31: baslik betige elle yazilmaz; her baslik degisikliginde (10-04 LeCun turu, 10-31
    konsey manseti) kapi eski dizgeyi arayip KALDI veriyordu."""
    m_ = re.search(r"^\\title\{", metin, re.M)
    if not m_:
        return None
    i, der, bas = m_.end(), 1, m_.end()
    while i < len(metin) and der:
        der += {"{": 1, "}": -1}.get(metin[i], 0)
        i += 1
    if der:
        return None
    g = metin[bas:i - 1]
    g = re.sub(r"(?<!\\)%[^\n]*", "", g)                 # yorum
    g = re.sub(r"\\\\(\[[^\]]*\])?|~", " ", g)            # \\ ve ~ -> bosluk
    g = re.sub(r"\\[A-Za-z]+\*?\s*", "", g)              # kalan komut adlari
    g = g.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", g).strip()


baslik = tex_baslik(tex)
if not baslik:
    sys.exit("KAPI HATASI: main.tex icinde \\title{...} bulunamadi.")
# Ana baslik ve alt baslik (ilk ':' ile ayrilir); alt baslik yoksa yalniz ana baslik aranir.
ana_baslik, _, alt_baslik = (s_.strip() for s_ in baslik.partition(":"))

d = fitz.open(PDF)
s1 = re.sub(r"\s+", " ", d[0].get_text())
son = re.sub(r"\s+", " ", d[-1].get_text())
n = len(d)

hata = []


def kontrol(ad, kosul, detay=""):
    print(f"  {'GECTI' if kosul else 'KALDI':6s} {ad}{('  -- ' + detay) if detay and not kosul else ''}")
    if not kosul:
        hata.append(ad)


kontrol("ozet ilk cumlesi ilk sayfada", ozet_anahtar in s1, f"aranan: '{ozet_anahtar}'")
kontrol("INDEX TERMS ilk sayfada", "INDEX TERMS" in s1)
kontrol("ABSTRACT basligi ilk sayfada", "ABSTRACT" in s1)
# 2026-10-31: baslik dizgesi main.tex'ten okunur (eski elle yazilmis dizgeler: 10-04 "The
# Conditioning Set Decides ...", alt baslik "Source-Effect Reading"). Ana baslik ve alt baslik
# AYRI aranir: ikisi ayni on eki tasiyabilir (10-04 hakem gecisi dersi). Satir sonundaki tire
# bolunmesi ("CNN- ViT") birlestirilir.
s1_bitisik = s1.replace("- ", "-")
kontrol("baslik ilk sayfada", ana_baslik in s1_bitisik, f"aranan: '{ana_baslik}'")
if alt_baslik:
    kontrol("alt baslik ilk sayfada", alt_baslik in s1_bitisik, f"aranan: '{alt_baslik}'")

# yazar bandi: buyuk harfli ad icinde kucuk dotless-i (ı) kalmis mi?
band = s1[: s1.find("INTRODUCTION")] if "INTRODUCTION" in s1 else s1[:1500]
kotu = re.findall(r"[A-ZÇĞİÖŞÜ]{2,}ı[A-ZÇĞİÖŞÜı]*", band)
kontrol("yazar bandinda kucuk 'ı' kalintisi yok", not kotu, f"bulunan: {kotu}")
# Ayni tuzak biyografi basliklarinda da (son sayfa): sinif adi buyuk harfe
# cevirir, {\i} yine buyumez. Ilk surum yalniz bandi taradi ve bunu KACIRDI.
kotu_bio = re.findall(r"[A-ZÇĞİÖŞÜ]{2,}ı[A-ZÇĞİÖŞÜı]*", son)
kontrol("biyografi basliklarinda kucuk 'ı' kalintisi yok", not kotu_bio, f"bulunan: {kotu_bio}")

kontrol("sayfa sayisi 15-30 arasinda", 15 <= n <= 30, f"n={n}")
kontrol("son sayfada biyografi var", ("received the" in son) or ("is with the" in son))
kontrol("PDF'te 'undefined' / '??' gonderme yok", "??" not in s1 and "??" not in son)

print("-" * 60)
if hata:
    print(f"SONUC: KALDI -- {len(hata)} render kusuru: " + "; ".join(hata))
    sys.exit(1)
print(f"SONUC: GECTI -- PDF ({n} sayfa) ozet, anahtar kelime, baslik, yazar bandi ve biyografiyi tasiyor.")
