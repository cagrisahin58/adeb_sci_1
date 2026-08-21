#!/usr/bin/env python3
"""Bildirinin tasiyici sayilari Q1 SONRASI makale ile tutuyor mu?

NEDEN VAR: bildiri (paper/bildiri/) dort kapinin HICBIRI tarafindan
taranmiyor ve main ile q1 dallarinda BAYT AYNI, yani Q1 kampanyasi ona hic
dokunmadi. Kampanya bazi anlatilari degistirdi (ornegin SVHN'de asimetrinin
isareti protokole bagli cikti); bildiride eskimis sayi ya da curutulmus
iddia kalmis olabilir. Bu betik onu OLCER.

TASARIM -- neden dize degil SAYI karsilastiriliyor: bildiri 3 anlamli
basamak, makale 4 basamak yaziyor (0,493 ile 0,4928). Duz dize aramasi
iki yonde de yanilir:
  - dize ararsan yuvarlama farkini SAHTE UYUSMAZLIK sayarsin;
  - "dize varsa kontrol et" dersen sayi baska bir degere donustugunde
    kontrol SESSIZCE ATLANIR (oz-sinamanin 1. adimi tam bunu yakaladi:
    37,93 -> 36,00 karantina degeri gorunmez kaliyordu).
Bu yuzden her buyukluk BAGLAM DESENIYLE bildiriden cekilir ve makaledeki
otoriter degerle SAYISAL olarak karsilastirilir. Bildirinin yazdigi
basamak sayisi tolerans olur.

Cikis kodu: uyusmazlik varsa 1, yoksa 0.
"""
import os
import re
import sys
from pathlib import Path

# MANUSCRIPT_ROOT: oz-sinama kirilmis bir KOPYAYI denetlemek icin kullanir.
_kok = os.environ.get("MANUSCRIPT_ROOT")
ROOT = Path(_kok) if _kok else (
    Path("/workspace") if Path("/workspace/results").is_dir()
    else Path(__file__).resolve().parents[1])
R = ROOT / "paper"
b = (R / "bildiri/bildiri.tex").read_text(encoding="utf-8")
en = "\n".join(p.read_text(encoding="utf-8")
               for p in sorted((R / "manuscript").rglob("*.tex")))
if not b.strip() or not en.strip():
    sys.exit("KAPI HATASI: bildiri ya da makale okunamadi; denetim yapilmadi.")

# (etiket, bildirideki baglam deseni [tek yakalama grubu], otoriter deger)
# Otoriter degerler makale Tablo I / Tablo gradyan ve c1_transfer_summary.json
# kaynaklidir; makaledeki tam basamakli halleriyle yazilmistir.
SAYILAR = [
    ("AA ResNet",            r"\((\d+\.\d+)\$\\pm\$0\.14\\% vs",          37.93),
    ("AA ViT",               r"vs (\d+\.\d+)\$\\pm\$0\.40\\%",            29.14),
    ("temiz fark",           r"a (\d+\.\d+)-point clean accuracy",        12.3),
    ("kosullu yaniltma CNN", r"\((\d+\.\d+)\\% vs \d+\.\d+\\% under PGD", 48.58),
    ("kosullu yaniltma ViT", r"\(\d+\.\d+\\% vs (\d+\.\d+)\\% under PGD", 55.53),
    ("protokol alt sinir",   r"\$\+\$(\d+\.\d+) to \$\+\$\d+\.\d+ points", 4.36),
    ("protokol ust sinir",   r"\$\+\$\d+\.\d+ to \$\+\$(\d+\.\d+) points", 14.60),
    ("Hoyer CNN",            r"Hoyer (\d+\.\d+) vs \d+\.\d+",             0.4928),
    ("Hoyer ViT",            r"Hoyer \d+\.\d+ vs (\d+\.\d+)",             0.4561),
    ("hizalanma ViT",        r"absolute cosine \((\d+\.\d+) vs \d+\.\d+", 0.0562),
    ("hizalanma CNN",        r"absolute cosine \(\d+\.\d+ vs (\d+\.\d+)", 0.0378),
]

print(f"{'BUYUKLUK':22s} {'BILDIRIDE':>10s} {'OTORITER':>10s}  DURUM")
print("-" * 60)
uyusmaz = []
for ad, desen, otoriter in SAYILAR:
    m = re.search(desen, b)
    if not m or not m.group(m.lastindex or 1):
        print(f"{ad:22s} {'BULUNAMADI':>10s} {otoriter:>10} KALDI")
        uyusmaz.append(f"{ad}: baglam bildiride bulunamadi "
                       f"(cumle yeniden yazilmis olabilir, elle bakin)")
        continue
    yazilan = m.group(m.lastindex or 1)
    basamak = len(yazilan.split(".")[1])
    tutuyor = round(otoriter, basamak) == float(yazilan)
    print(f"{ad:22s} {yazilan:>10s} {otoriter:>10} "
          f"{'tutuyor' if tutuyor else 'KALDI'}")
    if not tutuyor:
        uyusmaz.append(f"{ad}: bildiri {yazilan}, otoriter deger {otoriter} "
                       f"({basamak} basamaga yuvarlanmisi "
                       f"{round(otoriter, basamak)})")

# Oransal iddia: makalede de 3,3 kat yazili mi (K2 -- kat iddiasi tek basina
# gezmez, alt/ust sinirla birlikte anilir).
print()
for ad, s, kaynak in [("bildiride 3,3 kat", "3.3-fold", b),
                      ("makalede 3,3 kat", "3.3-fold", en)]:
    print(f"  {'VAR' if s in kaynak else 'YOK':4s}  {ad}")
if "3.3-fold" in b and "3.3-fold" not in en:
    uyusmaz.append("bildiri 3,3 kat diyor, makale demiyor")

print()
print("=== Q1 KAMPANYASININ DEGISTIRDIGI IDDIALAR ===")
# Bildiri CIFAR-10 ile sinirli; SVHN'deki isaret cevrilmesi onu CURUTMEZ.
# Ama bunu ANCAK acik sinirlama cumlesi ayakta oldugu surece soyleyebiliriz.
YON = ("The direction, CNN$\\rightarrow$ViT stronger, "
       "is stable across protocols and seeds.")
SINIR = "preliminary results on one dataset and one model pair"
print(f"  {'VAR' if YON in b else 'YOK':4s}  yon protokoller/tohumlar boyunca kararli (CIFAR-10)")
print(f"  {'VAR' if SINIR in b else 'YOK':4s}  tek veri kumesi sinirlamasi ACIK YAZILI")
if YON in b and SINIR not in b:
    uyusmaz.append("yon iddiasi var ama tek-veri-kumesi sinirlamasi YOK; "
                   "SVHN'deki isaret cevrilmesi karsisinda savunulamaz")

print()
print("=== Q1'DE OLUP BILDIRIDE OLMAYAN KONULAR (genisletme payi) ===")
for konu, anahtar in [("SVHN", "SVHN"), ("CIFAR-100", "CIFAR-100"),
                      ("L2 tehdit modeli", "L_2"), ("ozdeslik", "identity"),
                      ("on kayit", "pre-registration"), ("TGR", "TGR")]:
    print(f"  bildiri={'VAR' if anahtar in b else 'YOK':4s} "
          f"makale={'VAR' if anahtar in en else 'YOK':4s}  {konu}")

print()
print(f"Bildiri: {len(b.splitlines())} satir, "
      f"{len(re.findall(chr(92) + chr(92) + 'cite', b))} atif cagrisi")
if uyusmaz:
    print("\nSONUC: KALDI")
    for u in uyusmaz:
        print("  -", u)
    sys.exit(1)
print("\nSONUC: GECTI -- bildirinin tasiyici sayilari makaleyle SAYISAL olarak "
      "tutuyor, curutulmus iddia yok.")
