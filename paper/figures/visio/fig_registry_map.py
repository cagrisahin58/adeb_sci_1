#!/usr/bin/env python
"""Registry map (fig:registry_map, Y4), style 8, Visio, full width (double), naming step 4 (strip).

    python paper/figures/visio/fig_registry_map.py --uslup 8 [--check]

Binding plan: raporlar/visio_2026-10-31/04_cizim_plani.md section 9.5 (replaces Table 3; target 90 mm,
ceiling 95 mm; template tablodan_sekle). Four column panels under one title baseline (title strip):
family, test and quantity, the pre-registered values on a number line (predicted size as a filled diamond,
falsification threshold as an open circle, the +-delta equivalence band as a grey bar, the value printed
beside the line), and the falsification rule. Seven family groups are separated by rules: CIFAR-10 panel
(F_B2), 2 x 2 design (F_B4), attack side (B5), masking check (B6), CIFAR-100 replication (F_B9), gradient
Mantel (F_B10), ImageNetV2 (B8, descriptive). Measured outcomes are NOT drawn (plan: the registry should
not repeat the results of Tables 7 and 9 and Figure 8).

Every threshold comes from results/q1/konsey_kayit_kurallari.json (key paths in the evidence file) and is
compared with the reference sheet section M13.2 (tables a-c); one mismatch stops the figure. The number
line's ticks (0, 0.4, 0.8) are an axis, not data; one axis carries quantities in log units, ratios and
Spearman correlations, so each row names its quantity and the values are printed.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _sema_ortak as O  # noqa: E402
from _sema_ortak import vf, bl, gr, gc, gf, lh, tw, T, TW  # noqa: E402

O.baslat()
K = O.K
STEM = "registry_map"
KIND = "double"
STEP = 4
HEDEF, TAVAN = 90.0, 95.0
S = vf.SMALL
LHS = lh(S)
W = vf.page_width(KIND)
XR = gf(W - 0.5)
SRC = "results/q1/konsey_kayit_kurallari.json"
D = K.load_json(SRC)
SIN = {(s["kimlik"], s["blok"]): (i, s) for i, s in enumerate(D["sinamalar"])}
FOY = K.Foy()
OKUNAN = {}
LO, HI = -0.3, 0.9
MAC = "̄"                 # combining macron: tau-bar and A-bar, as macros_konsey.tex \simt, \AbarIN
# Notation of paper/manuscript/macros_konsey.tex without sub- and superscript positions: the engine has no
# script position and a Visio subscript would print under the 8 pt floor, so the script letters follow the
# symbol on the line (Dseed -> "Δseed", Asig{scr} -> "Aσscr", Isig -> "Iσ", Arho -> "Aρ").


def val(path):
    v = K.dig(D, path)
    OKUNAN[path] = v
    return v


def sp(kimlik, blok, rest):
    i, _ = SIN[(kimlik, blok)]
    return val(f"sinamalar.{i}.{rest}")


def kural_esik(kimlik, blok, key):
    """A threshold inside sinamalar[].kurallar_sirasiyla (the B10 falsification thresholds)."""
    i, s = SIN[(kimlik, blok)]
    for j, r in enumerate(s["kurallar_sirasiyla"]):
        if key in r:
            return val(f"sinamalar.{i}.kurallar_sirasiyla.{j}.{key}.deger")
    raise SystemExit(f"{kimlik}/{blok}: no {key} in kurallar_sirasiyla")


def f(v):
    s = f"{v:g}"
    return s.replace("-", "−")


DELTA = val("sabitler.DELTA.deger")
ALFA = val("sabitler.ALFA.deger")


def rows():
    fam = lambda a: val(f"aileler.{a}.aile_buyuklugu_json")  # noqa: E731
    d = f(DELTA)
    R = []
    # (family, family note, test, quantity, pred (op, value) | None, band?, fals value | None, values text, rule)
    ka = sp("K-a", "B2", "ongorulen_buyukluk.deger")
    kaf = sp("K-a", "B2", "curutme.esik.deger")
    R.append(("CIFAR-10 panel", f"Holm, {fam('F_B2')} tests", "K-a", "σ share of the gap, q", ("≥", ka), False,
              kaf, f"≥ {f(ka)}", f"90% CI top < {f(kaf)}"))
    R.append(("", "", "K-b", "ρ(V-scr), log", None, True, None, f"±{d}", f"95% CI excludes 0, |mean| > {d}"))
    kc = sp("K-c", "B2", "ongorulen_buyukluk.deger")
    R.append(("", "", "K-c", "Δseed, family vs panel", ("≥", kc), False, DELTA, f"≥ {f(kc)}", f"90% CI top < {d}"))
    h1 = sp("H1", "B4", "ongorulen_buyukluk.deger")
    R.append(("2 × 2 design", f"Holm, {fam('F_B4')} tests", "H1", "Aσscr, ViT − ResNet", ("≤", h1), True,
              None, f"≤ {f(h1)}", f"90% CI inside ±{d} †"))
    h2 = sp("H2", "B4", "ongorulen_buyukluk.deger")
    R.append(("", "", "H2", "Iσ, init. × architecture", ("≥", h2), True, None, f"≥ {f(h2)}",
              f"90% CI inside ±{d} †"))
    R.append(("", "", "H3", "Aρ, architecture on ρ", None, True, None, f"±{d}",
              f"95% CI excludes 0, |est.| > {d}"))
    b5 = sp("B5", "B5", "esik.deger")
    R.append(("attack side", "one test, no Holm", "B5", "retention, best / PGD", ("≥", b5), False, b5,
              f"≥ {f(b5)}", f"90% CI top < {f(b5)}"))
    b6 = sp("B6", "B6", "esik.deger")
    R.append(("masking check", "decision rule", "B6", "PGD-10 − AA, points", None, False, None,
              f"> {f(b6)} pt", "flagged models out, H1–H3 rerun"))
    R.append(("CIFAR-100", f"Holm, {fam('F_B9')} tests", "K-a–c", "as the CIFAR-10 panel", None, False, None, "",
              "same rules"))
    h10 = sp("H10-cifar10", "B10", "ongorulen_buyukluk.deger")
    e10 = kural_esik("H10-cifar10", "B10", "esik")
    p10 = kural_esik("H10-cifar10", "B10", "p_esigi")
    R.append(("gradient", f"Holm, {fam('F_B10')} tests", "H10", "Spearman(c, log τ" + MAC + ")", ("≥", h10), False, e10,
              f"{f(h10)}", f"est. ≤ {f(e10)} and p ≥ {f(p10)}"))
    h10k = sp("H10k-cifar10", "B10", "ongorulen_buyukluk.deger")
    R.append(("", "", "H10k", "same, model effects out", ("≥", h10k), False, e10, f"{f(h10k)}",
              f"est. ≤ {f(e10)} and p ≥ {f(p10)}"))
    b8 = sp("B8-A_sigma_IN", "B8", "beklenti_esigi.deger")
    R.append(("ImageNetV2", "descriptive", "B8", "A" + MAC + "σIN, mean of the IN pairs", ("≤", b8), True, None, f"≤ {f(b8)}",
              "no decision"))
    b8l = sp("B8-A_sigma_scr_Liu", "B8", "beklenti_esigi.deger")
    R.append(("", "", "B8", "Aσscr,Liu, Liu scratch pair", ("≤", b8l), True, None, f"≤ {f(b8l)}", "no decision"))
    # the B10 family repeats H10/H10k on three data sets: the same thresholds must hold for all six
    for ds in ("cifar10", "cifar100", "imagenetv2"):
        if sp(f"H10-{ds}", "B10", "ongorulen_buyukluk.deger") != h10 or \
                sp(f"H10k-{ds}", "B10", "ongorulen_buyukluk.deger") != h10k:
            raise SystemExit(f"B10 thresholds differ on {ds}; one row per test would be needed")
    return R


def foy_checks():
    a, b = O.foy_bolum(FOY, "### M13.2")
    for name, v in (("DELTA", DELTA), ("ALFA", ALFA), ("B5_ESIK", val("sabitler.B5_ESIK.deger")),
                    ("B6_ESIK_PUAN", val("sabitler.B6_ESIK_PUAN.deger"))):
        n = O.foy_satiri_bul(FOY, a, b, f"| {name} |")
        FOY.metin(f"M13.2(a) {name}", f"| {f(v).replace('−', '-')} |", n or a, f"| {name} |")
    for fam_, blok in (("F_B2", "B2"), ("F_B4", "B4"), ("F_B9", "B9"), ("F_B10", "B10")):
        n = O.foy_satiri_bul(FOY, a, b, f"| {fam_} | {blok} |")
        FOY.metin(f"M13.2(b) {fam_} size", f"| evet | {val(f'aileler.{fam_}.aile_buyuklugu_json')} |", n or a,
                  f"| {fam_} | {blok} |")
    checks = [("K-a", "B2", f"ongorulen_buyukluk {sp('K-a', 'B2', 'ongorulen_buyukluk.deger'):g}"),
              ("K-a", "B2", f"curutme esigi {sp('K-a', 'B2', 'curutme.esik.deger'):g}"),
              ("K-b", "B2", f"esdegerlik siniri ({-DELTA:g}; {DELTA:g})"),
              ("K-c", "B2", f"ongorulen_buyukluk {sp('K-c', 'B2', 'ongorulen_buyukluk.deger'):g}"),
              ("H1", "B4", f"ongorulen_buyukluk {sp('H1', 'B4', 'ongorulen_buyukluk.deger'):g}"),
              ("H2", "B4", f"ongorulen_buyukluk {sp('H2', 'B4', 'ongorulen_buyukluk.deger'):g}"),
              ("H3", "B4", f"esdegerlik siniri ({-DELTA:g}; {DELTA:g})"),
              ("K-a", "B9", f"ongorulen_buyukluk {sp('K-a', 'B9', 'ongorulen_buyukluk.deger'):g}"),
              ("K-b", "B9", f"esdegerlik siniri ({-DELTA:g}; {DELTA:g})"),
              ("K-c", "B9", f"ongorulen_buyukluk {sp('K-c', 'B9', 'ongorulen_buyukluk.deger'):g}"),
              ("B5", "B5", f"esik {sp('B5', 'B5', 'esik.deger'):g}"),
              ("B6", "B6", f"esik {sp('B6', 'B6', 'esik.deger'):g}"),
              ("B8-A_sigma_IN", "B8", f"beklenti_esigi {sp('B8-A_sigma_IN', 'B8', 'beklenti_esigi.deger'):g}"),
              ("B8-A_sigma_scr_Liu", "B8",
               f"beklenti_esigi {sp('B8-A_sigma_scr_Liu', 'B8', 'beklenti_esigi.deger'):g}")]
    for ds in ("cifar10", "cifar100", "imagenetv2"):
        checks.append((f"H10-{ds}", "B10", f"ongorulen_buyukluk {sp(f'H10-{ds}', 'B10', 'ongorulen_buyukluk.deger'):g}"))
        checks.append((f"H10k-{ds}", "B10",
                       f"ongorulen_buyukluk {sp(f'H10k-{ds}', 'B10', 'ongorulen_buyukluk.deger'):g}"))
        checks.append((f"H10-{ds}", "B10", f"(kestirim <= esik) {kural_esik(f'H10-{ds}', 'B10', 'esik'):g}"))
        checks.append((f"H10-{ds}", "B10", f"(p >= esik) {kural_esik(f'H10-{ds}', 'B10', 'p_esigi'):g}"))
    c0 = O.foy_satiri_bul(FOY, a, b, "(c) Sinamalar") or a          # table (c) of M13.2
    for kim, blok, frag in checks:
        n = O.foy_satiri_bul(FOY, c0, b, f"| {kim} | {blok} |")
        FOY.metin(f"M13.2(c) {kim}/{blok}: {frag}", frag, n or a, f"| {kim} | {blok} |")
    return FOY.bitir(), (a, b)


# ------------------------------------------------------------------ drawing
def xv(x0, w, v):
    return x0 + (v - LO) / (HI - LO) * w


def poly_circle(pid, cx, cy, r, grp, cont, fill=None):
    pts = [(cx + r * math.cos(2 * math.pi * k / 16), cy + r * math.sin(2 * math.pi * k / 16)) for k in range(16)]
    vf.poly(pid, pts + [pts[0]], fill=fill, line=vf.C["ink"], lw=vf.LW["normal"], role="mark", container=cont,
            group=grp)


def diamond(pid, cx, cy, r, grp, cont):
    pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy), (cx, cy - r)]
    vf.poly(pid, pts, fill=vf.C["ink"], line=vf.C["ink"], lw=vf.USLUP.line_min_pt, role="mark", container=cont,
            group=grp)


def band(pid, x0, x1, cy, h, grp, cont):
    pts = [(x0, cy - h / 2), (x1, cy - h / 2), (x1, cy + h / 2), (x0, cy + h / 2), (x0, cy - h / 2)]
    vf.poly(pid, pts, fill=vf.tint_of("katman_gri")[0], line=None, role="mark", container=cont, group=grp)


def lay(R):
    vf.reset(STEM, W, 140.0, naming_step=STEP, naming_kind="serit")
    x0, gap = 0.5, 1.5
    ws = [30.0, 56.0, 48.0]
    ws.append(gf(XR - x0 - sum(ws) - 3 * gap))
    xs = [x0]
    for w_ in ws[:-1]:
        xs.append(xs[-1] + w_ + gap)
    titles = ["Family", "Test and quantity", "Pre-registered values", "Falsified if"]
    ids = [f"k{i}" for i in range(4)]
    tops = [O.strip_panel(ids[i], titles[i], xs[i], 0.5, ws[i], tone="zemin_bandi") for i in range(4)]
    bl.title_strip(ids)
    top = tops[0]
    # number line geometry inside panel 3
    ax0, axw = xs[2] + 2.5, 30.5
    vx = gc(ax0 + axw + 1.5)
    vw = xs[2] + ws[2] - 1.5 - vx
    # tick labels (axis, not data)
    for t in (0.0, 0.4, 0.8):
        lab = f(t) if t else "0"
        wl = tw([lab], S)
        T(f"tick{t}", gr(xv(ax0, axw, t) - wl / 2), top, [lab], size=S, color="muted", cont="k2", w=wl, align="c")
    y = top + LHS + 0.5
    ytop_rows = y
    sep = []
    for i, (fam, note, test, qty, pred, has_band, fals, vals, rule) in enumerate(R):
        if fam and i > 0:
            sep.append(y + 0.5)
            y += 1.0
        # column texts; the row's height is its tallest column
        hs = []
        if fam:
            hs.append(TW(f"r{i}_fam", xs[0] + 1.5, y, fam, ws[0] - 3.0, size=S, cont="k0", key="sb"))
        tw_ = tw([[(test, "sb")]], S)
        T(f"r{i}_test", xs[1] + 1.5, y, [[(test, "sb")]], size=S, cont="k1", w=tw_)
        qx = gc(xs[1] + 1.5 + max(tw([[(r[2], "sb")]], S) for r in R) + 2.0)
        hs.append(TW(f"r{i}_qty", qx, y, qty, xs[1] + ws[1] - 1.5 - qx, size=S, cont="k1"))
        hs.append(TW(f"r{i}_rule", xs[3] + 1.5, y, rule, ws[3] - 3.0, size=S, cont="k3"))
        if vals:
            T(f"r{i}_val", vx, y, [vals], size=S, cont="k2", w=vw)
        cy = y + LHS / 2
        grp = f"r{i}_nl"
        if pred or has_band or fals is not None:
            vf.seg(f"r{i}_base", (ax0, cy), (ax0 + axw, cy), vf.C["muted"], vf.USLUP.line_min_pt)
            if has_band:
                band(f"r{i}_band", xv(ax0, axw, -DELTA), xv(ax0, axw, DELTA), cy, 2.5, grp, "k2")
            if fals is not None:          # a threshold equal to the prediction is a ring around the diamond
                same = pred is not None and abs(fals - pred[1]) < 1e-12
                poly_circle(f"r{i}_fals", xv(ax0, axw, fals), cy, 1.75 if same else 0.9, grp, "k2", fill="FFFFFF")
            if pred:
                diamond(f"r{i}_pred", xv(ax0, axw, pred[1]), cy, 1.2, grp, "k2")
        elif test == "B6":
            T(f"r{i}_nl", gc(xv(ax0, axw, 0.0) + 1.0), y, ["points scale"], size=S, color="muted", cont="k2")
        else:
            T(f"r{i}_nl", gc(xv(ax0, axw, 0.0) + 1.0), y, ["as above"], size=S, color="muted", cont="k2")
        y += max(hs + [LHS])
    # the zero line across the rows
    vf.seg("zero", (xv(ax0, axw, 0.0), ytop_rows - 0.25), (xv(ax0, axw, 0.0), y), vf.C["muted"], vf.USLUP.line_min_pt,
           dash=True)
    for j, ys in enumerate(sep):
        for k in range(4):
            vf.seg(f"sep{j}_{k}", (xs[k] + 0.75, ys), (xs[k] + ws[k] - 0.75, ys), vf.C["frame"], vf.USLUP.line_min_pt)
    for pid in ids:
        vf.IDS[pid]["h"] = gc(y + 1.0 - 0.5)
    # key line
    ky = 0.5 + vf.IDS["k0"]["h"] + 1.0
    kx = x0 + 1.0
    diamond("key_pred", kx + 1.2, ky + LHS / 2, 1.2, "key_p", None)
    w1 = tw(["predicted size"], S)
    T("key_pred_t", kx + 3.0, ky, ["predicted size"], size=S, color="muted")
    kx = gc(kx + 3.0 + w1 + 4.0)
    poly_circle("key_fals", kx + 1.0, ky + LHS / 2, 0.9, "key_f", None, fill="FFFFFF")
    T("key_fals_t", kx + 3.0, ky, ["falsification threshold"], size=S, color="muted")
    kx = gc(kx + 3.0 + tw(["falsification threshold"], S) + 4.0)
    band("key_band", kx, kx + 5.0, ky + LHS / 2, 2.5, "key_b", None)
    lab = f"equivalence band ±δ, δ = {f(DELTA)} (log); Holm α = {f(ALFA)} per family"
    T("key_band_t", kx + 6.5, ky, [lab], size=S, color="muted")
    kx = gc(kx + 6.5 + tw([lab], S) + 4.0)
    labs = ["axis: each row in its own unit (column 2)",
            "† also falsified by a significant reversed sign (H1, H2)"]
    for j, lab2 in enumerate(labs):
        if kx + tw([lab2], S) > XR - 0.5:
            kx, ky = x0 + 1.0, ky + LHS
        T(f"key_note{j}", kx, ky, [lab2], size=S, color="muted")
        kx = gc(kx + tw([lab2], S) + 4.0)
    return gc(ky + LHS + 0.75)


def main():
    R = rows()
    foy, (a, b) = foy_checks()
    h = lay(R)
    v = O.bitir(h, "The registry: every pre-registered test with its quantity, the predicted size and "
                   "falsification threshold on one number line, and the rule that falsifies it.",
                KIND, 4, n_exempt="a registry of thresholds draws no sample", sablon="tablodan_sekle",
                hedef=HEDEF, tavan=TAVAN,
                extra={"denge_muafiyet": {
                    "karakter_cm2": "the figure replaces Table 3; test names, quantities and rules are its content"},
                       "gosterim": {"tau_bar": "τ" + MAC, "Dseed": "Δseed", "Asig_scr": "Aσscr", "Isig": "Iσ",
                                    "Arho": "Aρ", "AbarIN": "A" + MAC + "σIN", "Asig_scr_Liu": "Aσscr,Liu",
                                    "kaynak": "paper/manuscript/macros_konsey.tex lines 3-13",
                                    "not": "script letters follow the symbol: no script position in the engine "
                                           "and a Visio subscript prints under the 8 pt floor"},
                       "sonuc_cizilmedi": "measured outcomes are not drawn (plan section 9.5)"})
    if v != "PASS":
        print("layout:", v, "| foy:", foy["karsilastirma_sayisi"], foy["uyusmayan"])
        return 0
    deg = [O.ev(p, v_, SRC, p, "read as is; printed with :g") for p, v_ in OKUNAN.items()
           if not isinstance(v_, (dict, list))]
    deg.append(O.ev("number line axis", [LO, HI], SRC, "(axis, not data)",
                    "axis range -0.3 to 0.9, ticks 0, 0.4, 0.8, chosen to hold every threshold"))
    O.kanit_yaz(STEM, deg, foy=foy, okunan={SRC: sorted(OKUNAN)},
                ek={"foy_M13_2_satirlari": [a, b], "satirlar": [r[2] for r in R]}, girdiler=[SRC])
    O.denge_ajan(STEM, 0, {"3b_veri": (False, "the figure draws no 3D object and no data in depth"),
                           "3b_kural_disi": (False, "no 3D object is drawn in this registry figure"),
                           "gereksiz_ikon": (False, "diamond, circle and band code the registered values"),
                           "dogrudan_etiket": (True, "every value is printed beside its number line"),
                           "panel_basina_bir_iddia": (True, "each column states one part of the registry"),
                           "gercek_goruntu": ("uygulanmaz", "a registry of tests shows no image"),
                           "her_sayinin_kaynagi": (True, "every threshold is a key of the registry JSON, checked "
                                                         "against the reference sheet")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
