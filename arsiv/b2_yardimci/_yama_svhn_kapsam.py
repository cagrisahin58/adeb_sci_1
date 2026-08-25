#!/usr/bin/env python3
"""B kolunun ON-KAYITLI bilesimini KODA yazar.

E3_YENIDEN_TASARIM EK E.1, B kolunu 18 nokta / 6 kume olarak sabitler ve
EK E.5, SVHN'e AYRI bir rol verir: "E3'un noktalarindan degil, SVHN'in kendi
uctan uca analizinden gelen BAGIMSIZ tutarlilik kontrolu."

2026-08-25'te SVHN icin B kolu noktalari da uretilebilir hale geldi (transfer
artefaktlari artik tam semali). Bunlari uydurmaya sessizce eklemek, kayitli
bilesimi SONUC GORULDUKTEN SONRA degistirmek olurdu. Bu yuzden:

  - varsayilan: SVHN uydurmaya GIRMEZ (kayitli bilesim, 18 nokta / 6 kume),
  - E3B_SVHN=1 ile GIRER ve DUYARLILIK olarak raporlanir.

Ikisinin farki makalede aciktan yazilir: SVHN eklendiginde dort protokollu
gozlemsel egim -0,567'den -0,133'e gecer ve guven araligi sifiri icerir.
Bu, makalenin ZATEN yazdigi "o egim 7,2 puanlik olculmemis bir bosluk
uzerinden gecer" uyarisinin nicel karsiligidir.
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/scripts/q1_e3_asimetri.py")
t = p.read_text(encoding="utf-8")

if "E3B_SVHN" in t:
    print("zaten yamali")
    sys.exit(0)

ESKI = '''pts = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(PTS.glob("*.json"))]
if not pts:
    raise SystemExit(f"HATA: {PTS} bos")'''

YENI = '''# --- ON-KAYITLI BILESIM (EK E.1/E.5) ---
# B kolu 18 nokta / 6 kumedir; SVHN uydurmaya girmez, BAGIMSIZ tutarlilik
# kontrolu olarak kullanilir. E3B_SVHN=1 duyarlilik kolunu acar.
SVHN_DAHIL = os.environ.get("E3B_SVHN", "0") == "1"

pts = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(PTS.glob("*.json"))]
if not pts:
    raise SystemExit(f"HATA: {PTS} bos")

_svhn = [q for q in pts if q.get("dataset") == "svhn"]
if not SVHN_DAHIL:
    pts = [q for q in pts if q.get("dataset") != "svhn"]
    print(f"ON-KAYITLI BILESIM: SVHN'in {len(_svhn)} noktasi uydurmanin DISINDA "
          f"(EK E.5: bagimsiz tutarlilik kontrolu). Duyarlilik icin E3B_SVHN=1.")
else:
    print(f"DUYARLILIK KOLU: SVHN'in {len(_svhn)} noktasi uydurmaya DAHIL "
          f"(kayitli bilesim DEGIL).")'''

if t.count(ESKI) != 1:
    print(f"YAMA BASARISIZ: {t.count(ESKI)} eslesme")
    sys.exit(1)
t = t.replace(ESKI, YENI, 1)

# os import'u
if "\nimport os\n" not in t:
    t = t.replace("import json\nimport re\n", "import json\nimport os\nimport re\n", 1)

# cikti dosyasi da duyarlilik kolunda ayrisir
ESKI_OUT = 'out = ROOT / "results/q1/e3_asimetri_fit.json"'
YENI_OUT = ('out = ROOT / ("results/q1/e3_asimetri_fit_svhnli.json" if SVHN_DAHIL\n'
            '              else "results/q1/e3_asimetri_fit.json")')
if t.count(ESKI_OUT) != 1:
    print("YAMA BASARISIZ: cikti satiri bulunamadi")
    sys.exit(1)
t = t.replace(ESKI_OUT, YENI_OUT, 1)

p.write_text(t, encoding="utf-8")
print("yamalandi: q1_e3_asimetri.py -- kayitli bilesim koda yazildi")
