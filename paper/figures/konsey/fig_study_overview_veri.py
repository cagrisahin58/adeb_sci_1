#!/usr/bin/env python3
"""Model counts for the study-overview TikZ figure (brief 12, section 6.1).

The overview carries no result numbers; its only numerals are model and run counts. This script
derives every count from the frozen cell tables and the B10 Mantel files, checks each against the
reference sheet, and writes them as LaTeX macros to paper/figures/konsey/fig_study_overview_sayilar.tex,
which fig_study_overview.tex reads with \\input. Nothing in the .tex is typed by hand.

Mode 1 (before compiling):  docker exec -w /workspace adeb_eval python -B paper/figures/konsey/fig_study_overview_veri.py
Mode 2 (after compiling):   ... fig_study_overview_veri.py --cikti-ekle   (adds PDF/PNG sha256, page size, fonts)
"""
import argparse
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import konsey_ortak as K  # noqa: E402

SCRIPT_REL = "paper/figures/konsey/fig_study_overview_veri.py"
NAME = "fig_study_overview"
HT10 = "raporlar/konsey_2026-10-29/hucre_tablosu.json"
HT100 = "raporlar/konsey_2026-10-29/hucre_tablosu_b9.json"
HT8 = "raporlar/konsey_2026-10-29/hucre_tablosu_b8.json"
M10 = "results/q1/konsey_b10_gradyan/mantel_cifar10.json"
M100 = "results/q1/konsey_b10_gradyan/mantel_cifar100.json"
M8 = "results/q1/konsey_b10_gradyan/mantel_imagenetv2.json"
J8 = "results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json"
TEX = K.OUTDIR / "fig_study_overview.tex"
SAY = K.OUTDIR / "fig_study_overview_sayilar.tex"


def count(ht, pred):
    return sum(1 for v in ht.values() if pred(v))


def foy_rows(foy, lo, hi, test):
    return sum(1 for n in range(lo, hi + 1) if test(foy.lines[n - 1]))


def cikti_ekle():
    kp = K.OUTDIR / f"{NAME}.kanit.json"
    k = json.loads(kp.read_text(encoding="utf-8"))
    pdf, png = K.OUTDIR / f"{NAME}.pdf", K.OUTDIR / f"{NAME}.png"
    for p in (pdf, png):
        if not p.is_file():
            K.fail(f"{p} missing; compile first")
    import fitz  # PyMuPDF, present in the container
    d = fitz.open(str(pdf))
    fonts = sorted({f[3] for f in d[0].get_fonts()})
    types = sorted({f[2] for f in d[0].get_fonts()})
    if "Type3" in types:
        K.fail("Type 3 font in the overview PDF")
    r = d[0].rect
    k["cikti"] = {"pdf_sha256": K.sha(pdf), "png_sha256": K.sha(png), "sayfa_boyutu_in": [round(r.width / 72, 3), round(r.height / 72, 3)],
                  "fontlar": fonts, "font_turleri": types, "tex_sha256": K.sha(TEX), "sayilar_sha256": K.sha(SAY)}
    k["yerlesim"]["boyut_in"] = k["cikti"]["sayfa_boyutu_in"]
    with io.open(kp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(k, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"updated: {kp}  page {k['cikti']['sayfa_boyutu_in']} in; fonts {fonts}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cikti-ekle", action="store_true")
    args = ap.parse_args()
    if args.cikti_ekle:
        return cikti_ekle()

    foy = K.Foy()
    h10, h100, h8 = (K.dig(K.load_json(p), "modeller") for p in (HT10, HT100, HT8))
    m10, m100, m8 = (K.load_json(p) for p in (M10, M100, M8))
    b8 = K.load_json(J8)
    c = {}
    c["NmodCten"], c["NmodChun"], c["NmodIN"] = (len(K.dig(m, "modeller_ortak")) for m in (m10, m100, m8))
    for key, ht in (("NmodCten", h10), ("NmodChun", h100), ("NmodIN", h8)):
        if c[key] != len(ht):
            K.fail(f"{key}: Mantel model count {c[key]} != cell table {len(ht)}")
    cell = lambda name: (lambda v: v["hucre"] == name)  # noqa: E731
    c["SeedRtt"] = count(h10, cell("C1-R32"))
    c["SeedVscr"] = count(h10, cell("V-scr"))
    c["SeedVin"] = count(h10, cell("V-IN"))
    c["SeedRscr"] = count(h10, cell("R224-scr"))
    c["SeedRin"] = count(h10, cell("R224-IN"))
    c["PanelCten"] = count(h10, lambda v: v["birincil_panel"])
    c["SecCten"] = count(h10, lambda v: v["ikincil_panel"])
    c["SeedChunR"] = count(h100, cell("C1-R32"))
    c["SeedChunV"] = count(h100, cell("V-scr"))
    c["PanelChun"] = count(h100, lambda v: v["birincil_panel"])
    c["SecChun"] = count(h100, lambda v: v["ikincil_panel"])
    c["PanelIN"] = count(h8, lambda v: v["birincil_panel"])
    c["SecIN"] = count(h8, lambda v: v["ikincil_panel"])
    c["PairsIN"] = len(K.dig(b8, "b2.F_B2.K-a.ciftler"))
    c["TransIN"] = count(h8, lambda v: v["hucre"] == "V-scr")
    c["UnpairedIN"] = c["TransIN"] - c["PairsIN"]
    # internal sums
    foy.esit("CIFAR-10 total == sum of groups", c["NmodCten"],
             sum(c[k] for k in ("SeedRtt", "SeedVscr", "SeedVin", "SeedRscr", "SeedRin", "PanelCten", "SecCten")), 0, "partition")
    foy.esit("CIFAR-100 total == sum of groups", c["NmodChun"],
             sum(c[k] for k in ("SeedChunR", "SeedChunV", "PanelChun", "SecChun")), 0, "partition")
    foy.esit("ImageNetV2 total == sum of groups", c["NmodIN"],
             c["PairsIN"] + c["TransIN"] + c["PanelIN"] + c["SecIN"], 0, "partition (pairs = CNN counterparts)")
    # foy
    foy.metin("CIFAR-10 K = 20 (S7)", f"S7, Hodge (K = {c['NmodCten']})", 1569, "| S7, Hodge")
    foy.metin("CIFAR-100 model count", f"| {c['NmodChun']} | 0 | 0 | evet |", 1826, "| B9 | cifar100 |")
    foy.metin("ImageNetV2 model count", f"| {c['NmodIN']} | 0 | 0 | evet |", 1827, "| B8 | imagenetv2 |")
    foy.metin("CIFAR-10 primary panel", f"panel {c['PanelCten']} uyeli", 1741, "Havuz modellerinde sigma ve rho")
    for cl, kk, ln in (("V-scr", "SeedVscr", 1496), ("V-IN", "SeedVin", 1497), ("R224-scr", "SeedRscr", 1498),
                       ("R224-IN", "SeedRin", 1499)):
        foy.metin(f"{cl} runs", f"| {cl} | {c[kk]} |", ln, f"| {cl} |")
    foy.esit("R32 runs == K-a seed pairs (foy 1593 lists three pairs)", c["SeedRtt"],
             foy.lines[1592].count("ResNet18_AT_s"), 0, "count of ResNet seeds named on foy 1593")
    foy.esit("CIFAR-100 seed pairs (foy 1848)", c["SeedChunR"], foy.lines[1847].count("C100_ResNet18_AT_s"), 0,
             "count of ResNet seeds named on foy 1848")
    foy.esit("CIFAR-100 primary panel rows (foy 1873-1887)", c["PanelChun"],
             foy_rows(foy, 1873, 1887, lambda t: "| panel | " in t and "| evet | hayir |" in t), 0, "row count")
    foy.esit("CIFAR-100 secondary panel rows", c["SecChun"],
             foy_rows(foy, 1873, 1887, lambda t: "| ikincil_panel | " in t and "| hayir | evet |" in t), 0, "row count")
    foy.esit("ImageNetV2 primary panel rows (foy 1909-1922)", c["PanelIN"],
             foy_rows(foy, 1909, 1922, lambda t: "| panel | CNN | - | panel |" in t), 0, "row count")
    foy.esit("ImageNetV2 secondary panel rows", c["SecIN"],
             foy_rows(foy, 1909, 1922, lambda t: "| ikincil_panel |" in t), 0, "row count")
    foy.esit("ImageNetV2 pairs (foy 1930-1932)", c["PairsIN"],
             foy_rows(foy, 1930, 1932, lambda t: t.startswith("| ") and "| IN_" in t), 0, "row count")
    foy.esit("ImageNetV2 unpaired transformer rows", c["UnpairedIN"],
             foy_rows(foy, 1909, 1922, lambda t: "ciftsiz" in t), 0, "row count")
    foy_sonuc = foy.bitir()

    lines = ["% Generated by paper/figures/konsey/fig_study_overview_veri.py; do not edit by hand.",
             "% Every count is read from the cell tables / Mantel files and checked against results/C1_REFERANS_FOYU.md."]
    lines += [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in c.items()]
    with io.open(SAY, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    okunan = {HT10: ["modeller.<m>.{hucre, birincil_panel, ikincil_panel}"], HT100: ["modeller.<m>.{hucre, birincil_panel, ikincil_panel}"],
              HT8: ["modeller.<m>.{hucre, birincil_panel, ikincil_panel}"], M10: ["modeller_ortak"], M100: ["modeller_ortak"],
              M8: ["modeller_ortak"], J8: ["b2.F_B2.K-a.ciftler"]}
    kp = K.write_kanit(K.OUTDIR, NAME, SCRIPT_REL, [], [HT10, HT100, HT8, M10, M100, M8, J8], (K.DOUBLE_IN, 0), 0, 0, okunan,
                       {"makrolar": c, "makro_dosyasi": str(SAY)}, foy_sonuc,
                       ["model totals == sum of groups for each data set",
                        "totals vs foy 1569 (K = 20), 1826 (15), 1827 (14); panel and secondary counts vs foy rows",
                        "run counts per cell vs foy 1496-1499; seed pairs vs foy 1593, 1848; ImageNetV2 pairs vs 1930-1932"],
                       ["TikZ figure: drawn by fig_study_overview.tex (copy of paper/figures/overview/fig_study_overview.tex, "
                        "rewritten per brief 12 section 6.1; the original is untouched). Numerals in the drawing are only the "
                        "macros above; names such as PGD-10, H1-H3 and 2x2 are labels.",
                        "Layout fields (size, fonts, PDF hash) are filled by --cikti-ekle after compiling with pdflatex in WSL."],
                       None)
    print(f"written: {SAY}\nwritten: {kp}")
    print(f"foy comparisons {foy_sonuc['karsilastirma_sayisi']}, all matched; counts {c}")


if __name__ == "__main__":
    main()
