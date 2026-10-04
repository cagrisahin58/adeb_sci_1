"""Model havuzu analizi (LeCun plani Faz 2, 2026-10-04).

Girdi: c1_c3_transfer_matrix.py'nin yazdigi klasor (per_sample_<src>_to_<tgt>.npz + transfer_matrix.json).
Her yonlu cift icin: dort protokol orani (src/analysis/protokoller.py), payda boyutlari, oncul
p = P(hedef cekismeli yanlis | hedef temiz yanlis), ozdeslikle ongorulen ham oran (e*p + r_tc*(1-e)) ve artik.
Her yonsuz cift icin: protokol basina asimetri (A->B eksi B->A), dort ve uc protokol yayilimi, temiz
dogruluk farki. Havuz ozeti: yayilim ~ temiz fark egimi (OLS; ciftler model paylastigi icin model
bazli kume bootstrap), p'nin hedef turune gore dagilimi, hedef-dogru oranlarda toplamsal kaynak+hedef
ayristirmasi (en kucuk kareler, toplam-sifir kisiti, kosegen haric).

Kullanim (konteyner, depo koku):
  python experiments/q1_havuz_analiz.py results/q1/havuz_cifar10 [--etiketler models.json] [--tohum 42]
Cikti: <klasor>/havuz_protokoller.json
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.analysis.protokoller import PROTOKOLLER, protokol_oranlari  # noqa: E402


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def yonlu(npz_path, kaynak_kosegen=None):
    z = np.load(npz_path)
    tc, aw = z["target_clean_correct"].astype(bool), z["target_adv_wrong"].astype(bool)
    if "source_adv_wrong" in z.files:
        sc, sa = z["source_clean_correct"].astype(bool), z["source_adv_wrong"].astype(bool)
    else:
        # eski sema (C1 kampanyasi): kaynagin kendi beyaz kutu sonucu kosegen dosyasindan
        # (per_sample_<src>_to_<src>.npz; ayni ornek sirasi) alinir.
        d = np.load(kaynak_kosegen)
        sc, sa = d["target_clean_correct"].astype(bool), d["target_adv_wrong"].astype(bool)
    oran = protokol_oranlari(tc, aw, sc, sa, tani=True)
    e = 100.0 * (~tc).mean()
    yanlis = ~tc
    p = float(aw[yanlis].mean()) if yanlis.sum() else float("nan")
    r_tc = oran["target_correct"]
    # Tam ozdeslik r_raw = e*p + r_tc*(1-e) ayni orneklerde TANIM GEREGI saglanir (toplam olasilik);
    # bilgi tasiyan nicelik p'dir. Makaledeki "0,41 puan" artigi p=1 yaklasikligina aittir:
    # r_raw - [e + r_tc*(1-e)] = -e*(1-p).
    ongoru_p1 = e + r_tc * (1 - e / 100.0)
    ongoru = e * p + r_tc * (1 - e / 100.0)
    return {
        "oranlar": {k: oran[k] for k in PROTOKOLLER},
        "successful_source_loose": oran.get("successful_source_loose"),
        "paydalar": {
            "raw": int(tc.size), "target_correct": int(tc.sum()),
            "both_correct": int((tc & sc).sum()), "successful_source": int((tc & sc & sa).sum()),
        },
        "hedef_temiz_hata_e": e,
        "hedef_temiz_dogruluk": 100.0 - e,
        "kaynak_temiz_dogruluk": 100.0 * sc.mean(),
        "kaynak_beyaz_kutu_basari_temiz_dogru": 100.0 * (sa[sc].mean()) if sc.sum() else float("nan"),
        "p_adv_yanlis_verili_temiz_yanlis": p,
        "n_temiz_yanlis": int(yanlis.sum()),
        "ozdeslik_tam_ongoru_ham": ongoru,
        "ozdeslik_tam_artik_kontrol": oran["raw"] - ongoru,  # ~0 beklenir (tanim geregi)
        "ozdeslik_p1_ongoru_ham": ongoru_p1,
        "ozdeslik_artigi_ham_eksi_ongoru": oran["raw"] - ongoru_p1,  # = -e(1-p), makaledeki artik
        "ham_eksi_tc": oran["raw"] - r_tc,
    }


def ols(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    A = np.vstack([x, np.ones_like(x)]).T
    (m, b), *_ = np.linalg.lstsq(A, y, rcond=None)
    yhat = A @ np.array([m, b])
    ss_res = float(((y - yhat) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    r = float(np.corrcoef(x, y)[0, 1]) if len(x) > 2 else float("nan")
    return float(m), float(b), r2, r


def toplamsal(adlar, oran):
    """oran[(s,t)] -> mu + a_s + b_t, toplam-sifir kisiti, kosegen haric."""
    n = len(adlar)
    idx = {a: i for i, a in enumerate(adlar)}
    rows, y = [], []
    for (s, t), v in oran.items():
        if s == t:
            continue
        r = np.zeros(1 + 2 * n)
        r[0] = 1
        r[1 + idx[s]] = 1
        r[1 + n + idx[t]] = 1
        rows.append(r)
        y.append(v)
    X, y = np.array(rows), np.array(y)
    # kisitlar: sum a = 0, sum b = 0 (agirlikli satir olarak)
    k1 = np.zeros(1 + 2 * n); k1[1:1 + n] = 1
    k2 = np.zeros(1 + 2 * n); k2[1 + n:] = 1
    Xc = np.vstack([X, 1e3 * k1, 1e3 * k2])
    yc = np.concatenate([y, [0.0, 0.0]])
    beta, *_ = np.linalg.lstsq(Xc, yc, rcond=None)
    yhat = X @ beta
    art = y - yhat
    ss_tot = float(((y - y.mean()) ** 2).sum())
    return {
        "mu": float(beta[0]),
        "kaynak_etkisi": {a: float(beta[1 + idx[a]]) for a in adlar},
        "hedef_etkisi": {a: float(beta[1 + n + idx[a]]) for a in adlar},
        "artik_max_mutlak": float(np.abs(art).max()),
        "artik_rms": float(np.sqrt((art ** 2).mean())),
        "R2": float(1 - (art ** 2).sum() / ss_tot) if ss_tot > 0 else float("nan"),
        "n_hucre": int(len(y)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("klasor")
    ap.add_argument("--tohum", type=int, default=42)
    ap.add_argument("--bootstrap", type=int, default=10000)
    ap.add_argument("--cikti", default=None)
    args = ap.parse_args()
    kl = Path(args.klasor)
    tm = json.loads((kl / "transfer_matrix.json").read_text(encoding="utf-8"))
    kaynaklar = {str(kl / "transfer_matrix.json"): sha(kl / "transfer_matrix.json")}
    # c1_c3_transfer_matrix.py semasi: {"models": [...], "results": {"A->B": {...}}}
    adlar = list(tm.get("models") or sorted({k.split("->")[0] for k in tm.get("results", tm) if "->" in k}))
    yon = {}
    for s in adlar:
        for t in adlar:
            f = kl / f"per_sample_{s}_to_{t}.npz"
            if not f.exists():
                continue
            kaynaklar[str(f)] = sha(f)
            yon[f"{s}->{t}"] = yonlu(f, kaynak_kosegen=kl / f"per_sample_{s}_to_{s}.npz")
    temiz = {a: yon[f"{a}->{a}"]["hedef_temiz_dogruluk"] for a in adlar if f"{a}->{a}" in yon}

    ciftler = []
    for a, b in combinations(adlar, 2):
        if f"{a}->{b}" not in yon or f"{b}->{a}" not in yon:
            continue
        ab, ba = yon[f"{a}->{b}"]["oranlar"], yon[f"{b}->{a}"]["oranlar"]
        asim = {p: ab[p] - ba[p] for p in PROTOKOLLER}
        v4 = list(asim.values())
        v3 = [asim[p] for p in ("raw", "target_correct", "both_correct")]
        ciftler.append({
            "cift": [a, b], "yon_ileri": f"{a}->{b}",
            "asimetri_ileri_eksi_geri": asim,
            "yayilim_dort_protokol": max(v4) - min(v4),
            "yayilim_uc_protokol_bas_kaynak_haric": max(v3) - min(v3),
            "temiz_dogruluk_farki_mutlak": abs(temiz[a] - temiz[b]),
            "onaylanan_ikili_ayni_isaret": (asim["target_correct"] > 0) == (asim["both_correct"] > 0),
            "isaret_degisiyor_mu_dort_protokol": (max(v4) > 0) and (min(v4) < 0),
        })

    # egim: yayilim ~ |temiz fark| ; model-bazli kume bootstrap (model birak-tut)
    rng = np.random.default_rng(args.tohum)
    xs = np.array([c["temiz_dogruluk_farki_mutlak"] for c in ciftler])
    y4 = np.array([c["yayilim_dort_protokol"] for c in ciftler])
    y3 = np.array([c["yayilim_uc_protokol_bas_kaynak_haric"] for c in ciftler])
    egimler = {}
    for ad, yy in (("dort_protokol", y4), ("uc_protokol_bas_kaynak_haric", y3)):
        if len(xs) >= 3:
            m, b, r2, r = ols(xs, yy)
            boots = []
            for _ in range(args.bootstrap):
                sec = set(rng.choice(adlar, size=len(adlar), replace=True))
                maske = np.array([c["cift"][0] in sec and c["cift"][1] in sec for c in ciftler])
                if maske.sum() >= 3 and np.ptp(xs[maske]) > 0:
                    boots.append(ols(xs[maske], yy[maske])[0])
            egimler[ad] = {"egim": m, "kesisim": b, "R2": r2, "pearson_r": r, "n_cift": int(len(xs)),
                           "egim_GA95_model_bootstrap": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))] if boots else None,
                           "bootstrap_gecerli_ornek": len(boots),
                           "NOT": "ciftler modelleri paylasir; GA model birak-tut bootstrap'indan, cift sayisi serbestlik derecesi DEGILDIR"}
        else:
            egimler[ad] = {"NOT": "uc ciftten az; egim uydurulmadi"}

    # p ozeti
    p_list = [(k, v["p_adv_yanlis_verili_temiz_yanlis"], v["n_temiz_yanlis"]) for k, v in yon.items()
              if k.split("->")[0] != k.split("->")[1]]
    art_list = [abs(v["ozdeslik_artigi_ham_eksi_ongoru"]) for k, v in yon.items() if k.split("->")[0] != k.split("->")[1]]
    ozet_p = {
        "n_yon": len(p_list),
        "p_min": float(min(p for _, p, _ in p_list)) if p_list else None,
        "p_max": float(max(p for _, p, _ in p_list)) if p_list else None,
        "p_hedef_bazinda": {t: {"p_min": float(min(p for k, p, _ in p_list if k.endswith("->" + t))),
                               "p_max": float(max(p for k, p, _ in p_list if k.endswith("->" + t))),
                               "hedef_temiz_dogruluk": temiz.get(t)} for t in adlar},
        "ozdeslik_artigi_mutlak_max_puan": float(max(art_list)) if art_list else None,
        "ozdeslik_artigi_mutlak_ort_puan": float(np.mean(art_list)) if art_list else None,
    }
    tc_oran = {(k.split("->")[0], k.split("->")[1]): v["oranlar"]["target_correct"] for k, v in yon.items()}
    ayristirma = toplamsal(adlar, tc_oran) if len(adlar) >= 3 else {"NOT": "ucten az model"}

    cikti = {
        "uretildi_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "klasor": str(kl), "modeller": adlar, "temiz_dogruluk": temiz,
        "kaynaklar": kaynaklar, "tohum": args.tohum,
        "yontem": "src/analysis/protokoller.py dort protokol; p = P(adv yanlis | temiz yanlis); "
                  "ozdeslik r_raw = e*p + r_tc*(1-e); yayilim = max-min asimetri; OLS + model bootstrap; "
                  "toplamsal ayristirma hedef-dogru oranlarda, toplam-sifir kisiti, kosegen haric",
        "yonlu": yon, "ciftler": ciftler, "egim_yayilim_temiz_fark": egimler,
        "oncul_p_ozeti": ozet_p, "toplamsal_kaynak_hedef_hedef_dogru": ayristirma,
    }
    out = Path(args.cikti) if args.cikti else kl / "havuz_protokoller.json"
    out.write_text(json.dumps(cikti, indent=1, ensure_ascii=False), encoding="utf-8")
    print("yazildi:", out)
    print("modeller:", adlar)
    print("temiz:", {k: round(v, 2) for k, v in temiz.items()})
    print("p min/max:", ozet_p["p_min"], ozet_p["p_max"], "| artik max:", ozet_p["ozdeslik_artigi_mutlak_max_puan"])
    for c in ciftler:
        print(f"  {c['yon_ileri']:40s} asim raw/tc/bc/ss = "
              + "/".join(f"{c['asimetri_ileri_eksi_geri'][p]:+.2f}" for p in PROTOKOLLER)
              + f"  yayilim4={c['yayilim_dort_protokol']:.2f} yayilim3={c['yayilim_uc_protokol_bas_kaynak_haric']:.2f} "
              + f"temiz_fark={c['temiz_dogruluk_farki_mutlak']:.2f}")
    print("egim:", {k: (round(v.get("egim", float('nan')), 3), v.get("egim_GA95_model_bootstrap")) for k, v in egimler.items()})
    print("ayristirma:", {k: (v if not isinstance(v, dict) else {a: round(b, 2) for a, b in v.items()}) for k, v in ayristirma.items() if k in ("kaynak_etkisi", "hedef_etkisi", "artik_max_mutlak", "R2")})


if __name__ == "__main__":
    main()
