#!/usr/bin/env python3
"""Gorev 1.4(b): ViT CLS dikkat entropisi degisimi icin katman basina TOST ve
devrilen / devrilmeyen orneklerin son blok kosinus karsilastirmasi.

Girdi : results/c1_c4/pair{1,2,3}/c4_summary.json
        results/c1_c45_summary.json (yalniz gerileme kontrolu: SD ve kosinus ortalamalari)
Cikti : results/c1_c4/c4_entropy_tost.json

Cikarim birimi KOSUDUR (n = 3 egitim cifti, df = 2). c4_summary yalniz koşu duzeyi ozet
tasir (entropy_delta_mean: 1000 ornek uzerinden ortalama; ornek bazli entropi saklanmamis),
bu yuzden ornek duzeyinde test yapilamaz.

TOST: H0: |mu| >= 0.05 nat. t_alt = (m + 0.05)/se, p_alt = 1 - F_t2(t_alt);
      t_ust = (m - 0.05)/se, p_ust = F_t2(t_ust); p_TOST = max(p_alt, p_ust).
Kosinus: katman 'block11.mlp' (son blok, tum-token duzlestirilmis kosinus), 'devrilen' =
temizde dogru VE cekismelide yanlis; 'devrilmeyen' = geri kalan (temizde yanlislar DAHIL).
Kosu duzeyinde eslestirilmis t (df = 2) ve iki yonlu p.

Calistirma (depo kokunden):
  docker exec -w /workspace adeb_eval python experiments/c1_c4_entropy_tost.py
"""
import datetime
import hashlib
import io
import json
import math
import os
import sys

import numpy as np
from scipy import stats

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
os.chdir(ROOT)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OUT = "results/c1_c4/c4_entropy_tost.json"
C45 = "results/c1_c45_summary.json"
MARJ = 0.05
KAYNAK = {}


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


def t2_cdf_kapali(t):
    """df = 2 icin kapali bicim: F(t) = 1/2 + t / (2 sqrt(2 + t^2)) (scipy capraz kontrolu)."""
    return 0.5 + t / (2 * math.sqrt(2 + t * t))


def tost(x, marj):
    x = np.asarray(x, dtype=float)
    n = x.size
    m, sd = float(x.mean()), float(x.std(ddof=1))
    se = sd / math.sqrt(n)
    df = n - 1
    t_alt = (m + marj) / se
    t_ust = (m - marj) / se
    p_alt = float(stats.t.sf(t_alt, df))
    p_ust = float(stats.t.cdf(t_ust, df))
    ga90 = [m - stats.t.ppf(0.95, df) * se, m + stats.t.ppf(0.95, df) * se]
    return {"degerler": x.tolist(), "ortalama": m, "sd": sd, "se": se, "df": df,
            "t_alt": t_alt, "t_ust": t_ust, "p_alt": p_alt, "p_ust": p_ust,
            "p_TOST": max(p_alt, p_ust),
            "p_TOST_kapali_bicim_df2": max(1 - t2_cdf_kapali(t_alt), t2_cdf_kapali(t_ust)) if df == 2 else None,
            "GA90": ga90, "GA90_marj_icinde": bool(-marj < ga90[0] and ga90[1] < marj),
            "esdeger_0.05": bool(max(p_alt, p_ust) < 0.05)}


def eslesik_t(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = a - b
    n = d.size
    m, sd = float(d.mean()), float(d.std(ddof=1))
    t = m / (sd / math.sqrt(n))
    p = float(2 * stats.t.sf(abs(t), n - 1))
    return {"fark_degerleri": d.tolist(), "fark_ortalama": m, "fark_sd": sd, "t": t, "df": n - 1, "p_iki_yonlu": p}


def main():
    P = [oku_json(f"results/c1_c4/pair{c}/c4_summary.json") for c in (1, 2, 3)]
    for p in P:
        assert p["n_samples"] == 1000
    L = len(P[0]["vit"]["attention"]["entropy_delta_mean"])
    katman = []
    for l in range(L):
        d = [p["vit"]["attention"]["entropy_delta_mean"][l] for p in P]
        r = tost(d, MARJ)
        r["katman"] = l
        r["temiz_entropi_ort"] = float(np.mean([p["vit"]["attention"]["entropy_clean_mean"][l] for p in P]))
        katman.append(r)
    en_buyuk = max(katman, key=lambda r: r["p_TOST"])
    temiz = [r["temiz_entropi_ort"] for r in katman]

    # --- devrilen / devrilmeyen son blok kosinus
    def kos(tag, ad):
        fl = [p[tag]["cos_by_attack_outcome"][ad]["flipped"]["mean"] for p in P]
        nf = [p[tag]["cos_by_attack_outcome"][ad]["not_flipped"]["mean"] for p in P]
        nfl = [p[tag]["cos_by_attack_outcome"][ad]["flipped"]["n"] for p in P]
        nnf = [p[tag]["cos_by_attack_outcome"][ad]["not_flipped"]["n"] for p in P]
        havuz_fl = float(np.dot(fl, nfl) / np.sum(nfl))
        havuz_nf = float(np.dot(nf, nnf) / np.sum(nnf))
        return {"katman": ad,
                "devrilen_kosu_ortalamalari": fl, "devrilmeyen_kosu_ortalamalari": nf,
                "devrilen_n": nfl, "devrilmeyen_n": nnf,
                "devrilen_ortalama_kosular_arasi": float(np.mean(fl)),
                "devrilmeyen_ortalama_kosular_arasi": float(np.mean(nf)),
                "devrilen_sd_kosular_arasi": float(np.std(fl, ddof=1)),
                "devrilmeyen_sd_kosular_arasi": float(np.std(nf, ddof=1)),
                "devrilen_havuz_n_agirlikli": havuz_fl, "devrilmeyen_havuz_n_agirlikli": havuz_nf,
                "eslesik_t_kosu_duzeyi": eslesik_t(fl, nf),
                "isaret_tutarliligi": f"{sum(a > b for a, b in zip(fl, nf))}/3 kosuda devrilen > devrilmeyen"}

    vit_son = f"block{L - 1}.mlp"
    rn_son = list(P[0]["resnet"]["cos_by_attack_outcome"].keys())[-1]
    kosinus = {"ViT": kos("vit", vit_son), "ResNet": kos("resnet", rn_son)}

    # --- gerileme kontrolu: c1_c45_summary
    c45 = oku_json(C45)
    sd_c45 = c45.get("attention", {}).get("entropy_delta_std")
    kontrol = {
        "c45_entropy_delta_std_ile_max_fark": (max(abs(a - b["sd"]) for a, b in zip(sd_c45, katman)) if sd_c45 else "yok"),
        "c45_flip_split_last_block": c45.get("flip_split_last_block", "yok"),
        "c45_flip_split_resnet_last": c45.get("flip_split_resnet_last", "yok"),
    }

    out = {
        "uretildi_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "kaynaklar": dict(KAYNAK),
        "yontem": ("Katman basina kosu duzeyi TOST (n=3, df=2), marj +-0.05 nat (onceden sabit), p_TOST = max(iki "
                   "tek yonlu p); %90 GA'nin marj icinde olmasi esdeger kontrol. Kosinus: son blok "
                   f"({vit_son} ViT, {rn_son} ResNet), kosu ortalamalarinin ortalamasi ve kosu duzeyi eslestirilmis t."),
        "birim": "kosu (egitim cifti), n = 3; ornek bazli entropi saklanmadigi icin ornek duzeyi test YOK",
        "entropi_TOST": {
            "marj_nat": MARJ,
            "katmanlar": katman,
            "en_buyuk_p_TOST": en_buyuk["p_TOST"],
            "en_buyuk_p_katman": en_buyuk["katman"],
            "esdeger_katman_sayisi_0.05": sum(r["esdeger_0.05"] for r in katman),
            "katman_sayisi": L,
            "max_abs_ortalama_degisim_nat": max(abs(r["ortalama"]) for r in katman),
            "max_kosular_arasi_sd_nat": max(r["sd"] for r in katman),
            "temiz_entropi_katman_ortalamasi_araligi_nat": [min(temiz), max(temiz)],
        },
        "son_blok_kosinus_devrilen_vs_devrilmeyen": kosinus,
        "kosinus_tanim_notu": ("'devrilmeyen' grubu temizde zaten yanlis siniflanan ornekleri de icerir "
                               "(flipped = ok_clean & adv_wrong, experiments/c1_c4_attention_features.py)."),
        "gerileme_kontrolu_c1_c45_summary": kontrol,
    }
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print("yazildi:", OUT)
    for r in katman:
        print(f"L{r['katman']:2d} m {r['ortalama']:+.5f} sd {r['sd']:.5f} pTOST {r['p_TOST']:.3e} (kapali {r['p_TOST_kapali_bicim_df2']:.3e}) GA90 [{r['GA90'][0]:+.4f},{r['GA90'][1]:+.4f}] esd {r['esdeger_0.05']}")
    e = out["entropi_TOST"]
    print("en buyuk p:", e["en_buyuk_p_TOST"], "katman", e["en_buyuk_p_katman"], "esdeger", e["esdeger_katman_sayisi_0.05"], "/", L,
          "max|m|", e["max_abs_ortalama_degisim_nat"], "temiz aralik", e["temiz_entropi_katman_ortalamasi_araligi_nat"])
    for k, v in kosinus.items():
        print(k, v["katman"], "devrilen %.4f devrilmeyen %.4f | havuz %.4f %.4f | t %.3f p %.4f | %s" % (
            v["devrilen_ortalama_kosular_arasi"], v["devrilmeyen_ortalama_kosular_arasi"],
            v["devrilen_havuz_n_agirlikli"], v["devrilmeyen_havuz_n_agirlikli"],
            v["eslesik_t_kosu_duzeyi"]["t"], v["eslesik_t_kosu_duzeyi"]["p_iki_yonlu"], v["isaret_tutarliligi"]))
    print(kontrol)


if __name__ == "__main__":
    main()
