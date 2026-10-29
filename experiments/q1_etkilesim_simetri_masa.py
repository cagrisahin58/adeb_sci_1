#!/usr/bin/env python3
"""Konsey 2026-10-29 masa testi: kaynak + hedef ana etkileri, aileler arasi etkilesim ve simetri.

Soru: yonlu transfer orani y(s->t) kaynak ve hedef ana etkilerinin toplamiyla ne kadar aciklaniyor,
aileler arasi (CNN = C, donusturucu = V) bir etkilesim var mi, varsa iki yonde simetrik mi?

Modeller (yalniz kosegen disi hucreler, etki kodlamasi, en kucuk kareler):
  M0: y = mu + a_s + b_t
  M1: M0 + g * 1[aile(s) != aile(t)]                      (simetrik aileler arasi terim)
  M2: M0 + g_CV * 1[s in C, t in V] + g_VC * 1[s in V, t in C]   (yonlu iki terim)

Cebirsel not (betik bunu sayisal olarak da dogrular):
  1[s in C, t in V] - 1[s in V, t in C] = 1[t in V] - 1[s in V]   (her hucrede)
Sag taraf ana etkilerin dogrusal birlesimidir; dolayisiyla M2'nin tasarim matrisi M1 ile ayni rankta,
uydurulan degerler aynidir ve g_CV - g_VC TAHMIN EDILEMEZ (ana etkilerle ozdes olarak karisir).
Ayni nedenle aile duzeyi asimetri, tam matriste, ana etkilerin aile ortalamalari farkina ozdes olarak esittir.

Girdiler (yeni olcum yok):
  results/q1/havuz_cifar10/                8 model, ornek bazli npz, dort protokol
  results/c1_c3/pair{1,2,3}/               CIFAR-10 3x3 (ResNet18_AT, ViT_Tiny_AT, WRN_28_10)
  results/q1/cifar100/transfer/pair{1,2,3}/ CIFAR-100 3x3
  results/q1/dis_veri/mahmood2021_tablolar.json  Mahmood ve ark. 2021, 8x8, her-ikisi-dogru
Cikti: results/q1/etkilesim_simetri_masa.json

Belirsizlik:
  havuz: ornek bazli bootstrap (ayni goruntu indeksleri tum hucrelerde ortak), birini-disarida-birakma
         (model jackknife), aile etiketlerinin tam permutasyonu (aile buyuklukleri sabit).
  3x3  : tohum (cift) duzeyi ortalama ve SD.
  Mahmood: parametrik binom bootstrap (m = 1000 varsayimi; hucreler bagimsiz varsayilir, yaklasiktir),
         model jackknife, tam etiket permutasyonu.
Calistirma (konteyner, depo koku):
  docker exec -w /workspace adeb_eval python experiments/q1_etkilesim_simetri_masa.py
"""
import datetime
import hashlib
import io
import itertools
import json
import os
import sys

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
os.chdir(ROOT)
sys.path.insert(0, ROOT)
from src.analysis.protokoller import PROTOKOLLER, maskeler  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OUT = "results/q1/etkilesim_simetri_masa.json"
TOHUM = 20261029
B_ORNEK = 1000
B_BINOM = 1000
KAYNAK = {}
OLCEKLER = ("oran", "logit")
V_HAVUZ = {"ViT_Tiny_AT", "Debenedetti2022_XCiT_S12"}


def sha256(yol):
    h = hashlib.sha256()
    with open(yol, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def logit_sayim(k, n):
    p = (np.asarray(k, float) + 0.5) / (np.asarray(n, float) + 1.0)
    return np.log(p / (1 - p))


def olcekle(k, n, olcek):
    k, n = np.asarray(k, float), np.asarray(n, float)
    return 100.0 * k / n if olcek == "oran" else logit_sayim(k, n)


# ------------------------------------------------------------------ tasarim
def etki_kodu(K, i):
    v = np.zeros(K - 1)
    if i < K - 1:
        v[i] = 1.0
    else:
        v[:] = -1.0
    return v


class Tasarim:
    def __init__(self, modeller, hucreler, ekler=()):
        self.modeller = list(modeller)
        self.K = K = len(modeller)
        self.idx = {m: i for i, m in enumerate(modeller)}
        self.hucreler = list(hucreler)
        rows = []
        for s, t in self.hucreler:
            r = [1.0] + list(etki_kodu(K, self.idx[s])) + list(etki_kodu(K, self.idx[t]))
            r += [float(f(s, t)) for f in ekler]
            rows.append(r)
        self.X = np.array(rows)
        self.p = self.X.shape[1]
        self.P = np.linalg.pinv(self.X)
        self.rank = int(np.linalg.matrix_rank(self.X))

    def a_vec(self, m):
        w = np.zeros(self.p)
        w[1:self.K] = etki_kodu(self.K, self.idx[m])
        return w

    def b_vec(self, m):
        w = np.zeros(self.p)
        w[self.K:2 * self.K - 1] = etki_kodu(self.K, self.idx[m])
        return w

    def tahmin_edilebilir(self, c):
        c = np.asarray(c, float)
        return bool(np.abs(c @ (self.P @ self.X) - c).max() < 1e-8)


def uydur(T, y):
    y = np.asarray(y, float)
    b = T.P @ y
    f = T.X @ b
    e = y - f
    ssr = float((e ** 2).sum())
    sst = float(((y - y.mean()) ** 2).sum())
    dof = len(y) - T.rank
    return {"b": b, "uydurulan": f, "artik": e, "R2": 1 - ssr / sst if sst > 0 else None,
            "artik_sd": float(np.sqrt(ssr / dof)) if dof > 0 else None, "artik_serbestlik": int(dof),
            "rank": T.rank, "parametre": T.p, "n_hucre": len(y)}


def R2_satir(T, Y):
    """Y: (B, n). Satir basina R2."""
    F = (Y @ T.P.T) @ T.X.T
    ssr = ((Y - F) ** 2).sum(1)
    sst = ((Y - Y.mean(1, keepdims=True)) ** 2).sum(1)
    return 1 - ssr / sst


# ------------------------------------------------------------------ cozumleme bir matris + olcek icin
class Cozumleyici:
    def __init__(self, modeller, aile, hucreler):
        self.modeller = list(modeller)
        self.aile = dict(aile)
        self.hucreler = list(hucreler)
        self.hidx = {h: i for i, h in enumerate(self.hucreler)}
        self.C = [m for m in modeller if aile[m] == "C"]
        self.V = [m for m in modeller if aile[m] == "V"]
        al = self.aile
        self.T0 = Tasarim(modeller, hucreler)
        self.T1 = Tasarim(modeller, hucreler, [lambda s, t: al[s] != al[t]])
        self.T2 = Tasarim(modeller, hucreler, [lambda s, t: al[s] == "C" and al[t] == "V",
                                               lambda s, t: al[s] == "V" and al[t] == "C"])
        T0 = self.T0
        # aile duzeyi kaynak ve hedef farklari (M0 parametreleri uzerinde dogrusal islevler)
        self.kvec = (np.mean([T0.a_vec(m) for m in self.C], 0) - np.mean([T0.a_vec(m) for m in self.V], 0)
                     if self.C and self.V else None)
        self.hvec = (np.mean([T0.b_vec(m) for m in self.V], 0) - np.mean([T0.b_vec(m) for m in self.C], 0)
                     if self.C and self.V else None)
        n = len(hucreler)
        self.cv = np.array([al[s] == "C" and al[t] == "V" for s, t in hucreler], float)
        self.vc = np.array([al[s] == "V" and al[t] == "C" for s, t in hucreler], float)
        # unordered ciftler
        self.ciftler = [(a, b) for a, b in itertools.combinations(modeller, 2)
                        if (a, b) in self.hidx and (b, a) in self.hidx]
        # yonlendirme: aileler arasi ciftte ileri yon C->V
        self.ciftler = [((b, a) if (al[a] == "V" and al[b] == "C") else (a, b)) for a, b in self.ciftler]
        D = np.zeros((len(self.ciftler), n))
        for i, (a, b) in enumerate(self.ciftler):
            D[i, self.hidx[(a, b)]] = 1.0
            D[i, self.hidx[(b, a)]] = -1.0
        self.D = D
        self.capraz = np.array([al[a] != al[b] for a, b in self.ciftler])
        self.G_lopo, self.lopo_gecerli = self._lopo()
        self.G_lmco, self.lmco_bilgi = self._lmco()

    def _asim_on(self, T, a, b):
        return T.a_vec(a) - T.a_vec(b) + T.b_vec(b) - T.b_vec(a)

    def _lopo(self):
        """Cift birak: (a,b) ve (b,a) hucreleri disarida, M0 geri kalanla uydurulur, asimetri ongorulur."""
        n = len(self.hucreler)
        G = np.full((len(self.ciftler), n), np.nan)
        ok = np.zeros(len(self.ciftler), bool)
        for i, (a, b) in enumerate(self.ciftler):
            mask = np.array([h not in ((a, b), (b, a)) for h in self.hucreler])
            Xr = self.T0.X[mask]
            if np.linalg.matrix_rank(Xr) < self.T0.rank:
                continue
            L = np.zeros((self.T0.p, n))
            L[:, mask] = np.linalg.pinv(Xr)
            G[i] = self._asim_on(self.T0, a, b) @ L
            ok[i] = True
        return G, ok

    def _lmco(self):
        """Model m'nin TUM aileler arasi hucreleri disarida; m'nin aileler arasi cift asimetrileri ongorulur."""
        n = len(self.hucreler)
        satirlar, bilgi = [], []
        for m in self.modeller:
            mask = np.array([not ((s == m or t == m) and self.aile[s] != self.aile[t]) for s, t in self.hucreler])
            Xr = self.T0.X[mask]
            if np.linalg.matrix_rank(Xr) < self.T0.rank:
                bilgi.append({"model": m, "tahmin_edilebilir": False})
                continue
            L = np.zeros((self.T0.p, n))
            L[:, mask] = np.linalg.pinv(Xr)
            idxs = [i for i, (a, b) in enumerate(self.ciftler) if m in (a, b) and self.aile[a] != self.aile[b]]
            for i in idxs:
                a, b = self.ciftler[i]
                satirlar.append((m, i, self._asim_on(self.T0, a, b) @ L))
            bilgi.append({"model": m, "tahmin_edilebilir": True, "cift_sayisi": len(idxs)})
        return satirlar, bilgi

    # -------------------------------------------------- nokta kestirimleri
    def nokta(self, y):
        y = np.asarray(y, float)
        f0, f1, f2 = uydur(self.T0, y), uydur(self.T1, y), uydur(self.T2, y)
        b0 = f0["b"]
        a = {m: float(self.T0.a_vec(m) @ b0) for m in self.modeller}
        bb = {m: float(self.T0.b_vec(m) @ b0) for m in self.modeller}
        out = {
            "M0": {k: f0[k] for k in ("R2", "artik_sd", "artik_serbestlik", "rank", "parametre", "n_hucre")},
            "M1": {k: f1[k] for k in ("R2", "artik_sd", "artik_serbestlik", "rank", "parametre")},
            "M2": {k: f2[k] for k in ("R2", "artik_sd", "artik_serbestlik", "rank", "parametre")},
        }
        out["M0"]["mu"] = float(b0[0])
        out["M0"]["kaynak_etkisi"] = a
        out["M0"]["hedef_etkisi"] = bb
        p1 = self.T1.p
        g_c = np.zeros(p1)
        g_c[-1] = 1.0
        out["M1"]["gamma_tahmin_edilebilir"] = self.T1.tahmin_edilebilir(g_c)
        out["M1"]["gamma"] = float(f1["b"][-1]) if out["M1"]["gamma_tahmin_edilebilir"] else None
        # M2: yonlu fark tahmin edilebilir mi?
        p2 = self.T2.p
        c_fark = np.zeros(p2)
        c_fark[-2], c_fark[-1] = 1.0, -1.0
        c_ort = np.zeros(p2)
        c_ort[-2], c_ort[-1] = 0.5, 0.5
        ozdeslik = None
        if self.C and self.V:
            sol = self.cv - self.vc
            sag = np.array([float(self.aile[t] == "V") - float(self.aile[s] == "V") for s, t in self.hucreler])
            ozdeslik = float(np.abs(sol - sag).max())
        out["M2"].update({
            "rank_M1": self.T1.rank,
            "max_mutlak_fark_uydurulan_M2_eksi_M1": float(np.abs(f2["uydurulan"] - f1["uydurulan"]).max()),
            "gamma_CV_eksi_gamma_VC_tahmin_edilebilir": self.T2.tahmin_edilebilir(c_fark),
            "gamma_CV_eksi_gamma_VC": (float(c_fark @ f2["b"]) if self.T2.tahmin_edilebilir(c_fark)
                                       else "tahmin edilemez (ana etkilerle ozdes karisir)"),
            "gamma_CV_arti_gamma_VC_bolu_2_tahmin_edilebilir": self.T2.tahmin_edilebilir(c_ort),
            "gamma_CV_arti_gamma_VC_bolu_2": float(c_ort @ f2["b"]) if self.T2.tahmin_edilebilir(c_ort) else None,
            "ozdeslik_kontrol_max_mutlak_1CV_eksi_1VC_eksi_1tV_arti_1sV": ozdeslik,
        })
        if self.kvec is not None:
            A = float(self.cv @ y / self.cv.sum() - self.vc @ y / self.vc.sum())
            k = float(self.kvec @ b0)
            h = float(self.hvec @ b0)
            out["aile_asimetrisi"] = {
                "A_aile_CVort_eksi_VCort": A, "kaynak_payi_Cort_alpha_eksi_Vort_alpha": k,
                "hedef_payi_Vort_beta_eksi_Cort_beta": h, "kontrol_A_eksi_kaynak_eksi_hedef": A - k - h,
                "kaynak_orani_k_bolu_A": k / A if abs(A) > 1e-12 else None,
                "aileler_arasi_hucre_sayisi_her_yon": int(self.cv.sum()),
            }
        # cift asimetrileri ve M0 artik asimetrisi
        asim = self.D @ y
        art_asim = self.D @ f0["artik"]
        out["cift_asimetrileri"] = [{"ileri": f"{a}->{b}", "aileler_arasi": bool(c), "gozlenen": float(o),
                                     "M0_artik_asimetrisi": float(r)}
                                    for (a, b), c, o, r in zip(self.ciftler, self.capraz, asim, art_asim)]
        out["M0_artik_asimetrisi_ozet"] = {
            "rms_aileler_arasi": float(np.sqrt((art_asim[self.capraz] ** 2).mean())) if self.capraz.any() else None,
            "ort_aileler_arasi": float(art_asim[self.capraz].mean()) if self.capraz.any() else None,
            "rms_aile_ici": float(np.sqrt((art_asim[~self.capraz] ** 2).mean())) if (~self.capraz).any() else None,
            "rms_gozlenen_asimetri_aileler_arasi": float(np.sqrt((asim[self.capraz] ** 2).mean())) if self.capraz.any() else None,
            "rms_gozlenen_asimetri_aile_ici": float(np.sqrt((asim[~self.capraz] ** 2).mean())) if (~self.capraz).any() else None,
        }
        # LOPO
        if self.lopo_gecerli.any():
            ok = self.lopo_gecerli
            pred = self.G_lopo[ok] @ y
            obs = asim[ok]
            err = pred - obs
            cz = self.capraz[ok]
            per = []
            for (a, b), pr, ob in zip([c for c, o in zip(self.ciftler, ok) if o], pred, obs):
                per.append({"ileri": f"{a}->{b}", "ongoru": float(pr), "gozlenen": float(ob), "hata": float(pr - ob)})
            model_rmse = {}
            for m in self.modeller:
                sel = np.array([m in c for c in [c for c, o in zip(self.ciftler, ok) if o]])
                if sel.any():
                    model_rmse[m] = float(np.sqrt((err[sel] ** 2).mean()))
            out["LOPO_cift_birak_M0"] = {
                "gecerli_cift": int(ok.sum()), "toplam_cift": len(self.ciftler),
                "rmse_tum": float(np.sqrt((err ** 2).mean())),
                "rmse_aileler_arasi": float(np.sqrt((err[cz] ** 2).mean())) if cz.any() else None,
                "rmse_aile_ici": float(np.sqrt((err[~cz] ** 2).mean())) if (~cz).any() else None,
                "ort_isaretli_hata_aileler_arasi_CVyonu": float(err[cz].mean()) if cz.any() else None,
                "beceri_1_eksi_SSE_bolu_SSsifir": float(1 - (err ** 2).sum() / (obs ** 2).sum()),
                "beceri_aileler_arasi": float(1 - (err[cz] ** 2).sum() / (obs[cz] ** 2).sum()) if cz.any() else None,
                "pearson_r_ongoru_gozlenen": float(np.corrcoef(pred, obs)[0, 1]) if len(obs) > 2 else None,
                "model_bazinda_rmse": model_rmse, "ciftler": per,
                "not": "M1'in simetrik g terimi asimetride sadelesir; asimetri ongorusu ana etkilerle yapilir.",
            }
        else:
            out["LOPO_cift_birak_M0"] = "tahmin edilemez (cift birakilinca tasarim rank kaybediyor)"
        # LMCO
        if self.G_lmco:
            rows = []
            for m, i, g in self.G_lmco:
                pr = float(g @ y)
                rows.append({"birakilan_model": m, "ileri": "%s->%s" % self.ciftler[i], "ongoru": pr,
                             "gozlenen": float(asim[i]), "hata": pr - float(asim[i])})
            e = np.array([r["hata"] for r in rows])
            ob = np.array([r["gozlenen"] for r in rows])
            by_m = {}
            for m in self.modeller:
                em = np.array([r["hata"] for r in rows if r["birakilan_model"] == m])
                if em.size:
                    by_m[m] = {"rmse": float(np.sqrt((em ** 2).mean())), "ort_isaretli_hata": float(em.mean()),
                               "aile": self.aile[m]}
            out["LMCO_model_capraz_birak_M0"] = {
                "bilgi": self.lmco_bilgi, "rmse": float(np.sqrt((e ** 2).mean())),
                "beceri": float(1 - (e ** 2).sum() / (ob ** 2).sum()),
                "model_bazinda": by_m, "satirlar": rows,
                "not": "m'nin ana etkileri yalniz aile ici hucrelerinden ve diger modellerin hucrelerinden kestirilir.",
            }
        else:
            out["LMCO_model_capraz_birak_M0"] = {"bilgi": self.lmco_bilgi}
        return out

    # -------------------------------------------------- vektorlestirilmis bootstrap istatistikleri
    def satir_istat(self, Y):
        st = {"R2_M0": R2_satir(self.T0, Y), "R2_M1": R2_satir(self.T1, Y)}
        st["dR2_M1_eksi_M0"] = st["R2_M1"] - st["R2_M0"]
        p1 = self.T1.p
        g_c = np.zeros(p1)
        g_c[-1] = 1.0
        if self.T1.tahmin_edilebilir(g_c):
            st["gamma_M1"] = (Y @ self.T1.P.T)[:, -1]
        if self.kvec is not None:
            B0 = Y @ self.T0.P.T
            st["A_aile"] = Y @ self.cv / self.cv.sum() - Y @ self.vc / self.vc.sum()
            st["kaynak_payi"] = B0 @ self.kvec
            st["hedef_payi"] = B0 @ self.hvec
        if self.lopo_gecerli.any():
            ok = self.lopo_gecerli
            pred = Y @ self.G_lopo[ok].T
            obs = Y @ self.D[ok].T
            err = pred - obs
            cz = self.capraz[ok]
            st["LOPO_rmse_tum"] = np.sqrt((err ** 2).mean(1))
            if cz.any():
                st["LOPO_rmse_aileler_arasi"] = np.sqrt((err[:, cz] ** 2).mean(1))
                st["LOPO_ort_isaretli_hata_aileler_arasi"] = err[:, cz].mean(1)
            st["LOPO_beceri"] = 1 - (err ** 2).sum(1) / (obs ** 2).sum(1)
        F0 = (Y @ self.T0.P.T) @ self.T0.X.T
        st["_artik_asim"] = (Y - F0) @ self.D.T
        return st


def ozet_dagilim(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if x.size == 0:
        return None
    return {"ort": float(x.mean()), "sd": float(x.std(ddof=1)), "GA95": [float(np.percentile(x, 2.5)),
                                                                        float(np.percentile(x, 97.5))],
            "n": int(x.size)}


def bootstrap_ozet(cz, st):
    out = {}
    for k, v in st.items():
        if k.startswith("_"):
            continue
        out[k] = ozet_dagilim(v)
    ra = st["_artik_asim"]
    sd = ra.std(0, ddof=1)
    out["artik_asimetri_olcum_sd_cift_basina"] = sd.tolist()
    return out, sd


def heterojenlik(noktasal_art_asim, sd, capraz):
    """M0 artik asimetrisinin RMS'i / ornekleme SD'sinin RMS'i: 1 civari = olcum gurultusu duzeyi."""
    r = np.asarray(noktasal_art_asim)
    out = {}
    for ad, sel in (("aileler_arasi", capraz), ("aile_ici", ~capraz), ("tum", np.ones_like(capraz))):
        if sel.any():
            out[ad] = {"rms_artik_asim": float(np.sqrt((r[sel] ** 2).mean())),
                       "rms_bootstrap_sd": float(np.sqrt((sd[sel] ** 2).mean())),
                       "oran": float(np.sqrt((r[sel] ** 2).mean()) / np.sqrt((sd[sel] ** 2).mean()))}
    return out


def jackknife(modeller, aile, hucre_y):
    sonuc, deg = [], {"gamma_M1": [], "kaynak_payi": [], "hedef_payi": [], "A_aile": [], "R2_M0": [], "R2_M1": []}
    for m in modeller:
        kal = [x for x in modeller if x != m]
        hs = [(s, t) for (s, t) in hucre_y if s in kal and t in kal]
        al = {x: aile[x] for x in kal}
        if len({al[x] for x in kal}) < 2:
            sonuc.append({"birakilan": m, "not": "tek aile kaldi"})
            continue
        cz = Cozumleyici(kal, al, hs)
        n = cz.nokta(np.array([hucre_y[h] for h in hs]))
        r = {"birakilan": m, "aile": aile[m], "R2_M0": n["M0"]["R2"], "R2_M1": n["M1"]["R2"],
             "gamma_M1": n["M1"]["gamma"]}
        if "aile_asimetrisi" in n:
            r.update({"A_aile": n["aile_asimetrisi"]["A_aile_CVort_eksi_VCort"],
                      "kaynak_payi": n["aile_asimetrisi"]["kaynak_payi_Cort_alpha_eksi_Vort_alpha"],
                      "hedef_payi": n["aile_asimetrisi"]["hedef_payi_Vort_beta_eksi_Cort_beta"]})
        sonuc.append(r)
        for k in deg:
            if r.get(k) is not None:
                deg[k].append(r[k])
    ozet = {}
    for k, v in deg.items():
        if len(v) >= 2:
            v = np.array(v)
            ozet[k] = {"min": float(v.min()), "max": float(v.max()), "n_gecerli": int(v.size),
                       "jackknife_se": float(np.sqrt((v.size - 1) / v.size * ((v - v.mean()) ** 2).sum()))}
        else:
            ozet[k] = {"n_gecerli": len(v), "not": "yetersiz gecerli birakma"}
    return {"tek_tek": sonuc, "ozet": ozet}


def permutasyon(modeller, aile, hucre_y):
    """Aile etiketlerinin tum yeniden atamalari (V buyuklugu sabit)."""
    nV = sum(1 for m in modeller if aile[m] == "V")
    hs = list(hucre_y)
    y = np.array([hucre_y[h] for h in hs])
    obs = None
    kayit = []
    for Vset in itertools.combinations(modeller, nV):
        al = {m: ("V" if m in Vset else "C") for m in modeller}
        cz = Cozumleyici(modeller, al, hs)
        n = cz.nokta(y)
        r = {"V": list(Vset), "gamma_M1": n["M1"]["gamma"], "dR2": n["M1"]["R2"] - n["M0"]["R2"],
             "kaynak_payi": n["aile_asimetrisi"]["kaynak_payi_Cort_alpha_eksi_Vort_alpha"],
             "hedef_payi": n["aile_asimetrisi"]["hedef_payi_Vort_beta_eksi_Cort_beta"],
             "A_aile": n["aile_asimetrisi"]["A_aile_CVort_eksi_VCort"]}
        kayit.append(r)
        if set(Vset) == {m for m in modeller if aile[m] == "V"}:
            obs = r
    out = {"etiketleme_sayisi": len(kayit), "en_kucuk_ulasilabilir_p": 1.0 / len(kayit), "gozlenen": obs}
    for k in ("gamma_M1", "dR2", "kaynak_payi", "hedef_payi", "A_aile"):
        v = np.array([r[k] for r in kayit if r[k] is not None], float)
        o = obs[k]
        out[k] = {"p_iki_yonlu_mutlak": float((np.abs(v) >= abs(o) - 1e-12).mean()),
                  "p_tek_yonlu_buyuk_esit": float((v >= o - 1e-12).mean()),
                  "sira_buyukten": int((v > o + 1e-12).sum()) + 1, "n": int(v.size)}
    return out


# ------------------------------------------------------------------ veri yukleme
def npz_hucre(kl, s, t):
    f = f"{kl}/per_sample_{s}_to_{t}.npz"
    KAYNAK[f] = sha256(f)
    z = np.load(f)
    tc, aw = z["target_clean_correct"].astype(bool), z["target_adv_wrong"].astype(bool)
    if "source_adv_wrong" in z.files:
        sc, sa = z["source_clean_correct"].astype(bool), z["source_adv_wrong"].astype(bool)
    else:
        fd = f"{kl}/per_sample_{s}_to_{s}.npz"
        KAYNAK[fd] = sha256(fd)
        d = np.load(fd)
        sc, sa = d["target_clean_correct"].astype(bool), d["target_adv_wrong"].astype(bool)
    return maskeler(tc, sc, sa, tani=False), aw


def ornek_matris(kl):
    tmf = f"{kl}/transfer_matrix.json"
    KAYNAK[tmf] = sha256(tmf)
    tm = json.load(io.open(tmf, encoding="utf-8"))
    mod = tm["models"]
    hs = [(s, t) for s in mod for t in mod if s != t]
    M = {p: [] for p in PROTOKOLLER}
    K = {p: [] for p in PROTOKOLLER}
    for s, t in hs:
        mk, aw = npz_hucre(kl, s, t)
        for p in PROTOKOLLER:
            M[p].append(mk[p])
            K[p].append(mk[p] & aw)
    M = {p: np.array(v, dtype=np.float32) for p, v in M.items()}
    K = {p: np.array(v, dtype=np.float32) for p, v in K.items()}
    return mod, hs, M, K, {k: tm[k] for k in tm if k != "results"}


def ozetle_nokta(n):
    """JSON'a girecek nokta kestirimi; buyuk listeler korunur."""
    return n


# ------------------------------------------------------------------ ana
def havuz_analizi(rng):
    kl = "results/q1/havuz_cifar10"
    mod, hs, M, K, meta = ornek_matris(kl)
    aile = {m: ("V" if m in V_HAVUZ else "C") for m in mod}
    # capraz kontrol: havuz_protokoller.json oranlariyla
    hp = f"{kl}/havuz_protokoller.json"
    KAYNAK[hp] = sha256(hp)
    hpj = json.load(io.open(hp, encoding="utf-8"))
    kontrol = 0.0
    N = M["raw"].shape[1]
    w1 = np.ones(N, np.float32)
    for p in PROTOKOLLER:
        y = 100 * (K[p] @ w1) / (M[p] @ w1)
        for (s, t), v in zip(hs, y):
            kontrol = max(kontrol, abs(v - hpj["yonlu"][f"{s}->{t}"]["oranlar"][p]))
    cz = Cozumleyici(mod, aile, hs)
    W = np.stack([np.bincount(rng.integers(0, N, N), minlength=N) for _ in range(B_ORNEK)]).astype(np.float32)
    out = {"modeller": mod, "aile": aile, "meta": meta, "kontrol_max_mutlak_fark_havuz_protokoller_json": kontrol,
           "paydalar_min": {p: float((M[p] @ w1).min()) for p in PROTOKOLLER}, "protokoller": {}}
    for p in PROTOKOLLER:
        k0, n0 = K[p] @ w1, M[p] @ w1
        kb, nb = W @ K[p].T, W @ M[p].T
        out["protokoller"][p] = {}
        for olc in OLCEKLER:
            y = olcekle(k0, n0, olc)
            Yb = olcekle(kb, nb, olc)
            nok = cz.nokta(y)
            st = cz.satir_istat(Yb)
            bo, sd = bootstrap_ozet(cz, st)
            hucre_y = {h: float(v) for h, v in zip(hs, y)}
            out["protokoller"][p][olc] = {
                "nokta": nok,
                "ornek_bootstrap": bo,
                "artik_asimetri_heterojenligi": heterojenlik(
                    [c["M0_artik_asimetrisi"] for c in nok["cift_asimetrileri"]], sd, cz.capraz),
                "model_jackknife": jackknife(mod, aile, hucre_y),
                "aile_etiket_permutasyonu": permutasyon(mod, aile, hucre_y),
            }
    return out


def uc_kare_analizi():
    veri = {"CIFAR-10": "results/c1_c3", "CIFAR-100": "results/q1/cifar100/transfer"}
    out = {}
    for ds, kok in veri.items():
        ds_out = {"ciftler": {}, "ozet": {}}
        topla = {}
        for c in (1, 2, 3):
            kl = f"{kok}/pair{c}"
            mod, hs, M, K, meta = ornek_matris(kl)
            aile = {m: ("V" if m.startswith("ViT") else "C") for m in mod}
            cz = Cozumleyici(mod, aile, hs)
            w1 = np.ones(M["raw"].shape[1], np.float32)
            ds_out["ciftler"][f"pair{c}"] = {"meta": meta, "aile": aile}
            for p in PROTOKOLLER:
                for olc in OLCEKLER:
                    y = olcekle(K[p] @ w1, M[p] @ w1, olc)
                    n = cz.nokta(y)
                    kisa = {"M0_R2": n["M0"]["R2"], "M0_rank": n["M0"]["rank"], "n_hucre": n["M0"]["n_hucre"],
                            "M1_rank": n["M1"]["rank"], "M1_gamma_tahmin_edilebilir": n["M1"]["gamma_tahmin_edilebilir"],
                            "M2_rank": n["M2"]["rank"],
                            "M2_fark_tahmin_edilebilir": n["M2"]["gamma_CV_eksi_gamma_VC_tahmin_edilebilir"],
                            "aile_asimetrisi": n["aile_asimetrisi"],
                            "kaynak_etkisi": n["M0"]["kaynak_etkisi"], "hedef_etkisi": n["M0"]["hedef_etkisi"]}
                    ds_out["ciftler"][f"pair{c}"].setdefault(p, {})[olc] = kisa
                    for k in ("A_aile_CVort_eksi_VCort", "kaynak_payi_Cort_alpha_eksi_Vort_alpha",
                              "hedef_payi_Vort_beta_eksi_Cort_beta"):
                        topla.setdefault((p, olc, k), []).append(kisa["aile_asimetrisi"][k])
                    topla.setdefault((p, olc, "M0_R2"), []).append(kisa["M0_R2"])
        for (p, olc, k), v in topla.items():
            v = np.array(v)
            ds_out["ozet"].setdefault(p, {}).setdefault(olc, {})[k] = {
                "ort": float(v.mean()), "sd_tohumlar_arasi": float(v.std(ddof=1)), "degerler": v.tolist()}
        ds_out["not"] = ("Tek donusturucu (ViT_Tiny_AT) varken 1[capraz] = 1[s=V] + 1[t=V]; M1 ve M2 terimleri "
                         "ViT'in kendi kaynak/hedef etkisiyle tamamen karisir (rank artmaz). Aile duzeyi ayristirma "
                         "burada ViT'in tek model etkisidir; aile genellemesi yapilamaz.")
        out[ds] = ds_out
    return out


def mahmood_analizi(rng):
    yol = "results/q1/dis_veri/mahmood2021_tablolar.json"
    KAYNAK[yol] = sha256(yol)
    mh = json.load(io.open(yol, encoding="utf-8"))
    adlar = mh["model_adlari"]
    out = {"protokol": "her-ikisi-dogru (Mahmood Denklem 3), hucre basina m = 1000 ornek varsayimi",
           "kunye": mh["kunye"]}
    for ds in ("CIFAR-10", "CIFAR-100"):
        Mx = mh["transfer_matrisleri_yuzde"][ds]
        hs = [(s, t) for s in adlar for t in adlar if s != t]
        y_or = np.array([float(Mx[s][t]) for s, t in hs])
        k0 = np.round(y_or * 10.0)
        n0 = np.full_like(k0, 1000.0)
        kb = rng.binomial(1000, np.clip(y_or / 100.0, 0, 1), size=(B_BINOM, len(hs))).astype(float)
        ds_out = {}
        for atama in ("hibrit_V", "hibrit_C"):
            aile = {m: ("V" if mh["aile"][m] == "ViT" or (mh["aile"][m] == "hibrit" and atama == "hibrit_V")
                        else "C") for m in adlar}
            cz = Cozumleyici(adlar, aile, hs)
            ds_out[atama] = {"aile": aile}
            for olc in OLCEKLER:
                y = y_or if olc == "oran" else logit_sayim(k0, n0)
                Yb = olcekle(kb, np.full_like(kb, 1000.0), olc)
                nok = cz.nokta(y)
                st = cz.satir_istat(Yb)
                bo, sd = bootstrap_ozet(cz, st)
                hucre_y = {h: float(v) for h, v in zip(hs, y)}
                ds_out[atama][olc] = {
                    "nokta": nok, "binom_bootstrap_yaklasik": bo,
                    "artik_asimetri_heterojenligi": heterojenlik(
                        [c["M0_artik_asimetrisi"] for c in nok["cift_asimetrileri"]], sd, cz.capraz),
                    "model_jackknife": jackknife(adlar, aile, hucre_y),
                    "aile_etiket_permutasyonu": permutasyon(adlar, aile, hucre_y),
                }
        # Uc cins (Mahmood: ViT [ViT-R50 dahil], BiT, ResNet): dongusel (dolasim) yonlu terim tahmin edilebilir
        cins = {m: ("ViT" if mh["aile"][m] in ("ViT", "hibrit") else ("BiT" if m.startswith("BiT") else "ResNet"))
                for m in adlar}
        dongu = {("ViT", "BiT"): 1, ("BiT", "ResNet"): 1, ("ResNet", "ViT"): 1,
                 ("BiT", "ViT"): -1, ("ResNet", "BiT"): -1, ("ViT", "ResNet"): -1}
        dol_out = {"cins": cins, "yon": "+1: ViT->BiT, BiT->ResNet, ResNet->ViT"}
        for olc in OLCEKLER:
            y = y_or if olc == "oran" else logit_sayim(k0, n0)
            Yb = olcekle(kb, np.full_like(kb, 1000.0), olc)

            def kur(cn):
                return (Tasarim(adlar, hs, [lambda s, t: cn[s] == cn[t]]),
                        Tasarim(adlar, hs, [lambda s, t: cn[s] == cn[t],
                                            lambda s, t: dongu.get((cn[s], cn[t]), 0)]))
            Ta, Tb = kur(cins)
            fa, fb = uydur(Ta, y), uydur(Tb, y)
            c = np.zeros(Tb.p)
            c[-1] = 1.0
            kap = float(fb["b"][-1]) if Tb.tahmin_edilebilir(c) else None
            kb_ = (Yb @ Tb.P.T)[:, -1]
            # cins etiketi permutasyonu (4/2/2)
            perm = []
            for vset in itertools.combinations(adlar, 4):
                kalan = [m for m in adlar if m not in vset]
                for bset in itertools.combinations(kalan, 2):
                    cn = {m: ("ViT" if m in vset else ("BiT" if m in bset else "ResNet")) for m in adlar}
                    _, Tp = kur(cn)
                    perm.append(float((Tp.P @ y)[-1]))
            perm = np.array(perm)
            dol_out[olc] = {
                "R2_M0_arti_ayni_cins": fa["R2"], "R2_arti_dolasim": fb["R2"], "dolasim_kappa": kap,
                "kappa_tahmin_edilebilir": Tb.tahmin_edilebilir(c), "rank": Tb.rank, "parametre": Tb.p,
                "kappa_binom_bootstrap_yaklasik": ozet_dagilim(kb_),
                "kappa_permutasyon": {"etiketleme": int(perm.size),
                                      "p_iki_yonlu_mutlak": float((np.abs(perm) >= abs(kap) - 1e-12).mean())},
                "ayni_cins_gamma": float(fa["b"][-1]),
            }
        ds_out["uc_cins_dolasim"] = dol_out
        out[ds] = ds_out
    return out


def main():
    rng = np.random.default_rng(TOHUM)
    t0 = datetime.datetime.now()
    sonuc = {"havuz_cifar10": havuz_analizi(rng), "uc_kare": uc_kare_analizi(), "mahmood2021": mahmood_analizi(rng)}
    out = {
        "uretildi_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "betik": "experiments/q1_etkilesim_simetri_masa.py", "tohum": TOHUM,
        "B_ornek_bootstrap": B_ORNEK, "B_binom_bootstrap": B_BINOM,
        "kaynaklar": dict(KAYNAK),
        "birim": "oran olceginde yuzde puan; logit olceginde logit((k+0.5)/(n+1))",
        "aile_kodu": "C = CNN, V = donusturucu (havuz: ViT_Tiny_AT, Debenedetti2022_XCiT_S12)",
        "yontem": __doc__,
        "sonuc": sonuc,
        "sure_sn": (datetime.datetime.now() - t0).total_seconds(),
    }
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False, default=float)
        fh.write("\n")
    print("yazildi:", OUT, "sure_sn", out["sure_sn"])


if __name__ == "__main__":
    main()
