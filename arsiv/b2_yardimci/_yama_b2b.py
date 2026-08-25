#!/usr/bin/env python3
"""B2 yamasi, ikinci parca: A kolu (GPU). Idempotent."""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/scripts/q1_e3_akolu.py")
t = orig = p.read_text(encoding="utf-8")
hata = []

if "protokoller as PROTO" in t:
    print("zaten yamali")
    sys.exit(0)

CIFTLER = [
    ("from src.attacks import PGDAttack  # noqa: E402",
     "from src.analysis import protokoller as PROTO  # noqa: E402\n"
     "from src.attacks import PGDAttack  # noqa: E402",
     "import"),
    ('''def oranlar(tc, aw, sc, sa):
    def r(m):
        return float(100 * aw[m].mean()) if m.sum() else float("nan")
    return {"raw": float(100 * aw.mean()), "target_correct": r(tc),
            "both_correct": r(tc & sc), "successful_source": r(tc & sa)}''',
     '''def oranlar(tc, aw, sc, sa):
    """Tanimlar src/analysis/protokoller.py'den (TEK KAYNAK).

    Gevsek varyant da yazilir: eski artefaktlara karsi GERILEME KONTROLU
    (yeni kosumun gevsek degeri eskisiyle birebir tutmali).
    """
    return PROTO.protokol_oranlari(tc, aw, sc, sa, tani=True)''',
     "oranlar"),
]

for eski, yeni, ad in CIFTLER:
    n = t.count(eski)
    if n != 1:
        hata.append(f"{ad}: {n} eslesme")
        continue
    t = t.replace(eski, yeni, 1)

if hata:
    print("YAMA BASARISIZ -- yazilmadi:", *hata, sep="\n  ")
    sys.exit(1)

p.write_text(t, encoding="utf-8")
print("yamalandi: scripts/q1_e3_akolu.py")
