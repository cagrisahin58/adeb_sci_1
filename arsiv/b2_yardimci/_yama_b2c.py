#!/usr/bin/env python3
"""B2 yamasi, ucuncu parca: A kolu kaydina GEVSEK varyant da yazilir.

Gerekce: yeni kosumun gevsek degeri, eski artefaktin `successful_source`
degeriyle BIREBIR tutmali. Tutuyorsa yeniden kosum deterministik demektir
ve siki degere guvenilebilir; tutmuyorsa yeniden kosumun kendisi supheli
demektir ve bunu SESSIZ gecemeyiz.
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/scripts/q1_e3_akolu.py")
t = p.read_text(encoding="utf-8")

if "asimetri_gevsek" in t:
    print("zaten yamali")
    sys.exit(0)

CIFTLER = [
    ('PROTOKOLLER = ["raw", "target_correct", "both_correct", "successful_source"]',
     "PROTOKOLLER = PROTO.PROTOKOLLER          # TEK KAYNAK\n"
     "GEVSEK = PROTO.TANI_PROTOKOLLERI[0]      # geri-uyum/gerileme kontrolu",
     "PROTOKOLLER"),
    ('''            "asimetri": {k: round(v, 4) for k, v in asim.items()},
            "y_asimetri_yayilimi": max(asim.values()) - min(asim.values()),''',
     '''            "asimetri": {k: round(v, 4) for k, v in asim.items()},
            "y_asimetri_yayilimi": max(asim.values()) - min(asim.values()),
            # GERILEME KONTROLU: bu deger, 2026-08-25 oncesi artefaktlarin
            # "successful_source" degeriyle birebir tutmali.
            "asimetri_gevsek_successful_source": round(
                ileri[GEVSEK] - geri[GEVSEK], 4),''',
     "kayit"),
]

for eski, yeni, ad in CIFTLER:
    if t.count(eski) != 1:
        print(f"YAMA BASARISIZ ({ad}): {t.count(eski)} eslesme")
        sys.exit(1)
    t = t.replace(eski, yeni, 1)

p.write_text(t, encoding="utf-8")
print("yamalandi: A kolu artik gevsek varyanti da kaydediyor")
