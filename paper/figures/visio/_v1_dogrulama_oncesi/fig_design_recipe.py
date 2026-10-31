#!/usr/bin/env python
"""Design and training recipe (fig:design_recipe, Y1), style 8, Visio, one column, naming step 4 (strip).

    python paper/figures/visio/fig_design_recipe.py --uslup 8 [--check]

Binding plan: raporlar/visio_2026-10-31/04_cizim_plani.md section 9.2 (replaces Table 1; target 92 mm,
ceiling 100 mm; template tasarim_izgarasi, 3D model blocks in the cells). Top: the 2 x 2 design on a light
band, column heads 'scratch' and 'ImageNet init.', a row strip line per architecture (model and input
pipeline), one strip panel per cell with a 3D model block (front face = the entity hue: ViT-Tiny #D55E00,
ResNet-18 224 #0072B2) and the cell's initialisation, clean stage and seeds. Below: the C1-R32 bridge cell
(#56B4E9 block), then a letterless conventions strip with the AT recipe shared by the cells.

Every value comes from results/q1/konsey_b3_tarif.json (key paths in the evidence file), whose rows are
compared with the reference sheet section M13.1 (tables a-c) and the seeds with M9.1 (lines 1452-1457) and
the cell definitions (line 1443); one mismatch stops the figure. The 7x7 stem of the timm ResNet-18 is read
from src/models/r224.py (its docstring line), the 3x3 stem of the CIFAR ResNet-18 from the JSON. ViT-Tiny's
depth, width and heads (12, 192, 3) are not in any data file of the paper and are not drawn.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _sema_ortak as O  # noqa: E402
from _sema_ortak import vf, bl, gr, gc, gf, lh, tw, T, TW, yuz_tonlari  # noqa: E402
from _yuz_tonlari import notr_kenar  # noqa: E402

O.baslat()
K = O.K
STEM = "design_recipe"
KIND = "single"
STEP = 4
HEDEF, TAVAN = 92.0, 100.0
S = vf.SMALL
LHS = lh(S)
W = vf.page_width(KIND)
XR = gf(W - 0.5)
SRC = "results/q1/konsey_b3_tarif.json"
R224_PY = "src/models/r224.py"
D = K.load_json(SRC)
H = D["hucreler"]
FOY = K.Foy()
DEG, OKUNAN = [], {}


def get(path):
    """Read a key path of the recipe JSON and record it for the evidence file."""
    v = K.dig(D, path)
    OKUNAN[path] = v if not isinstance(v, (dict, list)) or len(str(v)) < 120 else "(structure)"
    return v


def first_run(cell):
    return next(iter(H[cell]["kosular"]))


def stage(cell, st, key):
    return get(f"hucreler.{cell}.kosular.{first_run(cell)}.{st}.{key}")


def num(v):
    return f"{v:g}" if isinstance(v, float) else str(v)


def stem_r224():
    """'7x7 stem' from the docstring of the timm ResNet-18 wrapper (src/models/r224.py)."""
    lines = Path(R224_PY).read_text(encoding="utf-8").splitlines()
    for i, t in enumerate(lines, 1):
        m = re.search(r"(\d+)x(\d+) stem", t)
        if m and "resnet18" in t:
            return f"{m.group(1)}×{m.group(2)}", i
    raise SystemExit(f"{R224_PY}: no 'NxN stem' line")


def stem_r32():
    m = re.search(r"\((\d+)x(\d+) kok, maxpool yok\)", get("hucreler.C1-R32.girdi_hatti.model"))
    if not m:
        raise SystemExit("C1-R32 model string has no '(NxN kok, maxpool yok)'")
    return f"{m.group(1)}×{m.group(2)}"


# ------------------------------------------------------------------ reference sheet comparisons
def foy_checks():
    a, b = O.foy_bolum(FOY, "### M13.1")
    for cell in ("V-scr", "V-IN", "R224-scr", "R224-IN", "C1-R32"):
        seeds = ", ".join(str(s) for s in get(f"hucreler.{cell}.tohumlar"))
        n = O.foy_satiri_bul(FOY, a, b, f"| {cell} | ", seeds)
        FOY.metin(f"M13.1(a) {cell} seeds", seeds, n or a, f"| {cell} | ")
        ep, opt = stage(cell, "temiz", "epok_bayragi"), stage(cell, "temiz", "eniyileyici_eniyileyici")
        lr, wd = stage(cell, "temiz", "eniyileyici_lr_etkin"), stage(cell, "temiz", "eniyileyici_agirlik_azaltma")
        row = f"| {cell} | {ep} | {opt} | {num(lr)} | {num(wd)} |"
        n = O.foy_satiri_bul(FOY, a, b, row)
        FOY.metin(f"M13.1(b) {cell} clean", row, n or a, f"| {cell} | ")
        cap = stage(cell, "AT", "epok_tavani") if "epok_tavani" in H[cell]["kosular"][first_run(cell)]["AT"] \
            else stage(cell, "AT", "epok_bayragi")
        at = [cap, f"cosine (T_max {stage(cell, 'AT', 'lr_cizelgesi')['T_max_epok']})", stage(cell, "AT", "sabir"),
              stage(cell, "AT", "eniyileyici_eniyileyici"), num(stage(cell, "AT", "eniyileyici_lr_etkin")),
              num(stage(cell, "AT", "eniyileyici_agirlik_azaltma"))]
        row = f"| {cell} | " + " | ".join(str(x) for x in at) + " |"
        n = O.foy_satiri_bul(FOY, a, b, row)
        FOY.metin(f"M13.1(c) {cell} AT", row, n or a, f"| {cell} | ")
        row2 = (f"| {stage(cell, 'AT', 'batch')} | {stage(cell, 'AT', 'eps_ifade')} | "
                f"{stage(cell, 'AT', 'alpha_ifade')} | {stage(cell, 'AT', 'pgd_adim')} |")
        n = O.foy_satiri_bul(FOY, a, b, f"| {cell} | ", row2)
        FOY.metin(f"M13.1(c) {cell} AT batch/eps/alpha/steps", row2, n or a, f"| {cell} | ")
    # M9.1: seeds of the six B3 runs (lines 1452-1457) and the cell definitions (line 1443)
    for cell in ("V-IN", "R224-scr", "R224-IN"):
        for run, kos in H[cell]["kosular"].items():
            s = kos["temiz"]["tohum"]
            n = O.foy_satiri_bul(FOY, 1446, 1489, f"| {run} | {cell} | {s} |")
            FOY.metin(f"M9.1 {run} seed", f"| {run} | {cell} | {s} |", n or 1446, f"| {run} |")
    FOY.metin("cell definitions (line 1443)", "C1-R32: " + get("hucreler.C1-R32.hucre_tablosu_tanimi"), 1443,
              "Hucre tanimlari")
    FOY.metin("M13.1 common: mix ratio and min_delta",
              f"mix_ratio {num(get('ortak.at_kaybi.mix_ratio'))}", *_line_with(a, b, "Ortak (`ortak`)"))
    FOY.metin("M13.1 common: validation n", f"n {get('ortak.veri.dogrulama_n')}", *_line_with(a, b, "Ortak (`ortak`)"))
    FOY.metin("M13.1 common: pilot cap", f"pilot secilen tavan {get('ortak.at_tavani_pilot.secilen_tavan')}",
              *_line_with(a, b, "Ortak (`ortak`)"))
    return FOY.bitir(), (a, b)


def _line_with(a, b, anchor):
    n = O.foy_satiri_bul(FOY, a, b, anchor)
    return (n or a), anchor


# ------------------------------------------------------------------ drawing
def block(pid, x, y, ent, cont):
    with yuz_tonlari(ent) as tint:
        return notr_kenar(bl.iso_box(pid, gr(x), gr(y), 6.0, 4.0, 7.0, tint, container=cont))


def seeds_txt(seeds):
    """'2001-2003' for consecutive seeds, else the list (the JSON list is in the evidence)."""
    if len(seeds) > 1 and seeds == list(range(seeds[0], seeds[0] + len(seeds))):
        return f"{seeds[0]}–{seeds[-1]}"
    return ", ".join(str(x) for x in seeds)


def cell_lines(cell):
    init = get(f"hucreler.{cell}.girdi_hatti.baslatma")
    ep, lr = stage(cell, "temiz", "epok_bayragi"), stage(cell, "temiz", "eniyileyici_lr_etkin")
    blok = get(f"hucreler.{cell}.blok").split(" ")[0]
    return {"title": f"{cell}, {blok}", "init": None if init == "rastgele" else init,
            "clean": f"{ep} ep, lr {num(lr)}", "seeds": "seeds " + seeds_txt(get(f"hucreler.{cell}.tohumlar"))}


def lay():
    vf.reset(STEM, W, 140.0, naming_step=STEP, naming_kind="serit")
    x0 = 0.5
    f, _ = vf.tint_of("zemin_bandi")
    vf.rect("band", x0, 0.5, gf(XR - x0), 10.0, fill=f, line=None, role="container", ctype="band")
    gap = 1.5
    cw = gf((XR - x0 - 2 * 1.0 - gap) / 2)
    cx = [x0 + 1.0, x0 + 1.0 + cw + gap]
    y = 0.5 + 0.5
    for c, lab in enumerate(("scratch (random init.)", "ImageNet init.")):
        T(f"colh{c}", cx[c] + 1.25, y, [[(lab, "sb")]], size=S, color="muted", cont="band")
    y += LHS
    T("cellkey", cx[0] + 1.25, y, ["in each cell: clean stage (epochs, lr) and seeds"], size=S, color="muted",
      cont="band")
    y += LHS
    stem7, stem7_line = stem_r224()
    rows = [("ViT-Tiny", "vit", ("V-scr", "V-IN")), ("ResNet-18", "r224", ("R224-scr", "R224-IN"))]
    for r, (arch, ent, cells) in enumerate(rows):
        model = get(f"hucreler.{cells[0]}.girdi_hatti.model")
        inp = get(f"hucreler.{cells[0]}.girdi_hatti.girdi").replace("->", "→").replace(" bilinear buyutme", "")
        extra = f", {stem7} stem" if ent == "r224" else ""
        T(f"rowh{r}", cx[0] + 1.25, y, [[(arch + ": ", "sb"), (f"{model}{extra}, input {inp}", "r")]], size=S,
          cont="band")
        y += LHS
        ids, tops = [], []
        for c, cell in enumerate(cells):
            L = cell_lines(cell)
            pid = f"c{r}{c}"
            top = O.strip_panel(pid, L["title"], cx[c], y, cw, cont="band")
            ids.append(pid)
            rec = block(f"{pid}_b", cx[c] + 1.5, top + 0.25, ent, pid)
            bx, by, bw_, bh_ = rec["bbox_mm"]
            tx = gc(bx + bw_ + 1.25)
            room = cx[c] + cw - 1.5 - tx
            h1 = TW(f"{pid}_clean", tx, top, L["clean"], room, size=S, cont=pid)
            h2 = TW(f"{pid}_seed", tx, top + h1, L["seeds"], room, size=S, cont=pid)
            yy = max(by + bh_ + 0.5, top + h1 + h2)
            if L["init"]:
                yy += TW(f"{pid}_init", cx[c] + 1.5, yy, L["init"].replace(".", " .", 1) if
                         tw([L["init"]], S) > cw - 3.0 else L["init"], cw - 3.0, size=S, color="muted", cont=pid)
            tops.append(yy + 1.0)
        hh = gc(max(tops) - y)
        for pid in ids:
            vf.IDS[pid]["h"] = hh
        bl.title_strip(ids)
        y = y + hh + 0.75
    vf.IDS["band"]["h"] = gc(y - 0.5)
    # ---------------- the C1-R32 bridge cell
    yb = 0.5 + vf.IDS["band"]["h"] + 1.0
    cell = "C1-R32"
    L = cell_lines(cell)
    top = O.strip_panel("br", f"C1-R32 bridge, {L['seeds']}", x0, yb, XR - x0)
    rec = block("br_b", x0 + 1.5, top + 0.25, "r32", "br")
    bx, by, bw_, bh_ = rec["bbox_mm"]
    tx = gc(bx + bw_ + 1.25)
    room = XR - 1.5 - tx
    s32 = stem_r32()
    inp = get("hucreler.C1-R32.girdi_hatti.girdi").split(" ")[0]
    clean = (f"clean: {stage(cell, 'temiz', 'epok_bayragi')} ep, {stage(cell, 'temiz', 'eniyileyici_eniyileyici')} "
             f"lr {num(stage(cell, 'temiz', 'eniyileyici_lr_etkin'))}, momentum "
             f"{num(stage(cell, 'temiz', 'eniyileyici_momentum'))}")
    atl = (f"AT: {stage(cell, 'AT', 'eniyileyici_eniyileyici')} lr {num(stage(cell, 'AT', 'eniyileyici_lr_etkin'))}, "
           f"batch {stage(cell, 'AT', 'batch')}, cap {stage(cell, 'AT', 'epok_bayragi')} ep")
    h = 0.0
    for i, txt in enumerate((f"ResNet-18, {s32} stem, no max-pool, {inp}", clean, atl)):
        h += TW(f"br_t{i}", tx, top + h, txt, room, size=S, cont="br")
    vf.IDS["br"]["h"] = gc(max(by + bh_, top + h) + 1.0 - yb)
    # ---------------- conventions strip: the AT recipe the cells share
    ys = yb + vf.IDS["br"]["h"] + 1.0
    c = "V-IN"
    mix = get("ortak.at_kaybi.mix_ratio")
    items = [[(f"PGD-{stage(c, 'AT', 'pgd_adim')}, ε {stage(c, 'AT', 'eps_ifade')}, α {stage(c, 'AT', 'alpha_ifade')}, "
               f"mix {num(mix)}", "r")],
             [(f"{stage(c, 'AT', 'eniyileyici_eniyileyici')} lr {num(stage(c, 'AT', 'eniyileyici_lr_etkin'))}, "
               f"wd {num(stage(c, 'AT', 'eniyileyici_agirlik_azaltma'))}, batch {stage(c, 'AT', 'batch')}", "r")],
             [(f"patience {stage(c, 'AT', 'sabir')}, cap {stage(c, 'AT', 'epok_tavani')} ep "
               f"(V-scr {stage('V-scr', 'AT', 'epok_bayragi')})", "r")]]
    hs = bl.legend_strip("at", "AT", x0, gr(ys), gf(XR - x0), items, cols=1)
    return gc(ys + hs + 0.75), stem7_line


def main():
    foy, (a, b) = foy_checks()
    h, stem7_line = lay()
    v = O.bitir(h, "The two-by-two design (architecture by initialisation) and the bridge cell, with each cell's "
                   "initialisation, clean stage and seeds, and the adversarial-training recipe they share.",
                KIND, 6, n_exempt="the recipe figure draws no sample size", sablon="tasarim_izgarasi",
                hedef=HEDEF, tavan=TAVAN,
                extra={"denge_muafiyet": {
                    "karakter_cm2": "the figure replaces Table 1; each cell's training settings are its content "
                                    "and every value is read from the recipe file",
                    "yazi_kutusu_alani": "the settings of five cells and the shared adversarial recipe are text "
                                         "by nature; the 8 pt floor fixes their line boxes"}})
    if v != "PASS":
        print("layout:", v, "| foy:", foy["karsilastirma_sayisi"], foy["uyusmayan"])
        return 0
    for path, val in OKUNAN.items():
        if val != "(structure)":
            DEG.append(O.ev(path, val, SRC, path, "read as is; formatted with :g"))
    DEG.append(O.ev("timm ResNet-18 stem", "7x7", R224_PY, f"line {stem7_line} (docstring, 'NxN stem')",
                    "regex (\\d+)x(\\d+) stem on the timm resnet18 wrapper's docstring"))
    O.kanit_yaz(STEM, DEG, foy=foy, okunan={SRC: sorted(OKUNAN), R224_PY: f"line {stem7_line}"},
                ek={"foy_M13_1_satirlari": [a, b], "cizilmeyen": "ViT-Tiny depth/width/heads (12, 192, 3): "
                                                                "no data file of the paper carries them"},
                girdiler=[SRC, R224_PY])
    O.denge_ajan(STEM, 0, {"3b_veri": (False, "the 3D blocks stand for models, no data value is drawn in depth"),
                           "dogrudan_etiket": (True, "every cell names its model, initialisation, schedule and seeds"),
                           "panel_basina_bir_iddia": (True, "each cell panel states one training recipe"),
                           "gercek_goruntu": ("uygulanmaz", "a training recipe shows no data image"),
                           "her_sayinin_kaynagi": (True, "every number is a key of the recipe JSON, checked against "
                                                         "the reference sheet")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
