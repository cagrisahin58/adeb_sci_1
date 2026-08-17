"""E2 A2: bolme bootstrap'i BIRINCIL UC NOKTADA (hakem talebi 2026-08-17).

NEDEN: q1_e2_bootstrap.py secim kararsizligini olcuyordu ama degerlendirmeyi
VEKIL bir val bolmesiyle yapiyordu (val->test aktarimi zayif: secilen epok
ciftlerinde egim ~0.46, artik sd ~0.79 puan). P0 sonrasi artik her checkpoint'in
GERCEK 10k test dogrulugu elimizde; bu betik ayni bootstrap'i birincil uc
noktada tekrarlar.

Ayrica hakemin KRITIK itirazina cevap verir: "1,67 / 0,82 puan" n=3'un
MAKSIMUMUydu (diger cekilisler 0,00). Bootstrap, raporlanan degerin ORNEKLEME
DAGILIMINI verir (sd, %95 aralik, oracle pismanligi) - yani bolme duzeyinde
n=1 sinirlamasini yeni egitim olmadan onarir.

TASARIM: secici bolme = V_B (veya V_C) icinden 2000'lik bootstrap yeniden
ornekleme -> on-kayitli secim kurali (patience 20, min_delta 0.1) -> secilen
epogun GERCEK 10k test PGD-10 dogrulugu. Ayrica iki bagimsiz cekilisin farki =
sifir-sizinti altindaki Delta dagilimi (birincil uc noktada).

Kullanim: python scripts/q1_e2_split_bootstrap.py --n-boot 5000
Cikti: results/q1/e2/e2_split_bootstrap.json
"""
import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT / "scripts"))
from q1_offline_select import simulate_selection  # noqa: E402

ARCHS = {"resnet18": [1001, 1002, 1003], "vit_tiny": [2001, 2002, 2003]}
MIN_DELTA, PATIENCE = 0.1, 20


def bootstrap_selections(val_clean, val_adv, epochs, test_adv, n_boot, rng):
    """Bootstrap bolmelerle secim -> GERCEK test dogrulugu dagilimi."""
    n = val_adv.shape[1]
    picks, vals = np.empty(n_boot, dtype=np.int32), np.empty(n_boot)
    w = np.full(n, 1.0 / n)
    for b in range(n_boot):
        counts = rng.multinomial(n, w).astype(np.float64)
        adv = 100.0 * (val_adv @ counts) / n
        cln = 100.0 * (val_clean @ counts) / n
        ep, _, _ = simulate_selection(
            list(zip(epochs.tolist(), cln.tolist(), adv.tolist())),
            patience=PATIENCE, min_delta=MIN_DELTA)
        i = int(np.where(epochs == ep)[0][0]) if ep is not None else int(np.argmax(adv))
        picks[b] = epochs[i]
        vals[b] = test_adv[i]
    return picks, vals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default=str(ROOT / "results/q1/e2"))
    ap.add_argument("--out", default=str(ROOT / "results/q1/e2/e2_split_bootstrap.json"))
    ap.add_argument("--n-boot", type=int, default=5000)
    ap.add_argument("--seed", type=int, default=20260817)
    args = ap.parse_args()
    in_dir = Path(args.in_dir)
    rng = np.random.default_rng(args.seed)

    out = {"kesifsel": True, "n_boot": args.n_boot, "seed": args.seed,
           "uc_nokta": "GERCEK 10k test PGD-10 (testcurve_*.npz)",
           "secim_kurali": {"patience": PATIENCE, "min_delta": MIN_DELTA},
           "yorungeler": {}}

    print(f"{'yorunge':<18}{'bolme':>7}{'ort':>8}{'sd':>7}{'%95 aralik':>16}"
          f"{'oracle':>8}{'pismanlik':>11}{'essiz_ep':>9}")
    for arch, seeds in ARCHS.items():
        for seed in seeds:
            tag = f"{arch}_s{seed}"
            tc_p = in_dir / f"testcurve_{tag}.npz"
            if not tc_p.exists():
                print(f"ATLA {tag}: testcurve yok")
                continue
            tc = np.load(tc_p)
            epochs, test_adv = tc["epochs"].astype(int), tc["adv_acc"].astype(float)
            oracle = float(test_adv.max())
            res = {"oracle_test_adv": round(oracle, 4),
                   "oracle_epok": int(epochs[int(np.argmax(test_adv))]), "bolmeler": {}}
            store = {}
            for c in ["B", "C"]:
                vp = in_dir / f"select_{tag}_val{c}_valcurve.npz"
                if not vp.exists():
                    continue
                z = np.load(vp)
                picks, vals = bootstrap_selections(
                    z["clean_mask"].astype(np.float64), z["adv_mask"].astype(np.float64),
                    epochs, test_adv, args.n_boot, rng)
                store[c] = vals
                lo, hi = np.percentile(vals, [2.5, 97.5])
                res["bolmeler"][c] = {
                    "ort": round(float(vals.mean()), 4), "sd": round(float(vals.std(ddof=1)), 4),
                    "ci95": [round(float(lo), 4), round(float(hi), 4)],
                    "ci95_genislik": round(float(hi - lo), 4),
                    "ort_oracle_pismanligi": round(oracle - float(vals.mean()), 4),
                    "essiz_epok_sayisi": int(len(np.unique(picks))),
                    "en_sik_epok": int(np.bincount(picks).argmax()),
                    "en_sik_pay": round(float(np.bincount(picks).max() / picks.size), 4),
                }
                print(f"{tag:<18}{'V_' + c:>7}{vals.mean():>8.2f}{vals.std(ddof=1):>7.2f}"
                      f"{f'[{lo:.2f}, {hi:.2f}]':>16}{oracle:>8.2f}"
                      f"{oracle - vals.mean():>11.2f}{len(np.unique(picks)):>9}")
            # sifir-sizinti Delta dagilimi: iki BAGIMSIZ temiz cekilisin farki
            if "B" in store and "C" in store:
                i = rng.integers(0, args.n_boot, args.n_boot)
                j = rng.integers(0, args.n_boot, args.n_boot)
                d = store["B"][i] - store["C"][j]
                res["sifir_sizinti_Delta"] = {
                    "ort_mutlak": round(float(np.abs(d).mean()), 4),
                    "medyan_mutlak": round(float(np.median(np.abs(d))), 4),
                    "sd": round(float(d.std(ddof=1)), 4),
                    "p90_mutlak": round(float(np.percentile(np.abs(d), 90)), 4),
                    "p95_mutlak": round(float(np.percentile(np.abs(d), 95)), 4),
                    "P_absD_gt_1pp": round(float((np.abs(d) > 1.0).mean()), 4),
                    "beklenen_max_3_cekilis": round(float(np.mean(
                        np.abs(d).reshape(-1, 1).repeat(3, 1).max(axis=1))), 4),
                }
            out["yorungeler"][tag] = res

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out + ".tmp", "w") as f:
        json.dump(out, f, indent=2)
    os.replace(args.out + ".tmp", args.out)

    print("\nSIFIR-SIZINTI |Delta| (iki bagimsiz temiz bolme, GERCEK test):")
    for tag, r in out["yorungeler"].items():
        z = r.get("sifir_sizinti_Delta")
        if z:
            print(f"  {tag:<18} ort {z['ort_mutlak']:.2f} medyan {z['medyan_mutlak']:.2f} "
                  f"p95 {z['p95_mutlak']:.2f} | P(|D|>1pp) {100*z['P_absD_gt_1pp']:.0f}%")
    print(f"\nkaydedildi: {args.out}")


if __name__ == "__main__":
    main()
