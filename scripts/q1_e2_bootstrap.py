"""E2 KESIFSEL analiz: secim kararsizliginin AMPIRIK gurultu tabani.

On-kayitli protokol (E2_ISTATISTIK_PROTOKOLU.md Bolum 8) geregi KESIFSEL:
birincil uc noktalara girmez, secim kuralini degistirmez; makalede
"kesifsel" etiketiyle sunulur.

FIKIR: V_B ve V_C ikisi de "hic gorulmemis" (esit derecede temiz) 2000'er
ornek. Bir secim kuralini V_B'nin bootstrap yeniden-orneklemesi uzerinde
kosup, secilen checkpoint'i AYRIK V_C uzerinde degerlendirirsek, SIFIR
sizinti altinda iki bagimsiz bolmenin urettigi fark dagilimini elde ederiz.
Bu, V_C'nin tek cekilisiyle olculen gurultu tabaninin dagilim-duzeyi
karsiligidir ve "Delta_AB gurultu tabanindan buyuk mu?" sorusunu tek bir
sayiya degil, bir dagilima karsi sorar.

Girdi: results/q1/e2/select_<arch>_s<seed>_val{B,C}_valcurve.npz
       (100 epok x 2000 ornek dogru/yanlis maskeleri)
Cikti: results/q1/e2/e2_bootstrap.json + konsol ozeti

Kullanim (konteyner icinde):
    python scripts/q1_e2_bootstrap.py --n-boot 2000
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


def selection_curve_from_counts(adv_mask, counts):
    """Bootstrap agirliklariyla epok basina adv dogruluk egrisi (% puan)."""
    n = counts.sum()
    return 100.0 * (adv_mask @ counts) / n


def one_direction(sel_npz, eval_npz, n_boot, rng, patience, min_delta):
    """sel_npz uzerinde bootstrap secim -> eval_npz uzerinde degerlendirme."""
    sel = np.load(sel_npz)
    ev = np.load(eval_npz)
    epochs = sel["epochs"].astype(int)
    assert list(epochs) == list(ev["epochs"].astype(int)), "epok dizileri farkli"
    adv_sel = sel["adv_mask"].astype(np.float64)      # (E, N)
    clean_sel = sel["clean_mask"].astype(np.float64)
    adv_ev = 100.0 * ev["adv_mask"].mean(axis=1)      # (E,) ayrik degerlendirme
    n = adv_sel.shape[1]

    picks, evals = [], []
    for _ in range(n_boot):
        counts = rng.multinomial(n, np.full(n, 1.0 / n)).astype(np.float64)
        adv_curve = selection_curve_from_counts(adv_sel, counts)
        clean_curve = selection_curve_from_counts(clean_sel, counts)
        recs = list(zip(epochs.tolist(), clean_curve.tolist(), adv_curve.tolist()))
        ep, _adv, _stop = simulate_selection(recs, patience=patience, min_delta=min_delta)
        if ep is None:
            continue
        picks.append(int(ep))
        evals.append(float(adv_ev[int(np.where(epochs == ep)[0][0])]))
    return np.array(picks), np.array(evals), epochs, adv_ev


def summarize(picks, evals, epochs, adv_ev, rng):
    """Iki BAGIMSIZ cekilisin farki = sifir-sizinti altinda Delta dagilimi."""
    m = len(picks)
    i = rng.integers(0, m, size=m)
    j = rng.integers(0, m, size=m)
    d_eval = evals[i] - evals[j]
    d_epoch = picks[i] - picks[j]
    best_ep = int(epochs[int(np.argmax(adv_ev))])
    return {
        "n_boot": int(m),
        "secilen_epok": {
            "medyan": float(np.median(picks)), "min": int(picks.min()),
            "max": int(picks.max()), "essiz_sayisi": int(len(np.unique(picks))),
            "en_sik": int(np.bincount(picks).argmax()),
            "en_sik_pay": float(np.bincount(picks).max() / m),
        },
        "ayrik_degerlendirmede_adv": {
            "ort": float(evals.mean()), "sd": float(evals.std(ddof=1)),
            "min": float(evals.min()), "max": float(evals.max()),
            "oracle_en_iyi": float(adv_ev.max()), "oracle_epok": best_ep,
            "ortalama_oracle_kaybi": float(adv_ev.max() - evals.mean()),
        },
        "sifir_sizinti_Delta_dagilimi": {
            "ort_mutlak": float(np.abs(d_eval).mean()),
            "medyan_mutlak": float(np.median(np.abs(d_eval))),
            "sd": float(d_eval.std(ddof=1)),
            "p90_mutlak": float(np.percentile(np.abs(d_eval), 90)),
            "p95_mutlak": float(np.percentile(np.abs(d_eval), 95)),
            "P_ayni_epok": float((d_epoch == 0).mean()),
            "P_absDelta_gt_1pp": float((np.abs(d_eval) > 1.0).mean()),
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default=str(ROOT / "results/q1/e2"))
    ap.add_argument("--out", default=str(ROOT / "results/q1/e2/e2_bootstrap.json"))
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20260816)
    ap.add_argument("--patience", type=int, default=20)
    ap.add_argument("--min-delta", type=float, default=0.1)
    args = ap.parse_args()

    in_dir = Path(args.in_dir)
    rng = np.random.default_rng(args.seed)
    out = {"kesifsel": True,
           "protokol": "E2_ISTATISTIK_PROTOKOLU.md Bolum 8",
           "n_boot": args.n_boot, "seed": args.seed,
           "secim_kurali": {"patience": args.patience, "min_delta": args.min_delta},
           "yorungeler": {}}

    curves = sorted(in_dir.glob("select_*_valB_valcurve.npz"))
    if not curves:
        sys.exit(f"{in_dir}: valB_valcurve.npz bulunamadi (secim kosumlari bitti mi?)")

    for bpath in curves:
        tag = re.sub(r"^select_|_valB_valcurve\.npz$", "", bpath.name)
        cpath = bpath.with_name(bpath.name.replace("_valB_", "_valC_"))
        if not cpath.exists():
            print(f"ATLA {tag}: {cpath.name} yok")
            continue
        res = {}
        for yon, (s, e) in {"B_sec_C_degerlendir": (bpath, cpath),
                            "C_sec_B_degerlendir": (cpath, bpath)}.items():
            picks, evals, epochs, adv_ev = one_direction(
                str(s), str(e), args.n_boot, rng, args.patience, args.min_delta)
            res[yon] = summarize(picks, evals, epochs, adv_ev, rng)
        out["yorungeler"][tag] = res
        d = res["B_sec_C_degerlendir"]
        print(f"\n{tag}")
        print(f"  secilen epok (B bootstrap): medyan {d['secilen_epok']['medyan']:.0f}, "
              f"aralik [{d['secilen_epok']['min']},{d['secilen_epok']['max']}], "
              f"{d['secilen_epok']['essiz_sayisi']} essiz epok, "
              f"en sik ep{d['secilen_epok']['en_sik']} (%{100*d['secilen_epok']['en_sik_pay']:.0f})")
        a = d["ayrik_degerlendirmede_adv"]
        print(f"  ayrik degerlendirme adv: {a['ort']:.2f} +- {a['sd']:.2f} "
              f"(oracle {a['oracle_en_iyi']:.2f} @ep{a['oracle_epok']}, "
              f"ort. kayip {a['ortalama_oracle_kaybi']:.2f} puan)")
        z = d["sifir_sizinti_Delta_dagilimi"]
        print(f"  SIFIR-SIZINTI |Delta|: ort {z['ort_mutlak']:.2f}, medyan "
              f"{z['medyan_mutlak']:.2f}, p90 {z['p90_mutlak']:.2f}, p95 {z['p95_mutlak']:.2f} puan | "
              f"P(ayni epok)={100*z['P_ayni_epok']:.1f}%, P(|D|>1pp)={100*z['P_absDelta_gt_1pp']:.1f}%")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out + ".tmp", "w") as f:
        json.dump(out, f, indent=2)
    os.replace(args.out + ".tmp", args.out)
    print(f"\nkaydedildi: {args.out}")


if __name__ == "__main__":
    main()
