#!/usr/bin/env python
"""Reference-panel members (fig:panel_members, Y2), style 8, Visio, one column, naming step 4 (strip).

    python paper/figures/visio/fig_panel_members.py --uslup 8 [--check]

Binding plan: raporlar/visio_2026-10-31/04_cizim_plani.md sections 5 and 9.4 (Y2 is its own one-column
figure; target 100 mm, ceiling 110 mm; template tasarim_izgarasi). Second version after the adversarial
check of 31.10.2026 (verifier findings RED-1 and YELLOW-5).

One symbol set for the whole figure, every channel read from a data field:
  shape  square = CNN, triangle = transformer         (cell table modeller.<m>.aile; 'CNN' or not)
  fill   filled = primary member, open = secondary    (modeller.<m>.{birincil_panel, ikincil_panel})
  hue    grey = robust CNN panel (#999999), purple = XCiT (#CC79A7), black = ImageNetV2 pair or
         unpaired model (descriptive members outside the panel)
  dot    ResNet-18 derivative, only where an architecture check exists: the CIFAR-10 primary panel,
         results/q1/konsey_ek_masa/a10_panel.json mimari_dogrulama.modeller.<m>.resnet18_turevi
         (reference sheet M12.3, table (a)). No such check exists for CIFAR-100 or ImageNet members,
         so the dot is not inferred from a name (the first version's regex missed Wong2020Fast,
         a PreActResNet-18).

Top panel: the CIFAR block, one row per RobustBench model in the union of the CIFAR-10 and CIFAR-100
panels, membership columns C10 and C100, ResNet-18 column R18. Bottom: the ImageNetV2 block in two
columns: the panel (six CNNs and the secondary XCiT-S12, marker column) and, on the right, the pairs
grouped by row: author, row ('IN-init.' for the ImageNet-initialized row, 'scratch' for the scratch
row, from results/q1/konsey_b8_imagenetv2/b8_betimsel.json ciftler[k].satir) and the shared name
suffix, then one line per pair (CNN, transformer), then the unpaired transformer.

Row names: the cell-table keys without the table prefixes 'C100_' and 'IN_'. Pair lines drop the
author (in the group heading) and a shared trailing name token when both names keep two tokens
('-CvSt' of the Singh pairs; Liu's '-B' is kept). The full RobustBench IDs are in the evidence file.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _sema_ortak as O  # noqa: E402
from _sema_ortak import vf, gr, gc, gf, lh, tw, T  # noqa: E402

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
A10 = "results/q1/konsey_ek_masa/a10_panel.json"
B8B = "results/q1/konsey_b8_imagenetv2/b8_betimsel.json"
MK = 2.25                          # marker side, mm
MG = 0.5                           # gap between the two markers of a pair line
ROW_WORD = {"IN": "IN-init.", "scr": "scratch"}   # b8_betimsel ciftler[k].satir -> printed row name


def strip_pre(k, pre):
    return k[len(pre):] if k.startswith(pre) else k


def split_name(short):
    """'Singh_ConvNeXt-T-CvSt' -> ('Singh', 'ConvNeXt-T-CvSt')."""
    a, _, m = short.partition("_")
    return a, m


def pair_label(m1, m2):
    """Drop shared trailing '-' tokens while both names keep at least two tokens."""
    t1, t2 = m1.split("-"), m2.split("-")
    suf = []
    while len(t1) > 2 and len(t2) > 2 and t1[-1] == t2[-1]:
        suf.insert(0, t1.pop())
        t2.pop()
    return "-".join(t1), "-".join(t2), "-".join(suf)


def rows_data():
    h10, h100, h8 = (K.dig(K.load_json(p), "modeller") for p in (IC.HT10, IC.HT100, IC.HT8))
    arch = K.dig(K.load_json(A10), "mimari_dogrulama.modeller")
    pairs = K.dig(K.load_json(IC.J8), "b2.F_B2.K-a.ciftler")
    bet = K.dig(K.load_json(B8B), "ciftler")
    cif = {}
    for tab, ds, pre in ((h10, "c10", ""), (h100, "c100", "C100_")):
        for k, v in tab.items():
            if not (v["birincil_panel"] or v["ikincil_panel"]):
                continue
            name = strip_pre(k, pre)
            r = cif.setdefault(name, {"id": name, "aile": v["aile"], "c10": None, "c100": None, "keys": [],
                                      "r18": None})
            r[ds] = "primary" if v["birincil_panel"] else "secondary"
            r["keys"].append(f"{'hucre_tablosu_b9' if ds == 'c100' else 'hucre_tablosu'}:{k}")
    p10 = {k for k, v in h10.items() if v["birincil_panel"]}
    if set(arch) != p10:
        raise SystemExit(f"architecture check {sorted(arch)} != CIFAR-10 primary panel {sorted(p10)}")
    for k, a in arch.items():
        cif[k]["r18"] = bool(a["resnet18_turevi"])
    order = {("primary", "primary"): 0, ("primary", None): 1, (None, "primary"): 2}
    names = list(cif)
    cif_rows = sorted(cif.values(), key=lambda r: (order.get((r["c10"], r["c100"]), 3), names.index(r["id"])))
    in_panel = [{"id": strip_pre(k, "IN_"), "key": k, "role": "primary" if v["birincil_panel"] else "secondary",
                 "aile": v["aile"], "rb": v["kontrol_noktasi"].split(" (")[0]}
                for k, v in h8.items() if v["birincil_panel"] or v["ikincil_panel"]]
    in_panel.sort(key=lambda r: r["role"] != "primary")
    # pairs: the frozen order of b8_dondurulmus_b2 K-a, the row from b8_betimsel (same order, checked)
    if [[b["cnn"], b["donusturucu"]] for b in bet] != [list(p) for p in pairs]:
        raise SystemExit("b8_betimsel ciftler and b8_dondurulmus_b2 K-a ciftler disagree")
    groups = []
    for j, (b, (cnn, tr)) in enumerate(zip(bet, pairs)):
        a1, m1 = split_name(strip_pre(cnn, "IN_"))
        a2, m2 = split_name(strip_pre(tr, "IN_"))
        if a1 != a2:
            raise SystemExit(f"pair {cnn} / {tr}: two authors")
        l1, l2, suf = pair_label(m1, m2)
        gkey = (a1, b["satir"], suf)
        if not groups or groups[-1]["key"] != gkey:
            groups.append({"key": gkey, "head": ", ".join(x for x in (a1, ROW_WORD[b["satir"]], suf) if x),
                           "lines": []})
        groups[-1]["lines"].append({"pair_no": b["cift"], "cnn": cnn, "tr": tr, "satir": b["satir"],
                                    "label": f"{l1}, {l2}", "aile": (h8[cnn]["aile"], h8[tr]["aile"]),
                                    "rb": (h8[cnn]["kontrol_noktasi"].split(" (")[0],
                                           h8[tr]["kontrol_noktasi"].split(" (")[0])})
    paired = {m for p in pairs for m in p}
    unp = [k for k, v in h8.items() if not (v["birincil_panel"] or v["ikincil_panel"]) and k not in paired]
    for k in unp:
        a, m = split_name(strip_pre(k, "IN_"))
        groups.append({"key": (a, "unpaired", ""), "head": f"{a}, unpaired",
                       "lines": [{"pair_no": None, "cnn": None, "tr": k, "satir": None, "label": m,
                                  "aile": (None, h8[k]["aile"]),
                                  "rb": (None, h8[k]["kontrol_noktasi"].split(" (")[0])}]})
    return cif_rows, in_panel, groups, pairs, unp, arch, bet


CIF, INP, GROUPS, PAIRS, UNP, ARCH, BET = rows_data()


def check_counts():
    """The drawn rows against the counts the reference sheet carries (via IC.sayilar)."""
    got = {"PanelCten": sum(1 for r in CIF if r["c10"] == "primary"),
           "PanelChun": sum(1 for r in CIF if r["c100"] == "primary"),
           "SecCten": sum(1 for r in CIF if r["c10"] == "secondary"),
           "SecChun": sum(1 for r in CIF if r["c100"] == "secondary"),
           "PanelIN": sum(1 for r in INP if r["role"] == "primary"),
           "SecIN": sum(1 for r in INP if r["role"] == "secondary"),
           "PairsIN": sum(1 for g in GROUPS for ln in g["lines"] if ln["pair_no"] is not None),
           "UnpairedIN": len(UNP)}
    bad = {k: (v, C[k]) for k, v in got.items() if v != C[k]}
    if bad:
        raise SystemExit(f"drawn rows disagree with the checked counts: {bad}")
    return got


def foy_checks():
    """Reference-sheet rows for the two facts this version adds: the ResNet-18 flag (M12.3 (a)) and
    the row of each ImageNetV2 pair (M10.4 pair table)."""
    foy = K.Foy()
    lo, hi = O.foy_bolum(foy, "### M12.3 ")
    for k, a in ARCH.items():
        n = O.foy_satiri_bul(foy, lo, hi, f"| {k} | ")
        if n is None:
            raise SystemExit(f"M12.3 has no row for {k}")
        foy.metin(f"R18 flag {k}", f"| {'evet' if a['resnet18_turevi'] else 'hayir'} |", n, f"| {k} | ")
    lo, hi = O.foy_bolum(foy, "### M10.4 ")
    for b in BET:
        n = O.foy_satiri_bul(foy, lo, hi, f"| {b['cift']} | {b['cnn']} | {b['donusturucu']} |")
        if n is None:
            raise SystemExit(f"M10.4 has no pair row for {b['cnn']}")
        foy.metin(f"pair {b['cift']} row", f"| {b['cnn']} | {b['donusturucu']} | {b['satir']} |", n,
                  f"| {b['cift']} | {b['cnn']} |")
    return foy.bitir()


def hue(r_aile, member_of_panel=True):
    if r_aile == "XCiT":
        return vf.C["xcit"]
    return vf.C["panel"] if member_of_panel else vf.C["ink"]


def mark(pid, x, y, aile, role, hexv, cont):
    """Square (CNN) or triangle (transformer); filled (primary) or open (secondary) in ``hexv``."""
    yy = gr(y + (LHS - MK) / 2)
    x0 = gr(x)
    filled = role == "primary"
    fill = hexv if filled else "FFFFFF"
    line = vf.C["muted"] if filled else hexv
    lw = vf.USLUP.line_min_pt if filled else vf.LW["vurgu"]
    if aile == "CNN":
        vf.rect(pid, x0, yy, MK, MK, fill=fill, line=line, lw=lw, role="mark", container=cont)
    else:
        vf.poly(pid, [(x0, yy + MK), (x0 + MK, yy + MK), (x0 + MK / 2, yy), (x0, yy + MK)], fill=fill,
                line=line, lw=lw, role="mark", container=cont)


def dot(pid, x, y, cont):
    d = 1.25
    vf.oval(pid, gr(x + (MK - d) / 2), gr(y + (LHS - d) / 2), d, d, fill=vf.C["ink"], line=None, role="mark",
            container=cont)


def lay():
    vf.reset(STEM, W, 140.0, naming_step=STEP, naming_kind="serit")
    x0 = 0.5
    pw = XR - x0
    # ---------------- CIFAR block: one row per model, membership columns
    cy = O.strip_panel("pa", "CIFAR-10 and CIFAR-100", x0, 0.5, pw, tone="zemin_bandi")
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
                mark(f"ca{i}_{ds}", xm, y, r["aile"], r[ds], hue(r["aile"]), "pa")
        if r["r18"]:
            dot(f"ca{i}_r18", xr18, y, "pa")
    vf.IDS["pa"]["h"] = gc(cy + len(CIF) * LHS + 1.0 - 0.5)
    # ---------------- ImageNetV2 block: panel column (left) and pairs by row (right)
    yb = vf.IDS["pa"]["y"] + vf.IDS["pa"]["h"] + 1.5
    cy = O.strip_panel("pb", "ImageNetV2", x0, yb, pw, tone="zemin_bandi")
    ty = vf.IDS["pb_title"]["y"]
    lx = x0 + 1.5
    xm = lx                                    # the panel's marker column, left of the names, so the
    nx = gc(xm + MK + 1.0)                     # grey panel markers never touch the pair markers
    rx = gc(nx + max(tw([r["id"]], S) for r in INP) + 1.25)         # right column: markers, then labels
    xl = gc(rx + 2 * MK + MG + 1.0)
    need = max([tw([ln["label"]], S) + xl for g in GROUPS for ln in g["lines"]] +
               [tw([g["head"]], S) + rx for g in GROUPS])
    print("ImageNetV2 right column slack", round(XR - 1.5 - need, 2))
    if need > XR - 1.5 + 1e-6:
        raise SystemExit(f"ImageNetV2 right column needs {need + 1.5:.2f} mm, the page ends at {XR}")
    for i, r in enumerate(INP):
        y = cy + i * LHS
        T(f"ib{i}", nx, y, [r["id"]], size=S, cont="pb")
        mark(f"ib{i}_m", xm, y, r["aile"], r["role"], hue(r["aile"]), "pb")
    y = ty                                     # the first group heading shares the strip title's line
    lines_r = 0
    for gi, g in enumerate(GROUPS):
        T(f"ig{gi}", rx, y, [g["head"]], size=S, color="muted", cont="pb")
        y = cy if gi == 0 else y + LHS
        for li, ln in enumerate(g["lines"]):
            if ln["cnn"]:
                mark(f"ig{gi}_{li}_c", rx, y, ln["aile"][0], "primary", hue(ln["aile"][0], False), "pb")
            mark(f"ig{gi}_{li}_t", rx + MK + MG, y, ln["aile"][1], "primary", hue(ln["aile"][1], False), "pb")
            T(f"ig{gi}_{li}", xl, y, [ln["label"]], size=S, cont="pb")
            y += LHS
            lines_r += 1
    bottom = max(cy + len(INP) * LHS, y)
    vf.IDS["pb"]["h"] = gc(bottom + 1.0 - yb)
    # ---------------- key (conventions), wrapped to the page width
    ky = yb + vf.IDS["pb"]["h"] + 1.0
    items = [("CNN", "primary", vf.C["panel"], "panel CNN"),
             ("CNN", "secondary", vf.C["panel"], "secondary CNN"),
             ("XCiT", "secondary", vf.C["xcit"], "XCiT, secondary"),
             ("pair", None, vf.C["ink"], "pair: CNN, transformer"),
             ("dot", None, None, "ResNet-18 variant (C10)")]
    x = x0 + 1.0
    for i, (aile, role, hexv, lab) in enumerate(items):
        sw = 2 * MK + MG if aile == "pair" else MK
        if x + sw + 1.0 + tw([lab], S) > XR + 1e-6:          # wrap the key to a new line
            x, ky = x0 + 1.0, ky + LHS
        if aile == "pair":
            mark(f"key{i}_c", x, ky, "CNN", "primary", hexv, None)
            mark(f"key{i}_tr", x + MK + MG, ky, "ViT", "primary", hexv, None)
        elif aile == "dot":
            dot(f"key{i}", x, ky, None)
        else:
            mark(f"key{i}", x, ky, aile, role, hexv, None)
        T(f"key{i}_lab", x + sw + 1.0, ky, [lab], size=S, color="muted")
        x = gc(x + sw + 1.0 + tw([lab], S) + 2.5)
    return gc(ky + LHS + 0.5)


def main():
    got = check_counts()
    foy2 = foy_checks()
    h = lay()
    v = O.bitir(h, "Reference panels: which RobustBench models form the fixed CIFAR panels and the ImageNetV2 "
                   "panel, which are secondary, which are ResNet-18 variants, and the ImageNetV2 CNN-transformer "
                   "pairs by row.", KIND, 2,
                n_exempt="every member is drawn as one row", sablon="tasarim_izgarasi", hedef=HEDEF, tavan=TAVAN,
                extra={"denge_muafiyet": {
                    "karakter_cm2": "a membership table whose rows are model identifiers; the names are the content "
                                    "and replace about 330 words of section 3.6 (plan section 5)",
                    "yazi_kutusu_alani": "the 28 RobustBench model names are the figure's content; at the 8 pt floor "
                                         "each row needs its 4.0 mm line box"},
                    "kodlama": {"shape": "square CNN, triangle transformer (modeller.<m>.aile)",
                                "fill": "filled primary, open secondary (birincil_panel / ikincil_panel)",
                                "hue": "grey robust CNN panel, purple XCiT, black ImageNetV2 pair or unpaired model",
                                "dot": "ResNet-18 derivative, CIFAR-10 primary panel only (a10_panel.json "
                                       "mimari_dogrulama, reference sheet M12.3)"}})
    if v != "PASS":
        print("layout:", v, got)
        return 0
    deg = []
    for r in CIF:
        deg.append(O.ev(f"CIFAR row {r['id']}", {"c10": r["c10"], "c100": r["c100"], "aile": r["aile"]},
                        IC.HT10 if any(k.startswith("hucre_tablosu:") for k in r["keys"]) else IC.HT100,
                        "; ".join(r["keys"]) + " -> modeller.<m>.{birincil_panel, ikincil_panel, aile}",
                        "primary = birincil_panel, secondary = ikincil_panel; C100 keys in hucre_tablosu_b9.json"))
        if r["r18"] is not None:
            deg.append(O.ev(f"R18 dot {r['id']}", r["r18"], A10,
                            f"mimari_dogrulama.modeller.{r['id']}.resnet18_turevi",
                            "dot drawn iff true; checked against reference sheet M12.3 table (a)"))
    for r in INP:
        deg.append(O.ev(f"ImageNetV2 panel row {r['id']}", {"rol": r["role"], "aile": r["aile"], "robustbench": r["rb"]},
                        IC.HT8, f"modeller.{r['key']}.{{birincil_panel, ikincil_panel, aile, kontrol_noktasi}}",
                        "row name = key without 'IN_'; RobustBench ID from kontrol_noktasi"))
    for g in GROUPS:
        for ln in g["lines"]:
            if ln["pair_no"] is not None:
                deg.append(O.ev(f"ImageNetV2 pair line '{ln['label']}' under '{g['head']}'",
                                {"cift": ln["pair_no"], "cnn": ln["cnn"], "donusturucu": ln["tr"],
                                 "satir": ln["satir"], "aile": list(ln["aile"]), "robustbench": list(ln["rb"])},
                                B8B, f"ciftler[{ln['pair_no'] - 1}].{{cift, cnn, donusturucu, satir}}",
                                "same pairs and order as b8_dondurulmus_b2.json b2.F_B2.K-a.ciftler; row word "
                                "IN -> 'IN-init.', scr -> 'scratch'; reference sheet M10.4 pair table"))
            else:
                deg.append(O.ev(f"ImageNetV2 unpaired line '{ln['label']}'",
                                {"model": ln["tr"], "aile": ln["aile"][1], "robustbench": ln["rb"][1]},
                                IC.HT8, f"modeller.{ln['tr']} (neither panel nor pair)", "unpaired = not panel, "
                                "not in b2.F_B2.K-a.ciftler"))
    deg += [O.ev(f"count {k}", v_, IC.HT10 if "Cten" in k else IC.HT100 if "Chun" in k else IC.HT8,
                 "count over drawn rows", "equals _icerik_study_overview.sayilar() count, checked against the "
                                          "reference sheet") for k, v_ in got.items()]
    foy = dict(FOY)
    foy["ayrinti"] = list(FOY["ayrinti"]) + list(foy2["ayrinti"])
    foy["karsilastirma_sayisi"] = len(foy["ayrinti"])
    O.kanit_yaz(STEM, deg, foy=foy, okunan=dict(OKUNAN, **{
                    A10: "mimari_dogrulama.modeller.<m>.resnet18_turevi",
                    B8B: "ciftler[k].{cift, cnn, donusturucu, satir}"}),
                ek={"satir_sayisi": {"cifar": len(CIF), "in_panel": len(INP),
                                     "in_cift_satiri": sum(len(g["lines"]) for g in GROUPS)},
                    "r18_kaynagi": f"{A10} mimari_dogrulama (CIFAR-10 primary panel only; no check exists for "
                                   "CIFAR-100 or ImageNet members, so no dot is drawn there)"},
                girdiler=[IC.HT10, IC.HT100, IC.HT8, IC.J8, A10, B8B])
    O.denge_ajan(STEM, 0, {"3b_veri": (False, "this figure draws no 3D object and no data in depth"),
                           "3b_kural_disi": (False, "no 3D object is drawn in this figure at all"),
                           "gereksiz_ikon": (False, "markers code architecture, membership and pairing, all in "
                                                    "the key"),
                           "dogrudan_etiket": (True, "every row carries its model name beside its markers"),
                           "panel_basina_bir_iddia": (True, "each panel lists the members of one data set's panel"),
                           "gercek_goruntu": ("uygulanmaz", "a membership chart shows no image")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
