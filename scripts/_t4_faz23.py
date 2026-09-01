#!/usr/bin/env python3
"""FAZ 2.3: on kayit beyani kayittan GUCLU idi.

Makale "Before running it we registered ..." diyordu. Git kaydi:
  bb08868  2026-08-17 17:59:33  on kayit eki eklendi
  aae9bfc  2026-08-17 19:05:11  "E1 pilot kapisi ep5'te GECILDI"
Arada 66 dakika var; yani kayit, ILK OLCUMDEN once ama EGITIM BASLADIKTAN
sonra yazilmis. "Kosumdan once" ifadesi bunu ortuyor.

E6 (L2) icin ayni sorun YOK: on kayit b2f38c0 (08-20 16:52), ilk L2
artefakti 86dee28 (08-21 06:45) -- 14 saat sonra. O cumle degismiyor.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

EN = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")
TR = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")

if not uygula([
    ("04_experiments.tex",
     r"Before running it we registered three directional predictions and three "
     r"endpoint bands in an append-only document, so that the outcome could not "
     r"be reinterpreted after the fact.",
     r"We registered three directional predictions and three endpoint bands in "
     r"an append-only document before any measurement from this dataset "
     r"existed, so that the outcome could not be reinterpreted after the fact. "
     r"The registration does not precede the start of training, and we say so "
     r"rather than let ``pre-registered'' be read as preceding the run: the "
     r"registration commit precedes the first reported number, an epoch-5 pilot "
     r"gate, by sixty-six minutes.",
     "2.3 EN on kayit siralamasi"),
], EN):
    sys.exit(1)

if not uygula([
    ("04_deneyler.tex",
     r"Koşumdan önce üç yönsel ön kestirim ile üç uç nokta bandını salt "
     r"eklemeli bir belgeye kaydettik; böylece sonuç, ölçüldükten sonra yeniden "
     r"yorumlanamazdı.",
     r"Üç yönsel ön kestirim ile üç uç nokta bandını, bu veri kümesinden "
     r"herhangi bir ölçüm mevcut olmadan önce salt eklemeli bir belgeye "
     r"kaydettik; böylece sonuç, ölçüldükten sonra yeniden yorumlanamazdı. "
     r"Kayıt, eğitimin başlangıcından önce gelmemektedir ve bunu, ``ön kayıtlı'' "
     r"ifadesinin koşumdan önce anlamına gelmesini engellemek için "
     r"yazıyoruz: kayıt işlemesi, sayı bildiren ilk adımdan, epok 5'teki pilot "
     r"kapısından altmış altı dakika öncedir.",
     "2.3 TR on kayit siralamasi"),
], TR):
    sys.exit(1)
