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

# >>> IKINCI DALGA BASI (2026-10-04, LeCun plani Faz 1-2; yerlestir.py ile yazildi)
# ===========================================================================
# GENISLETME 2026-10-04 (ikinci dalga, LeCun plani Faz 1-2): sekiz yeni bolum.
# Kaynak: results/q1_research/LECUN_PLANI_2026-10-04.md. Her sayi artefakttan
# okunur; hicbir sayi elle yazilmaz. Mevcut bolumlere dokunulmaz; bolumler
# 'Sabit dizgeler' bolumunden once eklenir. Alan bulunamazsa 'ARTEFAKT YOK'.
# Karantina yollarindan OKUNMAZ.
# ===========================================================================
PM = "$\\pm$"
_ETIKET = {k: lab for k, lab in PROTO}


def ortsd(vals, nd=2, plus=False):
    """ort$\\pm$SD (ddof=1); tek deger gelirse SD yazilmaz."""
    a = np.asarray(vals, dtype=float)
    if a.size == 1:
        return sg(float(a[0]), nd, plus)
    m, s = ms(a)
    return f"{sg(m, nd, plus)}{PM}{s:.{nd}f}"


def uc(vals, nd=2, plus=False):
    return " / ".join(sg(float(v), nd, plus) for v in vals)


def ga(a, nd=2, plus=True):
    return f"[{sg(a[0], nd, plus)}; {sg(a[1], nd, plus)}]"


def pf(x):
    return f"{x:.2e}" if x < 1e-3 else f"{x:.4f}"


def mm(vals, nd=2, plus=False):
    a = np.asarray(vals, dtype=float)
    return f"{sg(float(a.min()), nd, plus)}; {sg(float(a.max()), nd, plus)}"


def T(bas, satirlar):
    L.append("| " + " | ".join(bas) + " |")
    L.append("|" + "---|" * len(bas))
    for s in satirlar:
        L.append("| " + " | ".join(str(x) for x in s) + " |")
    L.append("")


def _hata(e):
    L.append(f"\nARTEFAKT YOK: alan bulunamadi ({e!r}); bu bolumun kalani uretilemedi.\n")


# --- 9. Kaynak-hedef toplamsal ayristirma ------------------------------------------
sec("Kaynak-hedef toplamsal ayristirma (hedef-dogru oranlar)", "results/q1/kaynak_hedef_ayristirma.json")
KH = load("results/q1/kaynak_hedef_ayristirma.json")
if KH is None:
    yok("results/q1/kaynak_hedef_ayristirma.json")
else:
    try:
        R = KH["sonuc"]
        L.append(f"Yontem (artefaktin kendi alani): {KH['yontem']}. Birim: {KH['birim']}. "
                 f"Artefakt uretim zamani: {KH['uretildi_utc']}.\n")
        L.append("Okuma: kaynak etkisi farki = alpha_ResNet - alpha_ViT; hedef etkisi farki = beta_ViT - beta_ResNet; "
                 "asimetri = ResNet->ViT eksi ViT->ResNet = kaynak farki + hedef farki + artik farki. "
                 "'Cift' = bir egitim cifti (uc tohum cifti); ortalama$\\pm$SD ciftler arasidir (ddof=1, n=3).\n")
        _sapma = []

        def _ist(d, alan):
            v = np.asarray(d[alan]["degerler"], dtype=float)
            m_, s_ = ms(v)
            _sapma.append(max(abs(m_ - d[alan]["ortalama"]), abs(s_ - d[alan]["sd_ciftler_arasi"])))
            return v

        for ds in ("CIFAR-10", "CIFAR-100"):
            cb = R[ds]["cift_basina"]
            L.append(f"\n### {ds}: cift basina ayristirma (uc cift)\n")
            satir = []
            notlar = []
            for k, lab in PROTO:
                d = cb[k]
                if isinstance(d, str):
                    satir.append([lab] + ["ARTEFAKT YOK"] * 8)
                    notlar.append(f"- {lab}: artefakt notu: {d}")
                    continue
                ks = _ist(d, "kaynak_etkisi_farki_ResNet_eksi_ViT")
                hs = _ist(d, "hedef_etkisi_farki_ViT_eksi_ResNet")
                asm = _ist(d, "asimetri_ResNettoViT_eksi_ViTtoResNet")
                ar = _ist(d, "artik_farki")
                mx = _ist(d, "max_abs_artik")
                r2 = _ist(d, "R2")
                satir.append([lab, ortsd(ks, 2, True), ortsd(hs, 2, True), ortsd(asm, 2, True), ortsd(ar, 2, True),
                              ortsd(mx, 2), ortsd(r2, 4), uc(ks, 2, True), uc(hs, 2, True)])
            T(["Protokol", "Kaynak etkisi farki (R-V)", "Hedef etkisi farki (V-R)", "Asimetri (R->V eksi V->R)",
               "Artik farki", "En buyuk mutlak artik", "R2", "Kaynak farki, cift degerleri",
               "Hedef farki, cift degerleri"], satir)
            L.extend(notlar)
            L.append(f"\nSabit-WRN karsitliklari ({ds}, cift basina oranlar, ortalama$\\pm$SD): "
                     "WRN hedefine ResNet kaynaktan ve ViT kaynaktan gelen oran (fark = ResNet - ViT); "
                     "WRN kaynagindan ResNet ve ViT hedefe giden oran (fark = ResNet hedef - ViT hedef).\n")
            satir = []
            for k, lab in PROTO:
                d = cb[k]
                if isinstance(d, str):
                    satir.append([lab] + ["ARTEFAKT YOK"] * 6)
                    continue
                satir.append([lab] + [ortsd(_ist(d, a_), 2, sgn) for a_, sgn in (
                    ("WRN_hedef_ResNetten", False), ("WRN_hedef_ViTden", False),
                    ("WRN_hedef_fark_ResNet_eksi_ViT", True), ("WRN_kaynak_ResNete", False),
                    ("WRN_kaynak_ViTe", False), ("WRN_kaynak_fark_ResNet_eksi_ViT", True))])
            T(["Protokol", "WRN hedefine ResNet'ten", "WRN hedefine ViT'ten", "Hedef karsitligi (R-V)",
               "WRN kaynagindan ResNet'e", "WRN kaynagindan ViT'e", "Kaynak karsitligi (R-V)"], satir)

            om = R[ds]["ozet_matris"]
            L.append(f"\n{ds}: uc tohum ortalamasi matris (`{R[ds]['ozet_matris_kaynagi']}`), tek uydurma "
                     "(kosegen haric 6 hucre, 5 parametre, 1 artik serbestlik derecesi).\n")
            _kol = (("Hedef-dogru (target_correct)", om["target_correct"]), ("Ham (raw), duyarlilik", om["raw_duyarlilik"]))

            satir = []
            for ad, f_ in (
                ("Kaynak etkisi farki (R-V)", lambda u: sg(u["kaynak_etkisi_farki_ResNet_eksi_ViT"], 2, True)),
                ("Hedef etkisi farki (V-R)", lambda u: sg(u["hedef_etkisi_farki_ViT_eksi_ResNet"], 2, True)),
                ("Asimetri (R->V eksi V->R)",
                 lambda u: sg(u["asimetri_ayristirmasi_ResNettoViT_eksi_ViTtoResNet"]["asimetri"], 2, True)),
                ("Artik farki",
                 lambda u: sg(u["asimetri_ayristirmasi_ResNettoViT_eksi_ViTtoResNet"]["artik_farki"], 2, True)),
                ("En buyuk mutlak artik", lambda u: sg(u["uydurma"]["max_abs_artik"], 2)),
                ("R2", lambda u: sg(u["uydurma"]["R2"], 4)),
                ("mu", lambda u: sg(u["uydurma"]["mu"], 2)),
                ("Hucre / parametre / artik serbestlik",
                 lambda u: f"{u['uydurma']['n_hucre']} / {u['uydurma']['parametre_sayisi']} / "
                           f"{u['uydurma']['artik_serbestlik']}"),
                ("WRN hedefine ResNet'ten / ViT'ten / fark",
                 lambda u: f"{sg(u['sabit_WRN']['WRN_hedef_ResNetten'])} / {sg(u['sabit_WRN']['WRN_hedef_ViTden'])} / "
                           f"{sg(u['sabit_WRN']['WRN_hedef_fark_ResNet_eksi_ViT'], 2, True)}"),
                ("WRN kaynagindan ResNet'e / ViT'e / fark",
                 lambda u: f"{sg(u['sabit_WRN']['WRN_kaynak_ResNete'])} / {sg(u['sabit_WRN']['WRN_kaynak_ViTe'])} / "
                           f"{sg(u['sabit_WRN']['WRN_kaynak_fark_ResNet_eksi_ViT'], 2, True)}")):
                satir.append([ad] + [f_(d_) for _, d_ in _kol])
            T(["Olcut"] + [a_ for a_, _ in _kol], satir)
            _u = om["target_correct"]["uydurma"]
            satir = [[m_, sg(_u["alpha_kaynak"][m_], 2, True), sg(_u["beta_hedef"][m_], 2, True)]
                     for m_ in _u["alpha_kaynak"]]
            L.append(f"{ds}, hedef-dogru ozet matris, model etkileri (toplam-sifir kodlama, mu = {sg(_u['mu'], 2)}):\n")
            T(["Model", "Kaynak etkisi alpha", "Hedef etkisi beta"], satir)
            tk = R[ds]["npz_json_tutarlilik_kontrolu"]
            L.append("Ornek bazli npz ile JSON ozeti tutarliligi (en buyuk mutlak sapma, puan): "
                     + "; ".join(f"{p_}: ham {v_['max_abs_npz_raw_eksi_json']:.1e}, hedef-dogru "
                                 f"{v_['max_abs_npz_tc_eksi_json_cond']:.4f}" for p_, v_ in tk.items()) + "\n")
        L.append(f"\nCift basina ortalama ve SD alanlarinin `degerler` dizisinden yeniden hesabiyla tutarlilik: "
                 f"en buyuk sapma {max(_sapma):.2e} "
                 + ("(UYUMLU)" if max(_sapma) < 1e-6 else "(UYUSMUYOR; INCELE)") + ".\n")

        # --- Mahmood 8x8 ---
        for ds in ("CIFAR-10", "CIFAR-100"):
            m = R["Mahmood2021"][ds]
            L.append(f"\n### Mahmood ve ark. (2021) {ds} 8x8 matrisi: toplamsal ve aile-terimli uydurma\n")
            L.append(f"Protokol: {m['protokol']}.\n")
            u, a2 = m["uydurma"], m["ayni_cins_terimli_uydurma"]["uydurma"]
            T(["Uydurma", "R2", "En buyuk mutlak artik", "Hucre", "Parametre", "Artik serbestlik", "Ayni-cins gamma"],
              [["Toplamsal (mu + alpha_kaynak + beta_hedef)", sg(u["R2"], 4), sg(u["max_abs_artik"], 2), u["n_hucre"],
                u["parametre_sayisi"], u["artik_serbestlik"], "yok"],
               ["Toplamsal + ayni-cins terimi", sg(a2["R2"], 4), sg(a2["max_abs_artik"], 2), a2["n_hucre"],
                a2["parametre_sayisi"], a2["artik_serbestlik"], sg(a2["ayni_cins_gamma"], 2, True)]])
            L.append(f"Not (artefakttan): {m['ayni_cins_terimli_uydurma']['not']}\n")
            F1, F2 = m["aile_duzeyi_farklar"], m["ayni_cins_terimli_uydurma"]["aile_duzeyi_farklar"]
            satir = []
            for ad in F1:
                satir.append([ad,
                              sg(F1[ad]["kaynak_etkisi_farki_CNN_eksi_ViT"], 2, True),
                              sg(F1[ad]["hedef_etkisi_farki_ViT_eksi_CNN"], 2, True),
                              sg(F2[ad]["kaynak_etkisi_farki_CNN_eksi_ViT"], 2, True),
                              sg(F2[ad]["hedef_etkisi_farki_ViT_eksi_CNN"], 2, True)])
            T(["Aile karsitligi", "Toplamsal: kaynak farki (CNN-ViT)", "Toplamsal: hedef farki (ViT-CNN)",
               "Aile-terimli: kaynak farki (CNN-ViT)", "Aile-terimli: hedef farki (ViT-CNN)"], satir)
            cins = m["ayni_cins_terimli_uydurma"]["cins"]
            satir = [[ad, cins[ad], sg(u["alpha_kaynak"][ad], 2, True), sg(u["beta_hedef"][ad], 2, True),
                      sg(a2["alpha_kaynak"][ad], 2, True), sg(a2["beta_hedef"][ad], 2, True)]
                     for ad in u["alpha_kaynak"]]
            T(["Model", "Cins (uydurmadaki)", "Toplamsal alpha", "Toplamsal beta", "Aile-terimli alpha",
               "Aile-terimli beta"], satir)
            cp = m["aileler_arasi_cift_ayristirmasi_CNNtoViT_eksi_ViTtoCNN"]
            satir = [[ad, sg(v_["asimetri"], 2, True), sg(v_["kaynak_farki"], 2, True), sg(v_["hedef_farki"], 2, True),
                      sg(v_["artik_farki"], 2, True)] for ad, v_ in cp.items()]
            L.append("Aileler arasi 16 cift, toplamsal uydurmadan ayristirma (asimetri = CNN->ViT eksi ViT->CNN):\n")
            T(["Cift", "Asimetri", "Kaynak farki", "Hedef farki", "Artik farki"], satir)
            sb = m["sabit_ucuncu_model_BiT-M-R50x1_vs_ViT-L-16"]
            satir = [[ad, sg(v_["sabit_hedef_k_BiTten_eksi_ViTL16dan"], 1, True),
                      sg(v_["sabit_kaynak_k_BiTe_eksi_ViTL16ya"], 1, True)] for ad, v_ in sb.items()]
            L.append("Sabit ucuncu model karsitligi (BiT-M-R50x1 ve ViT-L-16 ayni ucuncu modele karsi; "
                     "hucre = ham matris farki, puan):\n")
            T(["Ucuncu model k", "Sabit hedef k: (BiT-M-R50x1->k) eksi (ViT-L-16->k)",
               "Sabit kaynak k: (k->BiT-M-R50x1) eksi (k->ViT-L-16)"], satir)
    except (KeyError, TypeError, IndexError, ValueError) as e_:
        _hata(e_)

# --- 10. Dis veri: Mahmood ve ark. (ICCV 2021) -------------------------------------
sec("Dis veri: Mahmood ve ark. (ICCV 2021)",
    "results/q1/dis_veri/mahmood2021_tablolar.json; results/q1/dis_veri/mahmood2021_ozdeslik.json; "
    "aile duzeyi kaynak/hedef etkileri icin results/q1/kaynak_hedef_ayristirma.json (Mahmood2021 bolumu)")
MT = load("results/q1/dis_veri/mahmood2021_tablolar.json")
MO = load("results/q1/dis_veri/mahmood2021_ozdeslik.json")
if MT is None:
    yok("results/q1/dis_veri/mahmood2021_tablolar.json")
if MO is None:
    yok("results/q1/dis_veri/mahmood2021_ozdeslik.json")
if MT is not None and MO is not None:
    try:
        L.append(f"Kunye (artefakttan): {MT['kunye']}. Tablo 2 yonu: {MT['yon_dogrulamasi']['tablo2_basligi']} "
                 f"(satir = kaynak). Protokol alintisi: \"{MT['protokol_alinti']}\".\n")
        L.append(f"Yon dogrulamasi (artefakt hukmu): {MT['yon_dogrulamasi']['hukum']}\n")
        L.append(f"Kosegen (artefakt hukmu): {MT['kosegen_notu']['hukum']}\n")
        # temiz dogruluk
        td = MT["temiz_dogruluk_yuzde"]
        L.append("### Temiz dogruluklar (yuzde)\n")
        T(["Model", "Aile (artefakttaki)", "CIFAR-10", "CIFAR-100"],
          [[ad, MT["aile"][ad], sg(td["CIFAR-10"][ad], 1), sg(td["CIFAR-100"][ad], 1)] for ad in td["CIFAR-10"]])
        L.append(f"CIFAR-100 kaynak notu: {td['CIFAR-100_kaynak_notu']}\n")
        # rejim notlari
        L.append("### Rejim notlari (artefakttan, satir satir)\n")
        for k_, v_ in MO["rejim_notlari"].items():
            L.append(f"- {k_}: {v_}")
        L.append("")
        # p
        pv = MO["p_degerleri"]
        L.append(f"Ozdeslikte kullanilan p (bizim AT yonlerimizde olculen): p_min = {pv['p_min']:.6f}, "
                 f"p_ort = {pv['p_ort']:.6f}; kaynak `{pv['kaynak']}`. Not: {pv['not']}\n")
        L.append(f"Ozdeslik yontemi (artefakttan): {MO['yontem']}\n")
        # anahtar cift
        L.append("### Anahtar cift: BiT-M-R50x1 ve ViT-L-16\n")
        satir = []
        for ds in ("CIFAR-10", "CIFAR-100"):
            a = MO["anahtar_cift_BiT-M-R50x1_ViT-L-16"][ds]
            for pk in [k_ for k_ in a if k_.startswith("p=")]:
                v_ = a[pk]
                satir.append([ds, pk, sg(a["temiz_dogruluk_farki_puan"], 2, True), sg(a["asimetri_bc_puan"], 2, True),
                              sg(v_["asimetri_ham_ongoru_puan"], 2, True), ga(v_["asimetri_ham_ongoru_aralik_puan"]),
                              sg(v_["protokol_etkisi_ham_eksi_bc_puan"], 2, True), ga(v_["protokol_etkisi_aralik_puan"]),
                              "evet" if v_["isaret_degisir_mi_merkez"] else "hayir",
                              "evet" if v_["isaret_degisebilir_mi_aralik"] else "hayir"])
        T(["Veri", "p", "Temiz fark (CNN-ViT, puan)", "Her-ikisi-dogru asimetri (CNN->ViT eksi ViT->CNN)",
           "Ozdeslik-ongorulu ham asimetri", "Ham asimetri araligi", "Protokol etkisi (ham eksi bc)",
           "Protokol etkisi araligi", "Isaret merkezde doner mi", "Isaret aralikta donebilir mi"], satir)
        L.append(f"Artefaktin yorum alani: {MO['yorum']['anahtar_cift_CIFAR10']}\n")
        # aile duzeyi
        L.append("### Aile duzeyi asimetri ve guclu kaynak ailesi sayimi\n")
        satir = []
        for ds in ("CIFAR-10", "CIFAR-100"):
            ao = MO["ozdeslik"][ds]["aile_ozeti"]
            for ad in ("hibrit_haric", "hibrit_ViT_sayildi"):
                v_ = ao[ad]
                satir.append([ds, ad, f"{len(v_['ViT_modelleri'])} ViT / {len(v_['CNN_modelleri'])} CNN",
                              sg(v_["CNN_to_ViT_bc_ortalama_yuzde"], 2), sg(v_["ViT_to_CNN_bc_ortalama_yuzde"], 2),
                              sg(v_["aile_asimetrisi_CNNtoViT_eksi_ViTtoCNN_puan"], 2, True),
                              f"{v_['ViT_daha_guclu_kaynak_oldugu_cift_sayisi']}/{v_['cift_sayisi']}",
                              v_["guclu_kaynak_ailesi"]])
            for ad in ("alt_aile_BiT-M_vs_ViT", "alt_aile_ResNet_vs_ViT"):
                v_ = ao[ad]
                satir.append([ds, ad, f"{len(v_['ViT_modelleri'])} ViT / {len(v_['CNN_modelleri'])} CNN",
                              sg(v_["CNN_to_ViT_bc_ortalama_yuzde"], 2), sg(v_["ViT_to_CNN_bc_ortalama_yuzde"], 2),
                              sg(v_["aile_asimetrisi_CNNtoViT_eksi_ViTtoCNN_puan"], 2, True),
                              f"CNN guclu: {v_['CNN_daha_guclu_kaynak_oldugu_cift_sayisi']}/{v_['cift_sayisi']}",
                              "CNN" if v_["CNN_daha_guclu_kaynak_oldugu_cift_sayisi"] == v_["cift_sayisi"] else
                              ("ViT" if v_["CNN_daha_guclu_kaynak_oldugu_cift_sayisi"] == 0 else "karisik")])
        T(["Veri", "Aile kumesi", "Model sayisi", "CNN->ViT bc ortalamasi (%)", "ViT->CNN bc ortalamasi (%)",
           "Aile asimetrisi (CNN->ViT eksi ViT->CNN)", "Cift sayimi (ViT daha guclu / CNN guclu)",
           "Guclu kaynak ailesi (artefakt: hibrit_* satirlari; alt aile: sayimdan)"], satir)
        L.append("`hibrit_haric`: ViT-R50 (hibrit) disarida; 3 ViT x 4 CNN = 12 cift. `hibrit_ViT_sayildi`: "
                 "ViT-R50 ViT sayilir; 4 ViT x 4 CNN = 16 cift (artefaktin model listelerinden).\n")
        # aileler arasi ozet
        L.append("### Aileler arasi 12 cift: temiz fark ve ozdeslik-ongorulu protokol etkisi\n")
        satir = []
        for ds in ("CIFAR-10", "CIFAR-100"):
            v_ = MO["ozdeslik"][ds]["aileler_arasi_ozet"]
            satir.append([ds, v_["cift_sayisi"], sg(v_["temiz_hata_farki_max_puan"], 2), sg(v_["abs_asimetri_bc_min_puan"], 2),
                          sg(v_["abs_protokol_etkisi_max_puan_p1"], 2), v_["abs_protokol_etkisi_max_cift"],
                          sg(v_["protokol_etkisi_bolu_abs_asimetri_max_p1"], 3),
                          f"{v_['isaret_degisen_cift_sayisi_merkez_p1']}/{v_['cift_sayisi']}",
                          f"{v_['isaret_degisen_cift_sayisi_merkez_pmin']}/{v_['cift_sayisi']}",
                          f"{v_['isaret_degisebilir_cift_sayisi_aralik_p1']}/{v_['cift_sayisi']}"])
        T(["Veri", "Cift", "En buyuk temiz hata farki (puan)", "En kucuk mutlak bc asimetrisi", "En buyuk mutlak protokol etkisi (p=1)",
           "Hangi cift", "Etki / mutlak asimetri en buyuk (p=1)", "Isaret donen (merkez, p=1)", "Isaret donen (merkez, p_min)",
           "Isaret donebilir (aralik, p=1)"], satir)
        L.append(f"Artefaktin uzlasma yorumu: {MO['yorum']['uzlasma']}\n")
        # CIFAR-100 ResNet cifti
        L.append("### CIFAR-100, ResNet-56 ve ResNet-164 x ViT ciftleri: yon ve protokol etkisi\n")
        satir = []
        for c in MO["ozdeslik"]["CIFAR-100"]["ciftler"]:
            if c["tur"] != "aileler_arasi" or not c["cift"].startswith("ResNet"):
                continue
            a = c["p=1 (ust sinir)"]
            satir.append([c["cift"], sg(c["temiz_dogruluk_farki_puan"], 1, True), sg(c["asimetri_bc_puan"], 1, True),
                          sg(a["asimetri_ham_ongoru_puan"], 2, True), sg(a["protokol_etkisi_ham_eksi_bc_puan"], 2, True),
                          ga(a["protokol_etkisi_aralik_puan"]),
                          "evet" if a["isaret_degisir_mi_merkez"] else "hayir",
                          "evet" if a["isaret_degisebilir_mi_aralik"] else "hayir"])
        T(["Cift (CNN vs ViT)", "Temiz fark (CNN-ViT)", "bc asimetrisi (CNN->ViT eksi ViT->CNN)",
           "p=1 ham ongoru", "Protokol etkisi", "Etki araligi", "Isaret merkezde doner mi", "Isaret aralikta donebilir mi"], satir)
        ra = MO["ozdeslik"]["CIFAR-100"]["aile_ozeti"]["alt_aile_ResNet_vs_ViT"]
        L.append(f"Yon sayimi: CNN daha guclu kaynak {ra['CNN_daha_guclu_kaynak_oldugu_cift_sayisi']}/{ra['cift_sayisi']} cift "
                 f"(ResNet ailesi, ViT-B-32/B-16/L-16); ResNet temiz dogrulugu "
                 + ", ".join(f"{k_} {v_:.1f}" for k_, v_ in ra["CNN_temiz_dogruluk_yuzde"].items()) + ".\n")
        yc = MO["yorum"]
        for ds in ("CIFAR-10", "CIFAR-100"):
            o_ = yc[f"isaret_donen_ciftler_{ds}"]
            L.append(f"- {ds}: bc'de CNN guclu kaynak olan cift {len(o_['bc_de_CNN_guclu_kaynak_olan_ciftler'])} "
                     f"({', '.join(o_['bc_de_CNN_guclu_kaynak_olan_ciftler']) or 'yok'}); ham ongoruyle isaret donen cift "
                     f"(p=1, merkez) {len(o_['ham_ongoruyle_isaret_donen_ciftler_p1_merkez'])}. {o_['not']}")
        L.append("")
        # kaynak/hedef etkileri
        if KH is not None:
            L.append("### Aile duzeyi kaynak ve hedef etkileri (`results/q1/kaynak_hedef_ayristirma.json`)\n")
            satir = []
            for ds in ("CIFAR-10", "CIFAR-100"):
                m_ = KH["sonuc"]["Mahmood2021"][ds]
                for ad in m_["aile_duzeyi_farklar"]:
                    f1, f2 = m_["aile_duzeyi_farklar"][ad], m_["ayni_cins_terimli_uydurma"]["aile_duzeyi_farklar"][ad]
                    satir.append([ds, ad, sg(f1["kaynak_etkisi_farki_CNN_eksi_ViT"], 2, True),
                                  sg(f1["hedef_etkisi_farki_ViT_eksi_CNN"], 2, True),
                                  sg(f2["kaynak_etkisi_farki_CNN_eksi_ViT"], 2, True),
                                  sg(f2["hedef_etkisi_farki_ViT_eksi_CNN"], 2, True)])
            T(["Veri", "Aile karsitligi", "Toplamsal kaynak farki (CNN-ViT)", "Toplamsal hedef farki (ViT-CNN)",
               "Aile-terimli kaynak farki", "Aile-terimli hedef farki"], satir)
        # bizim cift
        bz = MO["bizim_CIFAR10_ciftimiz"]
        L.append("### Bizim CIFAR-10 cifti uzerinde ayni ozdeslik ongorusu (yaklasim sinamasi)\n")
        L.append(f"Kaynak: `{bz['kaynak']}`. Temiz dogruluk ResNet-18 AT {bz['temiz_dogruluk_ResNet18_AT_yuzde']:.2f}, "
                 f"ViT-Tiny AT {bz['temiz_dogruluk_ViT_Tiny_AT_yuzde']:.2f}, fark {bz['temiz_dogruluk_farki_puan']:+.2f} puan. "
                 f"Dort protokol asimetrisi (CNN->ViT eksi ViT->CNN): "
                 + ", ".join(f"{_ETIKET[k_]} {v_:+.2f}" for k_, v_ in bz["asimetri_CNNtoViT_eksi_ViTtoCNN_puan"].items())
                 + f". Gozlenen ham eksi tc {bz['gozlenen_ham_eksi_tc_puan']:+.2f}, ham eksi bc {bz['gozlenen_ham_eksi_bc_puan']:+.2f}. "
                   f"Kaynak temiz hata: ResNet-18 AT {bz['kaynak_temiz_hata_bizde_yuzde']['ResNet18_AT']:.2f}, "
                   f"ViT-Tiny AT {bz['kaynak_temiz_hata_bizde_yuzde']['ViT_Tiny_AT']:.2f}; Mahmood'da en buyuk kaynak temiz hata "
                   f"CIFAR-10 {bz['kaynak_temiz_hata_max_Mahmood_CIFAR10_yuzde']:.2f}, CIFAR-100 "
                   f"{bz['kaynak_temiz_hata_max_Mahmood_CIFAR100_yuzde']:.2f}.\n")
        satir = []
        for pk, v_ in bz["ozdeslik_sinamasi"].items():
            satir.append([pk, sg(v_["ham_asimetri_ongoru_bc_den_rtc_esit_rbc_varsayimi_puan"], 2, True),
                          sg(v_["ham_asimetri_ongoru_tc_den_tam_ozdeslik_puan"], 2, True),
                          sg(v_["gozlenen_ham_asimetri_puan"], 2, True), sg(v_["yaklasim_hatasi_bc_den_puan"], 2, True),
                          sg(v_["protokol_etkisi_ongoru_ham_eksi_bc_puan"], 2, True)])
        T(["p", "Ham asimetri ongorusu (bc'den, r_tc = r_bc)", "Ham asimetri ongorusu (tc'den, tam ozdeslik)",
           "Gozlenen ham asimetri", "Yaklasim hatasi (bc'den)", "Ongorulen protokol etkisi (ham eksi bc)"], satir)
        L.append(f"Artefaktin notu: {bz['not']}\n")
    except (KeyError, TypeError, IndexError, ValueError) as e_:
        _hata(e_)

# --- 11. Secim kuralinin asimetriye etkisi -------------------------------------------
sec("Secim kuralinin asimetriye etkisi",
    "results/q1/secim_asimetri_etkisi.json (yorungeler/e3_akolu_v2); "
    "results/q1/son_kontrol_noktasi/pair{1,2,3}/havuz_protokoller.json; C1 secilmis kontrol noktasi degerleri: "
    "results/c1_transfer/c1_transfer_summary.json (values), results/c1_seeds/c1_seed_summary.json (pairs)")
SE = load("results/q1/secim_asimetri_etkisi.json")
if SE is None:
    yok("results/q1/secim_asimetri_etkisi.json")
else:
    try:
        L.append("### A. Saklanan egitim yorungeleri: secilen epok ve son epok\n")
        L.append(f"Yontem (artefakttan): {SE['yontem']}\n")
        L.append(f"Yon notu (artefakttan): {SE['yon_notu']}\n")
        L.append(f"Dizin notu (artefakttan): {SE['dizin_notu']} Kanonik dizin: `{SE['kanonik_dizin']}`.\n")
        YV = SE["yorungeler"][SE["kanonik_dizin"].rsplit("/", 1)[-1]]
        L.append("Temiz fark = temiz HATA farki, ViT eksi CNN (puan). 'Secilen' = referans secim hucresinin epoku "
                 "(artefaktta `referans_hucre`), 'en yakin saklanan epok'taki deger; 'Son' = yorungenin son epogu; "
                 "Delta = son - secilen. Yayilim = dort protokolde max-min asimetri. tc = hedef-dogru asimetri "
                 "(CNN->ViT eksi ViT->CNN). Saklanan epoklar yaklasik 10 epok aralikli; ara deger kestirimi yapilmamistir.\n")
        satir = []
        grup = {}
        for ad, v_ in YV.items():
            if isinstance(v_["secim_ozeti"], str):
                continue
            r_ = v_["secim_ozeti"]["referans_hucre"]
            s_ = v_["ozet"]["son"]
            d_ = v_["secim_ozeti"]["son_epok_eksi_referans"]
            tf_r, tf_s = r_["en_yakin_temiz_hata_farki_ViT_eksi_CNN"], s_["temiz_hata_farki_ViT_eksi_CNN"]
            y_r, y_s = r_["en_yakin_yayilim_dort"], s_["yayilim_dort"]
            a_r, a_s = r_["en_yakin_asimetri"]["target_correct"], s_["asimetri"]["target_correct"]
            b_r, b_s = r_["en_yakin_asimetri"]["both_correct"], s_["asimetri"]["both_correct"]
            assert abs((y_s - y_r) - d_["yayilim_dort"]) < 1e-3 and abs((a_s - a_r) - d_["asimetri"]["target_correct"]) < 1e-3
            kum = (v_["bilgi"]["dataset"], v_["bilgi"]["taranan_model"])
            grup.setdefault(kum, []).append((tf_s - tf_r, y_s - y_r, a_s - a_r, b_s - b_r, tf_r, tf_s, y_r, y_s, a_r, a_s))
            satir.append([ad, f"{r_['en_yakin_sakli_epok']} -> {v_['ozet']['son_epok']}",
                          f"{sg(tf_r)} / {sg(tf_s)} / {sg(tf_s - tf_r, 2, True)}",
                          f"{sg(y_r)} / {sg(y_s)} / {sg(y_s - y_r, 2, True)}",
                          f"{sg(a_r)} / {sg(a_s)} / {sg(a_s - a_r, 2, True)}",
                          f"{sg(b_r)} / {sg(b_s)} / {sg(b_s - b_r, 2, True)}"])
        T(["Yorunge", "Secilen (saklanan) -> son epok", "Temiz fark: secilen / son / Delta",
           "Yayilim (dort protokol): secilen / son / Delta", "tc asimetri: secilen / son / Delta",
           "bc asimetri: secilen / son / Delta"], satir)
        L.append("Grup ozeti (yorunge = bir egitim tohumu; ortalama$\\pm$SD ddof=1, ardindan en kucuk; en buyuk), Delta = son - secilen:\n")
        satir = []
        for (dset, mod), rows_ in grup.items():
            A = np.array(rows_)
            satir.append([dset, mod, len(rows_),
                          f"{ortsd(A[:, 0], 2, True)} ({mm(A[:, 0], 2, True)})",
                          f"{ortsd(A[:, 1], 2, True)} ({mm(A[:, 1], 2, True)})",
                          f"{ortsd(A[:, 2], 2, True)} ({mm(A[:, 2], 2, True)})",
                          f"{ortsd(A[:, 3], 2, True)} ({mm(A[:, 3], 2, True)})",
                          f"{mm(A[:, 4])} -> {mm(A[:, 5])}"])
        T(["Veri", "Taranan model", "n yorunge", "Temiz fark Delta", "Yayilim Delta", "tc asimetri Delta", "bc asimetri Delta",
           "Temiz fark: secilen araligi -> son araligi"], satir)
        L.append("Secim hucreleri arasi aralik (secim izgarasindaki hucrelerin en yakin saklanan epoklari; E2/B8 izgaralari), "
                 "en kucuk; en buyuk:\n")
        satir = []
        for ad, v_ in YV.items():
            if isinstance(v_["secim_ozeti"], str):
                continue
            so = v_["secim_ozeti"]
            ar = so["secim_hucreleri_arasi_asimetri_araligi"]
            satir.append([ad, len(v_["secim_hucreleri"]), f"{so['eslesen_sakli_epoklar']}", so["max_uzaklik_epok"],
                          mm(so["secim_hucreleri_arasi_yayilim_dort_araligi"]),
                          mm(so["secim_hucreleri_arasi_yayilim_uc_araligi"]),
                          mm(ar["target_correct"]), mm(ar["both_correct"])])
        T(["Yorunge", "Secim hucresi", "Eslesen saklanan epoklar", "En buyuk uzaklik (epok)", "Yayilim (dort)", "Yayilim (uc)",
           "tc asimetri", "bc asimetri"], satir)
        L.append("Veri kumesi duzeyinde yorunge ozetleri (artefaktin `veri_kumesi_duzeyi` alani; tum epok yorungesi uzerinden; "
                 "en kucuk; en buyuk, yorunge sayisiyla):\n")
        satir = []
        for ds, v_ in SE["veri_kumesi_duzeyi"].items():
            satir.append([ds, v_["yorunge_sayisi"], mm(v_["son_eksi_ilk_yayilim_dort"]["degerler"], 2, True),
                          mm(v_["yayilim_dort_max_eksi_min"]["degerler"]), mm(v_["asimetri_tc_max_eksi_min"]["degerler"]),
                          mm(v_["asimetri_bc_max_eksi_min"]["degerler"]),
                          mm(v_["yorunge_ici_r_yayilim_uc_vs_x"]["degerler"], 3), mm(v_["yorunge_ici_r_yayilim_dort_vs_x"]["degerler"], 3)])
        T(["Veri", "Yorunge", "Son - ilk yayilim (dort)", "Yayilim max-min (dort)", "tc asimetri max-min", "bc asimetri max-min",
           "Yorunge ici r: yayilim (uc) ~ temiz fark", "Yorunge ici r: yayilim (dort) ~ temiz fark"], satir)
        for k_, v_ in SE["eksikler"].items():
            L.append(f"- Eksik ({k_}): {v_}")
        L.append("")
    except (KeyError, TypeError, IndexError, ValueError, AssertionError) as e_:
        _hata(e_)

    # --- B. Son kontrol noktasi ---
    try:
        L.append("### B. Son kontrol noktasi (`last.pth`) ile C1 secilmis kontrol noktasi, ayni egitim ciftleri\n")
        SK = [load(f"results/q1/son_kontrol_noktasi/pair{p}/havuz_protokoller.json") for p in PAIRS]
        sd_ = load("results/c1_seeds/c1_seed_summary.json")
        if not all(SK):
            yok("results/q1/son_kontrol_noktasi/pair{1,2,3}/havuz_protokoller.json")
        elif sd_ is None or S["CIFAR-10 Linf"] is None:
            yok("results/c1_seeds/c1_seed_summary.json veya results/c1_transfer/c1_transfer_summary.json")
        else:
            C1D, C1S = S["CIFAR-10 Linf"]["D"], S["CIFAR-10 Linf"]["sprd"]
            L.append("Cift p = egitim cifti p (tohum 100p ResNet-18, 200p ViT-Tiny). Asimetri = ResNet-18 AT -> ViT-Tiny AT eksi "
                     "ViT-Tiny AT -> ResNet-18 AT (puan). Son kontrol noktasi: ornek bazli kayitlardan, `src/analysis/protokoller.py` "
                     "(dort protokol, n=10000), WRN-28-10 referansi ayni. C1 secilmis kontrol noktasi (`best.pth`): "
                     "`c1_transfer_summary.json` CNN_to_ViT ve ViT_to_CNN kosum degerleri (2 ondalikli saklidir), "
                     "temiz dogruluk `c1_seed_summary.json`. Yayilim (dort) = en buyuk - en kucuk protokol asimetrisi; "
                     "yayilim (uc) = raw, tc, bc uzerinden. Temiz fark = ResNet-18 AT eksi ViT-Tiny AT.\n")
            son, c1 = [], []
            for i, p_ in enumerate(PAIRS):
                cf = [c for c in SK[i]["ciftler"] if c["cift"] == ["ResNet18_AT", "ViT_Tiny_AT"]]
                assert len(cf) == 1
                cf = cf[0]
                asm = [cf["asimetri_ileri_eksi_geri"][k_] for k_, _ in PROTO]
                td_ = SK[i]["temiz_dogruluk"]
                son.append(asm + [cf["yayilim_dort_protokol"], cf["yayilim_uc_protokol_bas_kaynak_haric"],
                                  td_["ResNet18_AT"], td_["ViT_Tiny_AT"], td_["ResNet18_AT"] - td_["ViT_Tiny_AT"]])
                pr = sd_["pairs"][i]
                c1.append(list(C1D[:, i]) + [float(C1S[i]), float(C1D[:3, i].max() - C1D[:3, i].min()),
                                             pr["resnet"]["clean"], pr["vit"]["clean"],
                                             pr["resnet"]["clean"] - pr["vit"]["clean"]])
            son, c1 = np.array(son), np.array(c1)
            BAS = ["Cift", "raw", "tc", "bc", "ss", "Yayilim (dort)", "Yayilim (uc)", "Temiz ResNet-18", "Temiz ViT-Tiny",
                   "Temiz fark (R-V)"]

            def _blok(M, baslik, hepsi=False):
                L.append(f"{baslik}\n")
                satir_ = [[f"cift {p_}"] + [sg(x, 2, hepsi or k_ < 4 or k_ == 8) for k_, x in enumerate(M[i])]
                          for i, p_ in enumerate(PAIRS)]
                satir_.append(["ort.$\\pm$SD"] + [ortsd(M[:, k_], 2, hepsi or k_ < 4 or k_ == 8) for k_ in range(M.shape[1])])
                T(BAS, satir_)

            _blok(son, "Son kontrol noktasi (`last.pth`), `results/q1/son_kontrol_noktasi/pair*/havuz_protokoller.json`:")
            _blok(c1, "C1 secilmis kontrol noktasi (`best.pth`), `c1_transfer_summary.json` ve `c1_seed_summary.json`:")
            _blok(son - c1, "Fark (son kontrol noktasi - C1 secilmis), cift basina:", True)
            fk = son - c1
            L.append(f"Fark ozeti (son - C1 secilmis; ortalama$\\pm$SD, parantezde en kucuk ve en buyuk cift degeri): "
                     f"yayilim (dort) {ortsd(fk[:, 4], 2, True)} ({mm(fk[:, 4], 2, True)}); "
                     f"yayilim (uc) {ortsd(fk[:, 5], 2, True)} ({mm(fk[:, 5], 2, True)}); temiz fark {ortsd(fk[:, 8], 2, True)} "
                     f"({mm(fk[:, 8], 2, True)}); tc asimetri {ortsd(fk[:, 1], 2, True)} ({mm(fk[:, 1], 2, True)}). "
                     f"Aralik (en kucuk; en buyuk): temiz fark son {mm(son[:, 8])}, C1 secilmis {mm(c1[:, 8])}; "
                     f"yayilim (dort) son {mm(son[:, 4])}, C1 secilmis {mm(c1[:, 4])}; "
                     f"tc asimetri son {mm(son[:, 1], 2, True)}, C1 secilmis {mm(c1[:, 1], 2, True)}.\n")
            L.append("Son kontrol noktasi, ayni cift, yon bazinda p ve oncul p ozeti:\n")
            satir = []
            for i, p_ in enumerate(PAIRS):
                op = SK[i]["oncul_p_ozeti"]
                satir.append([f"cift {p_}", op["n_yon"], f"{op['p_min']:.4f}", f"{op['p_max']:.4f}",
                              sg(op["ozdeslik_artigi_mutlak_max_puan"], 2), sg(op["ozdeslik_artigi_mutlak_ort_puan"], 2)])
            T(["Cift", "Yon", "p en kucuk", "p en buyuk", "p=1 artigi, en buyuk mutlak (puan)", "p=1 artigi, ortalama mutlak (puan)"], satir)
            L.append("Son kontrol noktasi, WRN-28-10 referansli ciftler (cift basina, puan):\n")
            satir = []
            for i, p_ in enumerate(PAIRS):
                for c in SK[i]["ciftler"]:
                    if "WRN_28_10" not in c["cift"]:
                        continue
                    a_ = c["asimetri_ileri_eksi_geri"]
                    satir.append([f"cift {p_}", f"{c['cift'][0]} -> {c['cift'][1]} eksi ters"] +
                                 [sg(a_[k_], 2, True) for k_, _ in PROTO] +
                                 [sg(c["yayilim_dort_protokol"], 2), sg(c["yayilim_uc_protokol_bas_kaynak_haric"], 2),
                                  sg(c["temiz_dogruluk_farki_mutlak"], 2)])
            T(["Cift", "Yon", "raw", "tc", "bc", "ss", "Yayilim (dort)", "Yayilim (uc)", "Temiz fark (mutlak)"], satir)
    except (KeyError, TypeError, IndexError, ValueError, AssertionError) as e_:
        _hata(e_)

# --- 12. Standart egitimli hedeflerde oncul p (temiz ciftler) -----------------------
sec("Standart egitimli hedeflerde oncul p (temiz ciftler)",
    "results/q1/temiz_ciftler/pair{1,2,3}/havuz_protokoller.json")
TC = [load(f"results/q1/temiz_ciftler/pair{p}/havuz_protokoller.json") for p in PAIRS]
if not all(TC):
    yok("results/q1/temiz_ciftler/pair{1,2,3}/havuz_protokoller.json")
else:
    try:
        L.append("Ucu de standart (cekismeli olmayan) egitimli modellerdir: ResNet-18 ve ViT-Tiny temiz egitim cifti (tohum 100p / 200p), "
                 "Standard WRN-28-10 (RobustBench `Standard`, her ciftte ayni model). Saldiri PGD-10, Linf, eps = 8/255, n = 10000. "
                 "p = P(cekismeli ornek yanlis, hedef temizde yanlis iken); p=1 artigi = gozlenen ham oran eksi p = 1 "
                 f"varsayimiyla ozdeslik ongorusu (puan). Tohum {TC[0]['tohum']}. Kosegen yonler (kaynak = hedef) dahil degildir.\n")
        td_ = [t["temiz_dogruluk"] for t in TC]
        T(["Model"] + [f"cift {p}" for p in PAIRS] + ["ort.$\\pm$SD"],
          [[m_] + [sg(td_[i][m_]) for i in range(3)] + [ortsd([td_[i][m_] for i in range(3)])] for m_ in TC[0]["modeller"]])
        yon = [k_ for k_ in TC[0]["yonlu"] if k_.split("->")[0] != k_.split("->")[1]]
        satir = []
        P_hedef, A_hedef = {}, {}
        for y_ in yon:
            ps = [t["yonlu"][y_]["p_adv_yanlis_verili_temiz_yanlis"] for t in TC]
            ar = [t["yonlu"][y_]["ozdeslik_artigi_ham_eksi_ongoru"] for t in TC]
            nn = [t["yonlu"][y_]["n_temiz_yanlis"] for t in TC]
            tg = y_.split("->")[1]
            P_hedef.setdefault(tg, []).extend(ps)
            A_hedef.setdefault(tg, []).extend(ar)
            satir.append([y_, uc(nn, 0), uc(ps, 4), ortsd(ps, 4), f"{min(ps):.4f}; {max(ps):.4f}", uc(ar, 2, True), ortsd(ar, 2, True),
                          sg(max(abs(x) for x in ar), 2)])
        L.append("### Yon basina p ve p=1 artigi (uc cift)\n")
        T(["Yon (kaynak->hedef)", "Hedefte temiz yanlis sayisi (cift 1 / 2 / 3)", "p (cift 1 / 2 / 3)", "p ort.$\\pm$SD", "p en kucuk; en buyuk",
           "p=1 artigi (puan)", "Artik ort.$\\pm$SD", "En buyuk mutlak artik"], satir)
        L.append("### Hedef turune gore p ve p=1 artigi (uc cift x kaynaklar, 6 deger / hedef)\n")
        satir = []
        for tg in P_hedef:
            ps, ar = np.array(P_hedef[tg]), np.array(A_hedef[tg])
            satir.append([tg, len(ps), f"{ps.min():.4f}", f"{ps.max():.4f}", f"{ps.mean():.4f}", sg(float(ar.min()), 2, True),
                          sg(float(ar.max()), 2, True), sg(float(np.abs(ar).max()), 2), sg(float(np.abs(ar).mean()), 2)])
        allp = np.concatenate([np.array(v) for v in P_hedef.values()])
        alla = np.concatenate([np.array(v) for v in A_hedef.values()])
        satir.append(["Tum yonler", len(allp), f"{allp.min():.4f}", f"{allp.max():.4f}", f"{allp.mean():.4f}",
                      sg(float(alla.min()), 2, True), sg(float(alla.max()), 2, True), sg(float(np.abs(alla).max()), 2),
                      sg(float(np.abs(alla).mean()), 2)])
        T(["Hedef", "Deger sayisi", "p en kucuk", "p en buyuk", "p ortalama", "Artik en kucuk (puan)", "Artik en buyuk (puan)",
           "En buyuk mutlak artik", "Ortalama mutlak artik"], satir)
        _tut = max(abs(min(P_hedef[tg]) - min(t["oncul_p_ozeti"]["p_hedef_bazinda"][tg]["p_min"] for t in TC)) for tg in P_hedef)
        L.append(f"Artefaktin `oncul_p_ozeti` alanlariyla (hedef bazinda p_min) tutarlilik: en buyuk sapma {_tut:.2e}; "
                 "cift basina `ozdeslik_artigi_mutlak_max_puan`: " + ", ".join(
                     f"cift {p_} {t['oncul_p_ozeti']['ozdeslik_artigi_mutlak_max_puan']:.2f}" for p_, t in zip(PAIRS, TC)) + ".\n")
        # cift basina protokoller
        L.append("### Cift basina dort protokol asimetrisi ve yayilim\n")
        L.append("Asimetri = ilk model -> ikinci model eksi ters yon (puan); yayilim = en buyuk - en kucuk protokol asimetrisi "
                 "(dort ve uc: raw, tc, bc). Temiz fark mutlak.\n")
        satir = []
        tur = {}
        for i, p_ in enumerate(PAIRS):
            for c in TC[i]["ciftler"]:
                a_ = c["asimetri_ileri_eksi_geri"]
                satir.append([f"cift {p_}", f"{c['cift'][0]} -> {c['cift'][1]}"] + [sg(a_[k_], 2, True) for k_, _ in PROTO] +
                             [sg(c["yayilim_dort_protokol"], 2), sg(c["yayilim_uc_protokol_bas_kaynak_haric"], 2),
                              sg(c["temiz_dogruluk_farki_mutlak"], 2), "evet" if c["isaret_degisiyor_mu_dort_protokol"] else "hayir"])
                tur.setdefault(tuple(c["cift"]), []).append(c)
        T(["Cift", "Yon", "raw", "tc", "bc", "ss", "Yayilim (dort)", "Yayilim (uc)", "Temiz fark (mutlak)", "Isaret donuyor (dort)"], satir)
        L.append("### Cift turune gore ozet (uc cift, ortalama$\\pm$SD)\n")
        satir = []
        for ct, cs in tur.items():
            tf = [c["temiz_dogruluk_farki_mutlak"] for c in cs]
            y4 = [c["yayilim_dort_protokol"] for c in cs]
            y3 = [c["yayilim_uc_protokol_bas_kaynak_haric"] for c in cs]
            satir.append([f"{ct[0]} / {ct[1]}", uc(tf), ortsd(tf), uc(y4), ortsd(y4), uc(y3), ortsd(y3),
                          f"{sum(c['isaret_degisiyor_mu_dort_protokol'] for c in cs)}/{len(cs)}"])
        T(["Cift turu", "Temiz fark (cift 1 / 2 / 3)", "Temiz fark ort.$\\pm$SD", "Yayilim dort (1 / 2 / 3)", "Yayilim dort ort.$\\pm$SD",
           "Yayilim uc (1 / 2 / 3)", "Yayilim uc ort.$\\pm$SD", "Isaret donen cift (dort protokol)"], satir)
        rs = tur.get(("ResNet18_clean", "Standard_WRN28_10"))
        if rs:
            L.append("ResNet18_clean ve Standard_WRN28_10 cifti (eslenmis temiz dogruluk): temiz fark "
                     f"{uc([c['temiz_dogruluk_farki_mutlak'] for c in rs])} puan, yayilim (dort) "
                     f"{uc([c['yayilim_dort_protokol'] for c in rs])} puan, yayilim (uc) "
                     f"{uc([c['yayilim_uc_protokol_bas_kaynak_haric'] for c in rs])} puan (cift 1 / 2 / 3). "
                     "Bu ciftte dort protokol asimetrisi (raw / tc / bc / ss): "
                     + "; ".join(uc([c['asimetri_ileri_eksi_geri'][k_] for k_, _ in PROTO], 2, True) for c in rs) + " (cift basina).\n")
        # egim ve toplamsal
        L.append("### Cift basina yayilim ~ temiz fark egimi (3 nokta) ve toplamsal etkiler\n")
        satir = []
        for p_, t in zip(PAIRS, TC):
            e = t["egim_yayilim_temiz_fark"]
            satir.append([f"cift {p_}", sg(e["dort_protokol"]["egim"], 3, True), sg(e["dort_protokol"]["R2"], 4),
                          sg(e["uc_protokol_bas_kaynak_haric"]["egim"], 3, True), sg(e["uc_protokol_bas_kaynak_haric"]["R2"], 4),
                          e["dort_protokol"]["n_cift"]])
        T(["Cift", "Egim (dort)", "R2 (dort)", "Egim (uc)", "R2 (uc)", "Nokta"], satir)
        L.append("Her egim YALNIZ 3 noktadan (uc cift) hesaplanir; model bootstrap GA'si bu klasorlerde bos kalir "
                 f"(artefakt notu: {TC[0]['egim_yayilim_temiz_fark']['dort_protokol']['NOT']}). "
                 "Yayilim ~ temiz fark iliskisi icin tum-cift egimi 'Yayilim - temiz fark iliskisi (tum ciftler)' bolumundedir.\n")
        satir = []
        for p_, t in zip(PAIRS, TC):
            ta = t["toplamsal_kaynak_hedef_hedef_dogru"]
            for m_ in t["modeller"]:
                satir.append([f"cift {p_}", m_, sg(ta["kaynak_etkisi"][m_], 2, True), sg(ta["hedef_etkisi"][m_], 2, True)])
            satir.append([f"cift {p_}", "(uydurma)", f"R2 {ta['R2']:.4f}", f"en buyuk mutlak artik {ta['artik_max_mutlak']:.2f}; mu {ta['mu']:.2f}"])
        T(["Cift", "Model", "Kaynak etkisi", "Hedef etkisi"], satir)
    except (KeyError, TypeError, IndexError, ValueError) as e_:
        _hata(e_)

# --- 13. RobustBench havuzu (CIFAR-10, egitim yok) ----------------------------------
sec("RobustBench havuzu (CIFAR-10, egitim yok)", "results/q1/havuz_cifar10/havuz_protokoller.json")
HV = load("results/q1/havuz_cifar10/havuz_protokoller.json")
if HV is None:
    L.append("_ARTEFAKT HENUZ YOK: `results/q1/havuz_cifar10/havuz_protokoller.json` bulunamadi; GPU kosusu "
             "(`logs/q1_temiz_ve_havuz.log`) bu foy uretilirken bitmemisti. Bu bolumdeki sayilar uretilemedi; "
             "kosu bitince `bash scripts/q1_havuz_analiz_hepsi.sh` ve bu betik yeniden calistirilir._\n")
else:
    try:
        L.append(f"Model sayisi {len(HV['modeller'])}; tohum {HV['tohum']}; PGD-10, Linf, eps = 8/255, n = 10000, ornek bazli kayit. "
                 f"Uretim: {HV['uretildi_utc']}. p ve p=1 artigi tanimlari 'Standart egitimli hedeflerde oncul p' bolumundeki gibidir.\n")
        satir = [[m_, sg(HV["temiz_dogruluk"][m_]), sg(HV["oncul_p_ozeti"]["p_hedef_bazinda"][m_]["p_min"], 4),
                  sg(HV["oncul_p_ozeti"]["p_hedef_bazinda"][m_]["p_max"], 4)] for m_ in HV["modeller"]]
        L.append("### Modeller, temiz dogruluklar ve hedef bazinda p\n")
        T(["Model", "Temiz dogruluk (%)", "p en kucuk (bu hedefe giden yonler)", "p en buyuk"], satir)
        op = HV["oncul_p_ozeti"]
        L.append(f"Tum yonler (kosegen haric, n = {op['n_yon']}): p en kucuk {op['p_min']:.4f}, p en buyuk {op['p_max']:.4f}; "
                 f"p=1 artigi en buyuk mutlak {op['ozdeslik_artigi_mutlak_max_puan']:.2f} puan, ortalama mutlak "
                 f"{op['ozdeslik_artigi_mutlak_ort_puan']:.2f} puan.\n")
        yk = [k_ for k_ in HV["yonlu"] if k_.split("->")[0] != k_.split("->")[1]]
        _pp = np.array([HV["yonlu"][k_]["p_adv_yanlis_verili_temiz_yanlis"] for k_ in yk])
        _aa = np.array([HV["yonlu"][k_]["ozdeslik_artigi_ham_eksi_ongoru"] for k_ in yk])
        L.append(f"Yonlu kayitlardan yeniden hesap: p {_pp.min():.4f}; {_pp.max():.4f}, artik en kucuk {_aa.min():+.2f}, en buyuk "
                 f"{_aa.max():+.2f}, ortalama mutlak {np.abs(_aa).mean():.2f} puan (yon sayisi {len(yk)}) "
                 + ("(artefaktin ozetiyle UYUMLU)" if abs(_pp.min() - op["p_min"]) < 1e-12 and abs(np.abs(_aa).max() - op["ozdeslik_artigi_mutlak_max_puan"]) < 1e-9
                    else "(artefaktin ozetiyle UYUSMUYOR; INCELE)") + ".\n")
        L.append("### Cift basina dort protokol asimetrisi, yayilim ve temiz fark\n")
        L.append("Asimetri = ilk model -> ikinci model eksi ters yon (puan). Temiz fark mutlak (puan).\n")
        satir = []
        for c in HV["ciftler"]:
            a_ = c["asimetri_ileri_eksi_geri"]
            satir.append([f"{c['cift'][0]} / {c['cift'][1]}"] + [sg(a_[k_], 2, True) for k_, _ in PROTO] +
                         [sg(c["yayilim_dort_protokol"], 2), sg(c["yayilim_uc_protokol_bas_kaynak_haric"], 2),
                          sg(c["temiz_dogruluk_farki_mutlak"], 2), "evet" if c["isaret_degisiyor_mu_dort_protokol"] else "hayir"])
        T(["Cift", "raw", "tc", "bc", "ss", "Yayilim (dort)", "Yayilim (uc)", "Temiz fark (mutlak)", "Isaret donuyor (dort)"], satir)
        L.append(f"Cift sayisi {len(HV['ciftler'])}; dort protokolde isaret donen cift "
                 f"{sum(c['isaret_degisiyor_mu_dort_protokol'] for c in HV['ciftler'])}/{len(HV['ciftler'])}.\n")
        ta = HV["toplamsal_kaynak_hedef_hedef_dogru"]
        L.append("### Toplamsal kaynak ve hedef etkileri (hedef-dogru oranlar, kosegen haric)\n")
        L.append(f"mu = {ta['mu']:.2f}, R2 = {ta['R2']:.4f}, en buyuk mutlak artik {ta['artik_max_mutlak']:.2f}, "
                 f"artik RMS {ta['artik_rms']:.2f}, hucre {ta['n_hucre']}.\n")
        T(["Model", "Kaynak etkisi", "Hedef etkisi"],
          [[m_, sg(ta["kaynak_etkisi"][m_], 2, True), sg(ta["hedef_etkisi"][m_], 2, True)] for m_ in HV["modeller"]])
        L.append("### Yayilim ~ temiz fark egimi (model birak-tut bootstrap, B asagida)\n")
        satir = []
        for ad, lab in (("dort_protokol", "Dort protokol"), ("uc_protokol_bas_kaynak_haric", "Uc protokol (raw, tc, bc)")):
            e = HV["egim_yayilim_temiz_fark"][ad]
            satir.append([lab, sg(e["egim"], 3, True), sg(e["kesisim"], 2, True), sg(e["R2"], 4), sg(e["pearson_r"], 4), e["n_cift"],
                          ga(e["egim_GA95_model_bootstrap"], 3) if e.get("egim_GA95_model_bootstrap") else "ARTEFAKT YOK",
                          e["bootstrap_gecerli_ornek"]])
        T(["Yayilim", "Egim", "Kesisim", "R2", "Pearson r", "Cift", "Egim %95 GA (model bootstrap)", "Gecerli bootstrap ornegi"], satir)
        L.append("GA, modeller (cift degil) uzerinden birak-tut bootstrap'tan gelir; cift sayisi serbestlik derecesi DEGILDIR "
                 f"(artefakt notu: {HV['egim_yayilim_temiz_fark']['dort_protokol']['NOT']}).\n")
    except (KeyError, TypeError, IndexError, ValueError) as e_:
        _hata(e_)

# --- 14. Yayilim - temiz fark iliskisi (tum ciftler) --------------------------------
sec("Yayilim - temiz fark iliskisi (tum ciftler)", "results/q1/fig_yayilim_temiz_fark_veri.json")
FG = load("results/q1/fig_yayilim_temiz_fark_veri.json")
if FG is None:
    yok("results/q1/fig_yayilim_temiz_fark_veri.json")
else:
    try:
        L.append(f"{FG['aciklama']} Uretim: {FG['uretildi_utc']}. Nokta sayisi: {FG['n_nokta']}; grup sayisi {len(FG['gruplar'])}.\n")
        L.append("### Grup basina nokta sayisi ve aralik (puan)\n")
        satir = []
        for g_ in FG["gruplar"]:
            pt = [n_ for n_ in FG["noktalar"] if n_["grup"] == g_]
            tfx = [n_["temiz_fark_mutlak"] for n_ in pt]
            y4 = [n_["yayilim_dort"] for n_ in pt]
            y3 = [n_["yayilim_uc"] for n_ in pt]
            satir.append([g_, len(pt), mm(tfx), mm(y4), mm(y3)])
        satir.append(["Tum noktalar", len(FG["noktalar"]), mm([n_["temiz_fark_mutlak"] for n_ in FG["noktalar"]]),
                      mm([n_["yayilim_dort"] for n_ in FG["noktalar"]]), mm([n_["yayilim_uc"] for n_ in FG["noktalar"]])])
        T(["Grup", "Nokta", "Temiz fark mutlak (en kucuk; en buyuk)", "Yayilim dort (en kucuk; en buyuk)",
           "Yayilim uc (en kucuk; en buyuk)"], satir)
        _sd1 = load("results/c1_seeds/c1_seed_summary.json")
        if HV is not None and _sd1 is not None and _wrn:
            _p1, _tdh = _sd1["pairs"][0], HV["temiz_dogruluk"]
            _ayni = (abs(_tdh["ResNet18_AT"] - _p1["resnet"]["clean"]) < 1e-6
                     and abs(_tdh["ViT_Tiny_AT"] - _p1["vit"]["clean"]) < 1e-6
                     and abs(_tdh["Gowal2020_WRN28_10"] - _wrn["results"]["clean"]["accuracy"]) < 1e-6)
            _kes = [c for c in HV["ciftler"] if set(c["cift"]) <= {"ResNet18_AT", "ViT_Tiny_AT", "Gowal2020_WRN28_10"}]
            L.append(f"Ortusme kontrolu: havuzdaki ResNet18_AT / ViT_Tiny_AT / Gowal2020_WRN28_10 temiz dogruluklari "
                     f"({_tdh['ResNet18_AT']:.2f} / {_tdh['ViT_Tiny_AT']:.2f} / {_tdh['Gowal2020_WRN28_10']:.2f}) "
                     f"`c1_seed_summary.json` cift 1 ve `wrn_eval_summary.json` ile "
                     + ("AYNI (ayni kontrol noktalari); " if _ayni else "FARKLI; ")
                     + f"bu uc modelden olusan {len(_kes)} havuz cifti, C1 cift 1'in (ayri saldiri kosusuyla yeniden olculmus) "
                       "ayni model cifti noktalariyla ortusur; tum-cift veri setinde (fig_yayilim_temiz_fark_veri.py) bu uc cift "
                       "havuz grubundan CIKARILIR, yalniz 'AT cifti' / 'WRN-28-10 referansiyla' gruplarinda sayilir "
                       f"(havuz grubunda {sum(1 for n in FG['noktalar'] if 'havuzu' in n['grup'])} nokta kalir).\n")
        if FG["n_nokta"] != len(FG["noktalar"]):
            L.append(f"UYARI: n_nokta {FG['n_nokta']} ile noktalar uzunlugu {len(FG['noktalar'])} UYUSMUYOR.\n")
        L.append("### Egimler (yayilim ~ temiz fark, OLS; nokta = yonsuz model cifti)\n")
        satir = []
        for ad, lab in (("dort_protokol", "Dort protokol"), ("uc_protokol_bas_kaynak_haric", "Uc protokol (raw, tc, bc)")):
            e = FG["egim"][ad]
            gb = e["grup_birak_egimleri"]
            satir.append([lab, sg(e["egim"], 3, True), sg(e["kesisim"], 2, True), sg(e["pearson_r"], 4), sg(e["spearman_rho"], 4), e["n_cift"],
                          mm(list(gb.values()), 3, True)])
        T(["Yayilim", "Egim", "Kesisim", "Pearson r", "Spearman rho", "Nokta", "Grup-birak egimleri (en kucuk; en buyuk)"], satir)
        for ad, lab in (("dort_protokol", "Dort protokol"), ("uc_protokol_bas_kaynak_haric", "Uc protokol")):
            e = FG["egim"][ad]
            L.append(f"Grup-birak egimleri, {lab}:\n")
            T(["Birakilan grup", "Egim"], [[k_, sg(v_, 3, True)] for k_, v_ in e["grup_birak_egimleri"].items()])
            L.append(f"Not (artefakttan): {e['NOT']}\n")
        op_ = FG["egim"]["ozdeslik_paritesi"]
        L.append("### Ozdeslik paritesi (p=1 yaklasikligi)\n")
        L.append(f"n = {op_['n']} nokta; ozdeslik-ongorulu ile olculen ham eksi tc farki arasinda mutlak sapma en buyuk "
                 f"{op_['mutlak_sapma_max']:.2f} puan, ortalama {op_['mutlak_sapma_ort']:.2f} puan; Pearson r = {op_['pearson_r']:.4f}. "
                 f"Not (artefakttan): {op_['NOT']}.\n")
        eu = FG["egim"]["uc_protokol_yayilimi_vs_raw_tc_farki"]
        L.append(f"Uc-protokol yayilimi = |ham - tc| asimetri farki (1e-9 icinde): {eu['esit_cift_sayisi_1e-9']}/{eu['n']} nokta. "
                 f"Not (artefakttan): {eu['NOT']}.\n")
        L.append(f"Kaynak notu: nokta listesi {len(FG['kaynaklar'])} artefaktin ozetinden toplanir (yollar ve SHA-256 ozetleri artefaktin `kaynaklar` alanindadir).\n")
    except (KeyError, TypeError, IndexError, ValueError) as e_:
        _hata(e_)

# --- 15. Uc-protokol egimi, SVHN dahil ------------------------------------------------
sec("Uc-protokol egimi, SVHN dahil", "results/q1/e3_uc_protokol_svhnli_fit.json")
E3 = load("results/q1/e3_uc_protokol_svhnli_fit.json")
if E3 is None:
    yok("results/q1/e3_uc_protokol_svhnli_fit.json")
else:
    try:
        L.append(f"Yontem (artefakttan): {E3['yontem']} Makaledeki ifadenin kaynagi (artefakttan): {E3['makaledeki_ifade_kaynagi']}. "
                 f"Uretim: {E3['uretildi_utc']}.\n")
        r_ = E3["sonuc"]
        satir = []
        for ad, lab in (("uc_protokol_svhn_dahil", "Uc protokol (raw, tc, bc), SVHN dahil"),
                        ("dort_protokol_svhn_dahil", "Dort protokol, SVHN dahil"),
                        ("ozdeslik_terimi_abs_ham_eksi_tc_ongoru_svhn_dahil", "Yalniz ozdeslik terimi (mutlak (ham - tc) ongorusu), SVHN dahil"),
                        ("uc_protokol_svhn_haric_gerileme_kontrolu", "Uc protokol, SVHN haric (gerileme kontrolu)")):
            e = r_[ad]
            satir.append([lab, sg(e["egim"], 4, True), ga(e["egim_GA95_kume_bootstrap"], 4), sg(e["kesisim"], 2, True),
                          sg(e["pearson_r"], 4), e["n_nokta"], e["n_kume"], "evet" if e["GA_sifiri_iceriyor_mu"] else "hayir",
                          e["atlanan_bootstrap"], mm(e["y_araligi"])])
        T(["Uydurma", "Egim", "%95 GA (kume bootstrap)", "Kesisim", "Pearson r", "Nokta", "Kume", "GA sifiri iceriyor mu",
           "Atlanan bootstrap", "y araligi (en kucuk; en buyuk)"], satir)
        L.append("### Saklanan artefaktlara karsi yeniden uretim\n")
        satir = []
        for ad, lab in (("kontrol_dort_protokol_vs_e3_asimetri_fit_svhnli", "Dort protokol (e3_asimetri_fit_svhnli.json)"),
                        ("kontrol_uc_protokol_svhn_haric_vs_e3_iki_kol_fit_B", "Uc protokol, SVHN haric (e3_iki_kol_fit.json B kolu)")):
            k_ = r_[ad]
            satir.append([lab, sg(k_["saklanan_egim"], 4, True), ga(k_["saklanan_GA"], 4), sg(k_["yeniden_egim"], 4, True),
                          ga(k_["yeniden_GA"], 4), f"{k_['egim_farki']:.1e}"])
        T(["Kontrol", "Saklanan egim", "Saklanan GA", "Yeniden egim", "Yeniden GA", "Egim farki"], satir)
        tt = r_["totoloji_kontrolu"]
        L.append("### Uc-protokol yayilimi = mutlak (ham - tc) esitligi\n")
        L.append(f"Esit cift sayisi: {tt['yayilim_uc_esit_abs_ham_eksi_tc_sayisi']}/{tt['toplam']} (yon cifti); "
                 f"mutlak (ham - tc) ile ozdeslik ongorusu arasinda en buyuk sapma {tt['max_abs_ham_eksi_tc_eksi_ozdeslik_ongorusu']:.2f} puan.\n")
        for b in tt["esitlik_bozulan_ciftler"]:
            L.append(f"- Esitligin bozuldugu cift: {b['kume']}, {b['yon_ileri']}; temiz fark {b['x']:.2f}, yayilim (uc) {b['yayilim_uc']:.4f}, "
                     f"mutlak (ham - tc) {b['abs_ham_eksi_tc']:.4f}, ozdeslik ongorusu {b['abs_ozdeslik_ongorusu']:.4f}; "
                     f"neden (artefakttan): {b['aradaki_protokol']}")
        L.append("")
    except (KeyError, TypeError, IndexError, ValueError) as e_:
        _hata(e_)

# --- 16. Dikkat entropisi TOST ve devrilen/devrilmeyen kosinus ------------------------
sec("Dikkat entropisi TOST ve devrilen/devrilmeyen kosinus", "results/c1_c4/c4_entropy_tost.json")
C4T = load("results/c1_c4/c4_entropy_tost.json")
if C4T is None:
    yok("results/c1_c4/c4_entropy_tost.json")
else:
    try:
        L.append(f"Yontem (artefakttan): {C4T['yontem']} Birim: {C4T['birim']}. Uretim: {C4T['uretildi_utc']}.\n")
        et = C4T["entropi_TOST"]
        L.append(f"Marj +-{et['marj_nat']} nat; katman sayisi {et['katman_sayisi']}; esdeger katman sayisi (marj {et['marj_nat']}) "
                 f"{et['esdeger_katman_sayisi_0.05']}/{et['katman_sayisi']}; en buyuk TOST p = {et['en_buyuk_p_TOST']:.5f}, "
                 f"artefakt katman indeksi {et['en_buyuk_p_katman']} (0-tabanli; foyun diger bolumlerindeki 1-tabanli "
                 f"numara: katman {et['en_buyuk_p_katman'] + 1}); katman ortalamasi mutlak degisimin en buyugu "
                 f"{et['max_abs_ortalama_degisim_nat']:.4f} nat; kosular arasi SD'nin en buyugu {et['max_kosular_arasi_sd_nat']:.4f} nat; "
                 f"temiz entropi katman ortalamasi araligi {mm(et['temiz_entropi_katman_ortalamasi_araligi_nat'], 3)} nat.\n")
        satir = []
        for k_ in et["katmanlar"]:
            satir.append([f"{k_['katman'] + 1} (indeks {k_['katman']})", uc(k_["degerler"], 4, True), sg(k_["ortalama"], 4, True),
                          sg(k_["sd"], 4), pf(k_["p_TOST"]), ga(k_["GA90"], 4), "evet" if k_["GA90_marj_icinde"] else "hayir",
                          "evet" if k_["esdeger_0.05"] else "hayir", sg(k_["temiz_entropi_ort"], 3)])
        T(["Katman (1-tabanli; artefakt indeksi)", "Kosu degerleri (adv - temiz, nat)", "Ortalama", "SD (kosular arasi)",
           "TOST p", "%90 GA", "GA marj icinde", "Esdeger", "Temiz entropi"], satir)
        gk = C4T["gerileme_kontrolu_c1_c45_summary"]
        L.append(f"Gerileme kontrolu: `c1_c45_summary.json` entropy_delta SD'si ile bu dosyadaki SD arasinda en buyuk fark "
                 f"{gk['c45_entropy_delta_std_ile_max_fark']:.1e} nat.\n")
        L.append("### Son blok kosinusu: devrilen ve devrilmeyen ornekler\n")
        L.append(f"Tanim notu (artefakttan): {C4T['kosinus_tanim_notu']}\n")
        satir = []
        for ad in ("ViT", "ResNet"):
            v_ = C4T["son_blok_kosinus_devrilen_vs_devrilmeyen"][ad]
            t_ = v_["eslesik_t_kosu_duzeyi"]
            satir.append([ad, v_["katman"], uc(v_["devrilen_kosu_ortalamalari"], 4), uc(v_["devrilmeyen_kosu_ortalamalari"], 4),
                          f"{v_['devrilen_ortalama_kosular_arasi']:.4f}{PM}{v_['devrilen_sd_kosular_arasi']:.4f}",
                          f"{v_['devrilmeyen_ortalama_kosular_arasi']:.4f}{PM}{v_['devrilmeyen_sd_kosular_arasi']:.4f}",
                          f"{v_['devrilen_havuz_n_agirlikli']:.4f} / {v_['devrilmeyen_havuz_n_agirlikli']:.4f}",
                          uc(v_["devrilen_n"], 0), uc(v_["devrilmeyen_n"], 0),
                          sg(t_["fark_ortalama"], 4, True), uc(t_["fark_degerleri"], 4, True), f"{t_['t']:+.3f}", t_["df"],
                          f"{t_['p_iki_yonlu']:.4f}", v_["isaret_tutarliligi"]])
        T(["Model", "Katman", "Devrilen, kosu ortalamalari", "Devrilmeyen, kosu ortalamalari", "Devrilen ort.$\\pm$SD (kosular arasi)",
           "Devrilmeyen ort.$\\pm$SD", "Havuz (n agirlikli): devrilen / devrilmeyen", "n devrilen (kosu 1 / 2 / 3)", "n devrilmeyen (kosu 1 / 2 / 3)",
           "Fark ortalama (devrilen - devrilmeyen)", "Fark, kosu degerleri", "t (kosu duzeyi, eslestirilmis)", "df", "p (iki yonlu)",
           "Isaret tutarliligi"], satir)
        L.append("Yorum siniri: kosu duzeyi n = 3; ornek bazli test yok.\n")
    except (KeyError, TypeError, IndexError, ValueError) as e_:
        _hata(e_)

# <<< IKINCI DALGA SONU

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
