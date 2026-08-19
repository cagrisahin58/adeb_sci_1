#!/usr/bin/env python3
"""A2b — kosullama protokollerinin SINIF BILESIMI kontrolu.

Neden: kosullama (target_correct / both_correct / successful_source) test
kumesinin bir ALT KUMESINI secer. Iki yon (CNN->ViT ve ViT->CNN) farkli alt
kumeler uzerinde olculurse, aradaki asimetri kismen "hangi orneklerin
kaldigi"ndan dogabilir. SVHN'de bu risk ciddidir cunku sinif dagilimi
DENGESIZDIR (E7 zorunlu onlemi); CIFAR'da denge tam oldugu icin kontrol
kalibrasyon amaciyla orada da kosulabilir.

Olculen:
  1. Her protokol/yon icin kosullu alt kumenin sinif dagilimi, tam test
     dagilimindan TV uzakligi ve chi-kare uyum istatistigi.
  2. Iki YON arasindaki bilesim farki (asil karistiricinin olcusu).
  3. Asimetrinin BILESIM ETKISI ve ORAN ETKISI olarak ayristirilmasi
     (Kitagawa/Oaxaca tarzi; iki bilesen tam olarak asimetriyi verir).

Kullanim:
  docker exec -w /workspace \\
    -e A2B_IN_DIR=results/c1_transfer/pair1 -e A2B_DATASET=cifar10 \\
    adeb_eval python experiments/rev2/a2b_class_balance.py
"""

import json
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, ROOT)

IN_DIR = os.environ.get("A2B_IN_DIR", "results/c1_transfer/pair1")
DATASET = os.environ.get("A2B_DATASET", "cifar10")
SRC = os.environ.get("A2B_SRC", "ResNet18_AT")
TGT = os.environ.get("A2B_TGT", "ViT_Tiny_AT")
OUT_FILE = os.environ.get(
    "A2B_OUT", os.path.join("results", "rev2_blockA", "a2b_class_balance_" + DATASET + ".json")
)

PROTOCOLS = ["raw", "target_correct", "both_correct", "successful_source"]


def test_labels(dataset):
    """Test kumesi etiketleri, TEST YUKLEYICI SIRASINDA.

    get_loaders test yukleyicisini shuffle=False ile kurar; bu nedenle
    per_sample_*.npz maskeleriyle indeks hizasi korunur.
    """
    from src.data.datasets import DATASETS, _make_dataset

    if dataset not in DATASETS:
        raise ValueError("Bilinmeyen dataset: " + dataset)
    ds = _make_dataset(dataset, os.path.join(ROOT, "data"), False, None, True)
    if hasattr(ds, "targets"):
        y = np.asarray(ds.targets)
    elif hasattr(ds, "labels"):
        y = np.asarray(ds.labels)
    else:
        raise RuntimeError("Etiket alani bulunamadi")
    exp = DATASETS[dataset]["n_test"]
    if len(y) != exp:
        raise RuntimeError("Test boyutu %d != beklenen %d" % (len(y), exp))
    return y.astype(int)


def load_pair(src, tgt):
    path = os.path.join(ROOT, IN_DIR, "per_sample_" + src + "_to_" + tgt + ".npz")
    with np.load(path) as z:
        return {k: z[k].copy() for k in z.files}


def protocol_masks(pair, protocol):
    fool = pair["target_adv_wrong"]
    if protocol == "raw":
        cond = np.ones_like(fool, dtype=bool)
    elif protocol == "target_correct":
        cond = pair["target_clean_correct"]
    elif protocol == "both_correct":
        cond = pair["target_clean_correct"] & pair["source_clean_correct"]
    elif protocol == "successful_source":
        cond = pair["target_clean_correct"] & pair["source_adv_wrong"]
    else:
        raise ValueError(protocol)
    return fool, cond


def class_profile(y, cond, fool, n_classes):
    """Kosullu alt kumede sinif paylari ve sinif-basina kandirma oranlari."""
    idx = np.flatnonzero(cond)
    yy = y[idx]
    ff = fool[idx].astype(float)
    counts = np.bincount(yy, minlength=n_classes).astype(float)
    share = counts / max(counts.sum(), 1.0)
    rate = np.full(n_classes, np.nan)
    for c in range(n_classes):
        m = yy == c
        if m.any():
            rate[c] = ff[m].mean()
    return share, rate, counts


def tv(p, q):
    return float(0.5 * np.abs(p - q).sum())


def chi2_gof(counts, p_ref):
    """Beklenen frekansi <5 olan sinif sayisi da RAPORLANIR."""
    n = counts.sum()
    exp = p_ref * n
    ok = exp > 0
    stat = float(((counts[ok] - exp[ok]) ** 2 / exp[ok]).sum())
    return stat, int(ok.sum() - 1), int((exp[ok] < 5).sum())


def main():
    y = test_labels(DATASET)
    n_classes = int(y.max()) + 1
    p_test = np.bincount(y, minlength=n_classes).astype(float)
    p_test /= p_test.sum()

    fwd = load_pair(SRC, TGT)
    bwd = load_pair(TGT, SRC)
    for name, pair in (("ileri", fwd), ("geri", bwd)):
        if len(pair["target_adv_wrong"]) != len(y):
            raise RuntimeError(
                "%s: maske boyu %d != etiket boyu %d"
                % (name, len(pair["target_adv_wrong"]), len(y))
            )

    out = {
        "dataset": DATASET,
        "in_dir": IN_DIR,
        "yon": {"ileri": SRC + "->" + TGT, "geri": TGT + "->" + SRC},
        "n_test": int(len(y)),
        "n_classes": n_classes,
        "sinif_dengesi_tam_mi": bool(np.allclose(p_test, p_test[0])),
        "test_pay_min_max": [round(float(p_test.min()), 5), round(float(p_test.max()), 5)],
        "test_dengesizlik_orani": round(float(p_test.max() / p_test.min()), 3),
        "protokoller": {},
    }

    for proto in PROTOCOLS:
        f_f, c_f = protocol_masks(fwd, proto)
        f_b, c_b = protocol_masks(bwd, proto)
        sh_f, r_f, cnt_f = class_profile(y, c_f, f_f, n_classes)
        sh_b, r_b, cnt_b = class_profile(y, c_b, f_b, n_classes)

        chi_f = chi2_gof(cnt_f, p_test)
        chi_b = chi2_gof(cnt_b, p_test)

        rate_f = float(f_f[c_f].mean() * 100)
        rate_b = float(f_b[c_b].mean() * 100)
        asym = rate_f - rate_b

        rf = np.nan_to_num(r_f)
        rb = np.nan_to_num(r_b)
        comp = float(((sh_f - sh_b) * (rf + rb) / 2).sum() * 100)
        rate_eff = float(((rf - rb) * (sh_f + sh_b) / 2).sum() * 100)
        denom = abs(comp) + abs(rate_eff)

        out["protokoller"][proto] = {
            "n_kosullu": {"ileri": int(c_f.sum()), "geri": int(c_b.sum())},
            "oran_yuzde": {"ileri": round(rate_f, 2), "geri": round(rate_b, 2)},
            "asimetri_puan": round(asym, 3),
            "AYRISTIRMA": {
                "bilesim_etkisi": round(comp, 3),
                "oran_etkisi": round(rate_eff, 3),
                "toplam_kontrol": round(comp + rate_eff, 3),
                "bilesim_payi_yuzde": (round(abs(comp) / denom * 100, 1) if denom > 0 else None),
            },
            "bilesim_sapmasi": {
                "TV_ileri_vs_test": round(tv(sh_f, p_test), 4),
                "TV_geri_vs_test": round(tv(sh_b, p_test), 4),
                "TV_ileri_vs_geri": round(tv(sh_f, sh_b), 4),
                "max_mutlak_pay_farki": round(float(np.abs(sh_f - sh_b).max()), 4),
                "chi2_ileri": {
                    "stat": round(chi_f[0], 2), "df": chi_f[1], "dusuk_beklenen_sinif": chi_f[2]
                },
                "chi2_geri": {
                    "stat": round(chi_b[0], 2), "df": chi_b[1], "dusuk_beklenen_sinif": chi_b[2]
                },
            },
            "sinif_paylari": {
                "ileri": [round(float(v), 5) for v in sh_f],
                "geri": [round(float(v), 5) for v in sh_b],
            },
        }

    worst = max(
        out["protokoller"],
        key=lambda p: out["protokoller"][p]["bilesim_sapmasi"]["TV_ileri_vs_geri"],
    )
    bc_tv = out["protokoller"]["both_correct"]["bilesim_sapmasi"]["TV_ileri_vs_geri"]
    out["OZET"] = {
        "en_buyuk_yon_bilesim_farki_protokolu": worst,
        "en_buyuk_TV_ileri_vs_geri": out["protokoller"][worst]["bilesim_sapmasi"]["TV_ileri_vs_geri"],
        "both_correct_TV_ileri_vs_geri": bc_tv,
        "both_correct_sifir_mi_SAGLAMA": bool(bc_tv == 0.0),
        "yorum": (
            "both_correct protokolu iki yonu AYNI orneklerde puanladigi icin "
            "TV_ileri_vs_geri tam 0 olmalidir; olmuyorsa maskelerde hata vardir "
            "(bu alan bir SAGLAMA testidir). Diger protokollerde TV > 0 beklenir; "
            "AYRISTIRMA/bilesim_etkisi asimetrinin ne kadarinin sinif bilesiminden "
            "geldigini puan cinsinden verir."
        ),
    }

    outp = os.path.join(ROOT, OUT_FILE)
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    with open(outp, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)

    print(json.dumps({k: v for k, v in out.items() if k != "protokoller"},
                     indent=2, ensure_ascii=False))
    for p, d in out["protokoller"].items():
        a = d["AYRISTIRMA"]
        print("\n%-19s asimetri %+7.3f = bilesim %+7.3f + oran %+7.3f | bilesim payi %%%s | TV(ileri,geri)=%s"
              % (p, d["asimetri_puan"], a["bilesim_etkisi"], a["oran_etkisi"],
                 a["bilesim_payi_yuzde"], d["bilesim_sapmasi"]["TV_ileri_vs_geri"]))
    print("\nYazildi: " + OUT_FILE)


if __name__ == "__main__":
    main()
