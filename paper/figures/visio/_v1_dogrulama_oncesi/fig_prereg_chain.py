#!/usr/bin/env python
"""Pre-registration chain (fig:prereg_chain, Y5), style 8, Visio, full width (double), naming step 2 (flow).

    python paper/figures/visio/fig_prereg_chain.py --uslup 8 [--check]

Binding plan: raporlar/visio_2026-10-31/04_cizim_plani.md section 9.6 (replaces section 3.10 text; target
60 mm, ceiling 66 mm; the top band of the style's yontem_semasi template and its 7 mm strip; sayim_akisi is
not available in style 8). The band holds three panels joined by labelled thin arrows: data seen before
registration; the main registration (frozen 29 Oct 2026) and blocks B2-B6; the supplementary registration
(frozen 30 Oct 2026) and blocks B8-B10. Each arrow carries the freeze date, the commit and, for the main
registration, the SHA-256 prefix of its body (reference sheet M9.8). Every block prints its models, images
and matrix cells. The strip below names the two post hoc entries of the deviation log.

Sources: results/q1/konsey_zaman_cizelgesi.json (dondurma, matrisler, B3_asamalari, egitim_suresi,
sapma_kaydi_basliklari, kayit_oncesi_gorulen_veriler), compared with the reference sheet sections M13.3
(tables a-c), M9.1 (line 1470, training hours) and M9.8 (registration body SHA-256). The '3x3' and '8x8' of
the seen data are read from the registration's own section 1 (ON_KAYIT_2026-10-29.md, the line the JSON names).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _sema_ortak as O  # noqa: E402
from _sema_ortak import vf, bl, gr, gc, gf, lh, tw, T, TW  # noqa: E402

O.baslat()
K = O.K
STEM = "prereg_chain"
KIND = "double"
STEP = 2
HEDEF, TAVAN = 60.0, 66.0
S = vf.SMALL
LHS = lh(S)
W = vf.page_width(KIND)
XR = gf(W - 0.5)
SRC = "results/q1/konsey_zaman_cizelgesi.json"
D = K.load_json(SRC)
FOY = K.Foy()
OKUNAN = {}
MONTH = {"10": "Oct"}


def get(path):
    v = K.dig(D, path)
    OKUNAN[path] = v if not isinstance(v, (dict, list)) else "(structure)"
    return v


def mx(block, key):
    return get(f"matrisler.{block}.{key}")


def date_of(utc):
    y, m, d = utc[:10].split("-")
    return f"{int(d)} {MONTH.get(m, m)}"          # the year (2026) is in the caption


def seen_sizes():
    """'3x3' and '8x8' matrices named in the registration's section 1 (the line range the JSON names)."""
    ref = get("kayit_oncesi_gorulen_veriler.ana")
    path, rng = ref.rsplit(":", 1)
    a, b = (int(x) for x in rng.split("-"))
    lines = Path(path).read_text(encoding="utf-8").splitlines()[a - 1:b]
    txt = "\n".join(lines)
    m3 = re.search(r"C1 çiftlerinin (\d+)x(\d+) matrisleri", txt)
    m8 = re.search(r"tek tohumlu (\d+)x(\d+) matrisi", txt)
    if not (m3 and m8):
        raise SystemExit(f"{ref}: the seen-data sentence changed")
    n3 = next(a + i for i, t in enumerate(lines) if m3.group(0) in t)
    return f"{m3.group(1)}×{m3.group(2)}", f"{m8.group(1)}×{m8.group(2)}", path, n3


def body_sha():
    """SHA-256 of the main registration body from the reference sheet M9.8 (row of ON_KAYIT ... govdesi)."""
    a, b = O.foy_bolum(FOY, "### M9.8")
    n = O.foy_satiri_bul(FOY, a, b, "ON_KAYIT_2026-10-29.md` govdesi")
    if not n:
        raise SystemExit("M9.8: no registration-body row")
    h = re.findall(r"\b[0-9a-f]{64}\b", FOY.lines[n - 1])
    if not h or len(set(h)) != 1 or "UYUSUYOR" not in FOY.lines[n - 1]:
        raise SystemExit(f"M9.8 line {n}: body SHA-256 not unique or not UYUSUYOR")
    FOY.metin("M9.8 body SHA-256 row agrees", "UYUSUYOR", n, "govdesi")
    return h[0], n


def foy_checks():
    a, b = O.foy_bolum(FOY, "### M13.3")
    for key, lab in (("on_kayit", "On kayit dondurma"), ("ek_on_kayit", "Ek on kayit dondurma")):
        c = get(f"dondurma.{key}.commit")[:7]
        u = get(f"dondurma.{key}.utc").replace("T", " ")[:19]
        n = O.foy_satiri_bul(FOY, a, b, f"| {lab} (commit {c}) |")
        FOY.metin(f"M13.3(a) {lab}", f"| {u} |", n or a, f"(commit {c})")
    rows = {"B2": "| B2 | pgd |", "B4": "| B4 | pgd |", "B5-MI": "| B5-MI | mi |", "B5-TGR": "| B5-TGR | tgr |",
            "B9": "| B9 | pgd |", "B8": "| B8 | pgd |"}
    for blk, anchor in rows.items():
        frag = (f"| {mx(blk, 'n_goruntu')} | {mx(blk, 'model_sayisi')} | {mx(blk, 'hucre_sayisi')} | "
                f"{mx(blk, 'eps_x255'):g} |")
        n = O.foy_satiri_bul(FOY, a, b, anchor)
        FOY.metin(f"M13.3(b) {blk}", frag, n or a, anchor)
    n = O.foy_satiri_bul(FOY, a, b, "| B6-AA |")
    FOY.metin("M13.3(b) B6-AA", f"| {mx('B6-AA', 'n_goruntu')} | {mx('B6-AA', 'model_sayisi')} |", n or a, "| B6-AA |")
    for ds in ("cifar10", "cifar100", "imagenetv2"):
        n = O.foy_satiri_bul(FOY, a, b, f"| B10-{ds} |")
        FOY.metin(f"M13.3(b) B10-{ds}", f"| {mx(f'B10-{ds}', 'model_sayisi')} | {mx(f'B10-{ds}', 'cift_sayisi')} |",
                  n or a, f"| B10-{ds} |")
    hrs = get("egitim_suresi.defter_toplam_sure_sa")
    FOY.kontrol("M9.1 B3 training hours (line 1470)", hrs, 1470, "Defterdeki temiz ve AT asama", 2)
    for i, s in enumerate(get("sapma_kaydi_basliklari")):
        if "sonradan" in s["baslik"]:
            n = O.foy_satiri_bul(FOY, a, b, s["baslik"])
            FOY.metin(f"M13.3(c) deviation {i}", s["baslik"], n or a, s["tarih"])
    return a, b


def glyph(pid, x, y, n, cont, side=3.5):
    """A small n x n matrix glyph (a transfer matrix or a design grid)."""
    O.matrix_glyph(pid, x, y, side, n, cont, fill="FFFFFF", edge=vf.C["muted"])


def block_list(prefix, x, y, w, items, cont):
    """Rows of (block id, text, glyph n): glyph, bold id, wrapped text. Returns the bottom."""
    idw = max(tw([[(b, "sb")]], S) if b else 0.0 for b, _, _ in items)
    for i, (b, txt, n) in enumerate(items):
        if n:
            glyph(f"{prefix}{i}_g", x, y + (LHS - 3.5) / 2, n, cont)
        tx = x + 6.0
        if b:
            T(f"{prefix}{i}_id", tx, y, [[(b, "sb")]], size=S, cont=cont, w=idw)
            tx += idw + 1.0
        h = TW(f"{prefix}{i}_t", tx, y, txt, x + w - tx, size=S, cont=cont)
        y += max(h, LHS) + 1.0
    return y


def lay(sha, sha_line):
    vf.reset(STEM, W, 120.0, naming_step=STEP, naming_kind="akis")
    x0 = 0.5
    f, _ = vf.tint_of("zemin_bandi")
    # the band keeps under 80 % of the page (balance gate: a larger fill is an ornamental background)
    vf.rect("band", x0 + 2.0, 0.5, gf(XR - x0 - 4.0), 10.0, fill=f, line=None, role="container", ctype="band")
    gap = 16.0
    pw = [36.0, 56.0]
    pw.append(gf(XR - x0 - 4.0 - 4.0 - sum(pw) - 2 * gap))
    xs = [x0 + 4.0, x0 + 4.0 + pw[0] + gap, x0 + 4.0 + pw[0] + gap + pw[1] + gap]
    top = 0.5 + 2.0
    s3, s8, src_seen, n_seen = seen_sizes()
    titles = ["Seen beforehand", "Main registration: B2-B6", "Supplement: B8-B10"]
    cy = []
    for i in range(3):
        cy.append(O.strip_panel(f"p{i}", titles[i], xs[i], top, pw[i], cont="band", key="sb"))
        vf.IDS[f"p{i}"]["naming"] = "none"            # flow figure: the panels are named by their titles only
    # NOTE the strip naming recorded by strip_panel is dropped below (step 2 admits flow marks only)
    vf.NAMING_USED[:] = [u for u in vf.NAMING_USED if not u["id"].startswith("p")]
    # panel 1: what was seen
    seen = [("", f"C1 pair {s3} matrices (CIFAR-10, CIFAR-100)", 3),
            ("", f"one-seed {s8} pool matrix", 4),
            ("", "derived values", None)]
    y1 = block_list("s", xs[0] + 1.5, cy[0], pw[0] - 3.0, seen, "p0")
    # panel 2: main registration blocks
    runs = sorted({a["takma_ad"] for a in get("B3_asamalari")})
    hrs = get("egitim_suresi.defter_toplam_sure_sa")
    b2 = [("B2", f"{mx('B2', 'model_sayisi')} models, {mx('B2', 'hucre_sayisi')} cells, "
                 f"{mx('B2', 'n_goruntu')} images", 3),
          ("B3", f"{len(runs)} training runs, {hrs:.1f} h", 2),
          ("B4", f"{mx('B4', 'model_sayisi')} models, {mx('B4', 'hucre_sayisi')} cells", 3),
          ("B5", f"MI {mx('B5-MI', 'hucre_sayisi')} and TGR {mx('B5-TGR', 'hucre_sayisi')} cells, "
                 f"{mx('B5-MI', 'model_sayisi')} models", 3),
          ("B6", f"AutoAttack, {mx('B6-AA', 'model_sayisi')} models, {mx('B6-AA', 'n_goruntu')} images", None)]
    y2 = block_list("m", xs[1] + 1.5, cy[1], pw[1] - 3.0, b2, "p1")
    b3 = [("B9", f"CIFAR-100: {mx('B9', 'model_sayisi')} models, {mx('B9', 'hucre_sayisi')} cells", 3),
          ("B8", f"ImageNetV2, ε {mx('B8', 'eps_x255'):g}/255: {mx('B8', 'model_sayisi')} models, "
                 f"{mx('B8', 'n_goruntu')} images", 3),
          ("B10", "Mantel: " + "/".join(str(mx(f"B10-{d}", "model_sayisi")) for d in ("cifar10", "cifar100", "imagenetv2"))
           + " models, " + "/".join(str(mx(f"B10-{d}", "cift_sayisi")) for d in ("cifar10", "cifar100", "imagenetv2"))
           + " pairs", None)]
    y3 = block_list("e", xs[2] + 1.5, cy[2], pw[2] - 3.0, b3, "p2")
    ph = gc(max(y1, y2, y3) + 0.75 - top)
    for i in range(3):
        vf.IDS[f"p{i}"]["h"] = ph
    vf.IDS["band"]["h"] = gc(top + ph + 2.0 - 0.5)
    # flows with the freeze labels (date, commit; the main body's SHA-256 prefix)
    labs = [[date_of(get("dondurma.on_kayit.utc")), get("dondurma.on_kayit.commit")[:7], sha[:8]],
            [date_of(get("dondurma.ek_on_kayit.utc")), get("dondurma.ek_on_kayit.commit")[:7]]]
    for j in range(2):
        a, b = f"p{j}", f"p{j + 1}"
        bl.flow(f"f{j}", a, b, label=None, kind="arrow")
        xg0, xg1 = xs[j] + pw[j], xs[j + 1]
        mid = gr(top + ph / 2)
        lines = [[(t, "sb" if k == 0 else "r")] for k, t in enumerate(labs[j])]
        wl = max(tw([ln], S) for ln in lines)
        if wl > (xg1 - xg0) - 1.0:
            raise SystemExit(f"flow label {labs[j]} needs {wl} mm, gap {xg1 - xg0:.2f} mm")
        T(f"f{j}_lab", gr((xg0 + xg1) / 2 - wl / 2), mid - len(lines) * LHS - 1.25, lines, size=S, color="muted",
          cont="band", w=wl, align="c")
    # strip: the post hoc entries of the deviation log
    ys = 0.5 + vf.IDS["band"]["h"] + 2.5      # keeps the band under 80 % of the page
    dev = [s for s in get("sapma_kaydi_basliklari") if "sonradan" in s["baslik"]]
    if len(dev) != 2:
        raise SystemExit(f"expected two post hoc entries in the deviation log, found {len(dev)}")
    names = ["main §7: hierarchical bootstrap", "supplement §12: S10-3"]
    items = [[(names[i], "r")] for i in range(2)]
    hs = bl.legend_strip("dev", "Added after the fact", x0, gr(ys), gf(XR - x0), items, cols=2)
    return gc(ys + hs + 0.75), dev, (src_seen, n_seen), hrs


def main():
    sha, sha_line = body_sha()
    a, b = foy_checks()
    foy = FOY.bitir()
    h, dev, seen_src, hrs = lay(sha, sha_line)
    v = O.bitir(h, "The pre-registration chain: what was seen before registration, the frozen main registration "
                   "with blocks B2-B6, the frozen supplement with blocks B8-B10, and the post hoc entries.",
                KIND, 3, n_exempt="each block prints its model and image counts", sablon="yontem_semasi",
                hedef=HEDEF, tavan=TAVAN, extra={"surec_zinciri": True})
    if v != "PASS":
        print("layout:", v, "| foy:", foy["karsilastirma_sayisi"], foy["uyusmayan"])
        return 0
    deg = [O.ev(p, v_, SRC, p, "read as is") for p, v_ in OKUNAN.items() if v_ != "(structure)"]
    for k, m in get("matrisler").items():
        for kk in ("n_goruntu", "model_sayisi", "hucre_sayisi", "cift_sayisi", "eps_x255"):
            if kk in m:
                deg.append(O.ev(f"{k} {kk}", m[kk], SRC, f"matrisler.{k}.{kk}", "printed as is"))
    deg.append(O.ev("B3 runs", len({x["takma_ad"] for x in get("B3_asamalari")}), SRC,
                    "len(set(B3_asamalari[].takma_ad))", "distinct run names"))
    deg.append(O.ev("registration body SHA-256 prefix", sha[:8], str(K.FOY), f"line {sha_line}", "first 8 hex"))
    deg.append(O.ev("seen matrices 3x3 and 8x8", ["3x3", "8x8"], seen_src[0], f"line {seen_src[1]}",
                    "regex on the registration's section 1"))
    for d in dev:
        deg.append(O.ev("deviation entry", d["baslik"], d["kaynak"].rsplit(":", 1)[0], d["kaynak"], "title, translated"))
    O.kanit_yaz(STEM, deg, foy=foy, okunan={SRC: sorted(OKUNAN)},
                ek={"foy_M13_3_satirlari": [a, b], "b3_saat": hrs},
                girdiler=[SRC, "raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md"])
    O.denge_ajan(STEM, 0, {"3b_veri": (False, "the figure draws no 3D object and no data in depth"),
                           "3b_kural_disi": (False, "no 3D object is drawn in the chain figure"),
                           "gereksiz_ikon": (False, "the matrix glyphs stand for the blocks' transfer matrices"),
                           "dogrudan_etiket": (True, "every block and arrow is labelled where it stands"),
                           "panel_basina_bir_iddia": (True, "each panel states one stage of the chain"),
                           "gercek_goruntu": ("uygulanmaz", "a registration timeline shows no image"),
                           "her_sayinin_kaynagi": (True, "every count is a key of the timeline JSON, checked "
                                                         "against the reference sheet")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
