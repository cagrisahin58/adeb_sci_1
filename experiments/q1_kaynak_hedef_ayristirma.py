#!/usr/bin/env python3
"""Gorev 1.1: toplamsal kaynak + hedef ayristirmasi.

Model: oran(s -> t) = mu + alpha_s + beta_t + eps, yalniz kosegen DISI hucreler,
toplam-sifir kisiti (etki kodlamasi), en kucuk kareler.

Girdiler
  (a) results/c1_c3/c3_summary.json                       CIFAR-10 3x3, uc tohum ortalamasi
  (b) results/q1/cifar100/transfer/e1_c3_summary.json     CIFAR-100 3x3, ayni sema
  (c) results/c1_c3/pair{1,2,3}/transfer_matrix.json + per_sample_*.npz
      results/q1/cifar100/transfer/pair{1,2,3}/transfer_matrix.json + per_sample_*.npz
      (cift basina uydurma; bc ve ss protokolleri ornek bazli kayitlardan,
       tanimlar src/analysis/protokoller.py)
  (d) results/q1/dis_veri/mahmood2021_tablolar.json        Mahmood 8x8 (bc protokolu)
Cikti
  results/q1/kaynak_hedef_ayristirma.json

Asimetri ayristirmasi (3x3, ResNet ve ViT icin):
  oran(R->V) - oran(V->R) = (alpha_R - alpha_V) + (beta_V - beta_R) + (eps_RV - eps_VR)

Calistirma (depo kokunden):
  docker exec -w /workspace adeb_eval python experiments/q1_kaynak_hedef_ayristirma.py
"""
import datetime
import hashlib
import io
import json
import os
import sys

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
os.chdir(ROOT)
sys.path.insert(0, ROOT)
from src.analysis import protokoller as PROTO  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OUT = "results/q1/kaynak_hedef_ayristirma.json"
KAYNAK = {}
R, V, W = "ResNet18_AT", "ViT_Tiny_AT", "WRN_28_10"
MODELLER = [R, V, W]

VERI = {
    "CIFAR-10": {"ozet": "results/c1_c3/c3_summary.json", "cift_dizini": "results/c1_c3"},
    "CIFAR-100": {"ozet": "results/q1/cifar100/transfer/e1_c3_summary.json",
                  "cift_dizini": "results/q1/cifar100/transfer"},
}
MAHMOOD = "results/q1/dis_veri/mahmood2021_tablolar.json"


def sha256(yol):
    h = hashlib.sha256()
    with open(yol, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def oku_json(yol):
    KAYNAK[yol] = sha256(yol)
    with io.open(yol, encoding="utf-8") as fh:
        return json.load(fh)


def oku_npz(yol):
    KAYNAK[yol] = sha256(yol)
    return np.load(yol)


# ------------------------------------------------------------------ uydurma
def toplamsal(modeller, hucre, cins=None):
    """hucre: {(kaynak, hedef): oran}, kosegen disi. Etki kodlamasi ile EKK.
    cins verilirse ayni-cins gostergesi (gamma) ek terim olarak eklenir."""
    K = len(modeller)
    idx = {m: i for i, m in enumerate(modeller)}

    def etki(m):
        v = np.zeros(K - 1)
        i = idx[m]
        if i < K - 1:
            v[i] = 1.0
        else:
            v[:] = -1.0
        return v

    anahtarlar = [(s, t) for (s, t) in hucre if s != t]
    X = np.array([np.concatenate([[1.0], etki(s), etki(t)]
                                 + ([[1.0 if cins[s] == cins[t] else 0.0]] if cins else []))
                  for s, t in anahtarlar])
    y = np.array([hucre[k] for k in anahtarlar], dtype=float)
    b, _, rank, _ = np.linalg.lstsq(X, y, rcond=None)
    mu = float(b[0])
    a = np.append(b[1:K], -b[1:K].sum())
    be = np.append(b[K:2 * K - 1], -b[K:2 * K - 1].sum())
    gamma = float(b[2 * K - 1]) if cins else None
    fit = X @ b
    res = y - fit
    sst = float(((y - y.mean()) ** 2).sum())
    ssr = float((res ** 2).sum())
    return {
        "mu": mu,
        "alpha_kaynak": {m: float(a[idx[m]]) for m in modeller},
        "beta_hedef": {m: float(be[idx[m]]) for m in modeller},
        "artiklar": {f"{s}->{t}": float(r) for (s, t), r in zip(anahtarlar, res)},
        "uydurulan": {f"{s}->{t}": float(f) for (s, t), f in zip(anahtarlar, fit)},
        "max_abs_artik": float(np.abs(res).max()),
        "R2": 1 - ssr / sst if sst > 0 else None,
        "n_hucre": len(y),
        "ayni_cins_gamma": gamma,
        "parametre_sayisi": X.shape[1],
        "artik_serbestlik": len(y) - X.shape[1],
        "tasarim_rank": int(rank),
    }


def ayristir_ikili(fit, a, b, hucre):
    """asimetri a->b eksi b->a = kaynak farki + hedef farki + artik farki."""
    kf = fit["alpha_kaynak"][a] - fit["alpha_kaynak"][b]
    hf = fit["beta_hedef"][b] - fit["beta_hedef"][a]
    af = fit["artiklar"][f"{a}->{b}"] - fit["artiklar"][f"{b}->{a}"]
    asim = hucre[(a, b)] - hucre[(b, a)]
    return {"asimetri": asim, "kaynak_farki": kf, "hedef_farki": hf, "artik_farki": af,
            "toplam_kontrol": kf + hf + af}


def ozet_istat(xs):
    a = np.asarray([x for x in xs if x is not None], dtype=float)
    if a.size == 0:
        return None
    return {"ortalama": float(a.mean()), "sd_ciftler_arasi": float(a.std(ddof=1)) if a.size > 1 else None,
            "degerler": a.tolist()}


def uc_kare_ozet(hucre):
    """3x3 icin: kaynak/hedef farki, ayristirma, sabit-WRN karsitliklari, marjinaller."""
    fit = toplamsal(MODELLER, hucre)
    return {
        "uydurma": fit,
        "kaynak_etkisi_farki_ResNet_eksi_ViT": fit["alpha_kaynak"][R] - fit["alpha_kaynak"][V],
        "hedef_etkisi_farki_ViT_eksi_ResNet": fit["beta_hedef"][V] - fit["beta_hedef"][R],
        "asimetri_ayristirmasi_ResNettoViT_eksi_ViTtoResNet": ayristir_ikili(fit, R, V, hucre),
        "sabit_WRN": {
            "WRN_hedef_ResNetten": hucre[(R, W)],
            "WRN_hedef_ViTden": hucre[(V, W)],
            "WRN_hedef_fark_ResNet_eksi_ViT": hucre[(R, W)] - hucre[(V, W)],
            "WRN_kaynak_ResNete": hucre[(W, R)],
            "WRN_kaynak_ViTe": hucre[(W, V)],
            "WRN_kaynak_fark_ResNet_eksi_ViT": hucre[(W, R)] - hucre[(W, V)],
        },
        "marjinaller": {
            "gelen_ort_ResNet": (hucre[(V, R)] + hucre[(W, R)]) / 2,
            "gelen_ort_ViT": (hucre[(R, V)] + hucre[(W, V)]) / 2,
            "giden_ort_ResNet": (hucre[(R, V)] + hucre[(R, W)]) / 2,
            "giden_ort_ViT": (hucre[(V, R)] + hucre[(V, W)]) / 2,
        },
    }


def cift_hucreleri(dizin, cift):
    """Cift basina dort protokol hucreleri: transfer_matrix.json (raw, tc) + npz (bc, ss)."""
    tm = oku_json(f"{dizin}/pair{cift}/transfer_matrix.json")["results"]
    hucre = {p: {} for p in PROTO.PROTOKOLLER}
    kontrol = []
    for s in MODELLER:
        for t in MODELLER:
            if s == t:
                continue
            z = oku_npz(f"{dizin}/pair{cift}/per_sample_{s}_to_{t}.npz")
            tc = z["target_clean_correct"]
            sc = z["source_clean_correct"]
            aw = z["target_adv_wrong"]
            ss_var = "source_adv_wrong" in z.files
            sa = z["source_adv_wrong"] if ss_var else np.zeros_like(tc)
            o = PROTO.protokol_oranlari(tc, aw, sc, sa, tani=False)
            hucre["raw"][(s, t)] = o["raw"]
            hucre["target_correct"][(s, t)] = o["target_correct"]
            hucre["both_correct"][(s, t)] = o["both_correct"]
            hucre["successful_source"][(s, t)] = o["successful_source"] if ss_var else None
            v = tm[f"{s}->{t}"]
            kontrol.append({"yon": f"{s}->{t}",
                            "npz_raw_eksi_json_raw": o["raw"] - v["raw_fooling"],
                            "npz_tc_eksi_json_cond": o["target_correct"] - v["cond_fooling"]})
    for p in list(hucre):
        if any(v is None for v in hucre[p].values()):
            hucre[p] = None
    return hucre, kontrol


def main():
    sonuc = {}
    for ds, cfg in VERI.items():
        oz = oku_json(cfg["ozet"])
        hucre_tc = {(k.split("->")[0], k.split("->")[1]): v["cond"][0] for k, v in oz.items() if "->" in k}
        hucre_raw = {(k.split("->")[0], k.split("->")[1]): v["raw"][0] for k, v in oz.items() if "->" in k}
        ds_out = {
            "ozet_matris_kaynagi": cfg["ozet"],
            "ozet_matris": {
                "target_correct": uc_kare_ozet(hucre_tc),
                "raw_duyarlilik": uc_kare_ozet(hucre_raw),
            },
        }
        # ---- cift basina
        cift_fit = {p: [] for p in PROTO.PROTOKOLLER}
        kontroller = {}
        for c in (1, 2, 3):
            h, k = cift_hucreleri(cfg["cift_dizini"], c)
            kontroller[f"pair{c}"] = {
                "max_abs_npz_raw_eksi_json": max(abs(x["npz_raw_eksi_json_raw"]) for x in k),
                "max_abs_npz_tc_eksi_json_cond": max(abs(x["npz_tc_eksi_json_cond"]) for x in k),
            }
            for p in PROTO.PROTOKOLLER:
                cift_fit[p].append(uc_kare_ozet(h[p]) if h[p] is not None else None)
        cift_out = {}
        for p, lst in cift_fit.items():
            if all(x is None for x in lst):
                cift_out[p] = "yok (ornek bazli kayitta source_adv_wrong alani yok)"
                continue

            def g(f):
                return ozet_istat([f(x) for x in lst])

            cift_out[p] = {
                "kaynak_etkisi_farki_ResNet_eksi_ViT": g(lambda x: x["kaynak_etkisi_farki_ResNet_eksi_ViT"]),
                "hedef_etkisi_farki_ViT_eksi_ResNet": g(lambda x: x["hedef_etkisi_farki_ViT_eksi_ResNet"]),
                "asimetri_ResNettoViT_eksi_ViTtoResNet": g(lambda x: x["asimetri_ayristirmasi_ResNettoViT_eksi_ViTtoResNet"]["asimetri"]),
                "artik_farki": g(lambda x: x["asimetri_ayristirmasi_ResNettoViT_eksi_ViTtoResNet"]["artik_farki"]),
                "max_abs_artik": g(lambda x: x["uydurma"]["max_abs_artik"]),
                "R2": g(lambda x: x["uydurma"]["R2"]),
                "WRN_hedef_fark_ResNet_eksi_ViT": g(lambda x: x["sabit_WRN"]["WRN_hedef_fark_ResNet_eksi_ViT"]),
                "WRN_kaynak_fark_ResNet_eksi_ViT": g(lambda x: x["sabit_WRN"]["WRN_kaynak_fark_ResNet_eksi_ViT"]),
                "WRN_hedef_ResNetten": g(lambda x: x["sabit_WRN"]["WRN_hedef_ResNetten"]),
                "WRN_hedef_ViTden": g(lambda x: x["sabit_WRN"]["WRN_hedef_ViTden"]),
                "WRN_kaynak_ResNete": g(lambda x: x["sabit_WRN"]["WRN_kaynak_ResNete"]),
                "WRN_kaynak_ViTe": g(lambda x: x["sabit_WRN"]["WRN_kaynak_ViTe"]),
                "cift_basina_tam": lst,
            }
        ds_out["cift_basina"] = cift_out
        ds_out["npz_json_tutarlilik_kontrolu"] = kontroller
        sonuc[ds] = ds_out

    # ---- (d) Mahmood 8x8, bc protokolu
    mh = oku_json(MAHMOOD)
    aile = mh["aile"]
    mahmood = {}
    for ds in ("CIFAR-10", "CIFAR-100"):
        M = mh["transfer_matrisleri_yuzde"][ds]
        adlar = mh["model_adlari"]
        hucre = {(s, t): M[s][t] for s in adlar for t in adlar if s != t}
        fit = toplamsal(adlar, hucre)

        def ort_a(grup):
            return float(np.mean([fit["alpha_kaynak"][m] for m in grup]))

        def ort_b(grup):
            return float(np.mean([fit["beta_hedef"][m] for m in grup]))

        vit = [m for m in adlar if aile[m] == "ViT"]
        vit_h = [m for m in adlar if aile[m] in ("ViT", "hibrit")]
        cnn = [m for m in adlar if aile[m] == "CNN"]
        bit = [m for m in cnn if m.startswith("BiT")]
        rn = [m for m in cnn if m.startswith("ResNet")]
        aile_fark = {}
        for ad, cg, vg in (("CNN_vs_ViT_hibrit_haric", cnn, vit), ("CNN_vs_ViT_hibrit_dahil", cnn, vit_h),
                           ("BiT_vs_ViT", bit, vit), ("ResNet_vs_ViT", rn, vit)):
            aile_fark[ad] = {
                "kaynak_etkisi_farki_CNN_eksi_ViT": ort_a(cg) - ort_a(vg),
                "hedef_etkisi_farki_ViT_eksi_CNN": ort_b(vg) - ort_b(cg),
            }
        ciftler = {}
        for c in cnn:
            for v in vit_h:
                ciftler[f"{c} vs {v}"] = ayristir_ikili(fit, c, v, hucre)
        # sabit ucuncu model karsitliklari: anahtar cift BiT-M-R50x1 / ViT-L-16
        a, b = "BiT-M-R50x1", "ViT-L-16"
        ucuncu = {}
        for k in adlar:
            if k in (a, b):
                continue
            ucuncu[k] = {
                "sabit_hedef_k_BiTten_eksi_ViTL16dan": hucre[(a, k)] - hucre[(b, k)],
                "sabit_kaynak_k_BiTe_eksi_ViTL16ya": hucre[(k, a)] - hucre[(k, b)],
            }
        # Mahmood'un "model genus" ayrimi (ViT [ViT-R50 dahil], BiT, ResNet): ayni-cins terimli duyarlilik
        cins = {m: ("ViT" if aile[m] in ("ViT", "hibrit") else ("BiT" if m.startswith("BiT") else "ResNet"))
                for m in adlar}
        fit_c = toplamsal(adlar, hucre, cins=cins)

        def aile_farklari(f):
            def oa(g):
                return float(np.mean([f["alpha_kaynak"][m] for m in g]))

            def ob(g):
                return float(np.mean([f["beta_hedef"][m] for m in g]))
            return {ad: {"kaynak_etkisi_farki_CNN_eksi_ViT": oa(cg) - oa(vg),
                         "hedef_etkisi_farki_ViT_eksi_CNN": ob(vg) - ob(cg)}
                    for ad, cg, vg in (("CNN_vs_ViT_hibrit_haric", cnn, vit), ("CNN_vs_ViT_hibrit_dahil", cnn, vit_h),
                                       ("BiT_vs_ViT", bit, vit), ("ResNet_vs_ViT", rn, vit))}

        mahmood[ds] = {
            "protokol": "both_correct (Mahmood Denklem 3), m = 1000; kosegen (bagimsiz kopya) haric 56 hucre",
            "uydurma": fit,
            "ayni_cins_terimli_uydurma": {
                "cins": cins,
                "uydurma": fit_c,
                "aile_duzeyi_farklar": aile_farklari(fit_c),
                "not": "Toplamsal model Mahmood matrisinde cins-ici blok yapisini tasiyamaz (dusuk R2); "
                       "ayni-cins gostergesi eklenmis duyarlilik uydurmasi.",
            },
            "aile_duzeyi_farklar": aile_fark,
            "aileler_arasi_cift_ayristirmasi_CNNtoViT_eksi_ViTtoCNN": ciftler,
            "sabit_ucuncu_model_BiT-M-R50x1_vs_ViT-L-16": ucuncu,
        }
    sonuc["Mahmood2021"] = mahmood

    out = {
        "uretildi_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "kaynaklar": dict(KAYNAK),
        "yontem": ("oran(s->t) = mu + alpha_s + beta_t + eps, kosegen disi hucreler, toplam-sifir (etki kodlamasi), "
                   "numpy lstsq. 3x3'te 6 hucre, 5 parametre, 1 artik serbestlik derecesi. Ozet matris: uc tohum "
                   "ortalamasi (c3_summary 'cond' = hedef-dogru). Cift basina: transfer_matrix.json ve per_sample npz; "
                   "bc ve ss protokolleri src/analysis/protokoller.py maskeleriyle npz'den hesaplanir; ciftler arasi "
                   "SD ddof=1 (n=3). Kaynak farki = alpha_ResNet - alpha_ViT; hedef farki = beta_ViT - beta_ResNet; "
                   "toplamlari artik farkiyla birlikte ResNet->ViT eksi ViT->ResNet asimetrisine esittir. "
                   "Mahmood: 8x8 bc matrisi, ayni model; aile duzeyi farklar alpha/beta aile ortalamalarinin farki."),
        "birim": "yuzde puan",
        "sonuc": sonuc,
    }
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print("yazildi:", OUT)

    # konsol ozeti
    for ds in VERI:
        o = sonuc[ds]["ozet_matris"]["target_correct"]
        print(f"\n== {ds} ozet tc ==")
        print(" kaynak farki R-V: %.4f  hedef farki V-R: %.4f  max|artik| %.4f  R2 %.4f" % (
            o["kaynak_etkisi_farki_ResNet_eksi_ViT"], o["hedef_etkisi_farki_ViT_eksi_ResNet"],
            o["uydurma"]["max_abs_artik"], o["uydurma"]["R2"]))
        print(" ayristirma:", {k: round(v, 4) for k, v in o["asimetri_ayristirmasi_ResNettoViT_eksi_ViTtoResNet"].items()})
        print(" sabit WRN:", {k: round(v, 4) for k, v in o["sabit_WRN"].items()})
        print(" marjinal:", {k: round(v, 4) for k, v in o["marjinaller"].items()})
        for p, v in sonuc[ds]["cift_basina"].items():
            if isinstance(v, str):
                print(" ", p, v)
                continue
            print("  %-18s kaynak %.3f+-%.3f hedef %.3f+-%.3f asim %.3f+-%.3f maxart %.3f R2 %.3f | WRNhedef %.3f+-%.3f WRNkaynak %.3f+-%.3f" % (
                p, v["kaynak_etkisi_farki_ResNet_eksi_ViT"]["ortalama"], v["kaynak_etkisi_farki_ResNet_eksi_ViT"]["sd_ciftler_arasi"],
                v["hedef_etkisi_farki_ViT_eksi_ResNet"]["ortalama"], v["hedef_etkisi_farki_ViT_eksi_ResNet"]["sd_ciftler_arasi"],
                v["asimetri_ResNettoViT_eksi_ViTtoResNet"]["ortalama"], v["asimetri_ResNettoViT_eksi_ViTtoResNet"]["sd_ciftler_arasi"],
                v["max_abs_artik"]["ortalama"], v["R2"]["ortalama"],
                v["WRN_hedef_fark_ResNet_eksi_ViT"]["ortalama"], v["WRN_hedef_fark_ResNet_eksi_ViT"]["sd_ciftler_arasi"],
                v["WRN_kaynak_fark_ResNet_eksi_ViT"]["ortalama"], v["WRN_kaynak_fark_ResNet_eksi_ViT"]["sd_ciftler_arasi"]))
        print(" kontrol:", sonuc[ds]["npz_json_tutarlilik_kontrolu"])
    for ds, m in mahmood.items():
        print(f"\n== Mahmood {ds} == R2 %.4f max|artik| %.3f" % (m["uydurma"]["R2"], m["uydurma"]["max_abs_artik"]))
        for k, v in m["aile_duzeyi_farklar"].items():
            print("  ", k, {a: round(b, 3) for a, b in v.items()})
        mc = m["ayni_cins_terimli_uydurma"]
        print("   cins terimli: R2 %.4f max|artik| %.3f gamma %.3f" % (
            mc["uydurma"]["R2"], mc["uydurma"]["max_abs_artik"], mc["uydurma"]["ayni_cins_gamma"]))
        for k, v in mc["aile_duzeyi_farklar"].items():
            print("     ", k, {a: round(b, 3) for a, b in v.items()})
        print("   alpha:", {a: round(b, 2) for a, b in m["uydurma"]["alpha_kaynak"].items()})
        print("   beta :", {a: round(b, 2) for a, b in m["uydurma"]["beta_hedef"].items()})
        for k in ("BiT-M-R50x1 vs ViT-L-16", "ResNet-56 vs ViT-B-16"):
            print("  ", k, {a: round(b, 3) for a, b in m["aileler_arasi_cift_ayristirmasi_CNNtoViT_eksi_ViTtoCNN"][k].items()})


if __name__ == "__main__":
    main()
