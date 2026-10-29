# -*- coding: utf-8 -*-
"""Konsey on kayitli cozumleme betigi (B0/B7; 29.10.2026).

Tanimlar ON_KAYIT_TASLAGI.md (raporlar/konsey_2026-10-29) ile birebirdir:
  T_ij  : kaynak i'nin PGD-10 ornegi hedef j'yi yaniltir | hedef j temiz ornegi dogru siniflar (yuzde)
  w_j   : T_jj (beyaz kutu)
  r_ij  : log(T_ij/T_ji) - log(w_j/w_i)                      (yonlu artik)
  tau_ij: log tau_ij = 1/2 [log(T_ij T_ji) - log(w_i w_j)]   (simetrik verim)
  sigma_m = ort_{c in P} log tau_mc ; rho_m = ort_{c in P} r_cm ; omega_m = log w_m ;
  S_m = ort_{c in P} log T_mc (yalniz betimsel, "panel hizalanmasi").
  Ozdeslik: ort_c log T_mc = ort_c log w_c + sigma_m - 1/2 rho_m.
Birincil kestirim bolunmus yaridir: w cift indeksli, T tek indeksli goruntulerden ve tersi; iki yarinin
ortalamasi. Tam orneklem, logit ve oran olcekleri duyarliliktir.

Arayuz (fable karari K6):
  python experiments/q1_konsey_ayrisim.py --mod {masa,b2,b4} --matris-dizini DIR [--matris-dizini DIR ...]
         --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu.json --cikti JSON
Ek (istege bagli) bayraklar: --panel-en-az (varsayilan 5, ON_KAYIT §2), --bootstrap (varsayilan 2000),
--sentez (masa modunda regresyon hedefi), --sinama (ciktiya SINAMA_SONUC_DEGIL ekler).

--mod masa : mevcut havuz ve C1 cift klasorleri (eski takma adlar, MASA_ESLEME ile K5 adlarina cevrilir);
             her klasor kendi baglaminda cozumlenir; konsey_sentez_r_tau_masa.json ile regresyon yapilir.
--mod b2   : ON_KAYIT §5 B2 (K-a, K-b, K-c; Holm, aile F_B2).
--mod b4   : ON_KAYIT §5 B4 (H1-H3; Holm, aile F_B4), ikincil S1-S7 ve duyarliliklar; B6 maskeleme kurali
             icin --maskeleme-isaretli AD [AD ...].
--mod b5   : ON_KAYIT §5 B5 (korunma orani G_best/G_PGD). K6 arayuzunun eklentisidir (29.10 dogrulayici
             duzeltmesi, madde 12); saldiri turu her klasorun transfer_matrix.json 'attack' alanindan okunur.
Karar ilkesi (29.10 dogrulayici duzeltmesi): destek Holm sonrasi p ile, curutme ham aralikla okunur; H1, H2 ve
K-c'de curutme/esdegerlik destekten once denetlenir; hesaplanamayan sinama Holm ailesinde p = 1 sayilir;
sonuc haritasi sirali denetlenir (O2 > O5 > O1 > O3 > O3-varyant > O5a; O4 ek niteleme).
Klasorler birlestirilir; ayni (kaynak, hedef) hucresi birden cok klasorde varsa ilki kullanilir ve
ozdeslik denetimi ciktiya yazilir. Hucre tablosunda "dizin_takma_ad_esleme" varsa (yalniz sinama icin)
klasor icindeki adlar o eslemeyle yeniden adlandirilir.
"""
import argparse
import hashlib
import io
import json
import os
import re
import sys
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy import stats

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))
from src.analysis.protokoller import protokol_oranlari  # noqa: E402

DELTA = 0.10          # ON_KAYIT §5 esdegerlik siniri (log birimi)
DELTA_DUY = 0.06      # ON_KAYIT §5 duyarlilik siniri (yalniz CNN ciftlerinde r RMS 0,0605; karar degistirmez)
ALFA = 0.05
B5_ESIK = 0.5         # ON_KAYIT §5 B5 korunma orani esigi
BOOT_TOHUM = 20261029
S5_EGIM, S5_KESISIM, S5_BANT = 0.796, -0.01, 1.5   # ON_KAYIT S5 (FOY:1039)

# --mod masa icin eski takma ad -> K5 takma adi eslemesi (havuz ve C1 cift klasorleri).
HAVUZ_ESLEME = {
    "ResNet18_AT": "ResNet18_AT_s1001",
    "ViT_Tiny_AT": "ViT_Tiny_AT_s2001",
    "Wong2020_PRN18": "Wong2020Fast",
    "Engstrom2019_RN50": "Engstrom2019Robustness",
    "Carmon2019_WRN28_10": "Carmon2019Unlabeled",
    "Gowal2020_WRN28_10": "Gowal2020Uncovering_28_10_extra",
    "Debenedetti2022_XCiT_S12": "Debenedetti2022Light_XCiT-S12",
    # Standard_WRN28_10 (standart egitimli) K5 tablosunda yok; adi korunur, hicbir panele girmez.
}
CIFT_KUMESI = {"c1_c3": "c10_c1_secilen", "son_kontrol_noktasi": "c10_son_kontrol_noktasi",
               "cifar100/transfer": "c100_c1_secilen"}


def cift_esleme(kume, k):
    wrn = "Gowal2020Uncovering_28_10_extra" if kume.startswith("c10") else "Pang2022Robustness_WRN28_10"
    return {"ResNet18_AT": f"ResNet18_AT_s100{k}", "ViT_Tiny_AT": f"ViT_Tiny_AT_s200{k}", "WRN_28_10": wrn}


def masa_baglami(dizin):
    p = str(dizin).replace("\\", "/").rstrip("/")
    if p.endswith("havuz_cifar10"):
        return "havuz_cifar10", None, None, dict(HAVUZ_ESLEME)
    m = re.search(r"(c1_c3|son_kontrol_noktasi|cifar100/transfer)/pair(\d)$", p)
    if m:
        kume = CIFT_KUMESI[m.group(1)]
        return f"{kume}/pair{m.group(2)}", kume, int(m.group(2)), cift_esleme(kume, int(m.group(2)))
    return Path(p).name, None, None, {}


def sha256(yol):
    return hashlib.sha256(Path(yol).read_bytes()).hexdigest()


def jsonla(x):
    if isinstance(x, dict):
        return {str(k): jsonla(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonla(v) for v in x]
    if isinstance(x, (np.floating,)):
        x = float(x)
    if isinstance(x, float):
        return None if not np.isfinite(x) else x
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, np.ndarray):
        return jsonla(x.tolist())
    return x


# ----------------------------------------------------------------------------------------------
# Veri
# ----------------------------------------------------------------------------------------------
class Matris:
    """(kaynak, hedef) -> ornek bazli gostergeler. Butun klasorler ayni goruntu sirasini paylasmalidir."""

    def __init__(self):
        self.h = {}
        self.kaynaklar = {}
        self.cakisma = []
        self.n = None

    def ekle(self, dizin, esleme=None):
        dizin = Path(dizin)
        esleme = esleme or {}
        tm = dizin / "transfer_matrix.json"
        adlar = None
        if tm.exists():
            adlar = json.loads(tm.read_text(encoding="utf-8")).get("models")
            self.kaynaklar[str(tm)] = sha256(tm)
        dosyalar = {}
        if adlar:
            for s in adlar:
                for t in adlar:
                    f = dizin / f"per_sample_{s}_to_{t}.npz"
                    if f.exists():
                        dosyalar[(s, t)] = f
        else:
            for f in sorted(dizin.glob("per_sample_*_to_*.npz")):
                s, t = f.stem[len("per_sample_"):].split("_to_")
                dosyalar[(s, t)] = f
        ham = {}
        for (s, t), f in dosyalar.items():
            z = np.load(f)
            ham[(s, t)] = {k: z[k].astype(bool) for k in z.files}
            self.kaynaklar[str(f)] = sha256(f)
        for (s, t), d in ham.items():
            if "source_adv_wrong" not in d:
                # eski sema (C1 kampanyasi): kaynagin kendi beyaz kutu sonucu kosegen dosyasindan
                kd = ham.get((s, s))
                if kd is None:
                    raise SystemExit(f"{dizin}: {s} icin kosegen dosyasi yok, eski sema doldurulamaz")
                d["source_clean_correct"] = kd["target_clean_correct"]
                d["source_adv_wrong"] = kd["target_adv_wrong"]
            S, T = esleme.get(s, s), esleme.get(t, t)
            kayit = {"tc": d["target_clean_correct"], "aw": d["target_adv_wrong"],
                     "sc": d["source_clean_correct"], "sa": d["source_adv_wrong"], "dizin": str(dizin)}
            n = kayit["tc"].shape[0]
            if self.n is None:
                self.n = n
            elif n != self.n:
                raise SystemExit(f"{dizin}: orneklem {n}, onceki klasorler {self.n}")
            if (S, T) in self.h:
                e = self.h[(S, T)]
                ayni = bool(np.array_equal(e["tc"], kayit["tc"]) and np.array_equal(e["aw"], kayit["aw"]))
                self.cakisma.append({"hucre": f"{S}->{T}", "kullanilan": e["dizin"], "atlanan": str(dizin),
                                     "ozdes": ayni})
                continue
            self.h[(S, T)] = kayit

    def modeller(self):
        return sorted({s for s, _ in self.h} | {t for _, t in self.h})

    def var(self, s, t):
        return (s, t) in self.h

    def tutarlilik(self):
        """Ayni hedefin temiz-dogru maskesi butun kaynak dosyalarinda ayni olmali (goruntu sirasi denetimi)."""
        out = {}
        for t in self.modeller():
            vs = [d["tc"] for (s, tt), d in self.h.items() if tt == t]
            if vs:
                out[t] = all(np.array_equal(vs[0], v) for v in vs[1:])
        return {"hedef_maskesi_tutarli": all(out.values()), "tutarsiz_hedefler": [k for k, v in out.items() if not v]}


# ----------------------------------------------------------------------------------------------
# Oran alici ve olcekler
# ----------------------------------------------------------------------------------------------
class Alici:
    """g(s, t, alt): hedef-dogru oran (yuzde). alt in {'tam','cift','tek'}. W verilirse (n, B) agirlikla
    her bootstrap kopyasi icin (B,) dizi doner."""

    def __init__(self, M, W=None):
        self.M = M
        n = M.n
        idx = np.arange(n)
        self.mask = {"tam": np.ones(n, bool), "cift": idx % 2 == 0, "tek": idx % 2 == 1}
        self.W = None
        if W is not None:
            self.W = {a: np.ascontiguousarray(W[m]) for a, m in self.mask.items()}
        self.cache = {}

    def __call__(self, s, t, alt):
        k = (s, t, alt)
        if k not in self.cache:
            d = self.M.h[(s, t)]
            m = self.mask[alt]
            tc, aw = d["tc"][m], d["aw"][m]
            if self.W is None:
                v = 100.0 * aw[tc].mean()
            else:
                Wm = self.W[alt]
                v = 100.0 * ((aw & tc).astype(np.float32) @ Wm) / (tc.astype(np.float32) @ Wm)
            self.cache[k] = v
        return self.cache[k]


def olcek_f(ad):
    if ad == "log":
        return np.log
    if ad == "logit":
        return lambda T: (lambda p: np.log(p / (1 - p)))(np.clip(np.asarray(T) / 100.0, 1e-6, 1 - 1e-6))
    if ad == "oran":
        return lambda T: np.asarray(T, dtype=float) if np.ndim(T) else float(T)
    raise ValueError(ad)


YAPILAR = {"tam": [("tam", "tam")], "yari": [("cift", "tek"), ("tek", "cift")]}  # (w alt kumesi, T alt kumesi)


def r_ij(g, f, i, j, wa, Ta):
    return f(g(i, j, Ta)) - f(g(j, i, Ta)) - f(g(j, j, wa)) + f(g(i, i, wa))


def tau_ij(g, f, i, j, wa, Ta):
    return 0.5 * (f(g(i, j, Ta)) + f(g(j, i, Ta)) - f(g(i, i, wa)) - f(g(j, j, wa)))


def ort_yapi(fn, kestirim):
    v = [fn(wa, Ta) for wa, Ta in YAPILAR[kestirim]]
    return sum(v) / len(v)


def model_duzeyi(g, m, panel, olcek="log", kestirim="yari"):
    """sigma, rho, S (panelde m haric), omega (tam orneklem w). Eksik hucre -> KeyError."""
    f = olcek_f(olcek)
    P = [c for c in panel if c != m]
    if not P:
        raise KeyError("bos panel")
    sig = ort_yapi(lambda wa, Ta: sum(tau_ij(g, f, m, c, wa, Ta) for c in P) / len(P), kestirim)
    rho = ort_yapi(lambda wa, Ta: sum(r_ij(g, f, c, m, wa, Ta) for c in P) / len(P), kestirim)
    S = ort_yapi(lambda wa, Ta: sum(f(g(m, c, Ta)) for c in P) / len(P), kestirim)
    om = f(g(m, m, "tam"))
    return {"sigma": sig, "rho": rho, "S": S, "omega": om, "panel_n": len(P)}


def cift_nicelik(g, i, j, wa="tam", Ta="tam"):
    T_ij, T_ji, w_i, w_j = g(i, j, Ta), g(j, i, Ta), g(i, i, wa), g(j, j, wa)
    L = np.log(T_ij / T_ji)
    P = np.log(w_j / w_i)
    return {"T_ij": T_ij, "T_ji": T_ji, "w_i": w_i, "w_j": w_j, "asimetri_puan": T_ij - T_ji,
            "log_oran": L, "log_w_potansiyel": P, "r": L - P,
            "log_tau": 0.5 * (np.log(T_ij * T_ji) - np.log(w_i * w_j)),
            "potansiyel_payi": P / L if abs(L) > 1e-9 else None}


def cift_yari(g, i, j):
    q = [cift_nicelik(g, i, j, wa, Ta) for wa, Ta in YAPILAR["yari"]]
    return {k: 0.5 * (q[0][k] + q[1][k]) for k in ("r", "log_tau", "log_w_potansiyel", "log_oran")}


# ----------------------------------------------------------------------------------------------
# Istatistik
# ----------------------------------------------------------------------------------------------
def holm(p):
    p = np.asarray(p, float)
    m = len(p)
    sira = np.argsort(p)
    adj = np.empty(m)
    enb = 0.0
    for k, i in enumerate(sira):
        enb = max(enb, (m - k) * p[i])
        adj[i] = min(1.0, enb)
    return adj.tolist()


def tek_orneklem(x):
    x = np.asarray(x, float)
    n = len(x)
    out = {"degerler": x.tolist(), "n": n, "ort": float(x.mean())}
    if n < 2:
        out["not"] = "n < 2: aralik ve sinama tanimsiz"
        return out
    sd = float(x.std(ddof=1))
    se = sd / np.sqrt(n)
    df = n - 1
    out.update({"sd": sd, "se": se, "df": df,
                "ci90": [out["ort"] - stats.t.ppf(0.95, df) * se, out["ort"] + stats.t.ppf(0.95, df) * se],
                "ci95": [out["ort"] - stats.t.ppf(0.975, df) * se, out["ort"] + stats.t.ppf(0.975, df) * se]})
    return out


def holm_aile(pler):
    """ON_KAYIT §5 (29.10 dogrulayici duzeltmesi): hesaplanamayan sinama p = 1 sayilir ve ailede kalir;
    aile buyuklugu sabittir (B2 ve B4'te 3)."""
    p = [float(x) if (x is not None and np.isfinite(x)) else 1.0 for x in pler]
    return holm(p), [i for i, x in enumerate(pler) if not (x is not None and np.isfinite(x))]


def tost_p(est, se, df, delta=DELTA):
    if not (se > 0):
        return float("nan"), float("nan"), float("nan")
    p_alt = 1 - stats.t.cdf((est + delta) / se, df)   # H0: mu <= -delta
    p_ust = stats.t.cdf((est - delta) / se, df)       # H0: mu >= +delta
    return float(max(p_alt, p_ust)), float(p_alt), float(p_ust)


def karsitlik(deger, katsayi, havuz_hucreleri):
    """Hucre ortalamalari karsitligi; birlesik varyans havuz_hucreleri uzerinden (ON_KAYIT: df 5).
    Welch-Satterthwaite duyarliligi da doner."""
    ort = {h: float(np.mean(deger[h])) for h in havuz_hucreleri}
    n = {h: len(deger[h]) for h in havuz_hucreleri}
    s2 = {h: float(np.var(deger[h], ddof=1)) if n[h] > 1 else float("nan") for h in havuz_hucreleri}
    est = sum(c * ort[h] for h, c in katsayi.items())
    df = sum(n[h] - 1 for h in havuz_hucreleri)
    ss = sum(float(((np.asarray(deger[h]) - ort[h]) ** 2).sum()) for h in havuz_hucreleri)
    sp2 = ss / df if df > 0 else float("nan")
    carpan = float(np.sqrt(sum(c * c / n[h] for h, c in katsayi.items())))
    se = float(np.sqrt(sp2)) * carpan
    out = {"kestirim": est, "hucre_ort": {h: ort[h] for h in katsayi}, "hucre_n": {h: n[h] for h in katsayi},
           "katsayi": katsayi, "sp_birlesik": float(np.sqrt(sp2)), "se": se, "df": df, "carpan": carpan}
    if df > 0 and se > 0:
        t = est / se
        q90, q95 = stats.t.ppf(0.95, df), stats.t.ppf(0.975, df)
        out.update({"t": t, "ci90": [est - q90 * se, est + q90 * se], "ci95": [est - q95 * se, est + q95 * se],
                    "p_tek_kucuk": float(stats.t.cdf(t, df)), "p_tek_buyuk": float(1 - stats.t.cdf(t, df)),
                    "p_iki": float(2 * min(stats.t.cdf(t, df), 1 - stats.t.cdf(t, df)))})
        out["tost_p"], out["tost_p_alt"], out["tost_p_ust"] = tost_p(est, se, df)
    # Welch
    v = {h: c * c * s2[h] / n[h] for h, c in katsayi.items()}
    sew2 = sum(v.values())
    if all(n[h] > 1 for h in katsayi) and sew2 > 0:
        dfw = sew2 ** 2 / sum(v[h] ** 2 / (n[h] - 1) for h in katsayi)
        sew = float(np.sqrt(sew2))
        out["welch"] = {"se": sew, "df": dfw,
                        "ci90": [est - stats.t.ppf(0.95, dfw) * sew, est + stats.t.ppf(0.95, dfw) * sew],
                        "ci95": [est - stats.t.ppf(0.975, dfw) * sew, est + stats.t.ppf(0.975, dfw) * sew]}
    return out


def icinde(ci, a=-DELTA, b=DELTA):
    return ci is not None and ci[0] > a and ci[1] < b


def bootstrap_agirlik(n, B, rng):
    W = np.zeros((n, B), dtype=np.float32)
    for b in range(B):
        W[:, b] = np.bincount(rng.integers(0, n, n), minlength=n)
    return W


# ----------------------------------------------------------------------------------------------
# Hucre tablosu
# ----------------------------------------------------------------------------------------------
def tablo_oku(yol):
    t = json.loads(Path(yol).read_text(encoding="utf-8"))
    return t


def hucre_uyeleri(tablo, hucre, mevcut):
    return sorted([a for a, v in tablo["modeller"].items() if v["hucre"] == hucre and a in mevcut],
                  key=lambda a: (tablo["modeller"][a].get("tohum") or 0, a))


def paneller(tablo, mevcut):
    P = [a for a, v in tablo["modeller"].items() if v.get("birincil_panel") and a in mevcut]
    P2 = [a for a, v in tablo["modeller"].items() if v.get("ikincil_panel") and a in mevcut]
    eksik = [a for a, v in tablo["modeller"].items() if v.get("birincil_panel") and a not in mevcut]
    return P, P2, eksik


def tam_panel_kapsami(M, m, P):
    return [c for c in P if c != m and not (M.var(m, c) and M.var(c, m) and M.var(c, c))] + \
        ([] if M.var(m, m) else [m + "(kosegen)"])


# ----------------------------------------------------------------------------------------------
# B2
# ----------------------------------------------------------------------------------------------
TAHMINCILER = [("yari", "log"), ("tam", "log"), ("yari", "logit"), ("yari", "oran")]


def model_tablosu(g, modeller, P, M):
    out = {}
    for m in modeller:
        eks = tam_panel_kapsami(M, m, P)
        if eks:
            out[m] = {"eksik_hucreler": eks}
            continue
        if not [c for c in P if c != m]:
            out[m] = {"eksik_hucreler": ["panelde kendisinden baska uye yok"]}
            continue
        out[m] = {f"{k}_{o}": model_duzeyi(g, m, P, o, k) for k, o in TAHMINCILER}
    return out


def ka_kb(g, ciftler, Vler, P, kestirim="yari", olcek="log"):
    """K-a: q_s; K-b: rho(V-scr). Nokta degerleri (koşu duzeyi)."""
    qs, Ds, dsig, drho = [], [], [], []
    for R, V in ciftler:
        a = model_duzeyi(g, R, P, olcek, kestirim)
        b = model_duzeyi(g, V, P, olcek, kestirim)
        D = (a["S"] - b["S"])
        ds = a["sigma"] - b["sigma"]
        dr = -0.5 * (a["rho"] - b["rho"])
        Ds.append(D)
        dsig.append(ds)
        drho.append(dr)
        qs.append(ds / D if abs(D) > 1e-12 else float("nan"))
    rho_V = [model_duzeyi(g, V, P, olcek, kestirim)["rho"] for V in Vler]
    return {"ciftler": ciftler, "D": Ds, "simetrik_pay": dsig, "yonlu_pay": drho,
            "ozdeslik_artik_max": float(np.max(np.abs(np.array(Ds) - np.array(dsig) - np.array(drho)))) if Ds else None,
            "q": qs}, rho_V


def kc_nokta(g, Vler, P, kestirim="yari"):
    f = olcek_f("log")
    ic = {}
    for a, b in combinations(Vler, 2):
        ic[(a, b)] = ort_yapi(lambda wa, Ta: tau_ij(g, f, a, b, wa, Ta), kestirim)
    sig = {v: model_duzeyi(g, v, P, "log", kestirim)["sigma"] for v in Vler}
    return ic, sig


def b2_karar(ka, kat, kb, kc, adj, delta):
    """ON_KAYIT §5 B2 karar kurallari (29.10 dogrulayici duzeltmesi). Ilke: destek Holm sonrasi p ile,
    curutme ham aralikla okunur; kurallar ayriktir (curutme/esdegerlik once denetlenir)."""
    karar = {}
    # K-a
    if ka.get("payda_kucuk_tohumlar"):
        karar["K-a"] = "kararsiz (payda kucuk: bir tohumda D_s <= 0,10)"
    elif kat.get("ci90") is None:
        karar["K-a"] = "hesaplanamadi"
    elif kat["ci90"][1] < 0.5:
        karar["K-a"] = "curutuldu"
    elif adj[0] < ALFA:
        karar["K-a"] = "destek"
    else:
        karar["K-a"] = "kararsiz"
    karar["K-a_ongoru_buyuklugu_tuttu (her tohumda q >= 0,75)"] = ka.get("ongoru_her_tohumda_q_ge_0.75")
    # K-b: destek Holm sonrasi TOST p < 0,05; curutme mutlak deger (|ort| > delta ve %95 aralik sifiri disliyor)
    if kb.get("ci90"):
        cur = (kb["ci95"][0] > 0 or kb["ci95"][1] < 0) and abs(kb["ort"]) > delta
        if adj[1] < ALFA:
            karar["K-b"] = "destek (Holm sonrasi TOST p < 0,05)"
        elif cur:
            karar["K-b"] = "curutuldu (" + ("pozitif" if kb["ort"] > 0 else "negatif") + " yon)"
        else:
            karar["K-b"] = "kararsiz"
        karar["K-b_ham_ci90_delta_icinde"] = bool(icinde(kb["ci90"], -delta, delta))
        karar["K-b_eski_yalniz_pozitif_okuma_curutme"] = bool((kb["ci95"][0] > 0 or kb["ci95"][1] < 0) and kb["ort"] > delta)
    else:
        karar["K-b"] = "hesaplanamadi"
    # K-c: once curutme (ihmal edilebilir benzerlik farki), sonra destek
    if "bootstrap" in kc:
        if kc["bootstrap"]["ci90"][1] < delta:
            karar["K-c"] = "curutuldu"
        elif adj[2] < ALFA:
            karar["K-c"] = "destek"
        else:
            karar["K-c"] = "kararsiz"
        karar["K-c_ongoru_buyuklugu_tuttu (Delta_w >= 0,30)"] = kc.get("ongoru_Delta_ge_0.30")
    else:
        karar["K-c"] = "hesaplanamadi"
    return karar


def b2_coz(M, tablo, P, P2, args, rng):
    mevcut = set(M.modeller())
    R = hucre_uyeleri(tablo, "C1-R32", mevcut)
    V = hucre_uyeleri(tablo, "V-scr", mevcut)
    ciftler = [tuple(c) for c in tablo.get("b2_tohum_ciftleri", []) if c[0] in mevcut and c[1] in mevcut]
    g = Alici(M)
    out = {"hucreler": {"C1-R32": R, "V-scr": V}, "tohum_ciftleri": ciftler}
    out["model_tablosu"] = model_tablosu(g, sorted(mevcut & set(tablo["modeller"])), P, M)
    # K-a ve K-b, birincil (bolunmus yari, log)
    ka, rhoV = ka_kb(g, ciftler, V, P)
    kat = tek_orneklem(ka["q"])
    pa = float(1 - stats.t.cdf((kat["ort"] - 0.5) / kat["se"], kat["df"])) if kat.get("se") else float("nan")
    ka["sinama"] = kat
    ka["p_tek_H0_q_le_0.5"] = pa
    ka["ongoru_her_tohumda_q_ge_0.75"] = bool(all(q >= 0.75 for q in ka["q"])) if ka["q"] else None
    kb = tek_orneklem(rhoV)
    if kb.get("se"):
        kb["tost_p"], kb["tost_p_alt"], kb["tost_p_ust"] = tost_p(kb["ort"], kb["se"], kb["df"])
    else:
        kb["tost_p"] = float("nan")
    # K-c (tur ici benzerlik) nokta ve hiyerarsik bootstrap
    kc = {"vit_ciftleri": [list(c) for c in combinations(V, 2)]}
    eksik_kc = [f"{a}<->{b}" for a, b in combinations(V, 2) if not (M.var(a, b) and M.var(b, a))]
    if eksik_kc or len(V) < 2:
        kc["eksik_hucreler"] = eksik_kc
        kc["not"] = "Tur ici ViT hucreleri yok; K-c hesaplanamadi."
        p_kc = float("nan")
    else:
        ic, sig = kc_nokta(g, V, P)
        kc["log_tau_tur_ici"] = {f"{a}|{b}": v for (a, b), v in ic.items()}
        kc["sigma_V"] = sig
        kc["Delta_w"] = float(np.mean(list(ic.values())) - np.mean(list(sig.values())))
        W = bootstrap_agirlik(M.n, args.bootstrap, rng)
        gb = Alici(M, W)
        icb, sigb = kc_nokta(gb, V, P)
        dist = []
        yeniden = 0
        for kb_i in range(args.bootstrap):
            while True:
                sec = rng.integers(0, len(V), len(V))
                ciftb = [(V[i], V[j]) for x, i in enumerate(sec) for j in sec[x + 1:] if i != j]
                if ciftb:
                    break
                yeniden += 1
            vi = np.mean([icb[tuple(sorted((u, v), key=V.index))][kb_i] for u, v in ciftb])
            vs = np.mean([sigb[V[i]][kb_i] for i in sec])
            dist.append(vi - vs)
        dist = np.array(dist)
        kc["bootstrap"] = {"B": args.bootstrap, "ci90": [float(np.percentile(dist, 5)), float(np.percentile(dist, 95))],
                           "ci95": [float(np.percentile(dist, 2.5)), float(np.percentile(dist, 97.5))],
                           "yeniden_cekilen_tek_tohumlu_ornek": yeniden,
                           "yontem": "tohumlar yerine koyarak, goruntuler ortak agirlikla; ozdes kokenli tohum ciftleri disarida"}
        p_kc = float((1 + (dist <= 0).sum()) / (args.bootstrap + 1))
        kc["p_tek_H0_Delta_le_0"] = p_kc
        kc["ongoru_Delta_ge_0.30"] = kc["Delta_w"] >= 0.30
    # K-a payda kurali (ON_KAYIT §5, 29.10 duzeltmesi): bir tohumda D_s <= delta ise K-a kararsiz, p = 1
    ka["payda_kucuk_tohumlar"] = [i for i, D in enumerate(ka["D"]) if not (D > DELTA)]
    if ka["payda_kucuk_tohumlar"]:
        pa = float("nan")
        ka["p_tek_H0_q_le_0.5"] = pa
    # Holm F_B2 (aile buyuklugu 3, hesaplanamayan p = 1)
    pler = [pa, kb.get("tost_p", float("nan")), p_kc]
    adj, p1_sayilan = holm_aile(pler)
    karar = b2_karar(ka, kat, kb, kc, adj, DELTA)
    kb_d06 = dict(kb)
    if kb.get("se"):
        kb_d06["tost_p"] = tost_p(kb["ort"], kb["se"], kb["df"], DELTA_DUY)[0]
    adj06, _ = holm_aile([pa, kb_d06.get("tost_p", float("nan")), p_kc])
    out["F_B2"] = {"K-a": ka, "K-b": kb, "K-c": kc, "p_ham": pler, "p_holm": adj,
                   "p_1_sayilan_hesaplanamayan": p1_sayilan, "karar": karar,
                   "duyarlilik_delta_0.06": {"delta": DELTA_DUY, "p_holm": adj06,
                                             "karar": b2_karar(ka, kat, kb_d06, kc, adj06, DELTA_DUY)},
                   "not": "K-a p tek yonlu t (H0: ort q <= 0,50); K-b p TOST'un buyuk tek yonlu p'si; "
                          "K-c p hiyerarsik bootstrap (H0: Delta_w <= 0). Destek Holm sonrasi, curutme ham "
                          "aralikla okunur; ON_KAYIT §5 karar ilkesi."}
    # Duyarliliklar
    duy = {}
    for k, o in TAHMINCILER[1:]:
        a_, r_ = ka_kb(g, ciftler, V, P, k, o)
        duy[f"{k}_{o}"] = {"q_ort": float(np.mean(a_["q"])) if a_["q"] else None, "q": a_["q"],
                           "rho_V": tek_orneklem(r_)}
    jk = {}
    for c in (P if len(P) > 1 else []):
        Pj = [x for x in P if x != c]
        a_, r_ = ka_kb(g, ciftler, V, Pj)
        jk[c] = {"q_ort": float(np.mean(a_["q"])) if a_["q"] else None, "rho_V_ort": float(np.mean(r_)) if r_ else None}
    duy["panel_jackknife"] = jk
    if P2:
        try:
            a_, r_ = ka_kb(g, ciftler, V, P2)
            duy["ikincil_panel"] = {"panel": P2, "q": a_["q"], "rho_V": r_}
        except KeyError as e:
            duy["ikincil_panel"] = {"panel": P2, "eksik": str(e)}
    out["duyarlilik"] = duy
    # Tur ici ResNet benzerligi (betimsel)
    rr = {}
    f = olcek_f("log")
    for a, b in combinations(R, 2):
        if M.var(a, b) and M.var(b, a):
            rr[f"{a}|{b}"] = ort_yapi(lambda wa, Ta: tau_ij(g, f, a, b, wa, Ta), "yari")
    out["tur_ici_resnet_log_tau"] = rr
    return out


# ----------------------------------------------------------------------------------------------
# B4
# ----------------------------------------------------------------------------------------------
HUC4 = ["V-scr", "V-IN", "R224-scr", "R224-IN"]
K_H1 = {"V-scr": 1.0, "R224-scr": -1.0}
K_H2 = {"V-IN": 1.0, "V-scr": -1.0, "R224-IN": -1.0, "R224-scr": 1.0}
K_H3 = {"V-scr": 0.5, "R224-scr": -0.5, "V-IN": 0.5, "R224-IN": -0.5}


def b4_degerler(g, hucre, P, kestirim="yari", olcek="log"):
    sig, rho, om = {}, {}, {}
    for h, uy in hucre.items():
        d = [model_duzeyi(g, m, P, olcek, kestirim) for m in uy]
        sig[h] = [x["sigma"] for x in d]
        rho[h] = [x["rho"] for x in d]
        om[h] = [x["omega"] for x in d]
    return sig, rho, om


def b4_karsitliklar(sig, rho):
    return {"H1": karsitlik(sig, K_H1, HUC4), "H2": karsitlik(sig, K_H2, HUC4), "H3": karsitlik(rho, K_H3, HUC4)}


def b4_pler(k, delta=DELTA):
    """F_B4 ham p'leri: H1 tek yonlu (H0: A >= 0), H2 iki yonlu, H3 TOST +-delta. Hesaplanamayan -> nan."""
    h3 = k["H3"]
    p3 = tost_p(h3["kestirim"], h3["se"], h3["df"], delta)[0] if (h3.get("df", 0) > 0 and h3.get("se", 0) > 0) \
        else float("nan")
    return [k["H1"].get("p_tek_kucuk", float("nan")), k["H2"].get("p_iki", float("nan")), p3]


def sonuc_bolgesi(H1, H2, H3, h2_neg_holm):
    """ON_KAYIT §6 (29.10 duzeltmesi): bolgeler sirayla denetlenir, ilk tutan manseti verir; O4 ayrik bolge
    degil, H3 curutuldugunde secilen bolgeye eklenen nitelemedir."""
    if H1.startswith("curutuldu"):
        ana = "O2"
    elif not H1.startswith("destek"):
        ana = "O5"
    elif H2.startswith("destek") and H3.startswith("destek"):
        ana = "O1"
    elif H2 == "curutuldu (esdeger)":
        ana = "O3"
    elif H2 == "curutuldu (ters yon)" and h2_neg_holm:
        ana = "O3-varyant"
    else:
        ana = "O5a"
    return {"bolge": ana, "O4_niteleme": H3.startswith("curutuldu"),
            "kural": "sira: O2 > O5 > O1 > O3 > O3-varyant > O5a; O4 ek niteleme"}


def b4_karar(k, k_logit, adj=None, delta=DELTA):
    """ON_KAYIT §5 B4 karar kurallari (29.10 dogrulayici duzeltmesi). Ilke: destek Holm sonrasi p ile,
    curutme ham aralikla okunur; esdegerlik (ham %90 aralik +-delta icinde) H1 ve H2'de destekten once
    denetlenir, boylece kurallar ayriktir. adj verilmezse aile p'leri delta ile hesaplanir."""
    if adj is None:
        adj, _ = holm_aile(b4_pler(k, delta))
    out = {"delta": delta, "p_holm": list(adj)}
    h1, h2, h3 = k["H1"], k["H2"], k["H3"]
    if h1.get("ci90") is None:
        out["H1"] = "hesaplanamadi"
    elif icinde(h1["ci90"], -delta, delta):
        out["H1"] = "curutuldu (esdeger)"
    elif adj[0] < ALFA:
        out["H1"] = "destek"
    elif h1["kestirim"] > 0 and h1["ci95"][0] > 0:
        out["H1"] = "curutuldu (ters yon)"
    else:
        out["H1"] = "kararsiz"
    out["H1_ongoru_buyuklugu_tuttu (A <= -0,20)"] = bool(h1["kestirim"] <= -0.20)
    out["H1_esdeger"] = bool(icinde(h1.get("ci90"), -delta, delta))
    if h2.get("ci90") is None:
        out["H2"] = "hesaplanamadi"
    elif icinde(h2["ci90"], -delta, delta):
        out["H2"] = "curutuldu (esdeger)"
    elif adj[1] < ALFA and h2["kestirim"] > 0 and k_logit["H2"]["kestirim"] > 0:
        out["H2"] = "destek"
    elif h2["kestirim"] < 0 and h2.get("p_iki", 1) < ALFA:
        out["H2"] = "curutuldu (ters yon)"
    elif adj[1] < ALFA and h2["kestirim"] > 0:
        out["H2"] = "kararsiz (logit olceginde isaret tersine donuyor)"
    else:
        out["H2"] = "kararsiz"
    out["H2_ongoru_buyuklugu_tuttu (I >= +0,10)"] = bool(h2["kestirim"] >= 0.10)
    out["H2_esdeger"] = bool(icinde(h2.get("ci90"), -delta, delta))
    out["H2_negatif_anlamli_holm"] = bool(h2["kestirim"] < 0 and adj[1] < ALFA)
    out["H2_logit_kestirim"] = k_logit["H2"]["kestirim"]
    if h3.get("ci95") is None:
        out["H3"] = "hesaplanamadi"
    elif adj[2] < ALFA:
        out["H3"] = "destek (esdeger, Holm sonrasi TOST p < 0,05)"
    elif (h3["ci95"][0] > 0 or h3["ci95"][1] < 0) and abs(h3["kestirim"]) > delta:
        out["H3"] = "curutuldu"
    else:
        out["H3"] = "kararsiz"
    out["H3_ham_ci90_delta_icinde"] = bool(icinde(h3.get("ci90"), -delta, delta))
    sb = sonuc_bolgesi(out["H1"], out["H2"], out["H3"], out["H2_negatif_anlamli_holm"])
    out["sonuc_bolgesi"] = sb["bolge"]
    out["O4_niteleme"] = sb["O4_niteleme"]
    out["sonuc_kurali"] = sb["kural"]
    return out


def b4_cekirdek(g, hucre, P):
    sig, rho, om = b4_degerler(g, hucre, P)
    k = b4_karsitliklar(sig, rho)
    sigL, rhoL, _ = b4_degerler(g, hucre, P, "yari", "logit")
    kL = b4_karsitliklar(sigL, rhoL)
    pler = b4_pler(k)
    adj, p1 = holm_aile(pler)
    return sig, rho, om, k, kL, pler, adj, p1


def b4_coz(M, tablo, P, P2, args, rng):
    mevcut = set(M.modeller())
    hucre = {h: hucre_uyeleri(tablo, h, mevcut) for h in HUC4}
    out = {"hucreler": hucre}
    az = {h: len(v) for h, v in hucre.items() if len(v) < 2}
    if az:
        out["hata"] = f"n < 2 olan hucre: {az}; ON_KAYIT §4 hicbir hucrenin iki kosunun altina dusmesine izin vermez"
        return out
    g = Alici(M)
    out["model_tablosu"] = model_tablosu(g, sorted(mevcut & set(tablo["modeller"])), P, M)
    sig, rho, om, k, kL, pler, adj, p1 = b4_cekirdek(g, hucre, P)
    karar = b4_karar(k, kL, adj)
    out["F_B4"] = {"degerler": {"sigma": sig, "rho": rho, "omega": om}, "karsitliklar": k,
                   "p_ham": pler, "p_holm": adj, "p_1_sayilan_hesaplanamayan": p1, "karar": karar,
                   "not": "H1 tek yonlu (H0: A >= 0), H2 iki yonlu, H3 TOST +-0,10; birlesik varyans dort hucre. "
                          "Omega tam orneklem w'den (ON_KAYIT §2)."}
    # Duyarliliklar
    duy = {}
    duy["delta_0.06"] = b4_karar(k, kL, None, DELTA_DUY)
    # B6 maskeleme kurali (ON_KAYIT §5 B6): isaretli modeller cikarilarak H1-H3 yeniden; karar degisirse
    # o hipotezin manset cumlesi kararsiz (O5/O5a) sayilir.
    isaretli = [m for m in (getattr(args, "maskeleme_isaretli", None) or []) if m in mevcut]
    if isaretli:
        hm = {h: [m for m in v if m not in isaretli] for h, v in hucre.items()}
        az2 = {h: len(v) for h, v in hm.items() if len(v) < 2}
        mk = {"isaretli": isaretli, "hucreler": hm}
        if az2:
            mk["hata"] = f"isaretliler cikinca n < 2 olan hucre: {az2}; ilgili hipotezler manset disi (O5)"
            mk["degisen_hipotezler"] = [h for h, hs in (("H1", ("V-scr", "R224-scr")), ("H2", HUC4), ("H3", HUC4))
                                        if any(x in az2 for x in hs)]
        else:
            _, _, _, k_m, kL_m, _, adj_m, _ = b4_cekirdek(g, hm, P)
            km = b4_karar(k_m, kL_m, adj_m)
            mk["karar"] = km
            mk["karsitliklar"] = {h: {kk: v.get(kk) for kk in ("kestirim", "ci90", "ci95")} for h, v in k_m.items()}
            mk["degisen_hipotezler"] = [h for h in ("H1", "H2", "H3") if km[h] != karar[h]]
        mk["kural"] = "degisen hipotezin manset cumlesi kararsiz sayilir; H1 degisirse bolge O5"
        if "H1" in mk["degisen_hipotezler"]:
            mk["uygulanan_bolge"] = "O5"
        elif mk["degisen_hipotezler"]:
            mk["uygulanan_bolge"] = "O5a" if karar["sonuc_bolgesi"] in ("O1", "O3", "O3-varyant") else karar["sonuc_bolgesi"]
        else:
            mk["uygulanan_bolge"] = karar["sonuc_bolgesi"]
        out["F_B4"]["maskeleme_kurali"] = mk
    else:
        out["F_B4"]["maskeleme_kurali"] = {"isaretli": [], "uygulanan_bolge": karar["sonuc_bolgesi"],
                                           "not": "B6'da isaretli model verilmedi (--maskeleme-isaretli)"}
    for kk, o in TAHMINCILER[1:]:
        s_, r_, _ = b4_degerler(g, hucre, P, kk, o)
        duy[f"{kk}_{o}"] = {h: {key: v[key] for key in ("kestirim", "ci90", "ci95") if key in v}
                            for h, v in b4_karsitliklar(s_, r_).items()}
    duy["welch"] = {h: v.get("welch") for h, v in k.items()}
    jk = {}
    for c in (P if len(P) > 1 else []):
        Pj = [x for x in P if x != c]
        s_, r_, _ = b4_degerler(g, hucre, Pj)
        jk[c] = {h: v["kestirim"] for h, v in b4_karsitliklar(s_, r_).items()}
    duy["panel_jackknife"] = jk
    # Hiyerarsik bootstrap: hucre icinde kosular, goruntuler ortak
    W = bootstrap_agirlik(M.n, args.bootstrap, rng)
    gb = Alici(M, W)
    sb, rb, _ = b4_degerler(gb, hucre, P)
    dist = {"H1": [], "H2": [], "H3": []}
    for b in range(args.bootstrap):
        sec = {h: rng.integers(0, len(hucre[h]), len(hucre[h])) for h in HUC4}
        ms = {h: float(np.mean([sb[h][i][b] for i in sec[h]])) for h in HUC4}
        mr = {h: float(np.mean([rb[h][i][b] for i in sec[h]])) for h in HUC4}
        dist["H1"].append(sum(c * ms[h] for h, c in K_H1.items()))
        dist["H2"].append(sum(c * ms[h] for h, c in K_H2.items()))
        dist["H3"].append(sum(c * mr[h] for h, c in K_H3.items()))
    duy["hiyerarsik_bootstrap"] = {h: {"B": args.bootstrap,
                                       "ci90": [float(np.percentile(v, 5)), float(np.percentile(v, 95))],
                                       "ci95": [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]}
                                   for h, v in dist.items()}
    out["duyarlilik"] = duy
    # Ikincil (kesifsel, coklu duzeltme yok)
    ik = {}
    C1R = hucre_uyeleri(tablo, "C1-R32", mevcut)
    if len(C1R) >= 2:
        d1 = [model_duzeyi(g, m, P) for m in C1R]
        s1 = {"R224-scr": sig["R224-scr"], "C1-R32": [x["sigma"] for x in d1]}
        r1 = {"R224-scr": rho["R224-scr"], "C1-R32": [x["rho"] for x in d1]}
        a = karsitlik(s1, {"R224-scr": 1.0, "C1-R32": -1.0}, ["R224-scr", "C1-R32"])
        b = karsitlik(r1, {"R224-scr": 1.0, "C1-R32": -1.0}, ["R224-scr", "C1-R32"])
        ik["S1"] = {"sigma": a, "rho": b, "ongoru_ikisi_de_esdeger": bool(icinde(a.get("ci90")) and icinde(b.get("ci90"))),
                    "not": "birlesik varyans iki hucre (df = n1 + n2 - 2)"}
    else:
        ik["S1"] = {"eksik": "C1-R32 hucresi < 2 kosu"}
    ik["S2"] = karsitlik(rho, {"V-IN": 1.0, "V-scr": -1.0}, HUC4)
    ik["S2"]["ongoru_negatif"] = ik["S2"]["kestirim"] < 0
    ik["S3"] = {"V_baslatma": karsitlik(om, {"V-IN": 1.0, "V-scr": -1.0}, HUC4),
                "R224_baslatma": karsitlik(om, {"R224-IN": 1.0, "R224-scr": -1.0}, HUC4),
                "etkilesim": karsitlik(om, K_H2, HUC4)}
    ik["S3"]["ongoru_omega_VIN_lt_Vscr"] = ik["S3"]["V_baslatma"]["kestirim"] < 0
    # S4, S5: eslesik ciftler
    s4, s5 = [], []
    for Rm, Vm in [tuple(c) for c in tablo.get("s4_ciftleri", [])]:
        if not all(M.var(*x) for x in ((Rm, Vm), (Vm, Rm), (Rm, Rm), (Vm, Vm))):
            s4.append({"cift": [Rm, Vm], "eksik": True})
            continue
        q = cift_nicelik(g, Rm, Vm)
        qy = cift_yari(g, Rm, Vm)
        s4.append({"cift": [Rm, Vm], "tam": q, "bolunmus_yari": qy,
                   "potansiyel_payi_yari": qy["log_w_potansiyel"] / qy["log_oran"] if abs(qy["log_oran"]) > 1e-9 else None})
        asim = {}
        for yon, (s, t) in (("ileri", (Rm, Vm)), ("geri", (Vm, Rm))):
            d = M.h[(s, t)]
            asim[yon] = protokol_oranlari(d["tc"], d["aw"], d["sc"], d["sa"], tani=False)
        A = {p: asim["ileri"][p] - asim["geri"][p] for p in ("raw", "target_correct", "both_correct")}
        yay = max(A.values()) - min(A.values())
        temiz = abs(100 * M.h[(Vm, Rm)]["tc"].mean() - 100 * M.h[(Rm, Vm)]["tc"].mean())
        ong = S5_EGIM * temiz + S5_KESISIM
        s5.append({"cift": [Rm, Vm], "asimetriler": A, "yayilim_uc": yay, "temiz_fark_mutlak": temiz,
                   "ongoru": ong, "sapma": yay - ong})
    ik["S4"] = s4
    sap = [x["sapma"] for x in s5]
    s5o = tek_orneklem(sap) if sap else {"eksik": True}
    if sap and s5o.get("ci90"):
        s5o["ongoru_ort_sapma_bant_icinde"] = abs(s5o["ort"]) <= S5_BANT
        s5o["curutme_ci90_bant_disinda"] = bool(s5o["ci90"][0] > S5_BANT or s5o["ci90"][1] < -S5_BANT)
    ik["S5"] = {"ciftler": s5, "ozet": s5o, "egim_kesisim": [S5_EGIM, S5_KESISIM]}
    # S6 ikincil panel
    if P2:
        try:
            s6s, s6r, _ = b4_degerler(g, hucre, P2)
            kk2 = b4_karsitliklar(s6s, s6r)
            ik["S6"] = {"panel": P2, "A_sigma_scr": kk2["H1"]["kestirim"], "I_sigma": kk2["H2"]["kestirim"],
                        "isaret_ayni_A": bool(np.sign(kk2["H1"]["kestirim"]) == np.sign(k["H1"]["kestirim"])),
                        "isaret_ayni_I": bool(np.sign(kk2["H2"]["kestirim"]) == np.sign(k["H2"]["kestirim"]))}
        except KeyError as e:
            ik["S6"] = {"panel": P2, "eksik_hucre": str(e)}
    else:
        ik["S6"] = {"eksik": "ikincil panel yok"}
    ik["S7"] = hodge_r(g, M, sorted(mevcut & set(tablo["modeller"])))
    out["ikincil"] = ik
    return out


# ----------------------------------------------------------------------------------------------
# B5 (saldiri tarafi; ON_KAYIT §5 B5, 29.10 dogrulayici duzeltmesiyle eklendi)
# ----------------------------------------------------------------------------------------------
B5_IZINLI = {"CNN": ("pgd", "mi"), "ViT": ("pgd", "mi", "tgr")}


def b5_S(g, m, P, alt):
    Pm = [c for c in P if c != m]
    return sum(np.log(g(m, c, alt)) for c in Pm) / len(Pm)


def b5_kaynak(gler, Ms, m, aile, P, alt):
    """Kaynak m icin izinli ve panelde eksiksiz saldirilarin S_k degerleri (alt kumede)."""
    out = {}
    for s in B5_IZINLI.get(aile, ("pgd", "mi")):
        if s in Ms and all(Ms[s].var(m, c) for c in P if c != m):
            out[s] = b5_S(gler[s], m, P, alt)
    return out


def b5_en_iyi(Sc, St):
    """Capraz uydurmali secim: cift yarida en yuksek S'li saldiri tek yarida degerlendirilir ve tersi."""
    s1 = max(Sc, key=lambda s: Sc[s])
    s2 = max(St, key=lambda s: St[s])
    return 0.5 * (St[s1] + Sc[s2]), (s1, s2)


def b5_coz(Ms, tablo, P, args, rng):
    out = {"saldirilar": sorted(Ms), "izinli": {k: list(v) for k, v in B5_IZINLI.items()},
           "tanim": "S_k(m) = ort_{c in P} log T_k(m->c); G_k = ort_R S_k - ort_V S_k; korunma orani = G_best/G_PGD; "
                    "en iyi saldiri her kaynak icin panelde en yuksek S_k'yi veren izinli saldiri, capraz uydurmali "
                    "bolunmus yari secimle (cift yarida sec, tek yarida degerlendir ve tersi)."}
    if "pgd" not in Ms:
        out["hata"] = "PGD matrisi yok; G_PGD tanimsiz"
        return out
    mevcut = set().union(*[set(M.modeller()) for M in Ms.values()])
    n_ler = {s: M.n for s, M in Ms.items()}
    if len(set(n_ler.values())) != 1:
        out["hata"] = f"saldiri matrislerinin goruntu sayilari farkli: {n_ler}"
        return out
    gler = {s: Alici(M) for s, M in Ms.items()}

    def aile(m):
        return tablo["modeller"].get(m, {}).get("aile", "CNN")

    def cift_coz(hR, hV, karar_ver):
        R = hucre_uyeleri(tablo, hR, mevcut)
        V = hucre_uyeleri(tablo, hV, mevcut)
        kay = {}
        for m in R + V:
            Sc = b5_kaynak(gler, Ms, m, aile(m), P, "cift")
            St = b5_kaynak(gler, Ms, m, aile(m), P, "tek")
            Sf = b5_kaynak(gler, Ms, m, aile(m), P, "tam")
            if "pgd" not in Sc:
                kay[m] = {"eksik": "PGD panel hucreleri eksik"}
                continue
            best, sec = b5_en_iyi(Sc, St)
            kay[m] = {"S_tam": Sf, "S_pgd_yari": 0.5 * (Sc["pgd"] + St["pgd"]), "S_best_yari": best,
                      "secilen_cift_tek": list(sec), "secilen_tam_orneklem": max(Sf, key=lambda s: Sf[s]),
                      "S_best_tam": max(Sf.values())}
        R = [m for m in R if "S_best_yari" in kay.get(m, {})]
        V = [m for m in V if "S_best_yari" in kay.get(m, {})]
        o = {"R": R, "V": V, "kaynaklar": kay}
        if len(R) < 2 or len(V) < 2:
            o["hata"] = "hucrede PGD verisi tam olan kaynak < 2"
            return o
        Gp = np.mean([kay[m]["S_pgd_yari"] for m in R]) - np.mean([kay[m]["S_pgd_yari"] for m in V])
        Gb = np.mean([kay[m]["S_best_yari"] for m in R]) - np.mean([kay[m]["S_best_yari"] for m in V])
        Gpt = np.mean([kay[m]["S_tam"]["pgd"] for m in R]) - np.mean([kay[m]["S_tam"]["pgd"] for m in V])
        Gbt = np.mean([kay[m]["S_best_tam"] for m in R]) - np.mean([kay[m]["S_best_tam"] for m in V])
        o.update({"G_PGD": Gp, "G_best": Gb, "oran": Gb / Gp if abs(Gp) > 1e-12 else None,
                  "duyarlilik_tam_orneklem_secim": {"G_PGD": Gpt, "G_best": Gbt,
                                                    "oran": Gbt / Gpt if abs(Gpt) > 1e-12 else None}})
        if not karar_ver:
            return o
        # Hiyerarsik bootstrap: hucre icinde kosular yerine koyarak, goruntuler butun saldirilarda ortak agirlikla
        W = bootstrap_agirlik(n_ler["pgd"], args.bootstrap, rng)
        gb = {s: Alici(M, W) for s, M in Ms.items()}
        Sb = {}
        for m in R + V:
            Sb[m] = (b5_kaynak(gb, Ms, m, aile(m), P, "cift"), b5_kaynak(gb, Ms, m, aile(m), P, "tek"))
        dist, dGp = [], []
        for b in range(args.bootstrap):
            sR = rng.integers(0, len(R), len(R))
            sV = rng.integers(0, len(V), len(V))

            def Sbest(m):
                Sc = {s: float(v[b]) for s, v in Sb[m][0].items()}
                St = {s: float(v[b]) for s, v in Sb[m][1].items()}
                return b5_en_iyi(Sc, St)[0], 0.5 * (Sc["pgd"] + St["pgd"])
            vR = [Sbest(R[i]) for i in sR]
            vV = [Sbest(V[i]) for i in sV]
            gp = np.mean([x[1] for x in vR]) - np.mean([x[1] for x in vV])
            gbb = np.mean([x[0] for x in vR]) - np.mean([x[0] for x in vV])
            dGp.append(gp)
            dist.append(gbb / gp if abs(gp) > 1e-12 else np.nan)
        dist = np.array(dist)
        dist = dist[np.isfinite(dist)]
        o["bootstrap"] = {"B": args.bootstrap, "gecerli": int(len(dist)),
                          "ci90": [float(np.percentile(dist, 5)), float(np.percentile(dist, 95))],
                          "ci95": [float(np.percentile(dist, 2.5)), float(np.percentile(dist, 97.5))],
                          "G_PGD_ci90": [float(np.percentile(dGp, 5)), float(np.percentile(dGp, 95))],
                          "yontem": "yuzdelik; tohumlar hucre icinde yerine koyarak, goruntuler ortak agirlikla; "
                                    "secim her kopyada yeniden"}
        if not (Gp > DELTA):
            o["karar"] = "kararsiz (payda kucuk: G_PGD <= 0,10)"
        elif o["bootstrap"]["ci90"][1] < B5_ESIK:
            o["karar"] = "curutuldu (manset PGD ailesiyle sinirlanir)"
        elif o["bootstrap"]["ci90"][0] >= B5_ESIK:
            o["karar"] = "destek"
        else:
            o["karar"] = "kararsiz"
        return o

    out["birincil_C1-R32_V-scr"] = cift_coz("C1-R32", "V-scr", True)
    out["betimsel"] = {f"{a}_{b}": cift_coz(a, b, False) for a, b in (("R224-scr", "V-scr"), ("R224-IN", "V-IN"))}
    out["not"] = "B5 ayri ailedir (tek sinama), Holm'a girmez; F_B2 ve F_B4 kararlarini degistirmez."
    return out


def hodge_r(g, M, modeller, kestirim="yari"):
    """r matrisinin Hodge ayrisimi (tam bagli alt kume). delta_i = (1/K) sum_j r_ij; G = ||grad||^2/||r||^2."""
    tam = [m for m in modeller if all(M.var(m, x) and M.var(x, m) for x in modeller)]
    # tam bagli olmayan modelleri cikararak en buyuk alt kume (aci gozlu): once butun modeller
    secim = list(modeller)
    while secim and not all(M.var(a, b) for a in secim for b in secim):
        sayi = {m: sum(not (M.var(m, x) and M.var(x, m)) for x in secim) for m in secim}
        secim.remove(max(sayi, key=sayi.get))
    K = len(secim)
    if K < 3:
        return {"eksik": "tam bagli alt kume < 3 model", "tam_bagli_tek_tek": tam}
    f = olcek_f("log")
    r = np.zeros((K, K))
    for a in range(K):
        for b in range(K):
            if a != b:
                r[a, b] = ort_yapi(lambda wa, Ta: r_ij(g, f, secim[a], secim[b], wa, Ta), kestirim)
    delta = r.sum(1) / K
    grad = delta[:, None] - delta[None, :]
    curl = r - grad
    iu = np.triu_indices(K, 1)
    nA = float((r[iu] ** 2).sum())
    return {"modeller": secim, "K": K, "delta_potansiyel": {m: float(delta[i]) for i, m in enumerate(secim)},
            "G_potansiyel_payi": float((grad[iu] ** 2).sum() / nA) if nA > 0 else None,
            "G_rastgele_beklenti_2_bolu_K": 2.0 / K,
            "dolasim_rms": float(np.sqrt((curl[iu] ** 2).mean())), "r_rms": float(np.sqrt((r[iu] ** 2).mean())),
            "r_matrisi": r.tolist(), "dolasim_matrisi": curl.tolist()}


# ----------------------------------------------------------------------------------------------
# masa: havuz ve C1 cift klasorleri, SENTEZ regresyonu
# ----------------------------------------------------------------------------------------------
def ozet(liste, anahtar):
    a = np.array([q[anahtar] for q in liste], dtype=float)
    return {"degerler": a.tolist(), "ort": float(a.mean()), "sd_kosum": float(a.std(ddof=1)) if len(a) > 1 else None}


def sentez_bootstrap(M, i, j, B=300, tohum=0):
    """_sentez_r_tau_masa.py bootstrap_r ile ayni RNG sirasi (dogrulama icin birebir)."""
    rng = np.random.default_rng(tohum)
    d = {(a, b): (M.h[(a, b)]["tc"], M.h[(a, b)]["aw"]) for a in (i, j) for b in (i, j)}
    n = len(d[(i, i)][0])
    rs, ts = [], []
    for _ in range(B):
        ix = rng.integers(0, n, n)

        def o(a, b):
            tc, aw = d[(a, b)]
            tc, aw = tc[ix], aw[ix]
            return 100.0 * aw[tc].mean()
        wi, wj, Tij, Tji = o(i, i), o(j, j), o(i, j), o(j, i)
        rs.append(np.log(Tij / Tji) - np.log(wj / wi))
        ts.append(0.5 * (np.log(Tij * Tji) - np.log(wi * wj)))
    return {"r_sd": float(np.std(rs, ddof=1)), "log_tau_sd": float(np.std(ts, ddof=1)), "B": B}


def masa_coz(dizinler, tablo, args):
    out = {"baglamlar": {}, "sentez_uyumlu": {"kumeler": {}}}
    kume_kayit = {}
    havuz = None
    for dz in dizinler:
        ad, kume, k, esl = masa_baglami(dz)
        M = Matris()
        M.ekle(dz, esl)
        g = Alici(M)
        kayit = {"dizin": str(dz), "esleme": esl, "modeller": M.modeller(), "tutarlilik": M.tutarlilik()}
        if kume:
            R, V = f"ResNet18_AT_s100{k}", f"ViT_Tiny_AT_s200{k}"
            tam = cift_nicelik(g, R, V)
            yari = cift_yari(g, R, V)
            kayit["RV_tam"] = tam
            kayit["RV_bolunmus_yari"] = yari
            kume_kayit.setdefault(kume, {})[k] = (M, tam, yari)
        if ad == "havuz_cifar10":
            havuz = (M, g)
        out["baglamlar"][ad] = kayit
    # SENTEZ kumeler
    for kume, d in kume_kayit.items():
        ks = sorted(d)
        tam = [d[k][1] for k in ks]
        yari = [d[k][2] for k in ks]
        kayit = {"tam_orneklem": {key: ozet(tam, key) for key in ("asimetri_puan", "log_oran", "log_w_potansiyel", "r",
                                                                   "log_tau", "potansiyel_payi")},
                 "bolunmus_yari": {key: ozet(yari, key) for key in ("r", "log_tau", "log_w_potansiyel", "log_oran")}}
        if 1 in d:
            kayit["goruntu_bootstrap_pair1"] = sentez_bootstrap(d[1][0], "ResNet18_AT_s1001", "ViT_Tiny_AT_s2001")
        out["sentez_uyumlu"]["kumeler"][kume] = kayit
    # Havuz
    if havuz:
        M, g = havuz
        mevcut = set(M.modeller())
        P, P2, eksik = paneller(tablo, mevcut)
        ters = {v: k for k, v in HAVUZ_ESLEME.items()}
        R, V, X = "ResNet18_AT_s1001", "ViT_Tiny_AT_s2001", "Debenedetti2022Light_XCiT-S12"
        Pk = sorted(P, key=lambda c: list(HAVUZ_ESLEME.values()).index(c))
        # SENTEZ panel sirasi: Wong, Engstrom, Carmon, Gowal
        sira = ["Wong2020Fast", "Engstrom2019Robustness", "Carmon2019Unlabeled", "Gowal2020Uncovering_28_10_extra"]
        Pk = [c for c in sira if c in P] + [c for c in Pk if c not in sira]
        hv = {}
        for m in (V, R, X):
            satir = {c: cift_nicelik(g, c, m) for c in Pk}
            hv[ters[m]] = {"panel": [ters[c] for c in Pk],
                           "r_uyeler (CNN->m yonunde)": {ters[c]: satir[c]["r"] for c in Pk},
                           "r_ort": float(np.mean([satir[c]["r"] for c in Pk])),
                           "log_tau_uyeler": {ters[c]: satir[c]["log_tau"] for c in Pk},
                           "log_tau_ort": float(np.mean([satir[c]["log_tau"] for c in Pk]))}
        ic = [cift_nicelik(g, Pk[a], Pk[b])["log_tau"] for a in range(len(Pk)) for b in range(a + 1, len(Pk))]
        hv["panel_ici_log_tau"] = {"degerler": ic, "ort": float(np.mean(ic))}
        hv["ResNet18_ViT_cifti"] = cift_nicelik(g, R, V)
        mR = model_duzeyi(g, R, Pk, "log", "tam")
        mV = model_duzeyi(g, V, Pk, "log", "tam")
        dk = mR["S"] - mV["S"]
        sim = mR["sigma"] - mV["sigma"]
        yon = -0.5 * (mR["rho"] - mV["rho"])
        hed = lambda m: float(np.mean([np.log(g(c, m, "tam")) for c in Pk]))  # noqa: E731
        dh = hed(V) - hed(R)
        pot = float(mV["omega"] - mR["omega"])
        hv["kaynak_acigi_ayristirma_log"] = {"toplam": dk, "simetrik_pay": sim, "yonlu_pay": yon,
                                             "kontrol_artik": dk - sim - yon, "simetrik_oran": sim / dk}
        hv["hedef_farki_ayristirma_log"] = {"toplam": dh, "potansiyel_pay": pot, "simetrik_pay": -sim,
                                            "yonlu_pay": 0.5 * (mV["rho"] - mR["rho"]),
                                            "kontrol_artik": dh - pot + sim - 0.5 * (mV["rho"] - mR["rho"])}
        out["sentez_uyumlu"]["havuz_tohum1"] = hv
        # On kayit tanimlariyla (K5 adlari, bolunmus yari birincil) havuz model tablosu ve B2 nokta kestirimleri
        hz = {"birincil_panel_mevcut": Pk, "birincil_panel_eksik": eksik, "ikincil_panel": P2,
              "panel_en_az_saglaniyor_mu": len(Pk) >= args.panel_en_az,
              "model_tablosu": model_tablosu(g, sorted(mevcut & set(tablo["modeller"])), Pk, M)}
        bn = {}
        for k_, o_ in TAHMINCILER:
            a_, r_ = ka_kb(g, [(R, V)], [V], Pk, k_, o_)
            bn[f"{k_}_{o_}"] = {"D": a_["D"][0], "simetrik_pay": a_["simetrik_pay"][0], "yonlu_pay": a_["yonlu_pay"][0],
                                "q": a_["q"][0], "rho_V": r_[0]}
        hz["b2_nokta_tohum1"] = bn
        hz["not"] = "Tek tohum (1001/2001) ve dort uyeli panel: sinama degil, on kayit oncesi gorulmus veri (ON_KAYIT §1)."
        out["havuz_on_kayit_tanimlari"] = hz
    # kesinlik plani
    km = out["sentez_uyumlu"]["kumeler"].get("c10_c1_secilen")
    if km:
        t95 = 2.015
        s_r = km["tam_orneklem"]["r"]["sd_kosum"]
        s_t = km["tam_orneklem"]["log_tau"]["sd_kosum"]
        out["sentez_uyumlu"]["kesinlik_plani"] = {
            "t_0.95_df5": t95, "r_sd": s_r, "log_tau_sd": s_t,
            "yari_genislik_r_2e2": t95 * s_r * np.sqrt(1 / 2 + 1 / 2),
            "yari_genislik_r_2e3": t95 * s_r * np.sqrt(1 / 2 + 1 / 3),
            "yari_genislik_logtau_2e2": t95 * s_t * np.sqrt(1 / 2 + 1 / 2),
            "yari_genislik_logtau_2e3": t95 * s_t * np.sqrt(1 / 2 + 1 / 3),
            "t_0.95_df5_kesin": float(stats.t.ppf(0.95, 5))}
    return out


def duzlestir(x, onek=""):
    out = {}
    if isinstance(x, dict):
        for k, v in x.items():
            out.update(duzlestir(v, f"{onek}.{k}" if onek else str(k)))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            out.update(duzlestir(v, f"{onek}[{i}]"))
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        out[onek] = float(x)
    return out


def regresyon(sentez_yolu, yeni, tol=1e-6):
    eski = json.loads(Path(sentez_yolu).read_text(encoding="utf-8"))
    e = duzlestir({k: eski[k] for k in ("kumeler", "havuz_tohum1", "kesinlik_plani") if k in eski})
    y = duzlestir(jsonla(yeni))
    satir = []
    for k in sorted(e):
        if k in y:
            satir.append({"anahtar": k, "sentez": e[k], "yeni": y[k], "fark": y[k] - e[k]})
    eksik = sorted(set(e) - set(y))
    fazla = sorted(set(y) - set(e))
    mx = max((abs(s["fark"]) for s in satir), default=float("nan"))
    return {"sentez": str(sentez_yolu), "sentez_sha256": sha256(sentez_yolu), "tolerans": tol,
            "karsilastirilan": len(satir), "en_buyuk_mutlak_fark": mx,
            "gecti": bool(mx <= tol and not eksik), "sentezde_olup_yenide_olmayan": eksik,
            "yenide_olup_sentezde_olmayan_sayisi": len(fazla), "satirlar": satir}


# ----------------------------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mod", required=True, choices=["masa", "b2", "b4", "b5"])
    ap.add_argument("--matris-dizini", action="append", required=True)
    ap.add_argument("--hucre-tablosu", required=True)
    ap.add_argument("--cikti", required=True)
    ap.add_argument("--panel-en-az", type=int, default=5)
    ap.add_argument("--bootstrap", type=int, default=2000)
    ap.add_argument("--sentez", default=str(KOK / "results" / "q1" / "konsey_sentez_r_tau_masa.json"))
    ap.add_argument("--sinama", action="store_true")
    ap.add_argument("--maskeleme-isaretli", nargs="*", default=[],
                    help="B6'da PGD-10 ile AA arasi fark 10 puani asan modeller (b4 maskeleme kurali)")
    a = ap.parse_args(argv)
    tablo = tablo_oku(a.hucre_tablosu)
    rng = np.random.default_rng(BOOT_TOHUM)
    meta = {"betik": "experiments/q1_konsey_ayrisim.py", "betik_sha256": sha256(__file__),
            "hucre_tablosu": a.hucre_tablosu, "hucre_tablosu_sha256": sha256(a.hucre_tablosu),
            "mod": a.mod, "matris_dizinleri": a.matris_dizini, "uretildi_utc": datetime.now(timezone.utc).isoformat(),
            "delta": DELTA, "delta_duyarlilik": DELTA_DUY, "alfa": ALFA, "bootstrap_B": a.bootstrap,
            "bootstrap_tohum": BOOT_TOHUM, "panel_en_az": a.panel_en_az,
            "maskeleme_isaretli": a.maskeleme_isaretli,
            "numpy": np.__version__}
    sonuc = {}
    if a.sinama:
        sonuc["SINAMA_SONUC_DEGIL"] = True
    sonuc["meta"] = meta
    if a.mod == "masa":
        r = masa_coz(a.matris_dizini, tablo, a)
        r["regresyon"] = regresyon(a.sentez, r["sentez_uyumlu"])
        sonuc.update(r)
    elif a.mod == "b5":
        esl_tum = tablo.get("dizin_takma_ad_esleme", {})
        sal_tum = tablo.get("dizin_saldiri_esleme", {})
        Ms = {}
        for dz in a.matris_dizini:
            key = str(dz).replace("\\", "/").rstrip("/")
            esl = next((v for k, v in esl_tum.items() if key.endswith(k.rstrip("/"))), None)
            sal = next((v for k, v in sal_tum.items() if key.endswith(k.rstrip("/"))), None)
            if sal is None:
                tm = Path(dz) / "transfer_matrix.json"
                sal = json.loads(tm.read_text(encoding="utf-8")).get("attack", "pgd") if tm.exists() else "pgd"
            Ms.setdefault(sal, Matris()).ekle(dz, esl)
        mevcut = set().union(*[set(M.modeller()) for M in Ms.values()]) if Ms else set()
        P, P2, eksik = paneller(tablo, mevcut)
        sonuc["veri"] = {s: {"n_goruntu": M.n, "modeller": M.modeller(), "hucre_sayisi": len(M.h),
                             "cakismalar": M.cakisma, "tutarlilik": M.tutarlilik(), "girdi_sha256": M.kaynaklar}
                         for s, M in Ms.items()}
        sonuc["panel"] = {"birincil": P, "birincil_eksik": eksik, "ikincil": P2}
        if len(P) < a.panel_en_az:
            sonuc["hata"] = f"birincil panelde {len(P)} uye var; ON_KAYIT §2 en az {a.panel_en_az} ister"
        else:
            sonuc["b5"] = b5_coz(Ms, tablo, P, a, rng)
    else:
        M = Matris()
        esl_tum = tablo.get("dizin_takma_ad_esleme", {})
        for dz in a.matris_dizini:
            key = str(dz).replace("\\", "/").rstrip("/")
            esl = next((v for k, v in esl_tum.items() if key.endswith(k.rstrip("/"))), None)
            M.ekle(dz, esl)
        mevcut = set(M.modeller())
        P, P2, eksik = paneller(tablo, mevcut)
        sonuc["veri"] = {"n_goruntu": M.n, "modeller": sorted(mevcut), "hucre_sayisi": len(M.h),
                         "cakismalar": M.cakisma, "tutarlilik": M.tutarlilik(),
                         "tablo_disi_modeller": sorted(mevcut - set(tablo["modeller"])),
                         "girdi_sha256": M.kaynaklar}
        sonuc["panel"] = {"birincil": P, "birincil_eksik": eksik, "ikincil": P2}
        if len(P) < a.panel_en_az:
            sonuc["hata"] = f"birincil panelde {len(P)} uye var; ON_KAYIT §2 en az {a.panel_en_az} ister"
        else:
            sonuc[a.mod] = (b2_coz if a.mod == "b2" else b4_coz)(M, tablo, P, P2, a, rng)
    Path(a.cikti).parent.mkdir(parents=True, exist_ok=True)
    with io.open(a.cikti, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(jsonla(sonuc), fh, ensure_ascii=False, indent=1)
    if a.mod == "masa":
        rg = sonuc["regresyon"]
        print(f"regresyon: {rg['karsilastirilan']} anahtar, en buyuk |fark| {rg['en_buyuk_mutlak_fark']:.3e}, "
              f"gecti={rg['gecti']}, eksik={len(rg['sentezde_olup_yenide_olmayan'])}")
    print("yazildi:", a.cikti)
    return sonuc


if __name__ == "__main__":
    main()
