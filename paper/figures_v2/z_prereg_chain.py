#!/usr/bin/env python
"""z_prereg_chain (Fig. 6 v2, Üslup Z): the pre-registration chain as a time shelf running into depth.

    python paper/figures_v2/z_prereg_chain.py [--check] [--bak]

Double column. On one long sand plate three upright cards stand in time order, each 14 mm further back than the
previous one: the data seen before registration, the main registration (frozen 29 October 2026) with blocks
B2-B6, the supplement (frozen 30 October 2026) with blocks B8-B10. The depth axis is time: walking into the scene
is moving along the chain. Two flow arrows on the plate join the cards; their labels carry the freeze date, the
commit and, for the main registration, the SHA-256 prefix of the registration body. A strip under the plate names
the two post hoc entries of the deviation log. Content: the v1 rule paper/figures/visio/fig_prereg_chain.py (get,
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
PC = Z.yukle_sema("paper/figures/visio/fig_prereg_chain.py", "v1_prereg_chain")
K = PC.K

STEM = "z_prereg_chain"
KIND = "double"
W = vf.page_width(KIND)
CAPTION = ("Pre-registration chain as a time shelf. Seen beforehand lists the data looked at before registration; "
           "Main registration: B2-B6 and Supplement: B8-B10, the addendum of the text, give each block's models, "
           "images and cells. Cards recede in time; arrows carry the freeze dates (October 2026), commits and "
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
                ls.append((bid if k == 0 else "", ln))
        bodies.append(ls)
    heights = [1.0 + LH + 0.9 + len(ls) * LH + 1.0 for ls in bodies]
    H = max(heights)
    OY = 4.0 + 2 * DSTEP * 0.664 + H + 6.0
    S = Z.Sahne(1.5, OY)
    xs = [0.0, CWS[0] + GAP, CWS[0] + GAP + CWS[1] + GAP]
    Lp = xs[2] + CWS[2] + 2.0
    Z.plaka_un(S, "stage", *Z.un(S, 0.4, -3.0), Lp - 5.5, 2 * DSTEP + 21.0, 1.6, tint="sahne")
    boxes = []
    for i, ((title, items), cw, ls) in enumerate(zip(cards, CWS, bodies)):
        X, Y = Z.un(S, xs[i], i * DSTEP)
        fx, fy, fw, fh = Z.kart(S, f"c{i}", X, Y, 0.0, cw, H, "kutu", t=1.6, shadow=False, group=f"c{i}",
                                cont="stage_top")
        face = f"c{i}_face"
        T(f"ct{i}", fx + 1.2, fy + 1.0, [[(title, "sb")]], size=Z.S8, cont=face)
        for j, (bid, ln) in enumerate(ls):
            y = fy + 1.0 + LH + 0.9 + j * LH
            if bid:
                T(f"cb{i}{j}", fx + 1.2, y, [[(bid, "sb")]], size=Z.S8, cont=face)
            T(f"cl{i}{j}", fx + 1.2 + (IDW if any(b_ for b_, _ in ls) else 0.0), y, [Z.runs(ln)], size=Z.S8, cont=face)
        # a small matrix glyph: the blocks' transfer matrices (3 x 3 seen beforehand; schematic 4 x 4 otherwise)
        gn = 3 if i == 0 else 4
        gs = 3.6
        gx0, gy0 = fx + fw - gs - 1.6, fy + 1.2
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
        # the arrow runs on the plate along the time direction, from the foot of one card toward the next
        p0 = S.P(*Z.un(S, xs[j] + CWS[j] + 1.0, j * DSTEP + 1.0), 0.0)
        p1 = S.P(*Z.un(S, xs[j + 1] - 1.0, (j + 1) * DSTEP - 1.0), 0.0)
        vf.spline(f"f{j}", [p0, ((p0[0] + p1[0]) / 2, max(p0[1], p1[1]) + 1.6), p1], vf.C["arrow"], vf.LW["vurgu"], arrow=True)
        vf.note_naming(f"f{j}", "flow")
        lines = [[(t_, "sb" if k == 0 else "r")] for k, t_ in enumerate(labs[j])]
        wl = max(Z.tw([ln], Z.S8) for ln in lines)
        xm = (p0[0] + p1[0]) / 2
        ytop = min(p0[1], p1[1]) - len(lines) * LH - 1.2
        T(f"fl{j}", xm, ytop, lines, size=Z.S8, color="muted", align="c", w=wl, cont="stage_top")
    yd = OY + 5.0
    dev = [s for s in get("sapma_kaydi_basliklari") if "sonradan" in s["baslik"]]
    if len(dev) != 2:
        raise SystemExit(f"expected two post hoc entries, found {len(dev)}")
    T("dev", 1.0, yd, [[("Added after the fact:  ", "sb"), ("main §7: hierarchical bootstrap;  supplement §12: S10-3", "r")]],
      size=Z.S8)
    T("tnote", W - 1.0, yd, ["depth: time, front to back"], size=Z.S8, color="muted", align="r")
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
        manifest={"sahne_kalibi": "zaman_rafi", "surec_zinciri": True,
                  "panel_adlari": [c[0] for c in cards] + ["Added after the fact"],
                  "derinlik_ekseni": "time: each card 14 mm behind the previous one along the registration chain",
                  "ic_ice_derinlik": {"deger": 3, "gerekce": "stage plate holds the three cards, each card holds its "
                                                             "block entries; the polygon card faces read as one level"}},
        denge={"panel_basina_bir_iddia": (True, "each card is one stage of the registration chain"),
               "gereksiz_ikon": (False, "there are no icons; arrows carry the freeze labels")},
        n_exempt_reason="each block prints its model and image counts",
        okunan_ek=[PC.SRC, "raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md", ek_path, "results/C1_REFERANS_FOYU.md"])


if __name__ == "__main__":
    sys.exit(main())
