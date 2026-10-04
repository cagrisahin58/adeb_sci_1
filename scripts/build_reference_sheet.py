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


def _bc_mcnemar_satiri():
    """HER-IKISI-DOGRU altkumesinde McNemar (PGD ve AA), ornek bazindan.

    Makale 04:64 bu altkumenin sinirini veriyor. Sinir bir sure TAM KUME
    degerinden odunc alinmisti (1e-84); gercek altkume degeri daha zayif.
    Foy artik bunu kendisi uretir ki metne dogru olan girsin.
    """
    import glob
    from scipy import stats
    KS = os.path.join(ROOT, "results/c1_seeds")
    TOHUM = {1: (1001, 2001), 2: (1002, 2002), 3: (1003, 2003)}

    def mcn(b, c):
        n = b + c
        return 1.0 if n == 0 else float(
            stats.binomtest(min(b, c), n, 0.5, alternative="two-sided").pvalue)

    def aa(pair, ad):
        par = sorted(glob.glob(os.path.join(KS, f"pair{pair}/aa_chunk_{ad}_*.npz")))
        return np.concatenate([np.load(p)["robust_correct"] for p in par]) if par else None

    satir, pg, ap = [], [], []
    for pair, (rs, vs) in TOHUM.items():
        try:
            zr = np.load(os.path.join(KS, f"pair{pair}/pgd_per_sample_resnet18_s{rs}.npz"))
            zv = np.load(os.path.join(KS, f"pair{pair}/pgd_per_sample_vit_tiny_s{vs}.npz"))
        except OSError:
            continue
        ortak = zr["clean_correct"] & zv["clean_correct"]
        R, V = zr["robust_correct"][ortak], zv["robust_correct"][ortak]
        p1 = mcn(int((R & ~V).sum()), int((~R & V).sum()))
        pg.append(p1)
        rr, rv = aa(pair, "ResNet18_AT"), aa(pair, "ViT_Tiny_AT")
        p2 = None
        if rr is not None and rv is not None and len(rr) == len(ortak):
            Ra, Va = rr[ortak], rv[ortak]
            p2 = mcn(int((Ra & ~Va).sum()), int((~Ra & Va).sum()))
            ap.append(p2)
        satir.append(f"- cift {pair}: n_ortak={int(ortak.sum())}, PGD p={p1:.2e}"
                     + (f", AA p={p2:.2e}" if p2 is not None else ""))
    if not satir:
        return "\nHER-IKISI-DOGRU McNemar: ornek bazli dosyalar bulunamadi.\n"
    ust = max(pg + ap) if (pg or ap) else 1.0
    return ("\nHER-IKISI-DOGRU altkumesinde McNemar (tam binom, ornek bazindan):\n"
            + "\n".join(satir)
            # DIKKAT: floor DEGIL ceil. max p = 5.90e-68 icin floor 68 verir
            # ama 5.90e-68 > 1e-68'dir; dogru sinir 1e-67'dir.
            + f"\n  -> metne girecek ORTAK sinir: p < 1e-{int(-np.ceil(np.log10(ust)))}"
              "  (TAM KUME sinirindan ZAYIFTIR, onunla karistirilmamalidir)\n")


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


C4 = [load(f"results/c1_c4/pair{p}/c4_summary.json") for p in PAIRS]
C4_OK = all(C4)
C4_BLOK_ANAHTAR = (("CLS (cos_block_cls)", "cos_block_cls"),
                   ("Yama ortalamasi (cos_block_token_mean)", "cos_block_token_mean"),
                   ("Tum jetonlar (cos_block_output)", "cos_block_output"))


def _c4_blok_cikisi():
    """ViT residual blok CIKISI kosinusu: {etiket: (kosum ortalamasi[12], kosumlar arasi SD[12])}.

    Her kosumun kendi ortalamasi c4_summary.json icinde; kosumlar arasi SD ddof=1.
    """
    if not C4_OK:
        return None
    cikti = {}
    for ad, k in C4_BLOK_ANAHTAR:
        a = np.array([[d["vit"][k][f"block{i}"]["mean"] for i in range(12)] for d in C4])
        cikti[ad] = (a.mean(0), a.std(0, ddof=1))
    return cikti


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
    # 2026-10-04: bu satirdaki sayilar ARTEFAKTTAN OKUNMAZ; karantinadaki eski
    # (C1 oncesi, sizintili) tek kosudan elle tasinmis LITERALDIR. Silinmedi
    # (makale Tablo 2 alt blogu bunu basiyor); foyde acikca etiketlendi ve
    # "Sabit dizgeler" bolumunde dokumu yapildi.
    L.append(f"\n[ELLE TASINMIS LITERAL, karantinadaki eski kosudan, artefaktla DOGRULANMADI; "
             f"bkz. 'Sabit dizgeler' bolumu] "
             f"Eski tek kosu (sizintili) karsilastirmasi: kos. yaniltma PGD 52.15 vs 52.33, "
             f"AA 58.16 vs 56.46; her ikisi dogru PGD 54.92 vs 49.61, AA 48.15 vs 45.33 (n=7260).\n")
    # TUR 4: makale 04:64'te HER-IKISI-DOGRU altkumesinin McNemar sinirini
    # veriyor. O sinir asagidaki TAM KUME degerlerinden ZAYIFTIR ve bir
    # sure tam kumeden odunc alinmisti. Foy artik ikisini de tasiyor ki
    # metne dogru olan girsin (KARANTINA kurali: her sayi foyden).
    L.append(_bc_mcnemar_satiri())
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
    # 2026-10-04 (hakem paneli Y8): manset artik BLOK CIKISI olcumleridir
    # (makale Tablo 10 ve metni bunlari basiyor); MLP alt-blok serisi
    # duyarlilik analizi olarak altta kalir.
    _bo = _c4_blok_cikisi()
    if _bo:
        L.append("**MANSET: residual BLOK CIKISI (makale Tablo 10), uc kosum ortalamasi; "
                 "blok numaralari 1-tabanli, SD kosumlar arasi**\n")
        for _ad, (_ort, _sd) in _bo.items():
            _k = int(np.argmin(_ort))
            L.append(f"- {_ad}: minimum blok {_k + 1}, deger {_ort[_k]:.4f}$\\pm${_sd[_k]:.4f}")
        _ck = int(np.argmin(_bo["CLS (cos_block_cls)"][0]))
        _pk = int(np.argmin(_bo["Yama ortalamasi (cos_block_token_mean)"][0]))
        _c = _bo["CLS (cos_block_cls)"][0][_ck]
        _pm = _bo["Yama ortalamasi (cos_block_token_mean)"][0][_pk]
        L.append(f"- Oran (1 - cos) CLS minimumu / yama ortalamasi minimumu = "
                 f"{(1 - _c) / (1 - _pm):.2f} (ham ortalamalardan)")
        L.append("\nMLP alt-blok cikisi serisi (DUYARLILIK analizi; manset DEGIL; "
                 "kaynak c1_c45_summary.json vit_drift_minima, blok 1-tabanli):")
    mins = c45.get("vit_drift_minima", {})
    for k, v in mins.items():
        _et = "blok cikisi, tum jetonlar" if k == "cos_block_output" else "MLP alt-blok"
        L.append(f"- {k} ({_et}): minimum blok {v[0]}, deger {v[1]:.4f}")
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

# ===========================================================================
# GENISLETME 2026-10-04 (hakem paneli, raporlar/hakem_lecun_2026-10-04,
# mercek D Y8 ve LECUN_HUKUM B4): foyde olmayan basili sayilari ekler.
# Her sayi artefakttan okunur; hicbir sayi elle yazilmaz. Bulunamayan
# artefakt "ARTEFAKT YOK" notuyla yazilir. Mevcut bolumlere dokunulmaz.
# Karantina yollarindan (run1, run2, run3, attention_analysis_run3,
# stat_addendum, rev2_blockA) OKUNMAZ.
# ===========================================================================
import csv

from scipy import stats


def yok(rel):
    L.append(f"\n_ARTEFAKT YOK: `{rel}` bulunamadi; bu bolumdeki sayilar uretilemedi._\n")


def sg(x, nd=2, plus=False):
    return f"{x:+.{nd}f}" if plus else f"{x:.{nd}f}"


def hucre(vals, nd=2, plus=True):
    """3 deger: ort$\\pm$SD (ddof=1). 2 deger (SVHN): iki deger AYRI AYRI, SD yazilmaz."""
    a = np.asarray(vals, dtype=float)
    if a.size == 2:
        return " / ".join(sg(v, nd, plus) for v in a)
    m, s = ms(a)
    return f"{sg(m, nd, plus)}$\\pm${s:.{nd}f}"


def t_aralik(vals, conf=0.95):
    """Kosum duzeyi t araligi: ortalama +- t_{(1+conf)/2, n-1} * SD / sqrt(n)."""
    a = np.asarray(vals, dtype=float)
    m, s = ms(a)
    tk = float(stats.t.ppf(0.5 + conf / 2, a.size - 1))
    h = tk * s / np.sqrt(a.size)
    return m, s, m - h, m + h, tk


def holm(ps):
    """Holm-Bonferroni duzeltilmis p (girdi sirasiyla)."""
    ps = np.asarray(ps, dtype=float)
    sira = np.argsort(ps)
    m = ps.size
    cikti = np.empty(m)
    onceki = 0.0
    for r, i in enumerate(sira):
        onceki = max(onceki, min(1.0, (m - r) * ps[i]))
        cikti[i] = onceki
    return cikti


def _satir(ipucu):
    """Bu betikte `ipucu` gecen ilk satirin numarasi (cagri satirinin kendisi sayilmaz)."""
    with open(__file__, encoding="utf-8") as fh:
        for i, s in enumerate(fh, 1):
            if ipucu in s and "_satir(" not in s:
                return i
    return None


PROTO = [("raw", "Unconditioned (raw)"), ("target_correct", "Target-correct"),
         ("both_correct", "Both-correct"), ("successful_source", "Successful-source")]
AYARLAR = [
    ("CIFAR-10 Linf", "results/c1_transfer/c1_transfer_summary.json",
     "results/c1_transfer/pair{p}/a2_transfer_protocols.json", [1, 2, 3]),
    ("CIFAR-100 Linf", "results/q1/cifar100/transfer/e1_transfer_summary.json",
     "results/q1/cifar100/transfer/pair{p}/a2_transfer_protocols.json", [1, 2, 3]),
    ("SVHN Linf", "results/q1/svhn/transfer/e7_transfer_summary.json",
     "results/q1/svhn/transfer/pair{p}/a2_transfer_protocols.json", [1, 2]),
    ("CIFAR-10 L2", "results/q1/cifar10_l2/transfer/e6_l2_transfer_summary.json",
     "results/q1/cifar10_l2/transfer/pair{p}/a2_transfer_protocols.json", [1, 2, 3]),
]
S = {}
for _ad, _oy, _ay, _cift in AYARLAR:
    _d = load(_oy)
    if _d is None:
        S[_ad] = None
        continue
    # Kosum basina hucre: CNN->ViT ve ViT->CNN oranlari (artefaktta 2 ondalikli),
    # fark ve yayilim BURADA tam hassasiyetle hesaplanir (yuvarlanmis ozetten degil).
    _cv = np.array([_d["protocols"][k]["CNN_to_ViT"]["values"] for k, _ in PROTO])
    _vc = np.array([_d["protocols"][k]["ViT_to_CNN"]["values"] for k, _ in PROTO])
    _D = _cv - _vc
    S[_ad] = dict(d=_d, cift=_cift, ozet=_oy, cv=_cv, vc=_vc, D=_D,
                  sprd=_D.max(0) - _D.min(0),
                  a2=[load(_ay.format(p=p)) for p in _cift],
                  n=int(round(_d["protocols"]["raw"]["n_cond_CNN_to_ViT"]["mean"])))
AD = [a for a, *_ in AYARLAR]

# --- 1. Protokol x ayar tablosu ---------------------------------------------
sec("Transfer asimetrisi, dort protokol, ayarlar",
    "results/c1_transfer/c1_transfer_summary.json; results/q1/cifar100/transfer/e1_transfer_summary.json; "
    "results/q1/svhn/transfer/e7_transfer_summary.json; results/q1/cifar10_l2/transfer/e6_l2_transfer_summary.json")
L.append("Hucre = CNN->ViT eksi ViT->CNN (yuzde puan). 3 kosumlu ayarlarda kosum ortalamasi$\\pm$SD "
         "(ddof=1); SVHN'de yalniz IKI kosum vardir, SD YAZILMAZ, iki deger ayri ayri verilir "
         "(kosum 1 / kosum 2). Fark ve yayilim kosum basina tam hassasiyetle hesaplanir "
         "(artefaktta oranlar 2 ondalikli saklidir), yuvarlanmis ozetten degil. "
         "Yayilim = kosum basina (en buyuk - en kucuk protokol farki), sonra kosum ortalamasi$\\pm$SD.\n")
L.append("| Protokol | " + " | ".join(AD) + " |")
L.append("|---|" + "---|" * len(AD))
for i, (_k, _lab) in enumerate(PROTO):
    L.append(f"| {_lab} | " + " | ".join(
        hucre(S[a]["D"][i]) if S[a] else "ARTEFAKT YOK" for a in AD) + " |")
L.append("| Spread | " + " | ".join(
    hucre(S[a]["sprd"], plus=False) if S[a] else "ARTEFAKT YOK" for a in AD) + " |")
L.append("| n (test kumesi) | " + " | ".join(
    f"{S[a]['n']}" if S[a] else "ARTEFAKT YOK" for a in AD) + " |")
L.append("| Cift (kosum) sayisi | " + " | ".join(
    f"{len(S[a]['cift'])}" if S[a] else "ARTEFAKT YOK" for a in AD) + " |")
L.append("| Pozitif isaretli (kosum x protokol) | " + " | ".join(
    f"{int((S[a]['D'] > 0).sum())}/{S[a]['D'].size}" if S[a] else "ARTEFAKT YOK" for a in AD) + " |")
for a in AD:
    if S[a] is None:
        yok(a)
        continue
    _d = S[a]["d"]
    _sap = max(float(np.abs(S[a]["D"][i] - np.array(_d["protocols"][k]["diff"]["values"])).max())
               for i, (k, _) in enumerate(PROTO))
    _sps = float(np.abs(S[a]["sprd"] - np.array(_d["protocol_spread_pp"]["values"])).max())
    L.append(f"- {a}: kaynak `{S[a]['ozet']}`; kosumlar {S[a]['cift']}; artefaktin kendi "
             f"diff ve protocol_spread_pp alanlariyla "
             + ("UYUMLU (en buyuk sapma < 1e-6 puan)" if max(_sap, _sps) < 1e-6
                else f"UYUSMUYOR (en buyuk sapma fark {_sap:.2e}, yayilim {_sps:.2e}; INCELE)"))

L.append("\n### Yon bazinda oranlar (Tablo 6 ve 7 icin)\n")
L.append("| Ayar | Protokol | CNN->ViT | ViT->CNN | Fark |")
L.append("|---|---|---|---|---|")
for a in AD:
    if S[a] is None:
        continue
    for i, (_k, _lab) in enumerate(PROTO):
        L.append(f"| {a} | {_lab} | {hucre(S[a]['cv'][i], plus=False)} | "
                 f"{hucre(S[a]['vc'][i], plus=False)} | {hucre(S[a]['D'][i])} |")

L.append("\n### Her ikisi dogru, eslesmis analiz (ayar basina)\n")
L.append("| Ayar | n ortak | Fark (puan) | Bootstrap GA alt | Bootstrap GA ust | "
         "Isaret-cevirme perm. p (en buyuk) | TOST esdegerligi (herhangi marj) |")
L.append("|---|---|---|---|---|---|---|")
for a in AD:
    if S[a] is None:
        continue
    _b = S[a]["d"]["both_correct_paired"]
    L.append(f"| {a} | {hucre(_b['n_common']['values'], 0, False)} | {hucre(_b['diff_pp']['values'])} | "
             f"{hucre(_b['ci_low']['values'])} | {hucre(_b['ci_high']['values'])} | "
             f"{_b['perm_p_max']} | {'saglaniyor' if _b['tost_equivalent_any'] else 'saglanmiyor'} |")

# --- 2. Turetilmis manset sayilari --------------------------------------------
sec("Turetilmis", "yukaridaki ayar ozetlerinin kosum degerleri; results/c1_eval_summary.json; "
    "results/q1/e1_cifar100_summary.json; results/q1/e7_svhn_summary.json; "
    "results/*/pair*/a2_transfer_protocols.json")
L.append("Hepsi kosum basina tam hassasiyetle hesaplanir; yuvarlanmis tablo degerlerinin farki DEGILDIR.\n")
L.append("### Protokol farklarinin farki (puan)\n")
_FARK = (("raw - tc (Unconditioned eksi Target-correct)", 0, 1),
         ("ss - raw (Successful-source eksi Unconditioned)", 3, 0),
         ("bc - tc (Both-correct eksi Target-correct)", 2, 1),
         ("ss - bc (Successful-source eksi Both-correct)", 3, 2))
L.append("| Fark | " + " | ".join(AD) + " |")
L.append("|---|" + "---|" * len(AD))
for _lab, i, j in _FARK:
    L.append(f"| {_lab} | " + " | ".join(
        hucre(S[a]["D"][i] - S[a]["D"][j]) if S[a] else "ARTEFAKT YOK" for a in AD) + " |")

L.append("\n### bc - tc, kosum duzeyi %95 t araligi (df = kosum sayisi - 1)\n")
for a in AD:
    if S[a] is None:
        continue
    _v = S[a]["D"][2] - S[a]["D"][1]
    if _v.size < 3:
        L.append(f"- {a}: yalniz {_v.size} kosum (df={_v.size - 1}); aralik HESAPLANMADI. "
                 f"Iki kosum degeri: {' / '.join(sg(x, 2, True) for x in _v)}")
        continue
    _m, _s, _lo, _hi, _tk = t_aralik(_v)
    L.append(f"- {a}: ortalama {sg(_m, 2, True)}, SD {_s:.2f}, %95 t araligi "
             f"[{sg(_lo, 2, True)}; {sg(_hi, 2, True)}] (df={_v.size - 1}, t={_tk:.3f}); "
             f"kosum degerleri {', '.join(sg(x, 2, True) for x in _v)}; "
             f"aralik sifiri {'ICERIR' if _lo <= 0 <= _hi else 'icermez'}")

L.append("\n### Temiz dogruluk farki, ResNet-18 AT eksi ViT-Tiny AT (puan)\n")
_e1 = load("results/q1/e1_cifar100_summary.json")
_e7 = load("results/q1/e7_svhn_summary.json")
_TEMIZ = []
if ev:
    _TEMIZ.append(("CIFAR-10", ev["resnet18_at"]["clean"]["values"], ev["vit_tiny_at"]["clean"]["values"],
                   "results/c1_eval_summary.json resnet18_at/vit_tiny_at clean.values"))
else:
    yok("results/c1_eval_summary.json")
for _ad, _e, _yol in (("CIFAR-100", _e1, "results/q1/e1_cifar100_summary.json"),
                      ("SVHN", _e7, "results/q1/e7_svhn_summary.json")):
    if _e:
        _TEMIZ.append((_ad, _e["mimariler"]["resnet18"]["ozet"]["test_clean"]["degerler"],
                       _e["mimariler"]["vit_tiny"]["ozet"]["test_clean"]["degerler"],
                       f"{_yol} mimariler/*/ozet/test_clean/degerler"))
    else:
        yok(_yol)
L.append("| Ayar | ResNet-18 AT temiz | ViT-Tiny AT temiz | Fark (R - V) | Kaynak |")
L.append("|---|---|---|---|---|")
for _ad, _r, _v, _kay in _TEMIZ:
    _r, _v = np.asarray(_r, float), np.asarray(_v, float)
    L.append(f"| {_ad} | {hucre(_r, plus=False)} | {hucre(_v, plus=False)} | {hucre(_r - _v)} | `{_kay}` |")
L.append("\n(Fark kosum cifti basina alinir: kosum k icin ResNet tohum 100k, ViT tohum 200k. "
         "SVHN'de iki kosum, SD yazilmaz.)")

L.append("\n### Basarili-kaynak: siki ve gevsek okuma\n")
L.append("Siki okuma: kaynak temiz girdide dogru ve saldiri sonrasi yanlis (ss_definition). "
         "Gevsek okuma: kaynagin temizde zaten yanlis siniflandirdigi ornekler de dahil. "
         "Kaynak: her ayarin `pair*/a2_transfer_protocols.json` dosyasindaki "
         "`protocols/successful_source_loose`. Yayilim = kosum basina (en buyuk - en kucuk) "
         "{Unconditioned, Target-correct, Both-correct, Successful-source} farki; gevsek "
         "yayilimda son protokol gevsek okumadir.\n")
L.append("| Ayar | ss siki | ss gevsek | siki - gevsek | Yayilim (siki) | Yayilim (gevsek) |")
L.append("|---|---|---|---|---|---|")
for a in AD:
    if S[a] is None:
        continue
    _a2 = S[a]["a2"]
    if not all(p and "successful_source_loose" in p.get("protocols", {}) for p in _a2):
        L.append(f"| {a} | bulunamadi | bulunamadi | bulunamadi | bulunamadi | bulunamadi |")
        continue
    _lo = np.array([p["protocols"]["successful_source_loose"]["diff_CNNtoViT_minus_ViTtoCNN"] for p in _a2])
    _digd = [np.array([p["protocols"][k]["diff_CNNtoViT_minus_ViTtoCNN"] for p in _a2])
             for k in ("raw", "target_correct", "both_correct")]
    _sk = S[a]["D"][3]
    _spl = np.max(np.vstack(_digd + [_lo]), axis=0) - np.min(np.vstack(_digd + [_lo]), axis=0)
    L.append(f"| {a} | {hucre(_sk)} | {hucre(_lo)} | {hucre(_sk - _lo)} | "
             f"{hucre(S[a]['sprd'], plus=False)} | {hucre(_spl, plus=False)} |")

# --- 3. Tablo 8 ek sutunlari ---------------------------------------------------
sec("Tablo 8 ek sutunlari: isaretli hizalanma ve native-ViT kontrolu",
    "results/c1_a3/pair*/a3_gradient_paired.json (isaretli kosinus); "
    "results/c1_gradient/pair*/gradient_summary.json (native-ViT ve capraz kontrol)")
_a3 = [load(f"results/c1_a3/pair{p}/a3_gradient_paired.json") for p in PAIRS]
_gs = [load(f"results/c1_gradient/pair{p}/gradient_summary.json") for p in PAIRS]
L.append("Onceki foy ('Gradyan yapisi') isaretli kosinusu yalniz TEK sayi olarak veriyordu "
         "(iki modelin mutlak degerce en buyugu); asagida uc kosum ayri ayri, ortalama$\\pm$SD (ddof=1).\n")
if all(_a3):
    L.append("`results/c1_gradient/pair*/gradient_summary.json` isaretli kosinus ALANI TASIMAZ; "
             "isaretli deger `results/c1_a3/pair*/a3_gradient_paired.json` -> "
             "`alignment/<model>/all_pairs_signed_mean` alanindadir (artefakta 4 ondalikli yazilmis).\n")
    L.append("| Olcut | ResNet-18 AT | ViT-Tiny AT | Kosum degerleri (R / V) |")
    L.append("|---|---|---|---|")
    for _lab, _alan in (("Hizalanma (isaretli, tum cift ortalamasi)", "all_pairs_signed_mean"),
                        ("Hizalanma (mutlak, tum cift ortalamasi; Tablo 8 mutlak satirindan FARKLI olcum)", "all_pairs_abs_mean")):
        _r = [x["alignment"]["ResNet18_AT"][_alan] for x in _a3]
        _v = [x["alignment"]["ViT_Tiny_AT"][_alan] for x in _a3]
        L.append(f"| {_lab} | {fmt(_r, 4)} | {fmt(_v, 4)} | "
                 f"{', '.join(f'{x:.4f}' for x in _r)} / {', '.join(f'{x:.4f}' for x in _v)} |")
else:
    yok("results/c1_a3/pair*/a3_gradient_paired.json")
if all(_gs):
    L.append("\nResNet-18 AT ve ViT-Tiny AT sutunlari `gradient_summary.json` uc kosum ortalamasidir (Tablo 8 ile ayni); native-ViT kontrolu (`gradient_summary.json`, kosum basina n=500; "
             "sparsity_*_std alanlari 10 grup ortalamasi arasi SDdir, burada KULLANILMAZ):\n")
    L.append("| Olcut | ResNet-18 AT | ViT-Tiny AT | ViT (native) | Native kosum degerleri |")
    L.append("|---|---|---|---|---|")
    for _alan, _lab in (("sparsity_hoyer", "Hoyer"), ("sparsity_gini", "Gini"),
                        ("sparsity_rel_threshold", "Rel-esik (%1 alti)"),
                        ("gradient_alignment", "Hizalanma (mutlak kosinus)")):
        _h = {m: [g["statistics"][m][_alan] for g in _gs] for m in
              ("ResNet18_AT", "ViT_Tiny_AT", "ViT_CIFAR_Native_AT")}
        L.append(f"| {_lab} | {fmt(_h['ResNet18_AT'], 4)} | {fmt(_h['ViT_Tiny_AT'], 4)} | "
                 + (fmt(_h['ViT_CIFAR_Native_AT'], 4) if len(set(_h['ViT_CIFAR_Native_AT'])) > 1
                    else f"{_h['ViT_CIFAR_Native_AT'][0]:.4f} (tek checkpoint, SD yok)")
                 + f" | {', '.join(f'{x:.4f}' for x in _h['ViT_CIFAR_Native_AT'])} |")
    _nat = [g["statistics"]["ViT_CIFAR_Native_AT"]["sparsity_hoyer"] for g in _gs]
    L.append(f"\nNative-ViT: uc kosum dosyasindaki Hoyer degerleri "
             f"{'BIRBIRINDEN FARKLI' if len(set(_nat)) > 1 else 'ozdes'}; "
             f"makale tek checkpoint diyor (egitim bolunme protokolunden once, test kumesinde secilmis). "
             f"Model yollari: `gradient_summary.json` model_paths yalniz ResNet18_AT ve ViT_Tiny_AT'i "
             f"listeler, native checkpoint yolu artefaktta YOK.")
    L.append("\nNative-ViT isaretli hizalanma: ARTEFAKT YOK (`a3_gradient_paired.json` ve "
             "`gradient_summary.json` isaretli kosinusu yalniz ResNet18_AT ve ViT_Tiny_AT icin tasir).")
else:
    yok("results/c1_gradient/pair*/gradient_summary.json")

# --- 4. Tablo 9: Diff SD ve kosum duzeyi p (Holm) -----------------------------
sec("Tablo 9 ek sutunlari: Diff SD ve kosum duzeyi p (Holm)",
    "results/c1_c45_summary.json spatial/*/diff; results/c1_c5/pair*/c5_spatial.json "
    "paired_diff_ResNet_minus_ViT (kosum basina fark)")
_c5 = [load(f"results/c1_c5/pair{p}/c5_spatial.json") for p in PAIRS]
if c45 and all(_c5):
    L.append("Kosum duzeyi p: uc kosumun ResNet-eksi-ViT fark ortalamalarina tek orneklem iki yonlu t testi "
             "(H0: fark = 0, df=2); dort olcu uzerinde Holm duzeltmesi. Diff SD = kosumlar arasi SD "
             "(ddof=1). Wilcoxon sutunu onceki foydeki ornek duzeyi en buyuk p'dir ve ayri bir birimdir.\n")
    _ESLE = (("energy_area_50pct", "area50", "Enerji %50 alani"),
             ("energy_area_90pct", "area90", "Enerji %90 alani"),
             ("spatial_entropy", "entropy", "Mekansal entropi"),
             ("morans_i", "morans_i", "Moran's I"))
    _kv, _pr = [], []
    for _k, _dk, _ in _ESLE:
        _v = np.array([d["paired_diff_ResNet_minus_ViT"][_dk]["mean"] for d in _c5])
        _kv.append(_v)
        _pr.append(float(stats.ttest_1samp(_v, 0.0).pvalue))
    _ph = holm(_pr)
    L.append("| Olcut | Fark (R-V) ort.$\\pm$SD | Kosum degerleri | t (df=2) | p (ham) | p (Holm) | Wilcoxon p (en buyuk) |")
    L.append("|---|---|---|---|---|---|---|")
    for (_k, _dk, _lab), _v, _p, _pp in zip(_ESLE, _kv, _pr, _ph):
        _t = float(stats.ttest_1samp(_v, 0.0).statistic)
        _m, _s = ms(_v)
        _c = c45["spatial"][_k]["diff"]
        L.append(f"| {_lab} | {_m:+.4f}$\\pm${_s:.4f} | {', '.join(f'{x:+.4f}' for x in _v)} | "
                 f"{_t:+.3f} | {_p:.3f} | {_pp:.3f} | {c45['spatial'][_k]['p_max']:.2e} |")
        if abs(_c[0] - _m) > 1e-9 or abs(_c[1] - _s) > 1e-9:
            L.append(f"\n- UYARI: {_k} icin c1_c45_summary.json diff [{_c[0]:.6f}, {_c[1]:.6f}] ile "
                     f"kosum dosyalarindan hesap [{_m:.6f}, {_s:.6f}] UYUSMUYOR")
else:
    yok("results/c1_c45_summary.json veya results/c1_c5/pair*/c5_spatial.json")

# --- 5. Tablo 10: blok cikisi kosinusu, uc kosum ortalamasi ------------------
sec("Tablo 10: residual blok cikisi kosinusu (n=1000, uc kosum)",
    "results/c1_c4/pair*/c4_summary.json vit/cos_block_cls, vit/cos_block_token_mean, "
    "vit/cos_block_output; resnet/cos")
_bo = _c4_blok_cikisi()
if _bo:
    L.append("Kosum ortalamasi$\\pm$kosumlar arasi SD (ddof=1); her kosumun degeri c4_summary.json icindeki "
             "n=1000 ornek ortalamasidir. Blok numarasi 1-tabanli (makale 'Blk' sutunu). "
             "`cos_block_cls` = CLS jetonu, `cos_block_token_mean` = yama jetonlari ortalamasi, "
             "`cos_block_output` = tum jetonlar, hepsi blok CIKISINDA.\n")
    L.append("| Blok | CLS | Yama ortalamasi | Tum jetonlar |")
    L.append("|---|---|---|---|")
    for i in range(12):
        L.append(f"| {i + 1} | " + " | ".join(
            f"{_bo[ad][0][i]:.4f}$\\pm${_bo[ad][1][i]:.4f}" for ad, _ in C4_BLOK_ANAHTAR) + " |")
    L.append("\nMinimumlar ve oran (manset; 'C4' bolumundeki ayni sayilar):\n")
    for _ad, (_ort, _sd) in _bo.items():
        _k = int(np.argmin(_ort))
        L.append(f"- {_ad}: minimum blok {_k + 1}, {_ort[_k]:.4f}$\\pm${_sd[_k]:.4f}")
    _ck = int(np.argmin(_bo["CLS (cos_block_cls)"][0]))
    _pk = int(np.argmin(_bo["Yama ortalamasi (cos_block_token_mean)"][0]))
    L.append(f"- (1 - cos) orani, CLS minimumu / yama ortalamasi minimumu: "
             f"{(1 - _bo['CLS (cos_block_cls)'][0][_ck]) / (1 - _bo['Yama ortalamasi (cos_block_token_mean)'][0][_pk]):.2f}")
    _nrm = np.array([[d["vit"]["norm_change_pct"][f"block{i}"]["mean"] for i in range(12)] for d in C4])
    L.append(f"- Blok cikisi oznitelik normu degisimi: kosum ortalamasinin mutlak degerce en buyugu "
             f"{np.abs(_nrm.mean(0)).max():.2f}% (`vit/norm_change_pct/block*`, makale '%0.45 icinde' diyor)")
    L.append("\nResNet-18 AT, katman kosinusu (kosum ortalamasi$\\pm$SD):\n")
    L.append("| Katman | Kosinus | Norm degisimi (%) |")
    L.append("|---|---|---|")
    for _kat in C4[0]["resnet"]["cos"]:
        _cm = [d["resnet"]["cos"][_kat]["mean"] for d in C4]
        _nm = [d["resnet"]["norm_change_pct"][_kat]["mean"] for d in C4]
        L.append(f"| {_kat} | {fmt(_cm, 4)} | {np.mean(_nm):+.2f}$\\pm${np.std(_nm, ddof=1):.2f} |")
else:
    yok("results/c1_c4/pair*/c4_summary.json")

# --- 6. Dikkat entropisi ve TV yer degistirmesi -------------------------------
sec("Dikkat entropisi ve CLS dikkat yer degistirmesi (katman basina)",
    "results/c1_c4/pair*/c4_summary.json vit/attention/{entropy_clean_mean, entropy_adv_mean, "
    "entropy_delta_mean, displacement_mean}")
if C4_OK:
    _ec = np.array([d["vit"]["attention"]["entropy_clean_mean"] for d in C4])
    _ea = np.array([d["vit"]["attention"]["entropy_adv_mean"] for d in C4])
    _ed = np.array([d["vit"]["attention"]["entropy_delta_mean"] for d in C4])
    _dp = np.array([d["vit"]["attention"]["displacement_mean"] for d in C4])
    L.append("Entropi nat cinsinden, CLS dikkat dagilimi. Yer degistirme = temiz ile cekismeli CLS "
             "dikkat dagilimlari arasindaki toplam varyasyon uzakligi (`c1_c45_aggregate.py` "
             "etiketi: 'CLS yer degistirmesi (toplam varyasyon)'). Hucre = kosum ortalamasi$\\pm$SD "
             "(ddof=1), her kosum n=1000 ornek. Fark = cekismeli - temiz (kosum basina alinip "
             "ortalanir).\n")
    L.append("| Katman | Temiz entropi | Cekismeli entropi | Fark (adv - temiz) | TV yer degistirmesi |")
    L.append("|---|---|---|---|---|")
    for i in range(_ec.shape[1]):
        L.append(f"| {i + 1} | {fmt(_ec[:, i], 4)} | {fmt(_ea[:, i], 4)} | "
                 f"{hucre(_ed[:, i], 4)} | {fmt(_dp[:, i], 4)} |")
    L.append(f"| Genel (katman ortalamasi) | {fmt(_ec.mean(1), 4)} | {fmt(_ea.mean(1), 4)} | "
             f"{hucre(_ed.mean(1), 4)} | {fmt(_dp.mean(1), 4)} |")
    L.append(f"\n- En buyuk |entropi farki| (kosum ortalamasi, katman basina): {np.abs(_ed.mean(0)).max():.4f} nat "
             f"(katman {int(np.argmax(np.abs(_ed.mean(0)))) + 1})")
    L.append(f"- Katman ortalamasi temiz entropi {_ec.mean():.2f} nat")
    L.append(f"- TV yer degistirmesi: {_dp.mean(0).min():.4f} (katman {int(np.argmin(_dp.mean(0))) + 1}) "
             f"-> {_dp.mean(0).max():.4f} (katman {int(np.argmax(_dp.mean(0))) + 1}), kosum ortalamasi")
else:
    yok("results/c1_c4/pair*/c4_summary.json")

# --- 7. Epsilon taramasi -------------------------------------------------------
sec("Epsilon taramasi (PGD-10, Linf)", "results/c1_sweep/pair*/*/*_robustness_results.csv; "
    "results/wrn_eval/wrn_eval_summary.json; results/c1_eval_summary.json")
_NOKTA = [(0.0, "0 (temiz)"), (2 / 255, "2/255"), (4 / 255, "4/255"), (8 / 255, "8/255"), (16 / 255, "16/255")]


def _sweep(dizin):
    """Uc kosum icin {eps: dogruluk}; temiz satiri eps=0."""
    kosular = []
    for p in PAIRS:
        yol = os.path.join(ROOT, f"results/c1_sweep/pair{p}/{dizin}/{dizin}_robustness_results.csv")
        if not os.path.exists(yol):
            return None
        with open(yol, encoding="utf-8") as fh:
            kosular.append({float(r["Epsilon"]): float(r["Accuracy"]) for r in csv.DictReader(fh)})
    return kosular


def _al(kosu, e):
    for k, v in kosu.items():
        if abs(k - e) < 1e-6:
            return v
    return None


_sw = {"ResNet-18 AT": _sweep("resnet18"), "ViT-Tiny AT": _sweep("vit_tiny")}
_wrn = load("results/wrn_eval/wrn_eval_summary.json")
_WRN_ANAHTAR = {0.0: "clean", 2 / 255: "pgd10_eps0.00784", 4 / 255: "pgd10_eps0.01569",
                8 / 255: "pgd10_eps0.03137", 16 / 255: "pgd10_eps0.06275"}
if all(_sw.values()) and _wrn:
    L.append("ResNet-18 AT ve ViT-Tiny AT: uc kosum ortalamasi$\\pm$SD (ddof=1), tam test kumesi n=10000. "
             "WRN-28-10: TEK model (RobustBench Gowal2020), SD yok, n=10000, saldiri PGD-10 (alpha=2/255).\n")
    L.append("| eps | ResNet-18 AT | ViT-Tiny AT | WRN-28-10 |")
    L.append("|---|---|---|---|")
    for e, lab in _NOKTA:
        _r = [_al(k, e) for k in _sw["ResNet-18 AT"]]
        _v = [_al(k, e) for k in _sw["ViT-Tiny AT"]]
        _w = _wrn["results"].get(_WRN_ANAHTAR[e])
        L.append(f"| {lab} | {fmt(_r) if None not in _r else 'ARTEFAKT YOK'} | "
                 f"{fmt(_v) if None not in _v else 'ARTEFAKT YOK'} | "
                 f"{_w['accuracy']:.2f} |" if _w else f"| {lab} | ARTEFAKT YOK | ARTEFAKT YOK | ARTEFAKT YOK |")
    L.append("\nTablo I ile 8/255 (ve temiz) tutarliligi: tarama kosumlari tabloyu uretenlerle AYNI "
             "kosum degerleri mi?\n")
    L.append("| Model | Olcut | Tarama ort.$\\pm$SD | Tablo I (c1_eval_summary) ort.$\\pm$SD | "
             "Ortalama farki (tarama - Tablo I) | Kosum basina fark |")
    L.append("|---|---|---|---|---|---|")
    if ev:
        for ad, key in (("ResNet-18 AT", "resnet18_at"), ("ViT-Tiny AT", "vit_tiny_at")):
            for olc, e, ek in (("temiz", 0.0, "clean"), ("PGD-10 8/255", 8 / 255, "pgd")):
                _t = [_al(k, e) for k in _sw[ad]]
                _o = ev[key][ek]["values"]
                _fk = np.asarray(_t) - np.asarray(_o)
                L.append(f"| {ad} | {olc} | {fmt(_t)} | {fmt(_o)} | {np.mean(_t) - np.mean(_o):+.2f} | "
                         f"{', '.join(f'{x:+.2f}' for x in _fk)} |")
    else:
        yok("results/c1_eval_summary.json")
    L.append(f"| WRN-28-10 | PGD-10 8/255 | {_wrn['results']['pgd10_eps0.03137']['accuracy']:.2f} | "
             f"Tablo I WRN satiri ELLE YAZILMIS LITERAL (66.92; 'Sabit dizgeler' bolumu) | "
             f"{_wrn['results']['pgd10_eps0.03137']['accuracy'] - 66.92:+.2f} | tek model |")
else:
    yok("results/c1_sweep/pair*/ veya results/wrn_eval/wrn_eval_summary.json")

# --- 8. Sabit dizgeler -----------------------------------------------------------
sec("Sabit dizgeler (artefakttan OKUNMAYAN, elle tasinmis literaller)",
    "scripts/build_reference_sheet.py (satir numaralari calisma aninda bulunur)")
L.append("Asagidaki sayilar bu betikte string literal olarak durur; uretilemedikleri icin DOGRULANMIS "
         "SAYILMAZ. Metne girmeleri durumunda kaynak notu gerekir.\n")
L.append("| Sabit dizge | Foyde nerede | Betikte satir | Kaynak durumu |")
L.append("|---|---|---|---|")
L.append(f"| Kos. yaniltma PGD 52.15 vs 52.33, AA 58.16 vs 56.46; her ikisi dogru PGD 54.92 vs 49.61, "
         f"AA 48.15 vs 45.33; n=7260 (makale Tablo 2 alt blok) | 'Tablo II: kosullu ayrisma' | "
         f"{_satir('52.15 vs 52.33')} | KARANTINADAKI ESKI KOSU (C1 oncesi, sizintili tek kosu), ELLE "
         f"TASINMIS LITERAL; hangi dosyadan alindigi betikte kayitli degil; bu betik karantina "
         f"yolundan okumaz, dogrulayamaz |")
_tr = load("results/c1_transfer/c1_transfer_summary.json")
_old = ", ".join(f"{_tr['protocols'][k].get('old_run3_diff', 'yok')}" for k, _ in PROTO) if _tr else "ARTEFAKT YOK"
L.append(f"| 'run3 fark' sutunu (makale Tablo 3 Diff dagger): {_old} (sirayla Unconditioned, "
         f"Target-correct, Both-correct, Successful-source) | 'Tablo III: transfer protokolleri' | "
         f"{_satir('old_run3_diff')} | literal DEGIL, `c1_transfer_summary.json` icindeki "
         f"`old_run3_diff` alani; ancak `scripts/c1_transfer_aggregate.py` bu alani karantinadaki "
         f"`results/rev2_blockA/a2_transfer_protocols.json` (tek kosu, sizintili) dosyasindan "
         f"tasimistir. Bu betik o dosyayi OKUMAZ; deger yalniz summary JSON'daki kopyadir |")
_wl = (89.48, 70.91, 66.92, 62.76)
if _wrn:
    _wr = _wrn["results"]
    _dg = [_wr["clean"]["accuracy"], _wr["fgsm"]["accuracy"], _wr["pgd10_eps0.03137"]["accuracy"]]
    _ok = all(abs(a - b) < 1e-9 for a, b in zip(_dg, _wl[:3]))
    _wdurum = (f"temiz/FGSM/PGD `results/wrn_eval/wrn_eval_summary.json` ile "
               f"{'UYUSUYOR' if _ok else 'UYUSMUYOR (' + str(_dg) + ')'}; ")
else:
    _wdurum = "`results/wrn_eval/wrn_eval_summary.json` ARTEFAKT YOK; "
L.append(f"| WRN-28-10 satiri: temiz 89.48 / FGSM 70.91 / PGD 66.92 / AA 62.76 | 'Tablo I: ana gurbuzluk' | "
         f"{_satir('89.48 / FGSM 70.91')} | literal; {_wdurum}AA 62.76 harici RobustBench raporudur, "
         f"yerel AA artefakti ARTEFAKT YOK |")

out = os.path.join(ROOT, "results/C1_REFERANS_FOYU.md")
with open(out, "w", encoding="utf-8") as fh:
    fh.write("\n".join(L) + "\n")
print("\n".join(L))
print(f"\nkaydedildi: {out}")
