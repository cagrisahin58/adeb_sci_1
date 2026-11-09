#!/usr/bin/env python
"""z_prereg_chain (Fig. 6 v2, Üslup Z): the pre-registration chain as three flat cards on one chain card.

    python paper/figures_v2/z_prereg_chain.py [--check] [--bak]

Double column, flat-card composition (third round, 09.11.2026: no plate, no depth). One flat chain card holds
three stage cards side by side in time order, left to right: the data seen before registration, the main
registration (frozen 29 October 2026) with blocks B2-B6, the supplement (frozen 30 October 2026) with blocks
B8-B10. Two straight flow arrows join the cards; their labels carry the freeze date, the commit and, for the main
registration, the SHA-256 prefix of the registration body. A strip at the bottom of the chain card names the two
post hoc entries of the deviation log. Content: the v1 rule paper/figures/visio/fig_prereg_chain.py (get,
mx, seen_sizes, body_sha, seen_by_supplement, foy_checks; results/q1/konsey_zaman_cizelgesi.json against sheet
sections M13.3, M9.1 and M9.8). Naming: step 2 (labelled flow arrows).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
Z.duz()
PC =Z.yukle_sema("paper/figures/visio/fig_prereg_chain.py", "v1_prereg_chain")
K = PC.K

STEM = "z_prereg_chain"
KIND = "double"
W = vf.page_width(KIND)
CAPTION = ("Pre-registration chain. Seen beforehand lists the data looked at before registration; "
           "Main registration: B2-B6 and Supplement: B8-B10, the addendum of the text, give each block's models, "
           "images and cells. Time runs left to right; arrows carry the freeze dates (October 2026), commits and "
           "registration digest prefix; the strip Added after the fact names two post hoc analyses.")


def wrap(text, width):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if Z.tw([Z.runs(cand)], Z.S8) <= width or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    sha, sha_line = PC.body_sha()
    ek_path, ek_seen = PC.seen_by_supplement()
    a, b = PC.foy_checks()
    foy = PC.FOY.bitir()
    vf.reset(STEM, W, 140.0, naming_step=2, naming_kind="akis")
    LH = lh(Z.S8)
    s3, s8, src_seen, n_seen = PC.seen_sizes()
    get, mx = PC.get, PC.mx
    runs = sorted({x["takma_ad"] for x in get("B3_asamalari")})
    hrs = get("egitim_suresi.defter_toplam_sure_sa")
    cards = [
        ("Seen beforehand", [("", f"C1 pair {s3} matrices (CIFAR-10, CIFAR-100)"), ("", f"one-seed {s8} pool matrix"),
                             ("", "derived values")]),
        ("Main registration: B2-B6", [
            ("B2", f"{mx('B2', 'model_sayisi')} models, {mx('B2', 'hucre_sayisi')} cells, {mx('B2', 'n_goruntu')} images"),
            ("B3", f"{len(runs)} training runs, {hrs:.1f} h"),
            ("B4", f"{mx('B4', 'model_sayisi')} models, {mx('B4', 'hucre_sayisi')} cells"),
            ("B5", f"MI {mx('B5-MI', 'hucre_sayisi')} and TGR {mx('B5-TGR', 'hucre_sayisi')} cells, "
                   f"{mx('B5-MI', 'model_sayisi')} models"),
            ("B6", f"AutoAttack, {mx('B6-AA', 'model_sayisi')} models, {mx('B6-AA', 'n_goruntu')} images")]),
        ("Supplement: B8-B10", [
            ("B9", f"CIFAR-100: {mx('B9', 'model_sayisi')} models, {mx('B9', 'hucre_sayisi')} cells"),
            ("B8", f"ImageNetV2, ε {mx('B8', 'eps_x255'):g}/255: {mx('B8', 'model_sayisi')} models, "
                   f"{mx('B8', 'n_goruntu')} images"),
            ("B10", "Mantel: " + "/".join(str(mx(f"B10-{d}", "model_sayisi")) for d in ("cifar10", "cifar100", "imagenetv2"))
             + " models, " + "/".join(str(mx(f"B10-{d}", "cift_sayisi")) for d in ("cifar10", "cifar100", "imagenetv2"))
             + " pairs"),
            ("", "after B2 ran; B2 ρ seen")]),
    ]
    CWS = [40.0, 49.0, 45.0]
    GAP = 15.0
    DSTEP = 12.0
    IDW = 7.0
    bodies = []
    for (title, items), cw in zip(cards, CWS):
        ls = []
        for bid, txt in items:
            for k, ln in enumerate(wrap(txt, cw - IDW - 2.6)):
                ls.append((bid if k == 0 else "", ln, k == 0))
        bodies.append(ls)
    # third round: the flat chain is shorter than the stage was (48.9 mm), so the text density rose above the
    # balance gate (5.7 characters per cm2); air between the block entries and around the cards brings it back
    EG = 2.0                                       # gap before every new entry (not before a wrapped line)

    def ys(ls):
        out, y_ = [], 0.0
        for j, (_b, _l, first) in enumerate(ls):
            if first and j:
                y_ += EG
            out.append(y_)
            y_ += LH
        return out, y_
    heights = [2.0 + LH + 1.6 + ys(ls)[1] + 3.4 for ls in bodies]
    H = max(heights)
    # third round (09.11.2026): flat composition. One flat chain card holds the three stage cards side by side,
    # top-aligned, time running left to right, and the post hoc strip under them; no plate, no depth.
    GX, GY = 1.0, 1.0
    GW = W - 2 * GX
    x0 = GX + (GW - (sum(CWS) + 2 * GAP)) / 2
    xs = [x0, x0 + CWS[0] + GAP, x0 + CWS[0] + GAP + CWS[1] + GAP]
    cy = GY + 2.4
    yd = cy + H + 3.0                              # the post hoc note card under the stage cards
    DH = LH + 2.4
    GH = (yd + DH + 2.0) - GY
    Z.duz_kart("chain", GX, GY, GW, GH, "sahne")
    boxes = []
    for i, ((title, items), cw, ls) in enumerate(zip(cards, CWS, bodies)):
        fx, fy, fw, fh = Z.duz_kart(f"c{i}", xs[i], cy, cw, H, "kutu", cont="chain_face")
        face = f"c{i}_face"
        T(f"ct{i}", fx + 1.2, fy + 2.0, [[(title, "sb")]], size=Z.S8, cont=face)
        yy, _ = ys(ls)
        for j, (bid, ln, _first) in enumerate(ls):
            y = fy + 2.0 + LH + 1.6 + yy[j]
            if bid:
                T(f"cb{i}{j}", fx + 1.2, y, [[(bid, "sb")]], size=Z.S8, cont=face)
            T(f"cl{i}{j}", fx + 1.2 + (IDW if any(t_[0] for t_ in ls) else 0.0), y, [Z.runs(ln)], size=Z.S8, cont=face)
        # a small matrix glyph: the blocks' transfer matrices (3 x 3 seen beforehand; schematic 4 x 4 otherwise)
        gn = 3 if i == 0 else 4
        gs = 3.6
        gx0, gy0 = fx + fw - gs - 1.6, fy + 1.8
        sq = [(gx0, gy0), (gx0 + gs, gy0), (gx0 + gs, gy0 + gs), (gx0, gy0 + gs)]
        vf.poly(f"gm{i}", sq + [sq[0]], fill=vf.tint_of("ton_6")[0], line=vf.tint_of("ton_6")[1], lw=vf.LW["ince"],
                role="container", container=face)
        for q in range(gn):
            c_ = [(gx0 + q * gs / gn, gy0 + q * gs / gn), (gx0 + (q + 1) * gs / gn, gy0 + q * gs / gn),
                  (gx0 + (q + 1) * gs / gn, gy0 + (q + 1) * gs / gn), (gx0 + q * gs / gn, gy0 + (q + 1) * gs / gn)]
            vf.poly(f"gd{i}{q}", c_ + [c_[0]], fill=vf.tint_of("isi_0")[0], line=None, role="deco", container=f"gm{i}")
        for q in range(1, gn):
            vf.seg(f"gv{i}{q}", (gx0 + q * gs / gn, gy0), (gx0 + q * gs / gn, gy0 + gs), vf.tint_of("ton_6")[1], vf.LW["ince"])
            vf.seg(f"gh{i}{q}", (gx0, gy0 + q * gs / gn), (gx0 + gs, gy0 + q * gs / gn), vf.tint_of("ton_6")[1], vf.LW["ince"])
        boxes.append((fx, fy, fw, fh))
    labs = [[PC.date_of(get("dondurma.on_kayit.utc")), get("dondurma.on_kayit.commit")[:7], sha[:8]],
            [PC.date_of(get("dondurma.ek_on_kayit.utc")), get("dondurma.ek_on_kayit.commit")[:7]]]
    for j in range(2):
        # a straight flow arrow in the gap between two cards, at mid height, its label just above it
        ya = gr(cy + H * 0.62)
        p0 = (xs[j] + CWS[j] + 1.0, ya)
        p1 = (xs[j + 1] - 1.0, ya)
        vf.seg(f"f{j}", p0, p1, vf.C["arrow"], vf.LW["vurgu"], arrow=True)
        vf.note_naming(f"f{j}", "flow")
        lines = [[(t_, "sb" if k == 0 else "r")] for k, t_ in enumerate(labs[j])]
        wl = max(Z.tw([ln], Z.S8) for ln in lines)
        xm = (p0[0] + p1[0]) / 2
        ytop = ya - len(lines) * LH - 1.0
        T(f"fl{j}", xm, ytop, lines, size=Z.S8, color="muted", align="c", w=wl, cont="chain_face")
    dev = [s for s in get("sapma_kaydi_basliklari") if "sonradan" in s["baslik"]]
    if len(dev) != 2:
        raise SystemExit(f"expected two post hoc entries, found {len(dev)}")
    Z.duz_kart("devc", xs[0], yd, xs[2] + CWS[2] - xs[0], DH, "kap", cont="chain_face")
    T("dev", xs[0] + 1.2, yd + 1.2, [[("Added after the fact:  ", "sb"), ("main §7: hierarchical bootstrap;  supplement §12: S10-3", "r")]],
      size=Z.S8, cont="devc_face")
    Z.sayfa_sigdir()
    deg = [Z.ev(p, v_, PC.SRC, p, "read as is") for p, v_ in PC.OKUNAN.items() if v_ != "(structure)"]
    for k_, m in get("matrisler").items():
        for kk in ("n_goruntu", "model_sayisi", "hucre_sayisi", "cift_sayisi", "eps_x255"):
            if kk in m:
                deg.append(Z.ev(f"{k_} {kk}", m[kk], PC.SRC, f"matrisler.{k_}.{kk}", "printed as is"))
    deg.append(Z.ev("B3 runs", len(runs), PC.SRC, "len(set(B3_asamalari[].takma_ad))", "distinct run names"))
    deg.append(Z.ev("registration body SHA-256 prefix", sha[:8], f"results/C1_REFERANS_FOYU.md:{sha_line}",
                    "M9.8 SHA-256", "first 8 hex"))
    deg.append(Z.ev("seen matrices 3x3 and 8x8", ["3x3", "8x8"], f"{src_seen}:{n_seen}", "section 1", "regex"))
    deg.append(Z.ev("supplement row: after B2 ran; B2 rho seen", {k_: v["satir"] for k_, v in ek_seen.items()}, ek_path,
                    "lines " + ", ".join(str(v["satir"]) for v in ek_seen.values()), "sentences found verbatim"))
    for d in dev:
        deg.append(Z.ev("deviation entry", d["baslik"], d["kaynak"].rsplit(":", 1)[0], d["kaynak"], "title, translated"))
    return Z.bitir(
        STEM, message="The pre-registration chain: what was seen before registration, the frozen main registration "
                      "with blocks B2-B6, the frozen supplement with blocks B8-B10, and the post hoc entries.",
        kind=KIND, panels=3, caption=CAPTION, sablon="yontem_semasi", tur="sematik", degerler=deg,
        kanit_ek={"foy_karsilastirmasi": foy, "foy_M13_3_satirlari": [a, b], "b3_saat": hrs},
        manifest={"sahne_kalibi": "yok (duz zincir karti, ucuncu tur)", "surec_zinciri": True,
                  "panel_adlari": [c[0] for c in cards] + ["Added after the fact"],
                  "derinlik_ekseni": "none: time runs left to right",
                  "ic_ice_derinlik": {"deger": 3, "gerekce": "the chain card holds the three stage cards, each stage "
                                                             "card holds its matrix glyph and block entries"}},
        denge={"panel_basina_bir_iddia": (True, "each card is one stage of the registration chain"),
               "gereksiz_ikon": (False, "there are no icons; arrows carry the freeze labels")},
        n_exempt_reason="each block prints its model and image counts",
        okunan_ek=[PC.SRC, "raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md", ek_path, "results/C1_REFERANS_FOYU.md"])


if __name__ == "__main__":
    sys.exit(main())
