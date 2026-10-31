#!/usr/bin/env python
"""Per-entity 3D face tones for the Visio figures of adeb_sci_1 (plan 04_cizim_plani.md section 4).

The engine's ``bilesenler.face_tones`` reads one style-wide token, ``three_d.face_tones``;
it has no per-entity parameter (an open issue for the skill owner, plan section 12 item 4).
This helper swaps the token for one entity's three hex faces while a 3D object is drawn
and puts the style's own token back afterwards:

    with yuz_tonlari("vit") as tint:
        bl.iso_box("c0", x, y, 7, 5, 7, tint, container="k1")

Front face = the entity hex (the paper's semantic colour, konsey_ortak.COL), right face
0.25 toward white, top face 0.50 toward white, outline the front darkened 0.30. The values
are read from paper/figures/visio/palettes/adeb_konsey_uc_boyut.yaml, which
_palet_uret.py writes and checks (step >= 0.05 in WCAG relative luminance). The engine
re-checks the order and the step on every call (``face_step_ok``) and records the steps
(``tone_steps``) in the manifest; the manifest's ``three_d.token`` is written after the
block ends, so it carries the style's own token.

Karar (gorsel-uretici, 31.10.2026): the plan put this helper in _vz_ortam.py; the task of
the drawing phase puts it in its own module, because _vz_ortam.py (the Faz A venue shim) is
no longer needed and new scripts must not depend on it.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

import yaml

UC = Path(__file__).resolve().parent / "palettes" / "adeb_konsey_uc_boyut.yaml"
_MISSING = object()


def tablo():
    """{entity: {on, sag, ust, kenar, luminans, basamak, ...}} from the generated file."""
    return yaml.safe_load(UC.read_text(encoding="utf-8"))["varliklar"]


@contextmanager
def yuz_tonlari(varlik: str):
    """Draw 3D objects of ``varlik`` with its front/right/top hex faces; yields the tint key."""
    import visiofig as vf

    f = tablo()[varlik]
    td = vf.USLUP.three_d
    old = td.get("face_tones", _MISSING)
    key = f"{varlik}_3b"
    vf.TINT[key] = (f["on"].lstrip("#"), f["kenar"].lstrip("#"))      # fill unused: the faces are hex
    td["face_tones"] = {"top": f["ust"], "right": f["sag"], "front": f["on"]}
    try:
        yield key
    finally:
        if old is _MISSING:
            td.pop("face_tones", None)
        else:
            td["face_tones"] = old


def notr_kenar(rec, renk=None):
    """Draw the outline of a 3D object's faces in a neutral dark ink instead of the engine's
    hue-darkened outline (front darkened 0.30).

    Karar (gorsel-uretici, 31.10.2026): the balance gate (motor/host/denge.py) counts every
    chromatic stroke as an accent; with the engine's outline each 3D entity adds one more hue
    (#954200 for ViT, #00507D for R224) and study_overview reached 7 accents against the limit
    of 6. The face tones, which carry the meaning, stay as the plan sets them; only the stroke
    becomes the style's muted ink. The record keeps both values."""
    import visiofig as vf

    c = (renk or vf.C["muted"]).lstrip("#").upper()
    faces = []
    if "faces" in rec and isinstance(rec["faces"], dict):
        faces += list(rec["faces"].values())
    for lay in rec.get("layers", []):
        faces += list(lay["faces"].values())
    for fid in faces:
        vf.IDS[fid]["line"] = c
    rec["outline_engine"] = rec.get("outline")
    rec["outline_drawn"] = "#" + c
    return rec
