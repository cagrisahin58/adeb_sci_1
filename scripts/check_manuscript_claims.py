#!/usr/bin/env python3
"""Makale IDDIA denetimi: nitelemeler duruyor mu, yasak ifade girdi mi?

Kalici kapi olarak tutulur (cikis kodu 0/1). Ilk olarak IS-2 kabul olcutu
icin yazildi; sonraki her yeniden yazimda REGRESYON MUHAFIZIDIR -- ornegin
"ucu de dogrulandi" ifadesi geri gelirse burada yakalanir (EK I.3).

Kontroller:
  A. paper/ altinda CIFAR-100 geciyor mu (once SIFIR kez geciyordu)
  B. uc OLGUSAL YANLIS cumle duzeltildi mi
  C. DORT ZORUNLU NITELEME metinde mi
  D. YASAK ifadeler yok mu ("ucu de dogrulandi" ailesi, E2 oran mansети)
"""
import re
import sys
from pathlib import Path

R = Path("/home/firat/projects/adeb_sci_1/paper")
EN = (R / "manuscript").rglob("*.tex")
TR = (R / "manuscript_tr").rglob("*.tex")
en = "\n".join(p.read_text(encoding="utf-8") for p in EN)
tr = "\n".join(p.read_text(encoding="utf-8") for p in TR)

sonuc = []


def kontrol(ad, tamam, ayrinti=""):
    sonuc.append((ad, tamam, ayrinti))


# --- A: CIFAR-100 var mi ---
kontrol("A. EN'de CIFAR-100 geciyor", en.count("CIFAR-100") > 0, f"{en.count('CIFAR-100')} kez")
kontrol("A. TR'de CIFAR-100 geciyor", tr.count("CIFAR-100") > 0, f"{tr.count('CIFAR-100')} kez")

# --- B: uc olgusal yanlis DUZELTILDI mi (eski metin ARTIK YOK) ---
kontrol("B1. EN 'we have not measured that dependence' KALKTI",
        "we have not measured that dependence" not in en)
kontrol("B1. TR 'bu bağımlılığı ölçmedik' KALKTI",
        "bu bağımlılığı ölçmedik" not in tr)
kontrol("B2. EN 'A controlled leakage ablation would settle' KALKTI",
        "A controlled leakage ablation would settle" not in en)
kontrol("B2. TR 'Kontrollü bir sızıntı ablasyonu, kontrol noktası' KALKTI",
        "Kontrollü bir sızıntı ablasyonu, kontrol noktası" not in tr)
kontrol("B3. EN 'Three sources of variance' KALKTI",
        "Three sources of variance" not in en and "three sources of variance" not in en)
kontrol("B3. TR 'üç varyans kaynağı' KALKTI",
        "üç varyans kaynağı" not in tr and "Üç varyans kaynağını" not in tr)
kontrol("B3b. EN 'four sources' VAR", "four sources of variance" in en.lower())
kontrol("B3b. TR 'dört varyans kaynağı' VAR", "ört varyans kaynağ" in tr)

# --- C: DORT ZORUNLU NITELEME ---
# 1) E1 marj sinirlamasi: 0,22 ve 0,48 marjlari E2 genligiyle (1,58-2,85) yan yana
kontrol("C1. EN E1 marj sinirlamasi", "0.22" in en and "0.48" in en and "1.58" in en and "2.85" in en)
kontrol("C1. TR E1 marj sinirlamasi",
        "0{,}22" in tr and "0{,}48" in tr and "1{,}58" in tr and "2{,}85" in tr)
# 2) E2 karsi-agirligi: 25 epok / 0,32 puan
kontrol("C2. EN E2 karsi-agirligi", re.search(r"\$25\$ epochs", en) is not None and "0.32" in en)
kontrol("C2. TR E2 karsi-agirligi", "$25$ epok" in tr and "0{,}32" in tr)
# 3) B.4 madde 3 nitelemesi: "not testable" / "sinanamadi"
kontrol("C3. EN 'not testable in this design'", "not testable in this design" in en)
kontrol("C3. TR 'bu tasarımda sınanamadı'", "bu tasarımda sınanamadı" in tr)
# 4) E2 taahhudun ZAYIF surumunu karsiliyor
kontrol("C4. EN 'weaker question'", "weaker question" in en)
kontrol("C4. TR 'daha zayıf bir sürümünü'", "daha zayıf bir sürümünü" in tr)

# --- D: YASAK ifadeler ---
yasak_en = ["all three predictions", "all three of the predictions", "three of three",
            "all three were confirmed", "all three confirmed"]
yasak_tr = ["üçü de doğrulandı", "üçünü de doğrulad", "her üç ön kestirim doğruland"]
kontrol("D1. EN 'ucu de dogrulandi' ailesi YOK",
        not any(y in en.lower() for y in yasak_en),
        str([y for y in yasak_en if y in en.lower()]))
kontrol("D1. TR 'ucu de dogrulandi' ailesi YOK",
        not any(y in tr for y in yasak_tr),
        str([y for y in yasak_tr if y in tr]))
# E2 oran mansetlenmemeli: "kat" iddiasi E2 baglaminda gecmemeli
kontrol("D2. EN E2 orani mutlak birimle sunuluyor",
        "deliberately not as a ratio to seed-level dispersion" in en)
kontrol("D2. TR E2 orani mutlak birimle sunuluyor",
        "bilinçli olarak tohum düzeyi yayılıma oran biçiminde vermiyoruz" in tr)

print(f"{'KONTROL':52s} DURUM")
print("-" * 72)
kalan = 0
for ad, ok, ayr in sonuc:
    print(f"{ad:52s} {'GECTI' if ok else 'KALDI'}  {ayr}")
    if not ok:
        kalan += 1
print("-" * 72)
print(f"TOPLAM={len(sonuc)}  KALAN={kalan}")
sys.exit(1 if kalan else 0)
