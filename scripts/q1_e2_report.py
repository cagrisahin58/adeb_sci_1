"""E2 toplama raporu: on-kayitli protokolun (E2_ISTATISTIK_PROTOKOLU.md) uygulanmasi.

YALNIZ q1_offline_select.py ciktilarini tuketir (select_*.json + select_*_test.npz);
protokol disinda hicbir karar kurali icermez.

Uc noktalar (protokol Bolum 3):
  Es-birincil 1: McNemar (A-vs-B ve B-vs-C; tohumlar havuzlanmis adv maskeleri,
                 kesin binom testi)
  Es-birincil 2: eslesmis Delta + TOST (delta=1.0, alpha=0.05, n=tohum sayisi)
  Ikincil: secilen epok farklari, clean analoglari, val egrileri

Kullanim:
    python scripts/q1_e2_report.py                       # varsayilan yollar
    python scripts/q1_e2_report.py --allow-partial       # eksik dosyalari atla
"""
import argparse
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

try:
    from scipy import stats as sps
except ImportError:
    sys.exit("scipy gerekli (konteynerde mevcut): pip install scipy")

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"

ARCHS = {"resnet18": [1001, 1002, 1003], "vit_tiny": [2001, 2002, 2003]}
CONDS = ["A", "B", "C"]  # A=sizintili, B=temiz, C=negatif kontrol
DELTA = 1.0   # TOST esdegerlik marji (puan) - protokol Bolum 3
ALPHA = 0.05


EXPECTED_TEST_N = 10000  # CIFAR-10 tam test kumesi; smoke/--test-n ciktilari REDDEDILIR


def _resolve_npz(npz_str):
    """Goreli yolu ROOT'a bagla; baska ortamda (konteyner vs WSL) uretilmis
    mutlak yol dosyaya ulasamiyorsa 'results/...' kuyrugunu ROOT'a bagla."""
    p = Path(npz_str)
    if not p.is_absolute():
        return ROOT / p
    if p.exists():
        return p
    parts = p.parts
    if "results" in parts:
        return ROOT.joinpath(*parts[parts.index("results"):])
    return p


def load_cell(in_dir, arch, seed, cond, allow_partial):
    jpath = in_dir / f"select_{arch}_s{seed}_val{cond}.json"
    if not jpath.exists():
        if allow_partial:
            return None
        sys.exit(f"EKSIK: {jpath} (tamamlanmamis kampanyada --allow-partial kullan)")
    sel = json.load(open(jpath))
    if sel["selected_epoch"] is None:
        # Protokol Bolum 5: hucre analiz disi + insan incelemesi. Final modda
        # fail-safe olarak rapor tumden reddedilir; ara denetimde tohum atlanir
        if allow_partial:
            print(f"UYARI: {jpath} secim None - tohum atlandi (kosum incelenmeli)")
            return None
        sys.exit(f"HATA: {jpath} secim None - kosum incelenmeli, rapor uretilmedi")
    if not sel.get("test"):
        if allow_partial:
            print(f"UYARI: {jpath} test degerlendirmesi yok - tohum atlandi")
            return None
        sys.exit(f"HATA: {jpath} test degerlendirmesi yok (--test-eval ile kosulmali)")
    n = sel["test"].get("n")
    if n != EXPECTED_TEST_N:
        # Sessiz karisma sigortasi: final yola dusmus bir smoke (--test-n)
        # ciktisi pipeline guard'ini da SKIP ettirir - her modda sert hata
        sys.exit(f"HATA: {jpath} test n={n} != {EXPECTED_TEST_N} - smoke/--test-n "
                 f"ciktisi final yola karismis olabilir; dosyayi incele ve sil")
    npz_path = _resolve_npz(sel["test"]["per_sample_npz"])
    try:
        z = np.load(npz_path)
    except Exception as e:
        sys.exit(f"HATA: {jpath} -> npz okunamadi ({npz_path}): {e}")
    clean_mask = z["clean_correct"].astype(bool)
    adv_mask = z["adv_correct"].astype(bool)
    if clean_mask.size != n or adv_mask.size != n:
        sys.exit(f"HATA: {jpath} npz boyutu ({clean_mask.size}) != test.n ({n})")
    if int(z["selected_epoch"]) != int(sel["selected_epoch"]):
        sys.exit(f"HATA: {jpath} JSON secimi ({sel['selected_epoch']}) != npz secimi "
                 f"({int(z['selected_epoch'])}) - bayat/eslesmeyen dosya cifti")
    return {
        "selected_epoch": sel["selected_epoch"],
        "val_adv": sel["selected_adv_acc"],
        "test_clean": sel["test"]["clean_acc"],
        "test_adv": sel["test"]["adv_acc"],
        "clean_mask": clean_mask,
        "adv_mask": adv_mask,
    }


def paired_tost(deltas, margin=DELTA, alpha=ALPHA, identical_selection=False):
    """Eslesmis TOST + iki-yonlu t + %90 GA. Protokol Bolum 3 ve 5 (dejenere)."""
    d = np.asarray(deltas, dtype=float)
    n = d.size
    m = float(d.mean())
    s = float(d.std(ddof=1)) if n > 1 else float("nan")
    res = {"n": n, "mean": m, "sd": s, "deltas": [round(x, 4) for x in d.tolist()]}
    if n < 2 or not math.isfinite(s):
        res["verdict"] = "YETERSIZ_N"
        return res
    if s == 0.0:
        # Dejenere (protokol Bolum 5): t tanimsiz, hukum McNemar'a birakilir.
        # OZDES_SECIM etiketi yalniz epok ozdesliginin OLGUSAL dogrulanmasiyla
        # verilir; s=0 farkli epoklarla da olusabilir (esit test-acc farklari)
        if identical_selection:
            res["verdict"] = "DEJENERE_OZDES_SECIM"
        elif abs(m) < margin:
            res["verdict"] = "DEJENERE_ESIT_DELTA(|Delta|<marj)"
        else:
            res["verdict"] = "DEJENERE_MARJ_DISI"
        return res
    se = s / math.sqrt(n)
    df = n - 1
    p_lower = float(sps.t.sf((m + margin) / se, df))   # H0: mu <= -marj
    p_upper = float(sps.t.cdf((m - margin) / se, df))  # H0: mu >= +marj
    p_tost = max(p_lower, p_upper)
    t_stat = m / se
    p_diff = float(2 * sps.t.sf(abs(t_stat), df))
    half = float(sps.t.ppf(1 - alpha, df)) * se        # %90 GA yari-genisligi
    res.update({
        "se": se, "tost_margin": margin, "p_tost": round(p_tost, 5),
        "equivalent": bool(p_tost < alpha),
        "ci90": [round(m - half, 4), round(m + half, 4)],
        "t_two_sided_p": round(p_diff, 5),
        "different": bool(p_diff < alpha),
    })
    # Iki bayrak ayni anda dogru olabilir: "onemsiz buyuklukte ama sifir
    # olmayan fark" ceyregi - tek etikete indirgeyip bilgi kaybetme
    if res["equivalent"] and res["different"]:
        res["verdict"] = "ESDEGER_AMA_SIFIRDAN_FARKLI"
    elif res["equivalent"]:
        res["verdict"] = "ESDEGER"
    elif res["different"]:
        res["verdict"] = "FARKLI"
    else:
        res["verdict"] = "SONUCSUZ"
    return res


def mcnemar_exact(mask_x, mask_y):
    """Kesin (binom) McNemar: b = x dogru & y yanlis, c = x yanlis & y dogru."""
    b = int(np.sum(mask_x & ~mask_y))
    c = int(np.sum(~mask_x & mask_y))
    n_disc = b + c
    if n_disc == 0:
        p = 1.0
    else:
        p = float(sps.binomtest(min(b, c), n_disc, 0.5, alternative="two-sided").pvalue)
    # p cok kucuk olabilir (b+c binlerce); round(p, 6) 8.9e-13'u 0.0 yapiyordu
    return {"b_only_first": b, "c_only_second": c, "n_discordant": n_disc,
            "acc_diff_pp": round(100.0 * (b - c) / mask_x.size, 4),
            "p_exact": float(f"{p:.6g}"), "significant": bool(p < ALPHA)}


def contrast(cells, cond_x, cond_y, metric):
    """Tohum-bazli farklar + TOST + havuzlanmis McNemar (cond_x - cond_y)."""
    seeds = sorted(cells)
    deltas = [cells[s][cond_x][metric] - cells[s][cond_y][metric] for s in seeds]
    identical = all(cells[s][cond_x]["selected_epoch"] == cells[s][cond_y]["selected_epoch"]
                    for s in seeds)
    mask_key = "adv_mask" if metric == "test_adv" else "clean_mask"
    pooled_x = np.concatenate([cells[s][cond_x][mask_key] for s in seeds])
    pooled_y = np.concatenate([cells[s][cond_y][mask_key] for s in seeds])
    assert pooled_x.size == pooled_y.size, \
        f"{cond_x}/{cond_y} havuz boyutlari esit degil: {pooled_x.size} vs {pooled_y.size}"
    per_seed_mcnemar = {
        str(s): mcnemar_exact(cells[s][cond_x][mask_key], cells[s][cond_y][mask_key])
        for s in seeds
    }
    return {
        "contrast": f"{cond_x}-{cond_y}", "metric": metric,
        "identical_selection": identical,
        "tost": paired_tost(deltas, identical_selection=identical),
        "mcnemar_pooled": mcnemar_exact(pooled_x, pooled_y),
        "mcnemar_per_seed": per_seed_mcnemar,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default=str(ROOT / "results/q1/e2"))
    ap.add_argument("--out", default=str(ROOT / "results/q1/e2/e2_report.json"))
    ap.add_argument("--allow-partial", action="store_true",
                    help="Eksik/None hucrenin TOHUMUNU tumden atla (ara denetim; "
                         "eslesme hijyeni icin tohumun uc kosulu birlikte duser); "
                         "final rapor icin KULLANMA")
    args = ap.parse_args()
    in_dir = Path(args.in_dir)

    report = {
        "protocol": "results/q1_research/E2_ISTATISTIK_PROTOKOLU.md",
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tost_margin": DELTA, "alpha": ALPHA,
        "partial": bool(args.allow_partial),
        "archs": {},
    }

    for arch, seeds in ARCHS.items():
        cells = {}
        for seed in seeds:
            row = {}
            for cond in CONDS:
                cell = load_cell(in_dir, arch, seed, cond, args.allow_partial)
                if cell is None:
                    row = None
                    break
                row[cond] = cell
            if row is not None:
                cells[seed] = row
        if not cells:
            report["archs"][arch] = {"status": "VERI_YOK"}
            continue

        table = {str(s): {c: {k: cells[s][c][k] for k in
                              ("selected_epoch", "val_adv", "test_clean", "test_adv")}
                          for c in CONDS} for s in cells}
        arch_rep = {
            "status": "TAM" if len(cells) == len(seeds) else f"KISMI({len(cells)}/{len(seeds)})",
            "per_seed": table,
            # Es-birincil kontrastlar: A-B (sizinti+gurultu) vs B-C (saf gurultu tabani)
            "leak_AB_adv": contrast(cells, "A", "B", "test_adv"),
            "noise_BC_adv": contrast(cells, "B", "C", "test_adv"),
            # Ikincil: clean analoglari
            "leak_AB_clean": contrast(cells, "A", "B", "test_clean"),
            "noise_BC_clean": contrast(cells, "B", "C", "test_clean"),
        }
        report["archs"][arch] = arch_rep

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(str(out) + ".tmp", "w") as f:
        json.dump(report, f, indent=2)
    os.replace(str(out) + ".tmp", str(out))

    # Ozet (insan icin)
    print(f"\n=== E2 RAPORU ({'KISMI' if args.allow_partial else 'TAM'}) -> {out} ===")
    for arch, rep in report["archs"].items():
        if rep.get("status") == "VERI_YOK":
            print(f"\n{arch}: veri yok")
            continue
        print(f"\n{arch} [{rep['status']}]  (secilen epoklar A/B/C):")
        for s, row in rep["per_seed"].items():
            eps = "/".join(str(row[c]["selected_epoch"]) for c in CONDS)
            advs = " ".join(f"{c}:{row[c]['test_adv']:.2f}" for c in CONDS)
            print(f"  seed {s}: epok {eps} | test adv {advs}")
        for key in ("leak_AB_adv", "noise_BC_adv"):
            c = rep[key]
            t = c["tost"]
            mc = c["mcnemar_pooled"]
            print(f"  {c['contrast']} adv: Delta={t['mean']:+.3f} sd={t.get('sd', float('nan')):.3f} "
                  f"-> TOST {t['verdict']}"
                  + (f" (p_tost={t['p_tost']}, t_p={t['t_two_sided_p']})" if "p_tost" in t else "")
                  + f" | McNemar b={mc['b_only_first']} c={mc['c_only_second']} "
                    f"p={mc['p_exact']} {'ANLAMLI' if mc['significant'] else 'degil'}")


if __name__ == "__main__":
    main()
