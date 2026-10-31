#!/usr/bin/env python
"""Decomposition schematic (fig:decomposition_schematic), style 8, Visio, one column, naming step 2.

    python paper/figures/visio/fig_decomposition_schematic.py --uslup 8 [--check]

Binding plan: raporlar/visio_2026-10-31/04_cizim_plani.md section 9.3. One column, read top to
bottom: the 2 x 2 transfer matrix (a 3D plate, iso_slab, white-box rates w on the diagonal) with the
definitions of the symmetric similarity and the directional residual; the exact split per ordered
pair; the panel means sigma and rho; the panel source gap. Stages are joined by labelled chevrons,
the (a)-(d) letters of the council draft are gone. Similarity terms are green (#009E73, sym) and
direction terms orange (#E69F00, dir); every coloured term also carries its name, so tone is never
the only channel. Target 90 mm, ceiling 95 mm (template yontem_semasi, vertical).

The figure draws no result number; the only numeral is the 1/2 of the definitions. The two identities
it states are re-checked on seeded random positive matrices with the council script's own check
(paper/figures/konsey/fig_decomposition_schematic.py identity_check, seed 20261031); a residual over
1e-12 stops the figure.

Notation: function notation T(i, j), w(j), tau-bar(i, j), r(i, j) replaces subscripts, because the
figure font has no subscript c, R, V or P; <.> is the mean over the members c of the fixed CNN panel P.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _sema_ortak as O  # noqa: E402
from _sema_ortak import vf, bl, gr, gc, gf, lh, tw, T, kutu, yuz_tonlari  # noqa: E402
from _yuz_tonlari import notr_kenar  # noqa: E402

O.baslat()
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("konsey_decomposition", "paper/figures/konsey/fig_decomposition_schematic.py")
KD = importlib.util.module_from_spec(_spec)      # the council script (same file name as this one), identity_check only
_spec.loader.exec_module(KD)

STEM = "decomposition_schematic"
KIND = "single"
STEP = 2
HEDEF, TAVAN = 90.0, 95.0
SEED = 20261031
S = vf.SMALL
LHS = lh(S)
W = vf.page_width(KIND)
XR = gf(W - 0.5)
TB = "̄"                     # combining macron: tau-bar
TAU = "τ" + TB
GAP = 5.0                         # stage to stage: a chevron and its label beside it
SYM, DIR, INK = "sym", "dir", "ink"


def term_row(pid, y, items, cont, x0, x1):
    """One row of terms centred between x0 and x1; a term with a name gets an under-bracket in its
    colour and its name under it. Returns the row's height."""
    slots = []
    for txt, col, name in items:
        wt = tw([txt], S)
        wn = tw([[(name, "sb")]], S) if name else 0.0
        slots.append((txt, col, name, wt, wn, max(wt, wn)))
    gap = 1.5
    total = sum(s[5] for s in slots) + gap * (len(slots) - 1)
    if total > x1 - x0 + 1e-6:
        raise SystemExit(f"{pid}: the terms need {total:.2f} mm, the stage has {x1 - x0:.2f} mm")
    x = gr(x0 + (x1 - x0 - total) / 2)
    named = any(s[2] for s in slots)
    for i, (txt, col, name, wt, wn, ws) in enumerate(slots):
        cx = x + ws / 2
        T(f"{pid}_t{i}", cx - wt / 2, y, [txt], size=S, color=col, cont=cont, w=wt)
        if name:
            O.kosebent(f"{pid}_k{i}", gr(cx - wt / 2) + 0.25, gr(cx - wt / 2) + wt - 0.25, y + LHS + 0.25,
                       vf.C[col] if col in vf.C else col, depth=0.75)
            T(f"{pid}_n{i}", cx - wn / 2, y + LHS + 1.5, [[(name, "sb")]], size=S, color=col, cont=cont, w=wn)
        x = gc(x + ws + gap)
    return LHS + (1.5 + LHS if named else 0.0)


def lay():
    vf.reset(STEM, W, 120.0, naming_step=STEP, naming_kind="akis")
    x0, x1 = 0.5, XR
    pw = x1 - x0
    # ---------------- stage 1: the transfer matrix as a 3D plate, diagonal = w
    p1 = O.panel_bos("p1", x0, 0.5, pw, 10)
    rh_w = tw(["V"], S)
    px = x0 + 2.5 + rh_w + 1.0
    py = 0.5 + 2.0 + LHS
    with yuz_tonlari("panel") as tint:
        rec = notr_kenar(bl.iso_slab("mat", gr(px), gr(py), 15.0, 3.0, 15.0, tint, container="p1"))
    fr = vf.IDS[rec["faces"]["front"]]["pts"][:4]
    xl, xr_ = fr[0][0], fr[1][0]
    yb, yt = fr[0][1], fr[3][1]
    cw, ch = (xr_ - xl) / 2, (yb - yt) / 2
    # the off-diagonal cells (transfer rates T) are white tiles; the diagonal (white-box rates w)
    # keeps the plate's front tone, as the council draft shaded it
    for i in range(2):
        cx0, cy0 = xl + (1 - i) * cw, yt + i * ch
        vf.poly(f"mat_t{i}", [(cx0, cy0), (cx0 + cw, cy0), (cx0 + cw, cy0 + ch), (cx0, cy0 + ch), (cx0, cy0)],
                fill="FFFFFF", line=vf.C["muted"], lw=vf.USLUP.line_min_pt, role="mark", group="mat")
    vf.seg("mat_gv", (xl + cw, yt), (xl + cw, yb), vf.C["muted"], vf.USLUP.line_min_pt)
    vf.seg("mat_gh", (xl, yt + ch), (xr_, yt + ch), vf.C["muted"], vf.USLUP.line_min_pt)
    for i, m in enumerate(("R", "V")):
        T(f"col{i}", xl + i * cw + cw / 2 - rh_w / 2, py - LHS - 0.25, [m], size=S, cont="p1", w=rh_w, align="c")
        T(f"row{i}", x0 + 2.5, yt + i * ch + ch / 2 - LHS / 2, [m], size=S, cont="p1", w=rh_w, align="c")
    bx, by, bw_, bh_ = rec["bbox_mm"]
    lx = gc(bx + bw_ + 3.0)
    lab_t = [[("T", "i"), (": transfer rate", "r")]]
    lab_w = [[("w", "i"), (": white-box rate", "r")]]
    yr0 = gr(yt + ch / 2 - LHS / 2)
    yr1 = gr(yt + 1.5 * ch - LHS / 2)
    T("lt", lx, yr0, lab_t, size=S, cont="p1")
    T("lw", lx, yr1, lab_w, size=S, cont="p1")
    vf.seg("lt_lead", (lx - 0.3, yr0 + LHS / 2), (xl + 1.5 * cw, yr0 + LHS / 2), vf.C["muted"], vf.USLUP.line_min_pt)
    vf.seg("lw_lead", (lx - 0.3, yr1 + LHS / 2), (xl + 1.5 * cw, yr1 + LHS / 2), vf.C["muted"], vf.USLUP.line_min_pt)
    T("axes", lx, py - LHS - 0.25, [[("i", "i"), (" source, ", "r"), ("j", "i"), (" target", "r")]],
      size=S, color="muted", cont="p1")
    dy = gc(max(by + bh_, yr1 + LHS) + 1.25)
    defs = [(SYM, "similarity", f"log {TAU}(i, j) = ½ log[T(i, j) T(j, i) / w(i) w(j)]"),
            (DIR, "direction", "r(i, j) = log[T(i, j) w(i) / T(j, i) w(j)]")]
    namew = max(tw([[(n, "sb")]], S) for _, n, _ in defs)
    for i, (col, name, f) in enumerate(defs):
        T(f"def{i}_n", x0 + 2.5, dy + i * LHS, [[(name, "sb")]], size=S, color=col, cont="p1", w=namew)
        need = tw([f], S)
        room = x1 - 2.5 - (x0 + 2.5 + namew + 1.5)
        if need > room:
            raise SystemExit(f"definition {name} needs {need:.2f} mm, room {room:.2f} mm")
        T(f"def{i}_f", x0 + 2.5 + namew + 1.5, dy + i * LHS, [f], size=S, color=col, cont="p1")
    p1["h"] = gc(dy + 2 * LHS + 1.5 - 0.5)
    # ---------------- stage 2: the exact split
    y2 = p1["y"] + p1["h"] + GAP
    p2 = O.panel_bos("p2", x0, y2, pw, 10)
    T("sp_lead", x0 + 2.5, y2 + 1.5, ["log T(i, j) ="], size=S, cont="p2")
    h = term_row("sp", y2 + 1.5 + LHS, [("log w(j)", INK, "vulnerability"), ("+", INK, None),
                                        (f"log {TAU}(i, j)", SYM, "similarity"), ("+", INK, None),
                                        ("½ r(i, j)", DIR, "direction")], "p2", x0 + 2.0, x1 - 2.0)
    p2["h"] = gc(LHS + h + 2.75)
    # ---------------- stage 3: panel means
    y3 = p2["y"] + p2["h"] + GAP
    p3 = O.panel_bos("p3", x0, y3, pw, 10)
    h = term_row("pm", y3 + 1.5, [(f"σ(m) = ⟨log {TAU}(m, c)⟩", SYM, "panel similarity"),
                                  ("ρ(m) = ⟨r(c, m)⟩", DIR, "direction")], "p3", x0 + 2.0, x1 - 2.0)
    note = [[("⟨·⟩: mean over panel members ", "r"), ("c", "i"), (" ∈ ", "r"), ("P", "i")]]
    T("pm_note", x0 + 2.5, y3 + 1.5 + h + 0.75, note, size=S, color="muted", cont="p3")
    p3["h"] = gc(1.5 + h + 0.75 + LHS + 1.5)
    # ---------------- stage 4: the panel source gap
    y4 = p3["y"] + p3["h"] + GAP
    p4 = O.panel_bos("p4", x0, y4, pw, 10)
    h = term_row("sg", y4 + 1.5, [("G", INK, "source gap"), ("=", INK, None), ("[σ(R) − σ(V)]", SYM, "symmetric part"),
                                  ("− ½[ρ(R) − ρ(V)]", DIR, "directional part")], "p4", x0 + 2.0, x1 - 2.0)
    p4["h"] = gc(h + 2.75)
    # Karar: labelled thin arrows (the style's ok rule) join the stages. The plan asked for chevrons;
    # the balance gate (motor/host/denge.py, akis_etiketi) found no labelled flow with the open-stroke
    # chevrons of style 8, and bl.flow set a vertical chevron's label across its stroke.
    for fid, a, b, lab in (("f12", "p1", "p2", "per pair (i, j)"), ("f23", "p2", "p3", "panel mean"),
                           ("f34", "p3", "p4", "R minus V")):
        bl.flow(fid, a, b, label=lab, kind="arrow")
    return gc(y4 + p4["h"] + 0.75)


def main():
    wid, wgap = KD.identity_check(SEED)
    if max(wid, wgap) > 1e-12:
        raise SystemExit(f"identity check failed: {wid}, {wgap}")
    O.NOTES.append("No number from any result file is drawn; the only numeral is the 1/2 of the definitions.")
    O.NOTES.append("<.> is the mean over the members c of the fixed CNN panel P (for a panel member, P without "
                   "itself), as in the council script's note.")
    h = lay()
    v = O.bitir(h, "The exact split: a transfer rate is vulnerability times symmetric similarity times a "
                   "directional factor, and the panel source gap is a symmetric part plus a directional part.",
                KIND, 4, n_exempt="the schematic draws symbols and definitions only", sablon="yontem_semasi",
                hedef=HEDEF, tavan=TAVAN, extra={"surec_zinciri": True})
    if v != "PASS":
        print("layout:", v)
        return 0
    src = "paper/figures/konsey/fig_decomposition_schematic.py"
    deg = [O.ev("identity log T(i,j) = log w(j) + log tau-bar(i,j) + r(i,j)/2, max abs residual", wid, src,
                f"identity_check(seed={SEED}, trials=200)[0]",
                "200 seeded random positive 7-model matrices, off-diagonal residual; not drawn"),
           O.ev("gap G = (sigma_R - sigma_V) - (rho_R - rho_V)/2, max abs residual", wgap, src,
                f"identity_check(seed={SEED}, trials=200)[1]", "same matrices, panel of 5; not drawn"),
           O.ev("the constant 1/2 of the definitions", 0.5, "paper/figures/konsey/fig_decomposition_schematic.kanit.json",
                "cizilen_degerler.veri", "definition (brief 12 section 6.2), the only numeral drawn")]
    foy = {"karsilastirma_sayisi": 2, "uyusmayan": 0, "sonuc": "TAMAM",
           "ayrinti": [{"ad": "identity residual", "deger": wid, "esik": 1e-12, "eslesti": wid <= 1e-12},
                       {"ad": "gap residual", "deger": wgap, "esik": 1e-12, "eslesti": wgap <= 1e-12}],
           "not": "the figure draws no number from the reference sheet; the checks are internal identities"}
    O.kanit_yaz(STEM, deg, foy=foy, okunan={src: "identity_check (function)"},
                ek={"rastgele_denetim_tohumu": SEED, "gosterim": "function notation, see the module docstring"})
    O.denge_ajan(STEM, 0, {"3b_veri": (False, "the only 3D object is the two by two matrix plate, no data value"),
                           "gereksiz_ikon": (False, "the brackets tie each term to its name, no icon is drawn"),
                           "dogrudan_etiket": (True, "every term carries its name under a bracket in its colour"),
                           "panel_basina_bir_iddia": (True, "each stage states one step of the split"),
                           "her_sayinin_kaynagi": (True, "no data number is drawn; the identities are re-checked")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
