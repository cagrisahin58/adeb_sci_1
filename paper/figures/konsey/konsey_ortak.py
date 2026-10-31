"""Shared helpers for the council-round draft figures (paper/figures/konsey/).

Style follows paper/figures/fig_yayilim_temiz_fark.py: DejaVu Sans, 8-9 pt, single column
3.358 in, double column 6.989 in, Okabe-Ito colours with a second channel (marker, line style or
hatch), pdf.fonttype 42, no Type 3 fonts.

Change log (degisiklik notu):
- 2026-10-31 (hakem konseyi, sunum mercegi bulgu 13 / A12): SINGLE_IN and DOUBLE_IN set to the
  class geometry of ieeeaccess.cls (\\columnwidth 85.29 mm = 3.358 in, \\textwidth 177.53 mm =
  6.989 in) instead of 3.5 / 7.16 in, so that \\includegraphics[width=\\columnwidth|\\textwidth]
  places every council figure at scale 1.00 and the 8 pt minimum is 8 pt on the printed page
  (before: x0.959 single, x0.976 double, i.e. 7.7 and 7.8 pt).

Every number a figure draws is read from a JSON artefact and compared with the reference sheet
(results/C1_REFERANS_FOYU.md, "foy") at a named line that must also contain an anchor string, so
that a shifted or regenerated sheet fails loudly instead of matching the wrong row. A figure is
written only if every comparison passes.
"""
import datetime as dt
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.text  # noqa: E402,F401

FOY = Path("results/C1_REFERANS_FOYU.md")
OUTDIR = Path("paper/figures/konsey")
SINGLE_IN, DOUBLE_IN = round(85.29 / 25.4, 3), round(177.53 / 25.4, 3)  # ieeeaccess.cls lines 262-263
MIN_FONT = 8.0
INK, EDGE, ZERO, MUTE = "#262626", "#393939", "#8d8d8d", "#6e6e6e"

# Okabe-Ito, semantic: the same thing keeps the same colour in every council figure.
OI = {"black": "#000000", "orange": "#E69F00", "sky": "#56B4E9", "green": "#009E73",
      "yellow": "#F0E442", "blue": "#0072B2", "vermilion": "#D55E00", "purple": "#CC79A7",
      "grey": "#999999"}
COL = {
    # models (architecture)
    "vit": OI["vermilion"],      # ViT-Tiny cells and ImageNet transformers
    "r224": OI["blue"],          # ResNet-18 on the 32->224 pipeline, ImageNet CNN counterparts
    "r32": OI["sky"],            # 32-pixel CIFAR ResNet-18 (bridge cell, C1 pair)
    "panel": OI["grey"],         # robust CNN panel members
    "xcit": OI["purple"],        # secondary transformer panel member (XCiT-S12)
    # decomposition components
    "sym": OI["green"],          # symmetric part / similarity sigma
    "dir": OI["orange"],         # directional part / rho
}

# results/c1_* and results/q1/* (quarantine rule) plus the frozen cell tables (definitions only).
ALLOWED = ("results/c1_", "results/q1/", "raporlar/konsey_2026-10-29/hucre_tablosu")


def fail(msg):
    sys.stderr.write(f"HATA / ERROR: {msg}\n")
    sys.exit(1)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_source(path):
    p = str(path)
    if not p.startswith(ALLOWED):
        fail(f"input outside the quarantine-safe paths: {p}")
    if not Path(p).is_file():
        fail(f"{p} not found (run from the repo root)")
    return Path(p)


def load_json(path):
    p = check_source(path)
    return json.loads(p.read_text(encoding="utf-8"))


def dig(d, keypath):
    """Read d['a']['b'][0] for keypath 'a.b.0' (list indices as integers); fail if missing."""
    cur = d
    for k in keypath.split("."):
        try:
            cur = cur[int(k)] if isinstance(cur, list) else cur[k]
        except (KeyError, IndexError, ValueError, TypeError):
            fail(f"key path missing: {keypath} (at '{k}')")
    return cur


def git_info(paths):
    def run(*args):
        try:
            return subprocess.run(["git", "-c", f"safe.directory={Path.cwd()}", *args],
                                  capture_output=True, text=True, timeout=20).stdout.strip()
        except Exception:
            return ""
    return {"commit": run("rev-parse", "HEAD") or "unknown",
            "branch": run("rev-parse", "--abbrev-ref", "HEAD") or "unknown",
            "dirty_or_untracked": run("status", "--porcelain", "--", *[str(p) for p in paths]).splitlines()}


NUM_RE = re.compile(r"(?<![\w.])[+\-]?\d+(?:\.\d+)?(?:e[+\-]\d+)?")


class Foy:
    """Reference-sheet comparisons. kontrol() records, bitir() fails if any comparison failed."""

    def __init__(self, path=FOY):
        self.path = Path(path)
        if not self.path.is_file():
            fail(f"reference sheet {self.path} not found")
        self.lines = self.path.read_text(encoding="utf-8").splitlines()
        self.kayit = []

    def satir(self, n, capa):
        if n < 1 or n > len(self.lines):
            fail(f"foy line {n} out of range")
        t = self.lines[n - 1]
        if capa not in t:
            fail(f"foy line {n} does not contain anchor {capa!r}; the sheet has shifted, "
                 f"line reads: {t[:160]!r}")
        return t

    def sayilar(self, n, capa):
        return [float(x) for x in NUM_RE.findall(self.satir(n, capa))]

    def kontrol(self, ad, deger, n, capa, ondalik, tol=None):
        """deger (from JSON, unrounded) must match a number printed on foy line n to the sheet's
        own rounding (ondalik decimals): |deger - printed| <= 0.5 * 10**-ondalik."""
        nums = self.sayilar(n, capa)
        t = (0.5 * 10 ** -ondalik + 1e-9) if tol is None else tol
        best = min(nums, key=lambda x: abs(x - deger)) if nums else None
        ok = best is not None and abs(best - deger) <= t
        self.kayit.append({"ad": ad, "json_degeri": deger, "foy_satiri": n, "capa": capa,
                           "foy_en_yakin": best, "ondalik": ondalik, "tolerans": t, "eslesti": ok})
        return ok

    def metin(self, ad, aranan, n, capa):
        ok = aranan in self.satir(n, capa)
        self.kayit.append({"ad": ad, "aranan_metin": aranan, "foy_satiri": n, "capa": capa, "eslesti": ok})
        return ok

    def esit(self, ad, a, b, tol, aciklama):
        """Internal consistency check (JSON vs recomputation), recorded alongside foy checks."""
        ok = abs(a - b) <= tol
        self.kayit.append({"ad": ad, "a": a, "b": b, "tolerans": tol, "aciklama": aciklama, "eslesti": ok})
        return ok

    def bitir(self):
        bad = [k for k in self.kayit if not k["eslesti"]]
        if bad:
            for k in bad:
                sys.stderr.write(f"  MISMATCH: {json.dumps(k, ensure_ascii=False)}\n")
            fail(f"{len(bad)} of {len(self.kayit)} comparisons failed; figure NOT written")
        return {"karsilastirma_sayisi": len(self.kayit), "uyusmayan": 0, "sonuc": "TAMAM",
                "foy": str(self.path), "foy_sha256": sha(self.path), "ayrinti": self.kayit}


def style(seed=0):
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans"], "mathtext.fontset": "dejavusans",
        "font.size": 8, "axes.labelsize": 9, "legend.fontsize": 8,
        "xtick.labelsize": 8, "ytick.labelsize": 8,
        "axes.linewidth": 0.6, "axes.edgecolor": EDGE, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "xtick.major.size": 2.5, "ytick.major.size": 2.5, "xtick.color": INK, "ytick.color": INK,
        "axes.labelcolor": INK, "text.color": INK,
        "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.bbox": "standard", "svg.hashsalt": str(seed),
        "hatch.linewidth": 0.6,
    })


def layout_checks(fig, allow_overlap=(), min_font=MIN_FONT):
    """No text overlap, all text inside the figure, all text >= min_font pt. Returns min font.
    allow_overlap: substrings of texts that may overlap (e.g. a colour-bar label next to its axis)."""
    fig.canvas.draw()
    R = fig.canvas.get_renderer()
    tick_objs, drawn = set(), set()
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            for tk in axis.get_major_ticks() + axis.get_minor_ticks():
                tick_objs.update({id(tk.label1), id(tk.label2)})
            for tk in axis._update_ticks():
                if tk.label1.get_visible():
                    drawn.add(id(tk.label1))
                if tk.label2.get_visible():
                    drawn.add(id(tk.label2))
    texts = [t for t in fig.findobj(matplotlib.text.Text) if t.get_visible() and t.get_text().strip()
             and (id(t) not in tick_objs or id(t) in drawn)]
    for i in range(len(texts)):
        bb = texts[i].get_window_extent(R)
        if bb.x0 < -0.5 or bb.y0 < -0.5 or bb.x1 > fig.bbox.x1 + 0.5 or bb.y1 > fig.bbox.y1 + 0.5:
            fail(f"text outside the figure: {texts[i].get_text()!r} {bb.bounds}")
        for j in range(i + 1, len(texts)):
            if any(s in texts[i].get_text() or s in texts[j].get_text() for s in allow_overlap):
                continue
            if bb.overlaps(texts[j].get_window_extent(R)):
                fail(f"text overlap: {texts[i].get_text()!r} {bb.bounds} / {texts[j].get_text()!r} "
                     f"{texts[j].get_window_extent(R).bounds}")
    m = min(t.get_fontsize() for t in texts)
    if m < min_font - 1e-6:
        fail(f"text below {min_font} pt: {m}")
    return m


def keep_old(outdir, name):
    """Never overwrite a figure silently: move an existing version to _vN."""
    exts = [".pdf", ".png", ".kanit.json"]
    if not any((outdir / f"{name}{e}").exists() for e in exts):
        return None
    k = 1
    while any((outdir / f"{name}_v{k}{e}").exists() for e in exts):
        k += 1
    for e in exts:
        if (outdir / f"{name}{e}").exists():
            shutil.move(str(outdir / f"{name}{e}"), str(outdir / f"{name}_v{k}{e}"))
    return f"{name}_v{k}"


def save(fig, outdir, name, dpi):
    outdir.mkdir(parents=True, exist_ok=True)
    moved = keep_old(outdir, name)
    pdf, png = outdir / f"{name}.pdf", outdir / f"{name}.png"
    fig.savefig(pdf, metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(png, dpi=dpi)
    plt.close(fig)
    if b"/Type3" in pdf.read_bytes():
        fail("Type 3 font in PDF")
    return pdf, png, moved


def write_kanit(outdir, name, script_rel, argv, inputs, size_in, dpi, min_pt, okunan, cizilen,
                foy_sonuc, denetimler, notlar, moved, extra=None):
    k = {
        "sekil": name, "surum": 1, "durum": "taslak (matplotlib); kalici cizim visio-cizici turunda",
        "betik": script_rel, "ortak_modul": "paper/figures/konsey/konsey_ortak.py",
        "ortak_modul_sha256": sha("paper/figures/konsey/konsey_ortak.py"),
        "komut": "docker exec -w /workspace adeb_eval python -B " + " ".join([script_rel] + list(argv)),
        "uretim_zamani_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "girdiler_sha256": {str(p): sha(p) for p in inputs},
        "git": git_info(list(inputs) + [script_rel, "paper/figures/konsey/konsey_ortak.py"]),
        "yerlesim": {"boyut_in": list(size_in), "dpi": dpi, "en_kucuk_yazi_pt": min_pt,
                     "font": "DejaVu Sans, pdf.fonttype 42", "renkler": COL},
        "okunan_anahtarlar": okunan,
        "cizilen_degerler": cizilen,
        "foy_karsilastirmasi": foy_sonuc,
        "denetimler": denetimler,
        "notlar": notlar,
        "eski_surum_tasindi": moved,
    }
    if extra:
        k.update(extra)
    p = outdir / f"{name}.kanit.json"
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(k, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return p


def panel_label(fig, x, y, s, va="top"):
    fig.text(x, y, s, ha="left", va=va, fontsize=9, fontweight="bold", color=INK)
