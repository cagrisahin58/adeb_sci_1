#!/usr/bin/env python
"""Shared set-up, maquette parts and gates glue of the Üslup Z figures v2 (paper/figures_v2).

Derived from paper/figures/onizleme_v2/_z_ortak.py (Faz 1). Moving these parts into the engine's
bilesenler.py was a Faz 2 precondition; it was not done in this round, so this file is the single copy
(the Faz 1 copy stays where it is, untouched). Every figure script imports this module first. It points
every engine output into paper/figures_v2/yapim (VZ_OUT_DIR, VZ_PALET_DIZINI, VZ_TASKLIST_LOG,
VZ_PROJE_AYARI = paper/figures_v2/visio_cizici_v2.yaml), so nothing is written under paper/figures or
paper/manuscript, loads style Z (version 3) and the venue ieee_access, and offers:

  Sahne / prizma / golge / plaka   the dimetric 36 degree maquette parts (one view, style face tones)
  kart                             an upright card whose face is a true page rectangle: a vertical plane
                                   through world Z and the floor direction u that projects to page-
                                   horizontal, so it is drawn in the same dimetric projection (no second
                                   view); its thickness runs along the floor normal n
  Olcek, isaret, kot               2D data inside a card face (scale, markers, base line with ticks)
  istasyon                         ring-numbered station title (naming step 3)
  ev, kanit_yaz, manifest_ek, denge_ajan, bitir   evidence, manifest, balance answers, run
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import math
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
_R = str(ROOT).replace("\\", "/")
_H = str(HERE).replace("\\", "/")
OUT = HERE / "yapim"
_O = str(OUT).replace("\\", "/")
os.environ["VZ_PROJE_KOKU"] = _R
os.environ["VZ_PROJE_AYARI"] = _H + "/visio_cizici_v2.yaml"
os.environ["VZ_OUT_DIR"] = _O
os.environ["VZ_PALET_DIZINI"] = _H + "/palettes"
os.environ["VZ_TASKLIST_LOG"] = _H + "/visio_loglari/visio_tasklist.log"
os.environ["VZ_USLUP"] = "Z"
for _d in ("yapim", "palettes", "visio_loglari", "qc"):
    (HERE / _d).mkdir(exist_ok=True)
os.chdir(_R)
SKILL = Path.home() / ".claude" / "skills" / "visio-cizici"
for _p in (str(SKILL), str(SKILL / "motor" / "visio"), _H, _R + "/paper/figures/konsey"):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import visiofig as vf  # noqa: E402
import bilesenler as bl  # noqa: E402
from motor.figspec.kanit import write_kanit  # noqa: E402

VENUE = "ieee_access"
G = vf.GRID
U = None
CHECK = "--check" in sys.argv
BAK = "--bak" in sys.argv
S8 = B9 = TT = None
KARANTINA = ("okunan dosyalar yalniz su siniflardandir: results/q1/*, results/C1_REFERANS_FOYU.md, "
             "raporlar/konsey_2026-10-29/hucre_tablosu*.json (donmus hucre tablolari), src/models/*.py ve "
             "paper/figures/onizleme_v2/pv_b_model_yapisi.txt (yapi dokumu), salt okunur ice aktarilan v1 sekil "
             "betiklerinin veri() kurallari; run1, run2, run3, attention_analysis_run3, stat_addendum, rev2_blockA "
             "ve C1 oncesi hicbir dosya okunmadi")


def baslat():
    global U, S8, B9, TT
    U = vf.use(uslup="Z", venue=VENUE)
    S8, B9, TT = vf.SMALL, vf.BODY, vf.TITLE
    return U


def yukle(path, name):
    """Import a v1 figure script read-only under a unique module name (its main() is not run)."""
    p = ROOT / path
    spec = importlib.util.spec_from_file_location(name, str(p))
    mod = importlib.util.module_from_spec(spec)
    kon = _R + "/paper/figures/konsey"
    while kon in sys.path:          # _kart_ortak.kur() puts konsey ahead of charts, as in v1
        sys.path.remove(kon)
    sys.path.append(str(p.parent))
    extra = [] if "--uslup" in sys.argv else ["--uslup", "Z"]
    sys.argv += extra
    try:
        spec.loader.exec_module(mod)
    finally:
        if extra:
            del sys.argv[-2:]
        if kon not in sys.path:
            sys.path.insert(0, kon)
    return mod


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


def _en_dash(obj):
    """U+2212 -> U+2013 in every string of a (nested) line/run structure (T6: outside Windows-1252)."""
    if isinstance(obj, str):
        return obj.replace("−", "–")
    if isinstance(obj, tuple):
        return tuple(_en_dash(o) for o in obj)
    if isinstance(obj, list):
        return [_en_dash(o) for o in obj]
    return obj


def T(pid, x, y, lines, *, size=None, color="ink", cont=None, align="l", w=None, key="r", valign="t"):
    ln = vf.norm_lines(_en_dash(lines), key)
    ww = gc(w) if w is not None else tw(ln, size)
    h = len(ln) * lh(size)
    xx = gr(x)
    if align == "r":
        xx = gr(x - ww)
    elif align == "c":
        xx = gr(x - ww / 2)
    vf.text(pid, xx, gr(y), ww, h, ln, color=color, size=size, align=align, container=cont, valign=valign)
    return xx, gr(y), ww, h


def fmt(v, nd=2, plus=False):
    s = f"{v:+.{nd}f}" if plus else f"{v:.{nd}f}"
    # T6 (08.11.2026): Visio maps every glyph outside Windows-1252 to a blank in the PDF text layer; U+2212 is
    # outside it, the en dash U+2013 is inside, so negative numbers print with the en dash (copy-paste keeps them)
    return s.replace("-", "–")


# ------------------------------------------------------------------ the dimetric view
class Sahne:
    """World millimetres -> page millimetres for one origin (the page point of world 0, 0, 0)."""

    def __init__(self, ox, oy):
        self.ax = bl.iso_axes()
        self.ox, self.oy = ox, oy
        ew, ed = self.ax["w"], self.ax["d"]
        b = ew[1] / ed[1]                         # a*ew_y + b*ed_y = 0 with a = 1
        self.u = (1.0, -b)                        # world floor direction that projects to page +x
        self.u_page = ew[0] - b * ed[0]
        nn = math.hypot(*self.u)
        self.n = (b / nn, 1.0 / nn) if False else (-self.u[1] / nn, self.u[0] / nn)

    def P(self, X, Y, Z=0.0):
        ew, ed, eh = self.ax["w"], self.ax["d"], self.ax["h"]
        return (self.ox + X * ew[0] + Y * ed[0] + Z * eh[0], self.oy + X * ew[1] + Y * ed[1] + Z * eh[1])

    def W(self, x, y, Z=0.0):
        """Inverse on the plane Z: page (x, y) -> world (X, Y)."""
        ew, ed = self.ax["w"], self.ax["d"]
        px, py = x - self.ox, y - self.oy + Z
        det = ew[0] * ed[1] - ed[0] * ew[1]
        return ((px * ed[1] - ed[0] * py) / det, (ew[0] * py - px * ew[1]) / det)


def soft(hexv, t=0.22):
    return vf.mix(hexv, vf.C["ink"], t)


def _record(pid, kind, tint, size, tones, faces, pts, extra=None):
    ax = bl.iso_axes()
    t = bl._three_d()
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    rec = {"kind": kind, "tint": tint, "size_mm": size, "projection": ax["projection"],
           "angle_deg": round(ax["angle_d_deg"], 3), "angle_w_deg": round(ax["angle_w_deg"], 3),
           "tones": {k: "#" + v for k, v in tones["tones"].items()}, "darkening": tones["darkening"],
           "fill": "#" + tones["fill"], "outline": "#" + soft(tones["tones"]["front"]),
           "tone_source": tones["source"], "tone_steps": tones["steps"],
           "three_d_token": bl._token_record(t), "faces": faces,
           "bbox_mm": [round(min(xs), 4), round(min(ys), 4), round(max(xs) - min(xs), 4),
                       round(max(ys) - min(ys), 4)]}
    rec.update(extra or {})
    vf.THREE_D[pid] = rec
    return rec


def prizma(S, pid, X, Y, Z, w, d, h, tint, *, group=None, cont=None, faces=("front", "right", "top"),
           top_fill=None, role="obstacle", line=True, lw=None, rol=None):
    """A box at world (X, Y, Z) of size w x d x h in tint's face tones; returns its record.
    ``rol="veri"`` marks a box whose height carries a measured value (K7, twin coding required)."""
    tones = bl.face_tones(tint)
    c = {
        "front": [S.P(X, Y, Z), S.P(X + w, Y, Z), S.P(X + w, Y, Z + h), S.P(X, Y, Z + h)],
        "right": [S.P(X + w, Y, Z), S.P(X + w, Y + d, Z), S.P(X + w, Y + d, Z + h), S.P(X + w, Y, Z + h)],
        "top": [S.P(X, Y, Z + h), S.P(X + w, Y, Z + h), S.P(X + w, Y + d, Z + h), S.P(X, Y + d, Z + h)],
    }
    gid = group or pid
    out = {}
    edge = soft(tones["tones"]["front"])
    for f in ("front", "right", "top"):
        if f not in faces:
            continue
        fill = tones["tones"][f]
        if f == "top" and top_fill:
            fill = top_fill
        vf.poly(f"{pid}_{f}", c[f] + [c[f][0]], fill=fill, line=edge if line else None,
                lw=lw or vf.LW["ince"], role=role, container=cont, group=gid, ctype="iso")
        out[f] = f"{pid}_{f}"
    allp = [p for f in c.values() for p in f]
    ex = {"world_mm": [X, Y, Z], "corners": c}
    if rol:
        ex["rol"] = rol
    return _record(pid, "prizma", tint, {"w": w, "d": d, "h": h}, tones, out, allp, ex)


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


K_LIGHT = (0.42, 0.30)


def golge_pts(S, foot, h, Z=0.0, k=K_LIGHT):
    sx, sy = -k[0] * h, -k[1] * h
    pts = list(foot) + [(a + sx, b + sy) for a, b in foot]
    return _hull([S.P(a, b, Z) for a, b in pts])


def golge(S, pid, X, Y, Z, w, d, h, *, group=None, cont=None, k=K_LIGHT):
    """Cast shadow of a w x d x h box on the plane Z (light from the right and from behind)."""
    hull = golge_pts(S, [(X, Y), (X + w, Y), (X + w, Y + d), (X, Y + d)], h, Z, k)
    if not SAHNE:
        return hull
    f, _ = vf.tint_of("golge")
    vf.poly(pid, hull + [hull[0]], fill=f, line=None, role="deco", container=cont, group=group, ctype="golge")
    return hull


def plaka(S, pid, X, Y, w, d, t, tint="sahne", z=0.0, lw=None):
    """The stage plate: thin box whose top face holds what stands on it (role deco). Not drawn in flat mode."""
    if not SAHNE:
        return None
    tones = bl.face_tones(tint)
    edge = vf.tint_of(tint)[1]
    c = {
        "front": [S.P(X, Y, z - t), S.P(X + w, Y, z - t), S.P(X + w, Y, z), S.P(X, Y, z)],
        "right": [S.P(X + w, Y, z - t), S.P(X + w, Y + d, z - t), S.P(X + w, Y + d, z), S.P(X + w, Y, z)],
        "top": [S.P(X, Y, z), S.P(X + w, Y, z), S.P(X + w, Y + d, z), S.P(X, Y + d, z)],
    }
    for f in ("front", "right"):
        vf.poly(f"{pid}_{f}", c[f] + [c[f][0]], fill=tones["tones"][f], line=edge, lw=lw or vf.LW["ince"],
                role="deco", group=pid, ctype="iso")
    vf.poly(f"{pid}_top", c["top"] + [c["top"][0]], fill=tones["tones"]["top"], line=edge,
            lw=lw or vf.LW["ince"], role="deco", group=pid, ctype="plate")
    allp = [p for f in c.values() for p in f]
    return _record(pid, "plaka", tint, {"w": w, "d": d, "h": t}, tones,
                   {"front": f"{pid}_front", "right": f"{pid}_right", "top": f"{pid}_top"}, allp,
                   {"corners": c})


# ------------------------------------------------------------------ flat-card mode (third round, 09.11.2026)
# The user's feedback of 09.11.2026 ("sahne gösterimini azalt biraz"): a data chart is not framed by a plinth,
# slab, showcase, post, shelf or stage floor. A figure script that calls duz() before drawing turns the stage
# off: kart() draws only its face as a flat card (no thickness slivers, no cast shadow, no 3D record), plaka(),
# plaka_un() and golge() draw nothing, profil_kart() refuses. Style Z stays (palette, type, line tokens, card
# language); the five figures that keep the stage (1, 2, 3, 14, 17) never call duz() and draw as before.
SAHNE = True


def duz():
    """Turn the stage off for this figure (flat-card composition)."""
    global SAHNE
    SAHNE = False


def duz_kart(pid, x, y, w, h, tint="kutu", *, face_fill=None, lw=None, group=None, cont=None, edge=None):
    """A flat card of style Z: light sand face, one 0.75 pt edge, no thickness, no shadow. The face polygon is
    ``<pid>_face`` (the container of its 2D content, as for kart()). Returns (x, y, w, h)."""
    tones = bl.face_tones(tint)
    e = edge or soft(tones["tones"]["front"])
    e = vf.C.get(e, e)
    face = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    vf.poly(f"{pid}_face", face + [face[0]], fill=face_fill or tones["tones"]["top"], line=e,
            lw=lw or vf.LW["ince"], role="deco", group=group or pid, ctype="plate", container=cont)
    return x, y, w, h


def kart_duz(S, pid, X, Y, Zh, wp, hp, tint="kutu", *, face_fill=None, lw=None, group=None, cont=None):
    """A flat card at the page rectangle a kart() at world (X, Y, Zh) would face, in a figure that keeps its
    stage (third round: the readout and measurement cards of Figures 14 and 17 are flat, the stage object stays)."""
    p0 = S.P(X, Y, Zh)
    return duz_kart(pid, p0[0], p0[1] - hp, wp, hp, tint, face_fill=face_fill, lw=lw, group=group, cont=cont)


def kart(S, pid, X, Y, Z, wp, hp, tint="kutu", t=1.2, *, shadow=True, group=None, face_fill=None, lw=None,
         k=K_LIGHT, cont=None):
    """An upright card standing at world (X, Y, Z): its face is the vertical plane through Z and the floor
    direction u that projects to page-horizontal, so the face prints as a true page rectangle of wp x hp mm
    in the one dimetric view; the card is t mm thick along the floor normal n (top and right slivers).
    Returns the face rectangle (x, y, w, h) in page mm, the container of the 2D content.
    In flat-card mode (duz()) only the face is drawn, at the same page rectangle."""
    if not SAHNE:
        p0 = S.P(X, Y, Z)
        return duz_kart(pid, p0[0], p0[1] - hp, wp, hp, tint, face_fill=face_fill, lw=lw, group=group, cont=cont)
    a = wp / S.u_page
    ux, uy = S.u[0] * a, S.u[1] * a
    nx, ny = S.n[0] * t, S.n[1] * t
    A = (X, Y)
    B = (X + ux, Y + uy)
    gid = group or pid
    if shadow:
        foot = [A, B, (B[0] + nx, B[1] + ny), (A[0] + nx, A[1] + ny)]
        hull = golge_pts(S, foot, hp, Z, k)
        vf.poly(f"{pid}_g", hull + [hull[0]], fill=vf.tint_of("golge")[0], line=None, role="deco",
                group=gid, ctype="golge", container=cont)
    tones = bl.face_tones(tint)
    edge = soft(tones["tones"]["front"])
    p0 = S.P(A[0], A[1], Z)
    top = [S.P(A[0], A[1], Z + hp), S.P(B[0], B[1], Z + hp), S.P(B[0] + nx, B[1] + ny, Z + hp),
           S.P(A[0] + nx, A[1] + ny, Z + hp)]
    right = [S.P(B[0], B[1], Z), S.P(B[0] + nx, B[1] + ny, Z), S.P(B[0] + nx, B[1] + ny, Z + hp),
             S.P(B[0], B[1], Z + hp)]
    vf.poly(f"{pid}_top", top + [top[0]], fill=tones["tones"]["right"], line=edge, lw=lw or vf.LW["ince"],
            role="deco", group=gid, ctype="iso", container=cont)
    vf.poly(f"{pid}_right", right + [right[0]], fill=tones["tones"]["front"], line=edge,
            lw=lw or vf.LW["ince"], role="deco", group=gid, ctype="iso", container=cont)
    x0, y0 = p0[0], p0[1] - hp
    face = [(x0, y0), (x0 + wp, y0), (x0 + wp, y0 + hp), (x0, y0 + hp)]
    vf.poly(f"{pid}_face", face + [face[0]], fill=face_fill or tones["tones"]["top"], line=edge,
            lw=lw or vf.LW["ince"], role="deco", group=gid, ctype="plate", container=cont)
    _record(pid, "kart", tint, {"w": wp, "d": t, "h": hp}, tones,
            {"top": f"{pid}_top", "right": f"{pid}_right", "front": f"{pid}_face"}, face + top + right,
            {"world_mm": [X, Y, Z], "not": "face in the vertical plane through world Z and the page-horizontal "
                                           "floor direction; prints as a true rectangle in the dimetric view"})
    return x0, y0, wp, hp


def zemin_cizgi(S, pid, X0, Y0, X1, Y1, color="izgara", lw=None, Z=0.0):
    a, b = S.P(X0, Y0, Z), S.P(X1, Y1, Z)
    col = vf.tint_of(color)[0] if color in vf.TINT else vf.C.get(color, color)
    vf.seg(pid, a, b, col, lw or vf.LW["ince"])


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
        vf.seg(pid + "_ld", lead_from, anchor, vf.C["frame"], vf.LW["ince"])
    return bx, by, bw, bh


def istasyon(k, x, y, title, subs=(), cont=None, size_sub=None):
    """Ring-numbered station (naming step 3): ring, semibold title, muted sub-lines; returns the bottom y."""
    bl.ring(f"st{k}", gr(x), gr(y), k, container=cont)
    d = vf.IDS[f"st{k}"]["w"]
    T(f"st{k}_t", x + d + 1.0, y + (d - lh(TT)) / 2, [[(title, "sb")]], size=TT, cont=cont)
    yy = y + (d - lh(TT)) / 2 + lh(TT)
    ss = size_sub or S8
    for i, s_ in enumerate(subs):
        T(f"st{k}_s{i}", x + d + 1.0, yy + i * lh(ss), [s_] if isinstance(s_, str) else [s_], size=ss,
          color="muted", cont=cont)
    return yy + len(subs) * lh(ss)


# ------------------------------------------------------------------ 2D data on a card face
class Olcek:
    """Linear map value -> page coordinate."""

    def __init__(self, v0, v1, p0, p1):
        self.v0, self.v1, self.p0, self.p1 = v0, v1, p0, p1

    def __call__(self, v):
        return self.p0 + (v - self.v0) * (self.p1 - self.p0) / (self.v1 - self.v0)


def isaret(pid, x, y, shape="o", fill="ink", edge=None, size=1.6, group=None, role="obstacle"):
    """A data marker centred at (x, y): o circle, s square, D diamond, ^ / v triangles. fill None = open."""
    r = size / 2
    f = vf.C.get(fill, fill) if fill else "FFFFFF"
    e = vf.C.get(edge, edge) if edge else soft(f, 0.35) if fill else vf.C["ink"]
    lw = vf.LW["ince"]
    if shape == "o":
        out = vf.oval(pid, x - r, y - r, size, size, fill=f, line=e, lw=lw, role=role, grid=False)
        if group:
            vf.IDS[pid]["group"] = group
        return out
    if shape == "s":
        r *= 0.88
        pts = [(x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r)]
    elif shape == "D":
        r *= 1.15
        pts = [(x, y - r), (x + r, y), (x, y + r), (x - r, y)]
    elif shape == "^":
        pts = [(x, y - r * 1.1), (x + r * 1.05, y + r * 0.8), (x - r * 1.05, y + r * 0.8)]
    else:
        pts = [(x, y + r * 1.1), (x + r * 1.05, y - r * 0.8), (x - r * 1.05, y - r * 0.8)]
    return vf.poly(pid, pts + [pts[0]], fill=f, line=e, lw=lw, role=role, group=group)


def kot(pid, x0, x1, y, sc, ticks, labels=None, size=None, cont=None, below=True, lw=None, color="frame"):
    """Base line (kot) with small ticks and labels instead of an axis spine."""
    vf.seg(pid, (x0, y), (x1, y), vf.C[color], lw or vf.LW["eksen"])
    size = size or S8
    for i, v in enumerate(ticks):
        x = sc(v)
        vf.seg(f"{pid}_t{i}", (x, y), (x, y + (0.9 if below else -0.9)), vf.C[color], vf.LW["ince"])
        lab = labels[i] if labels else fmt(v, 1)
        if lab is None:                       # an unlabelled tick (labels crowd at this spacing)
            continue
        yy = y + 1.4 if below else y - 1.4 - lh(size)
        T(f"{pid}_l{i}", x, yy, [lab], size=size, align="c", color="muted", cont=cont)


def kot_dikey(pid, x, y0, y1, sc, ticks, labels=None, size=None, cont=None, left=True, color="frame"):
    vf.seg(pid, (x, y0), (x, y1), vf.C[color], vf.LW["eksen"])
    size = size or S8
    for i, v in enumerate(ticks):
        y = sc(v)
        vf.seg(f"{pid}_t{i}", (x, y), (x + (-0.9 if left else 0.9), y), vf.C[color], vf.LW["ince"])
        lab = labels[i] if labels else fmt(v, 1)
        if left:
            T(f"{pid}_l{i}", x - 1.7, y - lh(size) / 2, [lab], size=size, align="r", color="muted", cont=cont)
        else:
            T(f"{pid}_l{i}", x + 1.2, y - lh(size) / 2, [lab], size=size, color="muted", cont=cont)


# ------------------------------------------------------------------ evidence and manifest
def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git_head():
    try:
        return subprocess.run(["git", "-C", _R, "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True).stdout.strip()
    except Exception:
        return None


def ev(etiket_, deger, kaynak, anahtar, hesap="okundu"):
    import re as _re
    m = _re.match(r"^(.*?):(\d+)(.*)$", str(kaynak))
    d = {"etiket": etiket_, "deger": deger, "kaynak": kaynak, "anahtar_yolu": anahtar, "hesap": hesap}
    if m and (ROOT / m.group(1)).is_file():
        d["kaynak"], d["satir"] = m.group(1), int(m.group(2))
        if m.group(3).strip():
            d["not"] = m.group(3).strip()
    return d


SINIFLAR = [   # (path fragment, class statement) for the evidence file's quarantine declaration
    ("results/C1_REFERANS_FOYU.md", "results/C1_REFERANS_FOYU.md (C1 sonrasi referans foyu, tek sayi kaynagi)"),
    ("results/q1/", "results/q1/* (C1 sonrasi dondurulmus B2-B10 ciktilari)"),
    ("results/c1_", "results/c1_* (C1 sizinti duzeltmesi sonrasi yeniden uretilmis kosular; proje CLAUDE.md, 08.09.2026 "
                    "netlestirmesi: gecerli yollar yalniz results/c1_* ve results/q1/*; her deger foy satiriyla denetlenir)"),
    ("results/wrn_eval/", "results/wrn_eval/wrn_eval_summary.json (foy satir 354'un kaynak gosterdigi dosya; degerleri foy "
                          "satir 19 ve 360-364 ile denetlenir)"),
    ("results/q1_research/ONKAYIT_SAPMALAR.md", "results/q1_research/ONKAYIT_SAPMALAR.md (sapma kaydi basliklari, sayi degil)"),
    ("raporlar/konsey_2026-10-29/hucre_tablosu", "raporlar/konsey_2026-10-29/hucre_tablosu*.json (donmus hucre tablolari)"),
    ("raporlar/konsey_2026-10-29/ON_KAYIT", "raporlar/konsey_2026-10-29/ON_KAYIT*.md (kayit metni, tanim satirlari)"),
    ("data/cifar", "data/cifar-10-batches-py ve data/cifar-100-python test dosyalari (yalniz ilk dort goruntu)"),
    ("src/models/", "src/models/*.py (model tanimi satirlari)"),
    ("paper/figures/konsey/", "paper/figures/konsey/*.py (v1 veri kurallari, salt okunur ice aktarim; sayi yazmaz)"),
    ("paper/figures/charts/", "paper/figures/charts/*.py (v1 veri kurallari, salt okunur ice aktarim)"),
    ("paper/figures/visio/", "paper/figures/visio/*.py (v1 icerik kurallari, salt okunur ice aktarim)"),
    ("paper/manuscript/sections/", "paper/manuscript/sections/*.tex (tanim cumleleri; govde metni degismez)"),
    ("paper/manuscript/macros_konsey.tex", "paper/manuscript/macros_konsey.tex (gosterim makrolari)"),
]
YASAK = ("run1", "run2", "run3", "attention_analysis_run3", "stat_addendum", "rev2_blockA")


def _rel(f):
    f = str(f).replace("\\", "/")
    for pre in (_R + "/", _R.replace("//wsl.localhost/Ubuntu-22.04", "") + "/"):
        if f.startswith(pre):
            return f[len(pre):]
    i = f.find("/adeb_sci_1/")
    return f[i + len("/adeb_sci_1/"):] if i >= 0 else f


def kanit_yaz(stem, degerler, ek=None, okunan_ek=()):
    p = write_kanit(stem, _O, uslup_no="Z", degerler=degerler, records=None)
    k = json.loads(Path(p).read_text(encoding="utf-8"))
    k["betik"] = f"paper/figures_v2/{Path(sys.argv[0]).name}"
    k["git_head"] = git_head()
    files = {str(d.get("kaynak")) for d in k.get("degerler", []) if d.get("kaynak")}
    files |= {str(x) for x in okunan_ek if isinstance(x, str)}
    # the v1 rule modules this process imported (read-only), so the declaration lists them too
    for mod in list(sys.modules.values()):
        fp = getattr(mod, "__file__", None) or ""
        fp = fp.replace("\\", "/")
        if "/paper/figures/" in fp and "/paper/figures_v2/" not in fp and fp.endswith(".py"):
            files.add(fp)
    files = {_rel(f) for f in files if f and f != "None"}
    k["okunan_dosyalar"] = sorted(files)
    k["karantina_denetimi"] = {f: not any(b in f for b in YASAK) for f in k["okunan_dosyalar"]}
    if not all(k["karantina_denetimi"].values()):
        raise SystemExit("KARANTINA: a quarantined file was read: " + str(k["karantina_denetimi"]))
    sinif = sorted({lab for f in files for frag, lab in SINIFLAR if frag in f})
    bilinmeyen = sorted(f for f in files if not any(frag in f for frag, _ in SINIFLAR))
    k["karantina"] = ("bu sekil icin okunan dosya siniflari: " + "; ".join(sinif)
                      + (("; siniflandirilmamis: " + ", ".join(bilinmeyen)) if bilinmeyen else "")
                      + ". run1, run2, run3, attention_analysis_run3, stat_addendum, rev2_blockA ve C1 oncesi hicbir "
                        "dosya okunmadi (karantina_denetimi alani dosya dosya).")
    k["okunan_siniflar"] = sinif
    if ek:
        k.update(_jsonable(ek))
    try:
        man = json.loads(Path(vf.STEM + ".fig.json").read_text(encoding="utf-8"))
        if (man.get("denge_muafiyet") or {}).get("3b_veri"):
            k["k7_muafiyet"] = {"gerekce": man["denge_muafiyet"]["3b_veri"], "ikiz_kodlama": man.get("ikiz_kodlama"),
                                "kural": "uslup_Z.yaml three_d.veri_ikiz_kodlama (surum 3, K7, 08.11.2026); denge "
                                         "kapisi 3b_veri maddesini yalniz bu kosulla muaf sayar"}
    except Exception:
        pass
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(k, indent=2, ensure_ascii=False, default=str) + "\n")
    return p


def manifest_ek(**fields):
    p = Path(vf.STEM + ".fig.json")
    m = json.loads(p.read_text(encoding="utf-8"))
    m.update(fields)
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(m, indent=2, ensure_ascii=False, default=str) + "\n")


def denge_ajan(stem, gercek, ozel=None, veri=False):
    y = {
        "3b_veri": (False, "no measured value is encoded by height, depth or angle; 3D carries objects and design structure"),
        "3b_kural_disi": (False, "one dimetric 36 degree view from style Z, flat face tones, no perspective, gradient, gloss "
                                 "or soft mask; the cast shadow is a floor projection larger than the object, not an "
                                 "offset copy; text stays in the plane or on a card face parallel to the page"),
        "clip_art": (False, "every object is built from Visio polygons and stands for a study object"),
        "gokkusagi_renk_haritasi": (False, "no colour map; one low-chroma sequential ramp at most"),
        "sus_arka_plan": (False, "the stage plate and the cards are the grouping tools of style Z and carry the content"),
        "gereksiz_ikon": (False, "there are no icons; each drawn part is a study object or a data mark"),
        "dogrudan_etiket": (True, "every part is labelled beside it in the plane"),
        "gercek_goruntu": ("uygulanmaz", "the figure shows no photograph or test image"),
        "panel_basina_bir_iddia": (True, "each named part states one claim"),
        "her_sayinin_kaynagi": (True, "every printed number is in the evidence file with its source file and key"),
    }
    if not SAHNE:
        y.update({
            "3b_veri": (False, "no 3D is drawn; every value is a 2D position, length or colour on a flat card"),
            "3b_kural_disi": (False, "flat-card figure: no projection, no thickness, no shadow, no gradient or gloss"),
            "sus_arka_plan": (False, "white page; the flat cards of style Z are the grouping tools and carry the content"),
        })
    y.update(ozel or {})
    p = OUT / f"{stem}.denge_ajan.json"
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"stem": stem, "gercek_goruntu_sayisi": gercek,
                   "yanitlar": {k: {"deger": d, "gerekce": g} for k, (d, g) in y.items()}}, fh, indent=2,
                  ensure_ascii=False)
    return p


def _ys(p):
    k = p.get("kind")
    if k in ("poly", "spline"):
        return [pt[1] for pt in p["pts"]]
    if k == "seg":
        return [p["p1"][1], p["p2"][1]]
    return [p["y"], p["y"] + p.get("h", 0)]


def _shift_pt(v, dy):
    if isinstance(v, (list, tuple)) and len(v) == 2 and all(isinstance(a, (int, float)) for a in v):
        return type(v)((v[0], v[1] + dy))
    if isinstance(v, (list, tuple)):
        return type(v)(_shift_pt(a, dy) for a in v)
    if isinstance(v, dict):
        return {k: _shift_pt(a, dy) for k, a in v.items()}
    return v


def sayfa_sigdir(pad=0.75, top=0.75):
    """Move the content up so it starts ``top`` mm under the page edge (on the grid) and fit the page
    height to it (QC A5, no dead band)."""
    y0 = min(min(_ys(p)) for p in vf.SCENE)
    dy = -gf(y0 - top)
    if abs(dy) > 1e-9:
        for p in vf.SCENE:
            k = p.get("kind")
            if k in ("poly", "spline"):
                p["pts"] = [(a, b + dy) for a, b in p["pts"]]
            elif k == "seg":
                p["p1"] = (p["p1"][0], p["p1"][1] + dy)
                p["p2"] = (p["p2"][0], p["p2"][1] + dy)
            if "y" in p:
                p["y"] = p["y"] + dy
        for rec in vf.THREE_D.values():
            b = rec.get("bbox_mm")
            if b:
                rec["bbox_mm"] = [b[0], round(b[1] + dy, 4), b[2], b[3]]
            if "corners" in rec:
                rec["corners"] = _shift_pt(rec["corners"], dy)
    y1 = max(max(_ys(p)) for p in vf.SCENE)
    vf.PAGE_H = vf.snap_page(y1 + pad)
    return vf.PAGE_H


def bitir(stem, *, message, kind, panels, caption, sablon, tur, degerler, kanit_ek=None, manifest=None,
          denge=None, gercek=0, n_exempt_reason=None, okunan_ek=()):
    """Quick look (--bak), engine run, manifest, evidence and balance answers. Returns an exit code."""
    if BAK:
        onizle(str(OUT / f"{stem}_bak.png"))
        print("quick look written")
        return 0
    rep = vf.run()
    print("verdict", rep["verdict"], "max_dev", (rep.get("readback") or {}).get("max_deviation_mm"))
    if rep["verdict"] == "PREFLIGHT-ONLY":
        for i in (rep.get("preflight") or {}).get("issues", [])[:30]:
            print("  ", i)
        return 0
    if rep["verdict"] != "PASS":
        for i in (rep.get("preflight") or {}).get("issues", [])[:30]:
            print("  ", i)
        return 1
    vf.write_fig_manifest(message, kind=kind, panels=panels, n_exempt_reason=n_exempt_reason)
    m = dict(sablon=sablon, tur=tur, uslup_yolu="<skill>/styles/uslup_Z.yaml", altyazi_taslagi=caption,
             uslup_surumu=3, sahne=SAHNE,
             kompozisyon_dili="sahne (dimetrik maket)" if SAHNE else
             "duz kart (ucuncu tur 09.11.2026: kaide, levha, vitrin, direk, raf ve zemin yok)")
    m.update(manifest or {})
    manifest_ek(**m)
    kanit_yaz(stem, degerler, ek=dict(kanit_ek or {}, altyazi_taslagi=caption), okunan_ek=okunan_ek)
    denge_ajan(stem, gercek, denge)
    return 0


# ------------------------------------------------------------------ quick look (no Visio)
def onizle(path, dpi=200):
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
            ax.add_patch(Polygon(p["pts"], closed=True, fc=col(p["fill"]), ec=col(p["line"]), lw=(p["lw"] or 0.3) * 0.6))
        elif k == "rect":
            ax.add_patch(Rectangle((p["x"], p["y"]), p["w"], p["h"], fc=col(p["fill"]), ec=col(p["line"]),
                                   lw=(p["lw"] or 0.3) * 0.6))
        elif k == "oval":
            ax.add_patch(Ellipse((p["x"] + p["w"] / 2, p["y"] + p["h"] / 2), p["w"], p["h"], fc=col(p["fill"]),
                                 ec=col(p["line"]), lw=(p["lw"] or 0.3) * 0.6))
        elif k == "seg":
            ax.plot([p["p1"][0], p["p2"][0]], [p["p1"][1], p["p2"][1]], color=col(p["color"]), lw=p["lw"] * 0.6,
                    ls="--" if p.get("dash") else "-")
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


def profil_kart(S, pid, X, Y, Z, dx, heights, tint, t=1.4, *, edge_hex=None, group=None, shadow=True,
                k=(0.16, 0.11)):
    """A cut-out card: an upright card (face in the page-parallel vertical plane, as in kart()) whose top edge
    is the polyline through (dx[i], heights[i]) in page mm from the card's foot point; the face is therefore a
    flat 2D profile chart printed at true size. Returns (foot page point, top page points)."""
    if not SAHNE:
        raise SystemExit("profil_kart is a stage part; a flat-card figure draws its profile as a 2D line chart")
    p0 = S.P(X, Y, Z)
    top = [(p0[0] + a, p0[1] - h) for a, h in zip(dx, heights)]
    nvx = S.n[0] * t
    nvy = S.n[1] * t
    nv = (nvx * S.ax["w"][0] + nvy * S.ax["d"][0], nvx * S.ax["w"][1] + nvy * S.ax["d"][1])
    gid = group or pid
    tones = bl.face_tones(tint)
    edge = soft(tones["tones"]["front"])
    if shadow:
        pts = []
        for a, h in zip(dx, heights):
            Xa, Ya = S.W(p0[0] + a, p0[1], Z)
            pts += [(Xa, Ya), (Xa - k[0] * h, Ya - k[1] * h)]
        hull = _hull([S.P(x_, y_, Z) for x_, y_ in pts])
        vf.poly(f"{pid}_g", hull + [hull[0]], fill=vf.tint_of("golge")[0], line=None, role="deco", group=gid,
                ctype="golge")
    xr = p0[0] + dx[-1]
    right = [(xr, p0[1]), (xr + nv[0], p0[1] + nv[1]), (xr + nv[0], top[-1][1] + nv[1]), top[-1]]
    vf.poly(f"{pid}_r", right + [right[0]], fill=tones["tones"]["front"], line=edge, lw=vf.LW["ince"], role="deco",
            group=gid, ctype="iso")
    for i in range(len(top) - 1):
        a, b = top[i], top[i + 1]
        sl = [a, b, (b[0] + nv[0], b[1] + nv[1]), (a[0] + nv[0], a[1] + nv[1])]
        vf.poly(f"{pid}_s{i}", sl + [sl[0]], fill=tones["tones"]["right"], line=edge, lw=vf.LW["ince"],
                role="deco", group=gid, ctype="iso")
    face = [(p0[0] + dx[0], p0[1])] + top + [(xr, p0[1])]
    vf.poly(f"{pid}_face", face + [face[0]], fill=tones["tones"]["top"], line=edge, lw=vf.LW["ince"], role="deco",
            group=gid, ctype="plate")
    for i in range(len(top) - 1):
        vf.seg(f"{pid}_e{i}", top[i], top[i + 1], vf.C.get(edge_hex, edge_hex) if edge_hex else tones["tones"]["front"],
               vf.LW["vurgu"])
    _record(pid, "profil_kart", tint, {"w": dx[-1] - dx[0], "d": t, "h": max(heights)}, tones,
            {"front": f"{pid}_face", "right": f"{pid}_r"}, face + right,
            {"world_mm": [X, Y, Z], "rol": "veri",
             "not": "face in the page-parallel vertical plane; the top edge is a flat 2D profile at true size"})
    return p0, top


def plaka_un(S, pid, X, Y, L, D, t, tint="sahne", z=0.0, lw=None):
    """A stage plate aligned with the cards: its front edge runs along the page-horizontal floor direction u
    (L page mm long), its depth along the floor normal n (D world mm). The front face prints as a true page
    rectangle t mm high; the top face is the parallelogram the cards stand on. Returns the top-face corners.
    Not drawn in flat mode (the corners are still returned)."""
    a = L / S.u_page
    ux, uy = S.u[0] * a, S.u[1] * a
    nx, ny = S.n[0] * D, S.n[1] * D
    A, B, C, Dd = (X, Y), (X + ux, Y + uy), (X + ux + nx, Y + uy + ny), (X + nx, Y + ny)
    if not SAHNE:
        return [S.P(*p, z) for p in (A, B, C, Dd)]
    tones = bl.face_tones(tint)
    edge = vf.tint_of(tint)[1]
    top = [S.P(*p, z) for p in (A, B, C, Dd)]
    front = [S.P(*A, z - t), S.P(*B, z - t), S.P(*B, z), S.P(*A, z)]
    right = [S.P(*B, z - t), S.P(*C, z - t), S.P(*C, z), S.P(*B, z)]
    for f, pts, ct in (("front", front, "iso"), ("right", right, "iso"), ("top", top, "plate")):
        vf.poly(f"{pid}_{f}", pts + [pts[0]], fill=tones["tones"][f], line=edge, lw=lw or vf.LW["ince"], role="deco",
                group=pid, ctype=ct)
    _record(pid, "plaka", tint, {"w": L, "d": D, "h": t}, tones,
            {"front": f"{pid}_front", "right": f"{pid}_right", "top": f"{pid}_top"}, top + front + right,
            {"not": "plate aligned with the page-horizontal floor direction u and the floor normal n"})
    return top


def un(S, xpage_off, depth):
    """World floor point at page offset xpage_off along u from the origin and depth mm along n."""
    a = xpage_off / S.u_page
    return S.u[0] * a + S.n[0] * depth, S.u[1] * a + S.n[1] * depth


def _jsonable(v):
    """JSON-safe copy: tuple keys joined with ' | ', other keys as strings."""
    if isinstance(v, dict):
        out = {}
        for k, x in v.items():
            if isinstance(k, tuple):
                k = " | ".join(map(str, k))
            elif not isinstance(k, (str, int, float, bool)) and k is not None:
                k = str(k)
            out[k] = _jsonable(x)
        return out
    if isinstance(v, (list, tuple)):
        return [_jsonable(x) for x in v]
    return v


def yukle_sema(path, name):
    """Import a v1 Visio schematic script read-only: its module-level O.baslat() (which would load style 8
    and its palette into the engine) is replaced by a no-op that keeps style Z; nothing is drawn."""
    vis = _R + "/paper/figures/visio"
    if vis not in sys.path:
        sys.path.append(vis)
    import _sema_ortak as SO
    SO.baslat = lambda: U
    SO.U = U
    return yukle(path, name)


DV_GLYPHS = {"⟨", "⟩", "∈", "→", "⊇", "∞"}


def runs(s, key="r"):
    """Runs of one line: a character followed by a combining macron (U+0304) and glyphs Open Sans lacks go
    to the DejaVu Sans fallback; the rest stays in the style's face."""
    out, cur, i = [], "", 0
    while i < len(s):
        ch = s[i]
        if i + 1 < len(s) and s[i + 1] == "̄":
            if cur:
                out.append((cur, key))
                cur = ""
            out.append((ch + "̄", key + "@DejaVuSans"))
            i += 2
            continue
        if ch in DV_GLYPHS:
            if cur:
                out.append((cur, key))
                cur = ""
            out.append((ch, key + "@DejaVuSans"))
        else:
            cur += ch
        i += 1
    if cur:
        out.append((cur, key))
    return out


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
