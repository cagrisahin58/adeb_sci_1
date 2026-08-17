"""E2 A1: SECIM-PROTOKOLU IZGARASI (yeni manset; hakem denetimi 2026-08-17).

NEDEN: Onceki manset "secim bolmesi degisince raporlanan dogruluk 1,67 puana
kadar oynuyor" n=3'un MAKSIMUMUnu raporluyordu (diger cekilisler 0,00 ve 0,00)
ve "tohum yayiliminin 3 kati" orani MAKSIMUM/SD karsilastirmasiydi (esli oranda
ResNet'te 0,77x, yani TERSINE donuyor). Bu betik yerine gecen dayanikli manseti
uretir: sabit bir yorunge uzerinde SECIM PROTOKOLUNUN uc serbestlik derecesi
taranir ve raporlanan dogruluk GERCEK 10k test kumesinden okunur.

IZGARA (yorunge basina 18 hucre):
  secici bolme  x  patience      x  yumusatma
  V_B, V_C         0, 10, 20        k = 1, 3, 5
(V_A haric: sizintili bolme; ayri raporlanir. Patience 0 = saf argmax.)

Her hucre: secim kurali (min_delta 0.1) SMOOTHED val-adv egrisine uygulanir ->
secilen epok -> o epogun GERCEK test PGD-10 dogrulugu (testcurve_*.npz).

ESLI KARSILASTIRMA (hakemin talebi): protokol sd'si ile TOHUM sd'si AYNI
istatistik turunde kiyaslanir - protokol sd = 18 hucrenin sd'si (yorunge ici),
tohum sd = protokol SABITken 3 tohumun sd'si. Maksimumlar yalniz dagilimin uc
noktasi olarak raporlanir, tek basina ASLA.

Yumusatma konvansiyonu: KENAR-DOLGULU merkezi hareketli ortalama (kayitli:
"edge-padded centered"). Diger uc konvansiyon q1_e2_smoothing.py'de.

Kullanim: python scripts/q1_e2_grid.py
Cikti: results/q1/e2/e2_grid.json
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT / "scripts"))
from q1_offline_select import simulate_selection  # noqa: E402

SPLITS = ["B", "C"]          # yalniz TEMIZ bolmeler (V_A ayri raporlanir)
# DIKKAT (R3 denetimi): patience=0 SAF ARGMAX DEGILDIR - simulate_selection'da
# min_delta kosulsuz uygulanir, yani "kosan en iyiyi 0.1 puandan fazla asan SON
# epok" (cirit/ratchet) kurali cikar. 54 hucrenin 13'unde gercek argmax'tan
# farkli epok seciyor (test etkisi 2.37 puana kadar). Gercek argmax ayri bir
# kol olarak (ARGMAX_ARM) raporlanir.
PATIENCES = [0, 10, 20]      # 0 = erken durdurma yok (min_delta esigi HALA aktif)
KERNELS = [1, 3, 5]
MIN_DELTA = 0.1
REF_PROTOCOL = ("B", 20, 1)  # varsayilan referans; DUYARLILIK 18 referansta taranir
# Makalelerin fiilen degistirdigi cekirdek: bolme x patience (yumusatma HARIC).
# Yumusatma notr bir alternatif degil, monoton kotulestirici bir seci ci
# oldugundan yayilimin buyuk kismini o tasiyor; cekirdek ayri raporlanir.
CORE_KERNEL = 1


def smooth(y, k, conv="edge"):
    """Hareketli ortalama. conv: edge|zero|valid|causal.

    Hakem denetimi (2026-08-17) onceki bir yumusatma sayisinin konvansiyona
    bagli oldugunu gosterdi; bu yuzden konvansiyon acikca parametrik ve
    --conventions ile dordu birden taranabiliyor.
    """
    if k <= 1:
        return np.asarray(y, dtype=float)
    y = np.asarray(y, dtype=float)
    pad = k // 2
    ker = np.ones(k) / k
    if conv == "edge":       # kenar degerleriyle dolgu (varsayilan)
        yp = np.concatenate([np.full(pad, y[0]), y, np.full(pad, y[-1])])
        return np.convolve(yp, ker, mode="valid")
    if conv == "zero":       # sifir dolgu (uclarda asagi cekilir)
        return np.convolve(y, ker, mode="same")
    if conv == "valid":      # uclar kirpilmaz, kismi pencere ortalamasi
        out = np.empty_like(y)
        for i in range(y.size):
            lo, hi = max(0, i - pad), min(y.size, i + pad + 1)
            out[i] = y[lo:hi].mean()
        return out
    if conv == "causal":     # yalniz gecmise bakan (online secim gercekci hali)
        out = np.empty_like(y)
        for i in range(y.size):
            out[i] = y[max(0, i - k + 1):i + 1].mean()
        return out
    raise ValueError(conv)


def load_traj(in_dir, arch, seed):
    """Bir yorungenin val egrileri (A/B/C) + GERCEK test egrisi."""
    tc_path = in_dir / f"testcurve_{arch}_s{seed}.npz"
    if not tc_path.exists():
        return None
    tc = np.load(tc_path)
    out = {"epochs": tc["epochs"].astype(int),
           "test_adv": tc["adv_acc"].astype(float),
           "test_clean": tc["clean_acc"].astype(float), "val": {}}
    for c in "ABC":
        vp = in_dir / f"select_{arch}_s{seed}_val{c}_valcurve.npz"
        if not vp.exists():
            return None
        z = np.load(vp)
        assert list(z["epochs"].astype(int)) == list(out["epochs"]), "epok dizileri farkli"
        out["val"][c] = {"adv": 100.0 * z["adv_mask"].mean(axis=1),
                         "clean": 100.0 * z["clean_mask"].mean(axis=1)}
    return out


def run_cell(traj, split, patience, k, conv="edge"):
    """Bir protokol hucresi: secim -> GERCEK test dogrulugu."""
    ep = traj["epochs"]
    adv = smooth(traj["val"][split]["adv"], k, conv)
    cln = smooth(traj["val"][split]["clean"], k, conv)
    sel_ep, _, stop = simulate_selection(
        list(zip(ep.tolist(), cln.tolist(), adv.tolist())),
        patience=patience, min_delta=MIN_DELTA)
    if sel_ep is None:
        return None
    i = int(np.where(ep == sel_ep)[0][0])
    return {"split": split, "patience": patience, "k": k,
            "secilen_epok": int(sel_ep),
            "test_adv": round(float(traj["test_adv"][i]), 4),
            "test_clean": round(float(traj["test_clean"][i]), 4),
            "durus": stop}


def run_argmax_cell(traj, split, k, conv="edge"):
    """GERCEK saf argmax kolu (min_delta/ratchet yok) - patience=0'in dogrusu."""
    ep = traj["epochs"]
    adv = smooth(traj["val"][split]["adv"], k, conv)
    i = int(np.argmax(adv))
    return {"split": split, "patience": "argmax", "k": k,
            "secilen_epok": int(ep[i]),
            "test_adv": round(float(traj["test_adv"][i]), 4),
            "test_clean": round(float(traj["test_clean"][i]), 4)}


def ref_sensitivity(per_seed, seeds):
    """Oranin REFERANS PROTOKOL secimine duyarliligi (18 referansin tamami).

    R3 denetimi: tek sabit referansla (V_B,20,1) hesaplanan oran, ayna referansla
    (V_C,20,1) ViT'te 2.17x -> 0.63x'e donuyordu. Tek sayi yerine dagilim verilir.
    """
    keys = [(s, p, k) for s in SPLITS for p in PATIENCES for k in KERNELS]
    prot_sd = float(np.mean([per_seed[str(s)]["sd"] for s in seeds]))
    out = []
    for key in keys:
        vals = []
        for s in seeds:
            c = next((c for c in per_seed[str(s)]["hucreler"]
                      if (c["split"], c["patience"], c["k"]) == key), None)
            if c:
                vals.append(c["test_adv"])
        if len(vals) == len(seeds) and len(vals) > 1:
            ssd = float(np.std(vals, ddof=1))
            out.append({"referans": f"V_{key[0]}/p{key[1]}/k{key[2]}",
                        "tohum_sd": round(ssd, 4),
                        "oran": round(prot_sd / ssd, 3) if ssd > 1e-9 else None})
    oranlar = [o["oran"] for o in out if o["oran"] is not None]
    return {"referanslar": out,
            "oran_min": round(min(oranlar), 3), "oran_max": round(max(oranlar), 3),
            "oran_medyan": round(float(np.median(oranlar)), 3),
            "birin_altinda_referans_sayisi": int(sum(1 for o in oranlar if o <= 1.0)),
            "toplam_referans": len(oranlar)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default=str(ROOT / "results/q1/e2"))
    ap.add_argument("--out", default=str(ROOT / "results/q1/e2/e2_grid.json"))
    ap.add_argument("--conv", default="edge", choices=["edge", "zero", "valid", "causal"])
    ap.add_argument("--conventions", action="store_true",
                    help="Dort yumusatma konvansiyonunu tarayip dayanikliligi raporla")
    args = ap.parse_args()
    in_dir = Path(args.in_dir)

    ARCHS = {"resnet18": [1001, 1002, 1003], "vit_tiny": [2001, 2002, 2003]}
    report = {"izgara": {"bolmeler": SPLITS, "patience": PATIENCES, "yumusatma_k": KERNELS,
                         "min_delta": MIN_DELTA, "hucre_sayisi": len(SPLITS) * len(PATIENCES) * len(KERNELS),
                         "yumusatma_konvansiyonu": "kenar-dolgulu merkezi hareketli ortalama",
                         "uc_nokta": "GERCEK 10k test PGD-10 (testcurve_*.npz)"},
              "referans_protokol": {"bolme": REF_PROTOCOL[0], "patience": REF_PROTOCOL[1],
                                    "k": REF_PROTOCOL[2]},
              "mimariler": {}}

    for arch, seeds in ARCHS.items():
        per_seed, ref_vals = {}, []
        for seed in seeds:
            traj = load_traj(in_dir, arch, seed)
            if traj is None:
                print(f"ATLA {arch}_s{seed}: testcurve veya valcurve eksik")
                continue
            cells = [run_cell(traj, s, p, k, args.conv)
                     for s in SPLITS for p in PATIENCES for k in KERNELS]
            cells = [c for c in cells if c]
            # GERCEK argmax kolu (patience=0'in yanlis etiketlenmesine karsi)
            argmax_cells = [run_argmax_cell(traj, s, k, args.conv)
                            for s in SPLITS for k in KERNELS]
            # ratchet (patience=0) ile gercek argmax kac hucrede ayrisiyor?
            ratchet_diff = []
            for a in argmax_cells:
                r = next(c for c in cells if c["split"] == a["split"]
                         and c["patience"] == 0 and c["k"] == a["k"])
                if r["secilen_epok"] != a["secilen_epok"]:
                    ratchet_diff.append({"split": a["split"], "k": a["k"],
                                         "ratchet_epok": r["secilen_epok"],
                                         "argmax_epok": a["secilen_epok"],
                                         "test_fark": round(a["test_adv"] - r["test_adv"], 4)})
            vals = np.array([c["test_adv"] for c in cells])
            oracle_i = int(np.argmax(traj["test_adv"]))
            ref = next(c for c in cells if (c["split"], c["patience"], c["k"]) == REF_PROTOCOL)
            ref_vals.append(ref["test_adv"])
            per_seed[str(seed)] = {
                "hucreler": cells,
                "yayilim": round(float(vals.max() - vals.min()), 4),
                "sd": round(float(vals.std(ddof=1)), 4),
                "min": round(float(vals.min()), 4), "max": round(float(vals.max()), 4),
                "essiz_epok": sorted({c["secilen_epok"] for c in cells}),
                "oracle": {"epok": int(traj["epochs"][oracle_i]),
                           "test_adv": round(float(traj["test_adv"][oracle_i]), 4)},
                "ort_oracle_pismanligi": round(float(traj["test_adv"][oracle_i] - vals.mean()), 4),
                # hangi serbestlik derecesi ne kadar oynatiyor (marjinal yayilim)
                "_argmax": argmax_cells,
                "_ratchet": ratchet_diff,
                "kaldirac": {
                    "bolme": round(float(np.ptp([np.mean([c["test_adv"] for c in cells if c["split"] == s])
                                                 for s in SPLITS])), 4),
                    "patience": round(float(np.ptp([np.mean([c["test_adv"] for c in cells if c["patience"] == p])
                                                    for p in PATIENCES])), 4),
                    "yumusatma": round(float(np.ptp([np.mean([c["test_adv"] for c in cells if c["k"] == k])
                                                     for k in KERNELS])), 4),
                },
            }
        if not per_seed:
            continue
        prot_sds = [per_seed[s]["sd"] for s in per_seed]
        seed_sd = float(np.std(ref_vals, ddof=1)) if len(ref_vals) > 1 else float("nan")
        done_seeds = [int(s) for s in per_seed]
        # CEKIRDEK IZGARA (k=1): makalelerin fiilen degistirdigi boyutlar
        core_sds, core_ref = [], []
        for s in done_seeds:
            cv = [c["test_adv"] for c in per_seed[str(s)]["hucreler"] if c["k"] == CORE_KERNEL]
            core_sds.append(float(np.std(cv, ddof=1)))
            core_ref.append(next(c["test_adv"] for c in per_seed[str(s)]["hucreler"]
                                 if (c["split"], c["patience"], c["k"]) == REF_PROTOCOL))
        core_seed_sd = float(np.std(core_ref, ddof=1)) if len(core_ref) > 1 else float("nan")
        report["mimariler"][arch] = {
            "tohum_sayisi": len(per_seed),
            "per_seed": per_seed,
            "protokol_sd_ort": round(float(np.mean(prot_sds)), 4),
            "protokol_sd_araligi": [round(min(prot_sds), 4), round(max(prot_sds), 4)],
            "protokol_yayilim_araligi": [round(min(per_seed[s]["yayilim"] for s in per_seed), 4),
                                         round(max(per_seed[s]["yayilim"] for s in per_seed), 4)],
            "tohum_sd_referans_protokolde": round(seed_sd, 4),
            "oran_protokol_sd_bolu_tohum_sd": round(float(np.mean(prot_sds) / seed_sd), 3)
            if seed_sd and not np.isnan(seed_sd) else None,
            "REFERANS_DUYARLILIGI": ref_sensitivity(per_seed, done_seeds),
            "cekirdek_k1": {
                "aciklama": "yalniz bolme x patience (yumusatma HARIC; yumusatma "
                            "cogu yorungede tek yonlu kotulestirici oldugu icin "
                            "yayilimi sisiriyor - monotonluk sayimi asagida)",
                "protokol_sd_ort": round(float(np.mean(core_sds)), 4),
                "tohum_sd": round(core_seed_sd, 4),
                "oran": round(float(np.mean(core_sds)) / core_seed_sd, 3)
                if core_seed_sd and not np.isnan(core_seed_sd) else None,
            },
            "yumusatma_marjinal_ortalamalari": {
                str(s): {str(k): round(float(np.mean([c["test_adv"] for c in
                                                      per_seed[str(s)]["hucreler"] if c["k"] == k])), 4)
                         for k in KERNELS} for s in done_seeds},
            "argmax_kolu": {str(s): per_seed[str(s)].pop("_argmax") for s in per_seed},
            "ratchet_vs_argmax": {str(s): per_seed[str(s)].pop("_ratchet") for s in per_seed},
        }
        # Yumusatma MONOTON MU? (belge "her yorungede monoton" diyordu; sayilir)
        ym = report["mimariler"][arch]["yumusatma_marjinal_ortalamalari"]
        mono = {s: bool(all(ym[s][str(KERNELS[i])] >= ym[s][str(KERNELS[i + 1])]
                            for i in range(len(KERNELS) - 1))) for s in ym}
        report["mimariler"][arch]["yumusatma_monoton_mu"] = {
            "per_seed": mono, "monoton_sayisi": int(sum(mono.values())), "toplam": len(mono)}
        # ratchet-argmax ayrisma sayimi ve en buyuk test etkisi
        rv = [d for s in report["mimariler"][arch]["ratchet_vs_argmax"]
              for d in report["mimariler"][arch]["ratchet_vs_argmax"][s]]
        report["mimariler"][arch]["ratchet_ozet"] = {
            "ayrisan_hucre": len(rv),
            "toplam_hucre": len(SPLITS) * len(KERNELS) * len(done_seeds),
            "max_abs_test_fark": round(max((abs(d["test_fark"]) for d in rv), default=0.0), 4)}
        # argmax koluyla yayilim/oran (etiket hatasina karsi dayaniklilik)
        am_sds, am_spread = [], []
        for s in done_seeds:
            av = [c["test_adv"] for c in report["mimariler"][arch]["argmax_kolu"][str(s)]]
            am_sds.append(float(np.std(av, ddof=1)))
            am_spread.append(float(max(av) - min(av)))
        report["mimariler"][arch]["argmax_kolu_ozet"] = {
            "yayilim_araligi": [round(min(am_spread), 4), round(max(am_spread), 4)],
            "protokol_sd_ort": round(float(np.mean(am_sds)), 4)}
        # oranin n=3 belirsizligi (tohum sd'sinin chi2 GA'si)
        if len(done_seeds) > 1 and seed_sd and seed_sd > 1e-9:
            from scipy.stats import chi2 as _chi2
            dfree = len(done_seeds) - 1
            pm = float(np.mean(prot_sds))
            lo = pm / np.sqrt(seed_sd ** 2 * dfree / _chi2.ppf(0.025, dfree))
            hi = pm / np.sqrt(seed_sd ** 2 * dfree / _chi2.ppf(0.975, dfree))
            report["mimariler"][arch]["oran_95_GA"] = [round(hi, 3), round(lo, 3)]

    # Konvansiyon dayanikliligi: manset (yayilim ve oran) konvansiyona bagli mi?
    if args.conventions:
        rob = {}
        # konvansiyonlar HUCRE DUZEYINDE ozdes mi? (belge "dort konvansiyon"
        # diyordu; R3 ucunun ozdes secim verdigini buldu - burada sayilir)
        ident = {}
        base = {}
        for conv in ["edge", "zero", "valid", "causal"]:
            picks = []
            for arch, seeds in ARCHS.items():
                for seed in seeds:
                    traj = load_traj(in_dir, arch, seed)
                    if traj is None:
                        continue
                    picks += [c["secilen_epok"] for c in
                              (run_cell(traj, s, p, k, conv) for s in SPLITS
                               for p in PATIENCES for k in KERNELS) if c]
            base[conv] = picks
        ref = base["edge"]
        for conv, picks in base.items():
            same = sum(1 for a, b in zip(ref, picks) if a == b)
            ident[conv] = {"edge_ile_ayni_hucre": same, "toplam_hucre": len(ref)}
        report["konvansiyon_hucre_ozdesligi"] = ident
        print("\nKONVANSIYON HUCRE OZDESLIGI (edge referans):")
        for conv, d in ident.items():
            print(f"  {conv:<7} {d['edge_ile_ayni_hucre']}/{d['toplam_hucre']} hucrede ayni secim")
        for conv in ["edge", "zero", "valid", "causal"]:
            per_arch = {}
            for arch, seeds in ARCHS.items():
                sds, spreads, refs = [], [], []
                for seed in seeds:
                    traj = load_traj(in_dir, arch, seed)
                    if traj is None:
                        continue
                    cs = [c for c in (run_cell(traj, s, p, k, conv)
                                      for s in SPLITS for p in PATIENCES for k in KERNELS) if c]
                    v = np.array([c["test_adv"] for c in cs])
                    sds.append(float(v.std(ddof=1)))
                    spreads.append(float(v.max() - v.min()))
                    refs.append(next(c["test_adv"] for c in cs
                                     if (c["split"], c["patience"], c["k"]) == REF_PROTOCOL))
                if len(refs) > 1:
                    ssd = float(np.std(refs, ddof=1))
                    per_arch[arch] = {"protokol_sd_ort": round(float(np.mean(sds)), 4),
                                      "yayilim_araligi": [round(min(spreads), 4), round(max(spreads), 4)],
                                      "tohum_sd": round(ssd, 4),
                                      "oran": round(float(np.mean(sds)) / ssd, 3) if ssd else None}
            rob[conv] = per_arch
        report["konvansiyon_dayanikliligi"] = rob
        print("\nKONVANSIYON DAYANIKLILIGI (protokol sd / tohum sd):")
        for conv, pa in rob.items():
            s = "  ".join(f"{a}: {d['oran']}x (yayilim {d['yayilim_araligi'][0]:.2f}-"
                          f"{d['yayilim_araligi'][1]:.2f})" for a, d in pa.items())
            print(f"  {conv:<7} {s}")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out + ".tmp", "w") as f:
        json.dump(report, f, indent=2)
    os.replace(args.out + ".tmp", args.out)

    print(f"\n=== E2 PROTOKOL IZGARASI ({report['izgara']['hucre_sayisi']} hucre/yorunge; "
          f"uc nokta: gercek 10k test) -> {args.out} ===")
    for arch, r in report["mimariler"].items():
        print(f"\n{arch} ({r['tohum_sayisi']} tohum)")
        for s, d in r["per_seed"].items():
            kal = d["kaldirac"]
            print(f"  s{s}: yayilim {d['yayilim']:.2f} sd {d['sd']:.2f} | "
                  f"{d['min']:.2f}-{d['max']:.2f} | {len(d['essiz_epok'])} essiz epok | "
                  f"oracle ep{d['oracle']['epok']} {d['oracle']['test_adv']:.2f} "
                  f"(ort pismanlik {d['ort_oracle_pismanligi']:.2f})")
            print(f"       kaldirac: bolme {kal['bolme']:.2f} | patience {kal['patience']:.2f} | "
                  f"yumusatma {kal['yumusatma']:.2f}")
        print(f"  PROTOKOL sd {r['protokol_sd_ort']:.2f} "
              f"(aralik {r['protokol_sd_araligi'][0]:.2f}-{r['protokol_sd_araligi'][1]:.2f}) vs "
              f"TOHUM sd {r['tohum_sd_referans_protokolde']:.2f} -> "
              f"oran {r['oran_protokol_sd_bolu_tohum_sd']}x  [varsayilan referans]")
        rs = r["REFERANS_DUYARLILIGI"]
        print(f"  REFERANS DUYARLILIGI: oran {rs['oran_min']}x - {rs['oran_max']}x "
              f"(medyan {rs['oran_medyan']}x); {rs['birin_altinda_referans_sayisi']}/"
              f"{rs['toplam_referans']} referansta oran <= 1")
        ck = r["cekirdek_k1"]
        print(f"  CEKIRDEK (k=1, bolme x patience): protokol sd {ck['protokol_sd_ort']:.2f} / "
              f"tohum sd {ck['tohum_sd']:.2f} -> oran {ck['oran']}x")


if __name__ == "__main__":
    main()
