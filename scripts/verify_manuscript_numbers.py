"""Makaledeki tasiyici sayilarin artefaktlarla tutarliligini denetler.

Her kontrol: (aciklama, artefaktdan hesaplanan deger, metinde gecmesi beklenen dize).
Metinde bulunamayan veya artefaktla uyusmayan her sey RAPOR EDILIR.
"""
import json
import re
from pathlib import Path

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
TEX = "\n".join((ROOT / "paper/manuscript" / p).read_text(encoding="utf-8")
                for p in ["main.tex", "sections/01_introduction.tex", "sections/02_related_work.tex",
                          "sections/03_methodology.tex", "sections/04_experiments.tex",
                          "sections/05_discussion.tex", "sections/06_conclusion.tex"])


def jl(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


seed = jl("results/c1_seeds/c1_seed_summary.json")["aggregate"]
tr = jl("results/c1_transfer/c1_transfer_summary.json")
c3 = jl("results/c1_c3/c3_summary.json")
beh = jl("results/c1_behavior_summary.json")
c45 = jl("results/c1_c45_summary.json")
c2 = [jl(f"results/c1_c2/pair{p}/tgr_summary.json") for p in (1, 2, 3)]


def ms(v):
    a = np.asarray(v, dtype=float)
    return a.mean(), a.std(ddof=1)


checks = []


def chk(label, value, text, nd=2):
    s = f"{value:.{nd}f}"
    checks.append((label, s, s in text.replace(",", "")))


txt = TEX.replace("{,}", "")
chk("AA ResNet", seed["resnet"]["aa"]["mean"], txt)
chk("AA ViT", seed["vit"]["aa"]["mean"], txt)
chk("kos. yaniltma PGD ResNet", seed["resnet"]["cond_fooling_pgd"]["mean"], txt)
chk("kos. yaniltma PGD ViT", seed["vit"]["cond_fooling_pgd"]["mean"], txt)
chk("kos. yaniltma AA ResNet", seed["resnet"]["cond_fooling_aa"]["mean"], txt)
chk("kos. yaniltma AA ViT", seed["vit"]["cond_fooling_aa"]["mean"], txt)
chk("hedef-dogru fark", tr["protocols"]["target_correct"]["diff"]["mean"], txt)
chk("her-ikisi-dogru fark", tr["protocols"]["both_correct"]["diff"]["mean"], txt)
chk("basarili-kaynak fark", tr["protocols"]["successful_source"]["diff"]["mean"], txt)
chk("protokol yayilimi", tr["protocol_spread_pp"]["mean"], txt)
chk("C3 r", c3["raw_minus_cond_vs_target_error"]["pearson_r"], txt, 3)
chk("C3 gelen-transfer r", c3["incoming_transfer_vs_own_vulnerability"]["pearson_r"], txt, 3)
chk("Hoyer ResNet", beh["gradient"]["ResNet18_AT"]["sparsity_hoyer"]["mean"], txt, 4)
chk("Hoyer ViT", beh["gradient"]["ViT_Tiny_AT"]["sparsity_hoyer"]["mean"], txt, 4)
chk("alan50 ResNet", c45["spatial"]["energy_area_50pct"]["resnet"][0], txt, 4)
chk("alan50 ViT", c45["spatial"]["energy_area_50pct"]["vit"][0], txt, 4)
chk("TGR hedef-dogru", ms([d["tgr"]["transfer_target_correct"] for d in c2])[0], txt)
chk("MI hedef-dogru", ms([d["mi"]["transfer_target_correct"] for d in c2])[0], txt)
chk("ResNet layer4.0 kosinus", c45["resnet_drift"]["layer4.0"]["cos"][0], txt, 4)

bad = [c for c in checks if not c[2]]
for label, val, ok in checks:
    print(f"{'OK ' if ok else 'EKSIK'} {label:32s} {val}")
print(f"\nTOPLAM={len(checks)} EKSIK={len(bad)}")
