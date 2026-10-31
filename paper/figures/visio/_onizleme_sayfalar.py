#!/usr/bin/env python
"""Page-context style previews and their montages (visio-cizici, İSTEM 5G), IEEE Access geometry.

    python paper/figures/visio/_onizleme_sayfalar.py

For the two preview figures (fig:study_overview, Visio; fig:gradient_alignment, cards) each
style's figure PDF is placed at print size on an IEEE Access page (scripts/onizleme_montaj.py
``sayfa``, venue ``ieee_access`` registered in this process by _vz_ortam.py) with the
manuscript's current caption, and the three pages of one figure are set side by side
(``montaj``), which also compares the five composition keys and flags TOKEN-ONLY pairs.
Writes paper/figures/onizleme/{sema,veri}_uslup_<N>.{pdf,png}, {sema,veri}_uc_uslup.{pdf,png,json}
and onizleme_ozet.json (5F line and distance to the liked reference per preview).
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _vz_ortam  # noqa: E402

_vz_ortam.kur()
sys.path.insert(0, str(_vz_ortam.SKILL / "scripts"))
import onizleme_montaj as OM  # noqa: E402

OUT = Path("paper/figures/onizleme")
DUZ = Path("paper/figures/qc/main_en_duz.tex")
SETS = {
    "sema": {"label": "fig:study_overview", "number": 1,
             # 5 was the template-level third candidate; the montage measured 8 / 5 as TOKEN-ONLY
             # (only the panel count differs; kept in sema_uc_uslup_8_H_5_token_only.*), so 5 is
             # skipped and 3, the next style in the liked-distance order, is previewed
             "items": [("8", "Üslup 8 (seçilen)"), ("H", "Üslup H (aday)"), ("3", "Üslup 3 (aday)")],
             "atlanan": [("5", "Üslup 5 (atlandı: 8 ile TOKEN-ONLY)")],
             "pdf": "paper/figures/visio/_onizleme_study_overview_uslup_{}.pdf"},
    "veri": {"label": "fig:gradient_alignment", "number": 7,
             "items": [("7", "Üslup 7 (seçilen)"), ("H", "Üslup H (aday)"), ("1", "Üslup 1 (aday)")],
             "pdf": "paper/figures/charts/_onizleme_gradient_alignment_uslup_{}.pdf"},
}


def caption(label: str) -> str:
    """The figure's caption in the flattened manuscript, math reduced to plain text."""
    lines = DUZ.read_text(encoding="utf-8").splitlines()
    for i, ln in enumerate(lines):
        if f"\\label{{{label}}}" in ln:
            for j in range(i, max(i - 6, 0), -1):
                if "\\caption{" in lines[j]:
                    cap = lines[j].split("\\caption{", 1)[1].rsplit("}", 1)[0]
                    cap = cap.replace("$\\simt$", "τ̄").replace("~", " ")
                    cap = re.sub(r"Table \\ref\{[^}]*\}", "the Mantel table", cap)
                    cap = re.sub(r"\$([A-Za-z])\$", r"\1", cap)
                    return cap
    raise SystemExit(f"caption of {label} not found in {DUZ}")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ozet = {}
    for key, s in SETS.items():
        cap = caption(s["label"])
        pages, figs, labels = [], [], []
        for no, lab in s["items"]:
            pdf = Path(s["pdf"].format(no))
            out = OUT / f"{key}_uslup_{no}.pdf"
            r = OM.sayfa(pdf, _vz_ortam.VENUE, "double", cap, lab, out, number=s["number"])
            ozet[f"{key}_uslup_{no}"] = {"sekil": str(pdf).replace("\\", "/"), "sayfa": str(out).replace("\\", "/"),
                                        "ozet_satiri": r["ozet_satiri"], "olcum": r["olcum"]}
            pages.append(out)
            figs.append(pdf)
            labels.append(lab)
            print(f"{out}: {r['ozet_satiri']}")
        for no, lab in s.get("atlanan", []):
            pdf = Path(s["pdf"].format(no))
            out = OUT / f"{key}_uslup_{no}.pdf"
            r = OM.sayfa(pdf, _vz_ortam.VENUE, "double", cap, lab, out, number=s["number"])
            ozet[f"{key}_uslup_{no}_atlandi"] = {"sekil": str(pdf).replace("\\", "/"),
                                                 "sayfa": str(out).replace("\\", "/"),
                                                 "ozet_satiri": r["ozet_satiri"], "olcum": r["olcum"]}
        m = OM.montaj(pages, labels, OUT / f"{key}_uc_uslup.pdf", figures=figs)
        with io.open(OUT / f"{key}_uc_uslup.json", "w", encoding="utf-8", newline="\n") as fh:
            json.dump(m, fh, indent=2, ensure_ascii=False, default=str)
        ozet[f"{key}_montaj"] = m
        print(f"{key}: kompozisyon {json.dumps(m['kompozisyon'], ensure_ascii=False)}")
        for p in m["ciftler"]:
            print(f"  {p['a']} / {p['b']}: {p['farkli_anahtarlar']} -> {'GECERLI' if p['gecerli'] else 'TOKEN-ONLY'}")
    with io.open(OUT / "onizleme_ozet.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(ozet, fh, indent=2, ensure_ascii=False, default=str)
    return 0 if all(ozet[f"{k}_montaj"]["ayrisma_tamam"] for k in SETS) else 1


if __name__ == "__main__":
    sys.exit(main())
