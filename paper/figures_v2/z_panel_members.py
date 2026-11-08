#!/usr/bin/env python
"""z_panel_members (Fig. 4 v2, Üslup Z): the reference panel members as books on two shelves.

    python paper/figures_v2/z_panel_members.py [--check] [--bak]

Single column. Every panel member is a book lying in a stack, its spine (an upright face of the one dimetric view)
carrying the RobustBench identifier and its marks. Front shelf: the CIFAR-10 and CIFAR-100 block, roles in the C10
and C100 columns (filled square primary, open square secondary, triangle transformer) and the ResNet-18 dot in
the R18 column. Back shelf, higher: the ImageNetV2 block, the CNN panel and the secondary XCiT-S12, the three
pairs with their group heading on the spine (CNN and transformer marks) and the unpaired ViT-B. Depth carries the
registration level (CIFAR, main registration, in front; ImageNetV2, addendum, behind). Book length carries nothing.
Content: the v1 rule paper/figures/visio/fig_panel_members.py (cell tables, a10_panel.json, b8_betimsel.json;
sheet M12.3 and M10.4). Naming: step 4 (shelf titles and column heads).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
PM = Z.yukle_sema("paper/figures/visio/fig_panel_members.py", "v1_panel_members")
IC = PM.IC

STEM = "z_panel_members"
KIND = "single"
W = vf.page_width(KIND)
CAPTION = ("Reference panel members on two catalogue cards. The front card, CIFAR-10 and CIFAR-100, gives each "
           "RobustBench identifier its role in the C10 and C100 columns and marks ResNet-18 variants in the R18 "
           "column. The back card, ImageNetV2, holds the CNN panel and the secondary XCiT-S12, the transformer "
           "pairs and the unpaired ViT-B of Mo et al.")


def mark(pid, x, y, aile, role, tone, group):
    shape = "s" if aile == "CNN" else "^"
    col = vf.C[tone] if tone in vf.C else tone
    Z.isaret(pid, x, y, shape, fill=col if role == "primary" else None, edge=Z.soft(col, 0.3) if role == "primary"
             else Z.soft(col, 0.5), size=2.1, group=group)


def main():
    got = PM.check_counts()
    foy2 = PM.foy_checks()
    vf.reset(STEM, W, 160.0, naming_step=4, naming_kind="serit")
    LH = lh(Z.S8)
    CWd = W - 9.0
    SHT = 2.0
    nC = len(PM.CIF)
    left = list(PM.INP)
    right = []
    for g in PM.GROUPS:
        right.append(("head", g))
        for ln in g["lines"]:
            right.append(("line", (g, ln)))
    nI = max(len(left), len(right))
    HC = 1.0 + LH + 0.8 + nC * LH + 1.0
    HI = 1.0 + LH + 0.8 + nI * LH + 1.0
    DB = 10.0
    OY = 3.0 + HI + SHT + 3.6 + HC + SHT + 1.0
    S = Z.Sahne(2.0, OY)
    tone_cnn, tone_x, tone_pair = "vurgu6", "vurgu4", "vurgu1"
    deg = []
    # ---- front shelf and the CIFAR catalogue card
    X, Y = Z.un(S, 0.4, -3.0)
    Z.kart(S, "shelfC", X, Y, 0.0, CWd + 2.0, SHT, "govde_res", t=9.0, shadow=False, group="shelfC")
    X, Y = Z.un(S, 0.5, 1.0)
    fx, fy, fw, fh = Z.kart(S, "cardC", X, Y, SHT, CWd, HC, "kutu", t=1.4, shadow=False, group="cardC", cont="shelfC_top")
    face = "cardC_face"
    xcol = {"c10": fw - 19.5, "c100": fw - 11.5, "r18": fw - 3.8}
    T("hC", fx + 1.2, fy + 1.0, [[("CIFAR-10 and CIFAR-100", "sb")]], size=Z.S8, cont=face)
    for key, lab in (("c10", "C10"), ("c100", "C100"), ("r18", "R18")):
        T(f"hc_{key}", fx + xcol[key], fy + 1.0, [lab], size=Z.S8, align="c", color="muted", cont=face)
    for i, r in enumerate(PM.CIF):
        y = fy + 1.0 + LH + 0.8 + i * LH
        T(f"cn{i}", fx + 1.2, y, [r["id"]], size=Z.S8, cont=face)
        for key in ("c10", "c100"):
            if r[key]:
                mark(f"cm{i}{key}", fx + xcol[key], y + LH / 2, r["aile"], r[key],
                     tone_cnn if r["aile"] == "CNN" else tone_x, f"cr{i}")
        if r["r18"]:
            Z.isaret(f"cd{i}", fx + xcol["r18"], y + LH / 2, "o", fill="ink", edge="ink", size=1.1, group=f"cr{i}")
    # ---- back shelf, higher, and the ImageNetV2 card
    zb = SHT + HC + 3.6 - DB * 0.664
    X, Y = Z.un(S, -0.6, DB - 3.0)
    Z.kart(S, "shelfI", X, Y, zb, CWd + 1.6, SHT, "govde_res", t=9.0, shadow=False, group="shelfI")
    X, Y = Z.un(S, 0.5, DB + 1.0)
    gx, gy, gw, gh = Z.kart(S, "cardI", X, Y, zb + SHT, CWd, HI, "kutu", t=1.4, shadow=False, group="cardI",
                            cont="shelfI_top")
    face = "cardI_face"
    T("hI", gx + 1.2, gy + 1.0, [[("ImageNetV2", "sb")]], size=Z.S8, cont=face)
    xr = gx + 41.6
    for i, r in enumerate(left):
        y = gy + 1.0 + LH + 0.8 + i * LH
        mark(f"im{i}", gx + 2.4, y + LH / 2, r["aile"], r["role"], tone_cnn if r["aile"] == "CNN" else tone_x, f"ir{i}")
        T(f"in{i}", gx + 4.4, y, [r["id"].replace("Debenedetti2022Light_", "Debenedetti_")], size=Z.S8, cont=face)
    for i, (kind_, item) in enumerate(right):
        y = gy + 1.0 + (i if kind_ == "head" or i else 0) * LH
        y = gy + 1.0 + i * LH
        if kind_ == "head":
            T(f"rh{i}", xr, y, [item["head"]], size=Z.S8, color="muted", cont=face)
        else:
            g, ln = item
            if ln["pair_no"] is not None:
                mark(f"rm{i}a", xr + 1.2, y + LH / 2, "CNN", "primary", tone_pair, f"rr{i}")
            mark(f"rm{i}b", xr + 3.8, y + LH / 2, "T", "primary", tone_pair, f"rr{i}")
            T(f"rl{i}", xr + 5.6, y, [ln["label"]], size=Z.S8, cont=face)
    # legend under the front shelf
    yl = OY + 3.8
    items = [("s", tone_cnn, "primary", "panel CNN"), ("s", tone_cnn, "secondary", "secondary CNN"),
             ("^", tone_x, "secondary", "XCiT, secondary")]
    x = 1.0
    for j, (mk, tn, role, lab) in enumerate(items):
        mark(f"lg{j}", x + 1.2, yl + LH / 2, "CNN" if mk == "s" else "T", role, tn, f"lg{j}")
        T(f"lgt{j}", x + 2.8, yl, [lab], size=Z.S8)
        x += 2.8 + Z.tw([lab], Z.S8) + 2.2
    yl += LH + 0.4
    mark("lgp1", 2.2, yl + LH / 2, "CNN", "primary", tone_pair, "lgp")
    mark("lgp2", 4.8, yl + LH / 2, "T", "primary", tone_pair, "lgp")
    T("lgpt", 6.6, yl, ["pair: CNN, transformer"], size=Z.S8)
    xx = 6.6 + Z.tw(["pair: CNN, transformer"], Z.S8) + 3.0
    Z.isaret("lgd", xx + 0.8, yl + LH / 2, "o", fill="ink", edge="ink", size=1.1)
    T("lgdt", xx + 2.2, yl, ["ResNet-18 variant (C10)"], size=Z.S8)
    for _pid in ["hC", "hI"]:          # the panel titles are the strips of naming step 4
        vf.note_naming(_pid, "strip")
    Z.sayfa_sigdir()
    for r in PM.CIF:
        deg.append(Z.ev(f"CIFAR row {r['id']}", {"c10": r["c10"], "c100": r["c100"], "aile": r["aile"]},
                        IC.HT10 if any(k.startswith("hucre_tablosu:") for k in r["keys"]) else IC.HT100,
                        "; ".join(r["keys"]) + " -> modeller.<m>.{birincil_panel, ikincil_panel, aile}",
                        "primary = birincil_panel, secondary = ikincil_panel"))
        if r["r18"] is not None:
            deg.append(Z.ev(f"R18 dot {r['id']}", r["r18"], PM.A10, f"mimari_dogrulama.modeller.{r['id']}.resnet18_turevi",
                            "dot drawn iff true; == foy M12.3 table (a)"))
    for r in PM.INP:
        deg.append(Z.ev(f"ImageNetV2 panel row {r['id']}", {"rol": r["role"], "aile": r["aile"], "robustbench": r["rb"]},
                        IC.HT8, f"modeller.{r['key']}.{{birincil_panel, ikincil_panel, aile, kontrol_noktasi}}", "read"))
    for g in PM.GROUPS:
        for ln in g["lines"]:
            if ln["pair_no"] is not None:
                deg.append(Z.ev(f"ImageNetV2 pair '{ln['label']}' under '{g['head']}'",
                                {"cift": ln["pair_no"], "cnn": ln["cnn"], "donusturucu": ln["tr"], "satir": ln["satir"]},
                                PM.B8B, f"ciftler[{ln['pair_no'] - 1}].{{cift, cnn, donusturucu, satir}}",
                                "foy M10.4 pair table"))
            else:
                deg.append(Z.ev(f"ImageNetV2 unpaired '{ln['label']}'", {"model": ln["tr"]}, IC.HT8,
                                f"modeller.{ln['tr']}", "neither panel nor pair"))
    deg += [Z.ev(f"count {k}", v_, IC.HT10 if "Cten" in k else IC.HT100 if "Chun" in k else IC.HT8,
                 "count over drawn rows", "== _icerik_study_overview.sayilar(), checked against the sheet")
            for k, v_ in got.items()]
    foy = dict(PM.FOY)
    foy["ayrinti"] = list(PM.FOY["ayrinti"]) + list(foy2["ayrinti"])
    ents = {"panel": "#" + vf.C[tone_cnn]}
    return Z.bitir(
        STEM, message="The reference panels list every RobustBench member with its role; ImageNetV2 adds paired "
                      "CNN and transformer models.", kind=KIND, panels=2, caption=CAPTION, sablon="tablodan_sekle",
        tur="sematik", degerler=deg, kanit_ek={"foy_karsilastirmasi": foy},
        manifest={"entities": ents, "sahne_kalibi": "kitaplik",
                  "panel_adlari": ["CIFAR-10 and CIFAR-100", "ImageNetV2"],
                  "derinlik_ekseni": "registration level: CIFAR (main) in front, ImageNetV2 (addendum) behind",
                  "denge_muafiyet": {"karakter_cm2": "the figure lists the panel members by their full RobustBench "
                                                     "identifiers, read from the cell tables; the names are its content",
                                     "yazi_kutusu_alani": "one line per panel member at the 8 pt floor; the list replaces "
                                                          "a table and its line boxes are fixed by the floor"}},
        denge={"panel_basina_bir_iddia": (True, "each shelf is one data block of panel members")},
        n_exempt_reason="every member is one book; the counts are in the evidence file",
        okunan_ek=[IC.HT10, IC.HT100, IC.HT8, PM.A10, PM.B8B])


if __name__ == "__main__":
    sys.exit(main())
