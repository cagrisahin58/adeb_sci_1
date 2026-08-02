"""Dergi metninin yeniden yazimi icin TEK referans foyu uretir.

Butun C1 artefaktlarini okuyup makalede gececek her sayiyi tek dosyada,
kaynagiyla birlikte toplar. Amac: metne elle sayi tasirken hata yapmamak ve
her sayinin hangi dosyadan geldigini gorebilmek.

Cikti: results/C1_REFERANS_FOYU.md
"""
import json
import os

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
PAIRS = [1, 2, 3]
L = []


def load(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def ms(vals):
    a = np.asarray(vals, dtype=float)
    return a.mean(), (a.std(ddof=1) if a.size > 1 else 0.0)


def fmt(vals, nd=2):
    m, s = ms(vals)
    return f"{m:.{nd}f}$\\pm${s:.{nd}f}"


def sec(title, source):
    L.append(f"\n## {title}\n")
    L.append(f"_Kaynak: `{source}`_\n")


L.append("# C1 Referans Foyu - dergi metni icin tum sayilar\n")
L.append("Her sayi 3 tohum ortalamasi $\\pm$ standart sapma (aksi belirtilmedikce), "
         "tam test kumesi (n=10.000), $\\eps=8/255$.\n")
L.append("> Bu dosya otomatik uretilir: `python scripts/build_reference_sheet.py`. "
         "Metne sayi tasirken buradan al; artefakt yollari her bolumun altinda.\n")

# --- Tablo I ---------------------------------------------------------------
ev = load("results/c1_eval_summary.json")
seed = load("results/c1_seeds/c1_seed_summary.json")
if ev and seed:
    sec("Tablo I: ana gurbuzluk", "results/c1_eval_summary.json + c1_seeds/c1_seed_summary.json")
    L.append("| Model | AT | Temiz | FGSM | PGD-10 | AA |")
    L.append("|---|---|---|---|---|---|")
    for key, name in (("resnet18_clean", "ResNet-18"), ("vit_tiny_clean", "ViT-Tiny")):
        d = ev.get(key)
        if d:
            L.append(f"| {name} | -- | {d['clean']['mean']:.2f}$\\pm${d['clean']['std']:.2f} | "
                     f"{d['fgsm']['mean']:.2f}$\\pm${d['fgsm']['std']:.2f} | "
                     f"{d['pgd']['mean']:.2f}$\\pm${d['pgd']['std']:.2f} | -- |")
    agg = seed["aggregate"]
    for key, name, ak in (("resnet18_at", "ResNet-18", "resnet"), ("vit_tiny_at", "ViT-Tiny", "vit")):
        d = ev.get(key)
        aa = agg[ak]["aa"]
        if d:
            L.append(f"| {name} | + | {d['clean']['mean']:.2f}$\\pm${d['clean']['std']:.2f} | "
                     f"{d['fgsm']['mean']:.2f}$\\pm${d['fgsm']['std']:.2f} | "
                     f"{d['pgd']['mean']:.2f}$\\pm${d['pgd']['std']:.2f} | "
                     f"{aa['mean']:.2f}$\\pm${aa['std']:.2f} |")
    L.append("\nWRN-28-10 (harici referans): temiz 89.48 / FGSM 70.91 / PGD 66.92 / AA 62.76 "
             "(AA degeri RobustBench raporu).\n")

# --- Tablo II --------------------------------------------------------------
if seed:
    agg = seed["aggregate"]
    sec("Tablo II: kosullu ayrisma", "results/c1_seeds/c1_seed_summary.json")
    L.append("| Model | Kos. yaniltma PGD | Kos. yaniltma AA | Her ikisi dogru PGD | Her ikisi dogru AA |")
    L.append("|---|---|---|---|---|")
    b = agg["both_correct"]
    L.append(f"| ResNet-18 AT | {agg['resnet']['cond_fooling_pgd']['mean']:.2f}$\\pm${agg['resnet']['cond_fooling_pgd']['std']:.2f} | "
             f"{agg['resnet']['cond_fooling_aa']['mean']:.2f}$\\pm${agg['resnet']['cond_fooling_aa']['std']:.2f} | "
             f"{b['resnet_robust_pgd']['mean']:.2f}$\\pm${b['resnet_robust_pgd']['std']:.2f} | "
             f"{b['resnet_robust_aa']['mean']:.2f}$\\pm${b['resnet_robust_aa']['std']:.2f} |")
    L.append(f"| ViT-Tiny AT | {agg['vit']['cond_fooling_pgd']['mean']:.2f}$\\pm${agg['vit']['cond_fooling_pgd']['std']:.2f} | "
             f"{agg['vit']['cond_fooling_aa']['mean']:.2f}$\\pm${agg['vit']['cond_fooling_aa']['std']:.2f} | "
             f"{b['vit_robust_pgd']['mean']:.2f}$\\pm${b['vit_robust_pgd']['std']:.2f} | "
             f"{b['vit_robust_aa']['mean']:.2f}$\\pm${b['vit_robust_aa']['std']:.2f} |")
    L.append(f"\nOrtak kume n = {b['n_aa']['mean']:.0f}$\\pm${b['n_aa']['std']:.0f}. "
             f"Ayrisma ornegi (AA): {agg['resnet']['clean']['mean']:.2f} x "
             f"{100 - agg['resnet']['cond_fooling_aa']['mean']:.1f}% = {agg['resnet']['aa']['mean']:.2f} (CNN), "
             f"{agg['vit']['clean']['mean']:.2f} x {100 - agg['vit']['cond_fooling_aa']['mean']:.1f}% = "
             f"{agg['vit']['aa']['mean']:.2f} (ViT).")
    L.append(f"\nEski tek kosu (sizintili) karsilastirmasi: kos. yaniltma PGD 52.15 vs 52.33, "
             f"AA 58.16 vs 56.46; her ikisi dogru PGD 54.92 vs 49.61, AA 48.15 vs 45.33 (n=7260).\n")
    L.append("McNemar (kosu bazinda, tam binom): ")
    for r in seed["pairs"]:
        L.append(f"- cift {r['pair']}: PGD p={r['mcnemar_pgd']['p_exact']:.1e} "
                 f"({r['mcnemar_pgd']['resnet_only']}/{r['mcnemar_pgd']['vit_only']}), "
                 f"AA p={r['mcnemar_aa']['p_exact']:.1e} "
                 f"({r['mcnemar_aa']['resnet_only']}/{r['mcnemar_aa']['vit_only']})")

# --- Tablo III -------------------------------------------------------------
tr = load("results/c1_transfer/c1_transfer_summary.json")
if tr:
    sec("Tablo III: transfer protokolleri", "results/c1_transfer/c1_transfer_summary.json")
    labels = {"raw": "Kosulsuz (ham)", "target_correct": "Hedef dogru",
              "both_correct": "Her ikisi dogru", "successful_source": "Basarili kaynak"}
    L.append("| Protokol | CNN->ViT | ViT->CNN | Fark | N (CNN->ViT / ViT->CNN) | run3 fark |")
    L.append("|---|---|---|---|---|---|")
    for k, lab in labels.items():
        p = tr["protocols"][k]
        L.append(f"| {lab} | {p['CNN_to_ViT']['mean']:.2f}$\\pm${p['CNN_to_ViT']['std']:.2f} | "
                 f"{p['ViT_to_CNN']['mean']:.2f}$\\pm${p['ViT_to_CNN']['std']:.2f} | "
                 f"{p['diff']['mean']:+.2f}$\\pm${p['diff']['std']:.2f} | "
                 f"{p['n_cond_CNN_to_ViT']['mean']:.0f} / {p['n_cond_ViT_to_CNN']['mean']:.0f} | "
                 f"{p.get('old_run3_diff', '-')} |")
    bp = tr["both_correct_paired"]
    L.append(f"\nEslesmis analiz: fark {bp['diff_pp']['mean']:.2f}$\\pm${bp['diff_pp']['std']:.2f} puan, "
             f"bootstrap GA [{bp['ci_low']['mean']:.2f}; {bp['ci_high']['mean']:.2f}], "
             f"isaret-cevirme permutasyon p (en buyuk) = {bp['perm_p_max']}, "
             f"TOST esdegerligi hicbir marjda saglanmiyor.")
    L.append(f"\nProtokol yayilimi: {tr['protocol_spread_pp']['mean']:.2f}$\\pm${tr['protocol_spread_pp']['std']:.2f} puan "
             f"(en buyuk/en kucuk protokol tahmini orani ~"
             f"{tr['protocols']['successful_source']['diff']['mean'] / tr['protocols']['target_correct']['diff']['mean']:.1f} kat).\n")

# --- C3 --------------------------------------------------------------------
c3 = load("results/c1_c3/c3_summary.json")
if c3:
    sec("C3: WRN dahil 3x3 matris", "results/c1_c3/c3_summary.json")
    L.append("| kaynak -> hedef | ham | kosullu | ham - kosullu |")
    L.append("|---|---|---|---|")
    for k, v in c3.items():
        if "->" not in k:
            continue
        L.append(f"| {k.replace('->', ' -> ')} | {v['raw'][0]:.2f}$\\pm${v['raw'][1]:.2f} | "
                 f"{v['cond'][0]:.2f}$\\pm${v['cond'][1]:.2f} | {v['raw_minus_cond']:+.2f} |")
    r = c3.get("raw_minus_cond_vs_target_error", {})
    if r:
        L.append(f"\n(ham - kosullu) ile hedefin temiz hatasi: Pearson r = {r['pearson_r']:.3f}, "
                 f"egim {r['slope']:.3f} ({r['n_offdiagonal']} kosegen disi yon).")
    inc = c3.get("incoming_transfer_vs_own_vulnerability", {})
    if inc:
        L.append(f"\nGelen transfer ile hedefin kendi kirilganligi: r = {inc['pearson_r']:.3f} "
                 f"(hedefler: {', '.join(inc['targets'])}; kendi kosullu yaniltma "
                 f"{[round(x, 2) for x in inc['own_whitebox_cond_fooling']]}, gelen transfer "
                 f"{[round(x, 2) for x in inc['mean_incoming_cond_fooling']]}).\n")

# --- Gradyan ---------------------------------------------------------------
beh = load("results/c1_behavior_summary.json")
if beh and "gradient" in beh:
    sec("Gradyan yapisi", "results/c1_behavior_summary.json + results/c1_a3/pair*/")
    g = beh["gradient"]
    L.append("| Olcut | ResNet-18 AT | ViT-Tiny AT |")
    L.append("|---|---|---|")
    names = {"sparsity_hoyer": "Hoyer", "sparsity_gini": "Gini",
             "sparsity_rel_threshold": "Rel-esik (%1 alti)", "gradient_alignment": "Hizalanma (mutlak kosinus)"}
    for k, lab in names.items():
        L.append(f"| {lab} | {g['ResNet18_AT'][k]['mean']:.4f}$\\pm${g['ResNet18_AT'][k]['std']:.4f} | "
                 f"{g['ViT_Tiny_AT'][k]['mean']:.4f}$\\pm${g['ViT_Tiny_AT'][k]['std']:.4f} |")
    a3 = [load(f"results/c1_a3/pair{p}/a3_gradient_paired.json") for p in PAIRS]
    if all(a3):
        for m in ("hoyer", "gini", "rel"):
            ds = [x["paired_sparsity_ResNet_vs_ViT"][m]["cohens_d_paired"] for x in a3]
            ps = [x["paired_sparsity_ResNet_vs_ViT"][m]["wilcoxon_p_holm"] for x in a3]
            L.append(f"\n- {m}: Cohen d {min(ds):.2f}-{max(ds):.2f}, Holm p max {max(ps):.1e}")
        sg = [abs(x["alignment"][k]["all_pairs_signed_mean"]) for x in a3 for k in ("ResNet18_AT", "ViT_Tiny_AT")]
        L.append(f"- isaretli ortalama kosinus (mutlak deger) en buyuk: {max(sg):.4f}")
    cg = beh.get("clean_gradient", {}).get("per_pair")
    if cg:
        for m, lab in (("ResNet18_clean", "ResNet temiz"), ("ViT_Tiny_clean", "ViT temiz")):
            h = [p["statistics"][m]["hoyer_mean"] for p in cg]
            al = [p["statistics"][m]["align_mean"] for p in cg]
            L.append(f"- {lab}: Hoyer {fmt(h, 4)}, hizalanma {fmt(al, 4)}")

# --- C4 / C5 ---------------------------------------------------------------
c45 = load("results/c1_c45_summary.json")
if c45:
    sec("C4: oznitelik kaymasi ve attention (n=1000)", "results/c1_c45_summary.json")
    mins = c45.get("vit_drift_minima", {})
    for k, v in mins.items():
        L.append(f"- {k}: minimum blok {v[0]}, deger {v[1]:.4f}")
    rd = c45.get("resnet_drift", {})
    if rd:
        keys = list(rd)
        L.append(f"- ResNet: {keys[-2]} kosinus {rd[keys[-2]]['cos'][0]:.4f}$\\pm${rd[keys[-2]]['cos'][1]:.4f} "
                 f"(norm {rd[keys[-2]]['norm'][0]:+.2f}%), {keys[-1]} kosinus "
                 f"{rd[keys[-1]]['cos'][0]:.4f}$\\pm${rd[keys[-1]]['cos'][1]:.4f} "
                 f"(norm {rd[keys[-1]]['norm'][0]:+.2f}%)")
    at = c45.get("attention", {})
    if at:
        ed = np.asarray(at["entropy_delta_mean"])
        dp = np.asarray(at["displacement_mean"])
        L.append(f"- attention entropi degisimi: tum katmanlarda |delta| <= {np.abs(ed).max():.4f}")
        L.append(f"- CLS yer degistirmesi: {dp.min():.4f} (katman 1) -> {dp.max():.4f} (en derin)")
    fs = c45.get("flip_split_last_block")
    if fs:
        L.append(f"- ViT son blok, devrilen {fs['flipped'][0]:.4f} vs devrilmeyen {fs['not_flipped'][0]:.4f}")

    sec("C5: mekansal lokalite (n=500)", "results/c1_c45_summary.json")
    L.append("| Olcut | ResNet | ViT | Fark (R-V) | Wilcoxon p (en buyuk) |")
    L.append("|---|---|---|---|---|")
    sp = c45.get("spatial", {})
    labs = {"energy_area_50pct": "Enerji %50 alani", "energy_area_90pct": "Enerji %90 alani",
            "spatial_entropy": "Mekansal entropi", "morans_i": "Moran's I"}
    for k, lab in labs.items():
        v = sp.get(k)
        if v:
            L.append(f"| {lab} | {v['resnet'][0]:.4f}$\\pm${v['resnet'][1]:.4f} | "
                     f"{v['vit'][0]:.4f}$\\pm${v['vit'][1]:.4f} | {v['diff'][0]:+.4f} | {v['p_max']:.2e} |")
    L.append("\n**Negatif sonuc:** mekansal lokalite farki yok; makalede yalnizca 'daha seyrek' "
             "denebilir, 'daha lokalize/yogunlasmis' denemez.\n")

# --- C2 --------------------------------------------------------------------
c2 = [load(f"results/c1_c2/pair{p}/tgr_summary.json") for p in PAIRS]
if all(c2):
    sec("C2: TGR vs MI-FGSM (ViT -> CNN)", "results/c1_c2/pair*/tgr_summary.json")
    L.append("| Olcut | TGR | MI-FGSM |")
    L.append("|---|---|---|")
    for key, lab in (("whitebox_source_fooling_raw", "Kaynakta beyaz kutu (ham)"),
                     ("transfer_target_correct", "Transfer, hedef dogru"),
                     ("transfer_both_correct", "Transfer, her ikisi dogru")):
        L.append(f"| {lab} | {fmt([d['tgr'][key] for d in c2])} | {fmt([d['mi'][key] for d in c2])} |")
    L.append(f"\nEslesmis McNemar (her ikisi dogru): " +
             ", ".join(f"cift {d['pair']} p={d['mcnemar_both_correct']['p_exact']:.2e}" for d in c2))
else:
    L.append("\n## C2: TGR\n\n_Kosum devam ediyor; bittiginde bu bolum dolacak._\n")

out = os.path.join(ROOT, "results/C1_REFERANS_FOYU.md")
with open(out, "w", encoding="utf-8") as fh:
    fh.write("\n".join(L) + "\n")
print("\n".join(L))
print(f"\nkaydedildi: {out}")
