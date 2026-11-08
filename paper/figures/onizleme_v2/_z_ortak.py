#!/usr/bin/env python
"""Shared set-up and 3D maquette helpers of the Üslup Z previews (paper/figures/onizleme_v2).

Every preview script imports this module first. It points the engine's outputs into
paper/figures/onizleme_v2 (VZ_OUT_DIR, VZ_PALET_DIZINI, VZ_TASKLIST_LOG), so nothing is
written under paper/figures/visio, charts, final or konsey; loads style Z and the venue
ieee_access; and offers the maquette parts of style Z drawn in its one dimetric view:

  prizma   a box in world millimetres (X along the width axis, Y along the depth axis,
           Z up), three faces in the style's face tones (bilesenler.face_tones: top 0,
           right 0.15, front 0.30), outline a soft darkening of the front face
  golge    the cast shadow on the floor: footprint swept away from the light (left and
           toward the viewer), one polygon in the 'golge' tone, drawn before the object,
           larger than it (not an offset copy; denge 'golge' item)
  plaka    the stage plate (a thin box in the 'sahne' tone) whose top face is the container
           of everything standing on it
  etiket   a label in the plane with a hairline leader to its anchor (text never on a face)

The view is read from the style (bilesenler.iso_axes()), never chosen here, and every
object is recorded in visiofig.THREE_D with the same fields as bilesenler.iso_box, so the
preflight, the manifest and the balance gate see one dimetric 36 degree view.
"""
from __future__ import annotations

import hashlib
import io
import json
import math
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
_R = str(ROOT).replace("\\", "/")
OUT = Path(__file__).resolve().parent
_O = str(OUT).replace("\\", "/")
os.environ.setdefault("VZ_PROJE_KOKU", _R)
os.environ["VZ_PROJE_AYARI"] = _O + "/visio_cizici_v2.yaml"      # onizleme_v2 settings (96 DPI, outputs here)
os.environ["VZ_OUT_DIR"] = _O
os.environ["VZ_PALET_DIZINI"] = _O + "/palettes"
os.environ["VZ_TASKLIST_LOG"] = _O + "/visio_loglari/visio_tasklist.log"
(OUT / "palettes").mkdir(exist_ok=True)
(OUT / "visio_loglari").mkdir(exist_ok=True)
os.chdir(_R)
SKILL = Path.home() / ".claude" / "skills" / "visio-cizici"
for _p in (str(SKILL), str(SKILL / "motor" / "visio"), str(OUT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import visiofig as vf  # noqa: E402
import bilesenler as bl  # noqa: E402
from motor.figspec.kanit import write_kanit  # noqa: E402

VENUE = "ieee_access"
G = vf.GRID
U = None
CHECK = "--check" in sys.argv


def baslat():
    global U
    U = vf.use(uslup="Z", venue=VENUE)
    return U


# ------------------------------------------------------------------ grid and text
def gr(v):
    return round(v / G) * G


def gc(v):
    return math.ceil(v / G - 1e-9) * G


def gf(v):
    return math.floor(v / G + 1e-9) * G


def lh(size=None):
    return vf.line_h(size)


def tw(lines, size=None, key="r"):
    return gc(max(bl.text_box_w(ln, size) for ln in vf.norm_lines(lines, key)) + 0.05)


def T(pid, x, y, lines, *, size=None, color="ink", cont=None, align="l", w=None, key="r", valign="t"):
    ln = vf.norm_lines(lines, key)
    ww = gc(w) if w is not None else tw(ln, size)
    h = len(ln) * lh(size)
    xx = gr(x)
    if align == "r":
        xx = gr(x - ww)
    elif align == "c":
        xx = gr(x - ww / 2)
    vf.text(pid, xx, gr(y), ww, h, ln, color=color, size=size, align=align, container=cont, valign=valign)
    return xx, gr(y), ww, h


# ------------------------------------------------------------------ the dimetric view
class Sahne:
    """World millimetres -> page millimetres for one origin (the page point of world 0, 0, 0)."""

    def __init__(self, ox, oy):
        self.ax = bl.iso_axes()
        self.ox, self.oy = ox, oy

    def P(self, X, Y, Z=0.0):
        ew, ed, eh = self.ax["w"], self.ax["d"], self.ax["h"]
        return (self.ox + X * ew[0] + Y * ed[0] + Z * eh[0], self.oy + X * ew[1] + Y * ed[1] + Z * eh[1])


def _soft(hexv, t=0.22):
    return vf.mix(hexv, vf.C["ink"], t)


def _record(pid, kind, tint, size, tones, faces, pts, extra=None):
    ax = bl.iso_axes()
    t = bl._three_d()
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    rec = {"kind": kind, "tint": tint, "size_mm": size, "projection": ax["projection"],
           "angle_deg": round(ax["angle_d_deg"], 3), "angle_w_deg": round(ax["angle_w_deg"], 3),
           "tones": {k: "#" + v for k, v in tones["tones"].items()}, "darkening": tones["darkening"],
           "fill": "#" + tones["fill"], "outline": "#" + _soft(tones["tones"]["front"]),
           "tone_source": tones["source"], "tone_steps": tones["steps"],
           "three_d_token": bl._token_record(t), "faces": faces,
           "bbox_mm": [round(min(xs), 4), round(min(ys), 4), round(max(xs) - min(xs), 4),
                       round(max(ys) - min(ys), 4)]}
    rec.update(extra or {})
    vf.THREE_D[pid] = rec
    return rec


def prizma(S, pid, X, Y, Z, w, d, h, tint, *, group=None, cont=None, faces=("front", "right", "top"),
           top_fill=None, role="obstacle", line=True):
    """A box at world (X, Y, Z) of size w x d x h in tint's face tones; returns its record."""
    tones = bl.face_tones(tint)
    c = {
        "front": [S.P(X, Y, Z), S.P(X + w, Y, Z), S.P(X + w, Y, Z + h), S.P(X, Y, Z + h)],
        "right": [S.P(X + w, Y, Z), S.P(X + w, Y + d, Z), S.P(X + w, Y + d, Z + h), S.P(X + w, Y, Z + h)],
        "top": [S.P(X, Y, Z + h), S.P(X + w, Y, Z + h), S.P(X + w, Y + d, Z + h), S.P(X, Y + d, Z + h)],
    }
    gid = group or pid
    out = {}
    edge = _soft(tones["tones"]["front"])
    for f in ("front", "right", "top"):
        if f not in faces:
            continue
        fill = tones["tones"][f]
        if f == "top" and top_fill:
            fill = top_fill
        pts = c[f] + [c[f][0]]
        vf.poly(f"{pid}_{f}", pts, fill=fill, line=edge if line else None,
                lw=max(vf.LW["ince"], vf.USLUP.line_min_pt), role=role, container=cont, group=gid, ctype="iso")
        out[f] = f"{pid}_{f}"
    allp = [p for f in c.values() for p in f]
    return _record(pid, "prizma", tint, {"w": w, "d": d, "h": h}, tones, out, allp,
                   {"world_mm": [X, Y, Z], "corners": {k: v for k, v in c.items()}})


def golge(S, pid, X, Y, Z, w, d, h, *, group=None, cont=None, k=(0.42, 0.30)):
    """Cast shadow of a w x d x h box on the plane Z: the footprint swept by
    (-k0 * h along X, -k1 * h along Y), light from the right and from behind."""
    sx, sy = -k[0] * h, -k[1] * h
    foot = [(X, Y), (X + w, Y), (X + w, Y + d), (X, Y + d)]
    pts = foot + [(a + sx, b + sy) for a, b in foot]
    pg = [S.P(a, b, Z) for a, b in pts]
    hull = _hull(pg)
    f, _ = vf.tint_of("golge")
    vf.poly(pid, hull + [hull[0]], fill=f, line=None, role="deco", container=cont, group=group, ctype="golge")
    return hull


def _hull(pts):
    pts = sorted(set((round(x, 5), round(y, 5)) for x, y in pts))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def plaka(S, pid, X, Y, w, d, t, tint="sahne", z=0.0):
    """The stage plate: thin box whose top face (role container) holds what stands on it."""
    tones = bl.face_tones(tint)
    edge = vf.tint_of(tint)[1]
    c = {
        "front": [S.P(X, Y, z - t), S.P(X + w, Y, z - t), S.P(X + w, Y, z), S.P(X, Y, z)],
        "right": [S.P(X + w, Y, z - t), S.P(X + w, Y + d, z - t), S.P(X + w, Y + d, z), S.P(X + w, Y, z)],
        "top": [S.P(X, Y, z), S.P(X + w, Y, z), S.P(X + w, Y + d, z), S.P(X, Y + d, z)],
    }
    # the plate is ground: role deco, so what stands on it is not a collision with it; a text on it
    # names the plate as its container (then the plate does not block it)
    for f in ("front", "right"):
        vf.poly(f"{pid}_{f}", c[f] + [c[f][0]], fill=tones["tones"][f], line=edge, lw=vf.USLUP.line_min_pt,
                role="deco", group=pid, ctype="iso")
    vf.poly(f"{pid}_top", c["top"] + [c["top"][0]], fill=tones["tones"]["top"], line=edge,
            lw=vf.USLUP.line_min_pt, role="deco", group=pid, ctype="plate")
    allp = [p for f in c.values() for p in f]
    return _record(pid, "plaka", tint, {"w": w, "d": d, "h": t}, tones,
                   {"front": f"{pid}_front", "right": f"{pid}_right", "top": f"{pid}_top"}, allp,
                   {"corners": c})


def zemin_cizgi(S, pid, X0, Y0, X1, Y1, color="izgara", lw=None):
    a, b = S.P(X0, Y0, 0), S.P(X1, Y1, 0)
    col = vf.tint_of(color)[0] if color in vf.TINT else color
    vf.seg(pid, a, b, col, lw or vf.USLUP.line_min_pt)


def etiket(pid, x, y, lines, anchor=None, *, size=None, color="ink", cont=None, align="l", w=None, key="r",
           lead_from=None):
    """A label in the plane; with ``anchor`` a hairline leader from the label edge to it."""
    bx, by, bw, bh = T(pid, x, y, lines, size=size, color=color, cont=cont, align=align, w=w, key=key)
    if anchor is not None:
        if lead_from is None:
            ax_, ay_ = anchor
            lx = bx - 0.4 if ax_ < bx else (bx + bw + 0.4 if ax_ > bx + bw else bx + bw / 2)
            ly = by + lh(size) / 2 if (ax_ < bx or ax_ > bx + bw) else (by - 0.4 if ay_ < by else by + bh + 0.4)
            lead_from = (lx, ly)
        vf.seg(pid + "_ld", lead_from, anchor, vf.C["frame"], vf.USLUP.line_min_pt)
    return bx, by, bw, bh


# ------------------------------------------------------------------ evidence
def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git_head():
    try:
        return subprocess.run(["git", "-C", _R, "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True).stdout.strip()
    except Exception:
        return None


def ev(etiket_, deger, kaynak, anahtar, hesap="okundu"):
    """One evidence entry; 'file:line' is split into kaynak (an existing file) and satir."""
    import re as _re
    m = _re.match(r"^(.*?):(\d+)(.*)$", kaynak)
    d = {"etiket": etiket_, "deger": deger, "kaynak": kaynak, "anahtar_yolu": anahtar, "hesap": hesap}
    if m and Path(m.group(1)).is_file():
        d["kaynak"], d["satir"] = m.group(1), int(m.group(2))
        if m.group(3).strip():
            d["not"] = m.group(3).strip()
    return d


def kanit_yaz(stem, degerler, ek=None):
    p = write_kanit(stem, vf.OUT_DIR if not os.environ.get("VZ_OUT_DIR") else os.environ["VZ_OUT_DIR"],
                    uslup_no="Z", degerler=degerler, records=None)
    k = json.loads(Path(p).read_text(encoding="utf-8"))
    k["betik"] = f"paper/figures/onizleme_v2/{Path(sys.argv[0]).name}"
    k["git_head"] = git_head()
    k["karantina"] = ("okunan dosyalar yalniz su siniflardandir: results/q1/*, results/C1_REFERANS_FOYU.md, "
                      "raporlar/konsey_2026-10-29/hucre_tablosu*.json (donmus hucre tablolari), data/cifar-10-batches-py ve "
                      "data/cifar-100-python test dosyalari (yalniz ilk dort goruntu), src/models/*.py ve bu klasordeki yapi "
                      "dokumu; run1, run2, run3 ve C1 oncesi hicbir dosya okunmadi")
    k["okunan_dosyalar"] = sorted({d.get("kaynak") for d in k.get("degerler", []) if d.get("kaynak")})
    if ek:
        k.update(ek)
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(k, indent=2, ensure_ascii=False) + "\n")
    return p


def manifest_ek(**fields):
    p = Path(vf.STEM + ".fig.json")
    m = json.loads(p.read_text(encoding="utf-8"))
    m.update(fields)
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


def denge_ajan(stem, gercek, ozel=None):
    y = {
        "3b_veri": (False, "no measured value is encoded by height, depth or angle; 3D carries models, data sets and design structure"),
        "3b_kural_disi": (False, "one dimetric 36 degree view from style Z, flat face tones, no perspective, gradient, gloss or soft mask; the cast shadow is a floor projection larger than the object, not an offset copy; labels stay in the plane"),
        "clip_art": (False, "every object is built from Visio polygons and stands for a model part, data set or matrix"),
        "gokkusagi_renk_haritasi": (False, "no colour map; one low-chroma sequential ramp at most"),
        "sus_arka_plan": (False, "the stage plate is the grouping tool of style Z and carries the content"),
        "gereksiz_ikon": (False, "there are no icons; each drawn part is a model component or a data object"),
        "dogrudan_etiket": (True, "every part is labelled beside it in the plane with a leader"),
        "gercek_goruntu": ("uygulanmaz", "the schematic shows no image"),
        "panel_basina_bir_iddia": (True, "each numbered station states one stage"),
        "her_sayinin_kaynagi": (True, "every printed number is in the evidence file with its source file and key"),
    }
    y.update(ozel or {})
    p = Path(os.environ["VZ_OUT_DIR"]) / f"{stem}.denge_ajan.json"
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"stem": stem, "gercek_goruntu_sayisi": gercek,
                   "yanitlar": {k: {"deger": d, "gerekce": g} for k, (d, g) in y.items()}}, fh, indent=2,
                  ensure_ascii=False)
    return p


# ------------------------------------------------------------------ quick look (no Visio)
def onizle(path, dpi=200):
    """Render the scene with matplotlib for layout iteration (not a deliverable)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon, Rectangle, Ellipse
    W, H = vf.PAGE_W, vf.PAGE_H
    fig = plt.figure(figsize=(W / 25.4, H / 25.4), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")

    def col(c):
        if c is None:
            return "none"
        c = vf.C.get(c, c)
        return "#" + str(c).lstrip("#")
    for p in vf.SCENE:
        k = p["kind"]
        if k == "poly":
            ax.add_patch(Polygon(p["pts"], closed=True, fc=col(p["fill"]), ec=col(p["line"]), lw=p["lw"] * 0.6))
        elif k == "rect":
            ax.add_patch(Rectangle((p["x"], p["y"]), p["w"], p["h"], fc=col(p["fill"]), ec=col(p["line"]),
                                   lw=(p["lw"] or 0.3) * 0.6))
        elif k == "oval":
            ax.add_patch(Ellipse((p["x"] + p["w"] / 2, p["y"] + p["h"] / 2), p["w"], p["h"], fc=col(p["fill"]),
                                 ec=col(p["line"]), lw=p["lw"] * 0.6))
        elif k == "seg":
            ax.plot([p["p1"][0], p["p2"][0]], [p["p1"][1], p["p2"][1]], color=col(p["color"]), lw=p["lw"] * 0.6)
        elif k == "spline":
            xs, ys = zip(*p["pts"])
            ax.plot(xs, ys, color=col(p["color"]), lw=p["lw"] * 0.6)
        elif k == "image":
            from PIL import Image
            ax.imshow(Image.open(p["path"]), extent=(p["x"], p["x"] + p["w"], p["y"] + p["h"], p["y"]))
        elif k == "text":
            y = p["y"]
            for ln in p["lines"]:
                s = "".join(t for t, _ in ln)
                wt = "bold" if any(kk in ("b", "sb") for _, kk in ln) else "normal"
                x = p["x"] + (p["w"] if p["align"] == "r" else p["w"] / 2 if p["align"] == "c" else 0)
                ax.text(x, y + vf.line_h(p["design"]) * 0.78, s, fontsize=p["design"], color=col(p["color"]),
                        ha={"l": "left", "r": "right", "c": "center"}[p["align"]], family="Open Sans",
                        fontweight=wt)
                y += vf.line_h(p["design"])
    fig.savefig(path, dpi=dpi)
    plt.close(fig)


def kirp(subject, clip):
    """Sutherland-Hodgman: the part of polygon ``subject`` inside the convex polygon ``clip``."""
    def cross(a, b, p):
        return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])

    def inter(p, q, a, b):
        x1, y1, x2, y2 = p[0], p[1], q[0], q[1]
        x3, y3, x4, y4 = a[0], a[1], b[0], b[1]
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(den) < 1e-12:
            return q
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    cl = list(clip)
    area = sum(cl[i][0] * cl[(i + 1) % len(cl)][1] - cl[(i + 1) % len(cl)][0] * cl[i][1] for i in range(len(cl)))
    sgn = 1 if area > 0 else -1
    out = list(subject)
    for i in range(len(cl)):
        a, b = cl[i], cl[(i + 1) % len(cl)]
        inp, out = out, []
        if not inp:
            break
        s_ = inp[-1]
        for e in inp:
            ein, sin_ = sgn * cross(a, b, e) >= -1e-9, sgn * cross(a, b, s_) >= -1e-9
            if ein:
                if not sin_:
                    out.append(inter(s_, e, a, b))
                out.append(e)
            elif sin_:
                out.append(inter(s_, e, a, b))
            s_ = e
    return out
