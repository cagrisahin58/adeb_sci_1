#!/usr/bin/env python
"""Shared project-side helpers for the card (data) figures of adeb_sci_1 (visio-cizici, style 7).

Written by the card-figure agent (gorsel-uretici), 31.10.2026, Faz B. It replaces nothing and
depends on nothing project-specific except paper/figures/konsey/konsey_ortak.py (data rules,
reference-sheet comparisons; imported, never edited). It does NOT use paper/figures/visio/
_vz_ortam.py: the venue ``ieee_access`` is in the skill's REGISTRY since 31.10.2026.

What it does:

* ``kur()``  sets VZ_PROJE_KOKU / VZ_PROJE_AYARI, changes to the repository root (the konsey
  data rules read relative paths), and puts the skill and paper/figures/konsey on sys.path.
* ``basla(no)`` opens a figspec session in style ``no`` with the paper palette
  paper/figures/visio/palettes/adeb_konsey_uslup_<no>.yaml.
* ``eksen(ax)`` applies the style's veri_grafigi tokens (grey plot area, white grid both ways,
  no ticks) and keeps ONE spine, the value axis' baseline, as a thin ink line.
  Karar: the baseline stays, because the data-area gate (pdfolcu.data_area_share) can only
  measure a figure that has a dark horizontal axis stroke; a spineless figure returns "no data
  axis found" and the task forbids an unmeasured exemption.
* ``kaydet(...)`` runs cards.Canvas.save (millimetre controller first), writes the kanit file
  through the skill's write_kanit and extends it with the reference-sheet comparison, the keys
  read, the drawn values, git and the script path.
* ``ajan(...)`` writes <stem>.denge_ajan.json (answers to what the PDF cannot show).
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROOT_S = str(ROOT).replace("\\", "/")
SKILL = Path.home() / ".claude" / "skills" / "visio-cizici"
OUT_REL = "paper/figures/charts"
VENUE = "ieee_access"


def kur():
    os.environ.setdefault("VZ_PROJE_KOKU", ROOT_S)
    os.environ.setdefault("VZ_PROJE_AYARI", ROOT_S + "/paper/figures/visio_cizici.yaml")
    os.chdir(ROOT_S)
    for p in (str(SKILL), ROOT_S + "/paper/figures/konsey"):
        if p not in sys.path:
            sys.path.insert(0, p)


kur()
import numpy as np  # noqa: E402
from motor import figspec  # noqa: E402
from motor.figspec import cards  # noqa: E402
from motor.figspec.kanit import write_kanit  # noqa: E402
import konsey_ortak as K  # noqa: E402

OUT = Path(OUT_REL)
ST = U = PAL = VG = None


def argumanlar(doc):
    ap = argparse.ArgumentParser(description=doc.splitlines()[0])
    ap.add_argument("--uslup", required=True, help="catalogue style (this paper: 7 for data figures)")
    a, _ = ap.parse_known_args()
    return a


def basla(no):
    global ST, U, PAL, VG
    ST = figspec.use(venue=VENUE, palette=f"paper/figures/visio/palettes/adeb_konsey_uslup_{no}.yaml",
                     uslup=no)
    # recorded as the manifest's palette_path, so denge.py and fig_qc.py read the file drawn with
    ST.palette_path = f"{ROOT_S}/paper/figures/visio/palettes/adeb_konsey_uslup_{no}.yaml"
    U = ST.uslup
    PAL = ST.palette
    VG = (U.raw.get("bilesen_kurallari") or {}).get("veri_grafigi") or {}
    return ST


def vg():
    """The style's data-graphic tokens with the skill's defaults (motor/figspec/veri_dili.py).

    Style 7 writes five keys the reader does not know (eksen, izgara_rengi, cizim_alani, aralik,
    lejant), so veri_dili.veri_grafigi_oku raises on it (skill-side inconsistency, reported as an
    open issue). Here the known keys are read with veri_dili's own defaults and the style-7 keys
    are kept as they are; nothing is invented."""
    from motor.figspec import veri_dili
    raw = dict(VG)
    known = {k: raw[k] for k in raw if k in veri_dili.VERI_GRAFIGI_ANAHTARLARI}
    out = {k: known.get(k, spec["varsayilan"]) for k, spec in veri_dili.VERI_GRAFIGI_ANAHTARLARI.items()}
    out.update({k: v for k, v in raw.items() if k not in out})
    # Karar (duzeltme turu 2): line widths that style 7 does not set (referans_pt, baglayici_pt and
    # egim_pt fall back to veri_dili's 0.5 / 0.843 pt) are snapped to the nearest ST.weights token, so
    # the print carries only the style's stroke tokens (fig_mm_pdf --cizgi-kati)
    for k in ("referans_pt", "baglayici_pt", "egim_pt"):
        if k in out and k not in known:
            out[k] = agirlik(out[k])
    return out


def W(kind):
    return ST.venue.width_in(kind) * 25.4


def ent(key):
    """Palette entity (hex, marker, ls, label); a missing family stops the figure."""
    if key not in PAL.entities:
        K.fail(f"palette entity {key!r} missing in adeb_konsey_uslup_{U.no}.yaml "
               f"(regenerate with paper/figures/visio/_palet_uret.py; never hand-edit)")
    return PAL.entities[key]


def kenar(key):
    """Marker edge (hex, pt) of a palette entity: the palette's own marker_edge field when it has one
    (figspec's palette loader does not carry it, so the YAML is read), else ink and the style's
    marker edge."""
    import yaml
    raw = yaml.safe_load(Path(ST.palette_path).read_text(encoding="utf-8"))
    me = ((raw.get("entities") or {}).get(key) or {}).get("marker_edge")
    if isinstance(me, dict) and me.get("hex"):
        # Karar (duzeltme turu 2): the palette's edge width (0.4 pt for cift_vit) is snapped to the
        # nearest stroke token of ST.weights, so every printed width is a style token (--cizgi-kati)
        return me["hex"], agirlik(float(me.get("pt", figspec.layout.marker_edge_pt(U))))
    return U.ink, figspec.layout.marker_edge_pt(U)


def agirlik(pt):
    """The ST.weights stroke token nearest to ``pt`` (thin 0.354, line 0.49, emph 0.55 in style 7)."""
    toks = sorted({float(ST.weights.grid), float(ST.weights.line), float(ST.weights.emph),
                   float(ST.weights.marker_edge), float(ST.weights.err)})
    return min(toks, key=lambda t: abs(t - float(pt)))


# --- error-bar semantics (duzeltme turu 2, finding "errorbar_kinds bos") -----------------------------
ARALIK = {}   # kind -> definition written to the manifest (errorbar_tanimlari)


def aralik(ax, kind, tanim):
    """Record that ``ax``'s figure draws an interval of ``kind`` (manifest errorbar_kinds) with a
    one-line definition. Kinds outside annotate.ERRORBAR_KINDS (ci90) are recorded the same way,
    with the definition saying why: the skill's list has no 90 % interval (open issue)."""
    fig = ax.get_figure()
    kinds = getattr(fig, "_figspec_errorbar_kinds", set())
    kinds.add(kind)
    fig._figspec_errorbar_kinds = kinds
    ARALIK[kind] = tanim


def hata(ax, key, x, y, *, kind, tanim, yerr=None, **kw):
    """Error bars through motor.figspec.annotate.errorbar when the kind is one it knows (sd, ci95),
    else through ax.errorbar plus aralik(); the weights default to the style's err tokens."""
    from motor.figspec import annotate
    kw.setdefault("elinewidth", ST.weights.err)
    kw.setdefault("capsize", ST.weights.err_cap)
    kw.setdefault("capthick", ST.weights.err)
    ARALIK[kind] = tanim
    if kind in annotate.ERRORBAR_KINDS:
        return annotate.errorbar(ax, key, x, y, kind=kind, yerr=yerr, **kw)
    aralik(ax, kind, tanim)
    kw.setdefault("fmt", "none")
    return ax.errorbar(x, y, yerr=yerr, **kw)


def minus(s):
    return s.replace("-", "−")


def tick_fmt(ax, axis="both", fmt=None):
    import matplotlib.pyplot as plt
    f = plt.FuncFormatter((lambda v, _: minus(fmt.format(v))) if fmt else (lambda v, _: minus(f"{v:g}")))
    if axis in ("x", "both"):
        ax.xaxis.set_major_formatter(f)
    if axis in ("y", "both"):
        ax.yaxis.set_major_formatter(f)


def eksen(ax, base="x", grid="both", nbins=None):
    """Style 7 plot area; ``base`` is the spine kept as the data axis ('x' bottom, 'y' left, None)."""
    for sp in ax.spines.values():
        sp.set_visible(False)
    if base == "x":
        ax.spines["bottom"].set_visible(True)
        ax.spines["bottom"].set_color(U.ink)
        ax.spines["bottom"].set_linewidth(ST.weights.axis)
    elif base == "y":
        ax.spines["left"].set_visible(True)
        ax.spines["left"].set_color(U.ink)
        ax.spines["left"].set_linewidth(ST.weights.axis)
    ax.tick_params(length=0, pad=1.5)
    alan = str(VG.get("cizim_alani", "#EAEAF2"))
    ax.set_facecolor(alan if alan.startswith("#") else "#FFFFFF")
    if grid:
        ax.grid(True, axis=grid, color=str(VG.get("izgara_rengi", "#FFFFFF")),
                linewidth=ST.weights.grid, zorder=0)
        other = {"x": "y", "y": "x", "both": None}[grid]
        if other:
            ax.grid(False, axis=other)
    else:
        ax.grid(False)
    ax.set_axisbelow(True)
    if nbins:
        ax.locator_params(axis="both", nbins=nbins)


def anahtar_ekseni(cv, card, inset=1.0):
    """An invisible axes inside a key-strip card that only holds a legend."""
    return bos_eksen(cv, card.x + inset, card.y + inset, card.w - 2 * inset, card.h - 2 * inset)


def bos_eksen(cv, x, y, w, h):
    """An invisible axes at a canvas mm box (inside a card) that only holds a legend or text."""
    ax = cv.axes(x, y, w, h)
    ax.set_facecolor("none")
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
    return ax


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def kaydet(cv, stem, *, message, inputs, degerler, foy, okunan, cizilen, notlar, kararlar, betik,
           sablon, ekstra=None):
    man = cv.save(stem, OUT, message=message, sources=list(inputs))
    # the card engine has no template argument; the plan's template (04_cizim_plani.md section 3)
    # is added to the manifest so denge.py reads the style's F range for it
    mp = OUT / f"{stem}.fig.json"
    mj = json.loads(mp.read_text(encoding="utf-8"))
    mj["sablon"] = sablon
    if mj.get("errorbar_kinds"):
        # what each recorded interval kind means here (fig_qc D3 reads errorbar_kinds; ci90 is not in
        # annotate.ERRORBAR_KINDS, its definition says so)
        mj["errorbar_tanimlari"] = {k: ARALIK.get(k, "") for k in mj["errorbar_kinds"]}
    with io.open(mp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(mj, indent=2, ensure_ascii=False) + "\n")
    p = write_kanit(stem, OUT, uslup_no=U.no, degerler=degerler, records=None)
    k = json.loads(Path(p).read_text(encoding="utf-8"))
    k.update({
        "betik": betik,
        "ortak_modul": "paper/figures/charts/_kart_ortak.py",
        "veri_kurali_modulu": "paper/figures/konsey/konsey_ortak.py (imported unchanged)",
        "girdiler_sha256": {str(i): sha(i) for i in inputs},
        "foy_karsilastirmasi": foy,
        "okunan_anahtarlar": okunan,
        "cizilen": cizilen,
        "notlar": notlar,
        "kararlar": kararlar,
        "git": git_bilgisi(list(inputs), betik),
        "uslup": U.no,
        "venue": VENUE,
        "tuval_mm": [round(cv.W, 3), round(cv.H, 3)],
    })
    if ekstra:
        k.update(ekstra)
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(k, indent=2, ensure_ascii=False, default=float) + "\n")
    print(f"written: {OUT / stem}.pdf  ({cv.W:.2f} x {cv.H:.2f} mm); foy comparisons "
          f"{foy['karsilastirma_sayisi']}, mismatching {foy['uyusmayan']}; kanit values {len(degerler)}")
    return man


def git_bilgisi(inputs, betik):
    """Provenance (duzeltme turu 2): commit and branch, the git status of every file the figure
    depends on (inputs, the figure script, this module, the konsey modules it imported, the reference
    sheet and the palette) and the SHA-256 of each code and sheet file, because the scripts are not
    yet committed and a commit alone cannot rebuild the figure."""
    kod = {betik.split(" ")[0], "paper/figures/charts/_kart_ortak.py", str(K.FOY).replace("\\", "/"),
           f"paper/figures/visio/palettes/adeb_konsey_uslup_{U.no}.yaml"}
    root = Path(ROOT_S).resolve()
    for m in list(sys.modules.values()):
        f = getattr(m, "__file__", None)
        if not f:
            continue
        try:
            rel = Path(f).resolve().relative_to(root)
        except Exception:
            continue
        if rel.parts[:2] == ("paper", "figures"):
            kod.add(rel.as_posix())
    kod = sorted(kod)
    g = K.git_info(list(inputs) + kod)
    g["izlenen_yollar"] = [str(i) for i in inputs] + kod
    g["kod_ve_foy_sha256"] = {p: sha(p) for p in kod if Path(p).is_file()}
    g["not"] = ("dirty_or_untracked lists every path above that is modified or untracked; until the "
                "scripts are committed, kod_ve_foy_sha256 is what pins the code and the sheet")
    return g


def deger(etiket, v, kaynak, yol, hesap, foy_satiri=None):
    d = {"etiket": etiket, "deger": float(v) if isinstance(v, (np.floating,)) else v, "kaynak": kaynak,
         "anahtar_yolu": yol, "hesap": hesap}
    if foy_satiri is not None:
        d["foy_satiri"] = foy_satiri
    return d


def ajan(stem, *, iddia, dogrudan_etiket, renk_haritasi=None):
    """Answer file for motor/host/denge.py (items a PDF cannot show), reasons of 3+ words."""
    y = {
        "3b_veri": {"deger": False, "gerekce": "every panel is a flat two-dimensional chart"},
        "3b_kural_disi": {"deger": False, "gerekce": "no 3D object, perspective, shadow or gradient is drawn"},
        "clip_art": {"deger": False, "gerekce": "no raster or clip-art element is drawn"},
        "gokkusagi_renk_haritasi": {"deger": False, "gerekce": renk_haritasi or "no continuous colour map is drawn"},
        "sus_arka_plan": {"deger": False, "gerekce": "the grey fill is the style's plot-area card only"},
        "gereksiz_ikon": {"deger": False, "gerekce": "no icon is drawn, only data marks"},
        "dogrudan_etiket": {"deger": True, "gerekce": dogrudan_etiket},
        "gercek_goruntu": {"deger": "uygulanmaz", "gerekce": "a data chart of measured statistics, no images"},
        "panel_basina_bir_iddia": {"deger": True, "gerekce": iddia},
        "her_sayinin_kaynagi": {"deger": True,
                                "gerekce": "every drawn number is in the kanit file with source and key path"},
    }
    p = OUT / f"{stem}.denge_ajan.json"
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"stem": stem, "gercek_goruntu_sayisi": 0, "yanitlar": y}, indent=1,
                            ensure_ascii=False) + "\n")
    return p
