# -*- coding: utf-8 -*-
"""Curutme turu (07.11.2026) ortak yardimcilari. Dondurulmus betik (experiments/q1_konsey_ayrisim.py)
DEGISTIRILMEZ; yalniz fonksiyonlari ice aktarilir. Bu modul on kayit disi, kesifsel cozumlemeler icindir."""
import hashlib
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK))
import experiments.q1_konsey_ayrisim as K  # noqa: E402

CIKTI = KOK / "results/q1/curutme_2026-11-07"
DONDURULMUS_SHA = "4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389"

C10 = ("results/q1/konsey_b4_matris", "raporlar/konsey_2026-10-29/hucre_tablosu.json")
C100 = ("results/q1/konsey_b9_c100/matris", "raporlar/konsey_2026-10-29/hucre_tablosu_b9.json")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def yukle(dizin, tablo_yol):
    M = K.Matris()
    M.ekle(KOK / dizin)
    t = K.tablo_oku(KOK / tablo_yol)
    mevcut = set(M.modeller())
    P, P2, _ = K.paneller(t, mevcut)
    return M, t, P, P2


def hucre(t, M, ad):
    return K.hucre_uyeleri(t, ad, set(M.modeller()))


def f_log(T):
    return np.log(np.clip(np.asarray(T, float) / 100.0, 1e-6, 1 - 1e-6))


def f_kappa(kappa):
    def f(T):
        x = np.clip(np.asarray(T, float) / 100.0, 1e-6, 1 - 1e-6)
        return np.log(x) - kappa * np.log(1 - x)
    return f


def f_h(T):
    x = np.clip(np.asarray(T, float) / 100.0, 1e-6, 1 - 1e-6)
    return -np.log(1 - x)


def md(g, f, m, P, kestirim="yari"):
    """Dondurulmus model_duzeyi ile ayni tanim, olcek fonksiyonu disaridan."""
    Pm = [c for c in P if c != m]
    sig = K.ort_yapi(lambda wa, Ta: sum(K.tau_ij(g, f, m, c, wa, Ta) for c in Pm) / len(Pm), kestirim)
    rho = K.ort_yapi(lambda wa, Ta: sum(K.r_ij(g, f, c, m, wa, Ta) for c in Pm) / len(Pm), kestirim)
    S = K.ort_yapi(lambda wa, Ta: sum(f(g(m, c, Ta)) for c in Pm) / len(Pm), kestirim)
    return {"sigma": float(sig), "rho": float(rho), "S": float(S)}


def kb_ka(g, f, ciftler, Vler, P):
    q, G = [], []
    for R, V in ciftler:
        a, b = md(g, f, R, P), md(g, f, V, P)
        D = a["S"] - b["S"]
        G.append(D)
        q.append((a["sigma"] - b["sigma"]) / D if abs(D) > 1e-12 else float("nan"))
    rho = [md(g, f, V, P)["rho"] for V in Vler]
    kb = K.tek_orneklem(rho)
    if kb.get("se"):
        kb["tost_p"] = K.tost_p(kb["ort"], kb["se"], kb["df"])[0]
    return {"q": q, "q_ort": float(np.mean(q)), "G": G, "K-b": kb}


def b4(g, f, hucreler, P):
    sig, rho = {}, {}
    for h, uy in hucreler.items():
        d = [md(g, f, m, P) for m in uy]
        sig[h] = [x["sigma"] for x in d]
        rho[h] = [x["rho"] for x in d]
    k = K.b4_karsitliklar(sig, rho)
    out = {}
    for ad in ("H1", "H2", "H3"):
        x = k[ad]
        out[ad] = {"kestirim": x["kestirim"], "se": x.get("se"), "df": x.get("df"), "ci90": x.get("ci90"),
                   "ci95": x.get("ci95")}
        if ad == "H3" and x.get("se"):
            out[ad]["tost_p"] = K.tost_p(x["kestirim"], x["se"], x["df"])[0]
    return out, sig, rho


class AliciBC:
    """Her-ikisi-dogru alici: kaynak ve hedef temiz ornegi dogru siniflar; kosegende hedef-dogru ile ayni."""

    def __init__(self, M):
        self.M = M
        idx = np.arange(M.n)
        self.mask = {"tam": np.ones(M.n, bool), "cift": idx % 2 == 0, "tek": idx % 2 == 1}
        self.cache = {}

    def __call__(self, s, t, alt):
        k = (s, t, alt)
        if k not in self.cache:
            d = self.M.h[(s, t)]
            m = self.mask[alt]
            sel = d["tc"][m] & (d["sc"][m] if s != t else d["tc"][m])
            self.cache[k] = 100.0 * d["aw"][m][sel].mean()
        return self.cache[k]


def yaz(ad, veri, betik):
    CIKTI.mkdir(parents=True, exist_ok=True)
    veri = dict(veri)
    veri["meta"] = {"betik": str(Path(betik).relative_to(KOK)), "betik_sha256": sha(betik),
                    "ortak_modul_sha256": sha(__file__),
                    "dondurulmus_betik_sha256": sha(KOK / "experiments/q1_konsey_ayrisim.py"),
                    "dondurulmus_betik_ayni": sha(KOK / "experiments/q1_konsey_ayrisim.py") == DONDURULMUS_SHA,
                    "uretildi_utc": datetime.now(timezone.utc).isoformat(),
                    "etiket": "kesifsel, on kayit disi; curutme turu 07.11.2026 (Q1 istatistik hakemi mercegi)"}
    yol = CIKTI / f"{ad}.json"
    with io.open(yol, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(K.jsonla(veri), fh, ensure_ascii=False, indent=1)
    print("yazildi", yol)
