#!/usr/bin/env python
"""Content of the study-overview schematic (fig:study_overview), shared by every style preview.

The figure carries no result numbers; its numerals are model and run counts. They are
counted here from the frozen cell tables and the B10 Mantel files with the same rules as
paper/figures/konsey/fig_study_overview_veri.py (that script is left untouched: it writes
into paper/figures/konsey/), and every count is compared with the reference sheet
results/C1_REFERANS_FOYU.md at a named line that must also carry an anchor string
(konsey_ortak.Foy). A mismatch stops the figure.

The real images on the CIFAR decks are the first four test images of each data set
(data/cifar-10-batches-py/test_batch, data/cifar-100-python/test), tiled 2 x 2 and
enlarged by pixel repetition; no image is generated or edited. ImageNetV2 carries no
image (Karar: its images are Flickr photographs under the ImageNet terms; printing them
is not cleared, see the report).
"""
from __future__ import annotations

import hashlib
import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "konsey"))
import konsey_ortak as K  # noqa: E402

HT10 = "raporlar/konsey_2026-10-29/hucre_tablosu.json"
HT100 = "raporlar/konsey_2026-10-29/hucre_tablosu_b9.json"
HT8 = "raporlar/konsey_2026-10-29/hucre_tablosu_b8.json"
M10 = "results/q1/konsey_b10_gradyan/mantel_cifar10.json"
M100 = "results/q1/konsey_b10_gradyan/mantel_cifar100.json"
M8 = "results/q1/konsey_b10_gradyan/mantel_imagenetv2.json"
J8 = "results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json"
GORUNTU = {"cifar10": ("data/cifar-10-batches-py/test_batch", b"data"),
           "cifar100": ("data/cifar-100-python/test", b"data")}
IMG_DIR = Path("paper/figures/visio/_onizleme_img")


def _count(ht, pred):
    return sum(1 for v in ht.values() if pred(v))


def _foy_rows(foy, lo, hi, test):
    return sum(1 for n in range(lo, hi + 1) if test(foy.lines[n - 1]))


def sayilar():
    """(counts, foy result, keys read) -- the rules of fig_study_overview_veri.py main()."""
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
    c["SeedRtt"] = _count(h10, cell("C1-R32"))
    c["SeedVscr"] = _count(h10, cell("V-scr"))
    c["SeedVin"] = _count(h10, cell("V-IN"))
    c["SeedRscr"] = _count(h10, cell("R224-scr"))
    c["SeedRin"] = _count(h10, cell("R224-IN"))
    c["PanelCten"] = _count(h10, lambda v: v["birincil_panel"])
    c["SecCten"] = _count(h10, lambda v: v["ikincil_panel"])
    c["SeedChunR"] = _count(h100, cell("C1-R32"))
    c["SeedChunV"] = _count(h100, cell("V-scr"))
    c["PanelChun"] = _count(h100, lambda v: v["birincil_panel"])
    c["SecChun"] = _count(h100, lambda v: v["ikincil_panel"])
    c["PanelIN"] = _count(h8, lambda v: v["birincil_panel"])
    c["SecIN"] = _count(h8, lambda v: v["ikincil_panel"])
    c["PairsIN"] = len(K.dig(b8, "b2.F_B2.K-a.ciftler"))
    c["TransIN"] = _count(h8, lambda v: v["hucre"] == "V-scr")
    c["UnpairedIN"] = c["TransIN"] - c["PairsIN"]
    foy.esit("CIFAR-10 total == sum of groups", c["NmodCten"],
             sum(c[k] for k in ("SeedRtt", "SeedVscr", "SeedVin", "SeedRscr", "SeedRin", "PanelCten", "SecCten")),
             0, "partition")
    foy.esit("CIFAR-100 total == sum of groups", c["NmodChun"],
             sum(c[k] for k in ("SeedChunR", "SeedChunV", "PanelChun", "SecChun")), 0, "partition")
    foy.esit("ImageNetV2 total == sum of groups", c["NmodIN"],
             c["PairsIN"] + c["TransIN"] + c["PanelIN"] + c["SecIN"], 0, "partition (pairs = CNN counterparts)")
    foy.metin("CIFAR-10 K = 20 (S7)", f"S7, Hodge (K = {c['NmodCten']})", 1569, "| S7, Hodge")
    foy.metin("CIFAR-100 model count", f"| {c['NmodChun']} | 0 | 0 | evet |", 1826, "| B9 | cifar100 |")
    foy.metin("ImageNetV2 model count", f"| {c['NmodIN']} | 0 | 0 | evet |", 1827, "| B8 | imagenetv2 |")
    foy.metin("CIFAR-10 primary panel", f"panel {c['PanelCten']} uyeli", 1741, "Havuz modellerinde sigma ve rho")
    for cl, kk, ln in (("V-scr", "SeedVscr", 1496), ("V-IN", "SeedVin", 1497), ("R224-scr", "SeedRscr", 1498),
                       ("R224-IN", "SeedRin", 1499)):
        foy.metin(f"{cl} runs", f"| {cl} | {c[kk]} |", ln, f"| {cl} |")
    foy.esit("R32 runs == K-a seed pairs (foy 1593)", c["SeedRtt"], foy.lines[1592].count("ResNet18_AT_s"), 0,
             "count of ResNet seeds named on foy 1593")
    foy.esit("CIFAR-100 seed pairs (foy 1848)", c["SeedChunR"], foy.lines[1847].count("C100_ResNet18_AT_s"), 0,
             "count of ResNet seeds named on foy 1848")
    foy.esit("CIFAR-100 primary panel rows (foy 1873-1887)", c["PanelChun"],
             _foy_rows(foy, 1873, 1887, lambda t: "| panel | " in t and "| evet | hayir |" in t), 0, "row count")
    foy.esit("CIFAR-100 secondary panel rows", c["SecChun"],
             _foy_rows(foy, 1873, 1887, lambda t: "| ikincil_panel | " in t and "| hayir | evet |" in t), 0, "row count")
    foy.esit("ImageNetV2 primary panel rows (foy 1909-1922)", c["PanelIN"],
             _foy_rows(foy, 1909, 1922, lambda t: "| panel | CNN | - | panel |" in t), 0, "row count")
    foy.esit("ImageNetV2 secondary panel rows", c["SecIN"],
             _foy_rows(foy, 1909, 1922, lambda t: "| ikincil_panel |" in t), 0, "row count")
    foy.esit("ImageNetV2 pairs (foy 1930-1932)", c["PairsIN"],
             _foy_rows(foy, 1930, 1932, lambda t: t.startswith("| ") and "| IN_" in t), 0, "row count")
    foy.esit("ImageNetV2 unpaired transformer rows", c["UnpairedIN"],
             _foy_rows(foy, 1909, 1922, lambda t: "ciftsiz" in t), 0, "row count")
    sonuc = foy.bitir()
    okunan = {HT10: "modeller.<m>.{hucre, birincil_panel, ikincil_panel}",
              HT100: "modeller.<m>.{hucre, birincil_panel, ikincil_panel}",
              HT8: "modeller.<m>.{hucre, birincil_panel, ikincil_panel}",
              M10: "modeller_ortak", M100: "modeller_ortak", M8: "modeller_ortak", J8: "b2.F_B2.K-a.ciftler"}
    return c, sonuc, okunan


def kanit_degerleri(c):
    """write_kanit entries: every printed count with its source file and key."""
    src = {"NmodCten": (M10, "len(modeller_ortak)"), "NmodChun": (M100, "len(modeller_ortak)"),
           "NmodIN": (M8, "len(modeller_ortak)"), "PairsIN": (J8, "len(b2.F_B2.K-a.ciftler)")}
    out = []
    for k, v in c.items():
        f, key = src.get(k, (HT100 if "Chun" in k else HT8 if k.endswith("IN") else HT10,
                             "count over modeller.<m> (hucre / birincil_panel / ikincil_panel)"))
        out.append({"etiket": k, "deger": v, "kaynak": f, "anahtar_yolu": key,
                    "hesap": "count, checked against results/C1_REFERANS_FOYU.md "
                             "(paper/figures/visio/_icerik_study_overview.py sayilar)"})
    return out


def goruntuler(n=4, upscale=8):
    """Write the 2 x 2 CIFAR mosaics; returns {set: {path, source, sha256, indices}}."""
    import numpy as np
    from PIL import Image

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    out = {}
    for name, (src, key) in GORUNTU.items():
        raw = Path(src).read_bytes()
        d = pickle.loads(raw, encoding="bytes")
        x = np.asarray(d[key][:n]).reshape(n, 3, 32, 32).transpose(0, 2, 3, 1)
        side = int(round(n ** 0.5))
        rows = [np.concatenate(list(x[r * side:(r + 1) * side]), axis=1) for r in range(side)]
        mos = np.concatenate(rows, axis=0)
        im = Image.fromarray(mos.astype("uint8"), "RGB").resize(
            (mos.shape[1] * upscale, mos.shape[0] * upscale), Image.NEAREST)
        p = IMG_DIR / f"{name}_test_0-{n - 1}.png"
        im.save(p)
        # Visio's Import needs a full file name (a relative path is refused)
        out[name] = {"png": str(p.resolve()), "png_goreli": str(p).replace("\\", "/"), "kaynak": src,
                     "kaynak_sha256": hashlib.sha256(raw).hexdigest(),
                     "indeksler": list(range(n)), "islem": f"2x2 mosaic, nearest x{upscale}"}
    return out


if __name__ == "__main__":
    import json
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _vz_ortam
    _vz_ortam.kur()
    c, s, _ = sayilar()
    print(json.dumps(c), s["karsilastirma_sayisi"], s["sonuc"])
    print(json.dumps(goruntuler(), indent=1))
