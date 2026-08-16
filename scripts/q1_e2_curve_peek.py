"""E2 ara-bakis: tamamlanan yorungelerin metrics.jsonl ozeti (tepe/final/dusus).

Kullanim (konteyner icinde):
    python scripts/q1_e2_curve_peek.py            # tum e2 yorungeleri
    python scripts/q1_e2_curve_peek.py vit_tiny   # ada gore suz
"""
import json
import sys
from pathlib import Path

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
flt = sys.argv[1] if len(sys.argv) > 1 else ""

rows = []
for mfile in sorted((ROOT / "models/q1/e2").glob("*/*/adv/adversarial_training/epochs/metrics.jsonl")):
    tag = mfile.parents[4].name  # ornek: vit_tiny_s2002
    if flt and flt not in tag:
        continue
    recs = [json.loads(l) for l in mfile.read_text().splitlines() if l.strip()]
    if not recs:
        continue
    best = max(recs, key=lambda r: r["adv_acc"])
    peak = best["adv_acc"]
    # tepe-1.1 bandi (2k bolmesinin binom SE mertebesi)
    band = [r["epoch"] for r in recs if r["adv_acc"] >= peak - 1.1]
    rows.append((tag, len(recs), best["epoch"], peak, recs[-1]["adv_acc"],
                 peak - recs[-1]["adv_acc"], len(band), min(band), max(band),
                 best["clean_acc"]))

print(f"{'yorunge':<18}{'n':>4}{'tepe_ep':>8}{'tepe':>8}{'final':>8}{'dusus':>7}"
      f"{'bant_n':>8}{'bant_ep':>12}{'clean@tepe':>11}")
for r in rows:
    print(f"{r[0]:<18}{r[1]:>4}{r[2]:>8}{r[3]:>8.2f}{r[4]:>8.2f}{r[5]:>7.2f}"
          f"{r[6]:>8}{f'{r[7]}-{r[8]}':>12}{r[9]:>11.2f}")
