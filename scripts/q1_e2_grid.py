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
PATIENCES = [0, 10, 20]      # 0 = saf argmax
KERNELS = [1, 3, 5]
MIN_DELTA = 0.1
REF_PROTOCOL = ("B", 20, 1)  # tohum sd'si bu SABIT protokolde olculur (on-kayitli kural)


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
        }

    # Konvansiyon dayanikliligi: manset (yayilim ve oran) konvansiyona bagli mi?
    if args.conventions:
        rob = {}
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
              f"oran {r['oran_protokol_sd_bolu_tohum_sd']}x")


if __name__ == "__main__":
    main()
