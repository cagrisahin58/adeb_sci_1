#!/usr/bin/env python
"""z_protocol_sets (Fig. 14 v2, Üslup Z): nested conditioning sets as a terraced sand pit, and the asymmetry.

    python paper/figures_v2/z_protocol_sets.py [--check] [--bak]

Single column. Conditioning sets: on a sand plate four terraces rise, the widest and lowest the unconditioned
set, each nested set one step higher, narrower and further in (target-correct, both-correct, successful-
source); the terraces carry the nesting only (schematic, not area-proportional). A leader from each terrace's
front face leads to its label: name, the condition the set adds (the mask in words) and N averaged over the
seed pairs (CNN to ViT / ViT to CNN where the two differ). Measured asymmetry: an upright card under the pit,
per protocol the three seed-pair asymmetries (small open circles), the mean (protocol mark) and SD (line), the
mean +- SD printed, and a stepped path whose three steps print the distances between adjacent protocols.
Data: results/q1/fig_protokol_kumeleri_veri.json through konsey fig_protocol_sets.load_and_check, every number
against results/C1_REFERANS_FOYU.md lines 53-56, 60, 212-215, 805-808 (the checks of the v1 chart script
paper/figures/charts/fig_protocol_sets.py veri(), run here without its tab:protocol_masks lookup, a table the
manuscript no longer has). Naming: step 4 (two title strips).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
PV = Z.yukle("paper/figures/charts/fig_protocol_sets.py", "v1_protocol_sets")
K = PV.K

STEM = "z_protocol_sets"
KIND = "single"
W = vf.page_width(KIND)
MK = {"raw": ("o", "isi_2"), "target_correct": ("^", "isi_3"), "both_correct": ("s", "isi_4"),
      "successful_source": ("D", "isi_5")}
TINT = {"raw": "ton_6", "target_correct": "govde_panel", "both_correct": "govde_vit", "successful_source": "isi_4"}
CAPTION = ("Conditioning sets and measured asymmetry. Conditioning sets: nested evaluation sets as terraces "
           "(schematic, not area-proportional; terrace height carries no value) with masks and mean N. Measured "
           "asymmetry: mean±SD of the within-pair difference, pairs as open circles, read as positions on the "
           "flat card and printed; the steps print the three decomposition terms.")


def veri():
    """The v1 chart rule without its manuscript-table lookup (see the module docstring)."""
    d, k_seeds, per_seed = PV.PS.load_and_check(Path(PV.DATA))
    P, A = d["protokoller"], d["ayrisim"]
    if d["kaynak"] != PV.SRC:
        K.fail(f"{PV.DATA}: kaynak {d['kaynak']} != {PV.SRC}")
    if K.sha(PV.SRC) != d["kaynak_sha256"]:
        K.fail(f"{PV.SRC} changed since {PV.DATA} was written (sha256)")
    foy = K.Foy()
    for p_ in PV.PROTOCOLS:
        ln, anc = PV.FOY_ROW[p_]
        foy.kontrol(f"{p_}: asimetri_ort", P[p_]["asimetri_ort"], ln, anc, 2)
        foy.kontrol(f"{p_}: asimetri_sd", P[p_]["asimetri_sd"], ln, anc, 2)
        foy.kontrol(f"{p_}: n_CNN_to_ViT", P[p_]["n_CNN_to_ViT"], ln, anc, 0)
        foy.kontrol(f"{p_}: n_ViT_to_CNN", P[p_]["n_ViT_to_CNN"], ln, anc, 0)
        for i_, v_ in enumerate(P[p_]["asimetri_tohum_degerleri"]):
            foy.kontrol(f"{p_}: seed pair {i_ + 1}", v_, 805 + i_, f"| cift {i_ + 1} |", 2)
    foy.kontrol("yayilim", A["yayilim"], 60, "Protokol yayilimi", 2)
    for a, b, key, ln, anc, _ in PV.STEPS:
        foy.kontrol(key, A[key], ln, anc, 2)
        sgn = 1 if key.startswith("ozdeslik") else -1
        foy.esit(f"{key} == means", A[key], sgn * (P[a]["asimetri_ort"] - P[b]["asimetri_ort"]), 0.0101,
                 "step distance from the protocol means (one rounding unit per operand)")
    tex = Path(PV.TEX).read_text(encoding="utf-8")
    if "top card of Figure~\\ref{fig:protocol_sets}" not in tex:
        K.fail(f"{PV.TEX}: the sentence that places the masks in this figure is gone")
    return d, foy.bitir()


def main():
    d, foy = veri()
    P, A = d["protokoller"], d["ayrisim"]
    prots = list(PV.PROTOCOLS)
    vf.reset(STEM, W, 150.0, naming_step=4, naming_kind="serit")
    OX, OY = 3.0, 66.0
    S = Z.Sahne(OX, OY)
    deg = []
    # ---- Conditioning sets: the terraced pit
    T("h1", 1.0, 1.0, [[("Conditioning sets", "sb")]], size=Z.S8)
    L0, D0, TH = 34.0, 24.0, 4.2
    Z.plaka_un(S, "pit", *Z.un(S, -1.5, -1.0), L0 + 3.0, D0 + 2.0, 1.4, tint="sahne")
    anchors = []
    for i, p in enumerate(prots):
        Li, Di = L0 - 7.6 * i, D0 - 5.0 * i
        X, Y = Z.un(S, 3.8 * i, 2.5 * i)
        top = Z.plaka_un(S, f"t{i}", X, Y, Li, Di, TH, tint=TINT[p], z=TH * (i + 1))
        fr = S.P(*Z.un(S, 3.8 * i + Li, 2.5 * i), TH * (i + 0.5))
        anchors.append(fr)
    xl = OX + L0 + 13.0
    yl = 1.0
    for i, p in enumerate(prots):
        n1, n2 = P[p]["n_CNN_to_ViT"], P[p]["n_ViT_to_CNN"]
        nlab = f"N = {n1:,}" if n1 == n2 else f"N = {n1:,} / {n2:,}"
        y = yl + (3 - i) * (4 * lh(Z.S8) + 0.8)
        T(f"ln{i}", xl, y, [[(PV.NAME[p], "sb")]], size=Z.S8)
        words = PV.MASK[p][0].split()
        cut = max(1, (len(words) + 1) // 2) if len(words) > 3 else len(words)
        mlines = [" ".join(words[:cut])] + ([" ".join(words[cut:])] if words[cut:] else [])
        T(f"lc{i}", xl, y + lh(Z.S8), mlines, size=Z.S8, color="muted")
        T(f"lN{i}", xl, y + (1 + len(mlines)) * lh(Z.S8), [nlab], size=Z.S8)
        ax_, ay_ = anchors[i]
        vf.seg(f"ld{i}", (ax_ + 0.3, ay_), (xl - 0.6, y + lh(Z.S8) / 2), vf.C["frame"], vf.LW["ince"])
        for f, v in (("n_CNN_to_ViT", n1), ("n_ViT_to_CNN", n2)):
            deg.append(Z.ev(f"{PV.NAME[p]} {f}", v, PV.DATA, f"protokoller.{p}.{f}",
                            f"mean over seed pairs; == foy line {PV.FOY_ROW[p][0]}"))
    T("notprop", 1.0, max(OY + 2.6, yl + 4 * (4 * lh(Z.S8) + 0.8)), ["terraces: nesting only, not area-proportional;", "N: mean over the three seed pairs"],
      size=Z.S8, color="muted")
    # ---- Measured asymmetry: an upright card
    RH = lh(Z.S8) + 3.6
    CH = 1.0 + lh(Z.S8) + 0.8 + 4 * RH + 1.0 + 10.2
    cz_top = max(OY + 2.6, yl + 4 * (4 * lh(Z.S8) + 0.8)) + 2 * lh(Z.S8) + 2.0
    S2 = Z.Sahne(1.0, cz_top + CH)
    fx, fy, fw, fh = Z.kart(S2, "card", 0.0, 0.0, 0.0, W - 1.0 - 2.4, CH, "kutu", t=1.6, shadow=False)
    face = "card_face"
    T("h2", fx + 1.2, fy + 0.8, [[("Measured asymmetry", "sb")]], size=Z.S8, cont=face)
    T("h2n", fx + fw - 1.2, fy + 0.8, ["n = 3 seed pairs"], size=Z.S8, color="muted", align="r", cont=face)
    px0, px1 = fx + 26.8, fx + fw - 15.2
    sc = Z.Olcek(0.0, 22.0, px0, px1)
    ytop = fy + 1.0 + lh(Z.S8) + 0.8
    yc = {}
    for i, p in enumerate(prots):
        y = ytop + i * RH + RH / 2 + 0.6
        yc[p] = y
        m, sd = P[p]["asimetri_ort"], P[p]["asimetri_sd"]
        mk, tint = MK[p]
        col = vf.tint_of(tint)[0]
        T(f"rl{i}", px0 - 1.6, y - lh(Z.S8) / 2, [PV.NAME[p]], size=Z.S8, align="r", cont=face)
        vf.seg(f"sd{i}", (sc(m - sd), y), (sc(m + sd), y), vf.C["ink"], vf.LW["ince"])
        for j, v in enumerate(P[p]["asimetri_tohum_degerleri"]):
            Z.isaret(f"pr{i}_{j}", sc(v), y - 1.5, "o", fill=None, edge="ink", size=0.95, group=f"row{i}")
            deg.append(Z.ev(f"{PV.NAME[p]} seed pair {j + 1}", v, PV.DATA, f"protokoller.{p}.asimetri_tohum_degerleri[{j}]",
                            f"read; == foy line {805 + j} (2 dp); position"))
        Z.isaret(f"mn{i}", sc(m), y, mk, fill=col, edge=Z.soft(col, 0.4), size=2.0, group=f"row{i}")
        T(f"mv{i}", fx + fw - 1.2, y - lh(Z.S8) / 2, [f"{m:.2f}±{sd:.2f}"], size=Z.S8, align="r", cont=face)
        deg.append(Z.ev(f"{PV.NAME[p]} mean", m, PV.DATA, f"protokoller.{p}.asimetri_ort", f"read; == foy line {PV.FOY_ROW[p][0]}; printed 2 dp"))
        deg.append(Z.ev(f"{PV.NAME[p]} SD", sd, PV.DATA, f"protokoller.{p}.asimetri_sd", f"read; == foy line {PV.FOY_ROW[p][0]}; printed 2 dp"))
    for j, (a, b, key, ln, anc, lab) in enumerate(PV.STEPS):
        xa, xb = sc(P[a]["asimetri_ort"]), sc(P[b]["asimetri_ort"])
        ya, yb = yc[a] + 1.4, yc[b] - 2.6
        ym = (ya + yb) / 2
        pts = [(xa, ya), (xa, ym), (xb, ym), (xb, yb)]
        vf.seg(f"st{j}a", (xa, ya), (xa, ym), vf.C["arrow"], vf.LW["ince"])
        vf.seg(f"st{j}b", (xa, ym), (xb, ym), vf.C["arrow"], vf.LW["ince"])
        vf.seg(f"st{j}c", (xb, ym), (xb, yb), vf.C["arrow"], vf.LW["ince"], arrow=True)
        if max(xa, xb) > px1 - 12.0:
            T(f"sv{j}", max(xa, xb) - 1.0, ym - lh(Z.S8) - 0.1, [f"{A[key]:.2f}"], size=Z.S8, color="muted",
              align="r", cont=face)
        else:
            T(f"sv{j}", max(xa, xb) + 1.0, ym - lh(Z.S8) / 2, [f"{A[key]:.2f}"], size=Z.S8, color="muted", cont=face)
        deg.append(Z.ev(f"step {lab}", A[key], PV.DATA, f"ayrisim.{key}", f"read; == foy line {ln}; printed 2 dp"))
    Z.kot("ax", px0, px1, fy + fh - 10.2, sc, [0, 10, 20], ["0", "10", "20"], cont=face)
    T("axl", (px0 + px1) / 2, fy + fh - 4.4, ["CNN to ViT minus ViT to CNN (pts)"], size=Z.S8,
      color="muted", align="c", cont=face)
    vf.seg("rule", (fx + 1.0, fy + 1.0 + lh(Z.S8) + 0.3), (fx + fw - 1.0, fy + 1.0 + lh(Z.S8) + 0.3), vf.C["frame"],
           vf.LW["vurgu"])
    for _pid in ["h1", "h2"]:          # the panel titles are the strips of naming step 4
        vf.note_naming(_pid, "strip")
    Z.sayfa_sigdir()
    ents = {PV.NAME[p]: "#" + vf.tint_of(MK[p][1])[0] for p in prots}
    return Z.bitir(
        STEM, message="The four nested sets give asymmetries from 4.36 to 19.37 points; identity, marginal subsets and "
                      "source robustness account for the steps.", kind=KIND, panels=2, caption=CAPTION,
        sablon="ortak_satirli_katlar", tur="veri", degerler=deg,
        kanit_ek={"foy_karsilastirmasi": foy, "maske_tanimi": {p: PV.MASK[p][0] for p in prots},
                  "maske_kaynagi": "v1 MASK definitions; paper/manuscript/sections/03_methodology.tex line 215 places "
                                   "the masks in this figure (the former tab:protocol_masks no longer exists)"},
        manifest={"entities": ents, "sahne_kalibi": "terasli_havuz",
                  "panel_adlari": ["Conditioning sets", "Measured asymmetry"],
                  "derinlik_ekseni": "nesting: each inner set is one step higher and further in; no measured value",
                  "ikiz_kodlama": "asymmetries are positions on a flat card and printed as mean±SD; N printed"},
        denge={"panel_basina_bir_iddia": (True, "top the nested sets, bottom the asymmetry under each"),
               "3b_veri": (False, "terrace height and depth carry the registered nesting only, never a measured value")},
        n_exempt_reason="the card states n = 3 seed pairs", okunan_ek=[PV.DATA, PV.SRC, PV.TEX])


if __name__ == "__main__":
    sys.exit(main())
