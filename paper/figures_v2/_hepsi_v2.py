#!/usr/bin/env python
"""Redraw, gate and reinstall every v2 figure in order (second round 08.11.2026, third round 09.11.2026).

    python paper/figures_v2/_hepsi_v2.py [kok ...]

For each kok: removes the installed figN_<kok> files (this installer's own outputs), runs z_<kok>.py (Visio),
then _kapilar_v2.py <kok> --tsv with the figure's composition note. One summary line per figure goes to
visio_loglari/hepsi_v2.log.
"""
import datetime as dt
import io
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = HERE / "visio_loglari" / "hepsi_v2.log"
NOTES = {
    "study_overview": "maket masasi; harfler not kartinda sol altta, (c) kilavuzlari karo yuzunde noktali; 1.5 pt kural; en tire",
    "design_recipe": "kartotek dolabi; adim 6; yazi muafiyeti; 1.5 pt kural; V-scr ve R32 uc fis karti",
    "decomposition_schematic": "uc katli buzlu kesit, egri baglayicilar, katman 6 mm geri; adim 2",
    "panel_members": "duz: iki katalog karti ust uste; adim 4; yazi muafiyeti; baslik 1.5 pt kural",
    "registry_map": "duz: satirli tablo-grafik, ana kayit ve ek iki grup kartinda; adim 3; baslik 1.5 pt kural",
    "prereg_chain": "duz: zincir kartinda uc kart soldan saga, duz oklar; adim 2",
    "source_gap_split": "duz: uc kart, yatay cubuk, ortak olcek; K7 muafiyeti kalkti; adim 4; q n/a notu",
    "similarity_matrix": "duz: uc kartta duz isi haritasi; adim 3",
    "cells_interaction": "duz: uc kart ust uste, direk yok; adim 4",
    "attack_side": "duz: tek kart, satir cizgileri, hucre bantlari; tek panel",
    "gradient_alignment": "duz: uc sutun karti, ham/islem seridi/artik; adim 4; anahtar kurali 1.5 pt",
    "estimates_forest": "duz: iki kart ust uste; adim 4; anahtar kurali 1.5 pt",
    "protocol_settings": "duz: dort protokol karti ve sagda yayilim karti; adim 3",
    "protocol_sets": "terasli havuz (sahne) ve duz olcum karti; adim 4",
    "spread_clean_gap": "duz: iki kart ust uste, ortak x; adim 4; anahtar kurali 1.5 pt",
    "epsilon_sweep": "duz: tek kartta cizgi grafigi, dogrudan etiket, sayi satirlari; K7 muafiyeti kalkti",
    "feature_degradation": "ViT blok yigini (sahne), duz okuma kartlari; adim 2",
}
ORDER = list(NOTES)


def main():
    koks = sys.argv[1:] or ORDER
    mp = {}
    for ln in (HERE / "qc" / "ESLEME.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*z_(\w+)\s*\|\s*(fig\d+_\w+)\s*\|", ln)
        if m:
            mp[m.group(1)] = m.group(2)
    for kok in koks:
        name = mp[kok]
        for f in HERE.glob(f"{name}.*"):
            f.unlink()
        for f in HERE.glob(f"{name}_mm_kontrol.json"):
            f.unlink()
        r1 = subprocess.run([sys.executable, "-X", "utf8", str(HERE / f"z_{kok}.py")], capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
        v = [l for l in r1.stdout.splitlines() if l.startswith("verdict")]
        r2 = subprocess.run([sys.executable, "-X", "utf8", str(HERE / "_kapilar_v2.py"), kok, "--tsv", "--not", NOTES[kok]],
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
        q = [l for l in r2.stdout.splitlines() if l.startswith(name + " ")]
        d = re.findall(r'"karar": "(kurulabilir|kurulamaz)"', r2.stdout)
        line = f"{dt.datetime.now():%H:%M} {kok}: {v[-1] if v else 'NO VERDICT'} | denge {d[-1] if d else '?'} | {q[0] if q else 'NO QC'}"
        if not v or "FAIL" in v[-1]:
            line += " | " + " ".join(r1.stdout.splitlines()[-6:])[:600]
        with io.open(LOG, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(line + "\n")
        print(line, flush=True)


if __name__ == "__main__":
    main()
