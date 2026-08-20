"""C1 transfer protokol sonuclarini 3 tohum uzerinden toplulastirir.

Girdi : results/c1_transfer/pair{1,2,3}/a2_transfer_protocols.json
Eski  : results/rev2_blockA/a2_transfer_protocols.json (tek kosu, sizintili)
Cikti : results/c1_transfer/c1_transfer_summary.json + C1_TRANSFER_RAPORU.md
"""
import json
import os

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
# Girdi/cikti koku ortam degiskeniyle degistirilebilir: AYNI toplulastirma
# kodunu E1 (CIFAR-100) protokol sonuclarina da uygulayabilmek icin.
IN = os.path.join(ROOT, os.environ.get("AGG_IN_DIR", "results/c1_transfer"))
_old_rel = os.environ.get("AGG_OLD", "results/rev2_blockA/a2_transfer_protocols.json")
OLD = os.path.join(ROOT, _old_rel) if _old_rel else None
# IS-6(e): baslik ve rapor dosya adi SABITTI -> CIFAR-100 ciktisi 'C1'
# basligiyla ureiliyordu ve KARANTINA kurali acisindan karistirma riski
# tasiyordu (C1 = CIFAR-10 sizinti-duzeltmeli kampanya). Artik ortamdan.
TITLE = os.environ.get("AGG_TITLE", "C1 Transfer Protokolleri - 3 Tohum")
MD_NAME = os.environ.get("AGG_MD_NAME", "C1_TRANSFER_RAPORU.md")
DESC = os.environ.get(
    "AGG_DESC",
    "Ayni istatistik kodu (a2_transfer_protocols.py), C1 sizinti-duzeltmeli kontrol "
    "noktalarina uygulandi. Her satir 3 tohum ortalamasi +- std.")
PROTOCOLS = ["raw", "target_correct", "both_correct", "successful_source"]
LABELS = {
    "raw": "Kosulsuz (ham)",
    "target_correct": "Hedef dogru",
    "both_correct": "Her ikisi dogru",
    "successful_source": "Basarili kaynak",
}

pairs = []
for p in (1, 2, 3):
    with open(os.path.join(IN, f"pair{p}/a2_transfer_protocols.json"), encoding="utf-8") as fh:
        pairs.append(json.load(fh))

old = None
if OLD and os.path.exists(OLD):
    with open(OLD, encoding="utf-8") as fh:
        old = json.load(fh)


def ms(vals):
    a = np.asarray(vals, dtype=float)
    return {"mean": float(a.mean()), "std": float(a.std(ddof=1)), "values": [float(v) for v in a]}


agg = {"protocols": {}, "both_correct_paired": {}}
for proto in PROTOCOLS:
    agg["protocols"][proto] = {
        "CNN_to_ViT": ms([d["protocols"][proto]["CNN_to_ViT"]["rate"] for d in pairs]),
        "ViT_to_CNN": ms([d["protocols"][proto]["ViT_to_CNN"]["rate"] for d in pairs]),
        "diff": ms([d["protocols"][proto]["diff_CNNtoViT_minus_ViTtoCNN"] for d in pairs]),
        "n_cond_CNN_to_ViT": ms([d["protocols"][proto]["CNN_to_ViT"]["n_conditioned"] for d in pairs]),
        "n_cond_ViT_to_CNN": ms([d["protocols"][proto]["ViT_to_CNN"]["n_conditioned"] for d in pairs]),
    }
    if old and proto in old.get("protocols", {}):
        agg["protocols"][proto]["old_run3_diff"] = old["protocols"][proto]["diff_CNNtoViT_minus_ViTtoCNN"]

agg["both_correct_paired"] = {
    "n_common": ms([d["both_correct_paired"]["n_common"] for d in pairs]),
    "diff_pp": ms([d["both_correct_paired"]["diff_pp"] for d in pairs]),
    "ci_low": ms([d["both_correct_paired"]["paired_bootstrap_ci95_pp"][0] for d in pairs]),
    "ci_high": ms([d["both_correct_paired"]["paired_bootstrap_ci95_pp"][1] for d in pairs]),
    "perm_p_max": max(d["both_correct_paired"]["signflip_permutation_p"] for d in pairs),
    "tost_equivalent_any": any(
        d["both_correct_paired"]["tost_sensitivity"][m]["equivalent_at_0.05"]
        for d in pairs
        for m in ("margin_1pp", "margin_2pp", "margin_3pp")
    ),
}
if old:
    agg["both_correct_paired"]["old_run3_diff_pp"] = old["both_correct_paired"]["diff_pp"]

# protokolun yarattigi yayilim: en buyuk - en kucuk fark (tohum basina)
spread = [
    max(d["protocols"][p]["diff_CNNtoViT_minus_ViTtoCNN"] for p in PROTOCOLS)
    - min(d["protocols"][p]["diff_CNNtoViT_minus_ViTtoCNN"] for p in PROTOCOLS)
    for d in pairs
]
agg["protocol_spread_pp"] = ms(spread)

out_json = os.path.join(IN, os.environ.get("AGG_OUT_NAME", "c1_transfer_summary.json"))
with open(out_json, "w", encoding="utf-8") as fh:
    json.dump(agg, fh, indent=2, ensure_ascii=False)


def f(x, n=2):
    return f"{x:.{n}f}"


L = []
L.append(f"# {TITLE}\n")
L.append(
    DESC + "\n"
)
L.append("| Protokol | CNN->ViT | ViT->CNN | Fark | run3 fark |")
L.append("|---|---|---|---|---|")
for proto in PROTOCOLS:
    a = agg["protocols"][proto]
    oldv = a.get("old_run3_diff")
    L.append(
        f"| {LABELS[proto]} | {f(a['CNN_to_ViT']['mean'])} +- {f(a['CNN_to_ViT']['std'])} | "
        f"{f(a['ViT_to_CNN']['mean'])} +- {f(a['ViT_to_CNN']['std'])} | "
        f"**{f(a['diff']['mean'])} +- {f(a['diff']['std'])}** | "
        f"{('+' + f(oldv)) if oldv is not None else '-'} |"
    )

bp = agg["both_correct_paired"]
L.append("\n## Her ikisi dogru eslesmis analiz\n")
L.append(f"- Ortak kume n = {f(bp['n_common']['mean'], 0)} +- {f(bp['n_common']['std'], 0)}")
L.append(f"- Fark = {f(bp['diff_pp']['mean'])} +- {f(bp['diff_pp']['std'])} puan (run3: {bp.get('old_run3_diff_pp', '-')})")
L.append(f"- Eslesmis bootstrap GA (ort): [{f(bp['ci_low']['mean'])}; {f(bp['ci_high']['mean'])}]")
L.append(f"- Isaret cevirme permutasyon p (en buyuk): {bp['perm_p_max']}")
L.append(f"- Herhangi bir tohum/marjda TOST esdegerligi: {'EVET' if bp['tost_equivalent_any'] else 'HAYIR'}")
L.append(
    f"\n## Protokolun yarattigi yayilim\n\nAyni modeller, ayni veri: en buyuk ve en kucuk protokol farki "
    f"arasindaki mesafe {f(agg['protocol_spread_pp']['mean'])} +- {f(agg['protocol_spread_pp']['std'])} puan.\n"
)

out_md = os.path.join(IN, MD_NAME)
with open(out_md, "w", encoding="utf-8") as fh:
    fh.write("\n".join(L) + "\n")
print("\n".join(L))
