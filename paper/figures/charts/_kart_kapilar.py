#!/usr/bin/env python
"""Run the per-figure gates of a card figure and summarise them (visio-cizici, Faz B, card agent).

    python paper/figures/charts/_kart_kapilar.py <stem> [<stem> ...]

For each stem (built in paper/figures/charts):
  K1'  card controller   <stem>.mm.json verdict and issue count
  K2   printed PDF       motor/host/fig_mm_pdf.py --floor 8.0 -> paper/figures/qc/<stem>/fig_mm_pdf.json
  K3   balance           motor/host/denge.py -> paper/figures/qc/<stem>/denge.json ("kurulabilir")
       richness          scripts/zenginlik.py --pdf ... --tablo -> paper/figures/qc/<stem>/zenginlik.json
  K5   kanit             <stem>.kanit.json foy_karsilastirmasi.uyusmayan == 0, sheet hash == today's sheet
  K6   height            canvas height <= the plan's ceiling (04_cizim_plani.md section 9) and 165.33 mm
Every command line and its exit code is appended to paper/figures/visio_loglari/kart_ajani_komutlar.log;
the summary of all stems is written to paper/figures/qc/kart_kapilar_ozet.json (merged, newest wins).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = str(Path(__file__).resolve().parents[3]).replace("\\", "/")
SKILL = str(Path.home() / ".claude" / "skills" / "visio-cizici").replace("\\", "/")
os.environ.setdefault("VZ_PROJE_KOKU", ROOT)
os.environ.setdefault("VZ_PROJE_AYARI", ROOT + "/paper/figures/visio_cizici.yaml")
os.environ["PYTHONIOENCODING"] = "utf-8"
os.chdir(ROOT)
LOG = Path("paper/figures/visio_loglari/kart_ajani_komutlar.log")
OZET = Path("paper/figures/qc/kart_kapilar_ozet.json")
A = "paper/figures/charts"
# 04_cizim_plani.md section 9: (target, ceiling) mm
TAVAN = {"source_gap_split": 72, "similarity_matrix": 70, "cells_interaction": 125, "attack_side": 98,
         "gradient_alignment": 118, "estimates_forest": 130, "protocol_settings": 88, "protocol_sets": 120,
         "spread_clean_gap": 122, "epsilon_sweep": 66, "feature_degradation": 122}
GLOBAL_CEIL = 165.33


def run(cmd):
    t0 = dt.datetime.now().isoformat(timespec="seconds")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    with io.open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"{t0} rc={r.returncode} {' '.join(cmd)}\n")
    return r


def kapilar(stem):
    q = Path(f"paper/figures/qc/{stem}")
    q.mkdir(parents=True, exist_ok=True)
    res = {"stem": stem}
    mm = json.loads(Path(f"{A}/{stem}.mm.json").read_text(encoding="utf-8"))
    res["K1_kart_denetcisi"] = {"verdict": mm.get("verdict"), "sorun": len(mm.get("issues", []))}
    r = run(["python", f"{SKILL}/motor/host/fig_mm_pdf.py", "--assets", A, "--figure", stem, "--floor", "8.0",
             "--json-out", str(q / "fig_mm_pdf.json")])
    fj = json.loads((q / "fig_mm_pdf.json").read_text(encoding="utf-8"))
    res["K2_fig_mm_pdf"] = {"rc": r.returncode, "ozet": r.stdout.strip().splitlines()[-1:] if r.stdout else [],
                            "rapor": fj if len(json.dumps(fj)) < 600 else None}
    aj = Path(f"{A}/{stem}.denge_ajan.json")
    r = run(["python", f"{SKILL}/motor/host/denge.py", "--assets", A, "--figure", stem, "--ajan", str(aj),
             "--out", str(q / "denge.json")])
    dj = json.loads((q / "denge.json").read_text(encoding="utf-8"))
    sm = {m.get("ad") or m.get("olcut"): m for m in dj.get("sayisal_maddeler", []) if isinstance(m, dict)}
    va = sm.get("veri_alani_payi", {})
    res["K3_denge"] = {"rc": r.returncode, "sonuc": dj.get("sonuc") or dj.get("karar"),
                       "veri_alani_payi": va.get("deger"), "veri_alani_gecti": va.get("gecti"),
                       "veri_alani_uygulanmaz": va.get("uygulanmaz"),
                       "ihlaller": dj.get("ihlaller"), "eksikler": dj.get("eksikler"),
                       "ozet_satiri": dj.get("ozet_satiri"), "uyarilar": dj.get("uyarilar")}
    r = run(["python", f"{SKILL}/scripts/zenginlik.py", "--pdf", f"{A}/{stem}.pdf", "--tablo", "--yalniz-olc",
             "--json-out", str(q / "zenginlik.json")])
    res["zenginlik"] = {"rc": r.returncode, "tablo": r.stdout.strip().splitlines()[-3:]}
    kj = json.loads(Path(f"{A}/{stem}.kanit.json").read_text(encoding="utf-8"))
    fk = kj.get("foy_karsilastirmasi", {})
    today = hashlib.sha256(Path("results/C1_REFERANS_FOYU.md").read_bytes()).hexdigest()
    res["K5_kanit"] = {"karsilastirma": fk.get("karsilastirma_sayisi"), "uyusmayan": fk.get("uyusmayan"),
                       "foy_ozeti_bugunku": fk.get("foy_sha256") == today, "deger_sayisi": len(kj.get("degerler", []))}
    h = float(mm.get("canvas_mm", [0, 0])[1])
    t = TAVAN.get(stem)
    res["K6_yukseklik"] = {"mm": h, "tavan": t, "gecti": h <= GLOBAL_CEIL and (t is None or h <= t)}
    res["GECTI"] = (res["K1_kart_denetcisi"]["verdict"] == "PASS" and res["K1_kart_denetcisi"]["sorun"] == 0
                    and res["K2_fig_mm_pdf"]["rc"] == 0 and res["K3_denge"]["rc"] == 0
                    and res["K5_kanit"]["uyusmayan"] == 0 and res["K5_kanit"]["foy_ozeti_bugunku"]
                    and res["K6_yukseklik"]["gecti"]
                    and (va.get("gecti") is True or va.get("uygulanmaz") is not None))
    return res


def main():
    allr = json.loads(OZET.read_text(encoding="utf-8")) if OZET.is_file() else {}
    rc = 0
    for stem in sys.argv[1:]:
        r = kapilar(stem)
        allr[stem] = r
        print(json.dumps(r, ensure_ascii=False, indent=1, default=str))
        rc |= 0 if r["GECTI"] else 1
    with io.open(OZET, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(allr, ensure_ascii=False, indent=1, default=str) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
