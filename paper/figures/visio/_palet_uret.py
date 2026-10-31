#!/usr/bin/env python
"""Write the paper palette for one catalogue style: paper/figures/visio/palettes/adeb_konsey_uslup_<N>.yaml,
and the 3D face ladder of the paper's entities: paper/figures/visio/palettes/adeb_konsey_uc_boyut.yaml.

The entity colours are the paper's own semantic Okabe-Ito binding, read from
paper/figures/konsey/konsey_ortak.py (COL, MUTE, OI); nothing is typed twice. The structural
colours (ink, frame, grid, card tones) are the selected style's, taken from the palette the
skill derives for that style (motor/host/uslup_to_palette.py, written to a temporary folder).
Every entity gets a marker so that it stays identifiable without colour.

Families (raporlar/visio_2026-10-31/04_cizim_plani.md section 4.3):
  mimari    vit, r224, r32, panel, xcit          (konsey_ortak.COL)
  bilesen   sym, dir                             (konsey_ortak.COL)
  cift_turu cift_cnn (#000000, o), cift_vit (#F0E442, ^, 0.4 pt black edge), mixed (#6E6E6E, s)
  protokol  four nested conditioning sets, light to dark (#E7D4E8 ... #762A83; o ^ s D)
  ayar      the eight groups of the spread / clean-gap figure (fig_yayilim_temiz_fark.py GROUPS keys)
One hex codes one family. Every protokol and ayar hue is checked to differ from the seven
semantic hues (vit, r224, r32, panel, xcit, sym, dir) by at least CIEDE2000 10
(uslup.GLYPH_ACCENT_DE); a hue under it is fixed by darkening only, and the fix is recorded.

3D faces (plan section 4.1): the front face is the entity hex, the right face is the hex 0.25
toward white, the top face 0.50 toward white; the outline is the front darkened 0.30. The
WCAG relative luminance step top-right and right-front must be at least 0.05 or the
generator stops.

    python paper/figures/visio/_palet_uret.py --uslup 8 7
"""
from __future__ import annotations

import argparse
import io
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
_R = str(ROOT).replace("\\", "/")
os.environ.setdefault("VZ_PROJE_KOKU", _R)
os.environ.setdefault("VZ_PROJE_AYARI", _R + "/paper/figures/visio_cizici.yaml")
os.chdir(_R)
SKILL = Path.home() / ".claude" / "skills" / "visio-cizici"
sys.path.insert(0, str(SKILL))
sys.path.insert(0, "paper/figures/konsey")
import konsey_ortak as K  # noqa: E402
import yaml  # noqa: E402
from motor.figspec import cvd  # noqa: E402
from motor.figspec import palette as palette_mod  # noqa: E402
from motor.figspec import uslup as uslup_mod  # noqa: E402

OUT = Path("paper/figures/visio/palettes")
UC = OUT / "adeb_konsey_uc_boyut.yaml"
SEMANTIC = ("vit", "r224", "r32", "panel", "xcit", "sym", "dir")
# entity key -> (family, label, marker, line style, hex source)
ENTITIES = {
    "vit": ("mimari", "ViT-Tiny / transformer", "^", "-", ("COL", "vit")),
    "r224": ("mimari", "ResNet-18, 224 pipeline / CNN", "o", "-", ("COL", "r224")),
    "r32": ("mimari", "ResNet-18, CIFAR stem (R32)", "D", "--", ("COL", "r32")),
    "panel": ("mimari", "robust CNN panel member", "v", ":", ("COL", "panel")),
    "xcit": ("mimari", "XCiT-S12 (secondary)", "P", "-.", ("COL", "xcit")),
    "sym": ("bilesen", "symmetric part, sigma", "h", "-", ("COL", "sym")),
    "dir": ("bilesen", "directional part, rho", "X", "--", ("COL", "dir")),
    # pair types (plan 4.3): black and yellow are the two Okabe-Ito hues the paper does not use
    "cift_cnn": ("cift_turu", "CNN-CNN pair", "o", "-", ("OI", "black")),
    "cift_vit": ("cift_turu", "transformer-transformer pair", "^", "-", ("OI", "yellow")),
    "mixed": ("cift_turu", "mixed pair (CNN-transformer)", "s", "--", ("MUTE", None)),
}
EDGE_PT = {"cift_vit": 0.4}           # a yellow marker needs a black edge to be seen on white
# protokol: the four nested conditioning sets, light (largest set) to dark (smallest)
PROTOKOL = [("prot_raw", "Unconditioned", "#E7D4E8", "o"),
            ("prot_target", "Target-correct", "#C2A5CF", "^"),
            ("prot_both", "Both-correct", "#9970AB", "s"),
            ("prot_success", "Successful-source", "#762A83", "D")]
# ayar: the eight groups of fig_yayilim_temiz_fark.py (GROUPS keys, same order and markers);
# candidate hues from Paul Tol's 'muted' qualitative scheme, fixed by darkening if needed
AYAR = [("ayar_c10", "CIFAR-10 Linf, AT cifti", "CIFAR-10 Linf AT", "#332288", "o"),
        ("ayar_c10l2", "CIFAR-10 L2, AT cifti", "CIFAR-10 L2 AT", "#117733", "^"),
        ("ayar_c100", "CIFAR-100 Linf, AT cifti", "CIFAR-100 AT", "#88CCEE", "s"),
        ("ayar_svhn", "SVHN Linf, AT cifti", "SVHN AT", "#DDCC77", "D"),
        ("ayar_wrn", "CIFAR-10 Linf, WRN-28-10 referansiyla", "with WRN-28-10 ref.", "#882255", "v"),
        ("ayar_std", "CIFAR-10 Linf, standart egitimli modeller", "standard training", "#CC6677", "P"),
        ("ayar_last", "CIFAR-10 Linf, son kontrol noktasi", "last checkpoint", "#999933", "X"),
        ("ayar_pool", "CIFAR-10 Linf, RobustBench havuzu", "RobustBench pool", "#C4C4C4", "h")]
ACMA = {"sag": 0.25, "ust": 0.50}
# A neutral 3D ladder for objects that are not a paper entity (the transfer-matrix block and plate):
# verifier finding of 31.10.2026, the panel grey #999999 means "robust CNN panel" in the key of the
# study overview. #D9D9D9 is the light card grey the verifier proposed; it is not in the palette's
# entities, so it binds no meaning.
NOTR_3B = ("notr", "#D9D9D9")
KENAR = 0.30
HEADER = """# Generated by paper/figures/visio/_palet_uret.py; do not hand-edit.
# 3B yuzleri: on yuz varlik hex'idir; sag yuz 0.25, ust yuz 0.50 beyaza acilir (04_cizim_plani.md bolum 4).
# Lejant on yuz tonunu gosterir. Degerler paper/figures/visio/palettes/adeb_konsey_uc_boyut.yaml
# dosyasindadir ve paper/figures/visio/_yuz_tonlari.py (yuz_tonlari) ile uygulanir; uslubun
# three_d.face_tones koyulastirma degerleri bu makalede 3B varlik nesnelerinde kullanilmaz.
"""


def hex_of(src):
    kind, key = src
    if kind == "COL":
        return K.COL[key].upper()
    if kind == "OI":
        return K.OI[key].upper()
    return K.MUTE.upper()


def de(a, b):
    return float(cvd.delta_e2000(cvd.rgb_to_lab(cvd.hex_to_rgb(a)), cvd.rgb_to_lab(cvd.hex_to_rgb(b))))


def min_de(h, refs):
    return min((de(h, r), k) for k, r in refs.items())


def fix_by_darkening(h, refs, limit=uslup_mod.GLYPH_ACCENT_DE):
    """Darken toward black in 0.02 steps until every reference is at least `limit` away."""
    orig, t = h, 0.0
    while min_de(h, refs)[0] < limit:
        t = round(t + 0.02, 2)
        if t > 0.6:
            raise SystemExit(f"{orig}: cannot reach CIEDE2000 {limit} from {refs} by darkening")
        h = uslup_mod.mix(orig, "#000000", t)
    return h, t


def faces_of(h):
    on = h.upper()
    sag = uslup_mod.mix(on, "#FFFFFF", ACMA["sag"])
    ust = uslup_mod.mix(on, "#FFFFFF", ACMA["ust"])
    kenar = uslup_mod.mix(on, "#000000", KENAR)
    L = {k: uslup_mod.relative_luminance(v) for k, v in (("on", on), ("sag", sag), ("ust", ust))}
    steps = (L["ust"] - L["sag"], L["sag"] - L["on"])
    if min(steps) < uslup_mod.FACE_STEP_MIN:
        raise SystemExit(f"3D faces of {on}: steps {steps} under {uslup_mod.FACE_STEP_MIN}")
    return {"on": on, "sag": sag, "ust": ust, "kenar": kenar, "acma": dict(ACMA), "kenar_koyulastirma": KENAR,
            "luminans": {k: round(v, 4) for k, v in L.items()},
            "basamak": {"ust_sag": round(steps[0], 4), "sag_on": round(steps[1], 4)}}


def entities():
    sem = {k: hex_of(ENTITIES[k][4]) for k in SEMANTIC}
    ents, fixes = {}, []
    for k, (fam, lab, mk, ls, src) in ENTITIES.items():
        h = hex_of(src)
        ents[k] = {"hex": h, "marker": mk, "ls": ls, "label": lab, "emphasis": "primary", "aile": fam}
        if k in EDGE_PT:
            ents[k]["marker_edge"] = {"hex": "#000000", "pt": EDGE_PT[k]}
    for k, lab, h, mk in PROTOKOL:
        h2, t = fix_by_darkening(h, sem)
        if t:
            fixes.append({"varlik": k, "aday": h, "sonuc": h2, "koyulastirma": t})
        ents[k] = {"hex": h2, "marker": mk, "ls": "-", "label": lab, "emphasis": "primary", "aile": "protokol"}
    for k, grp, lab, h, mk in AYAR:
        h2, t = fix_by_darkening(h, sem)
        if t:
            fixes.append({"varlik": k, "aday": h, "sonuc": h2, "koyulastirma": t})
        ents[k] = {"hex": h2, "marker": mk, "ls": "-", "label": lab, "emphasis": "primary", "aile": "ayar",
                   "veri_grubu": grp}
    # one hex, one family
    seen = {}
    for k, e in ents.items():
        if e["hex"] in seen and ents[seen[e["hex"]]]["aile"] != e["aile"]:
            raise SystemExit(f"hex {e['hex']} binds {seen[e['hex']]} and {k} in two families")
        seen.setdefault(e["hex"], k)
    for k, e in ents.items():
        if cvd.contrast_ratio(e["hex"]) < palette_mod.MIN_CONTRAST:
            e["direct_label"] = True      # the skill's rule for a hue weak against white
    olcum = {k: {"en_yakin_anlam_rengi": min_de(ents[k]["hex"], sem)[1],
                 "ciede2000": round(min_de(ents[k]["hex"], sem)[0], 2)}
             for k in ents if ents[k]["aile"] in ("protokol", "ayar", "cift_turu")}
    return ents, fixes, olcum


def uret(no: str, ents, fixes, olcum) -> Path:
    u = uslup_mod.load_uslup(no, argv=[])
    with tempfile.TemporaryDirectory() as td:
        sp = uslup_mod.ensure_palette(u, Path(td))
        style_pal = yaml.safe_load(Path(sp).read_text(encoding="utf-8"))
    doc = {"paper": f"adeb_konsey_uslup_{u.no}",
           "kaynak": {"varliklar": "paper/figures/konsey/konsey_ortak.py COL, MUTE, OI; plan 04 bolum 4.3",
                      "konsey_ortak_sha256": K.sha("paper/figures/konsey/konsey_ortak.py"),
                      "yapisal": f"skill uslup_to_palette, uslup {u.no}",
                      "uc_boyut": str(UC).replace("\\", "/"),
                      "ciede2000_esigi": uslup_mod.GLYPH_ACCENT_DE,
                      "koyulastirma_duzeltmeleri": fixes, "anlam_renklerine_uzaklik": olcum},
           "entities": ents, "structural": style_pal.get("structural", {})}
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"adeb_konsey_uslup_{u.no}.yaml"
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(HEADER)
        yaml.safe_dump(doc, fh, allow_unicode=True, sort_keys=False)
    pal = palette_mod.load(str(p))
    rep = palette_mod.validate_binding(pal)
    print(f"wrote {p}: {len(pal.entities)} entities, {len(pal.structural)} structural, "
          f"{len(rep['warnings'])} warning(s)")
    for w in rep["warnings"]:
        print("  warning:", w)
    return p


def uret_uc_boyut() -> Path:
    doc = {"kaynak": "paper/figures/visio/_palet_uret.py; plan raporlar/visio_2026-10-31/04_cizim_plani.md 4.1",
           "kural": "on yuz varlik hex'i; sag 0.25, ust 0.50 beyaza acilir; kenar on yuzun 0.30 koyusu",
           "basamak_esigi": uslup_mod.FACE_STEP_MIN,
           "varliklar": {k: faces_of(hex_of(ENTITIES[k][4])) for k in SEMANTIC}}
    doc["varliklar"][NOTR_3B[0]] = dict(faces_of(NOTR_3B[1]), anlam="none: neutral 3D tone, not a paper entity")
    with io.open(UC, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Generated by paper/figures/visio/_palet_uret.py; do not hand-edit.\n")
        yaml.safe_dump(doc, fh, allow_unicode=True, sort_keys=False)
    for k, v in doc["varliklar"].items():
        print(f"  3D {k}: on {v['on']} sag {v['sag']} ust {v['ust']} kenar {v['kenar']} "
              f"L {v['luminans']} basamak {v['basamak']}")
    print(f"wrote {UC}")
    return UC


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--uslup", nargs="+", required=True)
    a = ap.parse_args()
    ents, fixes, olcum = entities()
    for f in fixes:
        print("  CIEDE2000 fix:", f)
    for k, v in olcum.items():
        print(f"  {k}: {ents[k]['hex']} nearest semantic {v['en_yakin_anlam_rengi']} dE2000 {v['ciede2000']}")
    for n in a.uslup:
        uret(n, ents, fixes, olcum)
    uret_uc_boyut()


if __name__ == "__main__":
    main()
