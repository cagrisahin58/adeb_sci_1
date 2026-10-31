#!/usr/bin/env python
"""Shared set-up and helpers of the Visio figure scripts of adeb_sci_1 (style 8, IEEE Access).

Every figure script imports this module first. It sets the project environment the skill's
engine reads (VZ_PROJE_KOKU, VZ_PROJE_AYARI; the root is the WSL path read through UNC by
Windows Python, written with forward slashes), changes to the repository root, puts the skill
(motor/visio, then the skill root) and paper/figures/konsey on sys.path, and loads the style
(--uslup, default 8), the venue ieee_access (in the skill's REGISTRY since 31.10.2026) and the
paper palette paper/figures/visio/palettes/adeb_konsey_uslup_<N>.yaml.

It does not use the Faz A shim _vz_ortam.py.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
_R = str(ROOT).replace("\\", "/")
os.environ.setdefault("VZ_PROJE_KOKU", _R)
os.environ.setdefault("VZ_PROJE_AYARI", _R + "/paper/figures/visio_cizici.yaml")
os.chdir(_R)
SKILL = Path.home() / ".claude" / "skills" / "visio-cizici"
for _p in (str(SKILL), str(SKILL / "motor" / "visio"), str(Path(__file__).resolve().parent),
           "paper/figures/konsey"):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import visiofig as vf  # noqa: E402
import bilesenler as bl  # noqa: E402
from motor.figspec.kanit import write_kanit  # noqa: E402
import konsey_ortak as K  # noqa: E402
from _yuz_tonlari import yuz_tonlari, tablo as yuz_tablosu  # noqa: E402,F401

VENUE = "ieee_access"
G = vf.GRID
IN = 1.5            # text inset from a box edge (controller 1.0 plus the print shift, T21)
ARGS = None
U = None
NOTES = []


def baslat():
    """Parse --uslup (default 8; --check is the engine's) and load style, venue and palette."""
    global ARGS, U
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--uslup", default=os.environ.get("VZ_USLUP", "8"))
    ARGS, _ = ap.parse_known_args()
    U = vf.use(uslup=ARGS.uslup, venue=VENUE,
               palette=f"paper/figures/visio/palettes/adeb_konsey_uslup_{ARGS.uslup}.yaml")
    ent = K.COL
    for k, h in ent.items():                       # entity hues: light fill, entity edge
        vf.C[k] = h.lstrip("#").upper()
        vf.TINT[k] = (vf.mix("FFFFFF", vf.C[k], 0.12), vf.C[k])
    return U


# ------------------------------------------------------------------ grid and text
def gr(v):
    return round(v / G) * G


def gc(v):
    return math.ceil(v / G - 1e-9) * G


def gf(v):
    return math.floor(v / G + 1e-9) * G


def lh(size=None):
    return vf.line_h(size)


def tw(spec, size=None, key="r"):
    return gc(max(bl.text_box_w(ln, size) for ln in vf.norm_lines(spec, key)))


def wrap(text, width, size=None, key="r"):
    """Greedy word wrap with the controller's own text measure; returns run lines."""
    out, cur = [], ""
    for word in text.split(" "):
        cand = (cur + " " + word).strip()
        if cur and bl.text_box_w([(cand, key)], size) > width:
            out.append(cur)
            cur = word
        else:
            cur = cand
    if cur:
        out.append(cur)
    return [[(t, key)] for t in out]


def T(pid, x, y, spec, *, size=None, color="ink", cont=None, align="l", w=None, key="r"):
    """A text box sized to its lines; returns (w, h)."""
    ln = vf.norm_lines(spec, key)
    ww = gc(w) if w is not None else tw(ln, size)
    h = len(ln) * lh(size)
    vf.text(pid, gr(x), gr(y), ww, h, ln, color=color, size=size, align=align, container=cont)
    return ww, h


def TW(pid, x, y, text, width, *, size=None, color="ink", cont=None, key="r"):
    """Wrapped text in a column ``width`` wide; returns its height."""
    ln = wrap(text, width, size, key)
    T(pid, x, y, ln, size=size, color=color, cont=cont, w=width, key=key)
    return len(ln) * lh(size)


def kutu(pid, x, y, w, h, tint, cont=None, dash=False, rnd=None, lw=None):
    """A box by the style's kutu rule (frame language, stroke, corner) in a tint."""
    k = vf.USLUP.component("kutu")
    frame = k.get("cerceve") or {"cercevesiz": "dolgu", "ince cerceve": "ince+dolgu",
                                 "dolgu bandi": "dolgu"}[vf.USLUP.cerceve_dili]
    f, e = vf.tint_of(tint)
    vf.rect(pid, gr(x), gr(y), gc(w), gc(h), fill=f if "dolgu" in frame else None,
            line=e if "ince" in frame else None, lw=lw if lw is not None else float(k.get("cizgi_pt", vf.LW["ince"])),
            rnd=rnd if rnd is not None else float(k.get("kose_mm", vf.USLUP.corner_mm)),
            role="container", ctype="box", container=cont, dash=dash)
    return vf.IDS[pid]


def _drop(pid):
    rec = vf.IDS.pop(pid)
    vf.SCENE.remove(rec)


def panel_alti(pid, letter, title, x, y, w, h, cont=None, naming=None):
    """A panel whose name stands UNDER it, as style 8 prints it ('(a)' regular 9.0 pt, panel_alti;
    the engine reads no letter position, references/panel_adlandirma.md section 5).

    The engine's panel is drawn (frame, naming record), its top letter and title are removed and
    one caption line '(a) Title' (letter regular, title semibold, BODY size) is set 1 mm under the
    frame, inside ``cont``. Returns the content top (the panel's inner top)."""
    kind = naming or ("letter" if letter else "none")
    vf.panel(pid, letter if kind == "letter" else None, title, gr(x), gr(y), gc(w), gc(h), naming=kind)
    vf.IDS[pid]["container"] = cont
    for suf in ("_letter", "_title"):
        if pid + suf in vf.IDS:
            _drop(pid + suf)
    vf.IDS[pid]["caption"] = {"letter": vf.USLUP.letter(letter) if letter else None, "title": title}
    return gr(y) + 2.0


def panel_alti_yaz(pid, cont=None):
    """Set the caption line of ``panel_alti`` once the panel's height is final; returns its bottom."""
    p = vf.IDS[pid]
    cap = p["caption"]
    runs = ([(cap["letter"] + "  ", "r")] if cap["letter"] else []) + [(cap["title"], "sb")]
    y = gc(p["y"] + p["h"] + 1.0)
    w = tw([runs])
    vf.text(pid + "_cap", gr(p["x"] + 1.0), y, w, lh(), [runs], container=cont)
    return y + lh()


def legend_keys(pid, x, y, w, keys, cont, size=None, gap=5.0):
    """Swatch + label conventions in one line (front-face hue of the entity), items packed left to
    right with ``gap`` mm between them; wraps to a new line when ``w`` is full. Returns the height."""
    bx, by, rows = x, y, 1
    for i, (hexv, lab) in enumerate(keys):
        iw = 3.0 + tw([lab], size)
        if bx > x and bx + iw > x + w:
            bx, by, rows = x, by + lh(size), rows + 1
        vf.rect(f"{pid}_s{i}", gr(bx), gr(by + (lh(size) - 2.0) / 2), 2.0, 2.0, fill=hexv.lstrip("#").upper(),
                line=None, role="mark", container=cont)
        T(f"{pid}_l{i}", bx + 3.0, by, [lab], size=size, cont=cont)
        bx = gc(bx + iw + gap)
    return rows * lh(size)


def matrix_glyph(pid, x, y, side, n, cont, fill="FFFFFF", edge=None, diag=None):
    """A flat n x n matrix glyph; ``diag`` fills the diagonal cells (hex)."""
    e = edge or vf.C["frame"]
    vf.rect(pid, gr(x), gr(y), side, side, fill=fill, line=e, lw=vf.USLUP.line_min_pt, role="obstacle",
            container=cont)
    step = side / n
    if diag:
        for i in range(n):
            vf.rect(f"{pid}_d{i}", gr(x) + i * step, gr(y) + i * step, step, step, fill=diag, line=None,
                    role="mark", container=cont, grid=False)
    for i in range(1, n):
        vf.seg(f"{pid}_v{i}", (gr(x) + i * step, gr(y)), (gr(x) + i * step, gr(y) + side), e, vf.USLUP.line_min_pt)
        vf.seg(f"{pid}_h{i}", (gr(x), gr(y) + i * step), (gr(x) + side, gr(y) + i * step), e, vf.USLUP.line_min_pt)


def cos_glyph(pid, x, y, size, cont):
    """Two unit vectors from one origin and the arc between them: the cosine glyph."""
    ox, oy = gr(x), gr(y) + size
    c = vf.C["ink"]
    vf.seg(pid + "_a", (ox, oy), (ox + size, oy), c, vf.LW["normal"], arrow=True)
    vf.seg(pid + "_b", (ox, oy), (ox + size * 0.62, oy - size * 0.78), c, vf.LW["normal"], arrow=True)
    pts = [(ox + 0.45 * size * math.cos(t), oy - 0.45 * size * math.sin(t))
           for t in [i * math.radians(51.5) / 6 for i in range(7)]]
    for i in range(len(pts) - 1):
        vf.seg(f"{pid}_arc{i}", pts[i], pts[i + 1], vf.C["muted"], vf.USLUP.line_min_pt)


# ------------------------------------------------------------------ evidence and finishing
def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def ev(etiket, deger, kaynak, anahtar_yolu, hesap, metinde=None):
    d = {"etiket": etiket, "deger": deger, "kaynak": kaynak, "anahtar_yolu": anahtar_yolu, "hesap": hesap}
    if metinde:
        d["metinde"] = metinde
    return d


def kanit_yaz(stem, degerler, foy=None, okunan=None, ek=None, girdiler=()):
    p = write_kanit(stem, vf.OUT_DIR, uslup_no=U.no, degerler=degerler, records=None)
    k = json.loads(Path(p).read_text(encoding="utf-8"))
    if foy is not None:
        k["foy_karsilastirmasi"] = foy
    if okunan is not None:
        k["okunan_anahtarlar"] = okunan
    k["git"] = K.git_info(list(girdiler))
    k["betik"] = f"paper/figures/visio/{Path(sys.argv[0]).name} --uslup {ARGS.uslup}"
    k["foy_sha256"] = sha_file(K.FOY)
    k["notlar"] = NOTES
    if ek:
        k.update(ek)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(k, indent=2, ensure_ascii=False) + "\n")
    return p


def manifest_ek(**fields):
    """Add fields to the written manifest (<stem>.fig.json): the template (sablon), figure type,
    target height and so on, which write_fig_manifest takes no parameter for."""
    p = Path(vf.STEM + ".fig.json")
    m = json.loads(p.read_text(encoding="utf-8"))
    m.update(fields)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


def denge_ajan_yaz(stem, yanit):
    p = Path(vf.OUT_DIR) / f"{stem}.denge_ajan.json"
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(yanit, indent=2, ensure_ascii=False) + "\n")
    return p


def bitir(page_h, message, kind, panels, *, n_exempt=None, sablon=None, hedef=None, tavan=None,
          extra=None, groups=None):
    """Snap the page to its content, run the controller, write the manifest. Returns the verdict."""
    if tavan is not None and page_h > tavan + 1e-6:
        raise SystemExit(f"page height {page_h:.2f} mm over the plan's ceiling {tavan} mm")
    vf.PAGE_H = vf.snap_page(page_h)
    print(f"page {vf.PAGE_W:.3f} x {vf.PAGE_H:.3f} mm (target {hedef}, ceiling {tavan})")
    rep = vf.run(groups=groups) if groups else vf.run()
    if rep["verdict"] in ("PREFLIGHT-ONLY",):
        return rep["verdict"]
    if rep["verdict"] != "PASS":
        sys.exit(1)
    vf.write_fig_manifest(message, kind=kind, panels=panels, n_exempt_reason=n_exempt)
    f = {"sablon": sablon, "tur": "sematik", "hedef_yukseklik_mm": hedef, "tavan_yukseklik_mm": tavan,
         "uc_boyut_yuz_kurali": "on yuz varlik hex'i; sag 0.25, ust 0.50 beyaza acik "
                                "(paper/figures/visio/palettes/adeb_konsey_uc_boyut.yaml)"}
    f.update(extra or {})
    manifest_ek(**f)
    return "PASS"


def denge_ajan(stem, gercek_goruntu_sayisi, ozel=None):
    """The drawing agent's answer file for motor/host/denge.py (items a PDF cannot show).
    ``ozel`` overrides an item: {key: (deger, gerekce)}."""
    y = {
        "3b_veri": (False, "no data value is drawn in depth; the 3D objects are models, decks and matrices"),
        "3b_kural_disi": (False, "one oblique 25 degree view from the style, flat faces, no shadow, "
                                 "gradient or gloss, labels stay in the plane with leader space"),
        "clip_art": (False, "every drawn object is built from Visio primitives and carries meaning"),
        "gokkusagi_renk_haritasi": (False, "no colour map is used; hues are the paper's semantic colours"),
        "sus_arka_plan": (False, "the only band is the template's light grouping band, no decoration"),
        "gereksiz_ikon": (False, "glyphs stand for a matrix, a cosine, a mean or a nested set"),
        "dogrudan_etiket": (True, "every block, deck and box is labelled beside it in the plane"),
        "gercek_goruntu": ("uygulanmaz", "a schematic of the study design shows no data image"),
        "panel_basina_bir_iddia": (True, "each panel states one stage of the design"),
        "her_sayinin_kaynagi": (True, "every printed count is in the evidence file with its source key"),
    }
    for k, v in (ozel or {}).items():
        y[k] = v
    return denge_ajan_yaz(stem, {"stem": stem, "gercek_goruntu_sayisi": gercek_goruntu_sayisi,
                                 "yanitlar": {k: {"deger": d, "gerekce": g} for k, (d, g) in y.items()}})


def panel_bos(pid, x, y, w, h, cont=None, naming="none"):
    """A titleless panel frame (style 8 grup rule) for a flow stage: the engine's title is removed,
    the stage is named by the labelled flow marks between stages (naming step 2)."""
    vf.panel(pid, None, "stage", gr(x), gr(y), gc(w), gc(h), naming=naming)
    vf.IDS[pid]["container"] = cont
    for suf in ("_letter", "_title"):
        if pid + suf in vf.IDS:
            _drop(pid + suf)
    return vf.IDS[pid]


def kosebent(pid, x0, x1, y, color, depth=1.0):
    """An under-bracket from x0 to x1 hanging ``depth`` mm below y (links a term to its name)."""
    lw = vf.LW["normal"]
    vf.seg(pid + "_l", (x0, y), (x0, y + depth), color, lw)
    vf.seg(pid + "_m", (x0, y + depth), (x1, y + depth), color, lw)
    vf.seg(pid + "_r", (x1, y + depth), (x1, y), color, lw)


def strip_panel(pid, title, x, y, w, cont=None, tone=None, key="sb"):
    """A letterless strip panel (naming step 4) whose title is set at the body size (9 pt) instead of
    the style's 10.9 pt title; ``tone`` fills it (a tone card). Returns the content top."""
    vf.panel(pid, None, title, gr(x), gr(y), gc(w), 10, naming="strip")
    vf.IDS[pid]["container"] = cont
    if tone:
        vf.IDS[pid]["fill"] = vf.tint_of(tone)[0]
    t = vf.IDS[pid + "_title"]
    t["design"], t["size"] = vf.BODY, vf.authored(vf.BODY)
    t["y"], t["h"] = gr(y) + 1.25, lh()
    t["lines"] = [[(title, key)]]
    t["w"] = tw([[(title, key)]])
    return gc(t["y"] + t["h"] + 0.25)


def foy_satiri_bul(foy, ilk, son, *parcalar):
    """First reference-sheet line in [ilk, son] holding every fragment; None if none."""
    for n in range(ilk, son + 1):
        t = foy.lines[n - 1]
        if all(p in t for p in parcalar):
            return n
    return None


def foy_bolum(foy, baslik):
    """(first, last) line numbers of the reference-sheet section whose heading starts with ``baslik``."""
    ilk = next(i + 1 for i, t in enumerate(foy.lines) if t.startswith(baslik))
    son = next((i for i in range(ilk, len(foy.lines)) if foy.lines[i].startswith("### ") or
                foy.lines[i].startswith("## ")), len(foy.lines))
    return ilk, son
