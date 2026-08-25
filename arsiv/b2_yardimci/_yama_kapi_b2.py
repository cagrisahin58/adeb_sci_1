#!/usr/bin/env python3
"""KAPIYA B2 MUHAFIZI: A kolu yeniden kosulana kadar makale GECEMEZ.

Neden bir NOT degil de bir KAPI: 'successful_source' tanimi 2026-08-25'te
duzeltildi (gevsek -> siki). Dort veri kumesinin tablolari ve B kolu yeniden
uretildi; A kolu (GPU, 116 kontrol noktasi) yeniden kosuluyorken durduruldu.
Bu sure boyunca makaledeki iki-kol paragrafi ESKI tanimla hesaplanmis A kolu
egimlerini tasimaktadir. Bir yorum satiri unutulabilir; kirmizi bir kapi
unutulamaz.

Muhafiz sartlari (hepsi saglaninca GECER):
  1. results/q1/e3_akolu_v2 altinda 116 nokta var,
  2. hepsi 'ck_tohum' alani tasiyor (kontrol-noktasi-basina tohumlama),
  3. results/q1/e3_iki_kol_fit.json bu dizinden uretilmis
     ('kaynak_dizin' alani e3_akolu_v2'yi gosteriyor).
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/scripts/check_manuscript_claims.py")
t = p.read_text(encoding="utf-8")

if "B2 MUHAFIZI" in t:
    print("zaten yamali")
    sys.exit(0)

ESKI = 'print(f"{\'KONTROL\':52s} DURUM")'

YENI = '''# --- H: B2 MUHAFIZI -- A kolu duzeltilmis tanimla yeniden kosuldu mu ---
# 'successful_source' tanimi 2026-08-25'te duzeltildi. Tablolar ve B kolu
# yeniden uretildi; A kolu (GPU) yarim kaldi. Bu kapi, A kolu bitmeden
# makalenin "temiz" gorunmesini ENGELLER.
_av2 = ROOT / "results/q1/e3_akolu_v2"
_v2 = sorted(_av2.glob("*.json")) if _av2.is_dir() else []
_tohumlu = sum(1 for f in _v2 if '"ck_tohum"' in f.read_text(encoding="utf-8"))
kontrol("H1. A kolu B2 tanimiyla YENIDEN KOSULDU (116 nokta)",
        len(_v2) == 116 and _tohumlu == 116,
        f"{len(_v2)}/116 nokta, {_tohumlu} tohumlu")

_ikk = ROOT / "results/q1/e3_iki_kol_fit.json"
_ikk_metin = _ikk.read_text(encoding="utf-8") if _ikk.exists() else ""
kontrol("H2. Iki-kol uydurmasi YENI A kolundan uretildi",
        "e3_akolu_v2" in _ikk_metin,
        "e3_iki_kol_fit.json hala eski A kolunu gosteriyor" if _ikk_metin else "dosya yok")

print(f"{'KONTROL':52s} DURUM")'''

if t.count(ESKI) != 1:
    print(f"YAMA BASARISIZ: {t.count(ESKI)} eslesme")
    sys.exit(1)

p.write_text(t.replace(ESKI, YENI, 1), encoding="utf-8")
print("yamalandi: kapiya B2 muhafizi eklendi")
