"""C2 (TGR) sonuclarini cift bazinda ve toplulastirilmis olarak yazar."""
import json

import numpy as np

rows = []
for p in (1, 2, 3):
    with open(f"results/c1_c2/pair{p}/tgr_summary.json", encoding="utf-8") as fh:
        rows.append(json.load(fh))

print("cift | saldiri | beyaz kutu (ham) | hedef dogru | her ikisi dogru")
for d in rows:
    for tag in ("tgr", "mi"):
        v = d[tag]
        print(f"  {d['pair']}  | {tag.upper():4s} | {v['whitebox_source_fooling_raw']:16.2f} | "
              f"{v['transfer_target_correct']:11.2f} | {v['transfer_both_correct']:15.2f}")
    m = d["mcnemar_both_correct"]
    print(f"       McNemar (her ikisi dogru): TGR-only {m['tgr_only']}, MI-only {m['mi_only']}, "
          f"p={m['p_exact']:.3e}")


def ms(vals):
    a = np.asarray(vals, dtype=float)
    return a.mean(), a.std(ddof=1)


print("\n3 tohum ortalamasi +- std:")
for key, lab in (("whitebox_source_fooling_raw", "beyaz kutu (ham)"),
                 ("transfer_target_correct", "hedef dogru"),
                 ("transfer_both_correct", "her ikisi dogru")):
    t = ms([d["tgr"][key] for d in rows])
    m = ms([d["mi"][key] for d in rows])
    print(f"  {lab:18s} TGR {t[0]:6.2f}+-{t[1]:.2f}   MI {m[0]:6.2f}+-{m[1]:.2f}   "
          f"fark {t[0] - m[0]:+.2f}")
