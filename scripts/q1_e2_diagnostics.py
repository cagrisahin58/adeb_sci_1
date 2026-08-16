"""E2 KESIFSEL tanilar: kural-duyarliligi + kanal ayrisimi + bolme ofseti.

On-kayitli protokol Bolum 8 kapsaminda KESIFSEL. Birincil uc noktalari
(q1_e2_report.py) DEGISTIRMEZ; makalede "kesifsel" etiketiyle sunulur.
Cursutme denetiminin (2026-08-16, 3 mercek) elde ettigi analizleri
tekrarlanabilir kod haline getirir.

UC TANI:
1. KURAL DUYARLILIGI: ayni val egrilerine farkli erken-durdurma sabirlariyla
   (patience 0=saf argmax, 10, 20=on-kayitli) secim kurali uygulanir. Amac:
   "A ve B ayni epogu secti" gibi desenlerin kurala kosullu olup olmadigini
   gostermek (denetim: patience 0'da desen TERSINE DONUYOR).
2. KANAL AYRISIMI (asil bulgu): V_A'nin (sizintili bolme) temiz ve cekismeli
   dogruluklari, HIC GORULMEMIS V_B u V_C havuzundan cekilen 2000'lik
   bootstrap referans dagilimina karsi z-skoruyla karsilastirilir. Beklenen
   desen: temiz kanalda ANLAMLI fazla (sizinti izi 100 epok AT'yi atlatiyor),
   cekismeli kanalda (SECIM METRIGI) fazla YOK -> "clean-asamasi sizintisi
   cekismeli val metrigini sismiyor". Ek olarak adv'ye KOSULLU temiz artik
   (bootstrap cizgisel uyumundan) raporlanir.
3. BOLME OFSETI: V_B vs V_C'nin sistematik zorluk farki - Delta_BC'nin "saf
   gurultu" degil "gurultu + sabit ofset" oldugunu beyan etmek icin.

Kullanim (konteyner icinde):
    python scripts/q1_e2_diagnostics.py --n-boot 20000
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

PATIENCES = [0, 10, 20]   # 0 = saf argmax (erken durdurma yok), 20 = on-kayitli


def load_curve(path):
    z = np.load(path)
    return (z["epochs"].astype(int), z["clean_mask"].astype(bool),
            z["adv_mask"].astype(bool))


def rule_sensitivity(epochs, clean_mask, adv_mask, min_delta):
    """Ayni egriye farkli patience degerleriyle secim kurali."""
    clean = 100.0 * clean_mask.mean(axis=1)
    adv = 100.0 * adv_mask.mean(axis=1)
    recs = list(zip(epochs.tolist(), clean.tolist(), adv.tolist()))
    out = {}
    for p in PATIENCES:
        ep, a, stop = simulate_selection(recs, patience=p, min_delta=min_delta)
        out[str(p)] = {"secilen_epok": ep, "val_adv": round(a, 4),
                       "durus": stop}
    out["ham_argmax_epok"] = int(epochs[int(np.argmax(adv))])
    out["tepe_val_adv"] = round(float(adv.max()), 4)
    return out


def channel_separation(a_clean, a_adv, ref_clean, ref_adv, n_boot, rng):
    """V_A'nin temiz/cekismeli seviyesi, V_B u V_C bootstrap referansina karsi.

    Ornek-basi skor = o ornegin 100 epok boyunca dogru bilinme orani; bir
    bolmenin "seviyesi" = bu skorlarin ortalamasi (= epoklar boyunca ortalama
    dogruluk). Referans: havuzdan 2000'lik yeniden ornekleme.
    """
    n = a_clean.size
    bc = rng.choice(ref_clean.size, size=(n_boot, n), replace=True)
    b_clean = ref_clean[bc].mean(axis=1)
    b_adv = ref_adv[bc].mean(axis=1)
    obs_clean, obs_adv = float(a_clean.mean()), float(a_adv.mean())

    def z(obs, dist):
        return float((obs - dist.mean()) / dist.std(ddof=1))

    # adv'ye KOSULLU temiz artik: bootstrap bulutunda clean ~ adv dogrusu
    slope, intercept = np.polyfit(b_adv, b_clean, 1)
    resid = b_clean - (slope * b_adv + intercept)
    cond_z = float((obs_clean - (slope * obs_adv + intercept)) / resid.std(ddof=1))
    return {
        "temiz": {"V_A": round(100 * obs_clean, 4),
                  "referans_ort": round(100 * float(b_clean.mean()), 4),
                  "fazla_puan": round(100 * (obs_clean - float(b_clean.mean())), 4),
                  "z": round(z(obs_clean, b_clean), 3),
                  "p_iki_yonlu": round(float(2 * min((b_clean >= obs_clean).mean(),
                                                     (b_clean <= obs_clean).mean())), 5)},
        "cekismeli_SECIM_METRIGI": {
            "V_A": round(100 * obs_adv, 4),
            "referans_ort": round(100 * float(b_adv.mean()), 4),
            "fazla_puan": round(100 * (obs_adv - float(b_adv.mean())), 4),
            "z": round(z(obs_adv, b_adv), 3),
            "p_iki_yonlu": round(float(2 * min((b_adv >= obs_adv).mean(),
                                               (b_adv <= obs_adv).mean())), 5),
            "fazla_ust_sinir_p95": round(100 * float(np.percentile(obs_adv - b_adv, 95)), 4)},
        "adv_kosullu_temiz_artik_z": round(cond_z, 3),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default=str(ROOT / "results/q1/e2"))
    ap.add_argument("--out", default=str(ROOT / "results/q1/e2/e2_diagnostics.json"))
    ap.add_argument("--n-boot", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=20260816)
    ap.add_argument("--min-delta", type=float, default=0.1)
    args = ap.parse_args()

    in_dir = Path(args.in_dir)
    rng = np.random.default_rng(args.seed)
    out = {"kesifsel": True, "protokol": "E2_ISTATISTIK_PROTOKOLU.md Bolum 8",
           "n_boot": args.n_boot, "seed": args.seed, "yorungeler": {}}

    for apath in sorted(in_dir.glob("select_*_valA_valcurve.npz")):
        tag = re.sub(r"^select_|_valA_valcurve\.npz$", "", apath.name)
        paths = {c: apath.with_name(apath.name.replace("_valA_", f"_val{c}_"))
                 for c in "ABC"}
        if not all(p.exists() for p in paths.values()):
            print(f"ATLA {tag}: A/B/C valcurve tamam degil")
            continue
        curves = {c: load_curve(str(p)) for c, p in paths.items()}
        epochs = curves["A"][0]

        res = {"kural_duyarliligi": {
            c: rule_sensitivity(*curves[c], args.min_delta) for c in "ABC"}}

        # kanal ayrisimi: ornek-basi "epoklar boyunca dogru bilinme orani"
        a_clean = curves["A"][1].mean(axis=0)
        a_adv = curves["A"][2].mean(axis=0)
        ref_clean = np.concatenate([curves["B"][1].mean(axis=0), curves["C"][1].mean(axis=0)])
        ref_adv = np.concatenate([curves["B"][2].mean(axis=0), curves["C"][2].mean(axis=0)])
        res["kanal_ayrisimi"] = channel_separation(a_clean, a_adv, ref_clean,
                                                   ref_adv, args.n_boot, rng)

        # bolme zorluk ofseti (B - C), epoklar boyunca ortalama
        res["bolme_ofseti_B_eksi_C"] = {
            "temiz_puan": round(100 * float(curves["B"][1].mean() - curves["C"][1].mean()), 4),
            "cekismeli_puan": round(100 * float(curves["B"][2].mean() - curves["C"][2].mean()), 4),
        }
        out["yorungeler"][tag] = res

        k = res["kural_duyarliligi"]
        print(f"\n{tag}")
        print("  KURAL DUYARLILIGI (secilen epok):")
        for p in PATIENCES:
            trio = "/".join(str(k[c][str(p)]["secilen_epok"]) for c in "ABC")
            lbl = "saf argmax" if p == 0 else ("ON-KAYITLI" if p == 20 else "")
            print(f"    patience {p:<3} A/B/C = {trio:<12} {lbl}")
        ch = res["kanal_ayrisimi"]
        print("  KANAL AYRISIMI (V_A, hic gorulmemis B u C referansina karsi):")
        print(f"    temiz    : {ch['temiz']['fazla_puan']:+.2f} puan  z={ch['temiz']['z']:+.2f}  p={ch['temiz']['p_iki_yonlu']}")
        print(f"    cekismeli: {ch['cekismeli_SECIM_METRIGI']['fazla_puan']:+.2f} puan  "
              f"z={ch['cekismeli_SECIM_METRIGI']['z']:+.2f}  p={ch['cekismeli_SECIM_METRIGI']['p_iki_yonlu']}"
              f"  (fazla %95 ust sinir {ch['cekismeli_SECIM_METRIGI']['fazla_ust_sinir_p95']:+.2f} puan)")
        print(f"    adv-kosullu temiz artik z = {ch['adv_kosullu_temiz_artik_z']:+.2f}")
        o = res["bolme_ofseti_B_eksi_C"]
        print(f"  BOLME OFSETI (B-C): temiz {o['temiz_puan']:+.2f}, cekismeli {o['cekismeli_puan']:+.2f} puan")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out + ".tmp", "w") as f:
        json.dump(out, f, indent=2)
    os.replace(args.out + ".tmp", args.out)
    print(f"\nkaydedildi: {args.out}")


if __name__ == "__main__":
    main()
