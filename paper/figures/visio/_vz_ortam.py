#!/usr/bin/env python
"""Project-side environment for the visio-cizici engine (adeb_sci_1, IEEE Access).

Why this file exists (gorsel-uretici, 31.10.2026, style-preview phase):

1. The venue ``ieee_access`` was measured with the skill's probe ("olculdu",
   raporlar/visio_2026-10-31/venue_probe_ieee_access.json) but it is not in the skill's
   ``motor/figspec/venues.py`` REGISTRY, and changing the skill is outside this phase.
   :func:`kur` registers it *in this process only*, from the measured block in
   ``raporlar/visio_2026-10-31/venue_ieee_access_blok.txt`` (the numbers are executed from
   that file, never typed here). Nothing in the skill is written.
2. The project root is a WSL path read through UNC by Windows Python; the engine reads it
   from ``VZ_PROJE_KOKU`` and the settings from ``VZ_PROJE_AYARI`` (paper/figures/
   visio_cizici.yaml), both set here before any engine module is imported.

Use as a module (first import in a figure script)::

    import _vz_ortam; _vz_ortam.kur()

or as a runner for a skill script that must see the venue::

    python paper/figures/visio/_vz_ortam.py <skill script.py> [args ...]

Remove this shim once ``ieee_access`` is in the skill's REGISTRY and the settings line
``venue: ieee_access`` is opened.
"""
from __future__ import annotations

import os
import re
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = Path.home() / ".claude" / "skills" / "visio-cizici"
AYAR = ROOT / "paper" / "figures" / "visio_cizici.yaml"
BLOK = ROOT / "raporlar" / "visio_2026-10-31" / "venue_ieee_access_blok.txt"
VENUE = "ieee_access"


def _posix_unc(p: Path) -> str:
    """'\\\\wsl.localhost\\...' -> '//wsl.localhost/...' (Windows Python reads both; the engine's
    relative-path writer compares strings, so one spelling is used everywhere)."""
    return str(p).replace("\\", "/")


def kur(chdir: bool = True):
    """Set the environment, put the skill on sys.path and register the venue. Returns the Venue."""
    os.environ.setdefault("VZ_PROJE_KOKU", _posix_unc(ROOT))
    os.environ.setdefault("VZ_PROJE_AYARI", _posix_unc(AYAR))
    if chdir:
        os.chdir(_posix_unc(ROOT))
    for p in (str(SKILL), str(SKILL / "motor" / "visio")):
        if p not in sys.path:
            sys.path.insert(0, p)
    from motor.figspec import venues

    if VENUE in venues.REGISTRY:
        return venues.REGISTRY[VENUE]
    text = BLOK.read_text(encoding="utf-8")
    m = re.search(r"^IEEE_ACCESS = Venue\((.*?)^\)", text, re.S | re.M)
    if not m:
        raise SystemExit(f"{BLOK}: no 'IEEE_ACCESS = Venue(...)' block")
    ns = {"Venue": venues.Venue}
    exec(compile("IEEE_ACCESS = Venue(" + m.group(1) + ")", str(BLOK), "exec"), ns)
    v = ns["IEEE_ACCESS"]
    if v.name != VENUE or not v.measured:
        raise SystemExit(f"{BLOK}: block is not the measured {VENUE!r} venue")
    venues.REGISTRY[VENUE] = v
    return v


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    kur()
    script = sys.argv[1]
    sys.argv = [script] + sys.argv[2:]
    try:
        runpy.run_path(script, run_name="__main__")
    except SystemExit as e:
        return int(e.code or 0) if not isinstance(e.code, str) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
