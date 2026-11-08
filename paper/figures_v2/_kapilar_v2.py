#!/usr/bin/env python
"""Run every gate for one figure v2, install it and score the installed figure (paper/figures_v2/qc/).

    python paper/figures_v2/_kapilar_v2.py <kok> [--no-install] [--not "..."]

  K1  controller report yapim/z_<kok>_mm_kontrol.json: PASS, read-back deviation < 0.01 mm
  K2  fig_mm_pdf.py --floor 8.0 --uslup Z  (verdict PASS and no T4 warning required)
  K3  denge.py --uslup Z                   ("kurulabilir")
  K4  zenginlik.py --pdf
  IN  install.py z_<kok> --hedef paper/figures_v2 --yeniden (mapping qc/ESLEME.md) -> figN_<kok>
  K5  fig_qc.py on the installed name with a one-figure .tex carrying the manifest's caption draft
      (adjusted and strict scores)
  MB  blue pixel share of the PNG (hue 180-270 among coloured pixels)
A row is appended to raporlar/sekil_v2_2026-11-07/02_ilerleme.tsv. Settings: VZ_PROJE_AYARI =
paper/figures_v2/visio_cizici_v2.yaml.
"""
from __future__ import annotations

import colorsys
import datetime as dt
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
_R = str(ROOT).replace("\\", "/")
_H = str(HERE).replace("\\", "/")
os.environ["VZ_PROJE_KOKU"] = _R
os.environ["VZ_PROJE_AYARI"] = _H + "/visio_cizici_v2.yaml"
os.environ["VZ_PALET_DIZINI"] = _H + "/palettes"
os.environ["VZ_USLUP"] = "Z"
os.chdir(_R)
sys.stdout.reconfigure(encoding="utf-8")
V = str(Path.home() / ".claude" / "skills" / "visio-cizici").replace("\\", "/")
B = "paper/figures_v2/yapim"
LOG = HERE / "visio_loglari" / "kapilar_komutlar.log"
TSV = ROOT / "raporlar" / "sekil_v2_2026-11-07" / "02_ilerleme.tsv"
HEAD = "sekil\tkok\tdurum\tkontrolcu\tmm_pdf\tdenge\tqc_ayarli\tqc_kati\tkurulum\tnot\tzaman\n"


def run(cmd):
    t = dt.datetime.now().isoformat(timespec="seconds")
    p = subprocess.run([sys.executable, "-X", "utf8"] + cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    with io.open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"{t} python {' '.join(cmd)}  -> exit {p.returncode}\n")
    return p.returncode, p.stdout + p.stderr


def tail(txt, n=8):
    return [ln for ln in txt.splitlines() if ln.strip()][-n:]


def mapping():
    out = {}
    for ln in (HERE / "qc" / "ESLEME.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(z_\w+)\s*\|\s*(fig(\d+)_\w+)\s*\|", ln)
        if m:
            out[m.group(1)] = (m.group(2), int(m.group(3)))
    return out


def blue_share(png):
    from PIL import Image
    im = Image.open(png).convert("RGB")
    im.thumbnail((900, 900))
    col = blue = 0
    for r, g, b in im.getdata():
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if s < 0.08 or v < 0.15:
            continue
        col += 1
        if 180 <= h * 360 <= 270:
            blue += 1
    return round(blue / col, 4) if col else 0.0, col


def main():
    kok = sys.argv[1]
    s = f"z_{kok}"
    note = sys.argv[sys.argv.index("--not") + 1] if "--not" in sys.argv else ""
    name, num = mapping()[s]
    qc = HERE / "qc" / s
    qc.mkdir(parents=True, exist_ok=True)
    q = str(qc).replace("\\", "/")
    out = {"stem": s, "kurulum_adi": name, "zaman": dt.datetime.now().isoformat(timespec="seconds"),
           "ayar": os.environ["VZ_PROJE_AYARI"]}
    man = json.loads((HERE / "yapim" / f"{s}.fig.json").read_text(encoding="utf-8"))
    k = json.loads((HERE / "yapim" / f"{s}_mm_kontrol.json").read_text(encoding="utf-8"))
    dev = (k.get("readback") or {}).get("max_deviation_mm")
    out["K1_kontrolcu"] = {"karar": k.get("verdict"), "en_buyuk_sapma_mm": dev,
                           "on_denetim_sorun": len((k.get("preflight") or {}).get("issues") or []),
                           "sayfa_mm": k.get("page_mm")}
    rc, txt = run([f"{V}/motor/host/fig_mm_pdf.py", "--assets", B, "--figure", s, "--floor", "8.0",
                   "--uslup", "Z", "--json-out", f"{q}/fig_mm_pdf.json"])
    mm = json.loads((qc / "fig_mm_pdf.json").read_text(encoding="utf-8")).get(s, {})
    warns = mm.get("warnings") or []
    t4 = [w for w in warns if w.startswith("T4") or w.startswith("T3/T4")]
    out["K2_fig_mm_pdf"] = {"cikis": rc, "karar": mm.get("verdict"), "en_kucuk_pt": mm.get("min_pt"),
                            "uyarilar": warns, "T4": t4, "basili_cizgi_pt": (mm.get("cizgi") or {}).get("basili_pt")}
    rc, txt = run([f"{V}/motor/host/denge.py", "--assets", B, "--figure", s, "--uslup", "Z",
                   "--ajan", f"{B}/{s}.denge_ajan.json", "--out", f"{q}/denge.json"])
    d = json.loads((qc / "denge.json").read_text(encoding="utf-8")) if (qc / "denge.json").is_file() else {}
    out["K3_denge"] = {"cikis": rc, "karar": d.get("sonuc"), "ihlaller": d.get("ihlaller"),
                       "eksikler": d.get("eksikler"), "uyarilar": d.get("uyarilar"),
                       "muaf_3b_veri": ((d.get("yasaklar") or {}).get("3b_veri") or {}).get("muaf")}
    rc, txt = run([f"{V}/scripts/zenginlik.py", "--pdf", f"{B}/{s}.pdf", "--tablo", "--json-out",
                   f"{q}/zenginlik.json"])
    z = json.loads((qc / "zenginlik.json").read_text(encoding="utf-8")) if (qc / "zenginlik.json").is_file() else {}
    out["K4_zenginlik"] = {"cikis": rc, "tablo": tail(txt, 6), "ozet": z.get("ozet_satiri")}
    ok_gates = (k.get("verdict") == "PASS" and mm.get("verdict") == "PASS" and not t4
                and d.get("sonuc") == "kurulabilir")
    inst = "yok"
    if ok_gates and "--no-install" not in sys.argv:
        rc, txt = run([f"{V}/motor/visio/install.py", s, "--hedef", "paper/figures_v2", "--yeniden"])
        inst = "kuruldu" if rc == 0 else "RED"
        out["IN_kurulum"] = {"cikis": rc, "son": tail(txt, 6)}
    cap = man.get("altyazi_taslagi") or ""
    lead, _, rest = cap.partition(". ")
    tex_cap = f"\\textbf{{{lead}.}} {rest}" if rest else cap
    qa = qk = None
    if inst == "kuruldu":
        rc1, _ = run([f"{V}/motor/host/fig_qc.py", "--tek-sekil-tex", f"{q}/tek_sekil.tex", "--figure", name,
                      "--caption", tex_cap, "--kind", man.get("kind", "double")])
        rc, txt = run([f"{V}/motor/host/fig_qc.py", "--assets", "paper/figures_v2", "--tex", f"{q}/tek_sekil.tex",
                       "--venue", "ieee_access", "--figure", name, "--out", f"{q}/qc"])
        rp = qc / "qc" / "report.json"
        rep = json.loads(rp.read_text(encoding="utf-8")) if rp.is_file() else {}
        out["K5_fig_qc"] = {"cikis": rc, "son": tail(txt, 14)}
        for ln in txt.splitlines():
            if ln.startswith(name + " "):
                parts = ln.split()
                qa, qk = parts[1], parts[2]
                out["K5_fig_qc"]["ayarli"], out["K5_fig_qc"]["kati"] = qa, qk
                out["K5_fig_qc"]["karar"] = parts[4] if len(parts) > 4 else None
        out["K5_fig_qc"]["rapor_anahtarlari"] = list(rep)[:12] if isinstance(rep, dict) else None
    png = HERE / "yapim" / f"{s}.png"
    if png.is_file():
        out["MB_mavi_pay"] = blue_share(png)
    with io.open(qc / "kapilar.json", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k_: v for k_, v in out.items() if k_ != "K5_fig_qc"}, indent=1, ensure_ascii=False)[:3000])
    print("QC:", "\n".join(out.get("K5_fig_qc", {}).get("son", [])))
    if "--tsv" in sys.argv:
        keep = [HEAD]
        if TSV.is_file():
            keep += [ln for ln in TSV.read_text(encoding="utf-8").splitlines(True)[1:]
                     if ln.split("\t")[1:2] != [kok]]
        with io.open(TSV, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("".join(keep))
            durum = "bitti" if inst == "kuruldu" else "takildi"
            fh.write("\t".join(str(x) for x in (
                num, kok, durum, f"{k.get('verdict')} {dev}", f"{mm.get('verdict')} T4={len(t4)}", d.get("sonuc"),
                sys.argv[sys.argv.index("--qa") + 1] if "--qa" in sys.argv else qa,
                sys.argv[sys.argv.index("--qk") + 1] if "--qk" in sys.argv else qk,
                f"{inst} {name}", note, dt.datetime.now().isoformat(timespec="minutes"))) + "\n")


if __name__ == "__main__":
    main()
