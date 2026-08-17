"""E2 A3: KOSULLU ATIF - secim sizintisi kosullu yaniltma isaretini ters cevirir mi?

NEDEN: Makale (05_discussion.tex, Limitations) su ablasyonu TAAHHUT ediyor:
"train pairs on identical data, varying only whether the selection split was
seen during pre-training, and measure whether CONDITIONAL ATTRIBUTION FLIPS."
E2 tam da bu ablasyonu kosturdu (V_A sizintili / V_B temiz / V_C negatif
kontrol) ama taahhut edilen UC NOKTAyi (kosullu yaniltma) olcmedi; yalniz
mutlak gurbuz dogruluk raporlandi. Bu betik eksik ucu kapatir ve GPU
GEREKTIRMEZ: gerekli her sey ornek-bazli maskelerde hazir.

TANIM (03_methodology.tex sat.97 + tab:conditional basligi):
    kosullu yaniltma = CLEAN-DOGRU orneklerin saldiriyla cevrilen orani
                     = 1 - P(adv dogru | clean dogru)
    Beyaz-kutu, AYNI model (capraz-model transfer DEGIL).
    Carpanlara ayirma tam: gurbuz = clean x (1 - kosullu_yaniltma).
    her-ikisi-dogru gurbuz = ciftin IKI modelinin de clean-dogru bildigi
    ortak alt kumede gurbuz dogruluk (birebir esli karsilastirma).

DORT KATMAN (giderek daha guclu yanit):
  1. SECILI checkpointler: 3 secim kurali (A/B/C) x 3 tohum cifti.
  2. CIFT FARKI: her kural icin kosullu yaniltmada ViT eksi CNN.
     Sizinti isareti ters cevirseydi, A ile B/C zit isaretli olurdu.
  3. IZGARA DAYANIKLILIGI: ayni fark, protokol izgarasinin TUM hucrelerinde
     (q1_e2_grid.py ile birebir ayni izgara: 2 bolme x 3 patience x
     3 yumusatma = 18 protokol) + ek olarak sizintili V_A izgarasi (9 hucre).
  4. EPOK-BAZLI: secim protokolunden TAMAMEN BAGIMSIZ yanit - farkin isareti
     100 epogun her birinde ve 100x100 epok kombinasyonunun tumunde.

SALDIRI NOTU: E2'de AutoAttack YOK, yalniz PGD-10 (eps=8/255, alpha=2/255,
10 adim). Makaledeki tab:conditional'in AA sutunu bu betikten gelmez.

Girdi (results/q1/e2/):
    select_<arch>_s<seed>_val{A,B,C}_test.npz   secili checkpoint 10k maskeleri
    select_<arch>_s<seed>_val{A,B,C}_valcurve.npz  100 epok x 2000 val maskesi
    testcurve_<arch>_s<seed>.npz                100 epok x 10k GERCEK test maskesi
Cikti: results/q1/e2/e2_conditional.json + konsol ozeti

Kullanim (konteyner icinde):
    python scripts/q1_e2_conditional.py --n-boot 10000
"""
import argparse
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT / "scripts"))
# Izgara tanimini TEKRAR YAZMA: A1 betiginden birebir devral (protokol tutarliligi)
from q1_e2_grid import KERNELS, MIN_DELTA, PATIENCES, SPLITS, smooth  # noqa: E402
from q1_offline_select import simulate_selection  # noqa: E402

CIFTLER = [("resnet18", 1001, "vit_tiny", 2001),
           ("resnet18", 1002, "vit_tiny", 2002),
           ("resnet18", 1003, "vit_tiny", 2003)]
KURALLAR = ["A", "B", "C"]
KURAL_ETIKET = {"A": "V_A sizintili", "B": "V_B temiz", "C": "V_C negatif kontrol"}
REF_PROTOKOL = ("B", 20, 1)   # q1_e2_grid.py ile ayni referans hucre


# ---------------------------------------------------------------- olcumler
def kosullu_yaniltma(clean, adv):
    """1 - P(adv dogru | clean dogru), yuzde puan. clean/adv: bool maske."""
    n_clean = int(clean.sum())
    if n_clean == 0:
        return float("nan"), 0, 0
    n_hayatta = int((clean & adv).sum())
    return 100.0 * (1.0 - n_hayatta / n_clean), n_clean, n_hayatta


def egri_kosullu_yaniltma(clean_mask, adv_mask):
    """Epok basina kosullu yaniltma (vektorlestirilmis). Girdi (E, N) bool."""
    n_clean = clean_mask.sum(axis=1).astype(float)
    n_hayatta = (clean_mask & adv_mask).sum(axis=1).astype(float)
    return 100.0 * (1.0 - n_hayatta / n_clean)


def mcnemar_log10p(n01, n10):
    """Esli ikili sonuclar icin tam (exact) McNemar; log10(p) doner."""
    n = n01 + n10
    if n == 0:
        return 0.0
    k = min(n01, n10)
    ln2 = math.log(2.0)
    terimler = [math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) - n * ln2
                for i in range(k + 1)]
    m = max(terimler)
    toplam = sum(math.exp(t - m) for t in terimler)
    log10p = (math.log(2.0) + m + math.log(toplam)) / math.log(10.0)
    return min(0.0, log10p)


def bootstrap_fark(clean_c, adv_c, clean_v, adv_v, n_boot, rng):
    """Ornek uzerinden yuzdelik bootstrap: ViT-CNN kosullu yaniltma farki CI.

    IKI model de AYNI 10k ornekte degerlendirildigi icin ayni yeniden-orneklem
    agirliklari her ikisine uygulanir -> fark ESLI olarak bootstraplanir.
    """
    bc = (clean_c & adv_c).astype(np.float64)
    cc = clean_c.astype(np.float64)
    bv = (clean_v & adv_v).astype(np.float64)
    cv = clean_v.astype(np.float64)
    n = cc.shape[0]
    p = np.full(n, 1.0 / n)
    farklar = np.empty(n_boot, dtype=np.float64)
    for t in range(n_boot):
        w = rng.multinomial(n, p).astype(np.float64)
        f_c = 100.0 * (1.0 - (w @ bc) / (w @ cc))
        f_v = 100.0 * (1.0 - (w @ bv) / (w @ cv))
        farklar[t] = f_v - f_c
    return farklar


# ---------------------------------------------------------------- yukleme
def yukle_secili(in_dir, arch, seed, kural):
    z = np.load(in_dir / f"select_{arch}_s{seed}_val{kural}_test.npz")
    return (z["clean_correct"].astype(bool), z["adv_correct"].astype(bool),
            int(z["selected_epoch"]))


def yukle_testcurve(in_dir, arch, seed):
    z = np.load(in_dir / f"testcurve_{arch}_s{seed}.npz")
    return {"epochs": z["epochs"].astype(int),
            "clean_mask": z["clean_mask"].astype(bool),
            "adv_mask": z["adv_mask"].astype(bool),
            "attack": str(z["attack"])}


def yukle_valcurve(in_dir, arch, seed, kural):
    z = np.load(in_dir / f"select_{arch}_s{seed}_val{kural}_valcurve.npz")
    return {"epochs": z["epochs"].astype(int),
            "adv": 100.0 * z["adv_mask"].mean(axis=1),
            "clean": 100.0 * z["clean_mask"].mean(axis=1)}


def sec_epok_index(vc, epochs, patience, k):
    """Bir protokol hucresinde secilen epogun testcurve icindeki indeksi."""
    adv = smooth(vc["adv"], k)
    cln = smooth(vc["clean"], k)
    ep, _, _ = simulate_selection(list(zip(epochs.tolist(), cln.tolist(), adv.tolist())),
                                 patience=patience, min_delta=MIN_DELTA)
    if ep is None:
        return None
    return int(np.where(epochs == ep)[0][0])


def isaret_ozeti(degerler):
    a = np.asarray([d for d in degerler if not math.isnan(d)], dtype=float)
    if a.size == 0:
        return {"n": 0}
    return {"n": int(a.size),
            "pozitif": int((a > 0).sum()), "negatif": int((a < 0).sum()),
            "sifir": int((a == 0).sum()),
            "isaret_tutarliligi": round(float(max((a > 0).mean(), (a < 0).mean())), 4),
            "min": round(float(a.min()), 4), "max": round(float(a.max()), 4),
            "ort": round(float(a.mean()), 4),
            "sd": round(float(a.std(ddof=1)), 4) if a.size > 1 else None}


# ---------------------------------------------------------------- ana akis
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default=str(ROOT / "results/q1/e2"))
    ap.add_argument("--out", default=str(ROOT / "results/q1/e2/e2_conditional.json"))
    ap.add_argument("--n-boot", type=int, default=10000, help="ornek-bazli bootstrap tekrari")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    in_dir = Path(args.in_dir)
    rng = np.random.default_rng(args.seed)

    rapor = {
        "meta": {
            "betik": "scripts/q1_e2_conditional.py",
            "amac": "05_discussion.tex Limitations'ta taahhut edilen ablasyonun uc noktasi: "
                    "secim sizintisi KOSULLU ATIFI ters cevirir mi?",
            "saldiri": "PGD-10, eps=8/255, alpha=2/255 (E2'de AutoAttack YOK)",
            "test_n": 10000, "bootstrap_n": args.n_boot, "seed": args.seed,
            "tohum_eslemesi": [f"{c[1]}<->{c[3]}" for c in CIFTLER],
        },
        "tanim": {
            "kosullu_yaniltma": "1 - P(adv dogru | clean dogru); beyaz-kutu, ayni model",
            "her_ikisi_dogru_gurbuz": "ciftin iki modelinin de clean-dogru bildigi ortak "
                                      "alt kumede adv dogruluk",
            "carpanlara_ayirma": "gurbuz = clean x (1 - kosullu_yaniltma)",
            "fark_yonu": "ViT eksi CNN (pozitif = ViT kosullu olarak DAHA kirilgan)",
        },
        "secili_checkpointler": {}, "cift_farklari": {},
        "izgara_dayanikliligi": {}, "sizintili_izgara": {},
        "epok_bazli": {}, "ozet": {},
    }

    # ---- 1 + 2: secili checkpointler ve cift farklari -----------------
    tablo = []
    for kural in KURALLAR:
        cift_kayit, farklar = [], []
        for arch_c, seed_c, arch_v, seed_v in CIFTLER:
            cc, ac, ep_c = yukle_secili(in_dir, arch_c, seed_c, kural)
            cv, av, ep_v = yukle_secili(in_dir, arch_v, seed_v, kural)
            assert cc.shape == cv.shape == (10000,), "test maskesi 10k degil"

            f_c, nc_c, _ = kosullu_yaniltma(cc, ac)
            f_v, nc_v, _ = kosullu_yaniltma(cv, av)
            ortak = cc & cv
            n_bc = int(ortak.sum())
            bc_c = 100.0 * ac[ortak].mean()
            bc_v = 100.0 * av[ortak].mean()
            n01 = int((ac[ortak] & ~av[ortak]).sum())   # CNN dogru, ViT yanlis
            n10 = int((~ac[ortak] & av[ortak]).sum())
            boot = bootstrap_fark(cc, ac, cv, av, args.n_boot, rng)

            for arch, seed, ep, cl, ad, f, ncl, bcr in (
                    (arch_c, seed_c, ep_c, cc, ac, f_c, nc_c, bc_c),
                    (arch_v, seed_v, ep_v, cv, av, f_v, nc_v, bc_v)):
                rapor["secili_checkpointler"].setdefault(arch, {}).setdefault(str(seed), {})[kural] = {
                    "secilen_epok": ep,
                    "clean_acc": round(100.0 * float(cl.mean()), 4),
                    "adv_acc": round(100.0 * float(ad.mean()), 4),
                    "kosullu_yaniltma": round(float(f), 4),
                    "n_clean_dogru": ncl,
                    "carpanlara_ayirma_kontrol": round(
                        100.0 * float(cl.mean()) * (1.0 - f / 100.0), 4),
                    "her_ikisi_dogru_gurbuz": round(float(bcr), 4),
                    "n_her_ikisi_dogru": n_bc,
                }

            fark = f_v - f_c
            farklar.append(fark)
            cift_kayit.append({
                "cift": f"{seed_c}<->{seed_v}",
                "cnn_secilen_epok": ep_c, "vit_secilen_epok": ep_v,
                "cnn_kosullu_yaniltma": round(f_c, 4), "vit_kosullu_yaniltma": round(f_v, 4),
                "fark_vit_eksi_cnn": round(fark, 4),
                "cnn_clean": round(100.0 * float(cc.mean()), 4),
                "vit_clean": round(100.0 * float(cv.mean()), 4),
                "cnn_adv": round(100.0 * float(ac.mean()), 4),
                "vit_adv": round(100.0 * float(av.mean()), 4),
                "n_her_ikisi_dogru": n_bc,
                "cnn_her_ikisi_dogru_gurbuz": round(bc_c, 4),
                "vit_her_ikisi_dogru_gurbuz": round(bc_v, 4),
                "her_ikisi_dogru_fark_cnn_eksi_vit": round(bc_c - bc_v, 4),
                "mcnemar_uyumsuz": {"cnn_dogru_vit_yanlis": n01, "vit_dogru_cnn_yanlis": n10},
                "mcnemar_log10_p": round(mcnemar_log10p(n01, n10), 2),
                "bootstrap_ci95_fark": [round(float(np.percentile(boot, 2.5)), 4),
                                        round(float(np.percentile(boot, 97.5)), 4)],
                "bootstrap_p_isaret_degisimi": round(float((boot <= 0).mean()), 6),
            })
            tablo.append((kural, f"{seed_c}<->{seed_v}", f_c, f_v, fark, bc_c, bc_v, n_bc))

        a = np.array(farklar)
        rapor["cift_farklari"][kural] = {
            "etiket": KURAL_ETIKET[kural], "per_cift": cift_kayit,
            "ort_fark": round(float(a.mean()), 4), "sd_fark": round(float(a.std(ddof=1)), 4),
            "isaret": "pozitif" if (a > 0).all() else ("negatif" if (a < 0).all() else "karisik"),
        }

    # ---- 3: protokol izgarasi ------------------------------------------
    tc = {(arch, seed): yukle_testcurve(in_dir, arch, seed)
          for arch, seed in [(c[0], c[1]) for c in CIFTLER] + [(c[2], c[3]) for c in CIFTLER]}
    epochs = tc[(CIFTLER[0][0], CIFTLER[0][1])]["epochs"]
    for v in tc.values():
        assert list(v["epochs"]) == list(epochs), "epok dizileri farkli"
    fool = {k: egri_kosullu_yaniltma(v["clean_mask"], v["adv_mask"]) for k, v in tc.items()}
    vc = {(arch, seed, kural): yukle_valcurve(in_dir, arch, seed, kural)
          for arch, seed in tc for kural in KURALLAR}

    def izgara_kos(bolmeler):
        hucreler, degerler = [], []
        for bolme in bolmeler:
            for patience in PATIENCES:
                for k in KERNELS:
                    for arch_c, seed_c, arch_v, seed_v in CIFTLER:
                        i_c = sec_epok_index(vc[(arch_c, seed_c, bolme)], epochs, patience, k)
                        i_v = sec_epok_index(vc[(arch_v, seed_v, bolme)], epochs, patience, k)
                        if i_c is None or i_v is None:
                            continue
                        f_c = float(fool[(arch_c, seed_c)][i_c])
                        f_v = float(fool[(arch_v, seed_v)][i_v])
                        hucreler.append({
                            "bolme": bolme, "patience": patience, "k": k,
                            "cift": f"{seed_c}<->{seed_v}",
                            "cnn_epok": int(epochs[i_c]), "vit_epok": int(epochs[i_v]),
                            "cnn_kosullu_yaniltma": round(f_c, 4),
                            "vit_kosullu_yaniltma": round(f_v, 4),
                            "fark_vit_eksi_cnn": round(f_v - f_c, 4)})
                        degerler.append(f_v - f_c)
        return hucreler, degerler

    hucreler, degerler = izgara_kos(SPLITS)
    rapor["izgara_dayanikliligi"] = {
        "izgara": {"bolmeler": SPLITS, "patience": PATIENCES, "yumusatma_k": KERNELS,
                   "min_delta": MIN_DELTA,
                   "protokol_sayisi": len(SPLITS) * len(PATIENCES) * len(KERNELS),
                   "cift_sayisi": len(CIFTLER),
                   "yumusatma_konvansiyonu": "kenar-dolgulu merkezi hareketli ortalama",
                   "kaynak": "q1_e2_grid.py ile birebir ayni izgara tanimi"},
        "hucreler": hucreler, "isaret": isaret_ozeti(degerler),
    }
    h_a, d_a = izgara_kos(["A"])
    rapor["sizintili_izgara"] = {
        "aciklama": "EK: sizintili V_A bolmesiyle ayni izgara (9 protokol x 3 cift). "
                    "On-kayitli izgara V_B/V_C ile sinirlidir; bu blok kesifseldir.",
        "hucreler": h_a, "isaret": isaret_ozeti(d_a),
    }

    # ---- 3b: ERISILEBILIR secim bolgesi --------------------------------
    # Bir protokolun ASLA secmedigi epoklar, "secim sizintisi isareti cevirir mi"
    # sorusuyla ilgisizdir. Her model icin 27 protokolun (A/B/C x patience x k)
    # secebildigi epok kumesini cikar; cift icin bu kumelerin TAM CAPRAZI'nda
    # (protokoller eslesmese bile) isaret degisiyor mu diye bak.
    erisilebilir = {}
    for arch, seed in tc:
        idx = set()
        for kural in KURALLAR:
            for patience in PATIENCES:
                for k in KERNELS:
                    i = sec_epok_index(vc[(arch, seed, kural)], epochs, patience, k)
                    if i is not None:
                        idx.add(i)
        erisilebilir[(arch, seed)] = sorted(idx)

    # ---- 4: epok-bazli (secim protokolunden bagimsiz) ------------------
    IKINCI_YARI = 50   # indeks >= 50 -> epok 51..100 (sabit butcenin ikinci yarisi)
    epok_kayit, tum_esli, tum_yari, tum_capraz, tum_eris = [], [], [], [], []
    for arch_c, seed_c, arch_v, seed_v in CIFTLER:
        f_c, f_v = fool[(arch_c, seed_c)], fool[(arch_v, seed_v)]
        d = f_v - f_c                                   # epok-esli (100,)
        capraz = f_v[:, None] - f_c[None, :]            # tum 100x100 kombinasyon
        neg = (np.where(d < 0)[0] + 1).tolist()
        i_c, i_v = erisilebilir[(arch_c, seed_c)], erisilebilir[(arch_v, seed_v)]
        eris = (f_v[i_v][:, None] - f_c[i_c][None, :]).ravel()
        epok_kayit.append({
            "cift": f"{seed_c}<->{seed_v}",
            "esli_epok": isaret_ozeti(d.tolist()),
            "negatif_epoklar": neg,
            "en_buyuk_negatif_epok": max(neg) if neg else None,
            "ikinci_yari_epok51_100": isaret_ozeti(d[IKINCI_YARI:].tolist()),
            "erisilebilir_capraz": {
                "cnn_epoklari": [int(epochs[i]) for i in i_c],
                "vit_epoklari": [int(epochs[i]) for i in i_v],
                **isaret_ozeti(eris.tolist())},
            "capraz_100x100": {"n": int(capraz.size),
                               "pozitif": int((capraz > 0).sum()),
                               "negatif": int((capraz < 0).sum()),
                               "min": round(float(capraz.min()), 4),
                               "max": round(float(capraz.max()), 4)},
            "cnn_kosullu_yaniltma_epok": [round(float(x), 3) for x in f_c],
            "vit_kosullu_yaniltma_epok": [round(float(x), 3) for x in f_v],
        })
        tum_esli.extend(d.tolist())
        tum_yari.extend(d[IKINCI_YARI:].tolist())
        tum_eris.extend(eris.tolist())
        tum_capraz.append(capraz)
    capraz_hep = np.concatenate([c.ravel() for c in tum_capraz])
    en_buyuk_neg = max([e["en_buyuk_negatif_epok"] or 0 for e in epok_kayit])
    rapor["epok_bazli"] = {
        "aciklama": "Hicbir secim kurali kullanilmaz: her epogun GERCEK 10k test maskesi.",
        "per_cift": epok_kayit,
        "tum_esli_epoklar": isaret_ozeti(tum_esli),
        "tum_esli_ikinci_yari": isaret_ozeti(tum_yari),
        "erisilebilir_bolge": {
            "aciklama": "27 protokolun (A/B/C x 3 patience x 3 yumusatma) secebildigi "
                        "epoklarin cift-ici TAM CAPRAZI; protokoller eslesmese bile.",
            **isaret_ozeti(tum_eris)},
        "isaret_degisiminin_epok_tavani": en_buyuk_neg,
        "tum_capraz_kombinasyonlar": {"n": int(capraz_hep.size),
                                      "pozitif": int((capraz_hep > 0).sum()),
                                      "negatif": int((capraz_hep < 0).sum()),
                                      "isaret_tutarliligi": round(float((capraz_hep > 0).mean()), 6),
                                      "min": round(float(capraz_hep.min()), 4),
                                      "max": round(float(capraz_hep.max()), 4)},
    }

    # ---- ozet ----------------------------------------------------------
    kural_ort = {k: rapor["cift_farklari"][k]["ort_fark"] for k in KURALLAR}
    tum_secili = [c["fark_vit_eksi_cnn"] for k in KURALLAR
                  for c in rapor["cift_farklari"][k]["per_cift"]]
    n_secili = isaret_ozeti(tum_secili)
    n_izgara = rapor["izgara_dayanikliligi"]["isaret"]
    n_sizinti = rapor["sizintili_izgara"]["isaret"]
    n_eris = rapor["epok_bazli"]["erisilebilir_bolge"]
    n_epok = rapor["epok_bazli"]["tum_esli_epoklar"]
    tavan = rapor["epok_bazli"]["isaret_degisiminin_epok_tavani"]
    secim_ters = any(b.get("negatif", 0) > 0 for b in (n_secili, n_izgara, n_sizinti, n_eris))
    rapor["ozet"] = {
        "kural_bazli_ort_fark": kural_ort,
        "kurallar_arasi_yayilim": round(max(kural_ort.values()) - min(kural_ort.values()), 4),
        "secili_9_olcum": n_secili,
        "izgara_isaret_tutarliligi": n_izgara["isaret_tutarliligi"],
        "erisilebilir_isaret_tutarliligi": n_eris["isaret_tutarliligi"],
        "epok_isaret_tutarliligi": n_epok["isaret_tutarliligi"],
        "secim_kaynakli_ters_donme": secim_ters,
        "hukum": None,
    }
    if secim_ters:
        rapor["ozet"]["hukum"] = (
            "TERS DONME GOZLENDI: bir secim kurali veya protokol hucresi kosullu "
            "atifin isaretini degistiriyor")
    elif n_epok.get("negatif", 0) > 0:
        rapor["ozet"]["hukum"] = (
            "SECIM KAYNAKLI TERS DONME YOK: ViT>CNN kosullu yaniltma isareti 9 secili "
            f"checkpointin, {n_izgara['n']} temiz + {n_sizinti['n']} sizintili protokol "
            f"hucresinin ve erisilebilir secim bolgesinin ({n_eris['n']} epok cifti) "
            f"TAMAMINDA korunuyor. Isaret yalnizca yakinsama ONCESI ilk {tavan} epokta "
            "degisiyor; hicbir secim protokolu o bolgeyi secmiyor (PGD-10)")
    else:
        rapor["ozet"]["hukum"] = (
            "TERS DONME YOK: kosullu yaniltmada ViT>CNN isareti tum secim kurallarinda, "
            "tum protokol hucrelerinde ve tum epoklarda korunuyor (PGD-10)")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out + ".tmp", "w") as f:
        json.dump(rapor, f, indent=2)
    os.replace(args.out + ".tmp", args.out)

    # ---- konsol --------------------------------------------------------
    print(f"\n=== E2 KOSULLU ATIF (PGD-10; E2'de AutoAttack YOK) -> {args.out} ===")
    print("kosullu yaniltma = 1 - P(adv dogru | clean dogru), beyaz-kutu\n")
    print(f"{'kural':<22}{'cift':<14}{'CNN fool':>10}{'ViT fool':>10}{'fark':>9}"
          f"{'CNN bc':>9}{'ViT bc':>9}{'n_bc':>7}")
    print("-" * 90)
    for kural, cift, f_c, f_v, fark, bc_c, bc_v, n_bc in tablo:
        print(f"{kural + ' (' + KURAL_ETIKET[kural] + ')':<22}{cift:<14}"
              f"{f_c:>10.2f}{f_v:>10.2f}{fark:>+9.2f}{bc_c:>9.2f}{bc_v:>9.2f}{n_bc:>7d}")
    print("-" * 90)
    for kural in KURALLAR:
        r = rapor["cift_farklari"][kural]
        print(f"{kural + ' (' + KURAL_ETIKET[kural] + ')':<22}{'ORT+-SD':<14}"
              f"{'':>10}{'':>10}{r['ort_fark']:>+9.2f}  (sd {r['sd_fark']:.2f}, "
              f"isaret: {r['isaret']})")

    print("\n--- ISARET TUTARLILIGI (ViT eksi CNN kosullu yaniltma) ---")
    s = rapor["ozet"]["secili_9_olcum"]
    print(f"  secili checkpointler : {s['pozitif']}/{s['n']} pozitif | "
          f"aralik {s['min']:+.2f}..{s['max']:+.2f}")
    g = rapor["izgara_dayanikliligi"]["isaret"]
    print(f"  protokol izgarasi    : {g['pozitif']}/{g['n']} pozitif "
          f"({rapor['izgara_dayanikliligi']['izgara']['protokol_sayisi']} protokol x "
          f"{len(CIFTLER)} cift) | aralik {g['min']:+.2f}..{g['max']:+.2f}")
    ga = rapor["sizintili_izgara"]["isaret"]
    print(f"  sizintili V_A izgara : {ga['pozitif']}/{ga['n']} pozitif | "
          f"aralik {ga['min']:+.2f}..{ga['max']:+.2f}")
    er = rapor["epok_bazli"]["erisilebilir_bolge"]
    print(f"  erisilebilir bolge   : {er['pozitif']}/{er['n']} pozitif "
          f"(27 protokolun secebildigi epoklarin tam caprazi) | "
          f"aralik {er['min']:+.2f}..{er['max']:+.2f}")
    e = rapor["epok_bazli"]["tum_esli_epoklar"]
    print(f"  epok-esli (protokolsuz): {e['pozitif']}/{e['n']} pozitif | "
          f"aralik {e['min']:+.2f}..{e['max']:+.2f} | negatiflerin epok tavani: "
          f"{rapor['epok_bazli']['isaret_degisiminin_epok_tavani']}")
    ey = rapor["epok_bazli"]["tum_esli_ikinci_yari"]
    print(f"  epok-esli 51-100     : {ey['pozitif']}/{ey['n']} pozitif | "
          f"aralik {ey['min']:+.2f}..{ey['max']:+.2f}")
    cx = rapor["epok_bazli"]["tum_capraz_kombinasyonlar"]
    print(f"  tum 100x100 epok cifti : {cx['pozitif']}/{cx['n']} pozitif | "
          f"aralik {cx['min']:+.2f}..{cx['max']:+.2f}")
    print(f"\n  kural ort: A {kural_ort['A']:+.2f} | B {kural_ort['B']:+.2f} | "
          f"C {kural_ort['C']:+.2f}  (yayilim {rapor['ozet']['kurallar_arasi_yayilim']:.2f} puan)")
    print(f"\nHUKUM: {rapor['ozet']['hukum']}")


if __name__ == "__main__":
    main()
