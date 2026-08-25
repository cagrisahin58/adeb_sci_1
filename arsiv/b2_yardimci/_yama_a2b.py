#!/usr/bin/env python3
"""a2b (sinif bilesimi) protokol tanimini TEK KAYNAGA baglar."""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/experiments/rev2/a2b_class_balance.py")
t = p.read_text(encoding="utf-8")

if "protokoller as PROTO" in t:
    print("zaten yamali")
    sys.exit(0)

CIFTLER = [
    ("sys.path.insert(0, ROOT)",
     "sys.path.insert(0, ROOT)\nfrom src.analysis import protokoller as PROTO  # noqa: E402",
     "import"),

    ('PROTOCOLS = ["raw", "target_correct", "both_correct", "successful_source"]',
     "PROTOCOLS = PROTO.PROTOKOLLER          # TEK KAYNAK (bkz. src/analysis/protokoller.py)",
     "PROTOCOLS"),

    ('''def protocol_masks(pair, protocol):
    fool = pair["target_adv_wrong"]
    if protocol == "raw":
        cond = np.ones_like(fool, dtype=bool)
    elif protocol == "target_correct":
        cond = pair["target_clean_correct"]
    elif protocol == "both_correct":
        cond = pair["target_clean_correct"] & pair["source_clean_correct"]
    elif protocol == "successful_source":
        cond = pair["target_clean_correct"] & pair["source_adv_wrong"]
    else:
        raise ValueError(protocol)
    return fool, cond''',
     '''def protocol_masks(pair, protocol):
    """Maskeler src/analysis/protokoller.py'den (TEK KAYNAK)."""
    m = PROTO.maskeler(pair["target_clean_correct"], pair["source_clean_correct"],
                       pair["source_adv_wrong"], tani=True)
    if protocol not in m:
        raise ValueError(protocol)
    return pair["target_adv_wrong"], m[protocol]''',
     "protocol_masks"),
]

for eski, yeni, ad in CIFTLER:
    if t.count(eski) != 1:
        print(f"YAMA BASARISIZ ({ad}): {t.count(eski)} eslesme")
        sys.exit(1)
    t = t.replace(eski, yeni, 1)

p.write_text(t, encoding="utf-8")
print("yamalandi: a2b")
