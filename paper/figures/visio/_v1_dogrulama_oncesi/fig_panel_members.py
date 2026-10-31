#!/usr/bin/env python
"""Reference-panel members (fig:panel_members, Y2), style 8, Visio, one column, naming step 4 (strip).

    python paper/figures/visio/fig_panel_members.py --uslup 8 [--check]

Binding plan: raporlar/visio_2026-10-31/04_cizim_plani.md sections 5 and 9.4 (Y2 is its own one-column
figure; target 100 mm, ceiling 110 mm; template tasarim_izgarasi). Top panel: the CIFAR block, one row
per RobustBench model in the union of the CIFAR-10 and CIFAR-100 panels, membership columns C10 and
C100 (filled square = primary member, open square = secondary member), a ResNet-18 column (dot).
Bottom: the ImageNetV2 block, one strip panel in two columns: the robust CNN panel with the secondary
XCiT-S12, and the same-recipe CNN-transformer pairs (rule under each pair) with the unpaired
transformer. Strip titles are set at the body size (9 pt) so that the rows fit the ceiling. CNN members carry the panel hue (#999999), XCiT rows the xcit hue (#CC79A7); ImageNetV2
transformers do not use the ViT-Tiny hue (#D55E00) and carry an open triangle with a neutral edge.

Every row comes from the frozen cell tables (raporlar/konsey_2026-10-29/hucre_tablosu{,_b9,_b8}.json,
modeller.<m>.{birincil_panel, ikincil_panel, hucre, aile}) and the frozen B8 pairs
(results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json b2.F_B2.K-a.ciftler); member counts (7, 7, 6)
and matrix sizes (20, 15, 14) are checked against the reference sheet (lines 1569, 1741, 1826, 1827,
1873-1887, 1909-1932) by _icerik_study_overview.sayilar(), which also feeds the study overview.

Row names: the cell-table keys. For CIFAR-100 the table prefix 'C100_' and for ImageNetV2 'IN_' are
dropped (table prefixes, not part of the RobustBench names); the CIFAR names are RobustBench IDs, the
ImageNetV2 names are the tables' short IDs (the full RobustBench IDs are in the evidence file).
ResNet-18 derivatives are the IDs whose name carries the token R18 or RN18.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _sema_ortak as O  # noqa: E402
from _sema_ortak import vf, bl, gr, gc, gf, lh, tw, T  # noqa: E402

O.baslat()
import _icerik_study_overview as IC  # noqa: E402

K = O.K
STEM = "panel_members"
KIND = "single"
STEP = 4
HEDEF, TAVAN = 100.0, 110.0
S = vf.SMALL
LHS = lh(S)
W = vf.page_width(KIND)
XR = gf(W - 0.5)
C, FOY, OKUNAN = IC.sayilar()
R18 = re.compile(r"(?:^|_)RN?18(?:_|$)")
MK = 2.25                          # marker side, mm


def rows_data():
    h10, h100, h8 = (K.dig(K.load_json(p), "modeller") for p in (IC.HT10, IC.HT100, IC.HT8))
    pairs = K.dig(K.load_json(IC.J8), "b2.F_B2.K-a.ciftler")
    cif = {}
    for tab, ds, pre in ((h10, "c10", ""), (h100, "c100", "C100_")):
        for k, v in tab.items():
            if not (v["birincil_panel"] or v["ikincil_panel"]):
                continue
            name = k[len(pre):] if pre and k.startswith(pre) else k
            r = cif.setdefault(name, {"id": name, "aile": v["aile"], "c10": None, "c100": None, "keys": []})
            r[ds] = "primary" if v["birincil_panel"] else "secondary"
            r["keys"].append(f"{'hucre_tablosu_b9' if ds == 'c100' else 'hucre_tablosu'}:{k}")
    order = {("primary", "primary"): 0, ("primary", None): 1, (None, "primary"): 2}
    cif_rows = sorted(cif.values(), key=lambda r: (order.get((r["c10"], r["c100"]), 3), list(cif).index(r["id"])))
    strip = lambda k: k[3:] if k.startswith("IN_") else k  # noqa: E731
    in_panel = [{"id": strip(k), "key": k, "role": "primary" if v["birincil_panel"] else "secondary",
                 "aile": v["aile"], "rb": v["kontrol_noktasi"].split(" (")[0]}
                for k, v in h8.items() if v["birincil_panel"] or v["ikincil_panel"]]
    in_panel.sort(key=lambda r: r["role"] != "primary")
    paired = {m for p in pairs for m in p}
    in_pairs = []
    for cnn, tr in pairs:
        for k in (cnn, tr):
            v = h8[k]
            in_pairs.append({"id": strip(k), "key": k, "aile": v["aile"], "pair": f"{strip(cnn)} / {strip(tr)}",
                             "rb": v["kontrol_noktasi"].split(" (")[0], "transformer": v["aile"] != "CNN"})
    for k, v in h8.items():
        if not (v["birincil_panel"] or v["ikincil_panel"]) and k not in paired:
            in_pairs.append({"id": strip(k), "key": k, "aile": v["aile"], "pair": None, "unpaired": True,
                             "rb": v["kontrol_noktasi"].split(" (")[0], "transformer": v["aile"] != "CNN"})
    return cif_rows, in_panel, in_pairs, pairs


CIF, INP, INQ, PAIRS = rows_data()


def check_counts():
    """The drawn rows against the counts the reference sheet carries (via IC.sayilar)."""
    n10 = sum(1 for r in CIF if r["c10"] == "primary")
    n100 = sum(1 for r in CIF if r["c100"] == "primary")
    s10 = sum(1 for r in CIF if r["c10"] == "secondary")
    s100 = sum(1 for r in CIF if r["c100"] == "secondary")
    nin = sum(1 for r in INP if r["role"] == "primary")
    sin = sum(1 for r in INP if r["role"] == "secondary")
    got = {"PanelCten": n10, "PanelChun": n100, "SecCten": s10, "SecChun": s100, "PanelIN": nin, "SecIN": sin,
           "PairsIN": len(PAIRS), "UnpairedIN": sum(1 for r in INQ if r.get("unpaired"))}
    bad = {k: (v, C[k]) for k, v in got.items() if v != C[k]}
    if bad:
        raise SystemExit(f"drawn rows disagree with the checked counts: {bad}")
    return got


def mark(pid, x, y, kind, hexv, cont):
    """Membership marker on one row: filled square, open square, open triangle, dot."""
    yy = gr(y + (LHS - MK) / 2)
    if kind == "primary":
        vf.rect(pid, gr(x), yy, MK, MK, fill=hexv, line=vf.C["muted"], lw=vf.USLUP.line_min_pt, role="mark",
                container=cont)
    elif kind == "secondary":
        vf.rect(pid, gr(x), yy, MK, MK, fill="FFFFFF", line=hexv, lw=vf.LW["vurgu"], role="mark", container=cont)
    elif kind == "triangle":
        x0 = gr(x)
        vf.poly(pid, [(x0, yy + MK), (x0 + MK, yy + MK), (x0 + MK / 2, yy), (x0, yy + MK)], fill="FFFFFF",
                line=vf.C["muted"], lw=vf.LW["normal"], role="mark", container=cont)
    elif kind == "dot":
        d = 1.25
        vf.oval(pid, gr(x + (MK - d) / 2), gr(y + (LHS - d) / 2), d, d, fill=vf.C["ink"], line=None, role="mark",
                container=cont)


def hue(aile):
    return vf.C["xcit"] if aile == "XCiT" else vf.C["panel"]


def strip_panel(pid, title, x, y, w):
    """A letterless strip panel whose title is set at the body size (9 pt) instead of the style's
    10.9 pt title, so the 27 model rows fit the plan's ceiling; returns the content top."""
    vf.panel(pid, None, title, gr(x), gr(y), gc(w), 10, naming="strip")
    vf.IDS[pid]["fill"] = vf.tint_of("zemin_bandi")[0]     # a tone card per data-set block (grouping tool)
    t = vf.IDS[pid + "_title"]
    t["design"], t["size"] = vf.BODY, vf.authored(vf.BODY)
    t["y"], t["h"] = gr(y) + 1.25, lh()
    t["w"] = tw([[(title, "sb")]])
    return gc(t["y"] + t["h"] + 0.25)


def lay():
    vf.reset(STEM, W, 140.0, naming_step=STEP, naming_kind="serit")
    x0 = 0.5
    pw = XR - x0
    # ---------------- CIFAR block: one row per model, membership columns
    cy = strip_panel("pa", "CIFAR-10 and CIFAR-100", x0, 0.5, pw)
    colw = 9.5                                   # column centres, right to left: R18, C100, C10
    cen = {"R18": gf(XR - 1.75 - tw(["R18"], S) / 2)}
    cen["C100"] = cen["R18"] - colw
    cen["C10"] = cen["C100"] - colw
    xr18, xc100, xc10 = (gr(cen[k] - MK / 2) for k in ("R18", "C100", "C10"))
    ty = vf.IDS["pa_title"]["y"]
    for lab in ("C10", "C100", "R18"):
        wl = tw([lab], S)
        T(f"pa_h{lab}", gr(cen[lab] - wl / 2), ty, [lab], size=S, color="muted", cont="pa", w=wl, align="c")
    idx = x0 + 1.75
    room = xc10 - 1.0 - idx
    for i, r in enumerate(CIF):
        y = cy + i * LHS
        if tw([r["id"]], S) > room:
            raise SystemExit(f"{r['id']} needs {tw([r['id']], S)} mm, the column has {room:.2f} mm")
        T(f"ca{i}", idx, y, [r["id"]], size=S, cont="pa")
        for ds, xm in (("c10", xc10), ("c100", xc100)):
            if r[ds]:
                mark(f"ca{i}_{ds}", xm, y, r[ds], hue(r["aile"]), "pa")
        if R18.search(r["id"]):
            mark(f"ca{i}_r18", xr18, y, "dot", None, "pa")
    vf.IDS["pa"]["h"] = gc(cy + len(CIF) * LHS + 1.0 - 0.5)
    # ---------------- ImageNetV2 block: one strip panel, two columns (panel | same-recipe pairs)
    yb = vf.IDS["pa"]["y"] + vf.IDS["pa"]["h"] + 1.5
    cy = strip_panel("pb", "ImageNetV2", x0, yb, pw)
    lx = x0 + 1.5
    lw_ = max(tw([r["id"]], S) + (MK + 1.0 if r["role"] != "primary" or R18.search(r["id"]) else 0.0) for r in INP)
    rx = gc(lx + lw_ + 1.5)
    rw_ = max(tw([r["id"] + (", unpaired" if r.get("unpaired") else "")], S) for r in INQ) + MK + 1.0
    print("ImageNetV2 right column slack", round(XR - 1.5 - (gc(lx + lw_ + 1.5) + rw_), 2))
    if rx + rw_ > XR - 1.5 + 1e-6:
        raise SystemExit(f"ImageNetV2 columns need {rx + rw_ + 1.5:.2f} mm, the page ends at {XR}")
    T("pb_hl", lx, cy, ["robust CNN panel"], size=S, color="muted", cont="pb")
    T("pb_hr", rx, cy, ["same-recipe pairs"], size=S, color="muted", cont="pb")
    cy += LHS
    for i, r in enumerate(INP):
        y = cy + i * LHS
        w_ = tw([r["id"]], S)
        T(f"ib{i}", lx, y, [r["id"]], size=S, cont="pb")
        if r["role"] != "primary":
            mark(f"ib{i}_m", lx + w_ + 1.0, y, r["role"], hue(r["aile"]), "pb")
        if R18.search(r["id"]):
            mark(f"ib{i}_r18", lx + w_ + 1.0, y, "dot", None, "pb")
    for i, r in enumerate(INQ):
        y = cy + i * LHS
        if r["transformer"]:
            mark(f"ic{i}_m", rx, y, "triangle", None, "pb")
        else:                          # the CNN of a pair: an open square with a neutral edge
            vf.rect(f"ic{i}_m", gr(rx), gr(y + (LHS - MK) / 2), MK, MK, fill="FFFFFF", line=vf.C["muted"],
                    lw=vf.LW["normal"], role="mark", container="pb")
        T(f"ic{i}", rx + MK + 1.0, y, [r["id"] + (", unpaired" if r.get("unpaired") else "")], size=S, cont="pb")
    # the same-recipe pairs: a thin bracket in the column gap, opening toward each pair's two markers
    xb = rx - 0.75
    for j in range(len(PAIRS)):
        ya, yb2 = cy + 2 * j * LHS + LHS / 2, cy + (2 * j + 1) * LHS + LHS / 2
        lw = vf.LW["normal"]
        vf.seg(f"pair{j}_a", (xb + 0.5, ya), (xb, ya), vf.C["muted"], lw)
        vf.seg(f"pair{j}_b", (xb, ya), (xb, yb2), vf.C["muted"], lw)
        vf.seg(f"pair{j}_c", (xb, yb2), (xb + 0.5, yb2), vf.C["muted"], lw)
    n = max(len(INP), len(INQ))
    vf.IDS["pb"]["h"] = gc(cy + n * LHS + 1.0 - yb)
    # ---------------- key line (conventions)
    ky = yb + vf.IDS["pb"]["h"] + 1.0
    items = [("primary", vf.C["panel"], "primary"), ("secondary", vf.C["panel"], "secondary"),
             ("triangle", None, "transformer"), ("square", None, "its CNN")]   # the R18 dot is named by its column head
    x = x0 + 1.0
    for i, (kind, hexv, lab) in enumerate(items):
        if x + MK + 1.0 + tw([lab], S) > XR + 1e-6:          # wrap the key to a second line
            x, ky = x0 + 1.0, ky + LHS
        if kind == "square":
            vf.rect(f"key{i}", gr(x), gr(ky + (LHS - MK) / 2), MK, MK, fill="FFFFFF", line=vf.C["muted"],
                    lw=vf.LW["normal"], role="mark")
        else:
            mark(f"key{i}", x, ky, kind, hexv, None)
        T(f"key{i}_t", x + MK + 1.0, ky, [lab], size=S, color="muted")
        x = gc(x + MK + 1.0 + tw([lab], S) + 2.5)
    return gc(ky + LHS + 0.5)


def main():
    got = check_counts()
    h = lay()
    v = O.bitir(h, "Reference panels: which RobustBench models form the fixed CIFAR panels and the ImageNetV2 "
                   "panel, which are secondary, and the same-recipe CNN-transformer pairs.", KIND, 2,
                n_exempt="every member is drawn as one row", sablon="tasarim_izgarasi", hedef=HEDEF, tavan=TAVAN,
                extra={"denge_muafiyet": {
                    "karakter_cm2": "a membership table whose rows are model identifiers; the names are the content "
                                    "and replace about 330 words of section 3.6 (plan section 5)",
                    "yazi_kutusu_alani": "the 28 RobustBench model names are the figure's content; at the 8 pt floor "
                                         "each row needs its 4.0 mm line box"}})
    if v != "PASS":
        print("layout:", v, got)
        return 0
    deg = []
    for r in CIF:
        deg.append(O.ev(f"CIFAR row {r['id']}", {"c10": r["c10"], "c100": r["c100"], "aile": r["aile"]},
                        IC.HT10 if any(k.startswith("hucre_tablosu:") for k in r["keys"]) else IC.HT100,
                        "; ".join(r["keys"]) + " -> modeller.<m>.{birincil_panel, ikincil_panel, aile}",
                        "primary = birincil_panel, secondary = ikincil_panel; C100 keys in hucre_tablosu_b9.json"))
    for r in INP:
        deg.append(O.ev(f"ImageNetV2 panel row {r['id']}", {"rol": r["role"], "aile": r["aile"], "robustbench": r["rb"]},
                        IC.HT8, f"modeller.{r['key']}.{{birincil_panel, ikincil_panel, aile, kontrol_noktasi}}",
                        "row name = key without 'IN_'; RobustBench ID from kontrol_noktasi"))
    for r in INQ:
        deg.append(O.ev(f"ImageNetV2 pair row {r['id']}", {"cift": r["pair"], "aile": r["aile"], "robustbench": r["rb"]},
                        IC.J8 if r["pair"] else IC.HT8,
                        "b2.F_B2.K-a.ciftler" if r["pair"] else f"modeller.{r['key']} (not paired, not panel)",
                        "pairs in frozen order; unpaired = neither panel nor pair"))
    deg += [O.ev(f"count {k}", v_, IC.HT10 if "Cten" in k else IC.HT100 if "Chun" in k else IC.HT8,
                 "count over drawn rows", "equals _icerik_study_overview.sayilar() count, checked against the "
                                          "reference sheet") for k, v_ in got.items()]
    O.kanit_yaz(STEM, deg, foy=FOY, okunan=OKUNAN,
                ek={"r18_kurali": R18.pattern, "satir_sayisi": {"cifar": len(CIF), "in_panel": len(INP),
                                                                "in_cift": len(INQ)}},
                girdiler=[IC.HT10, IC.HT100, IC.HT8, IC.J8])
    O.denge_ajan(STEM, 0, {"3b_veri": (False, "this figure draws no 3D object and no data in depth"),
                           "3b_kural_disi": (False, "no 3D object is drawn in this figure at all"),
                           "gereksiz_ikon": (False, "markers code membership and are explained in the key"),
                           "dogrudan_etiket": (True, "every row carries its model name beside its markers"),
                           "panel_basina_bir_iddia": (True, "each panel lists the members of one data set's panel"),
                           "gercek_goruntu": ("uygulanmaz", "a membership chart shows no image")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
