"""E2 ara-bakis: tamamlanan secim kosumlarinin ozeti (KESIFSEL, on-kayitli
analiz DEGIL - resmi rapor scripts/q1_e2_report.py ile uretilir).

Kullanim (konteyner icinde): python scripts/q1_e2_peek.py
"""
import json
from pathlib import Path

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
IN = ROOT / "results/q1/e2"

cells = {}
for jp in sorted(IN.glob("select_*_val?.json")):
    stem = jp.stem  # select_resnet18_s1001_valA
    parts = stem.split("_")
    cond = parts[-1][-1]
    seed = parts[-2]
    arch = "_".join(parts[1:-2])
    s = json.load(open(jp))
    cells.setdefault((arch, seed), {})[cond] = s

print(f"{'yorunge':<20}{'kosul':>6}{'sec_ep':>8}{'val_adv':>9}{'test_clean':>11}{'test_adv':>10}")
for (arch, seed), row in sorted(cells.items()):
    for cond in "ABC":
        if cond not in row:
            continue
        s = row[cond]
        t = s.get("test") or {}
        print(f"{arch + '_' + seed:<20}{cond:>6}{s['selected_epoch']:>8}"
              f"{s['selected_adv_acc']:>9.2f}{t.get('clean_acc', float('nan')):>11.2f}"
              f"{t.get('adv_acc', float('nan')):>10.2f}")
    have = [c for c in "ABC" if c in row and row[c].get("test")]
    if "A" in have and "B" in have:
        d = row["A"]["test"]["adv_acc"] - row["B"]["test"]["adv_acc"]
        de = row["A"]["selected_epoch"] - row["B"]["selected_epoch"]
        print(f"{'':<20}{'A-B':>6}{de:>8}{'':>9}{'':>11}{d:>10.2f}  <- sizinti(+gurultu)")
    if "B" in have and "C" in have:
        d = row["B"]["test"]["adv_acc"] - row["C"]["test"]["adv_acc"]
        de = row["B"]["selected_epoch"] - row["C"]["selected_epoch"]
        print(f"{'':<20}{'B-C':>6}{de:>8}{'':>9}{'':>11}{d:>10.2f}  <- SAF GURULTU TABANI")
print(f"\ntamamlanan hucre: {sum(len(r) for r in cells.values())}/18")
