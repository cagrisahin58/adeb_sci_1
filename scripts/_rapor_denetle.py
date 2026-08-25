#!/usr/bin/env python3
"""HIKAYE_VE_POSTER_RAPORU.md icindeki her sayiyi artefaktlara karsi denetler.

Rapor da disariya cikan bir belgedir; karantina kurali ona da uygulanir.
"""
import json
import re
from pathlib import Path

ROOT = Path("/workspace")
RAPOR = (ROOT / "results/q1_research/HIKAYE_VE_POSTER_RAPORU.md").read_text(
    encoding="utf-8")
# SIRA ONEMLI: once binlik ayracini (TR'de NOKTA) sil, sonra ondalik
# virgulu noktaya cevir. Ters sira "0,056" -> "0.056" -> "0056" yapar ve
# dogru bir sayiyi "bulunamadi" diye raporlar.
metin = re.sub(r"(?<=\d)\.(?=\d{3}(?!\d))", "", RAPOR)
metin = re.sub(r"(?<=\d),(?=\d)", ".", metin)
metin = metin.replace("\u2212", "-")          # Unicode eksi -> ASCII


def jl(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


tr = jl("results/c1_transfer/c1_transfer_summary.json")
seed = jl("results/c1_seeds/c1_seed_summary.json")["aggregate"]
beh = jl("results/c1_behavior_summary.json")
c3 = jl("results/c1_c3/c3_summary.json")
e7 = jl("results/q1/svhn/transfer/e7_transfer_summary.json")
e7s = jl("results/q1/e7_svhn_summary.json")
vr = jl("results/q1/variance_ratio.json")
c45 = jl("results/c1_c45_summary.json")
c2 = [jl(f"results/c1_c2/pair{p}/tgr_summary.json") for p in (1, 2, 3)]

K = []


def k(ad, deger, nd=2):
    K.append((ad, f"{deger:.{nd}f}"))


k("protokol yayilimi", tr["protocol_spread_pp"]["mean"])
k("yayilim sd", tr["protocol_spread_pp"]["std"])
k("hedef dogru fark", tr["protocols"]["target_correct"]["diff"]["mean"], 1)
k("her ikisi dogru fark", tr["protocols"]["both_correct"]["diff"]["mean"], 1)
k("ham fark", tr["protocols"]["raw"]["diff"]["mean"], 1)
k("basarili kaynak fark", tr["protocols"]["successful_source"]["diff"]["mean"], 1)
k("kosum sd min", vr["PAYDA_kosum_etkisi_AYNI_NICELIK"]["sd_min"])
k("kosum sd max", vr["PAYDA_kosum_etkisi_AYNI_NICELIK"]["sd_max"])
k("AA ResNet", seed["resnet"]["aa"]["mean"])
k("AA ViT", seed["vit"]["aa"]["mean"])
k("kos yaniltma ResNet", seed["resnet"]["cond_fooling_pgd"]["mean"])
k("kos yaniltma ViT", seed["vit"]["cond_fooling_pgd"]["mean"])
k("Hoyer ResNet", beh["gradient"]["ResNet18_AT"]["sparsity_hoyer"]["mean"], 4)
k("Hoyer ViT", beh["gradient"]["ViT_Tiny_AT"]["sparsity_hoyer"]["mean"], 4)
k("hizalanma ResNet", beh["gradient"]["ResNet18_AT"]["gradient_alignment"]["mean"], 3)
k("hizalanma ViT", beh["gradient"]["ViT_Tiny_AT"]["gradient_alignment"]["mean"], 3)
k("SVHN hedef dogru", e7["protocols"]["target_correct"]["diff"]["mean"])
k("SVHN her ikisi dogru", e7["protocols"]["both_correct"]["diff"]["mean"])
k("SVHN ham", e7["protocols"]["raw"]["diff"]["mean"])
k("SVHN basarili kaynak", e7["protocols"]["successful_source"]["diff"]["mean"])
for p in ("raw", "target_correct", "both_correct", "successful_source"):
    v = tr["protocols"][p]
    k(f"n {p} ileri", v["n_cond_CNN_to_ViT"]["mean"], 0)
    k(f"n {p} geri", v["n_cond_ViT_to_CNN"]["mean"], 0)

eksik = []
print(f"{'BUYUKLUK':28s}{'DEGER':>10s}  DURUM")
print("-" * 52)
for ad, v in K:
    var = re.search(r"(?<![\d.])" + re.escape(v) + r"(?!\d)", metin) is not None
    print(f"{ad:28s}{v:>10s}  {'OK' if var else 'YOK'}")
    if not var:
        eksik.append((ad, v))

print()
if eksik:
    print(f"RAPORDA BULUNAMAYAN: {len(eksik)}")
    for ad, v in eksik:
        print(f"  - {ad} = {v}")
else:
    print("RAPORUN HER SAYISI ARTEFAKTLA TUTUYOR")
