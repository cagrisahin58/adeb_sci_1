#!/usr/bin/env python3
"""B2 YAMASI: protokol tanimini kopyalayan betikleri TEK KAYNAGA baglar.

Her yama tekil-eslesme kontrolunden gecer; eslesme 1 degilse HICBIR SEY
yazilmaz ve betik hata koduyla doner.
"""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
hatalar, yazilan = [], []


def yama(rel, cift_listesi):
    p = ROOT / rel
    t = orig = p.read_text(encoding="utf-8")
    for eski, yeni, ad in cift_listesi:
        n = t.count(eski)
        if n != 1:
            hatalar.append(f"{rel} :: {ad}: {n} eslesme (1 bekleniyordu)")
            return
        t = t.replace(eski, yeni, 1)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        yazilan.append(rel)


# --------------------------------------------------------------- a2 (ana tablo)
A2_ESKI = '''def protocol_masks(pair, protocol):
    fool = pair["target_adv_wrong"]
    if protocol == "raw":
        cond = np.ones_like(fool, dtype=bool)
    elif protocol == "target_correct":
        cond = pair["target_clean_correct"]
    elif protocol == "both_correct":
        cond = pair["target_clean_correct"] & pair["source_clean_correct"]
    elif protocol == "successful_source":
        cond = pair["target_clean_correct"] & pair["source_adv_wrong"]
    else:
        raise ValueError(protocol)
    return fool, cond


report = {"seed": 42, "n_bootstrap": N_BOOT, "n_permutation": N_PERM, "protocols": {}}

for protocol in ["raw", "target_correct", "both_correct", "successful_source"]:'''

A2_YENI = '''def protocol_masks(pair, protocol):
    """Maskeler src/analysis/protokoller.py'den gelir (TEK KAYNAK).

    'successful_source' BEYAZ KUTU BASARISIDIR: kaynak temizde dogru VE
    cekismelide yanlis. 'successful_source_loose' terk edilmis gevsek
    varyanttir ve yalniz duyarlilik raporlamasi icin tasinir.
    """
    m = PROTO.maskeler(pair["target_clean_correct"], pair["source_clean_correct"],
                       pair["source_adv_wrong"], tani=True)
    if protocol not in m:
        raise ValueError(protocol)
    return pair["target_adv_wrong"], m[protocol]


report = {"seed": 42, "n_bootstrap": N_BOOT, "n_permutation": N_PERM,
          "ss_definition": "target_clean_correct & source_clean_correct & source_adv_wrong",
          "protocols": {}}

for protocol in PROTO.PROTOKOLLER + PROTO.TANI_PROTOKOLLERI:'''

A2_IMPORT_ESKI = '''import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")'''
A2_IMPORT_YENI = '''import sys

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
sys.path.insert(0, ROOT)
from src.analysis import protokoller as PROTO  # noqa: E402'''

yama("experiments/rev2/a2_transfer_protocols.py",
     [(A2_IMPORT_ESKI, A2_IMPORT_YENI, "import"), (A2_ESKI, A2_YENI, "protocol_masks")])

# --------------------------------------------------------------- B kolu (nokta)
B_ESKI = '''def protocol_rates(clean_ok, adv_wrong, src_clean_ok, src_adv_wrong):
    """q1_e3_calibration.protocol_rates ile AYNI tanimlar (bilerek kopya:
    o dosya torch import ediyor, bu betik GPU'suz calisabilmeli)."""
    def rate(mask):
        return float(100 * adv_wrong[mask].mean()) if mask.sum() else float("nan")
    raw = float(100 * adv_wrong.mean())
    tc = rate(clean_ok)
    bc = rate(clean_ok & src_clean_ok)
    ss = rate(clean_ok & src_adv_wrong)
    vals = [raw, tc, bc, ss]
    return {"raw": raw, "target_correct": tc, "both_correct": bc,
            "successful_source": ss, "raw_minus_cond": raw - tc,
            "spread": max(vals) - min(vals)}'''
B_YENI = '''def protocol_rates(clean_ok, adv_wrong, src_clean_ok, src_adv_wrong):
    """Tanimlar src/analysis/protokoller.py'den (TEK KAYNAK)."""
    r = PROTO.protokol_oranlari(clean_ok, adv_wrong, src_clean_ok, src_adv_wrong,
                                tani=True)
    r["raw_minus_cond"] = r["raw"] - r["target_correct"]
    r["spread"] = PROTO.yayilim(r)
    return r'''
B_IMP_ESKI = '''import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"'''
B_IMP_YENI = '''import sys

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT))
from src.analysis import protokoller as PROTO  # noqa: E402'''
yama("scripts/q1_e3_bkolu.py", [(B_IMP_ESKI, B_IMP_YENI, "import"),
                                (B_ESKI, B_YENI, "protocol_rates")])

# ----------------------------------------------------- kalibrasyon (A kolu nokta)
C_ESKI = '''def protocol_rates(clean_ok, adv_wrong, src_clean_ok, src_adv_wrong):
    """4 protokol orani + ham-kosullu sapma + yayilim."""
    def rate(mask):
        return float(100 * adv_wrong[mask].mean()) if mask.sum() else float("nan")
    raw = float(100 * adv_wrong.mean())
    tc = rate(clean_ok)
    bc = rate(clean_ok & src_clean_ok)
    ss = rate(clean_ok & src_adv_wrong)
    vals = [raw, tc, bc, ss]
    return {
        "raw": raw, "target_correct": tc, "both_correct": bc, "successful_source": ss,
        "raw_minus_cond": raw - tc,
        "spread": max(vals) - min(vals),
    }'''
C_YENI = '''def protocol_rates(clean_ok, adv_wrong, src_clean_ok, src_adv_wrong):
    """Tanimlar src/analysis/protokoller.py'den (TEK KAYNAK)."""
    r = PROTO.protokol_oranlari(clean_ok, adv_wrong, src_clean_ok, src_adv_wrong,
                                tani=True)
    r["raw_minus_cond"] = r["raw"] - r["target_correct"]
    r["spread"] = PROTO.yayilim(r)
    return r'''
C_IMP_ESKI = '''import numpy as np
import torch

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT))'''
C_IMP_YENI = '''import numpy as np
import torch

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT))
from src.analysis import protokoller as PROTO  # noqa: E402'''
yama("scripts/q1_e3_calibration.py", [(C_IMP_ESKI, C_IMP_YENI, "import"),
                                      (C_ESKI, C_YENI, "protocol_rates")])

# ------------------------------------------------------------------ A kolu (GPU)
A_ESKI = '''def oranlar(tc, aw, sc, sa):
    def r(m):
        return float(100 * aw[m].mean()) if m.sum() else float("nan")
    return {"raw": float(100 * aw.mean()), "target_correct": r(tc),
            "both_correct": r(tc & sc), "successful_source": r(tc & sa)}'''
A_YENI = '''def oranlar(tc, aw, sc, sa):
    """Tanimlar src/analysis/protokoller.py'den (TEK KAYNAK).

    Gevsek varyant da yazilir: eski artefaktlara karsi GERILEME KONTROLU
    (yeni kosumun gevsek degeri eskisiyle birebir tutmali).
    """
    return PROTO.protokol_oranlari(tc, aw, sc, sa, tani=True)'''
A_IMP_ESKI = '''from src.attacks.pgd import PGDAttack'''
A_IMP_YENI = '''from src.analysis import protokoller as PROTO
from src.attacks.pgd import PGDAttack'''
yama("scripts/q1_e3_akolu.py", [(A_IMP_ESKI, A_IMP_YENI, "import"),
                                (A_ESKI, A_YENI, "oranlar")])

# ------------------------------------------------------------- sinif dengesi (a2b)
D_ESKI = '''    elif protocol == "successful_source":'''
# a2b'nin tam govdesini gormeden korlemesine degistirmiyoruz; ayri ele alinacak.

if hatalar:
    print("YAMA BASARISIZ -- hicbir sey yazilmadi:", *hatalar, sep="\n  ")
    sys.exit(1)
print("yamalanan dosyalar:", *yazilan, sep="\n  ")
