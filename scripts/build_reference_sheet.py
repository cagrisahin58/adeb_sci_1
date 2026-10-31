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

# ===========================================================================
# GENISLETME 2026-10-04 (ucuncu dalga, hakem M8, yontem mercegi): govde metninde
# foyde karsiligi olmayan sayilar. Her sayi artefakttan (json, log, git) okunur;
# hicbir sayi elle yazilmaz. Mevcut bolumlere dokunulmaz. Karantina yollarindan
# (results/run1, run2, run3, attention_analysis_run3, stat_addendum, rev2_blockA)
# OKUNMAZ. Bolum 'Sabit dizgeler' bolumunden once eklenir.
# ===========================================================================
import glob as _m8glob
import re as _m8re
import subprocess as _m8sp
from itertools import combinations as _m8comb

sec("Govde metnindeki diger sayilar (hakem M8, 2026-10-04)",
    "results/q1/ozdeslik_kontrol.json; results/q1/c3_precision.json; results/c1_c3/c3_summary.json; "
    "results/q1/cifar10_l2/e6_onkestirim.json; results/c1_transfer/c1_transfer_summary.json; "
    "results/q1/cifar100/transfer/e1_transfer_summary.json; results/c1_addenda/pair*/mifgsm_transfer.json; "
    "results/c1_transfer/pair*/a2b_exclusive_subsets.json; results/q1/cifar100/transfer/pair*/a2b_class_balance_cifar100.json; "
    "results/q1/e1_cifar100_summary.json; logs/Q1_cifar100_clean_*.log; results/q1_research/E1_PILOT_KAPISI.md (kayitli bantlar); "
    "results/q1/e3_iki_kol_fit.json; results/q1/e3_surucu_ayristirma.json; results/q1/e3_asimetri_fit.json; "
    "results/q1/e2/e2_grid.json; results/q1/b8_secim_bandi.json; results/q1/variance_ratio.json; "
    "results/c1_seeds/c1_seed_summary.json; results/c1_gradient/pair*/gradient_summary.json; "
    "results/q1/cifar10_l2/e6_aa_l2_summary.json; results/q1/e7_svhn_summary.json; git (kayit ve pilot kapisi kayitlari); "
    "logs/C1_at_vit_200{1,2,3}.log; logs/C1_at_resnet_100{1,2,3}.log; results/q1/temiz_ciftler/pair{1,2,3}/havuz_protokoller.json; "
    "results/q1/havuz_cifar10/havuz_protokoller.json")
L.append("Hakem M8 (yontem mercegi), metinde foyde karsiligi olmayan yaklasik kirk sayi saptadi. Asagida her madde kendi alt "
         "basligindadir ve kendi artefaktindan okunur; 'Metin bicimi' sutunu sayinin metinde gececegi yuvarlamayi gosterir.\n")


def _oku(rel):
    d = load(rel)
    if d is None:
        raise OSError(f"ARTEFAKT YOK: {rel}")
    return d


def _m8(ad, fn):
    L.append(f"\n### {ad}\n")
    try:
        fn()
    except (KeyError, TypeError, IndexError, ValueError, OSError, ZeroDivisionError, AttributeError) as e_:
        _hata(e_)


def _tam(x):
    return f"{x:.6g}"


# --- M8.1 Ozdeslik artiklari -------------------------------------------------------------
def _m8_1():
    oz = _oku("results/q1/ozdeslik_kontrol.json")
    o = oz["ozet"]
    L.append(f"Artefakt: `results/q1/ozdeslik_kontrol.json`, uretim {o['uretildi_utc']}; yon sayisi {o['n_yon']}.\n")
    T(["Olcut", "Tam deger", "Metin bicimi", "Artefakt alani"], [
        ["En buyuk mutlak artik (puan)", _tam(o["ARTIK_puan"]["mutlak_max"]), sg(o["ARTIK_puan"]["mutlak_max"], 2),
         "ozet/ARTIK_puan/mutlak_max"],
        ["Ortalama mutlak artik (puan)", _tam(o["ARTIK_puan"]["mutlak_ort"]), sg(o["ARTIK_puan"]["mutlak_ort"], 3),
         "ozet/ARTIK_puan/mutlak_ort"],
        ["Artik / sapma orani, en buyuk (%)", _tam(o["artigin_sapmaya_orani_yuzde"]["max"]),
         sg(o["artigin_sapmaya_orani_yuzde"]["max"], 2), "ozet/artigin_sapmaya_orani_yuzde/max"],
        ["Artik / sapma orani, ortalama (%)", _tam(o["artigin_sapmaya_orani_yuzde"]["ort"]),
         sg(o["artigin_sapmaya_orani_yuzde"]["ort"], 2), "ozet/artigin_sapmaya_orani_yuzde/ort"],
        ["P(adv yanlis, verili temiz yanlis), en kucuk", _tam(o["P_advyanlis_verili_temizyanlis"]["min"]),
         sg(o["P_advyanlis_verili_temizyanlis"]["min"], 3), "ozet/P_advyanlis_verili_temizyanlis/min"],
        ["P(adv yanlis, verili temiz yanlis), ortalama", _tam(o["P_advyanlis_verili_temizyanlis"]["ort"]),
         sg(o["P_advyanlis_verili_temizyanlis"]["ort"], 3), "ozet/P_advyanlis_verili_temizyanlis/ort"]])


_m8("M8.1 Ozdeslik artiklari (36 yon)", _m8_1)


# --- M8.2 Egimler -------------------------------------------------------------------------
def _m8_2():
    cp = _oku("results/q1/c3_precision.json")["veri_kumeleri"]
    c3s = _oku("results/c1_c3/c3_summary.json")["raw_minus_cond_vs_target_error"]
    o1 = _oku("results/q1/cifar10_l2/e6_onkestirim.json")["O1_yon"]
    nok = o1["noktalar"]
    ayri = sorted({round(p_["e"], 2) for p_ in nok})
    wrn = sum(1 for p_ in nok if p_["yon"].split("->")[1].startswith("WRN"))
    T(["Ayar", "Egim (metin bicimi)", "Egim (tam)", "Kesisim", "Pearson r", "Yon sayisi", "Artefakt alani"], [
        ["CIFAR-10 Linf (ham - kosullu ~ hedef temiz hatasi)", sg(c3s["slope"], 3), _tam(c3s["slope"]), "-",
         sg(c3s["pearson_r"], 3), "6", "results/c1_c3/c3_summary.json raw_minus_cond_vs_target_error"],
        ["CIFAR-10 Linf (c3_precision, 4 ondalik)", sg(cp["cifar10"]["RAPOR_EDILEN_n6"]["egim"], 4),
         _tam(cp["cifar10"]["RAPOR_EDILEN_n6"]["egim"]), sg(cp["cifar10"]["RAPOR_EDILEN_n6"]["kesisim"], 4),
         sg(cp["cifar10"]["RAPOR_EDILEN_n6"]["pearson_r"], 4), cp["cifar10"]["n_kosegen_disi"],
         "results/q1/c3_precision.json veri_kumeleri/cifar10/RAPOR_EDILEN_n6"],
        ["CIFAR-100 Linf", sg(cp["cifar100"]["RAPOR_EDILEN_n6"]["egim"], 3), _tam(cp["cifar100"]["RAPOR_EDILEN_n6"]["egim"]),
         sg(cp["cifar100"]["RAPOR_EDILEN_n6"]["kesisim"], 4), sg(cp["cifar100"]["RAPOR_EDILEN_n6"]["pearson_r"], 4),
         cp["cifar100"]["n_kosegen_disi"], "results/q1/c3_precision.json veri_kumeleri/cifar100/RAPOR_EDILEN_n6"],
        ["CIFAR-10 L2", sg(o1["egim"], 3), _tam(o1["egim"]), sg(o1["kesisim"], 4), sg(o1["pearson_r"], 4), o1["n_yon"],
         "results/q1/cifar10_l2/e6_onkestirim.json O1_yon"]])
    L.append(f"L2 on-kestirim noktalari: {o1['n_yon']} yon, {len(ayri)} ayri hedef temiz hatasi degeri "
             f"({', '.join(sg(x, 2) for x in ayri)}); sabit WideResNet'e giden yon sayisi {wrn}. "
             f"Hedef hatasi araligi {mm(o1['hedef_hatasi_araligi'], 2)}.\n")


_m8("M8.2 Ham - kosullu egimleri (CIFAR-10 Linf, CIFAR-100 Linf, CIFAR-10 L2)", _m8_2)


# --- M8.3 Kosum duzeyi t araliklari ---------------------------------------------------------
def _m8_3():
    L.append("Kosum duzeyi t araligi: ortalama $\\pm$ t(0.975; df=2) x SD / sqrt(3); uc kosum (cift) degerinden. Her ayar icin iki "
             "kaynak verilir: eslestirilmis fark (`both_correct_paired/diff_pp/values`, ornek duzeyinde hesaplanmis, metindeki aralik "
             "bundan gelir) ve tabloda yazili protokol farki (`protocols/both_correct/diff/values`, 2 ondalikli yuvarlanmis).\n")
    satir = []
    for ad, rel in (("CIFAR-10 Linf", "results/c1_transfer/c1_transfer_summary.json"),
                    ("CIFAR-100 Linf", "results/q1/cifar100/transfer/e1_transfer_summary.json")):
        d = _oku(rel)
        for kay, v in (("both_correct_paired/diff_pp/values", d["both_correct_paired"]["diff_pp"]["values"]),
                       ("protocols/both_correct/diff/values", d["protocols"]["both_correct"]["diff"]["values"])):
            m, s, lo, hi, tk = t_aralik(v)
            satir.append([ad, f"`{rel.rsplit('/', 1)[-1]}` {kay}", uc(v, 2), sg(m, 3), sg(s, 3), f"{tk:.4f}",
                          ga((lo, hi), 2, False), ga((lo, hi), 3, False)])
    T(["Ayar", "Kaynak", "Kosum degerleri", "Ortalama", "SD (ddof=1)", "t(0.975; 2)", "t araligi (metin bicimi)", "t araligi (3 ondalik)"],
      satir)


_m8("M8.3 Her-ikisi-dogru farki icin kosum duzeyi t araligi (df=2)", _m8_3)


# --- M8.4 MI-FGSM iki yonlu kontrol ----------------------------------------------------------
def _m8_4():
    ps = [_oku(f"results/c1_addenda/pair{p}/mifgsm_transfer.json") for p in PAIRS]
    L.append(f"Saldiri (artefaktin kendi alani): {ps[0]['attack']}; eps = {ps[0]['eps']:.6f}; tohum {ps[0]['seed']}. "
             "Deger = kosullu (hedef-dogru) yaniltma orani (%), kosum basina; ortalama$\\pm$SD uc kosum arasi (ddof=1).\n")
    satir = []
    degerler = {}
    for s_, t_, lab in (("ResNet18_AT", "ViT_Tiny_AT", "CNN -> ViT"), ("ViT_Tiny_AT", "ResNet18_AT", "ViT -> CNN")):
        r_ = [[x for x in d["results"] if x["source"] == s_ and x["target"] == t_][0] for d in ps]
        v = [x["conditioned_fooling_rate"] for x in r_]
        degerler[lab] = v
        satir.append([lab, uc(v, 2), ortsd(v, 2), uc([x["n_conditioned"] for x in r_], 0),
                      "; ".join(ga(x["ci95"], 2, False) for x in r_)])
    T(["Yon", "Kosum degerleri (%)", "Ortalama$\\pm$SD", "n kosullu (kosum 1 / 2 / 3)", "Kosum basina %95 GA"], satir)
    fk = [a_ - b_ for a_, b_ in zip(degerler["CNN -> ViT"], degerler["ViT -> CNN"])]
    L.append(f"Yon farki (CNN -> ViT eksi ViT -> CNN), kosum basina: {uc(fk, 2, True)}; ortalama$\\pm$SD {ortsd(fk, 2, True)}.\n")
    bs = load("results/c1_behavior_summary.json")
    if bs and "mifgsm" in bs:
        L.append("Capraz kontrol, `results/c1_behavior_summary.json` mifgsm alani (ortalama, SD): "
                 + "; ".join(f"{k_}: {v_['mean']:.2f}, {v_['std']:.2f}" for k_, v_ in bs["mifgsm"].items()) + ".\n")


_m8("M8.4 MI-FGSM iki yonlu kontrol (alpha = eps/10)", _m8_4)


# --- M8.5 Marjinal alt kumeler, bilesim terimleri, korunma oranlari, bant marjlari -------------
def _m8_5():
    ex = [_oku(f"results/c1_transfer/pair{p}/a2b_exclusive_subsets.json") for p in PAIRS]
    L.append("#### Yalniz-hedef-dogru (marjinal) alt kumeler, CIFAR-10\n\n(kaynak: `results/c1_transfer/pair*/a2b_exclusive_subsets.json`): "
             "hedefin temizde dogru, kaynagin temizde yanlis bildigi ornekler; 'ortak dogru' ise her ikisinin dogru bildigi kume.\n")
    satir = []
    for yon, lab in (("ViT_to_CNN", "ViT -> CNN (hedef CNN)"), ("CNN_to_ViT", "CNN -> ViT (hedef ViT)")):
        n = [e[yon]["n_excl_target_only"] for e in ex]
        fe = [e[yon]["fooling_on_excl"] for e in ex]
        fb = [e[yon]["fooling_on_both"] for e in ex]
        satir.append([lab, ortsd(n, 0), ortsd(fe, 1), ortsd(fb, 1), sg(float(np.mean(fb)), 3), uc(n, 0), uc(fe, 2), uc(fb, 2)])
    T(["Yon", "Marjinal alt kume boyutu", "Yaniltma, marjinal (%)", "Yaniltma, ortak dogru (%)", "Ortak dogru ortalama (3 ondalik)", "Boyut (kosum 1 / 2 / 3)",
       "Marjinal yaniltma (kosum 1 / 2 / 3)", "Ortak dogru yaniltma (kosum 1 / 2 / 3)"], satir)
    L.append("Ortak dogru kume boyutu (kosum 1 / 2 / 3): " + uc([e["n_both_correct"] for e in ex], 0) + ".\n")

    a2b = [_oku(f"results/q1/cifar100/transfer/pair{p}/a2b_class_balance_cifar100.json") for p in PAIRS]
    L.append("\n#### Sinif bilesimi terimi, CIFAR-100\n\n(kaynak: `results/q1/cifar100/transfer/pair*/a2b_class_balance_cifar100.json` "
             "protokoller/*/AYRISTIRMA/bilesim_etkisi; puan, CNN -> ViT eksi ViT -> CNN asimetrisinin bilesim bileseni):\n")
    satir = []
    for k_, lab in PROTO:
        v = [d["protokoller"][k_]["AYRISTIRMA"]["bilesim_etkisi"] for d in a2b]
        satir.append([lab, uc(v, 3, True), ortsd(v, 3, True)])
    T(["Protokol", "Bilesim etkisi (kosum 1 / 2 / 3)", "Ortalama$\\pm$SD"], satir)

    e1 = _oku("results/q1/e1_cifar100_summary.json")
    L.append("\n#### Temiz on-egitim dogrulugunun adversarial egitimde korunmasi, CIFAR-100\n\npay = adversarial egitimli modelin temiz "
             "test dogrulugu (`e1_cifar100_summary.json` mimariler/*/ozet/test_clean/ort); payda = ayni tohumun temiz on-egitim "
             "logundaki `Best test accuracy` satiri (`logs/Q1_cifar100_clean_*.log`), uc tohum ortalamasi.\n")
    satir = []
    for arch, lab, onek, sd_ in (("resnet18", "ResNet-18", "resnet18", (1001, 1002, 1003)),
                                 ("vit_tiny", "ViT-Tiny", "vit_tiny", (2001, 2002, 2003))):
        en = []
        for s_ in sd_:
            yol = os.path.join(ROOT, f"logs/Q1_cifar100_clean_{onek}_{s_}.log")
            with open(yol, encoding="utf-8", errors="replace") as fh:
                bul = _m8re.findall(r"Best test accuracy:\s*([\d.]+)%", fh.read())
            en.append(float(bul[-1]))
        pay = e1["mimariler"][arch]["ozet"]["test_clean"]["ort"]
        satir.append([lab, uc(en, 2), sg(float(np.mean(en)), 3), sg(pay, 2), sg(pay / float(np.mean(en)), 3)])
    T(["Model", "Temiz on-egitim, en iyi (tohum 1 / 2 / 3)", "Ortalama", "AT sonrasi temiz (ort)", "Korunma orani"], satir)

    md_yol = os.path.join(ROOT, "results/q1_research/E1_PILOT_KAPISI.md")
    with open(md_yol, encoding="utf-8") as fh:
        md = fh.read()

    def bant(ad):
        m = _m8re.search(r"\|\s*" + _m8re.escape(ad) + r"\s*\|\s*%(\d+)-(\d+)\s*\|", md)
        return float(m.group(1)), float(m.group(2))

    L.append("\n#### Kayitli bantlara marj, ViT-Tiny, CIFAR-100\n\n(bantlar `results/q1_research/E1_PILOT_KAPISI.md` 'Beklenen aralik' "
             "tablosundan okunur; deger = `e1_cifar100_summary.json` vit_tiny/ozet/*/degerler, tohum duzeyi):\n")
    satir = []
    for ad, anah, lab in (("PGD-10 (test)", "test_pgd10", "PGD-10"), ("AutoAttack", "test_autoattack", "AutoAttack"),
                          ("Temiz (test)", "test_clean", "Temiz")):
        lo, hi = bant(ad)
        v = e1["mimariler"]["vit_tiny"]["ozet"][anah]["degerler"]
        alt, ust = min(v) - lo, hi - max(v)
        satir.append([lab, f"{sg(lo, 0)}-{sg(hi, 0)}", uc(v, 2), sg(alt, 2, True), sg(ust, 2, True),
                      sg(min(alt, ust), 2, True) if min(alt, ust) >= 0 else "bant disinda (marj negatif)"])
    T(["Uc nokta", "Kayitli bant (%)", "Tohum degerleri", "Alt kenara marj", "Ust kenara marj", "En yakin kenara marj (puan)"], satir)


_m8("M8.5 Marjinal alt kumeler, bilesim terimleri, korunma oranlari ve bant marjlari", _m8_5)


# --- M8.6 Iki kollu kalibrasyon ----------------------------------------------------------------
def _m8_6():
    f = _oku("results/q1/e3_iki_kol_fit.json")["kollar"]
    satir = []
    for kol, blk, lab in (("B", "dort_protokol", "B (gozlemsel havuz), dort protokol"),
                          ("B", "uc_protokol_bas_kaynak_haric", "B (gozlemsel havuz), uc protokol (basarili-kaynak haric)"),
                          ("A", "uc_protokol_bas_kaynak_haric", "A (kontrollu kol), uc protokol"),
                          ("A", "dort_protokol", "A (kontrollu kol), dort protokol"),
                          ("B_ana_cift", "dort_protokol", "B, yalniz ana cift (WRN'siz), dort protokol")):
        e = f[kol][blk]
        satir.append([lab, sg(e["egim"], 3, True), ga(e["egim_GA95"], 3), f[kol]["n_nokta"], f[kol]["n_kume"],
                      f"results/q1/e3_iki_kol_fit.json kollar/{kol}/{blk}"])
    T(["Kol ve uydurma", "Egim", "%95 GA (kume bootstrap)", "Nokta", "Kume", "Artefakt alani"], satir)
    sa = _oku("results/q1/e3_surucu_ayristirma.json")
    ak = sa["protokol_cifti_ortalama_aciklik"]["target_correct vs successful_source"]
    L.append(f"Hedef-dogru ile basarili-kaynak arasi ortalama aciklik (B kolu, {sa['n_cift']} yon): {sg(ak['ort_aciklik'], 2)} puan "
             f"(en buyuk {sg(ak['max_aciklik'], 2)}); `results/q1/e3_surucu_ayristirma.json` protokol_cifti_ortalama_aciklik.\n")
    uo = sa["protokol_uc_olma_sayilari"]["successful_source"]
    L.append(f"Basarili-kaynagin dort protokolun ucu (en kucuk ya da en buyuk) oldugu yon sayisi: {uo['min'] + uo['max']}/{sa['n_cift']} "
             f"(en kucuk {uo['min']}, en buyuk {uo['max']}); `protokol_uc_olma_sayilari`.\n")
    fa = _oku("results/q1/e3_asimetri_fit.json")["ciftler"]
    P4 = [k for k, _ in PROTO]
    gen = 0
    ss_uc = 0
    for c in fa:
        a_ = c["asimetri"]
        g = max(_m8comb(P4, 2), key=lambda pr: abs(a_[pr[0]] - a_[pr[1]]))
        gen += set(g) == {"target_correct", "successful_source"}
        ss_uc += (min(a_, key=a_.get) == "successful_source") + (max(a_, key=a_.get) == "successful_source")
    L.append(f"Ayni yon listesinden (`results/q1/e3_asimetri_fit.json` ciftler/*/asimetri, {len(fa)} yon) yeniden hesap: en genis protokol "
             f"cifti hedef-dogru ile basarili-kaynak olan yon sayisi {gen}/{len(fa)}; basarili-kaynagin uc oldugu yon sayisi {ss_uc}/{len(fa)}.\n")


_m8("M8.6 Iki kollu kalibrasyon (E3)", _m8_6)


# --- M8.7 Secim izgarasi ------------------------------------------------------------------------
def _m8_7():
    e2 = _oku("results/q1/e2/e2_grid.json")
    b8 = _oku("results/q1/b8_secim_bandi.json")["veri_kumeleri"]
    e1 = _oku("results/q1/e1_cifar100_summary.json")
    iz = e2["izgara"]
    L.append(f"CIFAR-10 izgarasi (`results/q1/e2/e2_grid.json`): {iz['hucre_sayisi']} hucre = bolme {iz['bolmeler']} x patience "
             f"{iz['patience']} x yumusatma k {iz['yumusatma_k']}; uc nokta: {iz['uc_nokta']}.\n")
    satir = []
    for arch, lab in (("resnet18", "ResNet-18"), ("vit_tiny", "ViT-Tiny")):
        m = e2["mimariler"][arch]
        rd = m["REFERANS_DUYARLILIGI"]
        satir.append([lab, ga(m["protokol_yayilim_araligi"], 2, False), sg(m["cekirdek_k1"]["oran"], 3),
                      f"{sg(rd['oran_min'], 3)}; {sg(rd['oran_max'], 3)}", f"{rd['birin_altinda_referans_sayisi']}/{rd['toplam_referans']}",
                      sg(m["tohum_sd_referans_protokolde"], 3)])
    T(["Model", "Protokol yayilimi, tohum basina aralik (puan)", "Cekirdek (yumusatma haric) oran", "Oran araligi (18 referans; en kucuk; en buyuk)",
       "Orani 1'in altinda kalan referans", "Tohum SD (referans protokolde)"], satir)
    L.append("CIFAR-100 ve CIFAR-10 icin 9 hucrelik (patience x yumusatma) secim yayilimi (`results/q1/b8_secim_bandi.json`):\n")
    satir = []
    for ds, lab in (("cifar100", "CIFAR-100"), ("cifar10", "CIFAR-10 (bolme basina)")):
        v = b8[ds]
        satir.append([lab, ga(v["yayilim_araligi"], 2, False), sg(v["yayilim_ort"], 4), len(v["yorungeler"]),
                      sg(v["yayilim_ort"], 2)])
    T(["Veri kumesi", "Yayilim araligi (puan)", "Yayilim ortalamasi (tam)", "Yorunge sayisi", "Ortalama (metin bicimi)"], satir)
    L.append("CIFAR-100 secim yolu ve sonuc (`results/q1/e1_cifar100_summary.json` mimariler/*/ozet):\n")
    satir = []
    for arch, lab in (("resnet18", "ResNet-18"), ("vit_tiny", "ViT-Tiny")):
        o = e1["mimariler"][arch]["ozet"]
        satir.append([lab, uc(o["en_iyi_epok"]["degerler"], 0), o["en_iyi_epok"]["aciklik"], uc(o["durma_epogu"]["degerler"], 0),
                      o["durma_epogu"]["aciklik"], sg(o["test_pgd10"]["sd"], 3), sg(o["test_pgd10"]["sd"], 2)])
    T(["Model", "En iyi epok (tohum 1 / 2 / 3)", "En iyi epok acikligi", "Durma epogu (tohum 1 / 2 / 3)", "Durma epogu acikligi",
       "Test PGD-10 SD (tam)", "Test PGD-10 SD (metin bicimi)"], satir)


_m8("M8.7 Secim izgarasi (CIFAR-10 18 hucre, 9 hucrelik sweep, CIFAR-100 epok acikligi)", _m8_7)


# --- M8.8 Varyans oranlari -----------------------------------------------------------------------
def _m8_8():
    vr = _oku("results/q1/variance_ratio.json")
    g = vr["ORAN_GUVEN_ARALIGI_chi2"]
    L.append(f"chi-kare araligi: {g['aciklama']}\n")
    satir = []
    for k_, lab in PROTO:
        p_ = g["protokol_bazli"][k_]
        satir.append([lab, sg(p_["kosum_sd"], 4), ga(p_["oran_95_GA"], 2, False), ga(p_["oran_95_GA"], 1, False),
                      "evet" if p_["GA_birimi_iceriyor_mu"] else "hayir"])
    T(["Protokol", "Kosum SD", "Oran %95 GA (2 ondalik)", "Oran %95 GA (metin bicimi)", "GA 1'i iceriyor mu"], satir)
    oa = vr["ORAN_ACIKLIGI"]
    sd2 = vr["ORAN_TANIMA_DUYARLI"]["sd_vs_sd"]["degerler"]
    T(["Olcut", "Tam deger", "Metin bicimi", "Artefakt alani"], [
        ["Oran duyarlilik araligi, en kucuk", _tam(oa["min"]), sg(oa["min"], 1), "ORAN_ACIKLIGI/min"],
        ["Oran duyarlilik araligi, en buyuk", _tam(oa["max"]), sg(oa["max"], 1), "ORAN_ACIKLIGI/max"],
        ["Benzeri-benzeriyle (both-correct) sd/sd orani", _tam(sd2["both_correct"]), sg(sd2["both_correct"], 1),
         "ORAN_TANIMA_DUYARLI/sd_vs_sd/degerler/both_correct"],
        ["Basarili-kaynak chi-kare GA, alt", _tam(g["protokol_bazli"]["successful_source"]["oran_95_GA"][0]),
         sg(g["protokol_bazli"]["successful_source"]["oran_95_GA"][0], 1), "protokol_bazli/successful_source/oran_95_GA[0]"],
        ["Basarili-kaynak chi-kare GA, ust", _tam(g["protokol_bazli"]["successful_source"]["oran_95_GA"][1]),
         sg(g["protokol_bazli"]["successful_source"]["oran_95_GA"][1], 1), "protokol_bazli/successful_source/oran_95_GA[1]"]])


_m8("M8.8 Varyans oranlari", _m8_8)


# --- M8.9 GPU-saat -------------------------------------------------------------------------------
def _m8_9():
    tm = _oku("results/c1_seeds/c1_seed_summary.json")["timing"]
    toplam = sum(tm["stage_seconds"].values()) / 3600.0
    T(["Olcut", "Tam deger", "Metin bicimi", "Artefakt alani"], [
        ["Toplam saat (artefakt)", _tam(tm["total_hours"]), sg(tm["total_hours"], 1), "timing/total_hours"],
        ["Asama saniyelerinin toplami / 3600", _tam(toplam), sg(toplam, 1), f"timing/stage_seconds ({len(tm['stage_seconds'])} asama)"]])


_m8("M8.9 GPU-saat (uc tohum hatti)", _m8_9)


# --- M8.10 Gradyan, kosum duzeyi p -----------------------------------------------------------------
def _m8_10():
    dos = sorted(_m8glob.glob(os.path.join(ROOT, "results/c1_gradient/pair*/gradient_summary.json")))
    if len(dos) != 3:
        raise OSError(f"ARTEFAKT YOK: results/c1_gradient/pair*/gradient_summary.json ({len(dos)} dosya)")
    S_ = []
    for f_ in dos:
        with open(f_, encoding="utf-8") as fh:
            S_.append(json.load(fh)["statistics"])
    L.append("Kosum duzeyi: uc kosumun (cift 1-3) ResNet18_AT ve ViT_Tiny_AT 500 ornek ortalamalari uzerinde eslestirilmis t testi "
             "(df=2, iki yonlu); Holm duzeltmesi yalniz uc olcek-bagimsiz seyreklik olcusu uzerinde (hizalanma ayri olcudur).\n")
    olc = (("sparsity_gini", "Gini"), ("sparsity_rel_threshold", "Rel-esik (%1 alti)"), ("sparsity_hoyer", "Hoyer"),
           ("gradient_alignment", "Hizalanma (mutlak kosinus)"))
    p = {}
    ist = {}
    for k_, _ in olc:
        R_ = np.array([s["ResNet18_AT"][k_] for s in S_])
        V_ = np.array([s["ViT_Tiny_AT"][k_] for s in S_])
        t_ = stats.ttest_rel(R_, V_)
        p[k_] = float(t_.pvalue)
        ist[k_] = (R_, V_, float(t_.statistic))
    hk = [k_ for k_, _ in olc[:3]]
    ph = holm([p[k_] for k_ in hk])
    satir = []
    for k_, lab in olc:
        R_, V_, t_ = ist[k_]
        if k_ in hk:
            pm, pol = sg(p[k_], 3), sg(float(ph[hk.index(k_)]), 3)
        else:
            pm, pol = sg(p[k_], 4), "-"
        satir.append([lab, uc(R_, 4), uc(V_, 4), sg(float((R_ - V_).mean()), 4, True), f"{t_:+.3f}", pm, sg(p[k_], 6), pol])
    T(["Olcu", "ResNet-18 AT (kosum 1 / 2 / 3)", "ViT-Tiny AT (kosum 1 / 2 / 3)", "Fark ortalamasi (R-V)", "t (df=2)",
       "p ham (metin bicimi)", "p ham (6 ondalik)", "p Holm (uc olcu)"], satir)
    L.append(f"Uc seyreklik olcusunun Holm duzeltilmis p'sinin en buyugu: {sg(float(max(ph)), 3)}.\n")


_m8("M8.10 Gradyan seyrekligi ve hizalanma, kosum duzeyi p", _m8_10)


# --- M8.11 L2 McNemar siniri -------------------------------------------------------------------------
def _m8_11():
    e6 = _oku("results/q1/cifar10_l2/e6_aa_l2_summary.json")
    mc = e6["mcnemar_gurbuz"]
    satir = [[f"cift {m['cift']}", f"{m['a']} / {m['b']}", m["yalniz_a_dogru"], m["yalniz_b_dogru"], f"{m['p']:.3e}"] for m in mc]
    T(["Cift", "A / B", "Yalniz A dogru", "Yalniz B dogru", "McNemar p (tam binom)"], satir)
    ust = max(m["p"] for m in mc)
    L.append(f"Uc cift icin ortak sinir: en buyuk p = {ust:.3e}; p < 10^-{int(-np.ceil(np.log10(ust)))} "
             "(ceil kuralina gore; bkz. foyun HER-IKISI-DOGRU McNemar notu). Eksik cift: "
             f"{e6['eksik_ciftler'] if e6['eksik_ciftler'] else 'yok'}.\n")


_m8("M8.11 L2 AutoAttack McNemar siniri (`mcnemar_gurbuz`)", _m8_11)


# --- M8.12 SVHN ----------------------------------------------------------------------------------------
def _m8_12():
    e7 = _oku("results/q1/e7_svhn_summary.json")["mimariler"]
    R_, V_ = e7["resnet18"], e7["vit_tiny"]
    sr, sv = sorted(R_["tohumlar"]), sorted(V_["tohumlar"])
    cr = [R_["tohumlar"][s]["test_clean"] for s in sr]
    cv = [V_["tohumlar"][s]["test_clean"] for s in sv]
    pr = [R_["tohumlar"][s]["test_pgd10"] for s in sr]
    pv = [V_["tohumlar"][s]["test_pgd10"] for s in sv]
    L.append(f"SVHN test kumesi n = {R_['tohumlar'][sr[0]]['test_n']}; iki tohum cifti (ResNet tohum {', '.join(sr)}; ViT tohum {', '.join(sv)}).\n")
    T(["Model", "Temiz (tohum 1 / 2)", "Temiz, artefaktin ort / sd alani", "PGD-10 (tohum 1 / 2)", "PGD-10, artefaktin ort / sd alani"], [
        ["ResNet-18 AT", uc(cr, 2), f"{sg(R_['ozet']['test_clean']['ort'], 2)} / {sg(R_['ozet']['test_clean']['sd'], 2)}",
         uc(pr, 2), f"{sg(R_['ozet']['test_pgd10']['ort'], 2)} / {sg(R_['ozet']['test_pgd10']['sd'], 2)}"],
        ["ViT-Tiny AT", uc(cv, 2), f"{sg(V_['ozet']['test_clean']['ort'], 2)} / {sg(V_['ozet']['test_clean']['sd'], 2)}",
         uc(pv, 2), f"{sg(V_['ozet']['test_pgd10']['ort'], 2)} / {sg(V_['ozet']['test_pgd10']['sd'], 2)}"]])
    gf = [a_ - b_ for a_, b_ in zip(cr, cv)]
    gm = float(np.mean(cr)) - float(np.mean(cv))
    gy = R_["ozet"]["test_clean"]["ort"] - V_["ozet"]["test_clean"]["ort"]
    pg = [a_ - b_ for a_, b_ in zip(pr, pv)]
    T(["Temiz dogruluk farki (ResNet - ViT, puan)", "Deger", "Metin bicimi (2 ondalik)"], [
        ["Cift 1 / cift 2 (tohum cifti basina)", uc(gf, 4, True), uc(gf, 2, True)],
        ["Ciftlerin fark ortalamasi", sg(float(np.mean(gf)), 4), sg(float(np.mean(gf)), 2)],
        ["Tam hassasiyetli ortalamalar farki (ort ResNet - ort ViT, iki tohum degerinden)", sg(gm, 4), sg(gm, 2)],
        ["Artefaktin 2 ondalikli `ort` alanlarinin farki (YUVARLANMIS ortalamalar)", sg(gy, 4), sg(gy, 2)]])
    L.append(f"Not: iki tohum cifti icin dogru fark ortalamasi {sg(float(np.mean(gf)), 2)} puandir (iki yontem de bunu verir). "
             f"{sg(gy, 2)} degeri yalniz yuvarlanmis ortalamalarin ({sg(R_['ozet']['test_clean']['ort'], 2)} - "
             f"{sg(V_['ozet']['test_clean']['ort'], 2)}) farkindan cikar; tam hassasiyetli degildir. Metne ciftlerin fark ortalamasi olan 1.84 girmelidir.\n")
    L.append(f"PGD-10 farki (ResNet - ViT): cift basina {uc(pg, 2, True)}; ortalama {sg(float(np.mean(pg)), 3)} "
             f"(artefakt ort alanlarindan {sg(R_['ozet']['test_pgd10']['ort'] - V_['ozet']['test_pgd10']['ort'], 2)}).\n")


_m8("M8.12 SVHN temiz ve PGD-10 degerleri, temiz fark", _m8_12)


# --- M8.13 On kayit suresi ------------------------------------------------------------------------------
def _m8_13():
    yol = os.path.join(ROOT, "results/q1_research/TUR4_EYLEM_PLANI.md")
    with open(yol, encoding="utf-8") as fh:
        md = fh.read()
    m = _m8re.search(r"kayit\s+`([0-9a-f]{7,40})`.*?pilot kapisi\s+`([0-9a-f]{7,40})`", md, _m8re.S)
    if not m:
        raise ValueError("TUR4_EYLEM_PLANI.md icinde kayit/pilot kapisi commit kimlikleri bulunamadi")
    kay, pil = m.group(1), m.group(2)
    L.append(f"Commit kimlikleri `results/q1_research/TUR4_EYLEM_PLANI.md` Faz 2B/2C maddesi 2.3'ten okunur (E1 ongoru kaydi `{kay}`, "
             f"ilk sayi bildiren epok-5 pilot kapisi `{pil}`); sure git commit zamanlarindan hesaplanir. `results/q1/KOKEN.json` bu "
             "iki commit'in zamanini tasimaz.\n")
    from datetime import datetime
    zam = {}
    for h_ in (kay, pil):
        r_ = _m8sp.run(["git", "-c", f"safe.directory={ROOT}", "show", "-s", "--format=%cI", h_], cwd=ROOT,
                       capture_output=True, text=True)
        if r_.returncode != 0 or not r_.stdout.strip():
            raise OSError(f"ARTEFAKT YOK: git commit zamani okunamadi ({h_}): {r_.stderr.strip()[:120]}")
        zam[h_] = datetime.fromisoformat(r_.stdout.strip())
    dk = (zam[pil] - zam[kay]).total_seconds() / 60.0
    T(["Olcut", "Deger"], [["Ongoru kaydi commit zamani", f"{kay}: {zam[kay].isoformat()}"],
                           ["Pilot kapisi commit zamani", f"{pil}: {zam[pil].isoformat()}"],
                           ["Aradaki sure (dakika, tam)", sg(dk, 2)], ["Metin bicimi (tam dakikaya yuvarlanmis)", sg(dk, 0)]])


_m8("M8.13 On kayit ile ilk sayi arasindaki sure", _m8_13)


# --- M8.14 Son kontrol noktasi epoklari ------------------------------------------------------------------
def _m8_14():
    L.append("Kaynak: C1 adversarial egitim loglari (`logs/C1_at_vit_200{1,2,3}.log`, `logs/C1_at_resnet_100{1,2,3}.log`); ilerleme "
             "cubuklari (carriage return) ayrilarak 'Epoch N/100 - Loss' satirlari, 'Best model saved!' (secilen = en iyi dogrulama "
             "adversarial dogrulugunun epogu) ve 'Early stopping triggered at epoch N' (durma = son egitilen epok) okunur. Egitim bazi "
             "loglarda yeniden baslatilmistir ('Resuming'); epok sayaci devam eder.\n")
    satir = []
    ozet = {}
    for ad, onek, sd_ in (("ViT-Tiny AT", "C1_at_vit_", (2001, 2002, 2003)), ("ResNet-18 AT", "C1_at_resnet_", (1001, 1002, 1003))):
        for s_ in sd_:
            yol = os.path.join(ROOT, f"logs/{onek}{s_}.log")
            with open(yol, encoding="utf-8", errors="replace") as fh:
                parca = _m8re.split(r"[\r\n]+", fh.read())
            cur = en_iyi = dur = son = sayac = None
            en_iyi_acc = None
            resume = 0
            for ln in parca:
                m = _m8re.match(r"Epoch (\d+)/(\d+) - Loss", ln)
                if m:
                    cur = int(m.group(1))
                    son = cur
                    continue
                m = _m8re.search(r"Best model saved! Adv accuracy: ([\d.]+)%", ln)
                if m:
                    en_iyi, en_iyi_acc = cur, float(m.group(1))
                    continue
                m = _m8re.search(r"No improvement \((\d+)/(\d+)\)", ln)
                if m:
                    sayac = f"{m.group(1)}/{m.group(2)}"
                    continue
                m = _m8re.search(r"Early stopping triggered at epoch (\d+)", ln)
                if m:
                    dur = int(m.group(1))
                if ln.startswith("Resuming from epoch"):
                    resume += 1
            if dur is None or en_iyi is None:
                raise ValueError(f"{yol}: durma ya da en iyi epok okunamadi")
            satir.append([ad, s_, dur, en_iyi, dur - en_iyi, sayac, sg(en_iyi_acc, 2), son, resume])
            ozet.setdefault(ad, []).append((dur, en_iyi))
    T(["Model", "Tohum", "Durma epogu", "Secilen (en iyi) epok", "Durma - secilen", "Son sabir sayaci", "En iyi val adv (%)",
       "Logdaki son epok", "Yeniden baslatma"], satir)
    for ad, v in ozet.items():
        L.append(f"{ad}: durma epoklari {uc([a_ for a_, _ in v], 0)}; secilen epoklar {uc([b_ for _, b_ in v], 0)} (tohum sirasiyla).\n")


_m8("M8.14 Son kontrol noktasi epoklari (durma ve secilen epok)", _m8_14)


# --- M8.15 Temiz ciftlerde toplamsal kaynak-hedef ayristirmasi --------------------------------------------
def _m8_15():
    TC_ = [_oku(f"results/q1/temiz_ciftler/pair{p}/havuz_protokoller.json") for p in PAIRS]
    R_, V_, W_ = "ResNet18_clean", "ViT_Tiny_clean", "Standard_WRN28_10"
    L.append("Hedef-dogru oranlar (`toplamsal_kaynak_hedef_hedef_dogru`; 6 kosegen-disi hucre, mu + alpha_kaynak + beta_hedef, toplam-sifir "
             "kodlama, 1 artik serbestlik derecesi). Kaynak farki = alpha_ResNet18_clean - alpha_ViT_Tiny_clean; hedef farki = beta_ViT_Tiny_clean "
             "- beta_ResNet18_clean; asimetri = (ResNet18_clean -> ViT_Tiny_clean) eksi (ViT_Tiny_clean -> ResNet18_clean) hedef-dogru orani "
             "(`yonlu/*/oranlar/target_correct`); artik farki = asimetri - kaynak farki - hedef farki (burada hesaplanir). "
             "Ortalama$\\pm$SD uc cift arasidir (ddof=1).\n")
    ks, hs, asm, art, r2, mx, mu = [], [], [], [], [], [], []
    for t in TC_:
        ta = t["toplamsal_kaynak_hedef_hedef_dogru"]
        ks.append(ta["kaynak_etkisi"][R_] - ta["kaynak_etkisi"][V_])
        hs.append(ta["hedef_etkisi"][V_] - ta["hedef_etkisi"][R_])
        y = t["yonlu"]
        a = y[f"{R_}->{V_}"]["oranlar"]["target_correct"] - y[f"{V_}->{R_}"]["oranlar"]["target_correct"]
        asm.append(a)
        art.append(a - ks[-1] - hs[-1])
        r2.append(ta["R2"])
        mx.append(ta["artik_max_mutlak"])
        mu.append(ta["mu"])
    T(["Olcut", "Cift 1 / 2 / 3", "Ortalama$\\pm$SD"], [
        ["Kaynak farki (ResNet - ViT)", uc(ks, 2, True), ortsd(ks, 2, True)],
        ["Hedef farki (ViT - ResNet)", uc(hs, 2, True), ortsd(hs, 2, True)],
        ["Asimetri (R->V eksi V->R)", uc(asm, 2, True), ortsd(asm, 2, True)],
        ["Artik farki (hesaplanan)", uc(art, 2, True), ortsd(art, 2, True)],
        ["R2", uc(r2, 4), ortsd(r2, 4)],
        ["En buyuk mutlak artik (puan)", uc(mx, 2), ortsd(mx, 2)],
        ["mu", uc(mu, 2), ortsd(mu, 2)]])
    satir = []
    for m_ in (R_, V_, W_):
        ka = [t["toplamsal_kaynak_hedef_hedef_dogru"]["kaynak_etkisi"][m_] for t in TC_]
        he = [t["toplamsal_kaynak_hedef_hedef_dogru"]["hedef_etkisi"][m_] for t in TC_]
        satir.append([m_, uc(ka, 2, True), ortsd(ka, 2, True), uc(he, 2, True), ortsd(he, 2, True)])
    T(["Model", "Kaynak etkisi (cift 1 / 2 / 3)", "Ortalama$\\pm$SD", "Hedef etkisi (cift 1 / 2 / 3)", "Ortalama$\\pm$SD"], satir)
    L.append("Sabit-Standard karsitliklari (hedef-dogru oran, %; `yonlu/*/oranlar/target_correct`; fark = ResNet18_clean tarafi eksi ViT_Tiny_clean tarafi):\n")
    satir = []
    for lab, a_, b_ in (("Hedef Standard: ResNet18_clean->Standard ile ViT_Tiny_clean->Standard", f"{R_}->{W_}", f"{V_}->{W_}"),
                        ("Kaynak Standard: Standard->ResNet18_clean ile Standard->ViT_Tiny_clean", f"{W_}->{R_}", f"{W_}->{V_}")):
        x = [t["yonlu"][a_]["oranlar"]["target_correct"] for t in TC_]
        z = [t["yonlu"][b_]["oranlar"]["target_correct"] for t in TC_]
        fk = [p_ - q_ for p_, q_ in zip(x, z)]
        satir.append([lab, uc(x, 2), ortsd(x, 2), uc(z, 2), ortsd(z, 2), uc(fk, 2, True), ortsd(fk, 2, True)])
    T(["Karsitlik", "Birinci taraf (cift 1 / 2 / 3)", "Ortalama$\\pm$SD", "Ikinci taraf (cift 1 / 2 / 3)", "Ortalama$\\pm$SD",
       "Fark (cift 1 / 2 / 3)", "Fark ortalama$\\pm$SD"], satir)


_m8("M8.15 Temiz ciftlerde toplamsal kaynak-hedef ayristirmasi ve sabit-Standard karsitliklari", _m8_15)


# --- M8.16 Havuz: XCiT ve ViT kaynak etkisi -----------------------------------------------------------------
def _m8_16():
    HV_ = _oku("results/q1/havuz_cifar10/havuz_protokoller.json")
    ta = HV_["toplamsal_kaynak_hedef_hedef_dogru"]
    rob = [m_ for m_ in HV_["modeller"] if m_ not in ("Standard_WRN28_10", "ViT_Tiny_AT")]
    ka = {m_: ta["kaynak_etkisi"][m_] for m_ in rob}
    he = {m_: ta["hedef_etkisi"][m_] for m_ in rob}
    L.append("Bu degerler foyun 'RobustBench havuzu' bolumundeki model etkileri tablosunda da vardir; burada metindeki aralik ifadeleri "
             "ayni artefakttan (`results/q1/havuz_cifar10/havuz_protokoller.json` toplamsal_kaynak_hedef_hedef_dogru) turetilir.\n")
    T(["Olcut", "Deger"], [
        ["R2 / hucre", f"{sg(ta['R2'], 4)} / {ta['n_hucre']}"],
        ["ViT_Tiny_AT kaynak etkisi", sg(ta["kaynak_etkisi"]["ViT_Tiny_AT"], 2, True)],
        ["ViT_Tiny_AT hedef etkisi", sg(ta["hedef_etkisi"]["ViT_Tiny_AT"], 2, True)],
        ["Debenedetti2022_XCiT_S12 kaynak etkisi", sg(ta["kaynak_etkisi"]["Debenedetti2022_XCiT_S12"], 2, True)],
        [f"Diger {len(rob)} gurbuz modelin kaynak etkisi araligi (ViT_Tiny_AT ve Standard haric)",
         f"{sg(min(ka.values()), 2, True)}; {sg(max(ka.values()), 2, True)}"],
        [f"Ayni {len(rob)} gurbuz modelin hedef etkisi araligi", f"{sg(min(he.values()), 2, True)}; {sg(max(he.values()), 2, True)}"]])


_m8("M8.16 Havuz: XCiT ve ViT-Tiny kaynak etkisi (foyde zaten var; aralik ifadeleri turetildi)", _m8_16)

# <<< UCUNCU DALGA SONU (hakem M8)

# ===========================================================================
# GENISLETME 2026-10-31 (M9, konsey turu 29-30.10.2026): on kayitli B2-B6
# bloklarinin sonuclari (sonuc bolgesi O1). Her sayi dondurulmus cozumleme
# betiginin JSON ciktilarindan, B3 defterinden (TSV) ve B6 dosyalarindan okunur;
# hicbir sayi elle yazilmaz. Esikler de JSON'dan ya da dondurulmus betigin
# kaynak metninden okunur. Mevcut bolumlere dokunulmaz; karantina yollarindan
# OKUNMAZ. Bolum 'Sabit dizgeler' bolumunden once eklenir. Kaynak dizini:
# raporlar/konsey_2026-10-29/09_sonuc_b2_b6.md ("Sayi kaynak dizini").
# ===========================================================================
import csv as _m9csv
import hashlib as _m9hl

_M9_J2 = "results/q1/konsey_ayrisim_b2.json"
_M9_J4 = "results/q1/konsey_ayrisim_b4.json"
_M9_J5 = "results/q1/konsey_ayrisim_b5.json"
_M9_M6 = "results/q1/konsey_b6_maskeleme.json"
_M9_DF = "results/q1/konsey_b3_defter.tsv"
_M9_HT = "raporlar/konsey_2026-10-29/hucre_tablosu.json"
_M9_TM = "results/q1/konsey_b4_matris/transfer_matrix.json"
_M9_AA = "results/q1/konsey_b6_aa/autoattack_results.csv"
_M9_BETIK = "experiments/q1_konsey_ayrisim.py"
_M9_OK = "raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md"
_M9_YOK = []


def _m9(ad, kaynak, fn):
    L.append(f"\n### {ad}\n")
    try:
        fn()
    except (KeyError, TypeError, IndexError, ValueError, OSError, ZeroDivisionError, AttributeError) as e_:
        _hata(e_)
    L.append(f"_Kaynak: {kaynak}_\n")


def _m9s(x, nd=3, plus=False):
    return "bulunamadi" if x is None else sg(float(x), nd, plus)


def _m9p(x):
    return "bulunamadi" if x is None else f"{float(x):.2e}"


def _m9a(a, nd=3, plus=False):
    if a is None:
        return "bulunamadi"
    return f"[{_m9s(a[0], nd, plus)}; {_m9s(a[1], nd, plus)}]"


def _m9e(x):
    return {True: "evet", False: "hayir", "True": "evet", "False": "hayir"}.get(x, "bulunamadi" if x is None else str(x))


def _m9g(d, yol, etiket):
    """Noktali anahtar yolunu izler; yoksa None doner ve kalemi bulunamayanlar listesine yazar."""
    x = d
    for k_ in yol:
        if isinstance(x, dict) and k_ in x:
            x = x[k_]
        else:
            _M9_YOK.append(etiket)
            return None
    return x


def _m9sha(rel, govde=False):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        b_ = fh.read()
    if govde:
        i_ = b_.find(b"\n## Dondurma eki\n")
        if i_ < 0:
            raise ValueError(f"{rel}: '## Dondurma eki' basligi yok")
        b_ = b_[:i_ + 1]
    return _m9hl.sha256(b_).hexdigest()


def _m9oran(d, nd=3, plus=True):
    """{model: deger} sozlugunde en kucuk ve en buyuk, model adlariyla."""
    k_min = min(d, key=d.get)
    k_max = max(d, key=d.get)
    return f"{sg(d[k_min], nd, plus)} ({k_min} cikinca) ile {sg(d[k_max], nd, plus)} ({k_max} cikinca)"


_M9_PZ = "results/q1/konsey_pilot_zaman.json"
_M9_C1S = "results/c1_seeds/c1_seed_summary.json"
_M9_SN = "results/q1/konsey_sentez_r_tau_masa.json"
_M9_MC = "results/q1/konsey_masa/konsey_masa_cozumlemeleri.json"
_M9_P3Y = "results/q1/konsey_masa/_p3_carpimsal_yasa_masa.json"
_M9_P3P = "results/q1/konsey_masa/_p3_potansiyel_masa.json"
_M9_SR = "raporlar/konsey_2026-10-29/09_sonuc_b2_b6.md"
_M9_YOK_YER = []

sec("M9: Konsey turu, mimari x baslatma 2x2 ve w-tau-r ayrisimi (2026-10-30)",
    f"{_M9_J2}; {_M9_J4}; {_M9_J5}; {_M9_M6}; {_M9_DF}; {_M9_TM}; {_M9_AA}; {_M9_HT}; {_M9_PZ}; {_M9_C1S} (yalniz V-scr AA "
    f"capraz basvurusu); {_M9_SN}; {_M9_MC}; {_M9_P3Y}; {_M9_P3P}; "
    f"{_M9_BETIK} (dondurulmus, yalniz esik sabitleri ve sha256); {_M9_OK} (yalniz Dondurma eki ve govde sha256)")
L.append("29-30.10.2026 konsey turunda on kayitli B2, B3, B4, B5 ve B6 bloklari kosuldu. Asagidaki her alt bolum kendi "
         "artefaktindan okunur ve altinda kaynak dosya ile anahtar yollari yazilidir. Yuvarlama: log olcekli nicelikler ve "
         "oranlar 3 ondalik, puanlar (yuzde) 2 ondalik, t istatistigi 2 ondalik, p degerleri bilimsel gosterim; 3 ondalikta "
         "sifira yuvarlanan ya da elle yeniden uretilmesi gereken farklarda 4 ondalik (ilgili satirda belirtilir).\n")
_m9ht = load(_M9_HT)
L.append("Hucre tanimlari (`" + _M9_HT + "` hucreler): "
         + ("; ".join(f"{k_}: {v_}" for k_, v_ in _m9ht["hucreler"].items()) if _m9ht and "hucreler" in _m9ht
            else "ARTEFAKT YOK") + ".\n")


# --- M9.1 B3 egitim defteri ----------------------------------------------------------------
def _m9_1():
    with open(os.path.join(ROOT, _M9_DF), encoding="utf-8", newline="") as fh:
        sat = list(_m9csv.DictReader(fh, delimiter="\t"))
    ht = _oku(_M9_HT)["modeller"]
    m6 = _oku(_M9_M6)
    sira = []
    for r_ in sat:
        if r_["takma_ad"] not in sira:
            sira.append(r_["takma_ad"])

    def bul(ad, asama):
        x_ = [r_ for r_ in sat if r_["takma_ad"] == ad and r_["asama"] == asama]
        return x_[-1] if x_ else None

    s1, s2, tutarsiz, denet = [], [], [], []
    for ad in sira:
        tz, at, oz = bul(ad, "temiz"), bul(ad, "AT"), bul(ad, "at_ozet")
        kv = dict(_m8re.findall(r"(\w+)=(\S+)", oz["not"])) if oz else {}
        if at and kv.get("kosulan_epok") != at["epok"]:
            tutarsiz.append(ad)
        vp = kv.get("val_pgd")
        s1.append([ad, ht[ad]["hucre"], ht[ad]["tohum"], tz["epok"] if tz else "bulunamadi",
                   at["epok"] if at else "bulunamadi", kv.get("secilen_epok", "bulunamadi"), _m9e(kv.get("erken_durma")),
                   _m9e(kv.get("tavanda_durdu")), _m9e(kv.get("kirpilmis_olabilir")),
                   _m9s(float(vp), 2) if vp is not None else "bulunamadi"])
        mm6 = m6["modeller"].get(ad)
        if mm6 is None:
            s2.append([ad, "bulunamadi", "bulunamadi", "bulunamadi", "bulunamadi"])
        else:
            s2.append([ad, _m9s(mm6["temiz_dogruluk_aa"], 2), _m9s(mm6["pgd10_dogruluk"], 2), _m9s(mm6["aa_dogruluk"], 2),
                       _m9s(mm6["fark_puan"], 2)])
        dt = bul(ad, "denetim_temiz")
        ck = _m8re.search(r"cokus denetimi (\S+) ([\d.]+)", at["not"]) if at else None
        fk_ = _m8re.search(r"fark=(\S+)", dt["not"]) if dt else None
        dt_m = (dt["durum"] + (" (fark " + fk_.group(1) + " puan)" if fk_ else "")) if dt else "satiri yok"
        ck_m = (ck.group(1) + " " + sg(float(ck.group(2)), 2)) if ck else "satiri yok"
        denet.append(f"{ad}: temiz denetimi {dt_m}; AT cokus denetimi {ck_m}")
    L.append("Egitim (B3 defteri; 'Dogrulama PGD' secilen epoktaki dogrulama bolmesi PGD dogrulugu, %):\n")
    T(["Takma ad", "Hucre", "Tohum", "Temiz epok", "AT epok (kosulan)", "Secilen epok", "Erken durma", "Tavanda durdu",
       "Kirpilmis olabilir", "Dogrulama PGD (%)"], s1)
    L.append(f"Test kumesinin ilk {m6['n']} goruntusu (B6; PGD-10 B4 kosegeninden, AA `{_M9_AA}`; %):\n")
    T(["Takma ad", f"Temiz (ilk {m6['n']})", "PGD-10", "AutoAttack", "Fark PGD-10 - AA (puan)"], s2)
    top = sum(float(r_["sure_s"]) for r_ in sat if r_["asama"] in ("temiz", "AT") and r_["sure_s"])
    L.append(f"Defterdeki temiz ve AT asama surelerinin toplami (sure_s): {sg(top / 3600.0, 2)} sa. "
             f"AT satirindaki epok ile at_ozet kosulan_epok: {'uyusuyor (' + str(len(sira)) + '/' + str(len(sira)) + ')' if not tutarsiz else 'UYUSMUYOR: ' + ', '.join(tutarsiz)}. "
             f"Durum 'OK' disindaki egitim satiri: {sum(1 for r_ in sat if r_['asama'] in ('temiz', 'AT') and r_['durum'] != 'OK')}.\n")
    L.append("Denetimler (defter): " + "; ".join(denet) + ".\n")
    pz = _oku(_M9_PZ)
    sz, kat = [], []
    for ad in sira:
        at = bul(ad, "AT")
        pk = ht[ad]["hucre"].replace("-", "_")
        tp = _m9g(pz, ["parcalar", pk, "t_at_epok_s"], f"Pilot AT epok suresi ({_M9_PZ} parcalar.{pk}.t_at_epok_s)")
        if at is None or not at["sure_s"] or not at["epok"]:
            sz.append([ad, ht[ad]["hucre"], "bulunamadi", "bulunamadi", "bulunamadi", _m9s(tp, 1), "bulunamadi"])
            continue
        ep_s = float(at["sure_s"]) / float(at["epok"])
        if tp is not None:
            kat.append(ep_s / float(tp))
        sz.append([ad, ht[ad]["hucre"], at["sure_s"], at["epok"], sg(ep_s, 1), _m9s(tp, 1),
                   sg(ep_s / float(tp), 2) if tp is not None else "bulunamadi"])
    tv = pz["secilen_tavan"]
    L.append("AT epok suresi (hesaplama ayrintilari beyani icin; 'Defter' = AT satirindaki sure_s / epok, turetilmis; "
             "'Pilot' = on kayit oncesi bos GPU'da olculen epok suresi):\n")
    T(["Takma ad", "Hucre", "AT sure_s", "AT epok", "Defter epok suresi (s)", "Pilot epok suresi (s)", "Defter / pilot (kat)"], sz)
    L.append(f"Defter / pilot kat araligi: {mm(kat, 2) if kat else 'bulunamadi'} ({len(kat)} kosu). Pilot tahmini duvar saati "
             f"W({tv}) = {sg(pz['W_sa'][str(tv)], 2)} sa (secilen tavan {tv} epok; egitim payi {sg(pz['egitim_payi_sa'], 2)} sa). "
             f"Pilot yontemi: '{pz['yontem']}'.\n")


_m9("M9.1 B3 egitim defteri (alti yeni kosu)",
    f"`{_M9_DF}` (takma_ad, asama, epok, sure_s, durum; at_ozet notu: secilen_epok, kosulan_epok, erken_durma, "
    f"tavanda_durdu, kirpilmis_olabilir, val_pgd; denetim_temiz notu: fark; AT notu: cokus denetimi); "
    f"`{_M9_HT}` modeller.<m>.hucre, .tohum; `{_M9_M6}` n, modeller.<m>.temiz_dogruluk_aa, .pgd10_dogruluk, "
    f".aa_dogruluk, .fark_puan; `{_M9_PZ}` parcalar.<hucre>.t_at_epok_s, secilen_tavan, W_sa.<tavan>, egitim_payi_sa, yontem", _m9_1)


# --- M9.2 2x2 hucre tablosu ----------------------------------------------------------------
def _m9_2():
    J4 = _oku(_M9_J4)
    b4 = J4["b4"]
    K = b4["F_B4"]["karsitliklar"]
    MT = b4["model_tablosu"]
    TM = _oku(_M9_TM)["results"]
    m6_ = _oku(_M9_M6)
    m6, n6 = m6_["modeller"], m6_["n"]
    ht = _oku(_M9_HT)["modeller"]
    kayitli = J4["veri"]["girdi_sha256"].get(_M9_TM)
    hes = _m9sha(_M9_TM)

    def temiz(m):
        v_ = {r_["target_clean_acc"] for k_, r_ in TM.items() if k_.split("->")[1] == m}
        if len(v_) != 1:
            raise ValueError(f"{m}: hedef temiz dogruluk kaynaklar arasinda tutarsiz {sorted(v_)}")
        return v_.pop()

    s1, s2, ex = [], [], []
    for h_, ms_ in b4["hucreler"].items():
        tz = [temiz(m) for m in ms_]
        w_ = [MT[m]["yari_oran"]["omega"] for m in ms_]
        aa = [m6[m]["aa_dogruluk"] for m in ms_ if m in m6]
        s1.append([h_, K["H2"]["hucre_n"][h_], uc(tz, 2), sg(float(np.mean(tz)), 2), uc(w_, 2), sg(float(np.mean(w_)), 2),
                   _m9s(b4["ikincil"]["S3"]["etkilesim"]["hucre_ort"][h_]), _m9s(K["H2"]["hucre_ort"][h_], 3, True),
                   _m9s(K["H3"]["hucre_ort"][h_], 3, True),
                   (uc(aa, 2) if len(aa) == len(ms_) else "B6 kapsami disi (konsey_b6_maskeleme.json'da yok)")])
        for m in ms_:
            ex.append(abs(float(np.exp(MT[m]["yari_log"]["omega"])) - MT[m]["yari_oran"]["omega"]))
            s2.append([h_, m, ht[m]["tohum"], sg(temiz(m), 2), sg(MT[m]["yari_oran"]["omega"], 2),
                       sg(MT[m]["yari_log"]["omega"], 3), sg(MT[m]["yari_log"]["sigma"], 3, True),
                       sg(MT[m]["yari_log"]["rho"], 3, True),
                       sg(m6[m]["aa_dogruluk"], 2) if m in m6 else "B6 disi"])
    L.append("Hucre ozetleri (w = beyaz kutu hedef-dogru kirilganlik, %; omega = log w; sigma ve rho bolunmus yari, log olcek; "
             "temiz dogruluk tam test kumesi):\n")
    T(["Hucre", "Tohum sayisi n", "Temiz dogruluk (model degerleri, %)", "Temiz ort (%)", "w (model degerleri, %)", "w ort (%)",
       "omega ort", "sigma ort", "rho ort", f"AA ilk {n6} (model degerleri, %)"], s1)
    L.append("Model duzeyi:\n")
    T(["Hucre", "Model", "Tohum", "Temiz (%)", "w (%)", "omega", "sigma", "rho", f"AA ilk {n6} (%)"], s2)
    L.append(f"w = exp(omega) denetimi: en buyuk mutlak fark {max(ex):.2e} puan. Temiz dogruluk `konsey_ayrisim_b4.json`'da "
             f"yoktur; B4'un girdi matrisinden (`{_M9_TM}` results.<kaynak>-><m>.target_clean_acc, butun kaynaklarda ayni oldugu "
             f"denetlendi) okunmustur. Bu dosyanin sha256'si {hes[:16]}..., B4 JSON'daki kayit (veri.girdi_sha256) "
             f"{'ile UYUSUYOR' if hes == kayitli else 'ile UYUSMUYOR (' + str(kayitli) + ')'}. "
             f"AA sutunundaki goruntu sayisi `{_M9_M6}` n alanindan: n = {n6}.\n")
    c1p = _oku(_M9_C1S)["pairs"]
    for h_, ms_ in b4["hucreler"].items():
        eks = [m for m in ms_ if m not in m6]
        if not eks:
            continue
        deg = []
        for m in eks:
            t_ = ht[m]["tohum"]
            p_ = [(p["vit"]["aa"] if p["vit_seed"] == t_ else p["resnet"]["aa"]) for p in c1p
                  if t_ in (p["vit_seed"], p["resnet_seed"])]
            deg.append(f"{m} {sg(p_[0], 2) if len(p_) == 1 else 'bulunamadi'}")
        L.append(f"{h_} hucresinin AA degeri B6 kapsami disindadir (ON_KAYIT Dondurma eki (i) m.7: B6'da AA yalniz yeni alti "
                 f"modelde kosar, V-scr ve C1-R32 icin maskeleme isareti tanimlanmamistir). Ayni modellerin C1 AA degerleri `{_M9_C1S}` pairs.<cift>.vit.aa alanindadir ve foyun "
                 f"'Tablo I: ana gurbuzluk' bolumundeki AA sutunu da bu dosyanin aggregate alanindan gelir: " + "; ".join(deg)
                 + f" (%). Bu degerler C1 AA degerlendirmesinin orneklemindendir (foy basligindaki tanim: tam test kumesi), "
                 f"B6 sutunu ise test kumesinin ilk {n6} goruntusundendir; iki orneklem karsilastirilamaz, hucre tablosunun AA "
                 f"sutununa ancak orneklemi etiketlenerek ya da dipnotla bos birakilarak girer.\n")


_m9("M9.2 2x2 hucre tablosu (temiz dogruluk, w, sigma, rho)",
    f"`{_M9_J4}` b4.hucreler; b4.F_B4.karsitliklar.H2.hucre_n, .H2.hucre_ort (sigma), .H3.hucre_ort (rho); "
    f"b4.ikincil.S3.etkilesim.hucre_ort (omega); b4.model_tablosu.<m>.yari_oran.omega (w), .yari_log.{{omega, sigma, rho}}; "
    f"veri.girdi_sha256; `{_M9_TM}` results.*-><m>.target_clean_acc; `{_M9_M6}` modeller.<m>.aa_dogruluk; "
    f"`{_M9_HT}` modeller.<m>.tohum; `{_M9_C1S}` pairs.<cift>.{{vit_seed, resnet_seed, vit.aa, resnet.aa}} (B6 disi hucre)", _m9_2)


# --- M9.3 B4 birincil aile F_B4 ------------------------------------------------------------
def _m9_3():
    J4 = _oku(_M9_J4)
    F = J4["b4"]["F_B4"]
    K, kr = F["karsitliklar"], F["karar"]
    adlar = ("H1", "H2", "H3")
    tanim = {"H1": "A^sigma_scr = sigma(V-scr) - sigma(R224-scr)",
             "H2": "I^sigma = [sigma(V-IN) - sigma(V-scr)] - [sigma(R224-IN) - sigma(R224-scr)]",
             "H3": "A^rho = 1/2 {[rho(V-scr) - rho(R224-scr)] + [rho(V-IN) - rho(R224-IN)]}"}
    satir = []
    for i_, h_ in enumerate(adlar):
        k_ = K[h_]
        ong = [f"{kk.split(h_ + '_ongoru_buyuklugu_tuttu')[1].strip()}: {_m9e(vv)}" for kk, vv in kr.items()
               if kk.startswith(h_ + "_ongoru_buyuklugu_tuttu")]
        satir.append([f"{h_}, {tanim[h_]}", sg(k_["kestirim"], 3, True), _m9a(k_["ci90"], 3, True), _m9a(k_["ci95"], 3, True),
                      f"{sg(k_['t'], 2, True)} ({k_['df']})", _m9p(F["p_ham"][i_]), _m9p(F["p_holm"][i_]), kr[h_],
                      "; ".join(ong) if ong else "(H3: esdegerlik; buyukluk satiri yok)"])
    T(["Sinama", "Kestirim", "%90 aralik", "%95 aralik", "t (df)", "Ham p", "Holm p", "Karar", "Ongorulen buyukluk"], satir)
    hk = holm(F["p_ham"])
    L.append(f"Ham p: H1 tek yonlu (p_tek_kucuk), H2 iki yonlu (p_iki), H3 TOST (iki tek yonlu p'nin buyugu, tost_p); "
             f"F_B4.not: '{F.get('not', 'bulunamadi')}'. Holm denetimi (bu betigin holm() fonksiyonuyla p_ham'dan): en buyuk "
             f"mutlak fark {float(np.max(np.abs(hk - np.asarray(F['p_holm'])))):.2e}.\n")
    L.append(f"TOST esdegerlik siniri delta = {kr['delta']} (meta.delta = {J4['meta']['delta']}; duyarlilik "
             f"meta.delta_duyarlilik = {J4['meta']['delta_duyarlilik']}); Holm alfa = {J4['meta']['alfa']}; "
             f"birlesik SD (sigma karsitliklari) {sg(K['H1']['sp_birlesik'], 4)}, (rho karsitligi) {sg(K['H3']['sp_birlesik'], 4)}.\n")
    L.append(f"H2 logit olcekli kestirim (karar kosulu): {sg(kr['H2_logit_kestirim'], 3, True)}; H2 ters yon Holm anlamli: "
             f"{_m9e(kr['H2_negatif_anlamli_holm'])}; H3 ham %90 aralik +-delta icinde: {_m9e(kr['H3_ham_ci90_delta_icinde'])}; "
             f"H1 esdeger: {_m9e(kr['H1_esdeger'])}; H2 esdeger: {_m9e(kr['H2_esdeger'])}; hesaplanamayip p = 1 sayilan sinama: "
             f"{', '.join(F['p_1_sayilan_hesaplanamayan']) or 'yok'}.\n")
    L.append(f"Sonuc bolgesi: **{kr['sonuc_bolgesi']}** (kural: {kr['sonuc_kurali']}); O4 nitelemesi: {_m9e(kr['O4_niteleme'])}; "
             f"B6 maskeleme kuralindan sonra uygulanan bolge: {F['maskeleme_kurali']['uygulanan_bolge']} (isaretli: "
             f"{', '.join(F['maskeleme_kurali']['isaretli']) or 'yok'}).\n")
    L.append(f"Gozlenen %90 yari genislikler (turetilmis, (ci90[1] - ci90[0]) / 2): "
             + "; ".join(f"{h_} {sg((K[h_]['ci90'][1] - K[h_]['ci90'][0]) / 2.0, 3)}" for h_ in adlar) + ".\n")


_m9("M9.3 B4 birincil aile F_B4 (H1, H2, H3; Holm)",
    f"`{_M9_J4}` b4.F_B4.karsitliklar.H{{1,2,3}}.{{kestirim, ci90, ci95, t, df, sp_birlesik}}; b4.F_B4.p_ham; b4.F_B4.p_holm; "
    f"b4.F_B4.karar.{{H1, H2, H3, *_ongoru_buyuklugu_tuttu, H2_logit_kestirim, H2_negatif_anlamli_holm, H3_ham_ci90_delta_icinde, "
    f"delta, sonuc_bolgesi, sonuc_kurali, O4_niteleme}}; b4.F_B4.maskeleme_kurali; b4.F_B4.p_1_sayilan_hesaplanamayan; "
    f"meta.{{delta, delta_duyarlilik, alfa}}", _m9_3)


# --- M9.4 B4 duyarliliklar ve ikincil ongoruler --------------------------------------------
def _m9_4():
    J4 = _oku(_M9_J4)
    b4 = J4["b4"]
    D = b4["duyarlilik"]
    adlar = ("H1", "H2", "H3")
    dk = f"delta_{J4['meta']['delta_duyarlilik']}"
    dd = D[dk]
    satir = [[f"delta = {dd['delta']} (Holm p; karar)"]
             + [f"{_m9p(dd['p_holm'][i_])}; {dd[h_]}" for i_, h_ in enumerate(adlar)] + [f"b4.duyarlilik.{dk}"]]
    for ad_, k_, nd in (("Tam orneklem, log (%90; %95)", "tam_log", 3), ("Logit olcek (%90; %95)", "yari_logit", 3),
                        ("Oran olcegi, puan (%90; %95)", "yari_oran", 2)):
        satir.append([ad_] + [f"{sg(D[k_][h_]['kestirim'], nd, True)} {_m9a(D[k_][h_]['ci90'], nd, True)}; "
                              f"{_m9a(D[k_][h_]['ci95'], nd, True)}" for h_ in adlar]
                     + [f"b4.duyarlilik.{k_}.H*.{{kestirim, ci90, ci95}}"])
    satir.append(["Welch, %95 (df)"] + [f"{_m9a(D['welch'][h_]['ci95'], 3, True)} ({sg(D['welch'][h_]['df'], 2)})" for h_ in adlar]
                 + ["b4.duyarlilik.welch.H*.{ci95, df}"])
    jk = D["panel_jackknife"]
    satir.append(["Panel jackknife (en kucuk ile en buyuk)"]
                 + [_m9oran({m: v[h_] for m, v in jk.items()}, 3) for h_ in adlar] + ["b4.duyarlilik.panel_jackknife.<uye>.H*"])
    hb = D["hiyerarsik_bootstrap"]
    satir.append([f"Hiyerarsik bootstrap (B = {hb['H1']['B']}), %90; %95"]
                 + [f"{_m9a(hb[h_]['ci90'], 3, True)}; {_m9a(hb[h_]['ci95'], 3, True)}" for h_ in adlar]
                 + ["b4.duyarlilik.hiyerarsik_bootstrap.H*.{ci90, ci95}"])
    L.append(f"Duyarliliklar (ON_KAYIT geregi karar degistirmez). delta duyarliliginda sonuc bolgesi: {dd['sonuc_bolgesi']}.\n")
    T(["Duyarlilik", "H1", "H2", "H3", "Anahtar"], satir)

    S = b4["ikincil"]
    s1, s3 = S["S1"], S["S3"]
    st = [
        ["S1, kopru sigma: sigma(R224-scr) - sigma(C1-R32) (kestirim 4 ondalik)", sg(s1["sigma"]["kestirim"], 4, True),
         _m9a(s1["sigma"]["ci90"], 3, True),
         f"df {s1['sigma']['df']}; Welch %90 {_m9a(s1['sigma']['welch']['ci90'], 3, True)} (Welch df "
         f"{sg(s1['sigma']['welch']['df'], 2)}); TOST p {_m9p(s1['sigma']['tost_p'])}",
         f"ikisi de esdeger: {_m9e(s1['ongoru_ikisi_de_esdeger'])}", "b4.ikincil.S1.sigma"],
        ["S1, kopru rho", sg(s1["rho"]["kestirim"], 3, True), _m9a(s1["rho"]["ci90"], 3, True),
         f"df {s1['rho']['df']}; Welch %90 {_m9a(s1['rho']['welch']['ci90'], 3, True)} (Welch df "
         f"{sg(s1['rho']['welch']['df'], 2)}); TOST p {_m9p(s1['rho']['tost_p'])}",
         f"ikisi de esdeger: {_m9e(s1['ongoru_ikisi_de_esdeger'])}", "b4.ikincil.S1.rho"],
        ["S2, rho(V-IN) - rho(V-scr)", sg(S["S2"]["kestirim"], 3, True), _m9a(S["S2"]["ci90"], 3, True),
         f"iki yonlu p {_m9p(S['S2']['p_iki'])}", f"negatif: {_m9e(S['S2']['ongoru_negatif'])}", "b4.ikincil.S2"],
        ["S3, omega baslatma etkisi ViT: omega(V-IN) - omega(V-scr)", sg(s3["V_baslatma"]["kestirim"], 3, True),
         _m9a(s3["V_baslatma"]["ci90"], 3, True), f"iki yonlu p {_m9p(s3['V_baslatma']['p_iki'])}",
         f"omega(V-IN) < omega(V-scr): {_m9e(s3['ongoru_omega_VIN_lt_Vscr'])}", "b4.ikincil.S3.V_baslatma"],
        ["S3, omega baslatma etkisi ResNet: omega(R224-IN) - omega(R224-scr)", sg(s3["R224_baslatma"]["kestirim"], 3, True),
         _m9a(s3["R224_baslatma"]["ci90"], 3, True), f"iki yonlu p {_m9p(s3['R224_baslatma']['p_iki'])}", "betimsel",
         "b4.ikincil.S3.R224_baslatma"],
        ["S3, omega etkilesimi", sg(s3["etkilesim"]["kestirim"], 3, True), _m9a(s3["etkilesim"]["ci90"], 3, True),
         f"iki yonlu p {_m9p(s3['etkilesim']['p_iki'])}", "betimsel", "b4.ikincil.S3.etkilesim"],
        ["S5, protokol katmani ornek disi sapma (puan)", sg(S["S5"]["ozet"]["ort"], 3, True), _m9a(S["S5"]["ozet"]["ci90"], 3, True),
         f"n = {S['S5']['ozet']['n']}; cift sapmalari {uc(S['S5']['ozet']['degerler'], 3, True)}; egim, kesisim "
         f"{', '.join(sg(float(x_), 3) for x_ in S['S5']['egim_kesisim'])}",
         f"ort sapma bant icinde: {_m9e(S['S5']['ozet']['ongoru_ort_sapma_bant_icinde'])}; curutme (%90 bant disinda): "
         f"{_m9e(S['S5']['ozet']['curutme_ci90_bant_disinda'])}", "b4.ikincil.S5.ozet; .egim_kesisim"],
        [f"S6, ikincil panel ({', '.join(S['S6']['panel'])}): A^sigma_scr; I^sigma",
         f"{sg(S['S6']['A_sigma_scr'], 3, True)}; {sg(S['S6']['I_sigma'], 3, True)}", "-", "-",
         f"isaret ayni A: {_m9e(S['S6']['isaret_ayni_A'])}; I: {_m9e(S['S6']['isaret_ayni_I'])}", "b4.ikincil.S6"]]
    s7 = S.get("S7")
    if s7:
        st.append([f"S7, Hodge (K = {s7['K']}): potansiyel payi", sg(s7["G_potansiyel_payi"], 3), "-",
                   f"rastgele beklenti {sg(s7['G_rastgele_beklenti_2_bolu_K'], 3)}; dolasim RMS {sg(s7['dolasim_rms'], 3)}; "
                   f"r RMS {sg(s7['r_rms'], 3)}", "betimsel", "b4.ikincil.S7"])
    L.append("Ikincil cozumlemeler (kesifsel, coklu duzeltme yok):\n")
    T(["Cozumleme", "Kestirim", "%90 aralik", "Ek bilgi", "Ongoru", "Anahtar"], st)
    s4 = []
    for c_ in S["S4"]:
        t_ = c_["tam"]
        s4.append([" / ".join(c_["cift"]), sg(t_["asimetri_puan"], 2, True), sg(t_["log_oran"], 3, True),
                   sg(t_["log_w_potansiyel"], 3, True), sg(t_["r"], 3, True), sg(t_["log_tau"], 3, True),
                   sg(t_["potansiyel_payi"], 3), sg(c_["potansiyel_payi_yari"], 3)])
    L.append("S4, tohum indeksiyle eslesmis ciftler (betimsel; tam orneklem; potansiyel payi = log_w_potansiyel / log_oran, "
             "log_oran sifira yakinken kararsizdir):\n")
    T(["Cift (ResNet / ViT)", "Hedef-dogru asimetri (puan)", "log oran", "Potansiyel (w) bileseni", "Yonlu artik r", "log tau",
       "Potansiyel payi", "Potansiyel payi (bolunmus yari)"], s4)


_m9("M9.4 B4 duyarliliklar ve ikincil ongoruler (S1-S7)",
    f"`{_M9_J4}` b4.duyarlilik.{{delta_<meta.delta_duyarlilik>, tam_log, yari_logit, yari_oran, welch, panel_jackknife, "
    f"hiyerarsik_bootstrap}}; b4.ikincil.{{S1 (kestirim, ci90, df, welch.ci90, welch.df, tost_p), S2, S3, S4, S5, S6, S7}}", _m9_4)


# --- M9.5 B2 aile F_B2 ---------------------------------------------------------------------
def _m9_5():
    J2 = _oku(_M9_J2)
    b2 = J2["b2"]
    F = b2["F_B2"]
    ka, kb, kc, kr = F["K-a"], F["K-b"], F["K-c"], F["karar"]

    def ong(ad):
        return "; ".join(f"{kk.split(ad + '_ongoru_buyuklugu_tuttu')[1].strip()}: {_m9e(vv)}" for kk, vv in kr.items()
                         if kk.startswith(ad + "_ongoru_buyuklugu_tuttu")) or "-"

    satir = [
        ["K-a, simetrik oran q_s = [sigma(R_s) - sigma(V_s)] / D_s", f"ort q {sg(ka['sinama']['ort'], 3)} (q_s: {uc(ka['q'], 3)})",
         _m9a(ka["sinama"]["ci90"]), _m9a(ka["sinama"]["ci95"]), _m9p(F["p_ham"][0]), _m9p(F["p_holm"][0]), kr["K-a"], ong("K-a")],
        ["K-b, ViT yonlu terimi rho(V-scr)", f"ort rho {sg(kb['ort'], 3, True)} (tohumlar: {uc(kb['degerler'], 3, True)})",
         _m9a(kb["ci90"], 3, True), _m9a(kb["ci95"], 3, True), f"TOST {_m9p(F['p_ham'][1])}", _m9p(F["p_holm"][1]), kr["K-b"],
         f"ham %90 aralik +-delta icinde: {_m9e(kr['K-b_ham_ci90_delta_icinde'])}"],
        ["K-c, tur ici benzerlik Delta_w", f"Delta_w {sg(kc['Delta_w'], 3, True)}", f"bootstrap {_m9a(kc['bootstrap']['ci90'], 3, True)}",
         f"bootstrap {_m9a(kc['bootstrap']['ci95'], 3, True)}", _m9p(F["p_ham"][2]), _m9p(F["p_holm"][2]), kr["K-c"], ong("K-c")]]
    T(["Sinama", "Gozlenen", "%90 aralik", "%95 aralik", "Ham p", "Holm p", "Karar", "Ongorulen buyukluk"], satir)
    hk = holm(F["p_ham"])
    L.append(f"F_B2.not: '{F.get('not', 'bulunamadi')}'. TOST siniri delta = {J2['meta']['delta']}; Holm alfa = {J2['meta']['alfa']}. "
             f"Holm denetimi (holm() ile p_ham'dan): en buyuk mutlak fark {float(np.max(np.abs(hk - np.asarray(F['p_holm'])))):.2e}. "
             f"Hesaplanamayip p = 1 sayilan: {', '.join(F['p_1_sayilan_hesaplanamayan']) or 'yok'}.\n")
    L.append(f"K-a ayrintisi: D_s {uc(ka['D'], 3)}; simetrik pay {uc(ka['simetrik_pay'], 3)}; yonlu pay {uc(ka['yonlu_pay'], 3)}; "
             f"payda kurali tetiklenen tohum: {', '.join(str(x_) for x_ in ka['payda_kucuk_tohumlar']) or 'yok'}; "
             f"ozdeslik artigi en buyuk {ka['ozdeslik_artik_max']:.1e}; ciftler: "
             + "; ".join(" / ".join(c_) for c_ in ka["ciftler"]) + ".\n")
    tr = b2.get("tur_ici_resnet_log_tau", {})
    L.append(f"K-c ayrintisi: ViT tur ici log tau {uc(list(kc['log_tau_tur_ici'].values()), 3, True)} (ort "
             f"{sg(float(np.mean(list(kc['log_tau_tur_ici'].values()))), 3, True)}); sigma_V {uc(list(kc['sigma_V'].values()), 3, True)}; "
             f"bootstrap B = {kc['bootstrap']['B']}, yeniden cekilen tek tohumlu ornek {kc['bootstrap']['yeniden_cekilen_tek_tohumlu_ornek']}; "
             f"ResNet tur ici log tau {uc(list(tr.values()), 3, True) if tr else 'bulunamadi'}"
             f"{(' (ort ' + sg(float(np.mean(list(tr.values()))), 3, True) + ')') if tr else ''}.\n")
    D = b2["duyarlilik"]
    dk = f"duyarlilik_delta_{J2['meta']['delta_duyarlilik']}"
    dd = F[dk]
    jk = D["panel_jackknife"]
    ds = [
        [f"delta = {dd['delta']}", f"Holm p {', '.join(_m9p(x_) for x_ in dd['p_holm'])}",
         f"K-a {dd['karar']['K-a']}; K-b {dd['karar']['K-b']}; K-c {dd['karar']['K-c']}", f"b2.F_B2.{dk}"],
        ["Tam orneklem, log", f"ort q {sg(D['tam_log']['q_ort'], 3)}",
         f"ort rho(V-scr) {sg(D['tam_log']['rho_V']['ort'], 3, True)}, %90 {_m9a(D['tam_log']['rho_V']['ci90'], 3, True)}",
         "b2.duyarlilik.tam_log"],
        ["Yari logit", f"ort q {sg(D['yari_logit']['q_ort'], 3)} (q_s: {uc(D['yari_logit']['q'], 3)})",
         f"ort rho(V-scr) {sg(D['yari_logit']['rho_V']['ort'], 3, True)}, %90 {_m9a(D['yari_logit']['rho_V']['ci90'], 3, True)}, "
         f"%95 {_m9a(D['yari_logit']['rho_V']['ci95'], 3, True)}", "b2.duyarlilik.yari_logit"],
        ["Yari oran (rho puan)", f"ort q {sg(D['yari_oran']['q_ort'], 3)}",
         f"ort rho(V-scr) {sg(D['yari_oran']['rho_V']['ort'], 2, True)} puan, %90 {_m9a(D['yari_oran']['rho_V']['ci90'], 2, True)}",
         "b2.duyarlilik.yari_oran"],
        ["Panel jackknife", "ort q " + _m9oran({m: v["q_ort"] for m, v in jk.items()}, 3, False),
         "ort rho(V-scr) " + _m9oran({m: v["rho_V_ort"] for m, v in jk.items()}, 3), "b2.duyarlilik.panel_jackknife"],
        [f"Ikincil panel ({', '.join(D['ikincil_panel']['panel'])})", f"q_s {uc(D['ikincil_panel']['q'], 3)}",
         f"rho(V-scr) {uc(D['ikincil_panel']['rho_V'], 3, True)}", "b2.duyarlilik.ikincil_panel"]]
    hb = _m9g(D, ["hiyerarsik_bootstrap"], "B2 K-a ve K-b hiyerarsik bootstrap duyarliligi (b2.duyarlilik.hiyerarsik_bootstrap)")
    ds.append(["K-a ve K-b hiyerarsik bootstrap", "bulunamadi" if hb is None else str(hb),
               "JSON'da anahtar yok; dondurulmus betik B2'de hiyerarsik bootstrap'i yalniz K-c birincil araligi olarak uretir"
               if hb is None else "-", "b2.duyarlilik.hiyerarsik_bootstrap"])
    L.append("Duyarliliklar (karar degistirmez):\n")
    T(["Duyarlilik", "q", "rho(V-scr) ve diger", "Anahtar"], ds)


_m9("M9.5 B2 aile F_B2 (K-a, K-b, K-c; Holm)",
    f"`{_M9_J2}` b2.F_B2.K-a.{{q, sinama.ort, sinama.ci90, sinama.ci95, D, simetrik_pay, yonlu_pay, ozdeslik_artik_max, "
    f"payda_kucuk_tohumlar}}; b2.F_B2.K-b.{{degerler, ort, ci90, ci95, tost_p}}; b2.F_B2.K-c.{{Delta_w, bootstrap, log_tau_tur_ici, "
    f"sigma_V}}; b2.F_B2.{{p_ham, p_holm, karar, not, duyarlilik_delta_<meta.delta_duyarlilik>}}; b2.duyarlilik.{{tam_log, "
    f"yari_logit, yari_oran, panel_jackknife, ikincil_panel}}; b2.tur_ici_resnet_log_tau; meta.{{delta, alfa}}", _m9_5)


# --- M9.6 B5 saldiri tarafi ----------------------------------------------------------------
def _m9_6():
    J5 = _oku(_M9_J5)
    b5 = J5["b5"]
    ht = _oku(_M9_HT)["modeller"]
    with open(os.path.join(ROOT, _M9_BETIK), encoding="utf-8") as fh:
        src = fh.read()
    m_es = _m8re.search(r"^B5_ESIK\s*=\s*([0-9.]+)", src, _m8re.M)
    m_de = _m8re.search(r"^DELTA\s*=\s*([0-9.]+)", src, _m8re.M)
    b5esik = float(m_es.group(1))
    gp_kural = "if not (Gp > DELTA)" in src
    esik = J5["meta"]["delta"]
    if not gp_kural or abs(float(m_de.group(1)) - esik) > 1e-12:
        raise ValueError("G_PGD esigi dondurulmus betikle JSON meta.delta arasinda dogrulanamadi")
    B = b5["birincil_C1-R32_V-scr"]
    bs = B["bootstrap"]
    L.append(f"Tanim (b5.tanim): {b5['tanim']}\n")
    L.append(f"Esikler: korunma orani esigi B5_ESIK = {b5esik} (`{_M9_BETIK}` satir {src[:m_es.start()].count(chr(10)) + 1}); "
             f"G_PGD hesaplanabilirlik esigi = {esik} (J5 meta.delta; betikte `if not (Gp > DELTA)` kosulu, DELTA = "
             f"{m_de.group(1)}, satir {src[:m_de.start()].count(chr(10)) + 1}). Izinli saldirilar: CNN {', '.join(b5['izinli']['CNN'])}; "
             f"ViT {', '.join(b5['izinli']['ViT'])}.\n")
    T(["Nicelik", "Deger", "Anahtar"], [
        ["G_PGD (log birimi; 4 ondalik)", sg(B["G_PGD"], 4), "b5.birincil_C1-R32_V-scr.G_PGD"],
        ["G_PGD bootstrap %90", _m9a(bs["G_PGD_ci90"], 3), ".bootstrap.G_PGD_ci90"],
        ["G_best (capraz uydurmali secim; 4 ondalik)", sg(B["G_best"], 4), ".G_best"],
        ["Secimin kapattigi acik G_PGD - G_best (turetilmis; 4 ondalik)", sg(B["G_PGD"] - B["G_best"], 4), ".G_PGD - .G_best"],
        ["Korunma orani G_best / G_PGD", sg(B["oran"], 3), ".oran"],
        ["Korunma orani %90", _m9a(bs["ci90"], 3), ".bootstrap.ci90"],
        ["Korunma orani %95", _m9a(bs["ci95"], 3), ".bootstrap.ci95"],
        ["Gecerli bootstrap kopyasi / B", f"{bs['gecerli']} / {bs['B']}", ".bootstrap.gecerli, .B"],
        ["Karar", B["karar"], ".karar"],
        ["Tam orneklem secim duyarliligi: oran", sg(B["duyarlilik_tam_orneklem_secim"]["oran"], 3),
         ".duyarlilik_tam_orneklem_secim.oran"]])
    bloklar = [("birincil_C1-R32_V-scr", B)] + list(b5["betimsel"].items())
    satir, gor, vit_fark, n_vit, n_tgr = [], set(), {}, 0, 0
    for bad, blk in bloklar:
        for m, k_ in blk["kaynaklar"].items():
            if m in gor:
                continue
            gor.add(m)
            St = k_["S_tam"]
            if "tgr" in St:
                n_vit += 1
                vit_fark.setdefault(ht[m]["hucre"], {})[m] = St["tgr"] - St["pgd"]
            if "tgr" in k_["secilen_cift_tek"] or k_["secilen_tam_orneklem"] == "tgr":
                n_tgr += 1
            satir.append([m, ht[m]["hucre"], " / ".join(k_["secilen_cift_tek"]), k_["secilen_tam_orneklem"],
                          sg(St["pgd"], 3), sg(St["mi"], 3), sg(St["tgr"], 3) if "tgr" in St else "-",
                          sg(St["mi"] - St["pgd"], 3, True), sg(St["tgr"] - St["pgd"], 3, True) if "tgr" in St else "-"])
    L.append("Kaynak bazinda secilen saldiri ve panel ortalamasi S_k (tam orneklem, log; farklar turetilmis):\n")
    T(["Kaynak", "Hucre", "Secilen (cift / tek yari)", "Secilen (tam orneklem)", "S_PGD", "S_MI", "S_TGR", "S_MI - S_PGD",
       "S_TGR - S_PGD"], satir)
    L.append(f"TGR'nin en iyi saldiri secildigi kaynak sayisi: {n_tgr} / {n_vit} ViT kaynagi (TGR yalniz ViT kaynaklarinda izinli). "
             + "; ".join(f"{h_} kaynaklarinda S_TGR - S_PGD araligi {mm(list(v_.values()), 3, True)} ({len(v_)} kaynak)"
                         for h_, v_ in vit_fark.items()) + ".\n")
    bt = []
    for bad, blk in b5["betimsel"].items():
        if blk["G_PGD"] > esik:
            bt.append([bad, sg(blk["G_PGD"], 3), sg(blk["G_best"], 3), sg(blk["oran"], 3),
                       sg(blk["duyarlilik_tam_orneklem_secim"]["oran"], 3), "betimsel"])
        else:
            bt.append([bad, sg(blk["G_PGD"], 3), "-", "-", "-",
                       f"G_PGD <= J5 meta.delta ({esik}); on kayitli B5 hesaplanabilirlik kurali (`if not (Gp > DELTA)`) "
                       f"birincil sinama icin tanimlidir, betimsel cifte uygulanmasi `{_M9_SR}` §7 m.4 kararidir; "
                       f"JSON'daki G_best ve oran bu karar geregi foye alinmaz, oran yorumlanmaz"])
    L.append("Betimsel hucre ciftleri (on kayit geregi karar yok):\n")
    T(["Cift (ResNet hucresi _ ViT hucresi)", "G_PGD", "G_best", "Korunma orani", "Tam orneklem secim orani", "Not"], bt)
    L.append(f"b5.not: '{b5.get('not', 'bulunamadi')}'.\n")


_m9("M9.6 B5 saldiri tarafi (korunma orani)",
    f"`{_M9_J5}` b5.tanim; b5.izinli; b5.birincil_C1-R32_V-scr.{{G_PGD, G_best, oran, bootstrap.{{ci90, ci95, G_PGD_ci90, gecerli, B}}, "
    f"karar, duyarlilik_tam_orneklem_secim.oran, kaynaklar.<m>.{{S_tam, secilen_cift_tek, secilen_tam_orneklem}}}}; "
    f"b5.betimsel.<cift>.{{G_PGD, G_best, oran, kaynaklar}}; meta.delta; `{_M9_BETIK}` B5_ESIK, DELTA (kaynak metninden); "
    f"`{_M9_HT}` modeller.<m>.hucre", _m9_6)


# --- M9.7 B6 maskeleme ---------------------------------------------------------------------
def _m9_7():
    m6 = _oku(_M9_M6)
    J4 = _oku(_M9_J4)
    with open(os.path.join(ROOT, _M9_AA), encoding="utf-8", newline="") as fh:
        aa = {r_["model"]: r_ for r_ in _m9csv.DictReader(fh)}
    satir, uy = [], 0
    for m, v in m6["modeller"].items():
        a_ = aa.get(m)
        if a_ and abs(float(a_["robust_accuracy"]) - v["aa_dogruluk"]) < 1e-9 and \
                abs(float(a_["clean_accuracy"]) - v["temiz_dogruluk_aa"]) < 1e-9:
            uy += 1
        satir.append([m, sg(v["temiz_dogruluk_aa"], 2), sg(v["temiz_dogruluk_matris"], 2), sg(v["pgd10_dogruluk"], 2),
                      sg(v["aa_dogruluk"], 2), sg(v["fark_puan"], 2), _m9e(v["isaretli"]), v["temiz_maske_uyusmazligi"],
                      v["aa_robust_pgd_yanilmis"]])
    T(["Model", "Temiz (AA dosyasi)", "Temiz (B4 matrisi)", "PGD-10", "AutoAttack", "Fark (puan)", "Isaretli",
       "Temiz maske uyusmazligi", "AA dogru, PGD-10 yanlis"], satir)
    fk = {m: v["fark_puan"] for m, v in m6["modeller"].items()}
    en = max(fk, key=fk.get)
    mk = J4["b4"]["F_B4"]["maskeleme_kurali"]
    L.append(f"Kural: test kumesinin ilk n = {m6['n']} goruntusunde PGD-10 ile AutoAttack farki esik_puan = {m6['esik_puan']} "
             f"puani asan model isaretlenir (PGD kaynagi: {m6['pgd_kaynagi']}; AA kaynagi: {m6['aa_kaynagi']}). Isaretli model: "
             f"{', '.join(m6['isaretli']) or 'yok'}; maskeleme_isaretli_arg: '{m6['maskeleme_isaretli_arg']}'; hatalar: "
             f"{', '.join(m6['hatalar']) or 'yok'}. En buyuk fark {en} ({sg(fk[en], 2)} puan; esige uzaklik "
             f"{sg(m6['esik_puan'] - fk[en], 2)} puan). Fark araligi {mm(list(fk.values()), 2)} puan.\n")
    L.append(f"`{_M9_AA}` ile capraz denetim (clean_accuracy, robust_accuracy): {uy} / {len(m6['modeller'])} modelde uyusuyor. "
             f"B4 maskeleme kurali: uygulanan bolge {mk['uygulanan_bolge']}; not: '{mk.get('not', '')}'.\n")


_m9("M9.7 B6 AutoAttack ve maskeleme kurali",
    f"`{_M9_M6}` n, esik_puan, pgd_kaynagi, aa_kaynagi, isaretli, maskeleme_isaretli_arg, hatalar, modeller.<m>.{{temiz_dogruluk_aa, "
    f"temiz_dogruluk_matris, pgd10_dogruluk, aa_dogruluk, fark_puan, isaretli, temiz_maske_uyusmazligi, aa_robust_pgd_yanilmis}}; "
    f"`{_M9_AA}` model, clean_accuracy, robust_accuracy; `{_M9_J4}` b4.F_B4.maskeleme_kurali", _m9_7)


# --- M9.8 Butunluk -------------------------------------------------------------------------
def _m9cak(veri):
    """veri.cakismalar (J2, J4) ya da veri.<saldiri>.cakismalar (J5)."""
    if "cakismalar" in veri:
        return "VAR" if veri["cakismalar"] else "yok"
    alt = {k_: v_["cakismalar"] for k_, v_ in veri.items() if isinstance(v_, dict) and "cakismalar" in v_}
    if not alt:
        return "bulunamadi"
    return ", ".join(f"{k_} {'VAR' if v_ else 'yok'}" for k_, v_ in alt.items())


def _m9_8():
    J = {ad: _oku(rel) for ad, rel in (("J2", _M9_J2), ("J4", _M9_J4), ("J5", _M9_J5))}
    with open(os.path.join(ROOT, _M9_OK), encoding="utf-8") as fh:
        ok = fh.read()
    eki = ok[ok.index("\n## Dondurma eki\n"):]
    kay_a = dict((p_, h_) for h_, p_ in _m8re.findall(r"^([0-9a-f]{64})\s+(\S+)$", eki, _m8re.M))
    m_b = _m8re.search(r"^\(b\)[^\n]*?`([0-9a-f]{64})`", eki, _m8re.M)
    satir = []
    for rel, alan in ((_M9_BETIK, "betik_sha256"), (_M9_HT, "hucre_tablosu_sha256")):
        js = {ad: d["meta"][alan] for ad, d in J.items()}
        hs = _m9sha(rel)
        tek = len(set(js.values())) == 1
        satir.append([f"`{rel}`", f"{list(js.values())[0]} (J2, J4, J5 meta.{alan}; uc JSON {'ayni' if tek else 'FARKLI'})",
                      kay_a.get(rel, "bulunamadi"), hs,
                      "UYUSUYOR" if tek and hs == list(js.values())[0] == kay_a.get(rel) else "UYUSMUYOR"])
    hg = _m9sha(_M9_OK, govde=True)
    kb = m_b.group(1) if m_b else None
    if kb is None:
        _M9_YOK.append("ON_KAYIT Dondurma eki (b) govde sha256 kaydi")
    satir.append([f"`{_M9_OK}` govdesi (ilk satirdan '## Dondurma eki' basligina kadar)",
                  "JSON'da kayitli degil; dosyadan hesaplandi", kb or "bulunamadi", hg, "UYUSUYOR" if hg == kb else "UYUSMUYOR"])
    T(["Dosya", "JSON kaydi", "On kayit Dondurma eki kaydi", "Dosyadan hesaplanan (bu betik)", "Durum"], satir)
    L.append("JSON uretim zamanlari: " + "; ".join(f"{ad} {d['meta']['uretildi_utc']}" for ad, d in J.items())
             + f". numpy (JSON meta): {', '.join(sorted({d['meta']['numpy'] for d in J.values()}))}. Birincil panel eksik uyesi: "
             + "; ".join(f"{ad} {', '.join(d['panel']['birincil_eksik']) or 'yok'}" for ad, d in J.items())
             + ". Matris cakismasi: " + "; ".join(f"{ad} {_m9cak(d['veri'])}" for ad, d in J.items()) + ".\n")
    # Eksikler satiri M9.9 (masa) da kosulduktan sonra doldurulur; yeri burada ayrilir.
    _M9_YOK_YER.append(len(L))
    L.append("")


_m9("M9.8 Butunluk (dondurulmus betik, hucre tablosu, on kayit govdesi)",
    f"`{_M9_J2}`, `{_M9_J4}`, `{_M9_J5}` meta.{{betik_sha256, hucre_tablosu_sha256, uretildi_utc, numpy}}, panel.birincil_eksik, "
    f"veri.cakismalar; `{_M9_OK}` Dondurma eki (a) ve (b) (sha256 kayitlari, metinden); dosya sha256'lari bu betikte hashlib ile "
    f"hesaplanir (`{_M9_BETIK}`, `{_M9_HT}`, `{_M9_OK}` govdesi)", _m9_8)


# --- M9.9 Masa cozumlemeleri (SENTEZ ve konsey_masa) ----------------------------------------
def _m9_9():
    SN = _oku(_M9_SN)
    MC = _oku(_M9_MC)
    PY = _oku(_M9_P3Y)
    PP = _oku(_M9_P3P)
    J4 = _oku(_M9_J4)
    L.append(f"On kayit oncesi masa cozumlemeleridir; yeni olcum yoktur ve sinama degildir (SENTEZ tanim: '{SN['tanim']}'; "
             f"`{_M9_MC}` not: '{MC['not']}'). Betimsel olarak okunur.\n")

    # (a) C1 cifti log asimetri ayrisimi
    nic = (("asimetri_puan", "Hedef-dogru asimetri (puan)", 2, True), ("log_oran", "log oran", 3, True),
           ("log_w_potansiyel", "Potansiyel (w) bileseni", 3, True), ("r", "Yonlu artik r", 3, True),
           ("log_tau", "log tau", 3, True), ("potansiyel_payi", "Potansiyel payi", 3, False))
    sat, gb = [], []
    for kn, kv in SN["kumeler"].items():
        for an, et, nd, pl in nic:
            x = _m9g(kv, ["tam_orneklem", an], f"SENTEZ kumeler.{kn}.tam_orneklem.{an}")
            if x is None:
                sat.append([kn, et, "bulunamadi", "bulunamadi", "bulunamadi"])
                continue
            sat.append([kn, et, sg(x["ort"], nd, pl), sg(x["sd_kosum"], nd), uc(x["degerler"], nd, pl)])
        g_ = kv.get("goruntu_bootstrap_pair1")
        if g_:
            gb.append(f"{kn} r SD {sg(g_['r_sd'], 3)}, log tau SD {sg(g_['log_tau_sd'], 3)} (B = {g_['B']})")
    L.append("C1 ResNet-18 / ViT-Tiny ciftinin log asimetri ayrisimi (uc tohum cifti; ort ve kosum SD'si JSON'dan; "
             "potansiyel payi = log_w_potansiyel / log_oran):\n")
    T(["Kume", "Nicelik", "Ort", "SD (kosum)", "Cift degerleri"], sat)
    L.append("Goruntu bootstrap SD'si, cift 1 (goruntu_bootstrap_pair1): " + ("; ".join(gb) if gb else "bulunamadi") + ".\n")

    # (b) Havuz: ViT'nin panel kaynak acigi ve hedef farki
    H = SN["havuz_tohum1"]
    ka, hf = H["kaynak_acigi_ayristirma_log"], H["hedef_farki_ayristirma_log"]
    on = "havuz_tohum1.kaynak_acigi_ayristirma_log"
    hn = "havuz_tohum1.hedef_farki_ayristirma_log"
    T(["Nicelik (tam orneklem, log)", "Deger", "Anahtar"], [
        ["Kaynak acigi toplam", sg(ka["toplam"], 3, True), f"{on}.toplam"],
        ["Kaynak acigi simetrik pay", sg(ka["simetrik_pay"], 3, True), f"{on}.simetrik_pay"],
        ["Kaynak acigi yonlu pay", sg(ka["yonlu_pay"], 3, True), f"{on}.yonlu_pay"],
        ["Kaynak acigi simetrik oran", sg(ka["simetrik_oran"], 3), f"{on}.simetrik_oran"],
        ["Kaynak acigi kontrol artigi", f"{ka['kontrol_artik']:.1e}", f"{on}.kontrol_artik"],
        ["Hedef farki toplam", sg(hf["toplam"], 3, True), f"{hn}.toplam"],
        ["Hedef farki potansiyel pay", sg(hf["potansiyel_pay"], 3, True), f"{hn}.potansiyel_pay"],
        ["Hedef farki simetrik pay", sg(hf["simetrik_pay"], 3, True), f"{hn}.simetrik_pay"],
        ["Hedef farki yonlu pay", sg(hf["yonlu_pay"], 3, True), f"{hn}.yonlu_pay"],
        ["Hedef farki kontrol artigi", f"{hf['kontrol_artik']:.1e}", f"{hn}.kontrol_artik"]])
    L.append(f"Tanimlar (SENTEZ): kaynak acigi '{ka['tanim']}'; hedef farki '{hf['tanim']}'. Panel: "
             f"{', '.join(H['ViT_Tiny_AT']['panel'])} (havuz_tohum1.ViT_Tiny_AT.panel).\n")
    vt = MC["1_havuz_model_tablosu"]
    jka = vt.get("jackknife_aralik", {})
    ks = []
    for m, v in vt["modeller"].items():
        if "kaynak_acigi_R_eksi_m_yari_log" not in v:
            continue
        parca = [f"{ol} {sg(v['kaynak_acigi_R_eksi_m_' + ol]['simetrik_oran'], 3)}"
                 for ol in ("yari_log", "tam_log", "yari_logit") if "kaynak_acigi_R_eksi_m_" + ol in v]
        j_ = jka.get(m, {}).get("simetrik_oran")
        ks.append(f"{m}: " + ", ".join(parca) + (f"; panel uyesi birakmali jackknife araligi (yari_log) {_m9a(j_, 3)}"
                                                    if j_ else ""))
    L.append(f"Ayni ayrisimin `{_M9_MC}` karsiligi, ResNet-18 AT (R) ile her model (m) arasindaki panel kaynak aciginin "
             f"simetrik orani (1_havuz_model_tablosu.modeller.<m>.kaynak_acigi_R_eksi_m_<olcek>.simetrik_oran; "
             f"jackknife_aralik.<m>.simetrik_oran; panel uyeleri icin panel kendisi haric): "
             + ("; ".join(ks) if ks else "bulunamadi") + ".\n")

    # (c) tab:external_pool icin sigma ve rho
    with open(os.path.join(ROOT, MC["betik"]), encoding="utf-8") as fh:
        mc_src = fh.read()
    hv = PP["havuz_cifar10"]
    ayni_veri = hv["klasor"] in mc_src
    MT4 = J4["b4"]["model_tablosu"]
    sat = []
    for m, v in vt["modeller"].items():
        b_ = MT4.get(m)
        sat.append([m, sg(v["yari_log"]["sigma"], 3, True), sg(v["yari_log"]["rho"], 3, True), v["yari_log"]["panel_n"],
                    sg(v["tam_log"]["sigma"], 3, True), sg(v["tam_log"]["rho"], 3, True),
                    sg(b_["yari_log"]["sigma"], 3, True) if b_ else "B4'te yok",
                    sg(b_["yari_log"]["rho"], 3, True) if b_ else "B4'te yok", b_["yari_log"]["panel_n"] if b_ else "-"])
    L.append(f"Havuz modellerinde sigma ve rho (`tab:external_pool` icin). 'Masa' sutunlari `{_M9_MC}` "
             f"1_havuz_model_tablosu.modeller.<m>.{{yari_log, tam_log}} alanindan, panel {len(vt['panel'])} CNN: "
             f"{', '.join(vt['panel'])} (1_havuz_model_tablosu.panel). 'B4' sutunlari `{_M9_J4}` b4.model_tablosu.<m>.yari_log "
             f"alanindan, panel {len(J4['panel']['birincil'])} uyeli birincil panel: {', '.join(J4['panel']['birincil'])} "
             f"(panel.birincil). panel_n, panel uyesinin kendisi haric hesaba giren panel modeli sayisidir.\n")
    T(["Model", "Masa sigma (yari, log)", "Masa rho (yari, log)", "Masa panel_n", "Masa sigma (tam, log)", "Masa rho (tam, log)",
       "B4 sigma (yari, log)", "B4 rho (yari, log)", "B4 panel_n"], sat)
    es = []
    for sm, sv in H.items():
        if not (isinstance(sv, dict) and "log_tau_ort" in sv and "r_ort" in sv):
            continue
        b_ = [m for m, v in vt["modeller"].items() if abs(v["tam_log"]["sigma"] - sv["log_tau_ort"]) < 1e-9
              and abs(v["tam_log"]["rho"] - sv["r_ort"]) < 1e-9]
        es.append(f"{sm} = {b_[0]}" if len(b_) == 1 else f"{sm} ESLESMEDI")
    L.append(f"Kaynak secimi: `tab:external_pool` sekiz modellik havuz verisinden kuruludur (`{_M9_P3P}` havuz_cifar10.klasor = "
             f"`{hv['klasor']}`, {len(hv['modeller'])} model: {', '.join(hv['modeller'])}). Masa sutunlari bu veriden hesaplanir "
             f"(`{MC['betik']}` kaynak metninde `{hv['klasor']}`: {'VAR' if ayni_veri else 'YOK'}); B4 sutunlari ayni modellerin "
             f"B4 matrisindeki (`{_M9_TM}`) ve farkli paneldeki degeridir. Bu foyde `tab:external_pool` icin secilen kaynak masa "
             f"sutunlaridir (ayni veri, {len(vt['panel'])} CNN'lik panel); B4 sutunlari yalniz karsilastirma icindir. Masa model tablosu {len(vt['modeller'])} model kapsar; havuzun kalan "
             f"{len(hv['modeller']) - len(vt['modeller'])} uyesi icin bu dosyada sigma ve rho yoktur. SENTEZ havuz_tohum1 "
             f"log_tau_ort ve r_ort degerleri masa tam_log sigma ve rho ile 1e-9 icinde ayni: " + ("; ".join(es) if es else
                                                                                                    "bulunamadi") + ".\n")

    # (d) Yorunge sonucu (carpimsal yasa, A kolu) ve havuz karsiligi
    A = PY["A_kolu"]
    sat = [["Yorunge noktalari (A_kolu), birlesik", A["n"], sg(A["R2_lambda_1"], 3), sg(A["lambda_kesisimsiz"], 3),
            f"{sg(A['egim_kesisimli'], 3)}, {sg(A['kesisim'], 3, True)}", sg(A["pearson_r"], 3), A["isaret"]]]
    for vn, vv in A.get("veri_ayrimi", {}).items():
        sat.append([f"A_kolu.veri_ayrimi.{vn}", vv["n"], "-", "-", f"{sg(vv['egim'], 3)}, {sg(vv['kesisim'], 3, True)}",
                    sg(vv["pearson_r"], 3), vv["isaret"]])
    h7 = PY["havuz_AT7"]
    sat.append([f"havuz_AT7 ({len(h7['modeller'])} AT modeli; R2 lambda uydurmali: {sg(h7['R2_lambda_uydurma'], 3)})", "-",
                sg(h7["R2_lambda_1_sabit"], 3), sg(h7["lambda"], 3), "-", "-", h7["isaret"]])
    L.append("Carpimsal yasa masasi (log oran ile log w orani; lambda = 1 sabit R2, kesisimsiz lambda, kesisimli egim ve kesisim):\n")
    T(["Kume", "n", "R2 (lambda = 1)", "Kesisimsiz lambda", "Kesisimli egim, kesisim", "Pearson r", "Isaret uyumu"], sat)

    # (e) Onerme 3, h olcegi ayar testi (havuz)
    at = hv["ayar_testi"]
    L.append(f"Onerme 3 ayar testi, havuz (`{_M9_P3P}` havuz_cifar10.ayar_testi; n = {hv['n']}, B = {hv['B']}): en buyuk |g| "
             f"{sg(at['g_mutlak_en_buyuk'], 4)}, ortalama |g| {sg(at['g_mutlak_ortalama'], 4)} (4 ondalik), en kucuk p "
             f"{sg(at['p_en_kucuk'], 3)}.\n")
    alan = (("kaynak_alfa_raw_eksi_tc_bolu_tc_alfa_SD", "Ham - tc kaynak etkisi / tc kaynak SD"),
            ("kaynak_alfa_raw_eksi_tc_en_buyuk_mutlak", "Ham - tc kaynak etkisi, en buyuk mutlak (olcek birimi)"),
            ("hedef_beta_raw_eksi_tc_ile_tau_korelasyonu", "Ham - tc hedef etkisi ile tau korelasyonu"),
            ("dolasim_raw_eksi_tc_rms_bolu_dolasim_tc_rms", "Ham - tc dolasim RMS / tc dolasim RMS"),
            ("kaynak_alfa_bc_eksi_tc_bolu_tc_alfa_SD", "bc - tc kaynak etkisi / tc kaynak SD"),
            ("dolasim_bc_eksi_tc_rms_bolu_dolasim_tc_rms", "bc - tc dolasim RMS / tc dolasim RMS"))
    olc = [o_ for o_ in ("oran", "logit", "h") if o_ in at]
    T(["Nicelik"] + olc + ["Anahtar"],
      [[et] + [sg(at[o_][an], 3) for o_ in olc] + [f"havuz_cifar10.ayar_testi.<olcek>.{an}"] for an, et in alan])

    # (f) ImageNet top-1 (yontem bolumu icin)
    t1 = _m9g(_oku(_M9_HT), ["imagenet_top1"],
              f"Iki ImageNet baslatma kontrol noktasinin ImageNet top-1 degeri (ON_KAYIT Dondurma eki (i) m.9; `{_M9_SR}` "
              f"§7 m.6; `{_M9_HT}` imagenet_top1 alani yok)")
    L.append(f"ImageNet baslatma kontrol noktalarinin ImageNet top-1 degeri: {'bulunamadi' if t1 is None else t1}.\n")


_m9("M9.9 Masa cozumlemeleri (SENTEZ ve konsey_masa)",
    f"`{_M9_SN}` tanim, kumeler.<kume>.{{tam_orneklem.<nicelik>.{{ort, sd_kosum, degerler}}, goruntu_bootstrap_pair1}}, "
    f"havuz_tohum1.{{kaynak_acigi_ayristirma_log, hedef_farki_ayristirma_log, <m>.{{panel, log_tau_ort, r_ort}}}}; "
    f"`{_M9_MC}` betik, not, 1_havuz_model_tablosu.{{panel, modeller.<m>.{{yari_log, tam_log, kaynak_acigi_R_eksi_m_<olcek>}}, "
    f"jackknife_aralik}}; `{_M9_J4}` panel.birincil, b4.model_tablosu.<m>.yari_log; `{_M9_P3Y}` A_kolu, havuz_AT7; "
    f"`{_M9_P3P}` havuz_cifar10.{{klasor, modeller, n, B, ayar_testi}}; `{_M9_HT}` imagenet_top1 (yok)", _m9_9)

for _i9 in _M9_YOK_YER:
    L[_i9] = ("Bu bolumde (M9.1-M9.9) JSON'da bulunamayip 'bulunamadi' yazilan kalemler: "
              + ("; ".join(_M9_YOK) if _M9_YOK else "yok") + ".\n")

# <<< M9 SONU (konsey turu)

# ===========================================================================
# GENISLETME 2026-10-31 (M10, ek on kayit B8-B10): ek bloklarin sonuclari.
# B9 (CIFAR-100 paneli; dondurulmus betigin --mod b2 cozumlemesi, baglayici),
# B8 (ImageNetV2 paneli; betimsel, Holm yok) ve B10 (girdi gradyani kosinusu
# ile log tau arasinda Mantel; aile F_B10). Her sayi JSON/log dosyalarindan
# okunur; on kayit kayitlari (sha256) ek on kaydin Dondurma ekinden ve sapma
# kaydindan regex ile okunur. Mevcut bolumlere dokunulmaz; karantina
# yollarindan OKUNMAZ. Bolum M9'dan sonra, 'Sabit dizgeler'den once gelir.
# ===========================================================================
_M10_EK = "raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md"
_M10_SP = "results/q1_research/ONKAYIT_SAPMALAR.md"
_M10_RG = "results/q1/ek_regresyon/gpu_n200"
_M10_RGJ = ("karsilastirma_ozgun_catal.json", "karsilastirma_ozgun_onb_catal_onb.json")
_M10_LG = "results/q1/ek_loglar"
_M10_OD = "results/q1/konsey_b8_imagenetv2/denetim/onisleme_denetimi.json"
_M10_MF = "results/q1/konsey_b8_imagenetv2/denetim/imagenetv2_manifest.json"
_M10_B9 = "results/q1/konsey_b9_c100/b9_dondurulmus_b2.json"
_M10_B9S = "results/q1/konsey_b9_c100/b9_sarmalayici_b2.json"
_M10_B9W = "results/q1/konsey_b9_c100/b9_sarmalayici_b2.json.sarmalayici.json"
_M10_B9M = "results/q1/konsey_b9_c100/matris"
_M10_B8D = "results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json"
_M10_B8B = "results/q1/konsey_b8_imagenetv2/b8_betimsel.json"
_M10_B8M = "results/q1/konsey_b8_imagenetv2/matris"
_M10_HT8 = "raporlar/konsey_2026-10-29/hucre_tablosu_b8.json"
_M10_HT9 = "raporlar/konsey_2026-10-29/hucre_tablosu_b9.json"
_M10_RB = "raporlar/konsey_2026-10-29/_ek_denetim/dis/rb/in_{}.json"
_M10_G = "results/q1/konsey_b10_gradyan"
_M10_GA = "results/q1/konsey_b10_gradyan/b10_aile.json"
_M10_VK = ("cifar10", "cifar100", "imagenetv2")
_M10_HTV = {"cifar10": _M9_HT, "cifar100": _M10_HT9, "imagenetv2": _M10_HT8}
_M10_OZG = "experiments/c1_c3_transfer_matrix.py"
_M10_YOK = []
_M10_YOK_YER = []


def _m10(ad, kaynak, fn):
    L.append(f"\n### {ad}\n")
    try:
        fn()
    except (KeyError, TypeError, IndexError, ValueError, OSError, ZeroDivisionError, AttributeError) as e_:
        _hata(e_)
    L.append(f"_Kaynak: {kaynak}_\n")


def _m10g(d, yol, etiket):
    """Anahtar yolunu izler; yoksa None doner ve kalemi M10 bulunamayanlar listesine yazar."""
    x = d
    for k_ in yol:
        if isinstance(x, dict) and k_ in x:
            x = x[k_]
        else:
            _M10_YOK.append(etiket)
            return None
    return x


def _m10metin(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def _m10kayit(metin):
    """Kod bloklarindaki '<sha256>  <yol>' satirlari: {yol: sha256}."""
    return dict((p_, h_) for h_, p_ in _m8re.findall(r"^([0-9a-f]{64})\s+(\S+)$", metin, _m8re.M))


def _m10ek():
    """Ek on kaydin Dondurma eki: (a)-(c) kod bloklari ve (d) govde ozeti."""
    ek = _m10metin(_M10_EK)
    eki = ek[ek.index("\n## Dondurma eki\n"):]
    m_d = _m8re.search(r"^\(d\)[^\n]*?`([0-9a-f]{64})`", eki, _m8re.M)
    return _m10kayit(eki), (m_d.group(1) if m_d else None)


def _m10sp_kod():
    """Sapma kaydinin Ek B8-B10 'kod eki' basligi altindaki ozetler."""
    sp = _m10metin(_M10_SP)
    m_ = _m8re.search(r"^### [^\n]*kod eki[^\n]*\n(.*?)(?=^### |\Z)", sp, _m8re.M | _m8re.S)
    return _m10kayit(m_.group(1)) if m_ else {}


def _m10temiz(TM, m):
    v_ = {r_["target_clean_acc"] for k_, r_ in TM["results"].items() if k_.split("->")[1] == m}
    if len(v_) != 1:
        raise ValueError(f"{m}: hedef temiz dogruluk kaynaklar arasinda tutarsiz {sorted(v_)}")
    return v_.pop()


def _m10ust(M):
    a = np.asarray(M, dtype=float)
    i_, j_ = np.triu_indices(a.shape[0], 1)
    return a[i_, j_]


def _m10payda(ka, etiket, numara=None):
    """payda_kucuk_tohumlar 0 tabanli indeks listesidir (dondurulmus betik: enumerate(ka['D'])); cift numarasina cevrilir."""
    out = []
    for i_ in ka["payda_kucuk_tohumlar"]:
        no_ = numara(i_) if numara else i_ + 1
        out.append(f"{etiket} {no_} ({' / '.join(ka['ciftler'][i_])}, D = {ka['D'][i_]:.4f}; JSON indeksi {i_})")
    return "; ".join(out) or "yok"


def _m10duy(D):
    """b2.duyarlilik alanlarinin tablo satirlari (B9 ve B8 icin ayni kalip)."""
    jk = D["panel_jackknife"]

    def rh(r_, nd, ek=""):
        return (f"ort rho(V-scr) {sg(r_['ort'], nd, True)}{ek}, %90 {_m9a(r_['ci90'], nd, True)}, "
                f"%95 {_m9a(r_['ci95'], nd, True)}")
    return [["Tam orneklem, log", f"ort q {sg(D['tam_log']['q_ort'], 3)}", rh(D['tam_log']['rho_V'], 3),
             "b2.duyarlilik.tam_log"],
            ["Yari logit", f"ort q {sg(D['yari_logit']['q_ort'], 3)} (q_s: {uc(D['yari_logit']['q'], 3)})",
             rh(D['yari_logit']['rho_V'], 3), "b2.duyarlilik.yari_logit"],
            ["Yari oran (rho puan)", f"ort q {sg(D['yari_oran']['q_ort'], 3)}", rh(D['yari_oran']['rho_V'], 2, " puan"),
             "b2.duyarlilik.yari_oran"],
            ["Panel jackknife", "ort q " + _m9oran({m: v["q_ort"] for m, v in jk.items()}, 3, False),
             "ort rho(V-scr) " + _m9oran({m: v["rho_V_ort"] for m, v in jk.items()}, 3), "b2.duyarlilik.panel_jackknife"],
            [f"Ikincil panel ({', '.join(D['ikincil_panel']['panel'])})", f"q_s {uc(D['ikincil_panel']['q'], 3)}",
             f"rho(V-scr) {uc(D['ikincil_panel']['rho_V'], 3, True)}", "b2.duyarlilik.ikincil_panel"]]


def _m10kosegen(md, TM, ms):
    """Kosegen npz denetimi: 100 - raw_fooling ile 100 * ort(~target_adv_wrong) farki ve temiz yanlis / saldiri altinda dogru
    ornek sayisi; cond_fooling'in 2 ondalikla saklanip saklanmadigi (round(x, 2) == x) hucre sayimi."""
    fk, ny = [], 0
    for m in ms:
        d_ = np.load(os.path.join(ROOT, md, f"per_sample_{m}_to_{m}.npz"))
        aw, cc = d_["target_adv_wrong"].astype(bool), d_["target_clean_correct"].astype(bool)
        fk.append(abs((100 - TM["results"][f"{m}->{m}"]["raw_fooling"]) - 100 * float((~aw).mean())))
        ny += int((~cc & ~aw).sum())
    cf = [r_["cond_fooling"] for r_ in TM["results"].values()]
    return max(fk), ny, sum(1 for x_ in cf if round(x_, 2) == x_), len(cf)


sec("M10: Ek bloklar, CIFAR-100 paneli, ImageNetV2 paneli ve gradyan kosinusu (2026-10-31)",
    f"{_M10_RG}/karsilastirma_*.json; {_M10_LG}/*.log, regresyon_gpu200.txt; {_M10_OD}; {_M10_MF}; {_M10_B9}; {_M10_B9W}; "
    f"{_M10_B9M}/{{transfer_matrix.json, cells_meta.json}}; {_M10_HT9}; {_M10_B8D}; {_M10_B8B}; "
    f"{_M10_B8M}/{{transfer_matrix.json, cells_meta.json}}; {_M10_HT8}; {_M10_RB.format('<model>')}; "
    f"{_M10_G}/<veri>/kosinus_ozet.json; {_M10_G}/mantel_<veri>.json; {_M10_GA}; {_M9_J2} (yalniz CIFAR-10 karsilastirma sutunu); "
    f"{_M10_EK} (yalniz Dondurma eki ve govde sha256); {_M10_SP} (yalniz Ek B8-B10 kayitlari)")
L.append("Ek on kayitli B8, B9 ve B10 bloklarinin sonuclaridir. B9 baglayicidir (aile F_B9, Holm); B8 betimseldir (Holm yok, "
         "baglayici karar yok); B10'un karar ailesi F_B10'dur (Holm). Asagidaki her alt bolum kendi artefaktindan okunur ve altinda "
         "kaynak dosya ile anahtar yollari yazilidir. Yuvarlama M9 kuraliyla: log olcekli nicelikler, oranlar ve korelasyonlar 3 "
         "ondalik, puanlar (yuzde) 2 ondalik, p degerleri bilimsel gosterim.\n")


# --- M10.1 On kosullar ----------------------------------------------------------------------
def _m10_1():
    sat = []
    for ad in _M10_RGJ:
        k = _oku(f"{_M10_RG}/{ad}")
        sat.append([f"`{ad}`", f"`{k['A']}` / `{k['B']}`", k["hucre_sayisi"], k["npz_sayisi"], len(k["json_farkli_hucreler"]),
                    len(k["npz_farklari"]), len(k["ust_alan_farklari"]), _m9e(k["BIREBIR"])])
    L.append(f"GPU catal regresyonu (ozgun matris betigi `{_M10_OZG}` ile catal betik; klasor adlari A / B sutununda):\n")
    T(["Karsilastirma", "A / B", "Hucre sayisi", "npz sayisi", "JSON'u farkli hucre", "npz farki", "Ust alan farki", "BIREBIR"], sat)
    lg = _m10metin(f"{_M10_LG}/regresyon_gpu200.txt")
    ay = _m8re.findall(r"^ayni (\S+)$", lg, _m8re.M)
    fk = _m8re.findall(r"^FARKLI (\S+)$", lg, _m8re.M)
    rc = []
    for g_ in ("ek_zincir_1.log", "ek_zincir_2.log"):
        rc += [f"{a_} rc={b_}" for a_, b_ in _m8re.findall(r"^(.+?) rc=(\d+)\s*$", _m10metin(f"{_M10_LG}/{g_}"), _m8re.M)]
    L.append(f"Onbellek dosyalarinin bayt karsilastirmasi (`{_M10_LG}/regresyon_gpu200.txt`, 'ayni'/'FARKLI' satirlari): "
             f"{len(ay)} ayni, {len(fk)} FARKLI. Zincir gunluklerindeki adim donus kodlari (`{_M10_LG}/ek_zincir_{{1,2}}.log`): "
             + "; ".join(dict.fromkeys(rc)) + ".\n")

    OD = _oku(_M10_OD)
    so = []
    for m, v in OD["modeller"].items():
        e_ = v["esik"]
        so.append([m, v["model"], sg(v["temiz_dogruluk_ortak"], 2), sg(v["temiz_dogruluk_kendi"], 2), sg(v["fark_puan"], 2, True),
                   sg(e_["mutlak_fark_puan"], 2), sg(e_["rb_temiz"], 2), sg(e_["esik_i"], 2), _m9e(e_["i_gecti"]),
                   _m9e(e_["ii_gecti"]), _m9e(e_["isaretli_3_5"]), e_["karar"]])
    L.append(f"B8 on isleme denetimi (n = {OD['n']} goruntu; ortak hat {OD['ortak_onisleme']}; temiz dogruluk %; varyant farki = "
             f"ortak - kendi, puan; 'Esik (i)' kendi hat icin alt sinir, puan; RB temiz `esik.rb_temiz`):\n")
    T(["Takma ad", "RobustBench adi", "Temiz, ortak hat", "Temiz, kendi hat", "Varyant farki", "Mutlak fark", "RB temiz",
       "Esik (i)", "(i) gecti", "(ii) gecti", "isaretli_3_5", "Karar"], so)
    mf = {m: v["esik"]["mutlak_fark_puan"] for m, v in OD["modeller"].items()}
    km = max(mf, key=mf.get)
    L.append(f"Model sayisi {len(OD['modeller'])}; `kalan` listesi: {', '.join(OD['kalan']) or 'bos'}; `isaretli` listesi: "
             f"{', '.join(OD['isaretli']) or 'bos'}; karari 'gecti' disinda olan: "
             f"{', '.join(m for m, v in OD['modeller'].items() if v['esik']['karar'] != 'gecti') or 'yok'}; en buyuk mutlak "
             f"varyant farki {sg(mf[km], 2)} puan ({km}). Model ici normalizasyon katmani tasiyan model: "
             f"{sum(1 for v in OD['normalizasyon'].values() if v['model_ici_normalizasyon_var'])}/{len(OD['normalizasyon'])}. "
             f"Kural (JSON `not`): '{OD['not']}'\n")

    MF = _oku(_M10_MF)
    TM8 = _oku(f"{_M10_B8M}/transfer_matrix.json")
    KO = _oku(f"{_M10_G}/imagenetv2/kosinus_ozet.json")
    sp = _m10metin(_M10_SP)
    m_l = _m8re.search(r"`([0-9a-f]{64})`[^`\n]{0,12}\(`" + _m8re.escape(_M10_MF) + r"`, `liste_sha256`", sp)
    ls = MF["liste_sha256"]
    kars = (("B8 matrisi (`transfer_matrix.json` manifest_liste_sha256)", TM8.get("manifest_liste_sha256")),
            ("B10 ImageNetV2 kosinus ozeti (imagenetv2_liste_sha256)", KO.get("imagenetv2_liste_sha256")),
            (f"sapma kaydi (`{_M10_SP}`)", m_l.group(1) if m_l else None))
    L.append(f"ImageNetV2 orneklemi (`{_M10_MF}`): n = {MF['n']}; dosya listesi uzunlugu {len(MF['dosyalar'])}; tensor sekli "
             f"{MF['tensor_sekli']}; on isleme {MF['onisleme']}; secim kurali '{MF['secim_kurali']}'; liste_sha256 {ls}. Ayni ozet: "
             + "; ".join(f"{a_} {'AYNI' if b_ == ls else ('bulunamadi' if b_ is None else 'FARKLI (' + b_ + ')')}" for a_, b_ in kars)
             + f". B8 matrisindeki manifest_n = {TM8['manifest_n']}.\n")

    sm = []
    for blok, md, js in (("B9", _M10_B9M, _M10_B9), ("B8", _M10_B8M, _M10_B8D)):
        cm = _oku(f"{md}/cells_meta.json")
        J = _oku(js)
        npz = len(_m8glob.glob(os.path.join(ROOT, md, "per_sample_*.npz")))
        sm.append([blok, cm["dataset"], f"{cm['attack']} {cm['norm']}", sg(cm["eps"] * 255, 2), sg(cm["alpha"] * 255, 2), cm["steps"],
                   cm["seed"], cm["n_samples"], _m9e(cm["per_source_seed"]), cm.get("onisleme", "-"), J["veri"]["hucre_sayisi"], npz,
                   len(J["veri"]["modeller"]), len(J["veri"]["cakismalar"]), len(J["veri"]["tablo_disi_modeller"]),
                   _m9e(J["veri"]["tutarlilik"]["hedef_maskesi_tutarli"])])
    L.append("Matris kosu ayarlari (`cells_meta.json`; eps ve alpha x 255 turetilmis) ve dondurulmus betigin veri denetimi (`veri`):\n")
    T(["Blok", "Veri", "Saldiri", "eps x 255", "alpha x 255", "Adim", "Tohum", "n", "Kaynak basina tohum", "On isleme",
       "JSON hucre sayisi", "Klasordeki per_sample npz", "Model sayisi", "Cakisma", "Tablo disi model", "Hedef maskesi tutarli"], sm)


_m10("M10.1 On kosullar (catal regresyonu, B8 on isleme denetimi, ImageNetV2 orneklemi, matris ayarlari)",
     f"`{_M10_RG}/karsilastirma_*.json` A, B, hucre_sayisi, npz_sayisi, json_farkli_hucreler, npz_farklari, ust_alan_farklari, BIREBIR; "
     f"`{_M10_LG}/regresyon_gpu200.txt` (ayni/FARKLI satirlari); `{_M10_LG}/ek_zincir_{{1,2}}.log` (rc satirlari); `{_M10_OD}` n, "
     f"ortak_onisleme, modeller.<m>.{{model, temiz_dogruluk_ortak, temiz_dogruluk_kendi, fark_puan, esik.{{karar, esik_i, i_gecti, "
     f"mutlak_fark_puan, ii_gecti, isaretli_3_5, rb_temiz}}}}, kalan, isaretli, normalizasyon, not; `{_M10_MF}` n, dosyalar, "
     f"tensor_sekli, onisleme, secim_kurali, liste_sha256; `{_M10_B8M}/transfer_matrix.json` manifest_liste_sha256, manifest_n; "
     f"`{_M10_G}/imagenetv2/kosinus_ozet.json` imagenetv2_liste_sha256; `{_M10_SP}` (liste ozeti kaydi); `<matris>/cells_meta.json`; "
     f"`{_M10_B9}`, `{_M10_B8D}` veri.{{hucre_sayisi, modeller, cakismalar, tablo_disi_modeller, tutarlilik}}", _m10_1)


# --- M10.2 B9 aile F_B9 (F_B2'nin CIFAR-100 yinelemesi) ----------------------------------------
def _m10_2():
    J9, J2 = _oku(_M10_B9), _oku(_M9_J2)
    F9, F2 = J9["b2"]["F_B2"], J2["b2"]["F_B2"]

    def gz(F):
        ka, kb, kc = F["K-a"], F["K-b"], F["K-c"]
        return {"K-a": (f"ort q {sg(ka['sinama']['ort'], 3)} (q_s: {uc(ka['q'], 3)})", _m9a(ka["sinama"]["ci90"]),
                        _m9a(ka["sinama"]["ci95"]), _m9p(F["p_ham"][0])),
                "K-b": (f"ort rho {sg(kb['ort'], 3, True)} (tohumlar: {uc(kb['degerler'], 3, True)})", _m9a(kb["ci90"], 3, True),
                        _m9a(kb["ci95"], 3, True), f"TOST {_m9p(F['p_ham'][1])}"),
                "K-c": (f"Delta_w {sg(kc['Delta_w'], 3, True)}", f"bootstrap {_m9a(kc['bootstrap']['ci90'], 3, True)}",
                        f"bootstrap {_m9a(kc['bootstrap']['ci95'], 3, True)}", _m9p(F["p_ham"][2]))}

    g9, g2 = gz(F9), gz(F2)
    tanim = {"K-a": "K-a, simetrik oran q_s", "K-b": "K-b, ViT yonlu terimi rho(V-scr)", "K-c": "K-c, tur ici benzerlik Delta_w"}
    satir = []
    for i_, k_ in enumerate(("K-a", "K-b", "K-c")):
        satir.append([tanim[k_], g9[k_][0], g9[k_][1], g9[k_][2], g9[k_][3], _m9p(F9["p_holm"][i_]), F9["karar"][k_],
                      g2[k_][0], g2[k_][1], _m9p(F2["p_holm"][i_]), F2["karar"][k_]])
    L.append("CIFAR-100 (B9) ve karsilastirma icin CIFAR-10 (B2, M9.5 ile ayni kaynak):\n")
    T(["Sinama", "CIFAR-100 gozlenen", "CIFAR-100 %90 aralik", "CIFAR-100 %95 aralik", "CIFAR-100 ham p", "CIFAR-100 Holm p",
       "CIFAR-100 karar", "CIFAR-10 gozlenen", "CIFAR-10 %90 aralik", "CIFAR-10 Holm p", "CIFAR-10 karar"], satir)
    hk = holm(F9["p_ham"])
    kr = F9["karar"]
    L.append(f"B9 karar ayrintilari (b2.F_B2.karar): " + "; ".join(f"{kk}: {_m9e(vv)}" for kk, vv in kr.items()
                                                                     if kk not in ("K-a", "K-b", "K-c")) + ".\n")
    kb = F9["K-b"]
    L.append(f"B9 K-b TOST tek yonlu p'leri: alt {_m9p(kb['tost_p_alt'])}, ust {_m9p(kb['tost_p_ust'])} (tost_p = buyugu "
             f"{_m9p(kb['tost_p'])}); sd {sg(kb['sd'], 3)}, df {kb['df']}. F_B2.not: '{F9.get('not', 'bulunamadi')}'. TOST siniri "
             f"delta = {J9['meta']['delta']}; Holm alfa = {J9['meta']['alfa']}; bootstrap B = {J9['meta']['bootstrap_B']}, tohum "
             f"{J9['meta']['bootstrap_tohum']}. Holm denetimi (holm() ile p_ham'dan): en buyuk mutlak fark "
             f"{float(np.max(np.abs(hk - np.asarray(F9['p_holm'])))):.2e}. Hesaplanamayip p = 1 sayilan: "
             f"{', '.join(str(x_) for x_ in F9['p_1_sayilan_hesaplanamayan']) or 'yok'}.\n")
    dk = f"duyarlilik_delta_{J9['meta']['delta_duyarlilik']}"
    dd = F9[dk]
    L.append(f"delta = {dd['delta']} duyarliligi (b2.F_B2.{dk}): Holm p {', '.join(_m9p(x_) for x_ in dd['p_holm'])}; K-a "
             f"{dd['karar']['K-a']}; K-b {dd['karar']['K-b']}; K-c {dd['karar']['K-c']}.\n")
    ka, kc = F9["K-a"], F9["K-c"]
    L.append(f"K-a ayrintisi: D_s {uc(ka['D'], 3)}; simetrik pay {uc(ka['simetrik_pay'], 3)}; yonlu pay {uc(ka['yonlu_pay'], 3)}; "
             f"tek yonlu t p (p_tek_H0_q_le_0.5) {_m9p(ka.get('p_tek_H0_q_le_0.5'))}; payda kurali tetiklenen tohum cifti: "
             f"{_m10payda(ka, 'tohum cifti')}; ozdeslik artigi en buyuk "
             f"{ka['ozdeslik_artik_max']:.1e}; ciftler: " + "; ".join(" / ".join(c_) for c_ in ka["ciftler"]) + ".\n")
    tr = J9["b2"].get("tur_ici_resnet_log_tau", {})
    lt = list(kc["log_tau_tur_ici"].values())
    L.append(f"K-c ayrintisi: ViT tur ici log tau {uc(lt, 3, True)} (ort {sg(float(np.mean(lt)), 3, True)}); sigma_V "
             f"{uc(list(kc['sigma_V'].values()), 3, True)}; bootstrap B = {kc['bootstrap']['B']}, yeniden cekilen tek tohumlu ornek "
             f"{kc['bootstrap']['yeniden_cekilen_tek_tohumlu_ornek']}; ResNet tur ici log tau "
             f"{uc(list(tr.values()), 3, True) if tr else 'bulunamadi'}"
             f"{(' (ort ' + sg(float(np.mean(list(tr.values()))), 3, True) + ')') if tr else ''}.\n")
    ds = _m10duy(J9["b2"]["duyarlilik"])
    L.append("B9 duyarliliklari ve kesifsel S9-1, S9-3 (karar degistirmez):\n")
    T(["Duyarlilik", "q", "rho(V-scr) ve diger", "Anahtar"], ds)
    W = _oku(_M10_B9W)
    wm = W["meta"]
    tz = W["temiz_dogruluk_yuzde"]
    ayni_k = W["dondurulmus_ozet"]["karar"] == F9["karar"]
    L.append(f"Sarmalayici yan bilgisi (`{_M10_B9W}`; mod {wm['mod']}; dondurulmus betik cagrisi "
             f"`{' '.join(wm['dondurulmus_cagri_argv'])}`): dondurulmus_ozet.karar ile `{_M10_B9}` b2.F_B2.karar "
             f"{'AYNI' if ayni_k else 'FARKLI'}; ozgun_matris_betigi_degismedi: {_m9e(wm['ozgun_matris_betigi_degismedi'])}. Temiz "
             f"dogruluk (temiz_dogruluk_yuzde, %): " + "; ".join(f"{m} {sg(v, 2)}" for m, v in tz.items())
             + f". Sarmalayicinin karistirici notu (JSON metni): '{W.get('karistirici_notu', 'bulunamadi')}'\n")


_m10("M10.2 B9 aile F_B9: F_B2'nin CIFAR-100 yinelemesi (K-a, K-b, K-c; Holm)",
     f"`{_M10_B9}` b2.F_B2.K-a.{{q, sinama.{{ort, ci90, ci95}}, D, simetrik_pay, yonlu_pay, p_tek_H0_q_le_0.5, ozdeslik_artik_max, "
     f"payda_kucuk_tohumlar, ciftler}}; b2.F_B2.K-b.{{degerler, ort, sd, df, ci90, ci95, tost_p, tost_p_alt, tost_p_ust}}; "
     f"b2.F_B2.K-c.{{Delta_w, bootstrap, log_tau_tur_ici, sigma_V}}; b2.F_B2.{{p_ham, p_holm, karar, not, p_1_sayilan_hesaplanamayan, "
     f"duyarlilik_delta_<meta.delta_duyarlilik>}}; b2.duyarlilik.{{tam_log, yari_logit, yari_oran, panel_jackknife, ikincil_panel}}; "
     f"b2.tur_ici_resnet_log_tau; meta.{{delta, alfa, bootstrap_B, bootstrap_tohum}}; `{_M9_J2}` b2.F_B2 (ayni anahtarlar, CIFAR-10 "
     f"sutunlari); `{_M10_B9W}` meta.{{mod, dondurulmus_cagri_argv, ozgun_matris_betigi_degismedi}}, temiz_dogruluk_yuzde, "
     f"karistirici_notu, dondurulmus_ozet.karar", _m10_2)


# --- M10.3 B9 model tablosu --------------------------------------------------------------------
def _m10_3():
    J9 = _oku(_M10_B9)
    TM = _oku(f"{_M10_B9M}/transfer_matrix.json")
    tzw = _oku(_M10_B9W)["temiz_dogruluk_yuzde"]
    HT = _oku(_M10_HT9)["modeller"]
    MT = J9["b2"]["model_tablosu"]
    sat, fw, ft = [], [], []
    for m, h in HT.items():
        d_ = TM["results"][f"{m}->{m}"]
        tz = _m10temiz(TM, m)
        yl, yo = MT[m]["yari_log"], MT[m]["yari_oran"]
        fw.append(abs(d_["cond_fooling"] - yo["omega"]))
        if m in tzw:
            ft.append(abs(tzw[m] - tz))
        sat.append([m, h["hucre"], h["aile"], "-" if h["tohum"] is None else h["tohum"], _m9e(h["birincil_panel"]),
                    _m9e(h["ikincil_panel"]), sg(tz, 2), sg(d_["raw_fooling"], 2), sg(100 - d_["raw_fooling"], 2),
                    sg(yo["omega"], 2), sg(yl["omega"], 3), sg(yl["sigma"], 3, True), sg(yl["rho"], 3, True), yl["panel_n"]])
    L.append(f"CIFAR-100, {TM['n_samples']} test goruntusu (temiz ve PGD beyaz kutu `transfer_matrix.json` kosegeninden, %; "
             f"PGD-{TM['steps']} gurbuz dogruluk turetilmis: 100 - raw_fooling, yani saldiri altinda dogru siniflanan ornek orani, "
             f"temiz dogrulukla kosullanmamis; w = "
             f"beyaz kutu hedef-dogru kirilganlik, model_tablosu.yari_oran.omega, %; omega = log w; sigma ve rho bolunmus yari, log "
             f"olcek; hucre, aile ve panel atamasi `{_M10_HT9}`):\n")
    T(["Model", "Hucre", "Aile", "Tohum", "Birincil panel", "Ikincil panel", "Temiz (%)", "PGD beyaz kutu ham yaniltma (%)",
       f"PGD-{TM['steps']} gurbuz dogruluk (%) (turetilmis: 100 - raw_fooling)", "w (%)", "omega", "sigma", "rho", "panel_n"], sat)
    hs = []
    for h_, ms_ in J9["b2"]["hucreler"].items():
        hs.append([h_, len(ms_), sg(float(np.mean([_m10temiz(TM, m) for m in ms_])), 2),
                   sg(float(np.mean([MT[m]["yari_oran"]["omega"] for m in ms_])), 2),
                   sg(float(np.mean([MT[m]["yari_log"]["sigma"] for m in ms_])), 3, True),
                   sg(float(np.mean([MT[m]["yari_log"]["rho"] for m in ms_])), 3, True)])
    L.append("Hucre ortalamalari (turetilmis, model degerlerinin aritmetik ortalamasi):\n")
    T(["Hucre", "n", "Temiz ort (%)", "w ort (%)", "sigma ort", "rho ort"], hs)
    kf, ky, kr, kn = _m10kosegen(_M10_B9M, TM, list(HT))
    L.append(f"Denetimler: kosegen cond_fooling ile w arasindaki en buyuk mutlak fark {max(fw):.2e} puan (5e-03'ten kucuk: "
             f"{_m9e(max(fw) < 5e-3)}; round(cond_fooling, 2) == cond_fooling olan hucre {kr}/{kn}); "
             f"`transfer_matrix.json` temiz dogrulugu ile sarmalayici temiz_dogruluk_yuzde arasindaki en buyuk mutlak fark "
             f"{max(ft):.2e} puan ({len(ft)} model); hucre tablosundaki model sayisi {len(HT)}, model_tablosu {len(MT)}; "
             f"100 - raw_fooling ile kosegen npz'den 100 * ort(~target_adv_wrong) en buyuk mutlak fark {kf:.2e} puan; kosegen "
             f"npz'lerde temiz yanlis olup saldiri altinda dogru siniflanan ornek sayisi (modeller toplami) {ky}.\n")


_m10("M10.3 B9 model tablosu (CIFAR-100)",
     f"`{_M10_B9M}/transfer_matrix.json` n_samples, steps, results.<m>-><m>.{{raw_fooling, cond_fooling}}, results.*-><m>.target_clean_acc, "
     f"results.*.cond_fooling (denetim); `{_M10_B9M}/per_sample_<m>_to_<m>.npz` target_adv_wrong, target_clean_correct (denetim); "
     f"`{_M10_B9}` b2.model_tablosu.<m>.{{yari_oran.omega, yari_log.{{omega, sigma, rho, panel_n}}}}, b2.hucreler; `{_M10_HT9}` "
     f"modeller.<m>.{{hucre, aile, tohum, birincil_panel, ikincil_panel}}; `{_M10_B9W}` temiz_dogruluk_yuzde (denetim)", _m10_3)


# --- M10.4 B8 ImageNetV2 paneli (betimsel) -------------------------------------------------------
def _m10_4():
    B = _oku(_M10_B8B)
    D8 = _oku(_M10_B8D)
    TM = _oku(f"{_M10_B8M}/transfer_matrix.json")
    OD = _oku(_M10_OD)["modeller"]
    HT = _oku(_M10_HT8)["modeller"]
    MO = B["model_tablosu_ozet"]
    MT = D8["b2"]["model_tablosu"]
    cs = {}
    for c_ in B["ciftler"]:
        cs[c_["cnn"]] = (c_["cift"], c_["satir"])
        cs[c_["donusturucu"]] = (c_["cift"], c_["satir"])
    sat, ft, fw, frb, fs, hh = [], [], [], [], [], []
    for m, h in HT.items():
        mo = MO[m]
        d_ = TM["results"][f"{m}->{m}"]
        tz = _m10temiz(TM, m)
        ft += [abs(tz - mo["temiz_dogruluk_yuzde"]), abs(TM["temiz_dogruluk"][m] - tz)]
        fw.append(abs(d_["cond_fooling"] - mo["w_yuzde"]))
        fs += [abs(mo["sigma"] - MT[m]["yari_log"]["sigma"]), abs(mo["rho"] - MT[m]["yari_log"]["rho"])]
        if mo["hucre"] != h["hucre"]:
            hh.append(m)
        if m in cs:
            st_ = f"cift {cs[m][0]}, {cs[m][1]} satiri"
        elif h["hucre"] in ("panel", "ikincil_panel"):
            st_ = h["hucre"]
        else:
            st_ = "ciftsiz (b8_betimsel ciftler disinda)"
        rbad = OD[m]["model"] if m in OD else None
        rb = load(_M10_RB.format(rbad)) if rbad else None
        if rb is None:
            _M10_YOK.append(f"{m} icin RobustBench model_info kopyasi ({_M10_RB.format(rbad)})")
        else:
            frb.append(abs(float(rb["clean_acc"]) - OD[m]["esik"]["rb_temiz"]))
        if m in cs:
            if h["tohum"] != cs[m][0]:
                raise ValueError(f"{m}: hucre tablosu tohum alani {h['tohum']} ile b8_betimsel cift {cs[m][0]} uyusmuyor")
            cn_ = cs[m][0]
        elif h["tohum"] is None:
            cn_ = "-"
        else:
            cn_ = f"- (tohum alani {h['tohum']}, ciftsiz)"
        sat.append([m, rbad or "bulunamadi", h["hucre"], h["aile"], cn_, st_,
                    sg(mo["temiz_dogruluk_yuzde"], 2), sg(d_["raw_fooling"], 2), sg(100 - d_["raw_fooling"], 2),
                    sg(mo["w_yuzde"], 2), sg(mo["sigma"], 3, True),
                    sg(mo["rho"], 3, True), mo["panel_n"],
                    _m9s(float(rb["clean_acc"]), 2) if rb else "bulunamadi",
                    _m9s(float(rb["autoattack_acc"]), 2) if rb else "bulunamadi"])
    L.append(f"B8 betimseldir: Holm yok, baglayici karar yok (`{_M10_B8B}` etiket: '{B['etiket']}').\n")
    L.append(f"ImageNetV2, {TM['n_samples']} goruntu, PGD-{TM['steps']} {TM['norm']} eps x 255 = {sg(TM['eps_255'], 2)} (temiz ortak "
             f"hatta, `b8_betimsel.json` model_tablosu_ozet.temiz_dogruluk_yuzde; PGD beyaz kutu ham yaniltma `transfer_matrix.json` "
             f"kosegeni; PGD-{TM['steps']} gurbuz dogruluk turetilmis: 100 - raw_fooling, yani saldiri altinda dogru siniflanan "
             f"ornek orani, temiz dogrulukla kosullanmamis; "
             f"w = model_tablosu_ozet.w_yuzde; sigma ve rho bolunmus yari, log; hucre ve aile `{_M10_HT8}`; cift numarasi "
             f"`b8_betimsel.json` ciftler.<k>.cift (hucre tablosu tohum alaniyla esitligi denetlenir; ciftsiz modelde tohum alani "
             f"parantez icinde), "
             f"satir `b8_betimsel.json` ciftler.<k>.satir; RB sutunlari RobustBench model_info kopyalarinin clean_acc ve "
             f"autoattack_acc alanlari, ortak hatta olculmemistir):\n")
    T(["Takma ad", "RobustBench adi", "Hucre (kod yolu)", "Aile", "Cift no", "Satir", "Temiz (%)",
       "PGD beyaz kutu ham yaniltma (%)", f"PGD-{TM['steps']} gurbuz dogruluk (%) (turetilmis: 100 - raw_fooling)", "w (%)",
       "sigma", "rho", "panel_n", "RB bildirilen temiz (%)", "RB bildirilen AA (%)"], sat)
    kf, ky, kr, kn = _m10kosegen(_M10_B8M, TM, list(HT))
    L.append(f"Denetimler: temiz dogruluk (`transfer_matrix.json` hedef temiz, temiz_dogruluk alani ve b8_betimsel) en buyuk mutlak "
             f"fark {max(ft):.2e} puan; kosegen cond_fooling ile w en buyuk mutlak fark {max(fw):.2e} puan (5e-03'ten kucuk: "
             f"{_m9e(max(fw) < 5e-3)}; round(cond_fooling, 2) == cond_fooling olan hucre {kr}/{kn}); 100 - raw_fooling ile kosegen "
             f"npz'den 100 * ort(~target_adv_wrong) en buyuk mutlak fark {kf:.2e} puan; kosegen npz'lerde temiz yanlis olup saldiri "
             f"altinda dogru siniflanan ornek sayisi (modeller toplami) {ky}; b8_betimsel sigma ve rho "
             f"ile `{_M10_B8D}` b2.model_tablosu.<m>.yari_log en buyuk mutlak fark {max(fs):.2e}; RB clean_acc ile on isleme "
             f"denetimindeki esik.rb_temiz en buyuk mutlak fark {max(frb):.2e} puan ({len(frb)} model); hucre etiketi uyusmayan: "
             f"{', '.join(hh) or 'yok'}.\n")

    KA = D8["b2"]["F_B2"]["K-a"]
    cf = []
    for i_, c_ in enumerate(B["ciftler"]):
        if list(KA["ciftler"][i_]) != [c_["cnn"], c_["donusturucu"]]:
            raise ValueError(f"cift sirasi uyusmuyor: {KA['ciftler'][i_]} / {c_['cnn']}, {c_['donusturucu']}")
        cf.append([c_["cift"], c_["cnn"], c_["donusturucu"], c_["satir"], sg(c_["A_sigma"], 3, True),
                   _m9a(c_["goruntu_bootstrap_ci90"], 3, True), _m9a(c_["goruntu_bootstrap_ci95"], 3, True),
                   sg(c_["A_sigma_logit"], 3, True), sg(c_["A_rho"], 3, True), sg(c_["A_omega_log_w"], 3, True),
                   sg(KA["D"][i_], 4), sg(KA["simetrik_pay"][i_], 3), sg(KA["yonlu_pay"][i_], 3, True), sg(KA["q"][i_], 3), c_["durum"]])
    L.append("Cift duzeyi (A = donusturucu - CNN; A^sigma bolunmus yari, log; aralik goruntu bootstrap'i; D, simetrik pay, yonlu pay "
             "ve q dondurulmus betigin K-a alanlarindan, ayni cift sirasiyla; D_k yuvarlama kuralina istisna olarak 4 ondalik, "
             f"payda kurali D_k <= {D8['meta']['delta']} (`{_M10_B8D}` meta.delta) ile karsilastirma icin):\n")
    T(["Cift", "CNN", "Donusturucu", "Satir", "A^sigma", "%90 aralik", "%95 aralik", "A^sigma (logit)", "A^rho", "A^omega (log w)",
       "D_k", "Simetrik pay", "Yonlu pay", "q_k", "Durum"], cf)
    se = []
    for an in ("A_sigma_IN", "A_sigma_scr_Liu"):
        x = B[an]
        gb = x["goruntu_bootstrap"]
        se.append([f"{an} ({x['tanim']})", ", ".join(str(c_) for c_ in x["ciftler"]), uc(x["cift_degerleri"], 3, True),
                   sg(x["kestirim"], 3, True), _m9a(gb["ci90"], 3, True), _m9a(gb["ci95"], 3, True), x["betimsel_etiket"],
                   f"'{x['beklenti']}' (esik {x['beklenti_esigi']}; nokta esikte ya da altinda: "
                   f"{_m9e(x['nokta_beklenti_esiginde_ya_da_altinda'])})"])
    L.append(f"Satir kestirimleri (`{_M10_B8B}`; 'Beklenti' sutunu JSON'daki beklenti ve beklenti_esigi alanlaridir, kaynagi ek on "
             f"kayit §5.6; betimsel etiket karar degildir):\n")
    T(["Nicelik", "Ciftler", "Cift degerleri", "Kestirim", "%90 aralik", "%95 aralik", "Betimsel etiket", "Beklenti"], se)
    ai = B["A_sigma_IN"]
    L.append(f"A_sigma_IN iki cift farki {sg(ai['iki_cift_farki'], 3)}; not: '{ai.get('not', 'bulunamadi')}'. Goruntu bootstrap'i "
             f"B = {ai['goruntu_bootstrap']['B']}, tohum {ai['goruntu_bootstrap']['tohum']} ('{ai['goruntu_bootstrap']['not']}').\n")
    L.append("Donusturucu rho ve sigma, ayri ayri (donusturucu_rho_ayri_ayri): "
             + "; ".join(f"{m} rho {sg(v['rho'], 3, True)}, sigma {sg(v['sigma'], 3, True)}"
                         for m, v in B["donusturucu_rho_ayri_ayri"].items()) + ".\n")
    F = D8["b2"]["F_B2"]
    kb, kc = F["K-b"], F["K-c"]
    lt8 = kc["log_tau_tur_ici"]
    k8n, k8x = min(lt8, key=lt8.get), max(lt8, key=lt8.get)
    L.append(f"Dondurulmus betigin B8 ciktisi (`{_M10_B8D}`; p degerleri, Holm ve etiketler B8'de karar DEGILDIR, yalniz betimsel): "
             f"K-a ort q {sg(KA['sinama']['ort'], 3)}, %90 {_m9a(KA['sinama']['ci90'])}, payda kurali tetiklenen cift: "
             f"{_m10payda(KA, 'cift', lambda i_: B['ciftler'][i_]['cift'])}; K-b {kb['n']} donusturucunun ort rho "
             f"{sg(kb['ort'], 3, True)}, %90 {_m9a(kb['ci90'], 3, True)}, %95 {_m9a(kb['ci95'], 3, True)}, TOST p "
             f"{_m9p(kb['tost_p'])}; K-c Delta_w "
             f"{sg(kc['Delta_w'], 3, True)}, bootstrap %90 {_m9a(kc['bootstrap']['ci90'], 3, True)}, p {_m9p(kc['p_tek_H0_Delta_le_0'])}, "
             f"donusturucu ciftleri arasi log tau (K-c.log_tau_tur_ici, {len(lt8)} cift) en kucuk {sg(lt8[k8n], 3, True)} ({k8n}), "
             f"en buyuk {sg(lt8[k8x], 3, True)} ({k8x}); "
             f"p_ham {', '.join('null (hesaplanamadi)' if x_ is None else _m9p(x_) for x_ in F['p_ham'])}; p_holm "
             f"{', '.join(_m9p(x_) for x_ in F['p_holm'])}; hesaplanamayip p = 1 sayilan "
             f"{', '.join(('indeks ' + str(x_) + ' (' + ('K-a', 'K-b', 'K-c')[x_] + ')') if isinstance(x_, int) else str(x_) for x_ in F['p_1_sayilan_hesaplanamayan']) or 'yok'}; betigin etiketleri K-a "
             f"'{F['karar']['K-a']}', K-b '{F['karar']['K-b']}', K-c '{F['karar']['K-c']}'.\n")
    hd = B["hodge_r_kesifsel"]
    L.append(f"S8-2 Hodge (kesifsel, K = {hd['K']}): potansiyel payi {sg(hd['G_potansiyel_payi'], 3)}; rastgele beklenti 2/K "
             f"{sg(hd['G_rastgele_beklenti_2_bolu_K'], 3)}; dolasim RMS {sg(hd['dolasim_rms'], 3)}; r RMS {sg(hd['r_rms'], 3)}.\n")
    L.append(f"B8 duyarliliklari (`{_M10_B8D}` b2.duyarlilik; ek on kayit §5.7 S8-3; betimsel, karar yok; rho(V-scr) V-scr "
             f"hucresindeki {kb['n']} donusturucu uzerinden):\n")
    T(["Duyarlilik", "q", "rho(V-scr) ve diger", "Anahtar"], _m10duy(D8["b2"]["duyarlilik"]))
    dk = f"duyarlilik_delta_{D8['meta']['delta_duyarlilik']}"
    dd = F[dk]
    L.append(f"delta = {dd['delta']} duyarliligi (b2.F_B2.{dk}; betimsel): Holm p {', '.join(_m9p(x_) for x_ in dd['p_holm'])}; "
             f"betigin etiketleri K-a '{dd['karar']['K-a']}', K-b '{dd['karar']['K-b']}', K-c '{dd['karar']['K-c']}'.\n")


_m10("M10.4 B8 ImageNetV2 paneli (betimsel; model tablosu ve ozet olculer)",
     f"`{_M10_B8B}` etiket, model_tablosu_ozet.<m>.{{temiz_dogruluk_yuzde, w_yuzde, sigma, rho, panel_n, hucre}}, ciftler.<k>.{{cift, cnn, "
     f"donusturucu, satir, A_sigma, A_sigma_logit, A_rho, A_omega_log_w, goruntu_bootstrap_ci90, goruntu_bootstrap_ci95, durum}}, "
     f"A_sigma_IN, A_sigma_scr_Liu (tanim, beklenti, ciftler, cift_degerleri, kestirim, goruntu_bootstrap, beklenti_esigi, "
     f"betimsel_etiket, nokta_beklenti_esiginde_ya_da_altinda, iki_cift_farki, not), donusturucu_rho_ayri_ayri, hodge_r_kesifsel; "
     f"`{_M10_B8D}` b2.F_B2.{{K-a.{{D, ciftler, payda_kucuk_tohumlar (0 tabanli indeks)}}, K-b.{{ci90, ci95}}, K-c.log_tau_tur_ici, "
     f"p_ham, p_holm, karar, p_1_sayilan_hesaplanamayan, duyarlilik_delta_<meta.delta_duyarlilik>}}, b2.duyarlilik.{{tam_log, "
     f"yari_logit, yari_oran, panel_jackknife, ikincil_panel}}, b2.model_tablosu.<m>.yari_log, meta.{{delta, delta_duyarlilik}}; "
     f"`{_M10_B8M}/transfer_matrix.json` n_samples, steps, norm, eps_255, temiz_dogruluk, results; "
     f"`{_M10_B8M}/per_sample_<m>_to_<m>.npz` target_adv_wrong, target_clean_correct (denetim); `{_M10_HT8}` modeller.<m>.{{hucre, "
     f"aile, tohum}}; `{_M10_OD}` modeller.<m>.{{model, esik.rb_temiz}}; `{_M10_RB.format('<RobustBench adi>')}` clean_acc, "
     f"autoattack_acc", _m10_4)


# --- M10.5 B10 Mantel ve c_ij --------------------------------------------------------------------
def _m10_5():
    A = _oku(_M10_GA)
    M = {vk: _oku(f"{_M10_G}/mantel_{vk}.json") for vk in _M10_VK}
    sat, tb = [], []
    for vk in _M10_VK:
        for sn in ("ham", "ana_etki_artik"):
            s_ = M[vk]["sinamalar"][sn]
            pt_ = 1 / (s_["perm"] + 1)
            tb.append(s_["p_tek"] == pt_)
            sat.append([vk, sn, s_["K"], s_["cift_sayisi"], sg(s_["istatistik"], 3, True), _m9p(s_["p_tek"]), _m9p(s_["p_iki"]),
                        s_["perm"], _m9p(pt_), s_["tohum"], f"{sg(s_['perm_ort'], 3, True)} / {sg(s_['perm_sd'], 3)}",
                        M[vk]["c_turu"], ", ".join(M[vk]["dislanan"]) or "yok"])
    L.append("Mantel sinamalari (Spearman r, c_ij ile log tau; 'ham' ve model ana etkileri cikarilmis 'ana_etki_artik'; tek yonlu "
             "p birincil; 'p tabani' turetilmis, 1/(perm+1), permutasyon sinamasinin ulasabilecegi en kucuk p):\n")
    T(["Veri kumesi", "Sinama", "K (model)", "Cift sayisi", "r", "Tek yonlu p", "Iki yonlu p", "Permutasyon",
       "p tabani 1/(perm+1) (turetilmis)", "Tohum", "Permutasyon ort / SD", "c turu", "Dislanan model"], sat)
    L.append(f"Tek yonlu p'si p tabanina esit olan sinama: {sum(tb)}/{len(tb)}.\n")
    FB = A["F_B10"]
    fs, dz = [], []
    for s_ in FB["sinamalar"]:
        vk = s_["sinama"].split("-", 1)[1]
        sn = "ana_etki_artik" if s_["sinama"].startswith("H10k") else "ham"
        dz.append(abs(s_["istatistik"] - M[vk]["sinamalar"][sn]["istatistik"]))
        fs.append([s_["sinama"], sg(s_["istatistik"], 3, True), _m9p(s_["p_tek_ham"]), _m9p(s_["p_holm"]), s_["perm"],
                   sg(s_["ongorulen_buyukluk"], 3), _m9e(s_["ongorulen_buyukluk_tuttu"]), s_["karar"]])
    L.append(f"Aile F_B10 (`{_M10_GA}`; aile buyuklugu {FB['aile_buyuklugu']}, Holm):\n")
    T(["Sinama", "Istatistik", "Ham p", "Holm p", "Permutasyon", "Ongorulen buyukluk", "Buyukluk tuttu", "Karar"], fs)
    hk = holm([s_["p_tek_ham"] for s_ in FB["sinamalar"]])
    L.append(f"Karar kurali (JSON): '{FB['kural']}'. Hesaplanamayip p = 1 sayilan: {', '.join(FB['p_1_sayilan']) or 'yok'}. Holm "
             f"denetimi (holm() ile p_tek_ham'dan): en buyuk mutlak fark "
             f"{float(np.max(np.abs(hk - np.asarray([s_['p_holm'] for s_ in FB['sinamalar']])))):.2e}. F_B10 istatistikleri ile "
             f"mantel_<veri>.json sinamalar.{{ham, ana_etki_artik}}.istatistik en buyuk mutlak fark {max(dz):.2e}. Mantel notu "
             f"(JSON): '{M[_M10_VK[0]]['not']}'\n")
    ks, dk = [], []
    for an in ("kismi_omega", "kismi_omega_gradnorm"):
        for vk in _M10_VK:
            s_ = A[f"kesifsel_{an}"][vk]
            dk.append(abs(s_["istatistik"] - M[vk]["sinamalar"][an]["istatistik"]))
            ks.append([an, vk, s_["K"], s_["cift_sayisi"], sg(s_["istatistik"], 3, True), _m9p(s_["p_tek"]), _m9p(s_["p_iki"]),
                       s_["perm"], s_["kovaryat_sayisi"]])
    L.append("Aile disi, kesifsel kismi Mantel sinamalari (F_B10'a ve Holm hesabina girmez; ek on kayit §6.2):\n")
    T(["Sinama", "Veri kumesi", "K", "Cift sayisi", "r", "Tek yonlu p", "Iki yonlu p", "Permutasyon", "Kovaryat sayisi"], ks)
    L.append(f"`{_M10_GA}` kesifsel_* ile mantel_<veri>.json sinamalar.<ad>.istatistik en buyuk mutlak fark {max(dk):.2e}.\n")
    cs, ad_ = [], set()
    for vk in _M10_VK:
        K_ = _oku(f"{_M10_G}/{vk}/kosinus_ozet.json")
        u_ = _m10ust(K_["c_tum"])
        u2 = _m10ust(K_["c_iki_model_dogru"])
        HA = _oku(_M10_HTV[vk])["modeller"]
        eks = [m for m in K_["modeller"] if m not in HA]
        if eks:
            raise ValueError(f"{vk}: hucre tablosunda olmayan model {eks}")
        don = np.array([HA[m]["aile"] != "CNN" for m in K_["modeller"]])
        ad_ |= {HA[m]["aile"] for m in K_["modeller"] if HA[m]["aile"] != "CNN"}
        i_, j_ = np.triu_indices(len(don), 1)
        gr = {"CNN-CNN": ~don[i_] & ~don[j_], "don-don": don[i_] & don[j_], "karma": don[i_] != don[j_]}
        if sum(int(v_.sum()) for v_ in gr.values()) != len(u_):
            raise ValueError(f"{vk}: aile gruplari ust ucgeni kapsamiyor")
        cs.append([vk, K_["n"], len(K_["modeller"]), len(u_), sg(float(u_.mean()), 3), f"{sg(float(u_.min()), 3)}; {sg(float(u_.max()), 3)}",
                   sg(float(u2.mean()), 3), K_["nan_kosinus_sayisi"]]
                  + [f"{sg(float(u_[v_].mean()), 3)} ({int(v_.sum())})" if v_.any() else "- (0)" for v_ in gr.values()])
    L.append("c_ij ozetleri (kosinus_ozet.json; ortalama, en kucuk ve en buyuk turetilmis, c matrisinin ust ucgeni; aile gruplari "
             "turetilmis: c_tum ust ucgeni, aile atamasi hucre tablolarinin aile alanindan "
             f"({', '.join(f'{vk} `{_M10_HTV[vk]}`' for vk in _M10_VK)}); donusturucu = aile alani CNN olmayan model "
             f"({', '.join(sorted(ad_))}); parantez icinde cift sayisi):\n")
    T(["Veri kumesi", "n goruntu", "Model sayisi", "Cift sayisi", "c_ij ort (tum goruntu)", "c_ij en kucuk; en buyuk",
       "c_ij ort (iki model dogru)", "NaN kosinus", "CNN-CNN ort (n) (turetilmis)", "Donusturucu-donusturucu ort (n) (turetilmis)",
       "Karma ort (n) (turetilmis)"], cs)
    L.append(f"Tanim (JSON): '{_oku(f'{_M10_G}/{_M10_VK[0]}/kosinus_ozet.json')['tanim']}'.\n")


_m10("M10.5 B10 girdi gradyani kosinusu ile log tau (Mantel, aile F_B10)",
     f"`{_M10_G}/mantel_<veri>.json` c_turu, dislanan, not, sinamalar.{{ham, ana_etki_artik, kismi_omega, kismi_omega_gradnorm}}."
     f"{{K, cift_sayisi, istatistik, p_tek, p_iki, perm, tohum, perm_ort, perm_sd}}; `{_M10_GA}` F_B10.{{sinamalar.<k>.{{sinama, "
     f"istatistik, p_tek_ham, p_holm, perm, ongorulen_buyukluk, ongorulen_buyukluk_tuttu, karar}}, aile_buyuklugu, p_1_sayilan, "
     f"kural}}, kesifsel_kismi_omega.<veri>, kesifsel_kismi_omega_gradnorm.<veri>; `{_M10_G}/<veri>/kosinus_ozet.json` n, "
     f"modeller, c_tum, c_iki_model_dogru, nan_kosinus_sayisi, tanim; `{_M9_HT}`, `{_M10_HT9}`, `{_M10_HT8}` modeller.<m>.aile "
     f"(aile gruplari icin)", _m10_5)


# --- M10.6 Butunluk ------------------------------------------------------------------------------
def _m10_6():
    kay, kd = _m10ek()
    kod = _m10sp_kod()
    J = {"B9": _oku(_M10_B9), "B9s": _oku(_M10_B9S), "B9w": _oku(_M10_B9W), "B8": _oku(_M10_B8D), "B8b": _oku(_M10_B8B),
         "B10": _oku(_M10_GA)}
    AD = {"B9": "b9_dondurulmus_b2.json", "B9s": "b9_sarmalayici_b2.json", "B9w": "b9_sarmalayici_b2.json.sarmalayici.json",
          "B8": "b8_dondurulmus_b2.json", "B8b": "b8_betimsel.json", "B10": "b10_aile.json"}
    TM8 =_oku(f"{_M10_B8M}/transfer_matrix.json")
    MN = {vk: _oku(f"{_M10_G}/mantel_{vk}.json") for vk in _M10_VK}
    KO = {vk: _oku(f"{_M10_G}/{vk}/kosinus_ozet.json") for vk in _M10_VK}

    def satir(rel, kayit_yeri, kayit, js, govde=False):
        hs = _m9sha(rel, govde)
        jv = [v_ for _, v_ in js]
        jt = all(v_ == hs for v_ in jv)
        L_ = (f"`{rel}`" + (" govdesi (ilk satirdan '## Dondurma eki' basligina kadar)" if govde else ""))
        return [L_, kayit_yeri, kayit or "bulunamadi", hs,
                ("; ".join(f"{a_} {'ayni' if v_ == hs else 'FARKLI'}" for a_, v_ in js) if js else "-"),
                "UYUSUYOR" if (kayit == hs and jt) else "UYUSMUYOR"]

    if kd is None:
        _M10_YOK.append("Ek on kayit Dondurma eki (d) govde sha256 kaydi")
    st = [satir(_M10_EK, "ek Dondurma eki (d)", kd, [], govde=True)]
    st.append(satir(_M9_BETIK, "ek Dondurma eki (a)", kay.get(_M9_BETIK),
                    [(f"{AD['B9']} meta.betik_sha256", J["B9"]["meta"]["betik_sha256"]),
                     (f"{AD['B8']} meta.betik_sha256", J["B8"]["meta"]["betik_sha256"])]
                    + [(f"{AD[a_]} meta.dondurulmus_betik_sha256_dogrulandi", J[a_]["meta"]["dondurulmus_betik_sha256_dogrulandi"])
                       for a_ in ("B9w", "B8b", "B10")]))
    st.append(satir(_M9_HT, "ek Dondurma eki (a)", kay.get(_M9_HT), []))
    st.append(satir(_M10_HT9, "ek Dondurma eki (b)", kay.get(_M10_HT9),
                    [(f"{AD[a_]} meta.hucre_tablosu_sha256", J[a_]["meta"]["hucre_tablosu_sha256"]) for a_ in ("B9", "B9w")]))
    st.append(satir(_M10_HT8, "ek Dondurma eki (b)", kay.get(_M10_HT8),
                    [(f"{AD[a_]} meta.hucre_tablosu_sha256", J[a_]["meta"]["hucre_tablosu_sha256"]) for a_ in ("B8", "B8b")]))
    st.append(satir(_M10_OZG, "ek Dondurma eki (c)", kay.get(_M10_OZG),
                    [(f"{AD[a_]} meta.ozgun_matris_betigi_sha256_simdi", J[a_]["meta"]["ozgun_matris_betigi_sha256_simdi"])
                     for a_ in ("B9w", "B8b", "B10")]))
    jsk = {"experiments/q1_ek_transfer_matrix.py": [("B8 matrisi transfer_matrix.json ek_betik_sha256", TM8.get("ek_betik_sha256"))],
           "experiments/q1_ek_ayrisim.py": [(f"{AD[a_]} meta.sarmalayici_sha256", J[a_]["meta"]["sarmalayici_sha256"])
                                            for a_ in ("B9w", "B8b", "B10")],
           "experiments/q1_ek_gradyan_kosinus.py": ([(f"mantel_{vk} betik_sha256", MN[vk]["betik_sha256"]) for vk in _M10_VK]
                                                    + [(f"{vk} kosinus_ozet betik_sha256", KO[vk]["betik_sha256"]) for vk in _M10_VK])}
    if not kod:
        _M10_YOK.append(f"Sapma kaydi kod eki ozetleri ({_M10_SP})")
    for rel, h_ in kod.items():
        st.append(satir(rel, "sapma kaydi, kod eki", h_, jsk.get(rel, [])))
    sp = _m10metin(_M10_SP)
    m_o = _m8re.search(_m8re.escape(_M10_OD) + r"`[^(`\n]*\(SHA-256 `([0-9a-f]{64})`", sp)
    st.append(satir(_M10_OD, "sapma kaydi (B8 on isleme denetimi notu)", m_o.group(1) if m_o else None, []))
    T(["Dosya", "Kayit yeri", "Kayitli sha256", "Dosyadan hesaplanan (bu betik)", "JSON kayitlari", "Durum"], st)

    gs = []
    for blok, rel, md in (("B9", _M10_B9, _M10_B9M), ("B8", _M10_B8D, _M10_B8M)):
        gi = _oku(rel)["veri"]["girdi_sha256"]
        fark = [p_ for p_, h_ in gi.items() if _m9sha(p_) != h_]
        gs.append(f"{blok} veri.girdi_sha256 ({len(gi)} dosya, `{md}` matrisi ve per_sample npz): yeniden hesaplananla farkli "
                  f"{len(fark)}" + (f" ({', '.join(fark[:5])})" if fark else ""))
    for vk in _M10_VK:
        g_ = J["B10"]["girdiler"][vk]
        gs.append(f"b10_aile girdiler.{vk} ({g_['dosya']}) {'ayni' if _m9sha(g_['dosya']) == g_['sha256'] else 'FARKLI'}")
        gs.append(f"mantel_{vk} kosinus_ozet_sha256 ({MN[vk]['kosinus_ozet']}) "
                  f"{'ayni' if _m9sha(MN[vk]['kosinus_ozet']) == MN[vk]['kosinus_ozet_sha256'] else 'FARKLI'}")
    gs.append(f"`{_M10_B9W}` meta.dondurulmus_cikti_sha256 ile `{_M10_B9S}` "
              f"{'ayni' if _m9sha(_M10_B9S) == J['B9w']['meta']['dondurulmus_cikti_sha256'] else 'FARKLI'}")
    a_, b_ = json.loads(json.dumps(J["B9"])), json.loads(json.dumps(J["B9s"]))
    a_["meta"].pop("uretildi_utc", None)
    b_["meta"].pop("uretildi_utc", None)
    gs.append(f"`{_M10_B9}` ile `{_M10_B9S}` meta.uretildi_utc disinda {'AYNI' if a_ == b_ else 'FARKLI'}")
    L.append("Girdi ve cikti ozetleri: " + "; ".join(gs) + ".\n")
    L.append("JSON uretim zamanlari: " + "; ".join(f"{AD[a_]} {d_['meta']['uretildi_utc']}" for a_, d_ in J.items())
             + "; " + "; ".join(f"mantel_{vk} {MN[vk]['uretildi_utc']}" for vk in _M10_VK)
             + f". numpy (JSON meta): {', '.join(sorted({d_['meta']['numpy'] for d_ in J.values()}))}.\n")
    # Bulunamayanlar satiri butun M10 alt bolumleri kosulduktan sonra doldurulur.
    _M10_YOK_YER.append(len(L))
    L.append("")


_m10("M10.6 Butunluk (ek on kayit govdesi, hucre tablolari, dondurulmus ve ek betikler)",
     f"`{_M10_EK}` Dondurma eki (a)-(c) kod bloklari ve (d) govde ozeti (metinden); `{_M10_SP}` Ek B8-B10 'kod eki' kod blogu ve "
     f"on isleme denetimi kaydi (metinden); `{_M10_B9}`, `{_M10_B8D}` meta.{{betik_sha256, hucre_tablosu_sha256, uretildi_utc, numpy}}, "
     f"veri.girdi_sha256; `{_M10_B9W}`, `{_M10_B8B}`, `{_M10_GA}` meta.{{sarmalayici_sha256, dondurulmus_betik_sha256_dogrulandi, "
     f"ozgun_matris_betigi_sha256_simdi, hucre_tablosu_sha256, dondurulmus_cikti_sha256}}, girdiler; `{_M10_B8M}/transfer_matrix.json` "
     f"ek_betik_sha256; `{_M10_G}/mantel_<veri>.json` betik_sha256, kosinus_ozet, kosinus_ozet_sha256, uretildi_utc; "
     f"`{_M10_G}/<veri>/kosinus_ozet.json` betik_sha256; dosya sha256'lari bu betikte hashlib ile hesaplanir", _m10_6)

for _i10 in _M10_YOK_YER:
    L[_i10] = ("Bu bolumde (M10.1-M10.6) JSON'da bulunamayip 'bulunamadi' yazilan kalemler: "
               + ("; ".join(_M10_YOK) if _M10_YOK else "yok") + ".\n")


# --- M10.7 Ek yer tutuculari icin kaynak veriler (2026-10-31, kod-mimar) ---------------------------
# 07_appendix.tex'teki iki '% TODO(foy)' kalemi icin: (a) saldiri tohumu tekrarinin SD'si (Ek, varyans
# kaynaklari paragrafi), (b) CIFAR-100 C3 hedeflerinin temiz hatalari (Ek, CIFAR-100 kayitli ongoruleri).
# Mevcut bolumlere dokunmaz; bu blok cikarilinca foy onceki surumle bayt bayt aynidir. Karantina
# yollarindan OKUNMAZ (c1_statval ve q1 gecerli yollardir).
_M107_SV = "results/c1_statval/statistical_validation.json"
_M107_SVB = "experiments/run_all_analyses_run2.py"
_M107_C3 = "results/q1/c3_precision.json"
_M107_B9M = f"{_M10_B9M}/transfer_matrix.json"
_M107_YOK = []
_M107_YOK_YER = []


def _m107g(d, yol, etiket):
    """Anahtar yolunu izler; yoksa None doner ve kalemi M10.7 bulunamayanlar listesine yazar."""
    x = d
    for k_ in yol:
        if isinstance(x, dict) and k_ in x:
            x = x[k_]
        else:
            _M107_YOK.append(etiket)
            return None
    return x


def _m107_7():
    sv = _oku(_M107_SV)
    svb = _m10metin(_M107_SVB)
    i_ = svb.find("def run_statistical_validation")
    govde = svb[i_:] if i_ >= 0 else ""
    m_st = _m8re.search(r"^STEPS\s*=\s*(\d+)", svb, _m8re.M)
    m_al = _m8re.search(r"^ALPHA\s*=\s*([^\n#]+)", svb, _m8re.M)
    std_ddof0 = bool(_m8re.search(r"'robust_std':\s*float\(np\.std\(robust_accs\)\)", govde))
    seeds = _m107g(sv, ("seeds",), f"{_M107_SV} seeds")
    n_s = _m107g(sv, ("n_samples",), f"{_M107_SV} n_samples")
    eps = _m107g(sv, ("eps",), f"{_M107_SV} eps")
    mp = _m107g(sv, ("model_paths",), f"{_M107_SV} model_paths") or {}
    L.append("(a) Saldiri tohumu tekrari (saldiri baslatma rastgeleligi; egitim tohumu degil). Ayni kontrol noktasi cifti, "
             f"test kumesinin ilk {n_s} goruntusu (yukleyici karistirmaz), saldiri tohumlari "
             f"{', '.join(str(s_) for s_ in seeds) if seeds else 'bulunamadi'}, eps x 255 = "
             f"{_m9s(None if eps is None else eps * 255, 2)}; saldiri PGD, adim sayisi `{_M107_SVB}` STEPS = "
             f"{m_st.group(1) if m_st else 'bulunamadi'}, adim boyu ALPHA = {m_al.group(1).strip() if m_al else 'bulunamadi'} "
             f"(kaynak metninden). Uretim zamani (JSON): {sv.get('timestamp', 'bulunamadi')}; model_variant alani: "
             f"'{sv.get('model_variant', 'bulunamadi')}'.\n")
    rs = []
    for r_ in _m107g(sv, ("results",), f"{_M107_SV} results") or []:
        n_r = r_.get("n_runs")
        sd0 = r_.get("robust_std")
        sd1 = (None if (sd0 is None or not n_r or n_r < 2) else sd0 * np.sqrt(n_r / (n_r - 1)))
        c0 = r_.get("clean_std")
        rs.append([r_.get("model", "bulunamadi"), f"`{mp.get(r_.get('model'), 'bulunamadi')}`", n_r, r_.get("n_samples"),
                   _m9s(r_.get("clean_mean"), 2), _m9s(c0, 2), _m9s(r_.get("robust_mean"), 2),
                   _m9s(sd0, 2), _m9s(sd0, 4), _m9s(sd1, 2), _m9s(sd1, 4)])
    T(["Model", "Kontrol noktasi", "Saldiri tohumu sayisi", "Goruntu", "Temiz ort (%)", "Temiz SD (puan)",
       "Gurbuz ort (%)", "Gurbuz SD, artefakt alani (puan)", "Gurbuz SD, artefakt alani (4 ondalik)",
       "Gurbuz SD, ddof=1 (turetilmis; puan)", "Gurbuz SD, ddof=1 (turetilmis; 4 ondalik)"], rs)
    L.append("SD tanimi: artefakttaki clean_std ve robust_std alanlari `np.std` varsayilanidir (ddof = 0, n = 3 saldiri "
             f"tohumu); kaynak metninde `'robust_std': float(np.std(robust_accs))` satiri: {'VAR' if std_ddof0 else 'YOK'}. "
             "'ddof=1' sutunu turetilmistir: SD x sqrt(n / (n - 1)). Foy basligindaki '+- standart sapma' tanimi egitim "
             "tohumu SD'sidir (ddof = 1); bu alt bolumdeki SD saldiri tohumu SD'sidir ve onunla karistirilmamalidir. "
             "Kontrol noktalari ilk C1 ciftidir (1001 / 2001); temiz dogruluk ilk 1000 goruntudendir ve Tablo I'in tam test "
             "kumesi ortalamasiyla karsilastirilamaz.\n")

    c3 = _oku(_M107_C3)
    v_ = _m107g(c3, ("veri_kumeleri", "cifar100"), f"{_M107_C3} veri_kumeleri.cifar100") or {}
    hd = _m107g(v_, ("hedefler",), f"{_M107_C3} veri_kumeleri.cifar100.hedefler") or []
    he = _m107g(v_, ("hedef_temiz_hatasi",), f"{_M107_C3} veri_kumeleri.cifar100.hedef_temiz_hatasi") or []
    hs = v_.get("hedef_sapmasi") or []
    xa = _m107g(v_, ("X_AYRIKLIGI",), f"{_M107_C3} veri_kumeleri.cifar100.X_AYRIKLIGI") or {}
    # Capraz denetim: B9 matrisinde ayni C1 CIFAR-100 modellerinin hedef temiz dogrulugu (M10.3 'Temiz (%)' sutunu).
    TM = _oku(_M107_B9M)

    def _b9temiz(on_ek):
        d_ = {}
        for k_, r_ in TM["results"].items():
            h_ = k_.split("->", 1)[1]
            if h_.startswith(on_ek):
                d_.setdefault(h_, r_["target_clean_acc"])
        return d_

    b9 = {"ResNet18_AT": _b9temiz("C100_ResNet18_AT_s"), "ViT_Tiny_AT": _b9temiz("C100_ViT_Tiny_AT_s")}
    L.append(f"(b) CIFAR-100 C3 on-kestirimi hedefleri (`{_M107_C3}` veri_kumeleri.cifar100; kosegen disi yon sayisi "
             f"{v_.get('n_kosegen_disi', 'bulunamadi')}, ayri hedef sayisi {v_.get('n_ayri_hedef', 'bulunamadi')}). Hedef temiz "
             "hatasi = 100 - hedef temiz dogrulugu (%); hedef sapmasi = ham - kosullu (puan), JSON'daki hedef sirasiyla:\n")
    rs = []
    for i_, h_ in enumerate(hd):
        b_ = b9.get(h_, {})
        tur = (f"{_m9s(100.0 - float(np.mean(list(b_.values()))), 2)} ({len(b_)} model; fark "
               f"{_m9s(abs(he[i_] - (100.0 - float(np.mean(list(b_.values()))))), 2)} puan)") if (b_ and i_ < len(he)) else "-"
        rs.append([h_, _m9s(he[i_], 2) if i_ < len(he) else "bulunamadi", _m9s(hs[i_], 2) if i_ < len(hs) else "-", tur])
    T(["Hedef", "Hedef temiz hatasi (%)", "Hedef sapmasi (puan)",
       "Capraz denetim: 100 - B9 matrisi hedef temiz dogrulugu ort (turetilmis)"], rs)
    srt = xa.get("hedef_hatalari_sirali")
    L.append(f"Hedef hatalari sirali: {' / '.join(_m9s(x_, 2) for x_ in srt) if srt else 'bulunamadi'}; en kucuk ara "
             f"{_m9s(xa.get('en_kucuk_ara'), 2)} puan; aralik {_m9s(xa.get('aralik'), 2)} puan; en kucuk ara / aralik "
             f"{_m9s(xa.get('en_kucuk_ara_aralik_orani'), 4)}; iki hedef cakisiyor: {_m9e(xa.get('IKI_HEDEF_CAKISIYOR'))}; etkin "
             f"ayri x degeri {xa.get('etkin_ayri_x_degeri', 'bulunamadi')}. Capraz denetim sutunu B9 matrisinin "
             f"(`{_M107_B9M}` results.*->C100_<model>_s*.target_clean_acc) uc tohum ortalamasidir; WRN_28_10 hedefi B9 "
             "matrisinde yoktur. Ayni egim ve r bu foyde M8.2 'CIFAR-100 Linf' satirindadir.\n")
    _M107_YOK_YER.append(len(L))
    L.append("")


_m10("M10.7 Ek yer tutuculari icin kaynak veriler (saldiri tohumu tekrari; CIFAR-100 C3 hedef temiz hatalari)",
     f"`{_M107_SV}` seeds, n_samples, eps, model_variant, timestamp, model_paths, results.<i>.{{model, clean_mean, clean_std, "
     f"robust_mean, robust_std, n_runs, n_samples}}; `{_M107_SVB}` STEPS, ALPHA ve run_statistical_validation govdesi (kaynak "
     f"metninden); `{_M107_C3}` veri_kumeleri.cifar100.{{n_kosegen_disi, n_ayri_hedef, hedefler, hedef_temiz_hatasi, "
     f"hedef_sapmasi, X_AYRIKLIGI}}; `{_M107_B9M}` results.*.target_clean_acc (capraz denetim)", _m107_7)

for _i107 in _M107_YOK_YER:
    L[_i107] = ("Bu alt bolumde (M10.7) JSON'da bulunamayip 'bulunamadi' yazilan kalemler: "
                + ("; ".join(_M107_YOK) if _M107_YOK else "yok") + ".\n")

# <<< M10.7 SONU

# <<< M10 SONU (ek bloklar B8-B10)

# ===========================================================================
# GENISLETME 2026-10-31 (M11): hakem paneli sonrasi masa cozumlemeleri.
# M11.1 ON_KAYIT §5 hiyerarsik bootstrap duyarliligi (K-a, K-b yeni; K-c
# yeniden uretim), M11.2 ek on kayit §6.4 S10-3 (aile gostergeli kismi Mantel),
# M11.3 kesifsel. Her sayi results/q1/konsey_ek_masa/*.json ve
# results/q1/konsey_b10_gradyan/mantel_<veri>.json dosyalarindan okunur; yorum
# yazilmaz. Mevcut bolumlere dokunulmaz; bolum M10'dan sonra, 'Sabit
# dizgeler'den once gelir.
# ===========================================================================
_M11_D = "results/q1/konsey_ek_masa"
_M11_BS = {"cifar10": f"{_M11_D}/bootstrap_cifar10.json", "cifar100": f"{_M11_D}/bootstrap_cifar100.json"}
_M11_MA = f"{_M11_D}/mantel_aile.json"
_M11_KS = f"{_M11_D}/kesifsel.json"
_M11_BETIK = "experiments/q1_ek_masa.py"
_M11_VK = ("cifar10", "cifar100", "imagenetv2")
_M11_YOK = []
_M11_YOK_YER = []


def _m11(ad, kaynak, fn):
    L.append(f"\n### {ad}\n")
    try:
        fn()
    except (KeyError, TypeError, IndexError, ValueError, OSError, ZeroDivisionError, AttributeError) as e_:
        _hata(e_)
    L.append(f"_Kaynak: {kaynak}_\n")


def _m11g(d, yol, etiket):
    """Anahtar yolunu izler; yoksa None doner ve kalemi M11 bulunamayanlar listesine yazar."""
    x = d
    for k_ in yol:
        if isinstance(x, dict) and k_ in x:
            x = x[k_]
        else:
            _M11_YOK.append(etiket)
            return None
    return x


def _m11c(x):
    return "bulunamadi" if x is None else f"{float(x):.4f}"


def _m11meta(J, rel):
    m_ = J["meta"]
    return (f"`{rel}` meta: betik_sha256 {m_['betik_sha256']} (dosyadan hesaplanan {_m9sha(_M11_BETIK)}; "
            f"{'AYNI' if m_['betik_sha256'] == _m9sha(_M11_BETIK) else 'FARKLI'}); dondurulmus_betik_sha256_dogrulandi "
            f"{m_['dondurulmus_betik_sha256_dogrulandi']}; uretildi_utc {m_['uretildi_utc']}; numpy {m_['numpy']}; "
            f"scipy {m_['scipy']}; girdi dosyasi sayisi (girdi_sha256) {len(m_['girdi_sha256'])}.")


sec("M11: Hakem paneli sonrasi masa cozumlemeleri (2026-10-31)",
    f"{_M11_BS['cifar10']}; {_M11_BS['cifar100']}; {_M11_MA}; {_M11_KS}; "
    f"results/q1/konsey_b10_gradyan/mantel_<veri>.json (yalniz yeniden uretim karsilastirmasi); "
    f"{_M11_BETIK} (yalniz sha256)")
L.append("Hakem paneli sonrasi 31.10.2026'da uretilen uc masa cozumlemesi. Her alt bolum kendi JSON'undan okunur ve "
         "altinda kaynak dosya ile anahtar yollari yazilidir; etiketler JSON'un 'etiket' alanindandir. Yuvarlama: "
         "oranlar, log olcekli nicelikler ve korelasyonlar 3 ondalik, c_ij 4 ondalik, p degerleri bilimsel gosterim.\n")


# --- M11.1 Hiyerarsik bootstrap ------------------------------------------------------------
def _m11_1():
    J = {v: _oku(r) for v, r in _M11_BS.items()}
    L.append(f"Etiket (`etiket`): {_m11g(J['cifar10'], ('etiket',), 'bootstrap_cifar10 etiket')}.\n")
    L.append(f"Tanim (`tanim`): {_m11g(J['cifar10'], ('tanim',), 'bootstrap_cifar10 tanim')}\n")
    for v, j in J.items():
        m_ = j["meta"]
        L.append(_m11meta(j, _M11_BS[v]) + f" Veri {m_['veri']} ({m_['blok']}); matris {m_['matris_dizini']}; hucre "
                 f"tablosu {m_['hucre_tablosu']}; dondurulmus cikti {m_['dondurulmus_cikti']}; B {m_['B']}; bootstrap "
                 f"tohumu {m_['bootstrap_tohum']} ({m_['tohum_kaynagi']}); n_goruntu {m_['n_goruntu']}.\n")
    st = []
    for v, j in J.items():
        ka, kb, kc = j["K-a"], j["K-b"], j["K-c"]
        bo, bv = ka["bootstrap"], kb["bootstrap"]
        st.append([v, "K-a ort q", _m9s(ka["nokta_ort_q"]), _m9a(ka["t_ci90"]), _m9a(ka["t_ci95"]), _m9a(bo["ci90"]),
                   _m9a(bo["ci95"]), _m9s(bo["sd"]), f"{_m9p(bo['p_tek_H0_q_le_0.5'])} (H0: ort q <= 0,50)",
                   "K-a.{nokta_ort_q, t_ci90, t_ci95, bootstrap}"])
        cv = ka["cift_duzeyi_varyant"]
        st.append([v, "K-a ort q, cift duzeyi varyant", "", "", "", _m9a(cv["ci90"]), _m9a(cv["ci95"]), _m9s(cv["sd"]), "",
                   "K-a.cift_duzeyi_varyant"])
        st.append([v, "K-b ort rho(V-scr)", _m9s(kb["nokta_ort_rho"], plus=True), _m9a(kb["t_ci90"], plus=True),
                   _m9a(kb["t_ci95"], plus=True), _m9a(bv["ci90"], plus=True), _m9a(bv["ci95"], plus=True), _m9s(bv["sd"]),
                   f"TOST {_m9p(bv['tost_p'])} (alt {_m9p(bv['tost_p_alt'])}, ust {_m9p(bv['tost_p_ust'])}; delta 0,06: "
                   f"{_m9p(bv['tost_p_delta_0.06'])}); t TOST {_m9p(kb['t_tost_p'])}",
                   "K-b.{nokta_ort_rho, t_ci90, t_ci95, t_tost_p, bootstrap}"])
        cv = kb["cift_duzeyi_varyant"]
        st.append([v, "K-b ort rho(V-scr), cift duzeyi varyant", "", "", "", _m9a(cv["ci90"], plus=True),
                   _m9a(cv["ci95"], plus=True), _m9s(cv["sd"]), "", "K-b.cift_duzeyi_varyant"])
        st.append([v, "K-c Delta_w (yeniden uretim)", _m9s(kc["Delta_w"], plus=True), "", "",
                   _m9a(kc["yeniden_bootstrap"]["ci90"], plus=True), _m9a(kc["yeniden_bootstrap"]["ci95"], plus=True), "",
                   f"{_m9p(kc['yeniden_bootstrap']['p'])} (H0: Delta_w <= 0)", "K-c.{Delta_w, yeniden_bootstrap}"])
        st.append([v, "K-c Delta_w (dondurulmus JSON)", "", "", "", _m9a(kc["dondurulmus_bootstrap"]["ci90"], plus=True),
                   _m9a(kc["dondurulmus_bootstrap"]["ci95"], plus=True), "", _m9p(kc["dondurulmus_bootstrap"]["p"]),
                   "K-c.dondurulmus_bootstrap"])
    T(["Veri", "Nicelik", "Nokta", "t %90", "t %95", "Hiyerarsik bootstrap %90", "Hiyerarsik bootstrap %95", "Bootstrap SD",
       "Bootstrap p", "Anahtar"], st)
    st = []
    for v, j in J.items():
        k_ = j["karar"]
        for s_ in ("K-a", "K-b", "K-c"):
            a_, b_ = k_["karsilastirma"][s_], k_["delta_0.06"]["karsilastirma"][s_]
            st.append([v, s_, a_["dondurulmus"], a_["bootstrap_araligiyla"], _m9e(a_["degisti"]), b_["dondurulmus"],
                       b_["bootstrap_araligiyla"], _m9e(b_["degisti"])])
    L.append("Karar karsilastirmasi (`karar.karsilastirma`, `karar.delta_0.06.karsilastirma`; kural: "
             f"'{_m11g(J['cifar10'], ('karar', 'kural'), 'bootstrap karar.kural')}'):\n")
    T(["Veri", "Sinama", "Dondurulmus karar (delta 0,10)", "Bootstrap araligiyla (delta 0,10)", "Degisti",
       "Dondurulmus karar (delta 0,06)", "Bootstrap araligiyla (delta 0,06)", "Degisti"], st)
    for v, j in J.items():
        k_, d_ = j["karar"], j["dogrulama"]
        nf = max(d_["nokta_kestirimleri_dondurulmus_json_ile_maks_fark"].values())
        kcf = d_["K-c_yeniden_uretim_maks_fark"]
        L.append(f"{v}: Holm p bootstrap p'lerinden (K-a, K-b, K-c) {', '.join(_m9p(x) for x in k_['p_holm_bootstrap'])}; "
                 f"dondurulmus Holm p {', '.join(_m9p(x) for x in k_['p_holm_dondurulmus'])}; degisen sinama "
                 f"{k_['degisen'] or 'yok'} (delta 0,06: {k_['delta_0.06']['degisen'] or 'yok'}). Nokta kestirimleri ile "
                 f"dondurulmus JSON en buyuk mutlak fark {nf:.2e} (nokta_esit {_m9e(d_['nokta_esit'])}); K-c yeniden uretim "
                 f"farki ci90 {kcf['ci90']:.2e}, ci95 {kcf['ci95']:.2e}, p {kcf['p_tek_H0_Delta_le_0']:.2e}, yeniden cekilen "
                 f"tek tohumlu ornek {j['K-c']['yeniden_bootstrap']['yeniden_cekilen']} (dondurulmus "
                 f"{j['K-c']['dondurulmus_bootstrap']['yeniden_cekilen']}; K-c_esit {_m9e(d_['K-c_esit'])}); bootstrap "
                 f"kopyalarinda bir ciftte D <= 0,10 olan kopya sayisi {j['K-a']['bootstrap']['D_le_0.10_kopya_sayisi']} "
                 f"(cift duzeyi varyant {j['K-a']['cift_duzeyi_varyant']['D_le_0.10_kopya_sayisi']}); bootstrap p tabani "
                 f"1/(B+1) (turetilmis) {_m9p(1 / (j['meta']['B'] + 1))}.\n")


_m11("M11.1 Hiyerarsik bootstrap duyarliligi: K-a, K-b ve K-c (CIFAR-10 B2, CIFAR-100 B9)",
     f"`{_M11_BS['cifar10']}`, `{_M11_BS['cifar100']}` etiket, tanim, meta.{{betik_sha256, dondurulmus_betik_sha256_dogrulandi, "
     f"uretildi_utc, numpy, scipy, girdi_sha256, veri, blok, matris_dizini, hucre_tablosu, dondurulmus_cikti, B, bootstrap_tohum, "
     f"tohum_kaynagi, n_goruntu}}; K-a.{{nokta_ort_q, t_ci90, t_ci95, bootstrap, cift_duzeyi_varyant}}; K-b.{{nokta_ort_rho, "
     f"t_ci90, t_ci95, t_tost_p, bootstrap, cift_duzeyi_varyant}}; K-c.{{Delta_w, yeniden_bootstrap, dondurulmus_bootstrap}}; "
     f"karar.{{kural, karsilastirma, degisen, p_holm_bootstrap, p_holm_dondurulmus, delta_0.06}}; dogrulama.{{nokta_kestirimleri_"
     f"dondurulmus_json_ile_maks_fark, nokta_esit, K-c_yeniden_uretim_maks_fark, K-c_esit}}; `{_M11_BETIK}` sha256 bu betikte "
     f"hashlib ile", _m11_1)


# --- M11.2 S10-3 ---------------------------------------------------------------------------
def _m11_2():
    J = _oku(_M11_MA)
    L.append(f"Etiket (`etiket`): {_m11g(J, ('etiket',), 'mantel_aile etiket')}.\n")
    L.append(f"Tanim (`tanim_S10_3`): {_m11g(J, ('tanim_S10_3',), 'mantel_aile tanim_S10_3')}\n")
    L.append(f"Ek §6.2 yeniden uretim tanimi (`tanim_6_2_yeniden_uretim`): "
             f"{_m11g(J, ('tanim_6_2_yeniden_uretim',), 'mantel_aile tanim_6_2_yeniden_uretim')}\n")
    L.append(_m11meta(J, _M11_MA) + f" Permutasyon {J['meta']['perm']}; tohum {J['meta']['tohum']} "
             f"({J['meta']['tohum_kaynagi']}).\n")
    st = []
    for v in _M11_VK:
        d_ = J["veri"][v]
        s_, h_ = d_["S10_3"], d_["S10_3_duyarlilik_ham_c_permutasyonu"]
        ct = d_["cift_turu_sayilari"]
        st.append([v, d_["K"], d_["cift_sayisi"], f"{ct['CNN-CNN']} / {ct['donusturucu-donusturucu']} / {ct['karma']}",
                   f"{d_['tasarim_rank']['rank_X_ana_etki']} / {d_['tasarim_rank']['rank_X_ana_etki_aile']}",
                   _m9s(s_["istatistik"], plus=True), _m9p(s_["p_tek"]), _m9p(s_["p_iki"]),
                   f"{_m9s(s_['perm_ort'], plus=True)} / {_m9s(s_['perm_sd'])}", _m9s(h_["istatistik"], plus=True),
                   _m9p(h_["p_tek"]), s_["perm"], s_["tohum"], _m9p(1 / (s_["perm"] + 1))])
    T(["Veri kumesi", "K (model)", "Cift sayisi", "Cift turu CNN-CNN / donusturucu-donusturucu / karma",
       "Tasarim rank (ana etki / ana etki + aile)", "S10-3 r", "Tek yonlu p", "Iki yonlu p", "Permutasyon ort / SD",
       "Duyarlilik r (ham c permutasyonu)", "Duyarlilik tek yonlu p", "Permutasyon", "Tohum", "p tabani 1/(perm+1) (turetilmis)"],
      st)
    st = []
    for v in _M11_VK:
        d_ = J["veri"][v]
        mn = _oku(f"results/q1/konsey_b10_gradyan/mantel_{v}.json")
        for s_ in ("ham", "ana_etki_artik"):
            y_, e_, k_ = d_["yeniden_uretim_6_2"][s_], mn["sinamalar"][s_], d_["mantel_json_karsilastirma"][s_]
            st.append([v, s_, _m9s(y_["istatistik"], plus=True), _m9p(y_["p_tek"]), _m9s(e_["istatistik"], plus=True),
                       _m9p(e_["p_tek"]), f"{abs(y_['istatistik'] - e_['istatistik']):.2e}", f"{k_['maks_fark']:.2e}",
                       _m9e(k_["esit_1e-6"])])
    L.append("Ek §6.2 istatistiklerinin bagimsiz yeniden uretimi (`veri.<veri>.yeniden_uretim_6_2`) ve "
             "`results/q1/konsey_b10_gradyan/mantel_<veri>.json` sinamalar.<sinama> ile karsilastirma:\n")
    T(["Veri kumesi", "Sinama", "r (yeniden)", "Tek yonlu p (yeniden)", "r (mantel JSON)", "Tek yonlu p (mantel JSON)",
       "|fark| r (bu betik)", "En buyuk |fark| (istatistik, p_tek, p_iki, perm_ort, perm_sd; JSON)", "Esit (1e-6)"], st)
    L.append(f"Tolerans {J['tolerans']}; yeniden_uretim_hepsi_esit_1e-6 {_m9e(J.get('yeniden_uretim_hepsi_esit_1e-6'))}; "
             f"c ve log tau matris simetrisi en buyuk asimetri: "
             + "; ".join(f"{v} c {J['veri'][v]['simetri']['c_maks_asimetri']:.1e}, log tau "
                         f"{J['veri'][v]['simetri']['log_tau_maks_asimetri']:.1e}" for v in _M11_VK) + ".\n")
    L.append("Model gruplari (`veri.<veri>.modeller`, `.aile`, `.grup`): "
             + "; ".join(f"{v}: donusturucu = " + ", ".join(m_ for m_, g_ in zip(J['veri'][v]['modeller'], J['veri'][v]['grup'])
                                                           if g_ == "donusturucu") for v in _M11_VK) + ".\n")


_m11("M11.2 S10-3: aile gostergeli kismi Mantel (ek on kayit §6.4)",
     f"`{_M11_MA}` etiket, tanim_S10_3, tanim_6_2_yeniden_uretim, tolerans, yeniden_uretim_hepsi_esit_1e-6, meta.{{betik_sha256, "
     f"dondurulmus_betik_sha256_dogrulandi, uretildi_utc, numpy, scipy, girdi_sha256, perm, tohum, tohum_kaynagi}}; "
     f"veri.<veri>.{{K, cift_sayisi, cift_turu_sayilari, tasarim_rank, S10_3, S10_3_duyarlilik_ham_c_permutasyonu, "
     f"yeniden_uretim_6_2, mantel_json_karsilastirma, simetri, modeller, grup}}; `results/q1/konsey_b10_gradyan/mantel_<veri>.json` "
     f"sinamalar.{{ham, ana_etki_artik}}.{{istatistik, p_tek}}", _m11_2)


# --- M11.3 Kesifsel ------------------------------------------------------------------------
def _m11_3():
    J = _oku(_M11_KS)
    L.append(f"Etiket (`etiket`): {_m11g(J, ('etiket',), 'kesifsel etiket')}.\n")
    for k_, t_ in (_m11g(J, ("tanim",), "kesifsel tanim") or {}).items():
        L.append(f"Tanim `{k_}`: {t_}\n")
    L.append(_m11meta(J, _M11_KS) + f" Permutasyon {J['meta']['perm']}; tohum {J['meta']['tohum']}.\n")
    st = []
    for v in _M11_VK:
        d_ = J["veri"][v]
        for s_ in ("ham", "ana_etki_artik"):
            x_ = d_["aile_ici_kisitli_permutasyon"][s_]
            st.append([v, d_["n_CNN"], d_["n_donusturucu"], d_["kisitli_permutasyon_sayisi"], s_,
                       _m9s(x_["istatistik"], plus=True), _m9p(x_["p_tek"]), _m9p(x_["p_iki"]),
                       f"{_m9s(x_['perm_ort'], plus=True)} / {_m9s(x_['perm_sd'])}", x_["perm"]])
    L.append("(a) Aile ici kisitli permutasyonla Mantel (`veri.<veri>.aile_ici_kisitli_permutasyon`):\n")
    T(["Veri kumesi", "n CNN", "n donusturucu", "Kisitli permutasyon sayisi", "Sinama", "r", "Tek yonlu p", "Iki yonlu p",
       "Permutasyon ort / SD", "Permutasyon"], st)
    st = []
    for v in _M11_VK:
        x_ = J["veri"][v]["aile_ayiklamali_artik_spearman_sira"]
        st.append([v, _m9s(x_["istatistik"], plus=True), _m9p(x_["p_tek"]), _m9p(x_["p_iki"]),
                   f"{_m9s(x_['perm_ort'], plus=True)} / {_m9s(x_['perm_sd'])}", _m9s(x_["deger_olcegi_istatistigi"], plus=True),
                   _m9s(x_["deger_olcegi_farki"], 4, plus=True), x_["perm"]])
    L.append("(b) Aile ayiklamali artik Spearman, sira olcegi (`veri.<veri>.aile_ayiklamali_artik_spearman_sira`):\n")
    T(["Veri kumesi", "r (sira olcegi)", "Tek yonlu p", "Iki yonlu p", "Permutasyon ort / SD",
       "r (deger olcegi, M11.2 S10-3 ile ayni hesap)", "Fark sira - deger (4 ondalik)", "Permutasyon"], st)
    st = []
    for v in _M11_VK:
        x_ = J["veri"][v].get("cnn_cnn_artik_spearman")
        if not x_:
            _M11_YOK.append(f"kesifsel veri.{v}.cnn_cnn_artik_spearman")
            continue
        st.append([v, x_["n_CNN"], x_["cift_sayisi"], _m9s(x_["tam_matris_artigi"]["istatistik"], plus=True),
                   _m9p(x_["tam_matris_artigi"]["p_tek"]), _m9s(x_["cnn_alt_matrisi"]["istatistik"], plus=True),
                   _m9p(x_["cnn_alt_matrisi"]["p_tek"]), _m9s(x_["cnn_cnn_ham_spearman"], plus=True)])
    L.append("(c) Yalniz CNN-CNN ciftlerinde artik Spearman (`veri.<veri>.cnn_cnn_artik_spearman`):\n")
    T(["Veri kumesi", "n CNN", "Cift sayisi", "r, tam matris artigi", "Tek yonlu p", "r, CNN alt matrisi artigi",
       "Tek yonlu p", "CNN-CNN ham Spearman (c, log tau)"], st)
    st = []
    for v in _M11_VK:
        x_ = J["veri"][v]["c_ozet"]
        st.append([v, f"{_m11c(x_['en_kucuk_c'])} ({' - '.join(x_['en_kucuk_c_cifti'])})",
                   _m9s(x_["en_kucuk_c_ciftinin_log_tau"], plus=True),
                   f"{_m11c(x_['ikinci_en_kucuk_c'])} ({' - '.join(x_['ikinci_en_kucuk_c_cifti'])})",
                   _m11c(x_["en_buyuk_kosegen_disi_c"])])
    L.append("(d) c_ij ozeti (`veri.<veri>.c_ozet`; c 4 ondalik):\n")
    T(["Veri kumesi", "En kucuk c_ij (cift)", "O ciftin log tau", "Ikinci en kucuk c_ij (cift)", "En buyuk kosegen disi c_ij"], st)
    r_ = _m11g(J, ("veri", "imagenetv2", "c_ozet", "R18_R50"), "kesifsel veri.imagenetv2.c_ozet.R18_R50")
    if r_:
        L.append(f"ImageNetV2 IN_Salman2020Do_R18 - IN_Salman2020Do_R50 (`veri.imagenetv2.c_ozet.R18_R50`): c {_m11c(r_['c'])} "
                 f"(simetrik hucre {_m11c(r_['c_simetrik_hucre'])}); log tau {_m9s(r_['log_tau'], plus=True)} (simetrik hucre "
                 f"{_m9s(r_['log_tau_simetrik_hucre'], plus=True)}); c sirasi {r_['c_sirasi_artan']}/{r_['cift_sayisi']} "
                 f"(artan, 1 = en kucuk); log tau sirasi {r_['log_tau_sirasi_artan']}/{r_['cift_sayisi']}; ana etki artigi c "
                 f"{_m11c(r_['ana_etki_artigi_c'])}, log tau {_m9s(r_['ana_etki_artigi_log_tau'], plus=True)}.\n")
    _M11_YOK_YER.append(len(L))
    L.append("")


_m11("M11.3 Kesifsel: aile ici kisitli permutasyon, aile ayiklamali ve CNN-CNN artik Spearman, R18-R50 ve en kucuk c_ij",
     f"`{_M11_KS}` etiket, tanim, meta.{{betik_sha256, dondurulmus_betik_sha256_dogrulandi, uretildi_utc, numpy, scipy, "
     f"girdi_sha256, perm, tohum}}; veri.<veri>.{{n_CNN, n_donusturucu, kisitli_permutasyon_sayisi, aile_ici_kisitli_permutasyon, "
     f"aile_ayiklamali_artik_spearman_sira, cnn_cnn_artik_spearman, c_ozet}}", _m11_3)

for _i11 in _M11_YOK_YER:
    L[_i11] = ("Bu bolumde (M11.1-M11.3) JSON'da bulunamayip 'bulunamadi' yazilan kalemler: "
               + ("; ".join(_M11_YOK) if _M11_YOK else "yok") + ".\n")

# <<< M11 SONU (hakem paneli sonrasi masa cozumlemeleri)

# ===========================================================================
# GENISLETME 2026-10-31 (M12): hakem paneli acik isleri A2, A9, A10.
# M12.1 2x2 basit etkiler ve turetilmis hucre farklari (kesifsel), M12.2 K-a
# icin 2q - 1 (turetilmis), M12.3 ResNet-18 turevleri cikarilmis 3 uyeli panel
# (kesifsel, on kayit disi). Her sayi results/q1/konsey_ek_masa/a2_*.json,
# a9_*.json, a10_*.json dosyalarindan okunur; yorum yazilmaz. Mevcut bolumlere
# dokunulmaz; bolum M11'den sonra, 'Sabit dizgeler'den once gelir.
# ===========================================================================
_M12_D = "results/q1/konsey_ek_masa"
_M12_A2 = f"{_M12_D}/a2_basit_etkiler.json"
_M12_A9 = f"{_M12_D}/a9_2q_eksi_1.json"
_M12_A10 = f"{_M12_D}/a10_panel.json"
_M12_BETIK = "arsiv/b2_yardimci/_m12_ek_masa.py"
_M12_YOK = []
_M12_YOK_YER = []
_M12_KAD = ("mimari_scr", "mimari_IN", "baslatma_V", "baslatma_R224", "etkilesim", "mimari_ana_etki")


def _m12(ad, kaynak, fn):
    L.append(f"\n### {ad}\n")
    try:
        fn()
    except (KeyError, TypeError, IndexError, ValueError, OSError, ZeroDivisionError, AttributeError) as e_:
        _hata(e_)
    L.append(f"_Kaynak: {kaynak}_\n")


def _m12g(d, yol, etiket):
    """Anahtar yolunu izler; yoksa None doner ve kalemi M12 bulunamayanlar listesine yazar."""
    x = d
    for k_ in yol:
        if isinstance(x, dict) and k_ in x:
            x = x[k_]
        else:
            _M12_YOK.append(etiket)
            return None
    return x


def _m12meta(J, rel):
    m_ = J["meta"]
    hs = _m9sha(_M12_BETIK)
    hk = _m9sha(m_["kutuphane_betik"])
    hd = _m9sha(m_["dondurulmus_betik"])
    return (f"`{rel}` meta: betik {m_['betik']} betik_sha256 {m_['betik_sha256']} (dosyadan hesaplanan {hs}; "
            f"{'AYNI' if m_['betik_sha256'] == hs else 'FARKLI'}); kutuphane {m_['kutuphane_betik']} "
            f"{m_['kutuphane_betik_sha256_dogrulandi']} ({'AYNI' if hk == m_['kutuphane_betik_sha256_dogrulandi'] else 'FARKLI'}); "
            f"dondurulmus_betik_sha256_dogrulandi {m_['dondurulmus_betik_sha256_dogrulandi']} "
            f"({'AYNI' if hd == m_['dondurulmus_betik_sha256_dogrulandi'] else 'FARKLI'}); uretildi_utc {m_['uretildi_utc']}; "
            f"numpy {m_['numpy']}; scipy {m_['scipy']}; girdi dosyasi sayisi (girdi_sha256) {len(m_['girdi_sha256'])}; "
            f"girdilerden dosyasi simdi farkli olan: "
            f"{[p_ for p_, h_ in m_['girdi_sha256'].items() if h_ is not None and _m9sha(p_) != h_] or 'yok'}.")


sec("M12: Hakem paneli acik isleri A2, A9 ve A10 (2026-10-31)",
    f"{_M12_A2}; {_M12_A9}; {_M12_A10}; {_M12_D}/a10_b4.json ve a10_b2.json (dondurulmus betik ciktilari, a10_panel.json "
    f"icinden okunur); {_M12_BETIK} (yalniz sha256)")
L.append("Hakem paneli acik isleri A2 (2x2 basit etkiler), A9 (2q - 1) ve A10 (ResNet-18 turevleri cikarilmis panel). Her "
         "alt bolum kendi JSON'undan okunur; etiketler JSON'un 'etiket' alanindandir. Yuvarlama: log olcekli nicelikler ve "
         "oranlar 3 ondalik, standartlastirilmis etki 2 ondalik, p degerleri bilimsel gosterim.\n")


# --- M12.1 Basit etkiler ve turetilmis farklar ----------------------------------------------
def _m12_1():
    J = _oku(_M12_A2)
    m_ = J["meta"]
    L.append(f"Etiket (`etiket`): {_m12g(J, ('etiket',), 'a2 etiket')}.\n")
    L.append(f"Tanim (`tanim`): {_m12g(J, ('tanim',), 'a2 tanim')}\n")
    L.append(_m12meta(J, _M12_A2) + f" Veri {m_['veri']} ({m_['blok']}); matris {m_['matris_dizini']}; hucre tablosu "
             f"{m_['hucre_tablosu']}; dondurulmus cikti {m_['dondurulmus_cikti']}; B {m_['B']}; bootstrap tohumu "
             f"{m_['bootstrap_tohum']} ({m_['tohum_kaynagi']}); n_goruntu {m_['n_goruntu']}; panel {', '.join(m_['panel'])}.\n")
    st = []
    for nic in ("sigma", "rho"):
        for ad in _M12_KAD:
            k_ = J["karsitliklar"][nic][ad]
            st.append([nic, ad, k_["tanim"], _m9s(k_["kestirim"], plus=True), _m9a(k_["ci90"], plus=True),
                       _m9a(k_["ci95"], plus=True), k_["df"], _m9p(k_["p_iki"]),
                       _m9p(k_["p_holm_kesifsel_aile"]) if "p_holm_kesifsel_aile" in k_ else "-",
                       _m9s(k_["standart_etki_kestirim_bolu_sp"], 2, plus=True), k_["on_kayitli_karsiligi"]])
    L.append("(a) Bolunmus yari, log olcek; dort hucre birlesik varyansli t (`karsitliklar.<sigma|rho>.<ad>`.{tanim, "
             "kestirim, ci90, ci95, df, p_iki, p_holm_kesifsel_aile, standart_etki_kestirim_bolu_sp, on_kayitli_karsiligi}):\n")
    T(["Nicelik", "Karsitlik", "Tanim", "Kestirim", "t %90", "t %95", "df", "p (iki yonlu)", "Holm p (kesifsel aile)",
       "Kestirim / birlesik SD", "On kayitli karsiligi"], st)
    st = []
    for nic in ("sigma", "rho"):
        for ad in _M12_KAD:
            k_ = J["karsitliklar"][nic][ad]
            w_ = k_.get("welch") or {}
            hb, gb, lg = k_["hiyerarsik_bootstrap"], k_["yalniz_goruntu_bootstrap"], k_["logit_duyarlilik"]
            st.append([nic, ad, _m9a(w_.get("ci90"), plus=True) if w_ else "tanimsiz",
                       _m9s(w_.get("df"), 2) if w_ else "-", _m9a(hb["ci90"], plus=True), _m9a(hb["ci95"], plus=True),
                       _m9a(gb["ci90"], plus=True), _m9s(lg["kestirim"], plus=True), _m9a(lg["ci90"], plus=True)])
    L.append("(b) Duyarlilik araliklari (`karsitliklar.<sigma|rho>.<ad>`.{welch, hiyerarsik_bootstrap, "
             "yalniz_goruntu_bootstrap, logit_duyarlilik}):\n")
    T(["Nicelik", "Karsitlik", "Welch %90", "Welch df", "Hiyerarsik bootstrap %90", "Hiyerarsik bootstrap %95",
       "Yalniz goruntu bootstrap %90", "Logit kestirim", "Logit t %90"], st)
    st = []
    for nic in ("sigma", "rho", "omega"):
        for h_, x_ in J["hucre_ozetleri"][nic].items():
            st.append([nic, h_, x_["n"], ", ".join(_m9s(v_, plus=True) for v_ in x_["degerler"]),
                       _m9s(x_["ort"], plus=True), _m9s(x_["sd"]), x_["aralik"]])
    L.append("(c) Hucre ozetleri, betimsel (`hucre_ozetleri.<nicelik>.<hucre>`; hucre ici aralik yok):\n")
    T(["Nicelik", "Hucre", "n", "Kosu degerleri", "Ortalama", "SD", "Aralik"], st)
    d_ = J["dogrulama"]
    L.append(f"Kesifsel Holm ailesi (`kesifsel_holm.aile`): {', '.join(J['kesifsel_holm']['aile'])}. Dogrulama (`dogrulama`): "
             f"model duzeyi sigma ve rho ile dondurulmus JSON en buyuk mutlak fark "
             f"{max(d_['model_duzeyi_dondurulmus_json_maks_fark'].values()):.2e}; on kayitli karsitliklar (H1, H2, H3, S2) "
             f"kestirim ve t araliklari en buyuk fark "
             f"{max(d_['on_kayitli_karsitliklar_dondurulmus_json_maks_fark'].values()):.2e}; hiyerarsik bootstrap H1-H3 "
             f"araliklari ile dondurulmus `duyarlilik.hiyerarsik_bootstrap` en buyuk fark "
             f"{max(d_['hiyerarsik_bootstrap_H1_H3_dondurulmus_json_maks_fark'].values()):.2e}; hedef maskesi tutarli "
             f"{_m9e(d_['tutarlilik']['hedef_maskesi_tutarli'])}.\n")


_m12("M12.1 2x2 basit etkiler ve turetilmis hucre farklari: sigma ve rho (A2; B4, CIFAR-10)",
     f"`{_M12_A2}` etiket, tanim, meta.{{betik, betik_sha256, kutuphane_betik, kutuphane_betik_sha256_dogrulandi, "
     f"dondurulmus_betik_sha256_dogrulandi, uretildi_utc, numpy, scipy, girdi_sha256, veri, blok, matris_dizini, hucre_tablosu, "
     f"dondurulmus_cikti, B, bootstrap_tohum, tohum_kaynagi, n_goruntu, panel}}; karsitliklar.<sigma|rho>.<ad>; hucre_ozetleri; "
     f"kesifsel_holm; dogrulama; `{_M12_BETIK}` sha256 bu betikte hashlib ile", _m12_1)


# --- M12.2 2q - 1 ---------------------------------------------------------------------------
def _m12_2():
    J = _oku(_M12_A9)
    L.append(f"Etiket (`etiket`): {_m12g(J, ('etiket',), 'a9 etiket')}.\n")
    L.append(f"Tanim (`tanim`): {_m12g(J, ('tanim',), 'a9 tanim')}\n")
    L.append(_m12meta(J, _M12_A9) + "\n")
    st = []
    for v, x_ in J["veri"].items():
        st.append([v, _m9s(x_["ort_q"]), _m9s(x_["iki_ort_q_eksi_1"], plus=True),
                   ", ".join(_m9s(y_, plus=True) for y_ in x_["iki_q_eksi_1_s"]), _m9a(x_["t_ci90"], plus=True),
                   _m9a(x_["t_ci95"], plus=True), _m9a(x_["bootstrap_ci90"], plus=True),
                   _m9a(x_["bootstrap_ci95"], plus=True), _m9p(x_["p_tek_H0_2q_eksi_1_le_0_(K-a ile ayni)"]),
                   f"`{x_['kaynak']}` {x_['kaynak_anahtar']}; `{x_['bootstrap_kaynak']}` {x_['bootstrap_anahtar']}"])
    T(["Veri", "Ort q (kaynak)", "2 ort(q) - 1", "Kosu basina 2q - 1 (cift sirasiyla)", "t %90", "t %95",
       "Hiyerarsik bootstrap %90", "Hiyerarsik bootstrap %95", "Tek yonlu p (H0: 2q - 1 <= 0; K-a p'si)", "Kaynak satiri"], st)
    for v, x_ in J["veri"].items():
        dn = x_["denetim"]
        L.append(f"{v} denetim (`veri.{v}.denetim`): kosu basina (simetrik - yonlu)/D ile 2q - 1 en buyuk fark "
                 f"{dn['kosu_basina_(simetrik-yonlu)/D_ile_2q-1_maks_fark']:.2e}; dondurulmus ozdeslik artigi "
                 f"{dn['ozdeslik_artik_max_(dondurulmus)']:.2e}; M11.1 bootstrap JSON nokta ort q ile dondurulmus ort q farki "
                 f"{dn['bootstrap_nokta_ort_q_ile_dondurulmus_ort_fark']:.2e}; ciftler "
                 f"{'; '.join(' / '.join(c_) for c_ in x_['ciftler'])}.\n")


_m12("M12.2 K-a icin turetilmis 2q - 1 satiri (A9; CIFAR-10 B2, CIFAR-100 B9)",
     f"`{_M12_A9}` etiket, tanim, meta; veri.<veri>.{{ort_q, iki_ort_q_eksi_1, iki_q_eksi_1_s, t_ci90, t_ci95, bootstrap_ci90, "
     f"bootstrap_ci95, p_tek_H0_2q_eksi_1_le_0_(K-a ile ayni), kaynak, kaynak_anahtar, bootstrap_kaynak, bootstrap_anahtar, "
     f"ciftler, denetim}}", _m12_2)


# --- M12.3 ResNet-18 turevleri cikarilmis panel --------------------------------------------
def _m12_3():
    J = _oku(_M12_A10)
    m_ = J["meta"]
    L.append(f"Etiket (`etiket`): {_m12g(J, ('etiket',), 'a10 etiket')}.\n")
    L.append(f"Tanim (`tanim`): {_m12g(J, ('tanim',), 'a10 tanim')}\n")
    L.append(_m12meta(J, _M12_A10) + f" Matris dizinleri {m_['matris_dizinleri']}; bootstrap B {m_['bootstrap_B']}, tohum "
             f"{m_['bootstrap_tohum']}; dondurulmus betige verilen panel_en_az {m_['panel_en_az_kullanilan']}.\n")
    md = J["mimari_dogrulama"]
    st = [[a_, x_["sinif"], " > ".join(x_["mro"]), ", ".join(x_["blok_siniflari"]), x_["blok_sayisi"], x_["conv2d_sayisi"],
           x_["parametre_sayisi"], _m9e(x_["resnet18_turevi"])] for a_, x_ in md["modeller"].items()]
    L.append(f"(a) Mimari dogrulama (`mimari_dogrulama`; kaynak {md['kaynak']}, {md['robustbench_dizin']}):\n")
    T(["Panel uyesi (dondurulmus)", "Sinif", "MRO", "Artik blok sinifi", "Blok sayisi", "Conv2d sayisi", "Parametre sayisi",
       "ResNet-18 turevi"], st)
    L.append(f"Cikarilan (`cikarilan`): {', '.join(J['cikarilan'])}. Kalan panel (`kalan_panel`): {', '.join(J['kalan_panel'])}. "
             f"Tablo farki (`tablo_farki`): {', '.join(J['tablo_farki'])}. Varsayilan bayrakla dondurulmus betik "
             f"(`varsayilan_bekci_hatasi`): b4 '{J['varsayilan_bekci_hatasi']['b4_varsayilan']}', b2 "
             f"'{J['varsayilan_bekci_hatasi']['b2_varsayilan']}'.\n")
    st = [[k_, f"`{c_['komut']}`", c_["donus_kodu"], f"`{c_['cikti']}`", c_["cikti_sha256"]]
          for k_, c_ in J["dondurulmus_cagrilar"].items()]
    L.append("(b) Dondurulmus betik cagrilari (`dondurulmus_cagrilar`):\n")
    T(["Cagri", "Komut", "Donus kodu", "Cikti", "Cikti sha256"], st)
    st = []
    for pn, b_ in (("3 uye (A10)", J["b4_a10"]), ("7 uye (dondurulmus)", J["b4_dondurulmus_panel"])):
        for h_ in ("H1", "H2", "H3"):
            x_ = b_[h_]
            st.append([h_, pn, _m9s(x_["kestirim"], plus=True), _m9a(x_["ci90"], plus=True), _m9a(x_["ci95"], plus=True),
                       _m9p(x_["p_ham"]), _m9p(x_["p_holm"]), _m9a(x_["hiyerarsik_bootstrap_ci90"], plus=True),
                       _m9a(x_["welch_ci90"], plus=True), x_["karar"]])
    L.append("(c) B4 aile F_B4 (`b4_a10.<H>`, `b4_dondurulmus_panel.<H>`; bolunmus yari, log, birlesik varyans df 5):\n")
    T(["Hipotez", "Panel", "Kestirim", "t %90", "t %95", "p ham", "p Holm", "Hiyerarsik bootstrap %90", "Welch %90", "Karar"], st)
    st = []
    for pn, b_ in (("3 uye (A10)", J["b4_a10"]), ("7 uye (dondurulmus)", J["b4_dondurulmus_panel"])):
        st.append([pn, b_["sonuc_bolgesi"], _m9e(b_["O4_niteleme"]), _m9s(b_["H2_logit_kestirim"], plus=True),
                   "; ".join(f"{h_} {b_['delta_0.06'][h_]}" for h_ in ("H1", "H2", "H3")),
                   f"{_m9s(b_['S2_rho_VIN_eksi_Vscr']['kestirim'], plus=True)} "
                   f"{_m9a(b_['S2_rho_VIN_eksi_Vscr']['ci90'], plus=True)}"])
    T(["Panel", "Sonuc bolgesi", "O4 niteleme", "H2 logit kestirim", "Karar, delta 0,06", "S2 rho(V-IN) - rho(V-scr) [%90]"], st)
    st = []
    for pn, b_ in (("3 uye (A10)", J["b2_a10"]), ("7 uye (dondurulmus)", J["b2_dondurulmus_panel"])):
        ka, kb, kc = b_["K-a"], b_["K-b"], b_["K-c"]
        st.append(["K-a ort q", pn, _m9s(ka["ort_q"]), ", ".join(_m9s(q_) for q_ in ka["q_s"]), _m9a(ka["ci90"]),
                   _m9a(ka["ci95"]), _m9p(ka["p_tek_H0_q_le_0.5"]), _m9p(b_["p_holm"][0]), ka["karar"]])
        st.append(["K-b ort rho(V-scr)", pn, _m9s(kb["ort_rho_Vscr"], plus=True),
                   ", ".join(_m9s(r_, plus=True) for r_ in kb["rho_s"]), _m9a(kb["ci90"], plus=True),
                   _m9a(kb["ci95"], plus=True), f"TOST {_m9p(kb['tost_p'])}", _m9p(b_["p_holm"][1]), kb["karar"]])
        st.append(["K-c Delta_w", pn, _m9s(kc["Delta_w"], plus=True), "", f"bootstrap {_m9a(kc['bootstrap_ci90'], plus=True)}",
                   "", _m9p(kc["p_tek_H0_Delta_le_0"]), _m9p(b_["p_holm"][2]), kc["karar"]])
    L.append("(d) B2 aile F_B2, CIFAR-10 (`b2_a10`, `b2_dondurulmus_panel`):\n")
    T(["Nicelik", "Panel", "Kestirim", "Kosu degerleri", "%90", "%95", "p ham", "p Holm", "Karar"], st)
    st = []
    for s_, x_ in J["karsilastirma"].items():
        if s_ == "sonuc_bolgesi":
            st.append([s_, "", "", "", x_["dondurulmus"], x_["a10"], _m9e(x_["ayni"])])
            continue
        st.append([s_, _m9s(x_["dondurulmus_kestirim"], plus=True), _m9s(x_["a10_kestirim"], plus=True),
                   f"{_m9e(x_['ayni_yon'])} ({x_.get('ayni_yon_tanimi', 'kestirim isareti')})", x_["dondurulmus_karar"],
                   x_["a10_karar"], _m9e(x_["karar_ayni"])])
    L.append("(e) Dondurulmus panelle karsilastirma (`karsilastirma`):\n")
    T(["Sinama", "Kestirim, 7 uye", "Kestirim, 3 uye", "Ayni yon", "Karar, 7 uye", "Karar, 3 uye", "Karar ayni"], st)
    bg = J["bagimsiz_yeniden_hesap"]
    L.append(f"Bagimsiz yeniden hesap (`bagimsiz_yeniden_hesap`; dondurulmus islevler importlib ile, panel "
             f"{', '.join(bg['panel'])}): H1-H3 kestirim en buyuk fark {bg['H_kestirim_maks_fark']:.2e}, t %90 en buyuk fark "
             f"{bg['H_ci90_maks_fark']:.2e}; K-a q {bg['K-a_q_maks_fark']:.2e}; K-b rho {bg['K-b_rho_maks_fark']:.2e}.\n")
    _M12_YOK_YER.append(len(L))
    L.append("")


_m12("M12.3 ResNet-18 turevleri cikarilmis 3 uyeli panelle B4 ve B2 (A10; kesifsel, on kayit disi panel)",
     f"`{_M12_A10}` etiket, tanim, meta; mimari_dogrulama; cikarilan; kalan_panel; tablo_farki; dondurulmus_cagrilar; "
     f"varsayilan_bekci_hatasi; b4_a10; b4_dondurulmus_panel; b2_a10; b2_dondurulmus_panel; karsilastirma; "
     f"bagimsiz_yeniden_hesap (b4_a10 ve b2_a10 alanlari `{_M12_D}/a10_b4.json` ile `{_M12_D}/a10_b2.json` dosyalarindan, "
     f"dondurulmus panel alanlari `results/q1/konsey_ayrisim_b4.json` ile `results/q1/konsey_ayrisim_b2.json` dosyalarindan "
     f"kopyalanmistir)", _m12_3)

for _i12 in _M12_YOK_YER:
    L[_i12] = ("Bu bolumde (M12.1-M12.3) JSON'da bulunamayip 'bulunamadi' yazilan kalemler: "
               + ("; ".join(_M12_YOK) if _M12_YOK else "yok") + ".\n")

# <<< M12 SONU (hakem paneli acik isleri A2, A9, A10)

# ===========================================================================
# GENISLETME 2026-10-31 (M13): sekil kaynaklari (visio yeniden cizimi; envanter
# raporlar/visio_2026-10-31/01_envanter.md bolum 5-6, Y1, Y4, Y5). M13.1 tasarim ve
# egitim tarifi (results/q1/konsey_b3_tarif.json), M13.2 kayit haritasi
# (results/q1/konsey_kayit_kurallari.json), M13.3 zaman cizelgesi
# (results/q1/konsey_zaman_cizelgesi.json). Uc JSON arsiv/b2_yardimci/_m13_tarif.py,
# _m13_kayit.py ve _m13_zaman.py ile kaynaklarindan uretilir; bu blok yalniz okur,
# yorum yazmaz. JSON'lardaki foy satir referanslari bu calismada L uzerinden satir
# sha256'siyla denetlenir (M13'ten onceki satirlar ciktida degismez). Mevcut
# bolumlere dokunulmaz; bolum M12'den sonra, 'Sabit dizgeler'den once gelir.
# ===========================================================================
_M13_TJ = "results/q1/konsey_b3_tarif.json"
_M13_KJ = "results/q1/konsey_kayit_kurallari.json"
_M13_ZJ = "results/q1/konsey_zaman_cizelgesi.json"
_M13_FOY = "results/C1_REFERANS_FOYU.md"
_M13_BETIKLER = ("arsiv/b2_yardimci/_m13_tarif.py", "arsiv/b2_yardimci/_m13_kayit.py", "arsiv/b2_yardimci/_m13_zaman.py",
                 "arsiv/b2_yardimci/_m13_ortak.py")
_M13_DEGISEN = []
_M13_YOK_YER = []


def _m13(ad, kaynak, fn):
    L.append(f"\n### {ad}\n")
    try:
        fn()
    except (KeyError, TypeError, IndexError, ValueError, OSError, ZeroDivisionError, AttributeError) as e_:
        _hata(e_)
    L.append(f"_Kaynak: {kaynak}_\n")


def _m13_foy(n, sha_, etiket):
    """Foy satiri n (bu calismadaki metin; M13'ten onceki satirlar ciktida aynen kalir) JSON'daki sha256 ile ayni mi."""
    s_ = "\n".join(L).split("\n")
    ok_ = n <= len(s_) and _m9hl.sha256(s_[n - 1].encode("utf-8")).hexdigest() == sha_
    if not ok_:
        _M13_DEGISEN.append(f"{etiket} (satir {n})")
    return ok_


def _m13g(x):
    if x is None:
        return "-"
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return str(x)
    return str(int(x)) if float(x).is_integer() else f"{x:g}"


def _m13t(x):
    return "-" if not x else str(x).replace("T", " ").replace("+00:00", "")


def _m13meta(J, rel):
    m_ = J["meta"]
    hb, ho = _m9sha(m_["betik"]), _m9sha(m_["ortak_modul"])
    farkli = [p_ for p_, h_ in m_["kaynaklar_sha256"].items() if p_ != _M13_FOY and _m9sha(p_) != h_]
    return (f"`{rel}` meta: betik {m_['betik']} betik_sha256 {m_['betik_sha256']} (dosyadan hesaplanan "
            f"{'AYNI' if hb == m_['betik_sha256'] else 'FARKLI ' + hb}); ortak modul {m_['ortak_modul']} "
            f"{m_['ortak_modul_sha256']} ({'AYNI' if ho == m_['ortak_modul_sha256'] else 'FARKLI'}); uretildi_utc "
            f"{m_['uretildi_utc']}; python {m_['python']}; kaynak dosya sayisi (kaynaklar_sha256) {m_['kaynak_sayisi']}; "
            f"kaynaklardan simdi farkli olan (foy haric; foy satirlari satir sha256'siyla ayrica denetlenir): "
            f"{farkli or 'yok'}."
            # 31.10.2026 duzeltme turu (bulgu 3): foy ozeti M13 haric metnin sha256'si; git'ten okunan surumler
            + (f" Foy ozeti (`meta.foy_ozeti.m13_haric_sha256`; foyden '## M13:' bolumu cikarilmis metnin sha256'si, "
               f"denetimi arsiv/b2_yardimci/_m13_kontrol.py): {m_['foy_ozeti']['m13_haric_sha256']}." if "foy_ozeti" in m_ else "")
            + (f" Git'ten salt okunan surumler (`meta.git_kaynaklari.blob`): {len(m_['git_kaynaklari']['blob'])} dosya "
               f"({', '.join(sorted({k_.split(':')[1] for k_ in m_['git_kaynaklari']['blob']}))})." if "git_kaynaklari" in m_ else ""))


sec("M13: Sekil kaynaklari, tasarim tarifi, kayit haritasi ve zaman cizelgesi (2026-10-31)",
    f"{_M13_TJ}; {_M13_KJ}; {_M13_ZJ}; {', '.join(_M13_BETIKLER)} (yalniz sha256)")
L.append("Uc yeni sekil (Y1 fig:design_recipe, Y4 fig:registry_map, Y5 fig:prereg_chain) icin makine okunur kaynaklardir. "
         "Her JSON uretici betiginin kaynak dosyalarindan okunur; degerin yaninda kaynak dosya ve satiri JSON'da yazilidir. "
         "Sonuc sayilari burada tekrarlanmaz; foyun ilgili satiri verilir ve satirin sha256'si bu calismada denetlenir.\n")


# --- M13.1 Tasarim ve egitim tarifi ---------------------------------------------------------
def _m13_1():
    J = _oku(_M13_TJ)
    L.append(f"Etiket (`etiket`): {J['etiket']}.\n")
    L.append(_m13meta(J, _M13_TJ) + "\n")
    H = J["hucreler"]
    sira = [h_ for h_ in ("V-scr", "V-IN", "R224-scr", "R224-IN", "C1-R32") if h_ in H]

    def ilk(h_):
        return list(H[h_]["kosular"].values())[0]

    st = []
    for h_ in sira:
        x_, g_ = H[h_], H[h_]["girdi_hatti"]
        nrm = g_["normalizasyon"]
        if g_.get("imagenet_ortalama"):
            nrm += (f"; ortalama {g_['imagenet_ortalama']}, SD {g_['imagenet_sd']}, cfg ile ayni "
                    f"{_m9e(g_.get('norm_cfg_ile_ayni'))} (`{g_['init_kaynak']}`)")
        st.append([h_, x_["blok"], g_["model"], g_["girdi"], nrm, g_["baslatma"],
                   ", ".join(str(t_) for t_ in x_["tohumlar"]),
                   f"`{x_['on_kayit_satiri']}`" if x_.get("on_kayit_satiri") else f"hucre tablosu: {x_.get('hucre_tablosu_tanimi')}",
                   "; ".join(f"`{k_}`" for k_ in g_["kaynak"])])
    L.append("(a) Hucreler ve girdi hatti (`hucreler.<h>`.{blok, girdi_hatti, tohumlar, on_kayit_satiri}):\n")
    T(["Hucre", "Blok", "Model", "Girdi hatti", "Normalizasyon", "Baslatma", "Tohumlar", "On kayit satiri",
       "Kod kaynagi"], st)
    st = []
    for h_ in sira:
        o_ = ilk(h_)["temiz"]
        st.append([h_, o_["epok_bayragi"], o_["eniyileyici_eniyileyici"], _m13g(o_["eniyileyici_lr_etkin"]),
                   _m13g(o_["eniyileyici_agirlik_azaltma"]), _m13g(o_.get("eniyileyici_momentum")),
                   f"{o_['lr_cizelgesi']['tur']} (T_max {_m13g(o_['lr_cizelgesi']['T_max_epok'])})", o_["batch"],
                   o_["baslatma_bayragi"], f"`{o_['komut_kaynagi']}`; {o_['eniyileyici_kaynak']}"])
    L.append("(b) Temiz asama (`hucreler.<h>.kosular.<ilk kosu>.temiz`; B3 hucrelerinde iki kosu tohum disinda ozdes, "
             "bkz. denetimler):\n")
    T(["Hucre", "Epok", "Eniyileyici", "lr (etkin)", "Agirlik azaltma", "Momentum", "LR cizelgesi", "Batch",
       "--init-weights", "Komut ve eniyileyici kaynagi"], st)
    st = []
    for h_ in sira:
        o_ = ilk(h_)["AT"]
        st.append([h_, o_["epok_tavani"], f"{o_['lr_cizelgesi']['tur']} (T_max {o_['lr_cizelgesi']['T_max_epok']})",
                   o_["sabir"], o_["eniyileyici_eniyileyici"], _m13g(o_["eniyileyici_lr_etkin"]),
                   _m13g(o_["eniyileyici_agirlik_azaltma"]), _m13g(o_.get("eniyileyici_momentum")), o_["batch"],
                   f"{_m13g(o_['eps_x255'])}/255", f"{_m13g(o_['alpha_x255'])}/255", o_["pgd_adim"],
                   _m13g(o_["gradyan_kirpma"]), o_["kaydet_her"], f"`{o_['komut_kaynagi']}`; {o_['epok_tavani_kaynagi']}"])
    L.append("(c) AT asamasi (`hucreler.<h>.kosular.<ilk kosu>.AT`; eps, alpha, adim ve gradyan kirpma cli/train.py "
             "varsayilanlari, satirlari JSON'da):\n")
    T(["Hucre", "Epok tavani", "LR cizelgesi", "Sabir", "Eniyileyici", "lr (etkin)", "Agirlik azaltma", "Momentum",
       "Batch", "eps", "alpha", "PGD adim", "Gradyan kirpma", "--save-every", "Komut ve tavan kaynagi"], st)
    o_ = J["ortak"]
    L.append(f"Ortak (`ortak`): AT kaybi {o_['at_kaybi']['tur']}, mix_ratio {_m13g(o_['at_kaybi']['mix_ratio'])}, PGD rastgele "
             f"baslangic {_m9e(o_['at_kaybi']['pgd_rastgele_baslangic'])} ({o_['at_kaybi']['kaynak']}); erken durma olcutu "
             f"{o_['erken_durma']['olcut']}, min_delta {_m13g(o_['erken_durma']['min_delta_puan'])} ({o_['erken_durma']['kaynak']}); "
             f"veri {o_['veri']['egitim_kumesi']}, dogrulama bolmesi `{o_['veri']['dogrulama_bolmesi_dosyasi']}` n "
             f"{o_['veri']['dogrulama_n']} ({o_['veri']['dogrulama_n_kaynagi']}); artirma {o_['veri']['artirma']} "
             f"({o_['veri']['artirma_kaynagi']}); pilot secilen tavan {o_['at_tavani_pilot']['secilen_tavan']} "
             f"(`{o_['at_tavani_pilot']['kaynak']}`; on kayit `{o_['at_tavani_pilot']['on_kayit']}`); secim kurali "
             f"`{o_['secim_kurali']['kaynak']}`.\n")
    for h_ in sira:
        if "takma_adlar" in H[h_]:
            k_ = H[h_]["kosular"]
            L.append(f"{h_} kosulari: " + "; ".join(
                f"{t_} temiz `{k_[t_]['temiz']['komut_kaynagi']}`, AT `{k_[t_]['AT']['komut_kaynagi']}` (kuyruk sablonu "
                f"`{k_[t_]['AT']['kuyruk_sablonu']}`, sablonla ayni bayraklar {_m9e(k_[t_]['AT']['sablonla_ayni_bayraklar'])})"
                for t_ in H[h_]["takma_adlar"]) + ".\n")
    d_ = J["denetimler"]
    gb = d_["gunluk_basliklari_cozumlenen_degerlerle_ayni"]
    L.append(f"Denetimler (`denetimler`): B3 AT tavani pilotla ayni {_m9e(d_['B3_AT_tavani_pilotla_ayni'])}; B3 komutlari kuyruk "
             f"sablonuyla ayni {_m9e(d_['B3_komutlar_kuyruk_sablonuyla_ayni'])}; B3 hucre ici kosular tohum disinda ozdes "
             f"{_m9e(d_['B3_hucre_ici_kosular_tohum_disinda_ozdes'])}; egitim gunlugu basliklari (Epochs, LR, eniyileyici) "
             f"cozumlenen degerlerle {gb['uyusan']}/{gb['denetlenen']} uyusuyor; AT eps, alpha ve adim hucreler arasi ayni "
             f"{_m9e(d_['AT_eps_alpha_adim_hucreler_arasi_ayni'])}.\n")
    f_ = J["foy_referanslari"]
    ep = "; ".join(f"{t_} satir {x_['foy_satiri']} ({'satir ayni' if _m13_foy(x_['foy_satiri'], x_['satir_metni_sha256'], 'M13.1 ' + t_) else 'SATIR DEGISTI'})"
                   for t_, x_ in f_["B3_gerceklesen_epoklar"].items())
    c1 = f_["C1_son_kontrol_noktasi_epoklari_bolumu"]
    te = f_["B3_toplam_egitim_suresi"]
    L.append(f"Gerceklesen epoklar bu bolumde tekrarlanmaz (`foy_referanslari`): B3, M9.1 tablosunun 'AT epok (kosulan)' sutunu, "
             f"{ep}; C1 V-scr ve C1-R32, M8.14 basligi satir {c1['foy_satiri']} "
             f"({'satir ayni' if _m13_foy(c1['foy_satiri'], c1['satir_metni_sha256'], 'M13.1 M8.14') else 'SATIR DEGISTI'}); "
             f"B3 toplam egitim suresi M9.1 satir {te['foy_satiri']} "
             f"({'satir ayni' if _m13_foy(te['foy_satiri'], te['satir_metni_sha256'], 'M13.1 toplam') else 'SATIR DEGISTI'}).\n")
    # 31.10.2026 duzeltme turu, bulgu 7: AT tavani cumlesi tam alinti ve V-scr tavan denetimi
    at_ = J["ortak"].get("at_tavani_on_kayit_cumlesi")
    if at_:
        L.append(f"AT tavani cumlesi (`ortak.at_tavani_on_kayit_cumlesi`, `{at_['kaynak']}`, tam alinti): \"{at_['alinti']}\" "
                 f"On kayit hucre tablosunda 'mevcut' isaretli hucreler: {', '.join(at_['on_kayit_tablosunda_mevcut_isaretli_hucreler'])}; "
                 f"yeni hucreler: {', '.join(at_['on_kayit_tablosunda_yeni_hucreler'])}.\n")
    vd = d_.get("V_scr_AT_tavani_ve_gerceklesen_durma")
    if vd:
        okv = all([_m13_foy(n_, vd["foy_satir_metni_sha256"][t_], f"M13.1 V-scr durma {t_}") for t_, n_ in vd["foy_satirlari"].items()])
        L.append(f"V-scr AT tavani (`denetimler.V_scr_AT_tavani_ve_gerceklesen_durma`): {vd['V_scr_AT_tavani']} "
                 f"({vd['V_scr_AT_tavani_kaynagi']}; kosinus T_max {vd['V_scr_lr_cizelgesi_T_max']}); B3 tavani {vd['B3_AT_tavani']} "
                 f"({vd['B3_AT_tavani_kaynagi']}); gerceklesen durma epoklari B3 tavaninin altinda "
                 f"{_m9e(vd['gerceklesen_durma_epoklari_B3_tavaninin_altinda'])} ({vd['foy_bolum']} '{vd['foy_sutun']}' sutunu, satir "
                 f"{min(vd['foy_satirlari'].values())}-{max(vd['foy_satirlari'].values())}, "
                 f"{'satirlar ayni' if okv else 'SATIR DEGISTI'}; epoklar burada tekrarlanmaz).\n")
    # 31.10.2026 duzeltme turu, bulgu 6: C1 hucrelerinin kosu anindaki kod surumu
    kh = [h_ for h_ in ("V-scr", "C1-R32") if "kosu_ani_kodu" in H.get(h_, {})]
    if kh:
        st = []
        for h_ in kh:
            for r_ in H[h_]["kosu_ani_kodu"]["karsilastirma"]:
                st.append([h_, r_["asama"], r_["ad"], _m13g(r_["kosu_ani"]), f"`{r_['kosu_ani_kaynagi']}`",
                           _m13g(r_["bugunku_tarif"]), _m9e(r_["ayni"])])
        ka_ = H[kh[0]]["kosu_ani_kodu"]
        dy = ka_["dayanak"]
        L.append(f"(d) C1 hucrelerinin kosu anindaki kod surumu (`hucreler.<V-scr|C1-R32>.kosu_ani_kodu`): (b) ve (c) "
                 f"tablolarindaki C1 'varsayilan' kaynaklari bugunku kod satirlaridir; kosular {ka_['commit_kisa']} "
                 f"({dy['commit_utc']}) ile yapilmistir. Dayanak (`dayanak`): ilk C1 egitim adimi {dy['ilk_C1_egitim_adimi_baslangic_utc']} "
                 f"(`{dy['ilk_adim_kaynagi']}`, commit'e gore {dy['ilk_adim_baslangici_commit_eksi_s']} s), son adim "
                 f"{dy['son_C1_egitim_adimi_bitis_utc']} (`{dy['son_adim_kaynagi']}`); izlenen dosyalari degistiren bir sonraki commit "
                 f"{dy['izlenen_dosyalari_sonra_degistiren_ilk_commit']['commit']} ({dy['izlenen_dosyalari_sonra_degistiren_ilk_commit']['utc']}), "
                 f"son adim ondan once {_m9e(dy['son_egitim_adimi_sonraki_committen_once'])}; egitim dosyalari commit'le degismedi "
                 f"{_m9e(dy['egitim_dosyalari_commitle_degismedi'])}; --val-indices secenegi commit oncesinde var "
                 f"{_m9e(dy['val_indices_secenegi']['77ae259_oncesi'])}, commit'te var {_m9e(dy['val_indices_secenegi']['77ae259'])}; "
                 f"TIMING.md saatleri ile gunluk mtime farki en buyuk {_m13g(round(dy['zaman_kaynagi_utc_denetimi_en_buyuk_fark_s'], 2))} s. "
                 f"Kosu aninda olmayan CLI secenekleri: {', '.join(ka_['kosu_aninda_olmayan_cli_secenekleri'])} (davranis o surumde "
                 f"sabit kodla belirleniyordu). Asagidaki tablo her degeri {ka_['commit_kisa']} metninden yeniden okur:\n")
        T(["Hucre", "Asama", "Deger", f"{ka_['commit_kisa']} (kosu ani)", "Kosu ani kaynagi", "Bugunku tarif", "Ayni"], st)
        L.append("Eniyileyici gozlemi (`kosu_ani_kodu.eniyileyici_gozlemi`): " + "; ".join(
            f"{h_} {a_}: {g_['durum']}" + (f" ({g_['kod']})" if "kod" in g_ else "")
            for h_ in kh for a_, g_ in H[h_]["kosu_ani_kodu"]["eniyileyici_gozlemi"].items())
            + f". C1 kosu ani kodu bugunku tarifle ayni (`denetimler.C1_kosu_ani_kodu_bugunku_tarifle_ayni`): "
              f"{_m9e(d_.get('C1_kosu_ani_kodu_bugunku_tarifle_ayni'))}.\n")


_m13("M13.1 Tasarim ve egitim tarifi: 2x2 hucreler ve R32 koprusu (Y1, fig:design_recipe)",
     f"`{_M13_TJ}` etiket, meta.{{betik, betik_sha256, ortak_modul, ortak_modul_sha256, uretildi_utc, python, kaynak_sayisi, "
     f"kaynaklar_sha256, foy_ozeti, yeniden_uretim_notu, git_kaynaklari}}; hucreler.<h>.{{blok, girdi_hatti, tohumlar, "
     f"on_kayit_satiri, hucre_tablosu_tanimi, takma_adlar, kosular.<k>.{{temiz, AT}}, kosu_ani_kodu}}; ortak "
     f"(at_tavani_on_kayit_cumlesi dahil); denetimler (C1_kosu_ani_kodu_bugunku_tarifle_ayni, "
     f"V_scr_AT_tavani_ve_gerceklesen_durma dahil); foy_referanslari", _m13_1)


# --- M13.2 Kayit haritasi --------------------------------------------------------------------
def _m13_esik(s_):
    out = []
    for a_ in ("ongorulen_buyukluk", "esik", "beklenti_esigi", "bant"):
        e_ = s_.get(a_)
        if isinstance(e_, dict) and "deger" in e_:
            out.append(f"{a_} {_m13g(e_['deger'])} (`{e_['kaynak']}`; on kayit `{e_.get('on_kayit', '-')}`)")
    h0 = (s_.get("sinama") or {}).get("H0_esik")
    if h0:
        out.append(f"H0 esigi {_m13g(h0['deger'])} (`{h0['kaynak']}`)")
    cu = (s_.get("curutme") or {}).get("esik")
    if cu:
        out.append(f"curutme esigi {_m13g(cu['deger'])} (`{cu['kaynak']}`)")
    for r_ in s_.get("kurallar_sirasiyla", []):
        for a_ in ("esik", "p_esigi"):
            if a_ in r_:
                out.append(f"{r_[a_]['ad']} {_m13g(r_[a_]['deger'])} (`{r_[a_]['kaynak']}`)")
    # 31.10.2026 duzeltme turu (bulgu 1, 2): esdegerlik siniri ve S5 ongoru dogrusu JSON'daki acik alanlardan; JSON'da
    # esik alani yoksa hucre '-' kalir (eski elle yazilmis dolgu kaldirildi)
    es_ = s_.get("esdegerlik_siniri")
    if isinstance(es_, dict):
        out.append(f"esdegerlik siniri ({es_['alt_sinir']:g}; {es_['ust_sinir']:g}), {es_['tur']} (`{es_['kaynak']}`"
                   + (f"; TOST tanimi `{es_['tost_tanimi']}`" if es_.get("tost_tanimi") else "")
                   + (f"; icinde tanimi `{es_['icinde_tanimi']}`, uygulama `{es_['uygulama']}`" if es_.get("icinde_tanimi") else "")
                   + f"; on kayit `{es_.get('on_kayit', '-')}` yazim {' / '.join(es_.get('on_kayit_metninde_yazimi', [])) or '-'})")
    od_ = s_.get("ongoru_dogrusu")
    if isinstance(od_, dict):
        out.append(f"ongoru dogrusu egim {_m13g(od_['egim']['deger'])}, kesisim {_m13g(od_['kesisim']['deger'])} "
                   f"(`{od_['egim']['kaynak']}`; uygulama `{od_['betik']['kaynak']}`; on kayit `{od_['on_kayit']['kaynak']}`)")
    return "; ".join(out) or "-"


def _m13_kural(s_):
    ks = []
    for a_ in ("payda_kurali", "curutme", "destek"):
        x_ = s_.get(a_)
        if isinstance(x_, dict):
            k_ = x_.get("kaynak") or (x_.get("esik") or {}).get("kaynak")
            okr = (f"; on kayit `{x_['on_kayit']['kaynak']}`" if isinstance(x_.get("on_kayit"), dict) else "")
            ks.append(f"{a_}: {x_.get('kural', '')} (`{k_}`{okr})".replace(":  (", ": ("))
    sn_ = s_.get("sinama") or {}
    for a_ in ("p_iki", "holm_girdisi"):  # 31.10.2026 bulgu 8 (H2)
        if isinstance(sn_.get(a_), dict):
            ks.append(f"{a_} `{sn_[a_]['kaynak']}`")
    for a_ in ("kurallar_sirasiyla", "etiketler_sirasiyla"):
        for r_ in s_.get(a_, []):
            ad = [x_ for x_ in ("i", "ii", "iii", "iv") if x_ in r_][0]
            k_ = r_.get("kaynak") or (r_.get("esik") or {}).get("kaynak")
            ks.append(f"({ad}) {r_[ad]}" + (f" (`{k_}`)" if k_ else ""))
    if isinstance(s_.get("kural"), str):
        ks.append(f"{s_['kural']} (`{s_['betik']['kaynak']}`)")
    elif isinstance(s_.get("betik"), dict):
        ks.append(f"betik `{s_['betik']['kaynak']}`")
    if s_.get("karar_sirasi"):
        ks.append("sira: " + s_["karar_sirasi"])
    return "; ".join(ks) or "-"


def _m13_karar(s_):
    g_ = s_["gerceklesen"]
    if "foy_satirlari" in g_:
        hucre = "; ".join(f"{m_} {v_}" for m_, v_ in g_["foy_hucreleri"].items())
        b_ = g_["bolgeye_uygulama"]
        okb = _m13_foy(b_["foy_satiri"], b_["satir_metni_sha256"], "M13.2 B6 bolge")
        okm = all([_m13_foy(n_, g_["foy_satir_metni_sha256"][m_], f"M13.2 B6 {m_}") for m_, n_ in g_["foy_satirlari"].items()])
        yer = (f"{g_['foy_bolum']} satir {min(g_['foy_satirlari'].values())}-{max(g_['foy_satirlari'].values())} "
               f"({'satirlar ayni' if okm else 'SATIR DEGISTI'}); "
               f"{b_['foy_bolum']} satir {b_['foy_satiri']} ({'satir ayni' if okb else 'SATIR DEGISTI'})")
        return (f"isaretli: {', '.join(g_['isaretli_json']) or 'yok'} (Isaretli sutunu: {hucre})", yer,
                _m9e(g_.get("json_ile_foy_ayni")))
    sha_ = g_.get("foy_satir_metni_sha256") or g_.get("satir_metni_sha256")
    ok_ = _m13_foy(g_["foy_satiri"], sha_, f"M13.2 {s_['kimlik']}/{s_['blok']}")
    karar = g_.get("foy_hucre", g_.get("deger"))
    if karar is None:
        karar = g_.get("not", "satir referansi")
    yer = f"{g_['foy_bolum']} satir {g_['foy_satiri']} ({'satir ayni' if ok_ else 'SATIR DEGISTI'})"
    return karar, yer, _m9e(g_.get("json_ile_foy_ayni")) if "json_ile_foy_ayni" in g_ else "-"


def _m13_2():
    J = _oku(_M13_KJ)
    L.append(f"Etiket (`etiket`): {J['etiket']}.\n")
    L.append(_m13meta(J, _M13_KJ) + "\n")
    st = [[k_, x_["ad"], _m13g(x_["deger"]), f"`{x_['kaynak']}`", f"`{x_['on_kayit']}`" if x_.get("on_kayit") else "-",
           " / ".join(x_.get("on_kayit_metninde_yazimi", [])) or "-"] for k_, x_ in J["sabitler"].items()]
    L.append("(a) Sabitler (`sabitler`; deger kaynak satirindan duzenli ifadeyle okunmus, on kayit satirinda ondalik "
             "virgullu yazimi aranmistir):\n")
    T(["Sabit", "Ad", "Deger", "Betik satiri", "On kayit satiri", "On kayitta bulunan yazim"], st)
    dt_ = J["delta_tost_tanimi"]
    ki = J["karar_ilkesi"]
    L.append(f"TOST siniri tanimi `{dt_['kaynak']}`; karar ilkesi `{ki['birincil']['kaynak']}` (ek on kayit "
             f"`{ki['ek']['kaynak']}`); hesaplanamayan sinamanin Holm'da p = 1 sayilmasi `{ki['hesaplanamayan_p_1']['kaynak']}`.\n")
    st = [[a_, x_["blok"], x_.get("veri", "-"), ", ".join(x_.get("sinamalar", [])) or "-", _m9e(x_["holm"]),
           _m13g(x_.get("aile_buyuklugu_json")), f"`{x_['on_kayit']['kaynak']}`", x_.get("not", "-")]
          for a_, x_ in J["aileler"].items()]
    L.append("(b) Aileler (`aileler`; aile buyuklugu sonuc JSON'undaki p_holm uzunlugundan):\n")
    T(["Aile", "Blok", "Veri", "Sinamalar", "Holm", "Aile buyuklugu (JSON)", "On kayit satiri", "Not"], st)
    st = []
    for s_ in J["sinamalar"]:
        karar, yer, ayni = _m13_karar(s_)
        ok_ = s_.get("on_kayit") or {}
        okk = ok_.get("kaynak") or "; ".join(f"{v_['kaynak']}" for v_ in ok_.values() if isinstance(v_, dict))
        oa_ = s_.get("ongoru_on_kayit")
        oal = f"\"{oa_['alinti']}\" (`{oa_['kaynak']}`)" if isinstance(oa_, dict) else "-"
        st.append([str(x_).replace("|", "\\|") for x_ in (
            s_["kimlik"], s_["blok"], s_["aile"], s_.get("nicelik", "-"), s_.get("ongoru", "-"), oal, _m13_esik(s_),
            _m13_kural(s_), f"`{okk}`", karar, yer, ayni)])
    L.append("(c) Sinamalar (`sinamalar`; 'Karar' sutunu foyun gosterilen tablo hucresidir, 'JSON ile ayni' sonuc JSON'unun "
             "karar anahtariyla, S satirlarinda b4.ikincil mantiksal anahtarlariyla karsilastirmadir, '-' karsilastirilmayan "
             "betimsel satirdir; 'Ongorulen buyukluk ve esikler' yalniz JSON'daki esik alanlarindan basilir, alan yoksa '-'; "
             "S satirlarinin ongorusu `ongoru` ve `ongoru_on_kayit` alanlarindandir; sonuc sayilari icin foy satirina bakilir):\n")
    T(["Sinama", "Blok", "Aile", "Nicelik", "Ongoru", "Ongoru (on kayit alintisi)", "Ongorulen buyukluk ve esikler",
       "Karar kurali (kaynak satirlari)", "On kayit satiri", "Karar (foy)", "Foy satiri", "JSON ile ayni"], st)
    b_ = J["sonuc_bolgesi"]
    g_ = b_["gerceklesen"]
    okb = _m13_foy(g_["foy_satiri"], g_["satir_metni_sha256"], "M13.2 sonuc bolgesi")
    L.append(f"Sonuc bolgesi (`sonuc_bolgesi`): denetim sirasi `{b_['sira']['kaynak']}`, on kayit tablosu "
             f"`{b_['on_kayit_tablosu']['kaynak']}`, sira cumlesi `{b_['on_kayit_sira']['kaynak']}`; gerceklesen bolge "
             f"{g_['bolge_json']} (O4 nitelemesi {_m9e(g_['O4_niteleme_json'])}; `{g_['json']}`), foy {g_['foy_bolum']} satir "
             f"{g_['foy_satiri']} ({'satir ayni' if okb else 'SATIR DEGISTI'}; satirda bolge var "
             f"{_m9e(g_['foy_satirinda_bolge_var'])}).\n")
    d_ = J["denetimler"]
    kz_ = "; ".join(f"{x_['kimlik']}/{x_['blok']} ({x_['neden']})" for x_ in d_.get("json_ile_foy_karsilastirilmayan", []))
    L.append(f"Denetimler (`denetimler`): sinama sayisi {d_['sinama_sayisi']}; JSON karari ile foy hucresi "
             f"(`json_ile_foy_ozet`): {d_.get('json_ile_foy_ozet', '-')}; ayni olmayan: {d_['json_ile_foy_ayni_olmayan'] or 'yok'}; "
             f"karsilastirilmayan (`json_ile_foy_karsilastirilmayan`): {kz_ or 'yok'}; dondurulmus "
             f"betik sha256 {d_['dondurulmus_betik_sha256']} (on kayit metninde geciyor {_m9e(d_['dondurulmus_betik_on_kayitla_ayni'])}; "
             f"dosyadan simdi hesaplanan {'AYNI' if _m9sha('experiments/q1_konsey_ayrisim.py') == d_['dondurulmus_betik_sha256'] else 'FARKLI'}); "
             f"JSON uretilirken okunan foyun ozeti (M13 bolumu cikarilmis metnin sha256'si, `foy_sha256_tanimi`) {d_['foy_sha256']}.\n")
    oa_ = d_.get("on_kayit_deger_aramasi")
    if oa_:
        L.append(f"On kayit metninde deger aramasi (`denetimler.on_kayit_deger_aramasi`; her esik ve sabitte "
                 f"`on_kayit_eslesmeleri` ve `on_kayit_aranan_yazimlar`): {oa_['denetlenen_deger_sayisi']} deger; kural: {oa_['kural']}\n")


_m13("M13.2 Kayit haritasi: on kayitli sinamalar, esikler, aileler ve gerceklesen kararlar (Y4, fig:registry_map)",
     f"`{_M13_KJ}` etiket, meta (foy_ozeti, yeniden_uretim_notu dahil); sabitler.<ad>.{{ad, deger, kaynak, on_kayit, "
     f"on_kayit_metninde_yazimi, on_kayit_eslesmeleri, on_kayit_aranan_yazimlar}}; delta_tost_tanimi; "
     f"karar_ilkesi; aileler.<aile>.{{blok, veri, sinamalar, holm, aile_buyuklugu_json, on_kayit, not}}; sinamalar[].{{kimlik, "
     f"blok, aile, nicelik, ongoru, ongoru_on_kayit, ongoru_turu, ongorulen_buyukluk, esdegerlik_siniri, ongoru_dogrusu, "
     f"sinama (p_iki, holm_girdisi dahil), destek, curutme (kural, on_kayit dahil), payda_kurali, kurallar_sirasiyla, "
     f"etiketler_sirasiyla, esik, bant, beklenti_esigi, on_kayit, gerceklesen (karar_json, json_ile_foy_ayni, "
     f"json_ile_foy_karsilastirma dahil)}}; sonuc_bolgesi; denetimler", _m13_2)


# --- M13.3 Zaman cizelgesi -------------------------------------------------------------------
def _m13_3():
    J = _oku(_M13_ZJ)
    L.append(f"Etiket (`etiket`): {J['etiket']}.\n")
    L.append(_m13meta(J, _M13_ZJ) + "\n")
    sd = J["saat_dilimi"]
    L.append(f"Saat dilimi (`saat_dilimi`): konsey zinciri gunlugu, durum TSV'si ve B3 defteri UTC'ye gore "
             f"{sd['konsey_zinciri_saat_farki_utc_gore']} saat fark; ek zincir gunlukleri {sd['ek_zincir_saat_farki_utc_gore']} "
             f"saat fark. Kanit: " + "; ".join(f"{x_['etiket']} (artik {x_['artik_s']} s, JSON zamani adim icinde "
                                            f"{_m9e(x_['json_zamani_adim_icinde'])})"
                                            for x_ in sd["konsey_zinciri_kanit"] + sd["ek_zincir_kanit"]) + ".\n")
    sat = []
    for a_, x_ in J["dondurma"].items():
        sat.append((x_["utc"], [f"{'On kayit' if a_ == 'on_kayit' else 'Ek on kayit'} dondurma (commit {x_['commit'][:7]})",
                                _m13t(x_["utc"]), "-", "-", f"`{x_['kaynak']}`; dosyayi ekleyen ilk commit "
                                f"{_m9e(x_['dondurma_commiti_dosyayi_ekleyen_ilk_commit'])}"]))
    b2 = J["B2"]
    sat.append((b2["baslangic_utc"], [b2["olay"], _m13t(b2["baslangic_utc"]), _m13t(b2["bitis_utc"]), b2["sure_s"],
                                       f"{b2['kaynak']} ({b2['kanit_turu']})"]))
    for x_ in J["konsey_zinciri"]:
        sat.append((x_["baslangic_utc"] or x_["bitis_utc"], [f"konsey zinciri: {x_['olay']} ({x_['durum']})",
                    _m13t(x_["baslangic_utc"]), _m13t(x_["bitis_utc"]), _m13g(x_.get("sure_s")), f"`{x_['kaynak']}`"]))
    for x_ in J["B3_asamalari"]:
        sat.append((x_["baslangic_utc"], [x_["olay"], _m13t(x_["baslangic_utc"]), _m13t(x_["bitis_utc"]), x_["sure_s"],
                                          f"`{x_['kaynak']}`; defter `{x_['defter_satiri']}`"]))
    for x_ in J["ek_zincir"]:
        sat.append((x_["baslangic_utc"], [x_["olay"] + (f" ({'; '.join(x_['donus_kodlari'])})" if x_["donus_kodlari"] else ""),
                                          _m13t(x_["baslangic_utc"]), _m13t(x_["bitis_utc"]), x_["sure_s"],
                                          f"`{x_['kaynak']}` (bitis: {x_['bitis_tanimi']})"]))
    for p_, x_ in J["masa_cozumlemeleri"].items():
        sat.append((x_["uretildi_utc"], [f"masa cozumlemesi: {p_.rsplit('/', 1)[-1]}", _m13t(x_["uretildi_utc"]), "-", "-",
                                         f"`{p_}` {x_['anahtar']}"]))
    sat.sort(key=lambda z_: z_[0])
    L.append("(a) Olaylar, UTC'ye gore sirali (`dondurma`, `B2`, `konsey_zinciri`, `B3_asamalari`, `ek_zincir`, "
             "`masa_cozumlemeleri`; +03 karsiliklari JSON'da `*_yerel` alanlarinda; sure gunluk saatlerinin farkidir, s):\n")
    T(["Olay", "Baslangic (UTC)", "Bitis (UTC)", "Sure (s)", "Kaynak"], [z_[1] for z_ in sat])
    st = [[b_, x_.get("saldiri", "-"), x_["n_goruntu"] if "n_goruntu" in x_ else "-", x_["model_sayisi"],
           x_.get("hucre_sayisi", x_.get("cift_sayisi", "-")), _m13g(x_.get("eps_x255")), f"`{x_['kaynak']}`"]
          for b_, x_ in J["matrisler"].items()]
    L.append("(b) Blok basina matris boyutlari (`matrisler`; B10 satirlarinda 'Hucre' sutunu sirasiz cift sayisidir):\n")
    T(["Blok", "Saldiri", "n goruntu", "Model", "Hucre / cift", "eps x 255", "Kaynak"], st)
    dn, eg = J["donanim"], J["egitim_suresi"]
    okt = _m13_foy(eg["foy"]["foy_satiri"], eg["foy"]["satir_metni_sha256"], "M13.3 toplam egitim")
    foy_s = "\n".join(L).split("\n")[eg["foy"]["foy_satiri"] - 1]
    top_ayni = f"{eg['defter_toplam_sure_sa']:.2f}" in foy_s
    L.append(f"Donanim (`donanim`): {dn['gpu']}, toplam bellek {dn['gpu_bellek_toplam_mib']} MiB, zincir basinda kullanilan "
             f"{dn['gpu_bellek_kullanilan_mib_zincir_basi']} MiB (`{dn['kaynak']}`); ek zincir basinda kullanilan "
             f"{dn['ek_zincir_bellek']['kullanilan_mib']} / {dn['ek_zincir_bellek']['toplam_mib']} MiB "
             f"(`{dn['ek_zincir_bellek']['kaynak']}`). B3 toplam egitim suresi bu bolumde tekrarlanmaz: M9.1 satir "
             f"{eg['foy']['foy_satiri']} ({'satir ayni' if okt else 'SATIR DEGISTI'}); `{eg['kaynak']}` ile yeniden hesaplanan "
             f"toplam iki ondalikta o satirdaki degerle ayni {_m9e(top_ayni)}; "
             f"zincir gunlugu karsiligi `{eg['zincir_gunlugu_satiri']}`; egitim payi on kayit `{eg['egitim_payi_on_kayit']}`.\n")
    st = [[x_["tarih"], x_["baslik"], _m9e(x_["sapma_degil_ibaresi"]), f"`{x_['kaynak']}`"] for x_ in J["sapma_kaydi_basliklari"]]
    L.append("(c) Sapma kaydi basliklari (`sapma_kaydi_basliklari`; `results/q1_research/ONKAYIT_SAPMALAR.md` '###' "
             "satirlari):\n")
    T(["Tarih", "Baslik", "'sapma degil' ibaresi", "Kaynak"], st)
    kg = J["kayit_oncesi_gorulen_veriler"]
    d_ = J["denetimler"]
    L.append(f"Kayit oncesi gorulen veriler (`kayit_oncesi_gorulen_veriler`): ana on kayit `{kg['ana']}`, ek on kayit "
             f"`{kg['ek']}`. Denetimler (`denetimler`): B3 asama sayisi {d_['B3_asama_sayisi']}; defter baslangiclari zincir "
             f"gunluguyle ayni {_m9e(d_['B3_defter_baslangiclari_zincir_gunluguyle_ayni'])}; defter ile gunluk bitis farki en "
             f"buyuk {d_['B3_defter_bitis_farki_s_en_buyuk_mutlak']} s; on kayit dondurmasi B2 matrisinden once "
             f"{_m9e(d_['on_kayit_dondurmasi_B2_matrisinden_once'])}; ek dondurma B3 kuyrugu sirasinda "
             f"{_m9e(d_['ek_dondurma_konsey_zinciri_icinde'])}; ek dondurma ek zincirden once "
             f"{_m9e(d_['ek_dondurma_ek_zincirden_once'])}.\n")
    _M13_YOK_YER.append(len(L))
    L.append("")


_m13("M13.3 On kayit ve deney zinciri zaman cizelgesi (Y5, fig:prereg_chain)",
     f"`{_M13_ZJ}` etiket, meta (foy_ozeti, yeniden_uretim_notu dahil); saat_dilimi; dondurma.<on_kayit|ek_on_kayit>.{{commit, utc, kaynak, "
     f"dondurma_commiti_dosyayi_ekleyen_ilk_commit}}; B2; konsey_zinciri[]; B3_asamalari[]; ek_zincir[]; masa_cozumlemeleri; "
     f"matrisler; donanim; egitim_suresi; sapma_kaydi_basliklari; kayit_oncesi_gorulen_veriler; denetimler", _m13_3)

for _i13 in _M13_YOK_YER:
    L[_i13] = ("Bu bolumde (M13.1-M13.3) satir sha256'si JSON'daki kayittan farkli cikan foy referanslari: "
               + ("; ".join(_M13_DEGISEN) if _M13_DEGISEN else "yok") + ".\n")

# <<< M13 SONU (sekil kaynaklari Y1, Y4, Y5)


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
