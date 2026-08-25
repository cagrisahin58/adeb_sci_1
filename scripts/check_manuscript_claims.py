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
import os
import re
import sys
from pathlib import Path

# MANUSCRIPT_ROOT: oz-sinama kirilmis bir METIN KOPYASINI denetlemek icin
# kullanir. ARTEFAKT okuyan muhafizlar (H1/H2) bu koke BAKMAZ; onlar
# ARTEFAKT_ROOT'tan okur ve varsayilani gercek depodur. Ayrilmasaydi
# oz-sinama, yalniz paper/ kopyalandigi icin bozulmamis kopyada bile
# KALDI verirdi (2026-08-25'te tam bu oldu).
_kok = os.environ.get("MANUSCRIPT_ROOT")
ROOT = Path(_kok) if _kok else (
    Path("/workspace") if Path("/workspace/results").is_dir()
    else Path(__file__).resolve().parents[1])
_avar = os.environ.get("ARTEFAKT_ROOT")
ARTEFAKT_ROOT = Path(_avar) if _avar else (
    Path("/workspace") if Path("/workspace/results").is_dir()
    else Path(__file__).resolve().parents[1])

R = ROOT / "paper"
EN = sorted((R / "manuscript").rglob("*.tex"))
TR = sorted((R / "manuscript_tr").rglob("*.tex"))
if not EN or not TR:
    sys.exit(f"KAPI HATASI: {R} altinda .tex bulunamadi "
             f"(EN={len(EN)}, TR={len(TR)}). Bos metin uzerinde YOKLUK "
             f"kontrolleri sahte gecer; denetim yapilmadi.")
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
kontrol("C3. TR 'bu tasarımda sınanama...'", "bu tasarımda sınanama" in tr)   # cekime duyarsiz govde
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

# --- E: r=0,997 OZDESLIK olarak sunulmali, korelasyon olarak DEGIL (EK J) ---
kontrol("E1. EN ozdeslik turetiliyor",
        "identity" in en.lower() and "eq:raw_identity" in en)
kontrol("E1. TR ozdeslik turetiliyor",
        "özdeşlik" in tr and "eq:raw_identity" in tr)
# olculen oncul metinde olmali: P(adv yanlis | temiz yanlis) = 0,989-1,000
kontrol("E2. EN oncul olcumu", "0.989" in en and "1.000" in en)
kontrol("E2. TR oncul olcumu", "0{,}989" in tr and "1{,}000" in tr)
# ESKI KORELASYON DILI GERI GELMEMELI
_eski_en = ["is almost entirely explained by the target's clean error (r = 0.997)",
            "almost perfectly explained by the clean error"]
kontrol("E3. EN eski korelasyon dili YOK",
        not any(s in en for s in _eski_en),
        str([s[:40] for s in _eski_en if s in en]))

# --- F: protokol yayiliminin IKI surucusu (EK C) ---
# F1 ONCE ZAYIFTI: "second" ve "driver" kelimeleri makalede baska yerlerde de
# geciyor, bu yuzden iddia silinse bile muhafiz GECIYORDU (sentetik regresyon
# sinamasinda yakalandi). Artik AYIRT EDICI ifadeye bagli.
kontrol("F1. EN ikinci surucu aniliyor",
        "second driver tied to" in en and "second and partly opposing term" in en)
kontrol("F1. TR ikinci surucu aniliyor",
        "ikinci bir sürücü ekler" in tr and "ikinci, kısmen ters yönlü bir" in tr)
# mekanizma anlatisi TEK surucuye indirgenmemeli
kontrol("F2. EN mekanizma EKSIK oldugu yaziyor",
        "incomplete" in en.lower() and "three of the four protocols" in en)
kontrol("F2. TR mekanizma EKSIK oldugu yaziyor",
        "eksiktir" in tr and "dört protokolün üçü" in tr)

# --- G: BAYAT KAPSAM IDDIASI (2026-08-21) ---
# Sonuc bolumu Q1 kampanyasi oncesinden kalma "tek veri kumesini
# kapsamaktadir" cumlesini tasiyordu; AYNI PARAGRAF CIFAR-100 ve SVHN
# sonuclarini anlatiyordu. Kusur ne sayidir ne de muhafizli bir ifade,
# yani mevcut kapilarin hicbiri gormezdi. Kapsam iddiasi, makalede
# gercekten kosulmus veri kumesi sayisiyla bagli tutuluyor.
_veri_kumeleri = [k for k in ("CIFAR-10", "CIFAR-100", "SVHN") if k in en]
kontrol("G1. EN kapsam iddiasi veri kumesi sayisiyla tutuyor",
        len(_veri_kumeleri) < 3 or "covers three datasets" in en,
        f"{len(_veri_kumeleri)} veri kumesi kosulmus")
kontrol("G1. TR kapsam iddiasi veri kumesi sayisiyla tutuyor",
        len(_veri_kumeleri) < 3 or "üç veri kümesini" in tr)
kontrol("G2. EN bayat 'one dataset' kapsami YOK",
        "covers one dataset" not in en)
kontrol("G2. TR bayat 'tek veri kümesini kapsamaktadır' YOK",
        "tek veri kümesini kapsamaktadır" not in tr)

# --- H: B2 MUHAFIZI -- A kolu duzeltilmis tanimla yeniden kosuldu mu ---
# 'successful_source' tanimi 2026-08-25'te duzeltildi. Tablolar ve B kolu
# yeniden uretildi; A kolu (GPU) yarim kaldi. Bu kapi, A kolu bitmeden
# makalenin "temiz" gorunmesini ENGELLER.
_av2 = ARTEFAKT_ROOT / "results/q1/e3_akolu_v2"
_v2 = sorted(_av2.glob("*.json")) if _av2.is_dir() else []
_tohumlu = sum(1 for f in _v2 if '"ck_tohum"' in f.read_text(encoding="utf-8"))
kontrol("H1. A kolu B2 tanimiyla YENIDEN KOSULDU (116 nokta)",
        len(_v2) == 116 and _tohumlu == 116,
        f"{len(_v2)}/116 nokta, {_tohumlu} tohumlu")

_ikk = ARTEFAKT_ROOT / "results/q1/e3_iki_kol_fit.json"
_ikk_metin = _ikk.read_text(encoding="utf-8") if _ikk.exists() else ""
kontrol("H2. Iki-kol uydurmasi YENI A kolundan uretildi",
        "e3_akolu_v2" in _ikk_metin,
        "e3_iki_kol_fit.json hala eski A kolunu gosteriyor" if _ikk_metin else "dosya yok")

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
