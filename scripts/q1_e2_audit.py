"""E2 curutme denetiminin KOD ARTEFAKTI: duzyazidaki 9 anahtar sayinin
bagimsiz yeniden uretimi ve iddia-karsilastirmasi.

NEDEN: `results/q1/e2/E2_SONUC_VE_DENETIM.md` hukum belgesindeki tum anahtar
sayilar (theta, sd uclusu, eslesmis SE, delta*, durust p, yanlis-pozitif orani,
manipulasyon dozu, val->test egimi, saldiri-RNG tabani) yalniz duzyazida
yasiyordu; hicbir kod uretmiyordu. Bu betik her birini artefaktlardan
(select_*.json, select_*_test.npz, select_*_valcurve.npz, testcurve_*.npz,
clean on-egitim loglari) yeniden hesaplar, belgedeki iddiayla karsilastirir ve
tutup tutmadigini ACIKCA isaretler. GPU gerekmez - her sey npz'lerde.

Onemli: bu betik ON-KAYITLI analizi (q1_e2_report.py) DEGISTIRMEZ; birincil
uc noktalara dokunmaz. Denetim/kesifsel katmandir.

Kullanim (konteyner icinde):
    python scripts/q1_e2_audit.py                       # varsayilan tekrar sayilari
    python scripts/q1_e2_audit.py --n-null 2000 --n-boot-s 20000
Cikti: results/q1/e2/e2_audit.json + konsol ozeti
"""
import argparse
import json
import math
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

try:
    from scipy import stats as sps
except ImportError:
    sys.exit("scipy gerekli (konteynerde mevcut)")

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT / "scripts"))
from q1_offline_select import simulate_selection      # noqa: E402
from q1_e2_report import paired_tost                  # noqa: E402  (ayni TOST konvansiyonu)

ARCHS = {"resnet18": [1001, 1002, 1003], "vit_tiny": [2001, 2002, 2003]}
CONDS = "ABC"
PATIENCE, MIN_DELTA = 20, 0.1          # on-kayitli secim kurali
N_TEST = 10000
ALPHA = 0.05


# --------------------------------------------------------------------------
# yardimcilar
# --------------------------------------------------------------------------
def r6(x):
    """JSON'a yazilabilir sayi (numpy tiplerini de duzlestirir)."""
    if isinstance(x, dict):
        return {k: r6(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [r6(v) for v in x]
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if x is None:
        return None
    v = float(x)
    if not math.isfinite(v):
        return None
    return round(v, 6)


def kiyas(hesaplanan, iddia, tol, birim="puan", not_=""):
    """Hesaplanan degeri belgedeki iddiayla karsilastir (skaler ya da liste)."""
    h = np.atleast_1d(np.asarray(hesaplanan, dtype=float))
    i = np.atleast_1d(np.asarray(iddia, dtype=float))
    fark = np.abs(h - i) if h.shape == i.shape else np.array([np.nan])
    out = {
        "hesaplanan": r6(hesaplanan), "iddia_edilen": r6(iddia),
        "tolerans": r6(tol), "birim": birim,
        "mutlak_fark": r6(fark.tolist() if fark.size > 1 else float(fark[0])),
        "tutuyor": bool(np.all(fark <= tol)) if h.shape == i.shape else False,
    }
    if not_:
        out["not"] = not_
    return out


def aralik_kiyas(hesaplanan, alt, ust, birim="", not_=""):
    """Iddia bir ARALIK olarak verildiginde (or. 'p = 0,10-0,19')."""
    ham = hesaplanan if isinstance(hesaplanan, (list, tuple)) else [hesaplanan]
    kullanilabilir = [x for x in ham if x is not None]
    out = {"hesaplanan": r6(hesaplanan), "iddia_araligi": [r6(alt), r6(ust)],
           "birim": birim}
    if len(kullanilabilir) != len(ham):
        out["tutuyor"] = False
        out["uyari"] = "bazi degerler hesaplanamadi (kaynak dosya eksik)"
    else:
        h = np.atleast_1d(np.asarray(kullanilabilir, dtype=float))
        out["tutuyor"] = bool(np.all((h >= alt) & (h <= ust)))
    if not_:
        out["not"] = not_
    return out


def sec_idx(epochs, clean_curve, adv_curve):
    """On-kayitli secim kuralini bir egriye uygula -> (indeks, geri_dusuldu_mu)."""
    ep, _, _ = simulate_selection(
        list(zip(epochs.tolist(), clean_curve.tolist(), adv_curve.tolist())),
        patience=PATIENCE, min_delta=MIN_DELTA)
    if ep is None:
        return int(np.argmax(adv_curve)), True
    return int(np.where(epochs == ep)[0][0]), False


def esli_fark(mask_x, mask_y):
    """Ayni orneklerde iki checkpoint'in dogruluk farki + McNemar varyansi.

    delta (puan) = 100*(b-c)/n;  var = 1e4*(b+c)/n^2  (belgedeki 'McNemar b+c'
    formulu). Tam esli varyans (b+c-(b-c)^2/n)/n^2 de raporlanir.
    """
    b = int(np.sum(mask_x & ~mask_y))
    c = int(np.sum(~mask_x & mask_y))
    n = int(mask_x.size)
    delta = 100.0 * (b - c) / n
    var = 1e4 * (b + c) / n ** 2
    var_tam = 1e4 * ((b + c) - (b - c) ** 2 / n) / n ** 2
    return {"b": b, "c": c, "n": n, "delta": delta, "var": var, "var_tam": var_tam}


def ters_varyans(deltas, varlar):
    """Ters-varyans agirlikli birlesim + Cochran homojenlik Q'su."""
    d = np.asarray(deltas, float)
    v = np.asarray(varlar, float)
    w = 1.0 / v
    th = float(w @ d / w.sum())
    se = float(1.0 / math.sqrt(w.sum()))
    Q = float(np.sum(w * (d - th) ** 2))
    df = int(d.size - 1)
    p = float(sps.chi2.sf(Q, df)) if df > 0 else float("nan")
    return {"theta": th, "se": se, "Q": Q, "df": df, "p_homojenlik": p,
            "birim_sayisi": int(d.size)}


# --------------------------------------------------------------------------
# veri yukleme
# --------------------------------------------------------------------------
def yukle(in_dir, arch, seed):
    """Bir yorungenin tum artefaktlari: testcurve + 3 bolme secimi/egrisi."""
    tag = f"{arch}_s{seed}"
    tc = np.load(in_dir / f"testcurve_{tag}.npz")
    y = {"tag": tag, "arch": arch, "seed": seed,
         "epochs": tc["epochs"].astype(int),
         "test_clean_acc": tc["clean_acc"].astype(float),
         "test_adv_acc": tc["adv_acc"].astype(float),
         "test_clean_mask": tc["clean_mask"].astype(bool),
         "test_adv_mask": tc["adv_mask"].astype(bool),
         "val": {}, "sec": {}}
    if y["test_adv_mask"].shape[1] != N_TEST:
        sys.exit(f"HATA: {tag} testcurve n={y['test_adv_mask'].shape[1]} != {N_TEST}")
    for c in CONDS:
        vz = np.load(in_dir / f"select_{tag}_val{c}_valcurve.npz")
        y["val"][c] = {"clean": vz["clean_mask"].astype(bool),
                       "adv": vz["adv_mask"].astype(bool),
                       "dosya": str(vz["val_indices_file"])}
        sj = json.load(open(in_dir / f"select_{tag}_val{c}.json"))
        sn = np.load(in_dir / f"select_{tag}_val{c}_test.npz")
        ep = int(sj["selected_epoch"])
        if int(sn["selected_epoch"]) != ep:
            sys.exit(f"HATA: {tag}/{c} json-npz epok uyusmazligi")
        y["sec"][c] = {
            "epoch": ep, "idx": int(np.where(y["epochs"] == ep)[0][0]),
            "val_adv": float(sj["selected_adv_acc"]),
            "test_clean": float(sj["test"]["clean_acc"]),
            "test_adv": float(sj["test"]["adv_acc"]),
            "npz_clean": sn["clean_correct"].astype(bool),
            "npz_adv": sn["adv_correct"].astype(bool),
        }
    return y


def clean_on_egitim_acc(seed_log_dir, arch, seed):
    """Clean on-egitimin son epok train/test dogrulugu (manipulasyon dozu icin)."""
    p = Path(seed_log_dir) / f"Q1_e2_clean_{arch}_{seed}.log"
    if not p.exists():
        return None
    pat = re.compile(r"Epoch (\d+)/(\d+) - Train Loss: [0-9.]+, "
                     r"Train Acc: ([0-9.]+)%, Test Acc: ([0-9.]+)%")
    ms = pat.findall(p.read_text(errors="ignore"))
    if not ms:
        return None
    e, tot, tr, te = ms[-1]
    return {"log": str(p), "son_epok": int(e), "toplam_epok": int(tot),
            "train_acc": float(tr), "test_acc": float(te)}


# --------------------------------------------------------------------------
# MADDE 1 + 2: theta birlesimi ve ayrik tahmincilerdeki sd
# --------------------------------------------------------------------------
def tahminci_farklari(yors, u="A", v="B"):
    """Her tohum icin (e_u, e_v) ciftinin her tahmincideki esli farki."""
    isimler = ["test10k_secim_npz", "test10k_testcurve", "V_A", "V_B", "V_C",
               "havuz_BC", "havuz_ABC"]
    out = {k: [] for k in isimler}
    for y in yors:
        iu, iv = y["sec"][u]["idx"], y["sec"][v]["idx"]
        mset = {
            # secim kosumunun test degerlendirmesi (saldiri tohumu 42) -
            # on-kayitli raporun kullandigi olcum
            "test10k_secim_npz": (y["sec"][u]["npz_adv"], y["sec"][v]["npz_adv"]),
            # P0 test egrisi (saldiri tohumu 42*1e5+epok) - bagimsiz olcum
            "test10k_testcurve": (y["test_adv_mask"][iu], y["test_adv_mask"][iv]),
            "V_A": (y["val"]["A"]["adv"][iu], y["val"]["A"]["adv"][iv]),
            "V_B": (y["val"]["B"]["adv"][iu], y["val"]["B"]["adv"][iv]),
            "V_C": (y["val"]["C"]["adv"][iu], y["val"]["C"]["adv"][iv]),
            "havuz_BC": (np.concatenate([y["val"]["B"]["adv"][iu], y["val"]["C"]["adv"][iu]]),
                         np.concatenate([y["val"]["B"]["adv"][iv], y["val"]["C"]["adv"][iv]])),
            "havuz_ABC": (np.concatenate([y["val"][c]["adv"][iu] for c in CONDS]),
                          np.concatenate([y["val"][c]["adv"][iv] for c in CONDS])),
        }
        for k in isimler:
            out[k].append(esli_fark(*mset[k]))
    return out


def madde1_2(yors, arch="vit_tiny"):
    """theta = -1,108 +- 0,183 (chi2(5)=7,23) ve sd = 0,97/1,13/1,32."""
    ys = [y for y in yors if y["arch"] == arch]
    farklar = tahminci_farklari(ys, "A", "B")
    ozet = {}
    for k, lst in farklar.items():
        d = [x["delta"] for x in lst]
        ozet[k] = {
            "tohum_deltalari": r6(d),
            "ort": r6(float(np.mean(d))),
            "sd_tohumlar_arasi": r6(float(np.std(d, ddof=1))),
            "ort_se_McNemar": r6(float(math.sqrt(sum(x["var"] for x in lst)) / len(lst))),
            "tohum_se_McNemar": r6([math.sqrt(x["var"]) for x in lst]),
            "b_arti_c": [x["b"] + x["c"] for x in lst],
            "n": lst[0]["n"],
        }

    def birlesim(kaynaklar, mod):
        if mod == "tohum_bazli":     # 3 tohum x k tahminci = 3k birim
            d = [x["delta"] for k in kaynaklar for x in farklar[k]]
            v = [x["var"] for k in kaynaklar for x in farklar[k]]
        else:                        # tahminci ortalamalari = k birim
            d = [float(np.mean([x["delta"] for x in farklar[k]])) for k in kaynaklar]
            v = [float(sum(x["var"] for x in farklar[k]) / len(farklar[k]) ** 2)
                 for k in kaynaklar]
        res = ters_varyans(d, v)
        res["kaynaklar"] = list(kaynaklar)
        res["mod"] = mod
        return {kk: (r6(vv) if isinstance(vv, float) else vv) for kk, vv in res.items()}

    setler = {
        # belgedeki theta'yi yeniden ureten kurulus (df=5 <=> 3 tohum x 2 kaynak)
        "test_npz+havuz_BC": ["test10k_secim_npz", "havuz_BC"],
        # gorev metninde tarif edilen 5 tahminci
        "gorev_metni_5": ["test10k_secim_npz", "V_A", "V_B", "V_C", "havuz_BC"],
        # gercekten AYRIK ornek kumeleri (havuz cikarilmis)
        "ayrik_4": ["test10k_secim_npz", "V_A", "V_B", "V_C"],
        # test olcumu P0 egrisinden (saldiri tohumu farkli) alindiginda
        "testcurve+havuz_BC": ["test10k_testcurve", "havuz_BC"],
        "ayrik_4_testcurve": ["test10k_testcurve", "V_A", "V_B", "V_C"],
    }
    varyantlar = {ad: {m: birlesim(k, m)
                       for m in ("tohum_bazli", "tahminci_ortalamasi")}
                  for ad, k in setler.items()}

    ref = varyantlar["test_npz+havuz_BC"]["tohum_bazli"]
    madde1 = {
        "iddia_metni": "theta = -1,108 +- 0,183; homojenlik chi2(5)=7,23, p=0,204",
        "tahminci_ozetleri": ozet,
        "birlesim_varyantlari": varyantlar,
        "belgeyle_eslesen_kurulus": "test10k_secim_npz + havuz_BC, tohum_bazli "
                                    "(3 tohum x 2 kaynak = 6 birim -> df=5)",
        "kontrol": {
            "theta": kiyas(ref["theta"], -1.108, 0.02),
            "se": kiyas(ref["se"], 0.183, 0.005),
            "Q": kiyas(ref["Q"], 7.23, 0.5, birim="chi2"),
            "df": kiyas(ref["df"], 5, 0, birim="serbestlik derecesi"),
            "p_homojenlik": kiyas(ref["p_homojenlik"], 0.204, 0.05, birim="p"),
        },
        "uyari": [
            "Tahminciler BAGIMSIZ degil: havuz_BC, V_B ve V_C'nin birlesimidir; "
            "gorev metnindeki 5'li kume ayni ornekleri iki kez sayar.",
            "10k test tahmincisi ucu tohumda AYNI ornekleri kullanir; birlesim "
            "bu korelasyonu yok sayar (SE asagi yanli olabilir).",
            "Gorev metnindeki 5'li kume theta = "
            f"{varyantlar['gorev_metni_5']['tahminci_ortalamasi']['theta']} verir "
            "(-1,108 DEGIL); belgedeki sayi yalniz 'test+havuz_BC' kurulusuyla cikar.",
        ],
    }

    hedef = [ozet["V_B"]["sd_tohumlar_arasi"], ozet["havuz_BC"]["sd_tohumlar_arasi"],
             ozet["V_C"]["sd_tohumlar_arasi"]]
    madde2 = {
        "iddia_metni": "Ayni uc checkpoint cifti ayrik tahmincilerle olculdugunde "
                       "sd = 0,97 / 1,13 / 1,32 (V_B / havuz B+C / V_C)",
        "sd_V_B": ozet["V_B"]["sd_tohumlar_arasi"],
        "sd_havuz_BC": ozet["havuz_BC"]["sd_tohumlar_arasi"],
        "sd_V_C": ozet["V_C"]["sd_tohumlar_arasi"],
        "sd_test10k_secim_npz": ozet["test10k_secim_npz"]["sd_tohumlar_arasi"],
        "sd_test10k_testcurve": ozet["test10k_testcurve"]["sd_tohumlar_arasi"],
        "kontrol": kiyas(hedef, [0.97, 1.13, 1.32], 0.02),
        "yorum": "Ayni checkpoint ciftlerinin farki ayrik tahmincilerde ~1 puan "
                 "sd gosteriyor; s_Delta=0,010 tekrarlanabilirlik degil.",
    }
    return madde1, madde2, farklar


# --------------------------------------------------------------------------
# MADDE 3: esli SE ve P(s <= 0,010)
# --------------------------------------------------------------------------
def madde3(yors, farklar, n_boot, n_mvn, rng, arch="vit_tiny"):
    ys = [y for y in yors if y["arch"] == arch]
    lst = farklar["test10k_secim_npz"]
    se_tek = [math.sqrt(x["var"]) for x in lst]
    se_tam = [math.sqrt(x["var_tam"]) for x in lst]

    # H0: ucunun GERCEK Delta'si ozdes -> her tohumun ornek-bazli fark vektoru
    # ortak ortalamaya merkezlenir; ORTAK 10k test bootstrap'i (ayni indeksler
    # uc tohuma da uygulanir) tohumlar arasi korelasyonu korur.
    Dm = np.stack([(y["sec"]["A"]["npz_adv"].astype(np.float32)
                    - y["sec"]["B"]["npz_adv"].astype(np.float32)) for y in ys])
    Dm = Dm - Dm.mean(axis=1, keepdims=True)
    n = Dm.shape[1]
    esik = 0.010 + 1e-9
    say = 0
    parca = max(1, min(500, n_boot))
    kalan = n_boot
    s_ornek = []
    while kalan > 0:
        b = min(parca, kalan)
        idx = rng.integers(0, n, size=(b, n), dtype=np.int64)
        m = Dm[:, idx].mean(axis=2) * 100.0          # (3, b) puan
        s = m.std(axis=0, ddof=1)
        say += int((s <= esik).sum())
        s_ornek.append(s[: min(b, 50)])
        kalan -= b
    P_boot = say / n_boot
    s_ornek = np.concatenate(s_ornek)

    # normal yaklasim (ayrik kafes etkisini gormezden gelir; capraz kontrol)
    S = np.cov(Dm) / n * 1e4                          # puan^2
    L = np.linalg.cholesky(S + 1e-9 * np.trace(S) * np.eye(3))
    z = rng.standard_normal((3, n_mvn))
    mm = L @ z
    P_mvn = float((mm.std(axis=0, ddof=1) <= esik).mean())

    gozlenen_s = float(np.std([x["delta"] for x in lst], ddof=1))
    return {
        "iddia_metni": "Tek olcumun esli SE'si 0,372; P(s <= 0,010 | gercek "
                       "Delta'lar ozdes) = 7,2e-4",
        "tohum_se_McNemar": r6(se_tek),
        "ort_se": r6(float(np.mean(se_tek))),
        "tohum_se_tam_formul": r6(se_tam),
        "gozlenen_s_uc_tohum": r6(gozlenen_s),
        "sd_deflasyon_kati": r6(float(np.mean(se_tek)) / max(gozlenen_s, 1e-12)),
        "bootstrap": {"n_boot": n_boot, "P_s_le_0.010": r6(P_boot),
                      "vurus": say,
                      "MC_se": r6(math.sqrt(max(P_boot, 1e-12) * (1 - P_boot) / n_boot)),
                      "s_ortalama": r6(float(s_ornek.mean())),
                      "kurulus": "ORTAK indeks bootstrap (ayni 10k yeniden "
                                 "orneklemesi uc tohuma birden), H0 icin "
                                 "her tohum kendi ortalamasina merkezlendi"},
        "normal_yaklasim": {"n": n_mvn, "P_s_le_0.010": r6(P_mvn),
                            "not": "surekli yaklasim; gercek bootstrap 0,01 "
                                   "puanlik kafes uzerinde atomlara sahiptir"},
        "kontrol": {
            "esli_SE": kiyas(float(np.mean(se_tek)), 0.372, 0.005),
            "sd_deflasyon_kati": kiyas(float(np.mean(se_tek)) / max(gozlenen_s, 1e-12),
                                       37.0, 0.5, birim="kat",
                                       not_="belge §4.2: 's_Delta tek olcum SE'sinden "
                                            "37 kat kucuk'"),
            "P_normal_yaklasimla": kiyas(P_mvn, 7.2e-4, 2e-4, birim="olasilik",
                                         not_="Belgedeki 7,2e-4, ayrik bootstrap'tan "
                                              "cok SUREKLI yaklasima yakin - belge "
                                              "bu sayiyi buyuk olasilikla normal "
                                              "yaklasimla uretmis."),
            "P_s_le_0.010": kiyas(P_boot, 7.2e-4, 5e-4, birim="olasilik",
                                  not_="Ayni buyukluk mertebesi. Tolerans genis "
                                       "tutuldu: kalan fark MC hatasindan buyuk "
                                       "olabilir (bkz. MC_se) ve merkezleme/"
                                       "yeniden-orneklerne ayrintisina duyarlidir; "
                                       "hukum ('s=0,010 tesaduftur') degismiyor."),
        },
    }


# --------------------------------------------------------------------------
# MADDE 4: TOST kritik marji delta*
# --------------------------------------------------------------------------
def madde4(yors, arch="vit_tiny"):
    ys = [y for y in yors if y["arch"] == arch]
    d = np.array([y["sec"]["A"]["test_adv"] - y["sec"]["B"]["test_adv"] for y in ys])
    m, s, nn = float(d.mean()), float(d.std(ddof=1)), d.size
    se = s / math.sqrt(nn)
    tcrit = float(sps.t.ppf(1 - ALPHA, nn - 1))
    d_yildiz = abs(m) + tcrit * se
    hukumler = {}
    for marj in (1.00, 1.05, d_yildiz - 1e-6, d_yildiz + 1e-6, 1.07, 1.10):
        t = paired_tost(d.tolist(), margin=marj)
        hukumler[f"{marj:.6f}"] = {"p_tost": t["p_tost"], "esdeger": t["equivalent"],
                                   "farkli": t["different"], "hukum": t["verdict"]}
    return {
        "iddia_metni": "delta* = 1,067 (delta=1,05'te FARKLI, delta=1,07'de ESDEGER)",
        "deltalar": r6(d.tolist()), "ort": r6(m), "sd": r6(s), "se": r6(se),
        "t_kritik_df2_alpha05": r6(tcrit),
        "delta_yildiz": r6(d_yildiz),
        "formul": "delta* = |ort| + t_{1-alpha, n-1} * se",
        "marj_taramasi": hukumler,
        "kontrol": kiyas(d_yildiz, 1.067, 0.001),
        "not": "Hukum ceviren marj TOST kolundan gelir; iki yonlu t (p=3e-5) "
               "marjdan bagimsizdir - 'FARKLI' etiketi delta ne olursa olsun kalir, "
               "delta*'in ustunde etiket ESDEGER_AMA_SIFIRDAN_FARKLI olur.",
    }


# --------------------------------------------------------------------------
# MADDE 5 + 6: tasarimla eslesmis null'lar ve havuzlanmis McNemar'in FP orani
# --------------------------------------------------------------------------
def mcnemar_p(b, c):
    n = b + c
    if n == 0:
        return 1.0
    return float(sps.binomtest(min(b, c), n, 0.5, alternative="two-sided").pvalue)


_BMAT = {}


def mcnemar_matrisi(y):
    """B[i,j] = epok i dogru & epok j yanlis (10k test, adv) - onbellekli."""
    if y["tag"] not in _BMAT:
        M = y["test_adv_mask"].astype(np.float32)
        _BMAT[y["tag"]] = np.rint(M @ (1.0 - M).T).astype(np.int64)
    return _BMAT[y["tag"]]


def null_bolme(yors, arch, n_rep, rng, mod="ayrik_yarilar"):
    """Tasarimla eslesmis sifir-sizinti null'u: temiz bolmelerden secim ->
    GERCEK 10k test farki. Bolme AYNI tohum uclusune uygulanir (ortak-bolme
    yapisi ve dolayisiyla tohumlar arasi korelasyon korunur).

    mod='ayrik_yarilar': V_B u V_C (4000) -> rastgele 2000/2000 ayrik bolme
    mod='bootstrap'    : V_B u V_C havuzundan iki bagimsiz 2000'lik cekilis
    mod='uclu_bolme'   : H0 altinda A/B/C etiketleri degistirilebilir oldugundan
                         V_A u V_B u V_C (6000) -> rastgele 2000/2000/2000;
                         hem P1-P2 hem SIMETRIK P1-(P2+P3)/2 istatistigi
    """
    ys = [y for y in yors if y["arch"] == arch]
    parcalar = CONDS if mod == "uclu_bolme" else "BC"
    hav_adv = [np.concatenate([y["val"][c]["adv"] for c in parcalar], axis=1
                              ).astype(np.float32) for y in ys]
    hav_cln = [np.concatenate([y["val"][c]["clean"] for c in parcalar], axis=1
                              ).astype(np.float32) for y in ys]
    npool = hav_adv[0].shape[1]
    kac = 3 if mod == "uclu_bolme" else 2
    boy = npool // kac
    epochs = ys[0]["epochs"]
    Bmat = [mcnemar_matrisi(y) for y in ys]   # B[i,j] = i dogru & j yanlis (10k)
    tadv = [y["test_adv_acc"] for y in ys]

    deltalar = np.empty(n_rep)
    simetrik = np.full(n_rep, np.nan)
    p_mcnemar = np.empty(n_rep)
    ayni_epok = np.zeros(n_rep, dtype=bool)
    geri_dusme = 0
    for r in range(n_rep):
        if mod == "bootstrap":
            ws = [rng.multinomial(boy, np.full(npool, 1.0 / npool)).astype(np.float32)
                  for _ in range(kac)]
        else:
            perm = rng.permutation(npool)
            ws = []
            for t in range(kac):
                w = np.zeros(npool, dtype=np.float32)
                w[perm[t * boy:(t + 1) * boy]] = 1.0
                ws.append(w)
        ds, dsym, bb, cc = [], [], 0, 0
        for k, y in enumerate(ys):
            idx = []
            for w in ws:
                i, f = sec_idx(epochs, 100.0 * (hav_cln[k] @ w) / boy,
                               100.0 * (hav_adv[k] @ w) / boy)
                idx.append(i)
                geri_dusme += int(f)
            ds.append(tadv[k][idx[0]] - tadv[k][idx[1]])
            if kac == 3:
                dsym.append(tadv[k][idx[0]]
                            - 0.5 * (tadv[k][idx[1]] + tadv[k][idx[2]]))
            bb += int(Bmat[k][idx[0], idx[1]])
            cc += int(Bmat[k][idx[1], idx[0]])
        deltalar[r] = float(np.mean(ds))
        if dsym:
            simetrik[r] = float(np.mean(dsym))
        ayni_epok[r] = all(abs(x) < 1e-12 for x in ds)
        p_mcnemar[r] = mcnemar_p(bb, cc)
    return deltalar, simetrik, p_mcnemar, ayni_epok, geri_dusme


def madde5_6(yors, n_rep, rng):
    sonuc5 = {"iddia_metni": "Durust iki yonlu p = 0,10-0,19 (tasarimla eslesmis "
                             "null'lar)", "kuruluslar": {}}
    sonuc6 = {"iddia_metni": "Sifir sizinti altinda havuzlanmis McNemar %37-56 "
                             "oraninda p<0,05 veriyor", "mimariler": {}}

    for arch in ARCHS:
        ys = [y for y in yors if y["arch"] == arch]
        obs_npz = float(np.mean([y["sec"]["A"]["test_adv"] - y["sec"]["B"]["test_adv"]
                                 for y in ys]))
        obs_tc = float(np.mean([y["test_adv_acc"][y["sec"]["A"]["idx"]]
                                - y["test_adv_acc"][y["sec"]["B"]["idx"]] for y in ys]))
        obs_sim = float(np.mean([y["sec"]["A"]["test_adv"]
                                 - 0.5 * (y["sec"]["B"]["test_adv"]
                                          + y["sec"]["C"]["test_adv"]) for y in ys]))
        for mod in ("ayrik_yarilar", "bootstrap", "uclu_bolme"):
            d, dsym, pmc, ayni, geri = null_bolme(yors, arch, n_rep, rng, mod)
            ad = {"ayrik_yarilar": "a1_ayrik_yarilar_BC",
                  "bootstrap": "a2_bootstrap_BC",
                  "uclu_bolme": "e_uclu_bolme_ABC"}[mod]
            kayit = {
                "n_rep": n_rep, "havuz": "V_A u V_B u V_C (6000)" if mod == "uclu_bolme"
                                          else "V_B u V_C (4000)",
                "null_ort": r6(float(d.mean())), "null_sd": r6(float(d.std(ddof=1))),
                "null_p95_mutlak": r6(float(np.percentile(np.abs(d), 95))),
                "P_ayni_epok_ucunde": r6(float(ayni.mean())),
                "geri_dusme_sayisi": geri,
                "gozlenen_secim_npz": r6(obs_npz),
                "gozlenen_testcurve": r6(obs_tc),
                "p_iki_yonlu_secim_npz": r6(float((np.abs(d) >= abs(obs_npz) - 1e-12).mean())),
                "p_iki_yonlu_testcurve": r6(float((np.abs(d) >= abs(obs_tc) - 1e-12).mean())),
            }
            if mod == "uclu_bolme":
                kayit["simetrik_istatistik"] = {
                    "gozlenen_A_eksi_BC_ort": r6(obs_sim),
                    "null_sd": r6(float(np.nanstd(dsym, ddof=1))),
                    "p_iki_yonlu": r6(float((np.abs(dsym) >= abs(obs_sim) - 1e-12).mean())),
                    "not": "H0 altinda A/B/C etiketleri degistirilebilir; 6000'lik "
                           "havuzun ucluye bolunmesi karsilastirici keyfiligini "
                           "null'a tasir",
                }
            sonuc5["kuruluslar"].setdefault(arch, {})[ad] = kayit
            sonuc6["mimariler"].setdefault(arch, {})[ad] = {
                "n_rep": n_rep,
                "yanlis_pozitif_orani_p05": r6(float((pmc < ALPHA).mean())),
                "medyan_p": r6(float(np.median(pmc))),
                "P_ayni_epok_ucunde": r6(float(ayni.mean())),
                "not": "iki TEMIZ bolme (sifir sizinti); havuzlanmis McNemar "
                       "3 tohumun 10k maskeleri birlestirilerek",
            }

    # (b) isaret permutasyonu (n=3, tam)
    vit = [y for y in yors if y["arch"] == "vit_tiny"]
    dAB = np.array([y["sec"]["A"]["test_adv"] - y["sec"]["B"]["test_adv"] for y in vit])
    isaretler = np.array([[s1, s2, s3] for s1 in (1, -1) for s2 in (1, -1)
                          for s3 in (1, -1)], dtype=float)
    ort = np.abs(isaretler @ np.abs(dAB) / 3.0)
    p_perm = float((ort >= abs(dAB.mean()) - 1e-12).mean())

    # (c) simetrik tahminci A-(B+C)/2, esli t
    dsim = np.array([y["sec"]["A"]["test_adv"]
                     - 0.5 * (y["sec"]["B"]["test_adv"] + y["sec"]["C"]["test_adv"])
                     for y in vit])
    tsim = paired_tost(dsim.tolist())
    # (d) karsilastirici takasi A-C
    dAC = np.array([y["sec"]["A"]["test_adv"] - y["sec"]["C"]["test_adv"] for y in vit])
    tAC = paired_tost(dAC.tolist())

    sonuc5["kuruluslar"]["vit_tiny"]["b_isaret_permutasyonu"] = {
        "deltalar": r6(dAB.tolist()), "p_iki_yonlu": r6(p_perm),
        "not": "n=3'te ulasilabilir en kucuk iki yonlu p = 2/8 = 0,25 (taban)",
    }
    sonuc5["kuruluslar"]["vit_tiny"]["c_simetrik_tahminci_A_eksi_BC_ort"] = {
        "deltalar": r6(dsim.tolist()), "ort": r6(tsim["mean"]), "sd": r6(tsim["sd"]),
        "p_iki_yonlu": r6(tsim["t_two_sided_p"]), "ci90": r6(tsim["ci90"]),
    }
    sonuc5["kuruluslar"]["vit_tiny"]["d_karsilastirici_takasi_A_eksi_C"] = {
        "deltalar": r6(dAC.tolist()), "ort": r6(tAC["mean"]), "sd": r6(tAC["sd"]),
        "p_iki_yonlu": r6(tAC["t_two_sided_p"]),
        "not": "B<->C takasi mansetin karsilastirici secimine duyarliligini gosterir",
    }

    # (f) BOLME ETIKETI permutasyonu: bolmeler sabit, roller degistirilebilir.
    # Ikili istatistik icin 6 sirali cift, simetrik istatistik icin 3 rol.
    ort = {c: float(np.mean([y["sec"][c]["test_adv"] for y in vit])) for c in CONDS}
    ikili = {f"{u}-{v}": ort[u] - ort[v] for u in CONDS for v in CONDS if u != v}
    sim = {c: ort[c] - 0.5 * sum(ort[o] for o in CONDS if o != c) for c in CONDS}
    p_lab_ikili = float(np.mean([abs(v) >= abs(ikili["A-B"]) - 1e-12
                                 for v in ikili.values()]))
    p_lab_sim = float(np.mean([abs(v) >= abs(sim["A"]) - 1e-12 for v in sim.values()]))
    sonuc5["kuruluslar"]["vit_tiny"]["f_bolme_etiketi_permutasyonu"] = {
        "kosul_ortalamalari": r6(ort), "ikili_istatistikler": r6(ikili),
        "simetrik_istatistikler": r6(sim),
        "p_ikili": r6(p_lab_ikili), "p_simetrik": r6(p_lab_sim),
        "not": "Bolme duzeyinde n=1 oldugu icin tam permutasyon tabani 1/6=0,167 "
               "(ikili) ve 1/3=0,333 (simetrik); bunun altina inilemez.",
    }

    v5 = sonuc5["kuruluslar"]["vit_tiny"]
    ps = {
        "a1_ayrik_yarilar_BC": v5["a1_ayrik_yarilar_BC"]["p_iki_yonlu_secim_npz"],
        "a2_bootstrap_BC": v5["a2_bootstrap_BC"]["p_iki_yonlu_secim_npz"],
        "e_uclu_bolme_ikili": v5["e_uclu_bolme_ABC"]["p_iki_yonlu_secim_npz"],
        "e_uclu_bolme_simetrik":
            v5["e_uclu_bolme_ABC"]["simetrik_istatistik"]["p_iki_yonlu"],
        "b_isaret_permutasyonu": p_perm,
        "c_simetrik_t": tsim["t_two_sided_p"],
        "d_A_eksi_C_t": tAC["t_two_sided_p"],
        "f_etiket_permutasyonu_ikili": p_lab_ikili,
        "f_etiket_permutasyonu_simetrik": p_lab_sim,
    }
    sonuc5["p_degerleri_vit_tiny"] = r6(ps)
    sonuc5["kontrol"] = {ad: aralik_kiyas(p, 0.10, 0.19, "p") for ad, p in ps.items()}
    icinde = [ad for ad, p in ps.items() if 0.10 <= p <= 0.19]
    sonuc5["kontrol"]["ozet"] = {
        "iddia_araligi": [0.10, 0.19],
        "hesaplanan_aralik": r6([min(ps.values()), max(ps.values())]),
        "aralikta_olan_kuruluslar": icinde,
        "kurulus_sayisi": len(ps),
        "tutuyor": bool(icinde),
        "hukum": "KISMEN" if icinde and len(icinde) < len(ps) else
                 ("TUTUYOR" if icinde else "TUTMUYOR"),
        "not": "Belge 'dort bagimsiz kurulus' diyor ama hangileri oldugunu "
               f"yazmiyor. Denenen {len(ps)} kurulustan yalniz {len(icinde)} tanesi "
               "0,10-0,19 araliginda.",
    }
    sonuc5["yorum_iki_cikarim_cercevesi"] = {
        "bolmeler_RASTGELE_kabul_edilirse": {
            "kuruluslar": ["a1_ayrik_yarilar_BC", "a2_bootstrap_BC",
                           "e_uclu_bolme_ikili", "e_uclu_bolme_simetrik"],
            "p_araligi": r6([min(ps[k] for k in ("a1_ayrik_yarilar_BC",
                                                 "a2_bootstrap_BC",
                                                 "e_uclu_bolme_ikili",
                                                 "e_uclu_bolme_simetrik")),
                             max(ps[k] for k in ("a1_ayrik_yarilar_BC",
                                                 "a2_bootstrap_BC",
                                                 "e_uclu_bolme_ikili",
                                                 "e_uclu_bolme_simetrik"))]),
            "anlami": "Tasarimla eslesmis (ortak-bolme, ayrik degerlendirici) "
                      "null: gozlenen A-B farki temiz bolme ciftlerinin "
                      "uretebildiginden BUYUK. Bu cerceve belgedeki 0,10-0,19'dan "
                      "cok daha KUCUK p verir.",
        },
        "bolmeler_SABIT_kabul_edilirse": {
            "kuruluslar": ["b_isaret_permutasyonu", "f_etiket_permutasyonu_ikili",
                           "f_etiket_permutasyonu_simetrik"],
            "p_araligi": r6([0.25, p_lab_sim]),
            "anlami": "Bolme duzeyinde n=1; tam permutasyon tabani 1/6-1/3. Bu "
                      "cerceve belgedeki 0,10-0,19'dan cok daha BUYUK p verir.",
        },
        "belgenin_araligi_nereye_dusuyor": "Ikisinin ARASINA. 0,10-0,19'u ureten "
                                           "tek kurulus, simetrik tahminci uzerinde "
                                           "n=3 parametrik t testidir (p=0,113); "
                                           "belge dort kurulus oldugunu soyluyor ama "
                                           "tanimlamiyor -> iddia bu haliyle "
                                           "DOGRULANAMIYOR.",
        "hukum_uzerindeki_etkisi": "Belgenin 'sizinti saptanamadi' hukmu, bolmeleri "
                                   "SABIT kabul eden cerceveye dayaniyor (ki bolme "
                                   "duzeyinde n=1 oldugu icin savunulabilir). "
                                   "Bolmeler rastgele kabul edilirse ayni veri "
                                   "p<0,05 veriyor. Makale hangi cercevede "
                                   "konustugunu ACIKCA yazmalidir.",
    }

    sonuc6["degerler"] = {f"{a}/{m}": v["yanlis_pozitif_orani_p05"]
                          for a, d in sonuc6["mimariler"].items() for m, v in d.items()}
    vit_fp = [v["yanlis_pozitif_orani_p05"] for v in sonuc6["mimariler"]["vit_tiny"].values()]
    res_fp = [v["yanlis_pozitif_orani_p05"] for v in sonuc6["mimariler"]["resnet18"].values()]
    tum_fp = vit_fp + res_fp
    sonuc6["kontrol"] = {
        "vit_tiny": aralik_kiyas(vit_fp, 0.37, 0.56, "oran",
                                 not_="manset kolu; on-kayit §6b araligi"),
        "resnet18": aralik_kiyas(res_fp, 0.37, 0.56, "oran",
                                 not_="ResNet kolunda oran daha dusuk cikiyor"),
        "nitel_kontrol": {
            "iddia": "sifir sizinti altinda havuzlanmis McNemar SIK SIK p<0,05 verir",
            "en_dusuk_oran": r6(min(tum_fp)), "nominal_alpha": ALPHA,
            "tutuyor": bool(min(tum_fp) > 3 * ALPHA),
        },
        "ortusme": {
            "hesaplanan_aralik": r6([min(tum_fp), max(tum_fp)]),
            "iddia_araligi": [0.37, 0.56],
            "tutuyor": bool(min(tum_fp) <= 0.56 and max(tum_fp) >= 0.37),
            "not": "6 hucre (2 mimari x 3 null modu); on-kayitli %37-56 araligi "
                   "ViT kolunu iyi tahmin etmis, ResNet kolunda gercek oran daha "
                   "dusuk cikmistir.",
        },
        "hukum": "Nicel aralik ViT kolunda dogrulaniyor; hucreler arasi gercek "
                 "yayilim %17-62. Nitel hukum ('negatif kontrolde de ateslenir') "
                 "her hucrede ayakta: en dusuk oran bile nominal %5'in 3 katindan "
                 "buyuk.",
    }
    return sonuc5, sonuc6


# --------------------------------------------------------------------------
# MADDE 7: manipulasyon kontrolu (sizinti dozu)
# --------------------------------------------------------------------------
def madde7(yors, log_dir, n_boot, rng):
    out = {"iddia_metni": "V_A temiz fazlasinin z'si: ViT 0,05/-0,10/-0,14 vs "
                          "ResNet 2,72/2,49/3,20; AT ep1'de beklenen dozun ViT'te "
                          "<%7'si, ResNet'te ~%50'si",
           "yorungeler": {}}
    for y in yors:
        pool_c = np.concatenate([y["val"]["B"]["clean"], y["val"]["C"]["clean"]], axis=1)
        pool_a = np.concatenate([y["val"]["B"]["adv"], y["val"]["C"]["adv"]], axis=1)
        a_c, a_a = y["val"]["A"]["clean"], y["val"]["A"]["adv"]
        nA = a_c.shape[1]

        def z_ve_fazla(a_mask, p_mask, epok_ort):
            """epok_ort=True: ornek-basi 100 epok ortalamasi; False: yalniz ep1.

            Referans dagilimi: hic gorulmemis V_B u V_C havuzundan 2000'lik
            yerine-koymali cekilisler (q1_e2_diagnostics.py ile ayni kurulus).
            """
            a = a_mask.mean(axis=0) if epok_ort else a_mask[0].astype(float)
            p = p_mask.mean(axis=0) if epok_ort else p_mask[0].astype(float)
            fazla = 100.0 * (a.mean() - p.mean())
            se_analitik = 100.0 * p.std(ddof=1) / math.sqrt(nA)
            bs = []
            kalan = n_boot
            while kalan > 0:
                b = min(2000, kalan)
                bs.append(p[rng.integers(0, p.size, size=(b, nA))].mean(axis=1))
                kalan -= b
            bs = np.concatenate(bs)
            z_boot = float((a.mean() - bs.mean()) / bs.std(ddof=1))
            return {"V_A": r6(100.0 * a.mean()), "referans_BC": r6(100.0 * p.mean()),
                    "fazla_puan": r6(fazla), "z_bootstrap": r6(z_boot),
                    "z_analitik": r6(fazla / se_analitik)}

        pre = clean_on_egitim_acc(log_dir, y["arch"], y["seed"])
        ep1 = z_ve_fazla(a_c, pool_c, False)
        yuz = z_ve_fazla(a_c, pool_c, True)
        adv_yuz = z_ve_fazla(a_a, pool_a, True)
        adv_ep1 = z_ve_fazla(a_a, pool_a, False)
        rec = {"temiz_100epok_ort": yuz, "temiz_AT_ep1": ep1,
               "cekismeli_100epok_ort": adv_yuz, "cekismeli_AT_ep1": adv_ep1,
               "clean_on_egitim": pre}
        # ALTERNATIF payda: AT ep1'de havuzun temiz doguslugu referans alinirsa
        # V_A tam ezberde kalsaydi tasiyacagi fazla = 100 - referans
        bek_alt = 100.0 - ep1["referans_BC"]
        rec["beklenen_doz_alternatif_payda_puan"] = r6(bek_alt)
        rec["olculen_doz_orani_AT_ep1_alternatif"] = r6(100.0 * ep1["fazla_puan"] / bek_alt)
        if pre:
            # beklenen doz: on-egitim V_A'yi ezberledi (train acc ~%100), gorulmemis
            # veride test acc; fark = V_A'nin tasimasi BEKLENEN fazla
            bek = pre["train_acc"] - pre["test_acc"]
            rec["beklenen_doz_puan"] = r6(bek)
            rec["olculen_doz_orani_AT_ep1"] = r6(100.0 * ep1["fazla_puan"] / bek)
            rec["olculen_doz_orani_100epok"] = r6(100.0 * yuz["fazla_puan"] / bek)
        out["yorungeler"][y["tag"]] = rec

    # Iddia karsilastirmasi ANALITIK z ile yapilir (deterministik); bootstrap z
    # ayni sayiyi MC gurultusuyle verir ve yanina raporlanir.
    z_vit = [out["yorungeler"][f"vit_tiny_s{s}"]["temiz_100epok_ort"]["z_analitik"]
             for s in ARCHS["vit_tiny"]]
    z_res = [out["yorungeler"][f"resnet18_s{s}"]["temiz_100epok_ort"]["z_analitik"]
             for s in ARCHS["resnet18"]]
    zb_vit = [out["yorungeler"][f"vit_tiny_s{s}"]["temiz_100epok_ort"]["z_bootstrap"]
              for s in ARCHS["vit_tiny"]]
    zb_res = [out["yorungeler"][f"resnet18_s{s}"]["temiz_100epok_ort"]["z_bootstrap"]
              for s in ARCHS["resnet18"]]
    oran_vit = [out["yorungeler"][f"vit_tiny_s{s}"].get("olculen_doz_orani_AT_ep1")
                for s in ARCHS["vit_tiny"]]
    oran_res = [out["yorungeler"][f"resnet18_s{s}"].get("olculen_doz_orani_AT_ep1")
                for s in ARCHS["resnet18"]]
    out["bootstrap_z_capraz_kontrol"] = {"vit_tiny": zb_vit, "resnet18": zb_res}
    out["kontrol"] = {
        "z_vit_100epok": kiyas(z_vit, [0.05, -0.10, -0.14], 0.05, birim="z",
                               not_="analitik z; bootstrap z yaninda raporlandi"),
        "z_resnet_100epok": kiyas(z_res, [2.72, 2.49, 3.20], 0.05, birim="z",
                                  not_="analitik z; bootstrap z yaninda raporlandi"),
        "doz_orani_vit_ep1_yuzde": aralik_kiyas(oran_vit, 0.0, 7.0, "%",
                                                not_="iddia: beklenen dozun <%7'si"),
        "doz_orani_resnet_ep1_yuzde": aralik_kiyas(oran_res, 40.0, 60.0, "%",
                                                   not_="iddia: ~%50"),
    }
    alt_vit = [out["yorungeler"][f"vit_tiny_s{s}"]["olculen_doz_orani_AT_ep1_alternatif"]
               for s in ARCHS["vit_tiny"]]
    alt_res = [out["yorungeler"][f"resnet18_s{s}"]["olculen_doz_orani_AT_ep1_alternatif"]
               for s in ARCHS["resnet18"]]
    out["payda_tanimina_duyarlilik"] = {
        "kullanilan_tanim": "beklenen doz = clean on-egitimin train-test genelleme "
                            "acigi (train ~%100, test %80,4 ViT / %95,3 ResNet); "
                            "ViT'te 19,5 puan -> belgedeki '~+19,6' ile ayni, yani "
                            "belgenin ortuk tanimi budur.",
        "alternatif_tanim": "beklenen doz = 100 - havuzun AT ep1 temiz dogrulugu",
        "alternatif_oranlar_yuzde": {"vit_tiny": alt_vit, "resnet18": alt_res},
        "uyari": "Belge paydayi TANIMLAMIYOR. Alternatif paydayla ResNet orani "
                 "%13-17'ye duser ve '~%50' iddiasi COKER; ViT'in '<%7' iddiasi "
                 "her iki paydayla da ayakta kalir. Makaleye girecek cumle paydayi "
                 "acikca yazmalidir.",
    }
    out["not"] = ("Beklenen doz = clean on-egitimin train-test genelleme acigi "
                  "(V_A egitimde gorulmus, train acc ~%100). Bu tanim ViT'te "
                  "~19,5 puan verir - belgedeki '~+19,6' ile ayni.")
    return out


# --------------------------------------------------------------------------
# MADDE 8: val -> test aktarimi
# --------------------------------------------------------------------------
def _ols(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    sl, ic = np.polyfit(x, y, 1)
    art = y - (sl * x + ic)
    sl0 = float(x @ y / (x @ x)) if float(x @ x) > 0 else float("nan")
    art0 = y - sl0 * x
    r = float(np.corrcoef(x, y)[0, 1]) if x.size > 2 else float("nan")
    return {"n": int(x.size), "egim": r6(sl), "kesme": r6(ic),
            "artik_sd": r6(float(art.std(ddof=1))),
            "egim_orijinden": r6(sl0),
            "artik_sd_orijinden": r6(float(art0.std(ddof=1))),
            "r": r6(r)}


def madde8(yors):
    ciftler = [("A", "B"), ("B", "C"), ("A", "C")]
    var = {}

    # (i) secilen epok ciftleri, x = her kosulun KENDI bolmesindeki val_adv
    for ad, sec in (("resnet18", ARCHS["resnet18"]), ("vit_tiny", ARCHS["vit_tiny"]),
                    ("hepsi", None)):
        X, Y = [], []
        for y in yors:
            if sec is not None and y["arch"] != ad:
                continue
            for u, v in ciftler:
                X.append(y["sec"][u]["val_adv"] - y["sec"][v]["val_adv"])
                Y.append(y["sec"][u]["test_adv"] - y["sec"][v]["test_adv"])
        var[f"secilen_ciftler_kendi_bolmesi/{ad}"] = _ols(X, Y)

    # (ii) secilen epok ciftleri, x ORTAK bir olcum bolmesinde
    for arch in ARCHS:
        for meas in CONDS:
            X, Y = [], []
            for y in yors:
                if y["arch"] != arch:
                    continue
                va = 100.0 * y["val"][meas]["adv"].mean(axis=1)
                for u, v in ciftler:
                    iu, iv = y["sec"][u]["idx"], y["sec"][v]["idx"]
                    X.append(va[iu] - va[iv])
                    Y.append(y["test_adv_acc"][iu] - y["test_adv_acc"][iv])
            var[f"secilen_ciftler_ortak_olcum_V{meas}/{arch}"] = _ols(X, Y)

    # (ii-b) x = ilk kosulun KENDI bolmesinde olculen fark (asimetrik olcum)
    # ve x = V_B u V_C havuzunda olculen fark
    for arch in ARCHS:
        for etiket in ("ilk_kosulun_bolmesi", "havuz_BC_olcum"):
            X, Y = [], []
            for y in yors:
                if y["arch"] != arch:
                    continue
                for u, v in ciftler:
                    iu, iv = y["sec"][u]["idx"], y["sec"][v]["idx"]
                    if etiket == "ilk_kosulun_bolmesi":
                        va = 100.0 * y["val"][u]["adv"].mean(axis=1)
                    else:
                        va = 100.0 * np.concatenate(
                            [y["val"]["B"]["adv"], y["val"]["C"]["adv"]], axis=1
                        ).mean(axis=1)
                    X.append(va[iu] - va[iv])
                    Y.append(y["test_adv_acc"][iu] - y["test_adv_acc"][iv])
            var[f"secilen_ciftler_{etiket}/{arch}"] = _ols(X, Y)

    # (iii) essiz, dejenere-olmayan secilen-epok ciftleri
    for kapsam in ("hepsi", "resnet18", "vit_tiny"):
        X, Y, kayit = [], [], []
        gorulen = set()
        for y in yors:
            if kapsam != "hepsi" and y["arch"] != kapsam:
                continue
            for u, v in ciftler:
                iu, iv = y["sec"][u]["idx"], y["sec"][v]["idx"]
                if iu == iv:
                    continue
                anahtar = (y["tag"], min(iu, iv), max(iu, iv))
                if anahtar in gorulen:
                    continue
                gorulen.add(anahtar)
                X.append(y["sec"][u]["val_adv"] - y["sec"][v]["val_adv"])
                Y.append(y["test_adv_acc"][iu] - y["test_adv_acc"][iv])
                kayit.append(f"{y['tag']} {u}-{v} "
                             f"ep{y['sec'][u]['epoch']}-{y['sec'][v]['epoch']}")
        var[f"essiz_dejenere_olmayan_ciftler/{kapsam}"] = _ols(X, Y)
        var[f"essiz_dejenere_olmayan_ciftler/{kapsam}"]["cift_listesi"] = kayit

    # (iv) P0: TUM 100 epok - seviye regresyonu (val_adv -> test_adv)
    for arch in ARCHS:
        for meas in CONDS:
            X, Y = [], []
            for y in yors:
                if y["arch"] != arch:
                    continue
                X.append(100.0 * y["val"][meas]["adv"].mean(axis=1))
                Y.append(y["test_adv_acc"])
            var[f"tum100_seviye_V{meas}/{arch}"] = _ols(np.concatenate(X),
                                                        np.concatenate(Y))
    # (v) P0: TUM epok ciftleri - fark regresyonu
    for arch in ARCHS:
        for meas in CONDS:
            X, Y = [], []
            for y in yors:
                if y["arch"] != arch:
                    continue
                va = 100.0 * y["val"][meas]["adv"].mean(axis=1)
                ta = y["test_adv_acc"]
                iu, iv = np.triu_indices(va.size, k=1)
                X.append(va[iu] - va[iv])
                Y.append(ta[iu] - ta[iv])
            var[f"tum100_ciftler_fark_V{meas}/{arch}"] = _ols(np.concatenate(X),
                                                              np.concatenate(Y))

    hedef = (0.457, 0.790)
    eslesen = [k for k, v in var.items()
               if v["egim"] is not None and abs(v["egim"] - hedef[0]) <= 0.03
               and abs(v["artik_sd"] - hedef[1]) <= 0.05]
    yalniz_egim = [k for k, v in var.items()
                   if v["egim"] is not None and abs(v["egim"] - hedef[0]) <= 0.05]
    yakin = sorted(var.items(), key=lambda kv: abs(kv[1]["egim"] - hedef[0]))[:4]
    return {
        "iddia_metni": "9 epok ciftinde egim +0,457, artik sd 0,790 puan "
                       "(val->test aktarimi zayif)",
        "varyantlar": var,
        "iddiayi_ureten_varyant": eslesen,
        "yalniz_egimi_eslesenler": yalniz_egim,
        "egime_en_yakin_dort_varyant": {k: {"egim": v["egim"], "artik_sd": v["artik_sd"],
                                            "n": v["n"]} for k, v in yakin},
        "kontrol": {
            "yeniden_uretildi": bool(eslesen),
            "denenen_varyant_sayisi": len(var),
            "not": "Belge kurulusu tanimlamiyor: '9 epok cifti'nin hangi bolmede "
                   "olculdugu ve hangi kolu kapsadigi yazili degil. Denenen "
                   f"{len(var)} makul varyantin hicbiri (0,457 ; 0,790) ikilisini "
                   "vermiyor -> iddia BU HALIYLE YENIDEN URETILEMEZ. Nitel hukum "
                   "('val->test aktarimi zayif') yine de ayakta: secilen-epok "
                   "ciftlerinde egim 0,02-0,68, artik sd 0,05-0,86 puan.",
        },
        "nitel_hukum": {
            "secilen_cift_varyantlarinda_egim_araligi": r6(
                [min(v["egim"] for k, v in var.items() if k.startswith("secilen") or
                     k.startswith("essiz")),
                 max(v["egim"] for k, v in var.items() if k.startswith("secilen") or
                     k.startswith("essiz"))]),
            "P0_tum100_egim_araligi": r6(
                [min(v["egim"] for k, v in var.items() if k.startswith("tum100")),
                 max(v["egim"] for k, v in var.items() if k.startswith("tum100"))]),
            "aciklama": "P0 (testcurve) ile TUM 100 epok uzerinden bakildiginda "
                        "val->test egimi ~0,80-0,97 ve artik sd ~0,56-0,90 puan: "
                        "aktarim SEVIYE olarak guclu, ama secim kuralinin ilgilendigi "
                        "KOMSU-EPOK farklarinda artik gurultu farkin kendisi "
                        "kadar buyuk.",
        },
    }


# --------------------------------------------------------------------------
# MADDE 9: saldiri-RNG tabani
# --------------------------------------------------------------------------
def madde9(yors):
    hucreler = {}
    dc, da, nd_c, nd_a = [], [], [], []
    for y in yors:
        for c in CONDS:
            i = y["sec"][c]["idx"]
            k1 = y["sec"][c]["npz_clean"]
            a1 = y["sec"][c]["npz_adv"]
            k2 = y["test_clean_mask"][i]
            a2 = y["test_adv_mask"][i]
            r = {"epoch": y["sec"][c]["epoch"],
                 "clean_fark_puan": r6(100.0 * (k1.mean() - k2.mean())),
                 "clean_uyusmaz_ornek": int((k1 != k2).sum()),
                 "adv_fark_puan": r6(100.0 * (a1.mean() - a2.mean())),
                 "adv_uyusmaz_ornek": int((a1 != a2).sum())}
            hucreler[f"{y['tag']}/{c}"] = r
            dc.append(abs(r["clean_fark_puan"]))
            da.append(r["adv_fark_puan"])
            nd_c.append(r["clean_uyusmaz_ornek"])
            nd_a.append(r["adv_uyusmaz_ornek"])
    da = np.array(da)
    return {
        "iddia_metni": "clean farki 0 olmali (determinizm); adv farki saldiri "
                       "tohumu varyansi",
        "karsilastirma": "select_*_test.npz (torch.manual_seed(42)) vs "
                         "testcurve_*.npz (torch.manual_seed(42*1e5+epok))",
        "hucreler": hucreler,
        "ozet": {
            "hucre_sayisi": len(dc),
            "clean_max_mutlak_fark": r6(max(dc)),
            "clean_uyusmaz_toplam": int(sum(nd_c)),
            "adv_fark_ort": r6(float(da.mean())), "adv_fark_sd": r6(float(da.std(ddof=1))),
            "adv_max_mutlak_fark": r6(float(np.abs(da).max())),
            "adv_uyusmaz_ort": r6(float(np.mean(nd_a))),
            "adv_uyusmaz_araligi": [int(min(nd_a)), int(max(nd_a))],
        },
        "kontrol": {
            "clean_determinizm": {"hesaplanan_max_fark": r6(max(dc)),
                                  "iddia_edilen": 0.0, "tutuyor": bool(max(dc) == 0.0
                                                                       and sum(nd_c) == 0)},
            "adv_saldiri_tohumu_tabani_puan": r6(float(np.abs(da).max())),
        },
        "yorum": "Ayni checkpoint, ayni 10k test: temiz tahminler ornegine kadar "
                 "ozdes (veri butunlugu kaniti); PGD rastgele baslangici degistiginde "
                 "adv dogruluk +-0,13 puana kadar oynuyor. Bu, olculen -1,05'lik "
                 "farkin ~%12'si buyuklugunde bir olcum tabani demektir.",
    }


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default=str(ROOT / "results/q1/e2"))
    ap.add_argument("--log-dir", default=str(ROOT / "logs"))
    ap.add_argument("--out", default=str(ROOT / "results/q1/e2/e2_audit.json"))
    # Varsayilanlar = kayitli e2_audit.json'u ureten degerler (~1 dk 45 sn, CPU).
    ap.add_argument("--n-boot-s", type=int, default=200000,
                    help="Madde 3: ortak 10k test bootstrap tekrari (>=20000)")
    ap.add_argument("--n-null", type=int, default=5000,
                    help="Madde 5-6: bolme null'u tekrar sayisi")
    ap.add_argument("--n-boot-z", type=int, default=20000,
                    help="Madde 7: referans bootstrap tekrari")
    ap.add_argument("--n-mvn", type=int, default=2000000,
                    help="Madde 3: normal yaklasim cekilisi")
    ap.add_argument("--seed", type=int, default=20260817)
    args = ap.parse_args()

    in_dir = Path(args.in_dir)
    rng = np.random.default_rng(args.seed)

    print("artefaktlar yukleniyor...", flush=True)
    yors = [yukle(in_dir, a, s) for a, ss in ARCHS.items() for s in ss]

    rapor = {
        "amac": "E2_SONUC_VE_DENETIM.md'deki anahtar sayilarin kodla yeniden "
                "uretimi (hakem KRITIK bulgusu: sayilar yalniz duzyazida yasiyordu)",
        "hukum_belgesi": "results/q1/e2/E2_SONUC_VE_DENETIM.md",
        "on_kayit": "results/q1_research/E2_ISTATISTIK_PROTOKOLU.md",
        "kesifsel": True,
        "birincil_uc_noktalari_degistirmez": True,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "seed": args.seed,
        "tekrarlar": {"n_boot_s": args.n_boot_s, "n_null": args.n_null,
                      "n_boot_z": args.n_boot_z, "n_mvn": args.n_mvn},
        "secim_kurali": {"patience": PATIENCE, "min_delta": MIN_DELTA},
        "maddeler": {},
    }

    print("madde 1-2: theta birlesimi + ayrik tahminci sd'leri...", flush=True)
    m1, m2, farklar = madde1_2(yors, "vit_tiny")
    rapor["maddeler"]["1_theta_birlesimi"] = m1
    rapor["maddeler"]["2_ayrik_tahminci_sd"] = m2

    print("madde 3: esli SE + P(s<=0,010) bootstrap...", flush=True)
    rapor["maddeler"]["3_esli_SE_ve_P"] = madde3(yors, farklar, args.n_boot_s,
                                                 args.n_mvn, rng, "vit_tiny")

    print("madde 4: TOST kritik marji...", flush=True)
    rapor["maddeler"]["4_delta_yildiz"] = madde4(yors, "vit_tiny")

    print(f"madde 5-6: bolme null'u ({args.n_null} tekrar x 2 mod x 2 mimari)...",
          flush=True)
    m5, m6 = madde5_6(yors, args.n_null, rng)
    rapor["maddeler"]["5_durust_p"] = m5
    rapor["maddeler"]["6_McNemar_yanlis_pozitif"] = m6

    print("madde 7: manipulasyon kontrolu (doz)...", flush=True)
    rapor["maddeler"]["7_manipulasyon_dozu"] = madde7(yors, args.log_dir,
                                                      args.n_boot_z, rng)

    print("madde 8: val->test aktarimi...", flush=True)
    rapor["maddeler"]["8_val_test_aktarimi"] = madde8(yors)

    print("madde 9: saldiri-RNG tabani...", flush=True)
    rapor["maddeler"]["9_saldiri_rng_tabani"] = madde9(yors)

    # --- ozet hukum tablosu ---
    def bayrak(x):
        if isinstance(x, dict) and "tutuyor" in x:
            return bool(x["tutuyor"])
        if isinstance(x, dict):
            vals = [bayrak(v) for v in x.values() if isinstance(v, dict) and
                    ("tutuyor" in v or any(isinstance(w, dict) for w in v.values()))]
            return all(vals) if vals else None
        return None

    ozet = {}
    for ad, m in rapor["maddeler"].items():
        k = m.get("kontrol")
        t = bayrak(k) if k else None
        ozet[ad] = {"iddia": m.get("iddia_metni"), "tutuyor": t,
                    "hukum": {True: "TUTUYOR", False: "TUTMUYOR",
                              None: "DEGERLENDIRILEMEDI"}[t]}
    # madde 5, 6 ve 8 icin ozel hukum (cok kuruluslu / cok kollu kontroller)
    m8 = rapor["maddeler"]["8_val_test_aktarimi"]
    ozet["8_val_test_aktarimi"].update({
        "tutuyor": bool(m8["iddiayi_ureten_varyant"]),
        "hukum": "TUTUYOR" if m8["iddiayi_ureten_varyant"] else "TUTMUYOR",
        "kosul": f"{m8['kontrol']['denenen_varyant_sayisi']} varyant denendi; "
                 "(0,457 ; 0,790) ikilisini hicbiri vermiyor. Nitel hukum "
                 "('aktarim zayif') ayakta.",
    })
    k5 = rapor["maddeler"]["5_durust_p"]["kontrol"]["ozet"]
    ozet["5_durust_p"].update({
        "tutuyor": bool(k5["tutuyor"]), "hukum": k5["hukum"],
        "kosul": f"{k5['kurulus_sayisi']} kurulustan aralikta olan: "
                 + (", ".join(k5["aralikta_olan_kuruluslar"]) or "yok")
                 + f"; hesaplanan p araligi {k5['hesaplanan_aralik']}",
    })
    k6 = rapor["maddeler"]["6_McNemar_yanlis_pozitif"]["kontrol"]
    tam6 = bool(k6["vit_tiny"]["tutuyor"] and k6["resnet18"]["tutuyor"])
    ozet["6_McNemar_yanlis_pozitif"].update({
        "tutuyor": bool(k6["ortusme"]["tutuyor"]),
        "hukum": "TUTUYOR" if tam6 else ("KISMEN" if k6["ortusme"]["tutuyor"]
                                         else "TUTMUYOR"),
        "kosul": f"hesaplanan aralik {k6['ortusme']['hesaplanan_aralik']}; "
                 f"ViT kolu aralik ici: {k6['vit_tiny']['tutuyor']}, "
                 f"ResNet kolu: {k6['resnet18']['tutuyor']}",
    })
    rapor["ozet"] = ozet
    rapor["yeniden_uretilen"] = [k for k, v in ozet.items() if v["hukum"] == "TUTUYOR"]
    rapor["kismen_uretilen"] = [k for k, v in ozet.items() if v["hukum"] == "KISMEN"]
    rapor["yeniden_uretilemeyen"] = [k for k, v in ozet.items()
                                     if v["hukum"] == "TUTMUYOR"]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(str(out) + ".tmp", "w") as f:
        json.dump(rapor, f, indent=2, ensure_ascii=True)
    os.replace(str(out) + ".tmp", str(out))

    print("\n=== E2 DENETIM OZETI ===")
    for ad, v in ozet.items():
        print(f"  [{v['hukum']:<18s}] {ad}")
        if v.get("kosul"):
            print(f"      {v['kosul']}")
    print(f"\ntheta = {m1['birlesim_varyantlari']['test_npz+havuz_BC']['tohum_bazli']['theta']}"
          f" +- {m1['birlesim_varyantlari']['test_npz+havuz_BC']['tohum_bazli']['se']}"
          f"  (Q={m1['birlesim_varyantlari']['test_npz+havuz_BC']['tohum_bazli']['Q']}, "
          f"df={m1['birlesim_varyantlari']['test_npz+havuz_BC']['tohum_bazli']['df']}, "
          f"p={m1['birlesim_varyantlari']['test_npz+havuz_BC']['tohum_bazli']['p_homojenlik']})")
    print(f"sd (V_B / havuz / V_C) = {m2['sd_V_B']} / {m2['sd_havuz_BC']} / {m2['sd_V_C']}")
    m3 = rapor["maddeler"]["3_esli_SE_ve_P"]
    print(f"esli SE = {m3['ort_se']}  P(s<=0,010) = {m3['bootstrap']['P_s_le_0.010']} "
          f"({m3['bootstrap']['vurus']}/{args.n_boot_s})")
    print(f"delta* = {rapor['maddeler']['4_delta_yildiz']['delta_yildiz']}")
    print("durust p (ViT A-B) kuruluslara gore:")
    for k, p in m5["p_degerleri_vit_tiny"].items():
        print(f"    {k:<34} p = {p}")
    print(f"McNemar FP oranlari: {m6['degerler']}")
    m8 = rapor["maddeler"]["8_val_test_aktarimi"]
    print(f"val->test egimi: iddia 0,457/0,790; {m8['kontrol']['denenen_varyant_sayisi']} "
          f"varyant denendi, en yakinlari:")
    for k, v in m8["egime_en_yakin_dort_varyant"].items():
        print(f"    {k:<44} egim={v['egim']:+.4f} artik_sd={v['artik_sd']:.4f} n={v['n']}")
    print(f"\nyeniden uretilen : {rapor['yeniden_uretilen'] or 'yok'}")
    print(f"kismen uretilen  : {rapor['kismen_uretilen'] or 'yok'}")
    print(f"URETILEMEYEN     : {rapor['yeniden_uretilemeyen'] or 'yok'}")
    print(f"kaydedildi: {out}")


if __name__ == "__main__":
    main()
