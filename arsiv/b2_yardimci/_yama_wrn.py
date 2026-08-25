#!/usr/bin/env python3
"""c10-WRN B kolu betigini TEK KAYNAGA baglar."""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/scripts/q1_e3_bkolu_c10_wrn.py")
t = p.read_text(encoding="utf-8")

if "protokoller as PROTO" in t:
    print("zaten yamali")
    sys.exit(0)

CIFTLER = [
    ('ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"',
     'ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"\n'
     'sys.path.insert(0, str(ROOT))\n'
     'from src.analysis import protokoller as PROTO  # noqa: E402',
     "import"),

    ('''def oranlar(tc, aw, sc, sa):
    """4 protokol orani (yuzde). a2_transfer_protocols ile AYNI tanimlar."""
    def r(m):
        return float(100 * aw[m].mean()) if m.sum() else float("nan")
    return {
        "raw": float(100 * aw.mean()),
        "target_correct": r(tc),
        "both_correct": r(tc & sc),
        "successful_source": r(tc & sa),
    }''',
     '''def oranlar(tc, aw, sc, sa):
    """Tanimlar src/analysis/protokoller.py'den (TEK KAYNAK)."""
    return PROTO.protokol_oranlari(tc, aw, sc, sa, tani=True)''',
     "oranlar"),
]

for eski, yeni, ad in CIFTLER:
    if t.count(eski) != 1:
        print(f"YAMA BASARISIZ ({ad}): {t.count(eski)} eslesme")
        sys.exit(1)
    t = t.replace(eski, yeni, 1)

p.write_text(t, encoding="utf-8")
print("yamalandi: q1_e3_bkolu_c10_wrn.py")
