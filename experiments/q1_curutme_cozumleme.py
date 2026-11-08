# -*- coding: utf-8 -*-
"""Curutme zinciri (08.11.2026) cozumleme sarmalayicisi: A, B, C1, C2, G ve B1-18 ara noktalari.

Dondurulmus experiments/q1_konsey_ayrisim.py DEGISTIRILMEDEN importlib ile yuklenir; yuklemeden once
sha256'si DONDURULMUS_SHA ile karsilastirilir, farkliysa durur (kod 5). sigma, rho, S ve omega yalniz
dondurulmus model_duzeyi() ile (bolunmus yari, log olcek) hesaplanir; Matris ve Alici siniflari ve
bootstrap_agirlik() de dondurulmus betiktendir. Bu dosyanin yaptigi yalniz hucre ortalamasi, karsitlik,
goruntu bootstrap'i ve ek on kayittaki (raporlar/konsey_2026-10-29/ON_KAYIT_EK_CURUTME_2026-11-08.md)
siniflandirma kurallaridir. Ciktiya dondurulmus betigin sha256'si yazilir.

Bloklar (--blok):
  A     ayna paneli {XCiT-S12, XCiT-M12, XCiT-L12} (hucre tablosunda ayna_panel = true); birincil karsitlik
        V-IN satirinda: rho_T(V-IN) ve sigma_T(V-IN) - sigma_T(R224-IN). Ikincil (betimsel): sifirdan satiri.
  B     birincil panel (7 RobustBench CNN); sigma(V-scr+) - sigma(R224-scr) ve eslesme kosullari
        (|temiz fark| <= 6 puan, |w fark| <= 2 puan; iki tohum ortalamasi).
  C1    sigma(V-IN21k) - sigma(V-IN) ve rho(V-IN21k) - rho(V-IN).
  C2    sigma(R224-SWSL) - sigma(R224-IN) ve olcek satiri etkilesimi
        [sigma(V-IN21k) - sigma(V-IN)] - [sigma(R224-SWSL) - sigma(R224-IN)].
  G     model duzeyi sigma ~ omega dogrusal regresyonu (224 girdili egitilmis hucreler); V hucrelerinin artik
        ortalamasi eksi R224 hucrelerinin artik ortalamasi; CKA kismi Mantel sonucu (--mantel) ile karar.
  B118  B3 kosularinin ara kontrol noktalari (<kosu>_eXXX) icin sigma, rho, omega yorungesi (betimsel).
Aralik: goruntu bootstrap'i (B = 2000, tohum 20261030, ortak agirlik butun hucrelerde), yuzdelik %90/%95.
Bu aralik tohum degiskenligini tasimaz (iki tohum); karar nokta kestirimiyle verilir, aralik raporlanir.
--dislanan: B6 maskeleme kuraliyla isaretlenen modeller (D blogu); verilirse karsitliklar onlar cikarilarak
da hesaplanir ve ikisi birlikte yazilir.
"""
import argparse
import re
import hashlib
import importlib.util
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

KOK = Path(__file__).resolve().parents[1]
DONDURULMUS = KOK / "experiments" / "q1_konsey_ayrisim.py"
DONDURULMUS_SHA = "4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389"
TOHUM = 20261030
_DM = None


def sha256(yol):
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def dondurulmus():
    global _DM
    if _DM is None:
        s = sha256(DONDURULMUS)
        if s != DONDURULMUS_SHA:
            print(f"DONDURULMUS BETIK DEGISMIS: {DONDURULMUS} sha256 {s} != {DONDURULMUS_SHA}; durduruldu")
            sys.exit(5)
        spec = importlib.util.spec_from_file_location("q1_konsey_ayrisim_dondurulmus", DONDURULMUS)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _DM = mod
    return _DM


def yuzdelik(v):
    v = np.asarray(v, float)
    return {"ci90": [float(np.percentile(v, 5)), float(np.percentile(v, 95))],
            "ci95": [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]}


class Olcum:
    """Model duzeyi nokta ve bootstrap degerleri (dondurulmus model_duzeyi ile)."""

    def __init__(self, M, panel, B, tohum):
        dm = dondurulmus()
        self.M = M
        self.panel = panel
        self.g = dm.Alici(M)
        rng = np.random.default_rng(tohum)
        self.gb = dm.Alici(M, dm.bootstrap_agirlik(M.n, B, rng)) if B > 0 else None
        self.cache = {}

    def model(self, m):
        if m in self.cache:
            return self.cache[m]
        dm = dondurulmus()
        eks = dm.tam_panel_kapsami(self.M, m, self.panel)
        if eks:
            self.cache[m] = None
            return None
        try:
            nokta = dm.model_duzeyi(self.g, m, self.panel, "log", "yari")
        except KeyError as e:
            # panel uyesinin kendisi (or. ayna panelde tek XCiT kaldiginda) kendini cikarinca bos panel
            if "bos panel" in str(e):
                self.cache[m] = None
                return None
            raise
        d = {"sigma": float(nokta["sigma"]), "rho": float(nokta["rho"]), "S": float(nokta["S"]),
             "omega": float(nokta["omega"]), "w": float(np.exp(nokta["omega"])), "panel_n": nokta["panel_n"],
             "temiz": float(100.0 * self.M.h[(m, m)]["tc"].mean())}
        if self.gb is not None:
            b = dm.model_duzeyi(self.gb, m, self.panel, "log", "yari")
            d["_b"] = {k: np.asarray(b[k], float) for k in ("sigma", "rho", "omega")}
        self.cache[m] = d
        return d


def hucre_ozeti(O, tablo, hucre, dislanan=()):
    uyeler = [a for a, v in tablo["modeller"].items() if v["hucre"] == hucre and a in O.M.modeller()
              and a not in dislanan]
    deg = {a: O.model(a) for a in uyeler}
    deg = {a: v for a, v in deg.items() if v is not None}
    if not deg:
        return None
    out = {"uyeler": list(deg), "n": len(deg)}
    for k in ("sigma", "rho", "omega", "w", "temiz"):
        out[k] = float(np.mean([v[k] for v in deg.values()]))
    out["model"] = {a: {k: v[k] for k in ("sigma", "rho", "omega", "w", "temiz", "S")} for a, v in deg.items()}
    if O.gb is not None:
        out["_b"] = {k: np.mean([v["_b"][k] for v in deg.values()], axis=0) for k in ("sigma", "rho", "omega")}
    return out


def fark(h, isaretler, nicelik):
    """isaretler: [(+1, 'V-IN'), (-1, 'R224-IN'), ...] -> nokta ve aralik."""
    if any(h.get(c) is None for _, c in isaretler):
        return {"hesaplanamadi": [c for _, c in isaretler if h.get(c) is None]}
    nokta = sum(s * h[c][nicelik] for s, c in isaretler)
    out = {"kestirim": float(nokta)}
    if all("_b" in h[c] for _, c in isaretler):
        out.update(yuzdelik(sum(s * h[c]["_b"][nicelik] for s, c in isaretler)))
    return out


def temizle(x):
    if isinstance(x, dict):
        return {k: temizle(v) for k, v in x.items() if k != "_b"}
    if isinstance(x, list):
        return [temizle(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    return x


# --------------------------------------------------------------------------------------------------
# Blok kurallari (ek on kayit ile ayni esikler; 02_deney_adaylari.json)
# --------------------------------------------------------------------------------------------------
def kural_A(h):
    r = fark(h, [(1, "V-IN")], "rho")
    s = fark(h, [(1, "V-IN"), (-1, "R224-IN")], "sigma")
    out = {"rho_T_V_IN": r, "sigma_T_fark_VIN_eksi_R224IN": s,
           "ikincil_sifirdan": {"rho_T_V_scr": fark(h, [(1, "V-scr")], "rho"),
                                "sigma_T_fark_Vscr_eksi_R224scr": fark(h, [(1, "V-scr"), (-1, "R224-scr")], "sigma")}}
    if "kestirim" in r and "ci90" in r:
        k, (lo, hi) = r["kestirim"], r["ci90"]
        if k <= 0.10 and lo >= -0.10 and hi <= 0.10:
            et = "esdeger"
        elif k >= 0.15 and lo > 0.10:
            et = "yonlu_zayif"
        elif k <= -0.10 and hi < -0.10:
            et = "ters"
        else:
            et = "ara_bolge"
        out["rho_etiketi"] = et
    if "kestirim" in s and "ci90" in s:
        k, (lo, hi) = s["kestirim"], s["ci90"]
        if k >= 0 or (lo <= 0 <= hi and k >= -0.05):
            out["sigma_etiketi"] = "ayna"
        elif k < 0 and hi < 0:
            out["sigma_etiketi"] = "negatif"
        else:
            out["sigma_etiketi"] = "belirsiz"
    return out


def kural_B(h):
    out = {}
    v, r = h.get("V-scr+"), h.get("R224-scr")
    if v is None or r is None:
        return {"hesaplanamadi": ["V-scr+" if v is None else "R224-scr"]}
    dt, dw = v["temiz"] - r["temiz"], v["w"] - r["w"]
    out["eslesme"] = {"temiz_fark_puan": dt, "w_fark_puan": dw, "temiz_esik": 6.0, "w_esik": 2.0,
                      "temiz_tutuyor": abs(dt) <= 6.0, "w_tutuyor": abs(dw) <= 2.0, "tohum_n": v["n"]}
    s = fark(h, [(1, "V-scr+"), (-1, "R224-scr")], "sigma")
    out["sigma_fark_Vscrp_eksi_R224scr"] = s
    out["rho_fark_Vscrp_eksi_R224scr"] = fark(h, [(1, "V-scr+"), (-1, "R224-scr")], "rho")
    out["sigma_fark_Vscrp_eksi_Vscr"] = fark(h, [(1, "V-scr+"), (-1, "V-scr")], "sigma")
    k = s.get("kestirim")
    if k is None:
        return out
    if k <= -0.20:
        et = "H_mimari"
    elif k > -0.15:
        et = "H_yakinsama"
    else:
        et = "kismen"
    if out["eslesme"]["temiz_tutuyor"] and out["eslesme"]["w_tutuyor"] and v["n"] >= 2:
        out["karar"] = et
    else:
        out["karar"] = "betimsel (eslesme kosulu tutmadi ya da iki tohum yok); G blogu birincil okuma"
        out["etiket_bilgi_icin"] = et
    return out


def kural_C1(h):
    s = fark(h, [(1, "V-IN21k"), (-1, "V-IN")], "sigma")
    r = fark(h, [(1, "V-IN21k"), (-1, "V-IN")], "rho")
    out = {"sigma_fark_VIN21k_eksi_VIN": s, "rho_fark_VIN21k_eksi_VIN": r}
    if "kestirim" in s and "kestirim" in r:
        ds, dr = s["kestirim"], r["kestirim"]
        if ds >= 0.05 and dr <= -0.05:
            out["karar"] = "doz_yanit"
        elif abs(ds) < 0.05 and abs(dr) < 0.05:
            out["karar"] = "etkisiz"
        else:
            out["karar"] = "kismi"
        out["sigma_dustu"] = ds < 0
    return out


def kural_C2(h):
    s = fark(h, [(1, "R224-SWSL"), (-1, "R224-IN")], "sigma")
    e = fark(h, [(1, "V-IN21k"), (-1, "V-IN"), (-1, "R224-SWSL"), (1, "R224-IN")], "sigma")
    out = {"sigma_fark_SWSL_eksi_R224IN": s, "olcek_etkilesimi": e}
    if "kestirim" in s and "kestirim" in e:
        if abs(s["kestirim"]) <= 0.05 and e["kestirim"] > 0:
            out["karar"] = "ViT_ozgu"
        elif s["kestirim"] >= 0.10:
            out["karar"] = "iki_aile_yaklasir"
        else:
            out["karar"] = "ara"
    return out


G_HUCRELER = ["V-scr", "V-scr+", "V-IN", "V-IN21k", "R224-scr", "R224-IN", "R224-SWSL"]


def kural_G(h, mantel_yolu):
    xs, ys, aile, bs = [], [], [], []
    for c in G_HUCRELER:
        if h.get(c) is None:
            continue
        for a, v in h[c]["model"].items():
            xs.append(v["omega"])
            ys.append(v["sigma"])
            aile.append("V" if c.startswith("V") else "R")
    out = {"hucreler": [c for c in G_HUCRELER if h.get(c) is not None], "n_model": len(xs)}
    if len(xs) < 4 or "V" not in aile or "R" not in aile:
        out["hesaplanamadi"] = "yeterli model yok"
        return out
    X = np.column_stack([np.ones(len(xs)), xs])
    beta, *_ = np.linalg.lstsq(X, np.asarray(ys), rcond=None)
    art = np.asarray(ys) - X @ beta
    a_ = np.asarray(aile)
    d = float(art[a_ == "V"].mean() - art[a_ == "R"].mean())
    out.update({"egim": float(beta[1]), "kesisim": float(beta[0]), "artik_fark_V_eksi_R": d})
    # hucre ortalamalariyla (betimsel)
    hx = [h[c]["omega"] for c in out["hucreler"]]
    hy = [h[c]["sigma"] for c in out["hucreler"]]
    hb, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(hx)), hx]), np.asarray(hy), rcond=None)
    out["hucre_duzeyi"] = {"egim": float(hb[1]), "kesisim": float(hb[0])}
    out["mantel"] = None
    if mantel_yolu and Path(mantel_yolu).exists():
        mj = json.loads(Path(mantel_yolu).read_text(encoding="utf-8"))
        km = mj["sinamalar"]["kismi_omega"]
        out["mantel"] = {"dosya": mantel_yolu, "kismi_omega": km, "ham": mj["sinamalar"]["ham"]}
        ist, p = km.get("istatistik"), km.get("p_tek")
        pozitif = ist is not None and p is not None and ist > 0 and p < 0.05
        sifira_yakin = ist is not None and p is not None and p >= 0.05 and abs(ist) < 0.10
        if d <= -0.15 and pozitif:
            out["karar"] = "indirgenmez"
        elif d > -0.05 or sifira_yakin:
            out["karar"] = "gurbuzlukle_aciklanir"
        else:
            out["karar"] = "ara"
    return out


def g_bootstrap(O, tablo, out_g):
    """G regresyon artik farkinin goruntu bootstrap araligi (model duzeyi, ayni agirliklar)."""
    if O.gb is None or "egim" not in out_g:
        return
    oms, sgs, aile = [], [], []
    for c in out_g["hucreler"]:
        for a in [x for x, v in tablo["modeller"].items() if v["hucre"] == c]:
            d = O.model(a) if a in O.M.modeller() else None
            if d is None:
                continue
            oms.append(d["_b"]["omega"])
            sgs.append(d["_b"]["sigma"])
            aile.append("V" if c.startswith("V") else "R")
    om, sg, a_ = np.stack(oms), np.stack(sgs), np.asarray(aile)
    fb = []
    for b in range(om.shape[1]):
        X = np.column_stack([np.ones(om.shape[0]), om[:, b]])
        be, *_ = np.linalg.lstsq(X, sg[:, b], rcond=None)
        r = sg[:, b] - X @ be
        fb.append(r[a_ == "V"].mean() - r[a_ == "R"].mean())
    out_g["artik_fark_V_eksi_R_bootstrap"] = yuzdelik(fb)


def b118_yorunge(O, tablo):
    out = {}
    for m in O.M.modeller():
        eslesme = re.match(r"^(.+)_e(\d{3})$", m)  # ara kontrol noktasi takma adi <kosu>_eXXX
        if eslesme is None:
            continue
        kosu, ep = eslesme.group(1), eslesme.group(2)
        d = O.model(m)
        if d is None:
            continue
        hucre = tablo["modeller"].get(kosu, {}).get("hucre", "?")
        out.setdefault(kosu, {"hucre": hucre, "epoklar": {}})["epoklar"][int(ep)] = {
            k: d[k] for k in ("sigma", "rho", "omega", "w", "temiz")}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--blok", required=True, choices=["A", "B", "C1", "C2", "G", "B118"])
    ap.add_argument("--matris-dizini", action="append", required=True)
    ap.add_argument("--hucre-tablosu", default=str(KOK / "raporlar/konsey_2026-10-29/hucre_tablosu_curutme.json"))
    ap.add_argument("--bootstrap", type=int, default=2000)
    ap.add_argument("--tohum", type=int, default=TOHUM)
    ap.add_argument("--dislanan", nargs="*", default=[])
    ap.add_argument("--mantel", default=None, help="G: q1_ek_gradyan_kosinus.py mantel ciktisi (CKA)")
    ap.add_argument("--sinama", action="store_true", help="sahte ya da kisa veriyle boru hatti sinamasi")
    ap.add_argument("--cikti", required=True)
    a = ap.parse_args(argv)
    dm = dondurulmus()
    tablo = json.loads(Path(a.hucre_tablosu).read_text(encoding="utf-8"))
    M = dm.Matris()
    for d in a.matris_dizini:
        M.ekle(d)
    tut = M.tutarlilik()
    if a.blok == "A":
        panel = [x for x, v in tablo["modeller"].items() if v.get("ayna_panel") and x in M.modeller()]
    else:
        panel = [x for x, v in tablo["modeller"].items() if v.get("birincil_panel") and x in M.modeller()]
    O = Olcum(M, panel, a.bootstrap, a.tohum)
    hucreler = sorted({v["hucre"] for v in tablo["modeller"].values()} - {"panel", "ayna_panel"})

    def hepsi(dis):
        return {c: hucre_ozeti(O, tablo, c, dis) for c in hucreler}

    sonuc = {}
    for etiket, dis in [("tum_modeller", [])] + ([("b6_isaretliler_cikarilmis", a.dislanan)] if a.dislanan else []):
        h = hepsi(dis)
        if a.blok == "A":
            k = kural_A(h)
        elif a.blok == "B":
            k = kural_B(h)
        elif a.blok == "C1":
            k = kural_C1(h)
        elif a.blok == "C2":
            k = kural_C2(h)
        elif a.blok == "G":
            k = kural_G(h, a.mantel)
            g_bootstrap(O, tablo, k)
        else:
            k = {"yorunge": b118_yorunge(O, tablo)}
        sonuc[etiket] = {"hucreler": {c: v for c, v in h.items() if v is not None}, "blok_sonucu": k}

    out = {"meta": {"sarmalayici": "experiments/q1_curutme_cozumleme.py", "sarmalayici_sha256": sha256(__file__),
                    "dondurulmus_betik": "experiments/q1_konsey_ayrisim.py",
                    "dondurulmus_betik_sha256_dogrulandi": DONDURULMUS_SHA,
                    "hucre_tablosu": a.hucre_tablosu, "hucre_tablosu_sha256": sha256(a.hucre_tablosu),
                    "blok": a.blok, "panel": panel, "bootstrap": a.bootstrap, "tohum": a.tohum,
                    "kestirici": "bolunmus yari, log olcek (dondurulmus model_duzeyi)",
                    "matris_dizinleri": a.matris_dizini, "girdi_sha256": M.kaynaklar, "tutarlilik": tut,
                    "cakisma": M.cakisma, "dislanan": a.dislanan,
                    "uretildi_utc": datetime.now(timezone.utc).isoformat()},
           "sonuc": sonuc}
    if a.sinama:
        out["SINAMA_SONUC_DEGIL"] = True
    Path(a.cikti).parent.mkdir(parents=True, exist_ok=True)
    with io.open(a.cikti, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(dm.jsonla(temizle(out)), fh, ensure_ascii=False, indent=1)
    print("yazildi", a.cikti)
    return out


if __name__ == "__main__":
    main()
