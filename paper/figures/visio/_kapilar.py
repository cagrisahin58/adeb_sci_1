#!/usr/bin/env python
"""Run the per-figure gates of the drawing phase for one Visio figure and summarise them.

    python paper/figures/visio/_kapilar.py study_overview [--uslup 8]

Gates (task of the drawing phase; plan 04_cizim_plani.md section 11, K1-K3 and the richness table):
  K1  controller report <stem>_mm_kontrol.json: verdict PASS, largest read-back deviation < 0.01 mm
  K2  motor/host/fig_mm_pdf.py --floor 8.0 -> paper/figures/qc/<stem>/fig_mm_pdf.json, PASS
  K3  motor/host/denge.py (answer file <stem>.denge_ajan.json) -> paper/figures/qc/<stem>/denge.json,
      "kurulabilir"
  Z   scripts/zenginlik.py --pdf <stem>.pdf --tablo (reported)
The summary goes to paper/figures/qc/<stem>/kapilar.json and the command log.
"""
from __future__ import annotations

import argparse
import datetime as dt
import io
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
_R = str(ROOT).replace("\\", "/")
os.environ.setdefault("VZ_PROJE_KOKU", _R)
os.environ.setdefault("VZ_PROJE_AYARI", _R + "/paper/figures/visio_cizici.yaml")
os.chdir(_R)
V = str(Path.home() / ".claude" / "skills" / "visio-cizici").replace("\\", "/")
ASSETS = "paper/figures/visio"
LOG = Path("paper/figures/visio_loglari/visio_ajan_komutlar.log")


def run(cmd):
    t = dt.datetime.now().isoformat(timespec="seconds")
    p = subprocess.run([sys.executable, "-X", "utf8"] + cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    with io.open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"{t} python {' '.join(cmd)}  -> exit {p.returncode}\n")
    return p.returncode, p.stdout + p.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stem")
    ap.add_argument("--uslup", default="8")
    a = ap.parse_args()
    s = a.stem
    qc = Path("paper/figures/qc") / s
    qc.mkdir(parents=True, exist_ok=True)
    out = {"stem": s, "zaman": dt.datetime.now().isoformat(timespec="seconds")}
    k = json.loads(Path(ASSETS, f"{s}_mm_kontrol.json").read_text(encoding="utf-8"))
    out["K1_kontrolcu"] = {"karar": k.get("verdict"),
                           "en_buyuk_sapma_mm": (k.get("readback") or {}).get("max_deviation_mm"),
                           "on_denetim_sorun": len((k.get("preflight") or {}).get("issues") or []),
                           "sayfa_mm": k.get("page_mm")}
    rc, txt = run([f"{V}/motor/host/fig_mm_pdf.py", "--assets", ASSETS, "--figure", s, "--floor", "8.0",
                   "--json-out", str(qc / "fig_mm_pdf.json").replace("\\", "/")])
    out["K2_fig_mm_pdf"] = {"cikis": rc, "ozet": [ln for ln in txt.splitlines() if ln.strip()][-6:]}
    rc, txt = run([f"{V}/motor/host/denge.py", "--assets", ASSETS, "--figure", s, "--uslup", a.uslup,
                   "--ajan", f"{ASSETS}/{s}.denge_ajan.json", "--out", str(qc / "denge.json").replace("\\", "/")])
    d = json.loads((qc / "denge.json").read_text(encoding="utf-8")) if (qc / "denge.json").is_file() else {}
    out["K3_denge"] = {"cikis": rc, "karar": d.get("karar") or d.get("sonuc"),
                       "ozet_satiri": d.get("ozet_satiri"),
                       "ihlaller": d.get("ihlaller"), "eksikler": d.get("eksikler"),
                       "uyarilar": d.get("uyarilar"), "son": [ln for ln in txt.splitlines() if ln.strip()][-4:]}
    rc, txt = run([f"{V}/scripts/zenginlik.py", "--pdf", f"{ASSETS}/{s}.pdf", "--tablo"])
    out["Z_zenginlik"] = {"cikis": rc, "tablo": [ln for ln in txt.splitlines() if ln.strip()]}
    with io.open(qc / "kapilar.json", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
