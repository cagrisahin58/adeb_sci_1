#!/usr/bin/env python
"""Run every gate for one Üslup Z preview and write the summary (paper/figures/onizleme_v2/qc/<stem>/).

    python paper/figures/onizleme_v2/_kapilar_v2.py pv_b_model_exploded

Gates (visio-cizici SKILL.md step 7):
  K1  controller report <stem>_mm_kontrol.json: verdict PASS, largest read-back deviation < 0.01 mm
  K2  motor/host/fig_mm_pdf.py --floor 8.0 --uslup Z            -> qc/<stem>/fig_mm_pdf.json
  K3  motor/host/denge.py --uslup Z (answer file <stem>.denge_ajan.json) -> qc/<stem>/denge.json
  K4  scripts/zenginlik.py --pdf <stem>.pdf                      -> qc/<stem>/zenginlik.json
  K5  motor/host/fig_qc.py on a one-figure .tex (--tek-sekil-tex, trap T29) with the caption draft of the
      manifest, adjusted and strict scores                        -> qc/<stem>/qc/report.json
The summary goes to qc/<stem>/kapilar.json; every command and exit code to visio_loglari/kapilar_komutlar.log.
Settings: VZ_PROJE_AYARI = paper/figures/onizleme_v2/visio_cizici_v2.yaml (96 DPI, outputs here).
"""
from __future__ import annotations

import datetime as dt
import io
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
_R = str(ROOT).replace("\\", "/")
_H = str(HERE).replace("\\", "/")
os.environ["VZ_PROJE_KOKU"] = _R
os.environ["VZ_PROJE_AYARI"] = _H + "/visio_cizici_v2.yaml"
os.environ["VZ_PALET_DIZINI"] = _H + "/palettes"
os.environ["VZ_USLUP"] = "Z"
os.chdir(_R)
V = str(Path.home() / ".claude" / "skills" / "visio-cizici").replace("\\", "/")
ASSETS = "paper/figures/onizleme_v2"
LOG = HERE / "visio_loglari" / "kapilar_komutlar.log"


def run(cmd):
    t = dt.datetime.now().isoformat(timespec="seconds")
    p = subprocess.run([sys.executable, "-X", "utf8"] + cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    with io.open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"{t} python {' '.join(cmd)}  -> exit {p.returncode}\n")
    return p.returncode, p.stdout + p.stderr


def tail(txt, n=8):
    return [ln for ln in txt.splitlines() if ln.strip()][-n:]


def main():
    s = sys.argv[1]
    qc = HERE / "qc" / s
    qc.mkdir(parents=True, exist_ok=True)
    q = str(qc).replace("\\", "/")
    out = {"stem": s, "zaman": dt.datetime.now().isoformat(timespec="seconds"),
           "ayar": os.environ["VZ_PROJE_AYARI"]}
    man = json.loads((HERE / f"{s}.fig.json").read_text(encoding="utf-8"))
    kp = HERE / f"{s}_mm_kontrol.json"
    if not kp.is_file():
        kp = HERE / f"{s}.mm.json"
    k = json.loads(kp.read_text(encoding="utf-8"))
    out["K1_kontrolcu"] = {"dosya": kp.name, "karar": k.get("verdict"),
                           "en_buyuk_sapma_mm": (k.get("readback") or {}).get("max_deviation_mm"),
                           "on_denetim_sorun": len((k.get("preflight") or {}).get("issues") or []),
                           "sayfa_mm": k.get("page_mm")}
    rc, txt = run([f"{V}/motor/host/fig_mm_pdf.py", "--assets", ASSETS, "--figure", s, "--floor", "8.0",
                   "--uslup", "Z", "--json-out", f"{q}/fig_mm_pdf.json"])
    out["K2_fig_mm_pdf"] = {"cikis": rc, "ozet": tail(txt, 6)}
    rc, txt = run([f"{V}/motor/host/denge.py", "--assets", ASSETS, "--figure", s, "--uslup", "Z",
                   "--ajan", f"{ASSETS}/{s}.denge_ajan.json", "--out", f"{q}/denge.json"])
    d = json.loads((qc / "denge.json").read_text(encoding="utf-8")) if (qc / "denge.json").is_file() else {}
    out["K3_denge"] = {"cikis": rc, "karar": d.get("karar") or d.get("sonuc"), "ozet_satiri": d.get("ozet_satiri"),
                       "ihlaller": d.get("ihlaller"), "eksikler": d.get("eksikler"), "uyarilar": d.get("uyarilar"),
                       "son": tail(txt, 4)}
    rc, txt = run([f"{V}/scripts/zenginlik.py", "--pdf", f"{ASSETS}/{s}.pdf", "--tablo", "--json-out",
                   f"{q}/zenginlik.json"])
    out["K4_zenginlik"] = {"cikis": rc, "tablo": tail(txt, 6)}
    cap = man.get("altyazi_taslagi") or ""
    lead, _, rest = cap.partition(". ")
    tex_cap = f"\\textbf{{{lead}.}} {rest}" if rest else cap
    rc1, txt1 = run([f"{V}/motor/host/fig_qc.py", "--tek-sekil-tex", f"{q}/tek_sekil.tex", "--figure", s,
                     "--caption", tex_cap, "--kind", man.get("kind", "double")])
    rc, txt = run([f"{V}/motor/host/fig_qc.py", "--assets", ASSETS, "--tex", f"{q}/tek_sekil.tex",
                   "--venue", "ieee_access", "--figure", s, "--out", f"{q}/qc"])
    rep = {}
    rp = qc / "qc" / "report.json"
    if rp.is_file():
        rep = json.loads(rp.read_text(encoding="utf-8"))
    out["K5_fig_qc"] = {"cikis": rc, "son": tail(txt, 12), "rapor": str(rp.relative_to(ROOT)).replace("\\", "/")}
    with io.open(qc / "kapilar.json", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
