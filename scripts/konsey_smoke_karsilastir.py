"""Iki transfer matrisi klasorunu hucre hucre karsilastirir (konsey B1 smoke).

    python scripts/konsey_smoke_karsilastir.py DIR_A DIR_B [--json CIKTI] [--yalniz-ortak]

transfer_matrix.json'daki results sozlugu ve per_sample_*.npz dizileri birebir
(np.array_equal) karsilastirilir. --yalniz-ortak verilirse yalniz iki klasorde
de bulunan hucreler karsilastirilir (alt kume testleri icin).
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--json", default=None)
    ap.add_argument("--yalniz-ortak", action="store_true")
    a = ap.parse_args()
    A, B = Path(a.a), Path(a.b)
    ja = json.loads((A / "transfer_matrix.json").read_text())
    jb = json.loads((B / "transfer_matrix.json").read_text())
    ra, rb = ja["results"], jb["results"]
    keys = sorted(set(ra) & set(rb)) if a.yalniz_ortak else sorted(set(ra) | set(rb))
    fark_json = [k for k in keys if ra.get(k) != rb.get(k)]
    fa = {p.name for p in A.glob("per_sample_*.npz")}
    fb = {p.name for p in B.glob("per_sample_*.npz")}
    files = sorted(fa & fb) if a.yalniz_ortak else sorted(fa | fb)
    fark_npz = []
    for f in files:
        if f not in fa or f not in fb:
            fark_npz.append(f"{f}: yalniz bir klasorde")
            continue
        da, db = np.load(A / f), np.load(B / f)
        if sorted(da.files) != sorted(db.files):
            fark_npz.append(f"{f}: anahtarlar farkli")
            continue
        for k in da.files:
            if not np.array_equal(da[k], db[k]):
                fark_npz.append(f"{f}:{k} ({int((da[k] != db[k]).sum())} ornek farkli)")
    ust = {k: (ja.get(k), jb.get(k)) for k in ("seed", "n_samples", "eps", "alpha", "steps",
                                               "norm", "models") if ja.get(k) != jb.get(k)}
    out = {"A": str(A), "B": str(B), "hucre_sayisi": len(keys), "npz_sayisi": len(files),
           "json_farkli_hucreler": fark_json, "npz_farklari": fark_npz,
           "ust_alan_farklari": ust,
           "BIREBIR": not fark_json and not fark_npz and not ust}
    print(json.dumps(out, indent=1, ensure_ascii=False))
    if a.json:
        Path(a.json).write_text(json.dumps(out, indent=2, ensure_ascii=False))
    sys.exit(0 if out["BIREBIR"] else 1)


if __name__ == "__main__":
    main()
