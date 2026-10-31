# -*- coding: utf-8 -*-
"""Hakem paneli acik isleri A2, A9, A10 (31.10.2026; GPU gerekmez). Kesifsel, on kayit disi.

Neden ayri dosya: experiments/q1_ek_masa.py'nin sha256'si (40454344...) foyun M11 meta satirlarinda "dosyadan
hesaplanan ... AYNI" olarak basilir ve ONKAYIT_SAPMALAR.md'de S10-3 kod eki olarak sabitlenmistir. O dosyaya kip
eklemek M11'i "FARKLI" yapar ve kod eki kaydini bozar. Bu betik q1_ek_masa.py'yi ve dondurulmus cozumleme betigini
importlib ile, sha256 denetimiyle ve degistirmeden yukler.

  --mod turetilmis  A2: 2x2 (B4) basit etkiler ve turetilmis hucre farklari, sigma ve rho icin (bolunmus yari, log
                    birincil; logit duyarlilik). Araliklar: (i) dondurulmus karsitlik() ile dort hucre birlesik
                    varyansli t (df 5; H1-H3 ile ayni yontem), (ii) Welch, (iii) hiyerarsik bootstrap (dondurulmus
                    b4_coz RNG akisinin birebir kopyasi; H1-H3 araliklari dondurulmus JSON ile karsilastirilir),
                    (iv) yalniz goruntu bootstrap (kosular sabit). Hucre ici aralik yok (n = 2), hucre ortalamalari
                    betimsel. Yeni karsitliklar icin kesifsel Holm (aile: on kayitli karsiligi olmayan sekiz karsitlik).
                    A9: K-a icin 2q - 1 = (simetrik pay - yonlu pay)/D, CIFAR-10 (B2) ve CIFAR-100 (B9); dogrusal
                    donusum, araliklar uc noktalarin donusumu (t: dondurulmus JSON; hiyerarsik bootstrap: M11.1 JSON).
  --mod a10_panel   A10: hucre_tablosu.json'dan ResNet-18 turevi panel uyeleri cikarilmis hucre_tablosu_a10.json
                    (yalniz birincil_panel alani degisir; mimari RobustBench model nesnelerinden dogrulanir); dondurulmus
                    betik --mod b4 ve --mod b2 ile once varsayilan bayraklarla (ON_KAYIT §2 panel_en_az = 5 bekcisi),
                    sonra --panel-en-az 3 ile (betigin kendi istege bagli bayragi; betik degismez) cagrilir; ozet,
                    dondurulmus panelle karsilastirma ve importlib ile bagimsiz yeniden hesap a10_panel.json'a yazilir.

Hicbir sayi elle yazilmaz; her JSON girdi sha256'larini, yontem tanimini ve tohumu tasir.
Kullanim (konteyner, depo kokunden):
  python -B arsiv/b2_yardimci/_m12_ek_masa.py --mod turetilmis
  python -B arsiv/b2_yardimci/_m12_ek_masa.py --mod a10_panel
"""
import argparse
import copy
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy import stats

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

KOK = Path(__file__).resolve().parents[2]
EK_BETIK = "experiments/q1_ek_masa.py"
EK_SHA = "40454344bd3f8b1a0318d4bdb295d1dad05f187d74fe22f739501654a785b8c1"   # foy M11, sapma kaydi S10-3 kod eki
DONDURULMUS = "experiments/q1_konsey_ayrisim.py"
HT = "raporlar/konsey_2026-10-29/hucre_tablosu.json"
HT_SHA = "2a891331f8c59897db14b30fb27a46c836ad391957aa4ff54a0ffef00bfe5500"   # B2/B4 meta.hucre_tablosu_sha256
HT_A10 = "raporlar/konsey_2026-10-29/hucre_tablosu_a10.json"
J4 = "results/q1/konsey_ayrisim_b4.json"
J2 = "results/q1/konsey_ayrisim_b2.json"
J9 = "results/q1/konsey_b9_c100/b9_dondurulmus_b2.json"
BS = {"cifar10": "results/q1/konsey_ek_masa/bootstrap_cifar10.json",
      "cifar100": "results/q1/konsey_ek_masa/bootstrap_cifar100.json"}
B4_MATRIS = "results/q1/konsey_b4_matris"
B2_MATRIS = "results/q1/konsey_b2_panel"
CIKTI = "results/q1/konsey_ek_masa"
R18_BEKLENEN = ["Wong2020Fast", "Sehwag2021Proxy_R18", "Addepalli2022Efficient_RN18", "Rade2021Helper_R18_ddpm"]
ETIKET_A2 = "kesifsel, on kayit disi (31.10.2026, hakem paneli acik isi A2; turetilmis karsitliklar)"
ETIKET_A9 = "turetilmis (31.10.2026, hakem paneli acik isi A9; 2q - 1, K-a'nin dogrusal donusumu)"
ETIKET_A10 = "kesifsel, on kayit disi panel, 3 uye (31.10.2026, hakem paneli acik isi A10)"


def sha256(yol):
    h = hashlib.sha256()
    p = Path(yol) if Path(yol).is_absolute() else KOK / yol
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def oku(yol):
    return json.loads((KOK / yol).read_text(encoding="utf-8"))


def ek_modul():
    s = sha256(EK_BETIK)
    if s != EK_SHA:
        raise SystemExit(f"{EK_BETIK} sha256 {s} != {EK_SHA}; durduruldu")
    spec = importlib.util.spec_from_file_location("q1_ek_masa_kutuphane", KOK / EK_BETIK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


EK = ek_modul()
DM = EK.dondurulmus()          # dondurulmus betik, sha256 4bce2c98... denetimli


def meta_temel(a, ek=None):
    m = {"betik": "arsiv/b2_yardimci/_m12_ek_masa.py", "betik_sha256": sha256(Path(__file__).resolve()),
         "kutuphane_betik": EK_BETIK, "kutuphane_betik_sha256_dogrulandi": EK_SHA,
         "dondurulmus_betik": DONDURULMUS, "dondurulmus_betik_sha256_dogrulandi": EK.DONDURULMUS_SHA,
         "mod": a.mod, "uretildi_utc": datetime.now(timezone.utc).isoformat(), "numpy": np.__version__,
         "scipy": __import__("scipy").__version__, "argv": sys.argv[1:]}
    if ek:
        m.update(ek)
    return m


def yaz(yol, obj):
    p = KOK / yol
    p.parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(DM.jsonla(obj), fh, ensure_ascii=False, indent=1)
    print("yazildi:", yol)


def mf(a, b):
    return EK.maks_fark(a, b)


def matris(dz, tablo):
    """Dondurulmus main() ile ayni yukleme (dizin_takma_ad_esleme varsa)."""
    M = DM.Matris()
    esl_tum = tablo.get("dizin_takma_ad_esleme", {})
    key = str(dz).replace("\\", "/").rstrip("/")
    esl = next((v for k, v in esl_tum.items() if key.endswith(k.rstrip("/"))), None)
    M.ekle(dz, esl)          # goreli yol; cwd depo koku olmali (dondurulmus cagriyla ayni sha anahtarlari)
    return M


# ==============================================================================================
# A2: 2x2 basit etkiler ve turetilmis farklar
# ==============================================================================================
KONTR = {
    "mimari_scr": ({"V-scr": 1.0, "R224-scr": -1.0}, "V-scr - R224-scr (sifirdan baslatmada mimari basit etkisi)"),
    "mimari_IN": ({"V-IN": 1.0, "R224-IN": -1.0}, "V-IN - R224-IN (ImageNet baslatmada mimari basit etkisi)"),
    "baslatma_V": ({"V-IN": 1.0, "V-scr": -1.0}, "V-IN - V-scr (ViT'te baslatma basit etkisi)"),
    "baslatma_R224": ({"R224-IN": 1.0, "R224-scr": -1.0}, "R224-IN - R224-scr (ResNet-224'te baslatma basit etkisi)"),
    "etkilesim": ({"V-IN": 1.0, "V-scr": -1.0, "R224-IN": -1.0, "R224-scr": 1.0},
                  "(V-IN - V-scr) - (R224-IN - R224-scr) = mimari_IN - mimari_scr"),
    "mimari_ana_etki": ({"V-scr": 0.5, "R224-scr": -0.5, "V-IN": 0.5, "R224-IN": -0.5},
                        "1/2 (mimari_scr + mimari_IN), baslatma uzerinden ortalanmis mimari etkisi"),
}
ON_KAYITLI = {("sigma", "mimari_scr"): "H1 (F_B4)", ("sigma", "etkilesim"): "H2 (F_B4)",
              ("rho", "mimari_ana_etki"): "H3 (F_B4)", ("rho", "baslatma_V"): "S2 (ikincil, ON_KAYIT §5)"}
J4_ANAHTAR = {("sigma", "mimari_scr"): ("F_B4", "H1"), ("sigma", "etkilesim"): ("F_B4", "H2"),
              ("rho", "mimari_ana_etki"): ("F_B4", "H3"), ("rho", "baslatma_V"): ("ikincil", "S2")}

A2_TANIM = (
    "Model duzeyi sigma ve rho dondurulmus model_duzeyi() ile (bolunmus yari, log olcek, birincil panel P, 7 uye) "
    "hesaplanir; hucreler dondurulmus hucre_uyeleri() ile (V-scr 3, V-IN 2, R224-scr 2, R224-IN 2 kosu). Karsitlik "
    "katsayilari KONTR sozlugundedir. (i) Birlesik varyansli t: dondurulmus karsitlik(deger, katsayi, HUC4); varyans "
    "dort hucreden birlestirilir (df = 1 + 1 + 1 + 2 = 5), H1-H3 ile ayni yontem; p_iki iki yonlu t. (ii) Welch: ayni "
    "islevin welch alani (yalniz katsayisi sifir olmayan hucreler). (iii) Hiyerarsik bootstrap: dondurulmus b4_coz() "
    "akisinin birebir kopyasi (rng = default_rng(BOOT_TOHUM = 20261029); once goruntu agirliklari W = "
    "bootstrap_agirlik(n, 2000, rng); her kopyada HUC4 sirasinda hucre icinde kosular yerine koyarak cekilir); yuzdelik "
    "%90 (5-95) ve %95 (2,5-97,5). H1, H2, H3 araliklari dondurulmus JSON'un duyarlilik.hiyerarsik_bootstrap alaniyla "
    "karsilastirilir. (iv) Yalniz goruntu bootstrap: ayni W, kosular sabit (hucre ortalamasi butun kosular). "
    "Standartlastirilmis etki = kestirim / birlesik SD. Kesifsel Holm: on kayitli karsiligi olmayan karsitliklarin iki "
    "yonlu birlesik varyans p'leri (sigma: mimari_IN, baslatma_V, baslatma_R224, mimari_ana_etki; rho: mimari_scr, "
    "mimari_IN, baslatma_R224, etkilesim). Hucre ici aralik verilmez (hucre basina n = 2; V-scr 3); hucre ortalamalari "
    "betimseldir. Logit olcek duyarliligi ayni karsitliklarin birlesik varyansli t kestirimidir.")


def a2_hesap(a):
    tablo = DM.tablo_oku(KOK / HT)
    if sha256(HT) != HT_SHA:
        raise SystemExit("hucre_tablosu.json degismis")
    J = oku(J4)
    if J["meta"]["betik_sha256"] != EK.DONDURULMUS_SHA or J["meta"]["hucre_tablosu_sha256"] != HT_SHA:
        raise SystemExit("B4 JSON baska betik ya da tablo surumuyle uretilmis")
    M = matris(B4_MATRIS, tablo)
    mevcut = set(M.modeller())
    P, P2, eksik = DM.paneller(tablo, mevcut)
    if P != J["panel"]["birincil"]:
        raise SystemExit(f"panel uyusmuyor {P}")
    hucre = {h: DM.hucre_uyeleri(tablo, h, mevcut) for h in DM.HUC4}
    if hucre != J["b4"]["hucreler"]:
        raise SystemExit("hucre uyeleri uyusmuyor")
    g = DM.Alici(M)
    sig, rho, om = DM.b4_degerler(g, hucre, P)
    sigL, rhoL, _ = DM.b4_degerler(g, hucre, P, "yari", "logit")
    Fd = J["b4"]["F_B4"]["degerler"]
    dog = {"sigma_degerler": max(mf(sig[h], Fd["sigma"][h]) for h in DM.HUC4),
           "rho_degerler": max(mf(rho[h], Fd["rho"][h]) for h in DM.HUC4)}
    deger = {"sigma": sig, "rho": rho}
    degerL = {"sigma": sigL, "rho": rhoL}
    out_k = {}
    for nic in ("sigma", "rho"):
        out_k[nic] = {}
        for ad, (kat, tanim) in KONTR.items():
            k = DM.karsitlik(deger[nic], kat, DM.HUC4)
            kL = DM.karsitlik(degerL[nic], kat, DM.HUC4)
            kay = {"tanim": tanim, "katsayi": kat, "kestirim": k["kestirim"], "hucre_ort": k["hucre_ort"],
                   "hucre_n": k["hucre_n"], "se": k["se"], "df": k["df"], "sp_birlesik": k["sp_birlesik"],
                   "ci90": k.get("ci90"), "ci95": k.get("ci95"), "p_iki": k.get("p_iki"),
                   "standart_etki_kestirim_bolu_sp": k["kestirim"] / k["sp_birlesik"] if k["sp_birlesik"] > 0 else None,
                   "welch": k.get("welch"),
                   "logit_duyarlilik": {"kestirim": kL["kestirim"], "ci90": kL.get("ci90"), "ci95": kL.get("ci95"),
                                        "p_iki": kL.get("p_iki")},
                   "on_kayitli_karsiligi": ON_KAYITLI.get((nic, ad), "yok (yeni, kesifsel)")}
            if (nic, ad) in J4_ANAHTAR:
                blok, hk = J4_ANAHTAR[(nic, ad)]
                ref = J["b4"][blok]["karsitliklar"][hk] if blok == "F_B4" else J["b4"]["ikincil"][hk]
                kay["dondurulmus_json_maks_fark"] = max(mf(k["kestirim"], ref["kestirim"]), mf(k["ci90"], ref["ci90"]),
                                                        mf(k["ci95"], ref["ci95"]))
            out_k[nic][ad] = kay
    # ---- hiyerarsik bootstrap: dondurulmus b4_coz RNG akisi
    B = a.B
    rng = np.random.default_rng(DM.BOOT_TOHUM)
    W = DM.bootstrap_agirlik(M.n, B, rng)
    gb = DM.Alici(M, W)
    sb, rb, _ = DM.b4_degerler(gb, hucre, P)
    vb = {"sigma": sb, "rho": rb}
    dist = {nic: {ad: np.empty(B) for ad in KONTR} for nic in vb}
    for b in range(B):
        sec = {h: rng.integers(0, len(hucre[h]), len(hucre[h])) for h in DM.HUC4}
        for nic in vb:
            ms = {h: float(np.mean([vb[nic][h][i][b] for i in sec[h]])) for h in DM.HUC4}
            for ad, (kat, _) in KONTR.items():
                dist[nic][ad][b] = sum(c * ms[h] for h, c in kat.items())
    # ---- yalniz goruntu bootstrap (kosular sabit; RNG kullanmaz)
    gdist = {nic: {} for nic in vb}
    for nic in vb:
        hm = {h: np.mean(np.vstack([np.asarray(x) for x in vb[nic][h]]), axis=0) for h in DM.HUC4}
        for ad, (kat, _) in KONTR.items():
            gdist[nic][ad] = sum(c * hm[h] for h, c in kat.items())
    bref = J["b4"]["duyarlilik"]["hiyerarsik_bootstrap"]
    b_dog = {}
    for nic in vb:
        for ad in KONTR:
            h90, h95 = EK.yuzdelik(dist[nic][ad])
            g90, g95 = EK.yuzdelik(gdist[nic][ad])
            k_ = out_k[nic][ad]
            k_["hiyerarsik_bootstrap"] = {"B": B, "ci90": h90, "ci95": h95, "sd": float(np.std(dist[nic][ad], ddof=1)),
                                          "iki_yonlu_p_isaret": float(min(1.0, 2 * min(
                                              (1 + (dist[nic][ad] <= 0).sum()) / (B + 1),
                                              (1 + (dist[nic][ad] >= 0).sum()) / (B + 1))))}
            k_["yalniz_goruntu_bootstrap"] = {"B": B, "ci90": g90, "ci95": g95,
                                              "sd": float(np.std(gdist[nic][ad], ddof=1))}
    for (nic, ad), (blok, hk) in J4_ANAHTAR.items():
        if blok == "F_B4":
            k_ = out_k[nic][ad]["hiyerarsik_bootstrap"]
            b_dog[hk] = max(mf(k_["ci90"], bref[hk]["ci90"]), mf(k_["ci95"], bref[hk]["ci95"]))
    # ---- kesifsel Holm (yeni karsitliklar)
    yeni = [(nic, ad) for nic in ("sigma", "rho") for ad in KONTR if (nic, ad) not in ON_KAYITLI]
    p_yeni = [out_k[nic][ad]["p_iki"] for nic, ad in yeni]
    adj = DM.holm(p_yeni)
    for (nic, ad), pa in zip(yeni, adj):
        out_k[nic][ad]["p_holm_kesifsel_aile"] = pa
    # ---- hucre ozetleri (betimsel)
    hoz = {}
    for nic, d in (("sigma", sig), ("rho", rho), ("omega", om)):
        hoz[nic] = {h: {"degerler": d[h], "n": len(d[h]), "ort": float(np.mean(d[h])),
                        "sd": float(np.std(d[h], ddof=1)) if len(d[h]) > 1 else None,
                        "aralik": "aralik yok, betimsel (hucre ici n = %d)" % len(d[h])} for h in DM.HUC4}
    girdi = dict(M.kaynaklar)
    for p_ in (J4, HT, DONDURULMUS, EK_BETIK):
        girdi[p_] = sha256(p_)
    return {
        "etiket": ETIKET_A2, "tanim": A2_TANIM,
        "meta_ek": {"veri": "cifar10", "blok": "B4", "matris_dizini": B4_MATRIS, "hucre_tablosu": HT,
                    "dondurulmus_cikti": J4, "B": B, "bootstrap_tohum": int(DM.BOOT_TOHUM),
                    "tohum_kaynagi": "dondurulmus betigin BOOT_TOHUM sabiti; RNG akisi dondurulmus b4_coz ile ayni",
                    "n_goruntu": M.n, "panel": P, "girdi_sha256": girdi},
        "hucreler": hucre, "hucre_ozetleri": hoz, "karsitliklar": out_k,
        "kesifsel_holm": {"aile": [f"{n}.{a_}" for n, a_ in yeni], "p_ham": p_yeni, "p_holm": adj},
        "dogrulama": {"model_duzeyi_dondurulmus_json_maks_fark": dog,
                      "on_kayitli_karsitliklar_dondurulmus_json_maks_fark":
                          {f"{n}.{a_}": out_k[n][a_]["dondurulmus_json_maks_fark"] for n, a_ in J4_ANAHTAR},
                      "hiyerarsik_bootstrap_H1_H3_dondurulmus_json_maks_fark": b_dog,
                      "tutarlilik": M.tutarlilik(), "cakismalar": M.cakisma},
    }


# ==============================================================================================
# A9: 2q - 1
# ==============================================================================================
A9_TANIM = (
    "q_s = simetrik_pay_s / D_s (K-a, dondurulmus F_B2). 1 - q_s yonlu payin D'deki payidir (ozdeslik D = simetrik + "
    "yonlu). 2q - 1 = (simetrik pay - yonlu pay)/D: simetrik payin yonlu payi D cinsinden asma orani; q = 0,5 (K-a'nin "
    "sifir hipotezi) 2q - 1 = 0'a karsilik gelir. Ortalama: 2 ort(q) - 1. Dogrusal donusum oldugundan t araliklari "
    "(dondurulmus F_B2.K-a.sinama.ci90/ci95) ve hiyerarsik bootstrap yuzdelik araliklari (M11.1, K-a.bootstrap) uc "
    "noktalarin 2x - 1 donusumudur; p degerleri K-a'nin p'leriyle aynidir. Denetim: kosu basina (simetrik - yonlu)/D "
    "ile 2q - 1 arasindaki en buyuk fark.")


def a9_hesap():
    out = {}
    girdi = {}
    for veri, yol in (("cifar10", J2), ("cifar100", J9)):
        J = oku(yol)
        bs = oku(BS[veri])
        girdi[yol] = sha256(yol)
        girdi[BS[veri]] = sha256(BS[veri])
        if J["meta"]["betik_sha256"] != EK.DONDURULMUS_SHA:
            raise SystemExit(f"{yol} baska betik surumu")
        if bs["meta"]["dondurulmus_cikti"] != yol:
            raise SystemExit(f"{BS[veri]} baska dondurulmus ciktiya bagli")
        ka = J["b2"]["F_B2"]["K-a"]
        q = np.asarray(ka["q"], float)
        D = np.asarray(ka["D"], float)
        sp = np.asarray(ka["simetrik_pay"], float)
        yp = np.asarray(ka["yonlu_pay"], float)
        s = ka["sinama"]
        dq = 2 * q - 1
        dogrudan = (sp - yp) / D

        def don(x):
            return None if x is None else [2 * x[0] - 1, 2 * x[1] - 1]
        out[veri] = {
            "kaynak": yol, "kaynak_anahtar": "b2.F_B2.K-a.{q, D, simetrik_pay, yonlu_pay, sinama.ort, sinama.ci90, "
                                            "sinama.ci95, p_tek_H0_q_le_0.5, ciftler}",
            "bootstrap_kaynak": BS[veri], "bootstrap_anahtar": "K-a.{nokta_ort_q, bootstrap.ci90, bootstrap.ci95}",
            "ciftler": ka["ciftler"], "q_s": q.tolist(), "iki_q_eksi_1_s": dq.tolist(),
            "ort_q": s["ort"], "iki_ort_q_eksi_1": 2 * s["ort"] - 1,
            "t_ci90": don(s.get("ci90")), "t_ci95": don(s.get("ci95")),
            "bootstrap_ci90": don(bs["K-a"]["bootstrap"]["ci90"]), "bootstrap_ci95": don(bs["K-a"]["bootstrap"]["ci95"]),
            "p_tek_H0_2q_eksi_1_le_0_(K-a ile ayni)": ka["p_tek_H0_q_le_0.5"],
            "denetim": {"kosu_basina_(simetrik-yonlu)/D_ile_2q-1_maks_fark": mf(dogrudan, dq),
                        "ozdeslik_artik_max_(dondurulmus)": ka["ozdeslik_artik_max"],
                        "bootstrap_nokta_ort_q_ile_dondurulmus_ort_fark": abs(bs["K-a"]["nokta_ort_q"] - s["ort"]),
                        "ort_2q-1_ile_2ort-1_fark": abs(float(dq.mean()) - (2 * s["ort"] - 1))}}
    return {"etiket": ETIKET_A9, "tanim": A9_TANIM, "veri": out, "girdi_sha256": girdi}


def turetilmis_kos(a):
    a2 = a2_hesap(a)
    me = a2.pop("meta_ek")
    a2["meta"] = meta_temel(a, me)
    yaz(f"{CIKTI}/a2_basit_etkiler.json", a2)
    a9 = a9_hesap()
    a9["meta"] = meta_temel(a, {"girdi_sha256": a9.pop("girdi_sha256")})
    yaz(f"{CIKTI}/a9_2q_eksi_1.json", a9)
    for nic in ("sigma", "rho"):
        for ad, k in a2["karsitliklar"][nic].items():
            print(nic, ad, round(k["kestirim"], 4), [round(x, 4) for x in k["ci90"]],
                  [round(x, 4) for x in k["hiyerarsik_bootstrap"]["ci90"]])
    print("dogrulama", json.dumps(DM.jsonla(a2["dogrulama"]), ensure_ascii=False)[:600])
    for v, d in a9["veri"].items():
        print(v, d["iki_ort_q_eksi_1"], d["t_ci90"], d["bootstrap_ci90"], d["denetim"])


# ==============================================================================================
# A10: ResNet-18 turevleri cikarilmis panel
# ==============================================================================================
R18_BLOK = {"BasicBlock", "PreActBlock", "_PreActBlock", "_Block"}   # iki evrisimli artik bloklar
TUM_BLOK = R18_BLOK | {"Bottleneck", "PreActBottleneck"}
A10_TANIM = (
    "Panel uyesi 'ResNet-18 turevi' sayilir eger RobustBench (cifar10, Linf) model nesnesindeki iki evrisimli artik blok "
    "sayisi 8 ise (BasicBlock, PreActBlock, _PreActBlock; ResNet-18 ve PreAct-ResNet-18'in [2, 2, 2, 2] dizilimi). "
    "Nesneler robustbench.model_zoo.cifar10.linf sozlugunden CPU'da kurulur (agirlik yuklenmez); blok sinifi ve sayisi, "
    "Conv2d sayisi ve parametre sayisi kaydedilir. hucre_tablosu_a10.json dondurulmus tablonun kopyasidir; yalniz bu "
    "uyelerin birincil_panel alani false yapilir ve belgeleme icin 'a10_kesifsel' anahtari eklenir (dondurulmus betik "
    "bu anahtari okumaz). Dondurulmus betik degistirilmeden alt surecle cagrilir: once runbook bicimiyle (varsayilan "
    "--panel-en-az 5), sonra betigin istege bagli --panel-en-az 3 bayragiyla. ON_KAYIT §2'nin en az bes uyelik panel "
    "kurali bu ikinci cagrida bilerek gevsetilmistir; sonuclar on kayit disi ve kesifseldir, F_B2/F_B4 kararlarinin "
    "yerine gecmez. Dondurulmus panelle karsilastirmada 'ayni_yon' kestirim isaretinin, 'karar_ayni' karar dizgesinin "
    "aynen tutmasidir. Bagimsiz denetim: dondurulmus islevler importlib ile yuklenip 3 uyeli panelle H1-H3 kestirimleri "
    "ve K-a q, K-b rho yeniden hesaplanir ve alt surec ciktisiyla karsilastirilir.")


def mimari_dogrula():
    try:
        import torch  # noqa: F401
        from robustbench.model_zoo.cifar10 import linf
        import robustbench
    except Exception as e:  # pragma: no cover
        return {"hata": f"robustbench yuklenemedi: {e!r}"}
    tablo = oku(HT)
    panel = [m for m, v in tablo["modeller"].items() if v.get("birincil_panel")]
    linf = dict(linf)
    out = {}
    for m in panel:
        if m not in linf:
            out[m] = {"hata": "RobustBench cifar10 Linf kaydinda yok"}
            continue
        net = linf[m]["model"]()
        bloklar = [type(x).__name__ for x in net.modules() if type(x).__name__ in TUM_BLOK]
        out[m] = {"sinif": type(net).__name__, "mro": [c.__name__ for c in type(net).__mro__][:4],
                  "blok_siniflari": sorted(set(bloklar)), "blok_sayisi": len(bloklar),
                  "conv2d_sayisi": sum(1 for x in net.modules() if type(x).__name__ == "Conv2d"),
                  "parametre_sayisi": int(sum(p.numel() for p in net.parameters())),
                  "resnet18_turevi": bool(len(bloklar) == 8 and set(bloklar) <= R18_BLOK)}
        del net
    return {"robustbench_surum": getattr(robustbench, "__version__", None) or "bilinmiyor",
            "robustbench_dizin": str(Path(robustbench.__file__).parent), "kaynak": "robustbench.model_zoo.cifar10.linf",
            "modeller": out}


def a10_tablo(mim):
    t = json.loads((KOK / HT).read_text(encoding="utf-8"))
    r18 = [m for m, v in mim["modeller"].items() if v.get("resnet18_turevi")]
    if sorted(r18) != sorted(R18_BEKLENEN):
        raise SystemExit(f"mimari dogrulama beklenen listeyi vermedi: {r18}")
    t2 = copy.deepcopy(t)
    for m in r18:
        t2["modeller"][m]["birincil_panel"] = False
    kalan = [m for m, v in t2["modeller"].items() if v.get("birincil_panel")]
    t2["a10_kesifsel"] = {
        "etiket": ETIKET_A10, "kaynak_tablo": HT, "kaynak_tablo_sha256": sha256(HT),
        "degisen_alan": "modeller.<uye>.birincil_panel (true -> false)", "cikarilan": r18, "kalan_birincil_panel": kalan,
        "mimari_kaynagi": "robustbench.model_zoo.cifar10.linf model nesneleri (arsiv/b2_yardimci/_m12_ek_masa.py)",
        "uretildi": "31.10.2026, hakem paneli acik isi A10; ON_KAYIT §2 en az 5 uye kurali disinda"}
    # yalniz birincil_panel degisti mi
    fark = []
    for k in set(t) | set(t2):
        if k == "a10_kesifsel":
            continue
        if k != "modeller" and t.get(k) != t2.get(k):
            fark.append(k)
    for m in set(t["modeller"]) | set(t2["modeller"]):
        a_, b_ = t["modeller"].get(m), t2["modeller"].get(m)
        if a_ is None or b_ is None:
            fark.append(f"modeller.{m} (eksik)")
            continue
        for kk in set(a_) | set(b_):
            if a_.get(kk) != b_.get(kk):
                fark.append(f"modeller.{m}.{kk}")
    p = KOK / HT_A10
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(t2, fh, ensure_ascii=False, indent=1)
    print("yazildi:", HT_A10)
    return t2, r18, kalan, sorted(fark)


def dondurulmus_cagir(mod, matris_dz, cikti, panel_en_az=None):
    kom = [sys.executable, "-B", DONDURULMUS, "--mod", mod, "--matris-dizini", matris_dz,
           "--hucre-tablosu", HT_A10, "--cikti", cikti]
    if panel_en_az is not None:
        kom += ["--panel-en-az", str(panel_en_az)]
    s = subprocess.run(kom, cwd=str(KOK), capture_output=True, text=True)
    return {"komut": " ".join(["python"] + kom[1:]), "donus_kodu": s.returncode,
            "stdout_son": s.stdout.strip().splitlines()[-3:], "stderr_son": s.stderr.strip().splitlines()[-5:],
            "cikti": cikti, "cikti_sha256": sha256(cikti) if (KOK / cikti).exists() else None}


def aralik(x):
    return None if x is None else [float(x[0]), float(x[1])]


def b4_ozet(J):
    F = J["b4"]["F_B4"]
    k = F["karsitliklar"]
    hb = J["b4"]["duyarlilik"]["hiyerarsik_bootstrap"]
    return {h: {"kestirim": k[h]["kestirim"], "ci90": aralik(k[h].get("ci90")), "ci95": aralik(k[h].get("ci95")),
                "se": k[h].get("se"), "df": k[h].get("df"), "hucre_ort": k[h]["hucre_ort"],
                "p_ham": F["p_ham"][i], "p_holm": F["p_holm"][i], "karar": F["karar"][h],
                "hiyerarsik_bootstrap_ci90": hb[h]["ci90"], "welch_ci90": (k[h].get("welch") or {}).get("ci90")}
            for i, h in enumerate(("H1", "H2", "H3"))} | {
        "sonuc_bolgesi": F["karar"]["sonuc_bolgesi"], "O4_niteleme": F["karar"]["O4_niteleme"],
        "H2_logit_kestirim": F["karar"]["H2_logit_kestirim"],
        "delta_0.06": {h: J["b4"]["duyarlilik"]["delta_0.06"][h] for h in ("H1", "H2", "H3")},
        "S2_rho_VIN_eksi_Vscr": {"kestirim": J["b4"]["ikincil"]["S2"]["kestirim"],
                                 "ci90": aralik(J["b4"]["ikincil"]["S2"].get("ci90"))},
        "panel_jackknife": J["b4"]["duyarlilik"]["panel_jackknife"]}


def b2_ozet(J):
    F = J["b2"]["F_B2"]
    ka, kb, kc = F["K-a"], F["K-b"], F["K-c"]
    return {"K-a": {"q_s": ka["q"], "D_s": ka["D"], "ort_q": ka["sinama"]["ort"], "ci90": aralik(ka["sinama"].get("ci90")),
                    "ci95": aralik(ka["sinama"].get("ci95")), "p_tek_H0_q_le_0.5": ka["p_tek_H0_q_le_0.5"],
                    "payda_kucuk_tohumlar": ka["payda_kucuk_tohumlar"], "karar": F["karar"]["K-a"]},
            "K-b": {"rho_s": kb["degerler"], "ort_rho_Vscr": kb["ort"], "ci90": aralik(kb.get("ci90")),
                    "ci95": aralik(kb.get("ci95")), "tost_p": kb.get("tost_p"), "karar": F["karar"]["K-b"],
                    "ham_ci90_delta_icinde": F["karar"].get("K-b_ham_ci90_delta_icinde")},
            "K-c": {"Delta_w": kc.get("Delta_w"), "bootstrap_ci90": aralik((kc.get("bootstrap") or {}).get("ci90")),
                    "p_tek_H0_Delta_le_0": kc.get("p_tek_H0_Delta_le_0"), "karar": F["karar"]["K-c"]},
            "p_ham": F["p_ham"], "p_holm": F["p_holm"],
            "delta_0.06_karar": {s: F["duyarlilik_delta_0.06"]["karar"][s] for s in ("K-a", "K-b", "K-c")}}


def isaret(x):
    return 0 if x is None else int(np.sign(x))


def a10_kos(a):
    mim = mimari_dogrula()
    if "hata" in mim:
        raise SystemExit(mim["hata"])
    t2, r18, kalan, fark = a10_tablo(mim)
    if any(not f.endswith(".birincil_panel") for f in fark):
        raise SystemExit(f"tabloda birincil_panel disinda fark: {fark}")
    cag = {
        "b4_varsayilan": dondurulmus_cagir("b4", B4_MATRIS, f"{CIKTI}/a10_b4_varsayilan_bekci.json"),
        "b2_varsayilan": dondurulmus_cagir("b2", B2_MATRIS, f"{CIKTI}/a10_b2_varsayilan_bekci.json"),
        "b4": dondurulmus_cagir("b4", B4_MATRIS, f"{CIKTI}/a10_b4.json", 3),
        "b2": dondurulmus_cagir("b2", B2_MATRIS, f"{CIKTI}/a10_b2.json", 3),
    }
    for k, v in cag.items():
        print(k, v["donus_kodu"], v["stdout_son"], v["stderr_son"])
        if v["donus_kodu"] != 0:
            raise SystemExit(f"dondurulmus betik {k} cagrisi basarisiz: {v['stderr_son']}")
    bekci = {k: oku(cag[k]["cikti"]).get("hata") for k in ("b4_varsayilan", "b2_varsayilan")}
    A4, A2_ = oku(cag["b4"]["cikti"]), oku(cag["b2"]["cikti"])
    for J_ in (A4, A2_):
        if "hata" in J_ or J_["meta"]["hucre_tablosu_sha256"] != sha256(HT_A10) or \
                J_["meta"]["betik_sha256"] != EK.DONDURULMUS_SHA or J_["panel"]["birincil"] != kalan:
            raise SystemExit("a10 ciktisi beklenen tablo/betik/panel ile uretilmemis")
    F4, F2 = oku(J4), oku(J2)
    y4, d4 = b4_ozet(A4), b4_ozet(F4)
    y2, d2 = b2_ozet(A2_), b2_ozet(F2)
    kars = {}
    for h in ("H1", "H2", "H3"):
        kars[h] = {"dondurulmus_kestirim": d4[h]["kestirim"], "a10_kestirim": y4[h]["kestirim"],
                   "ayni_yon": isaret(d4[h]["kestirim"]) == isaret(y4[h]["kestirim"]),
                   "dondurulmus_karar": d4[h]["karar"], "a10_karar": y4[h]["karar"],
                   "karar_ayni": d4[h]["karar"] == y4[h]["karar"]}
    kars["sonuc_bolgesi"] = {"dondurulmus": d4["sonuc_bolgesi"], "a10": y4["sonuc_bolgesi"],
                             "ayni": d4["sonuc_bolgesi"] == y4["sonuc_bolgesi"]}
    for s, an in (("K-a", "ort_q"), ("K-b", "ort_rho_Vscr"), ("K-c", "Delta_w")):
        kars[s] = {"dondurulmus_kestirim": d2[s][an], "a10_kestirim": y2[s][an],
                   "ayni_yon": isaret(d2[s][an]) == isaret(y2[s][an]) if s != "K-a" else
                   isaret(d2[s][an] - 0.5) == isaret(y2[s][an] - 0.5),
                   "ayni_yon_tanimi": "q - 0,5 isareti" if s == "K-a" else "kestirim isareti",
                   "dondurulmus_karar": d2[s]["karar"], "a10_karar": y2[s]["karar"],
                   "karar_ayni": d2[s]["karar"] == y2[s]["karar"]}
    # ---- bagimsiz yeniden hesap (importlib ile dondurulmus islevler, 3 uyeli panel)
    tablo = DM.tablo_oku(KOK / HT_A10)
    M4 = matris(B4_MATRIS, tablo)
    P3, _, _ = DM.paneller(tablo, set(M4.modeller()))
    hucre = {h: DM.hucre_uyeleri(tablo, h, set(M4.modeller())) for h in DM.HUC4}
    g4 = DM.Alici(M4)
    s_, r_, _ = DM.b4_degerler(g4, hucre, P3)
    kk = DM.b4_karsitliklar(s_, r_)
    M2 = matris(B2_MATRIS, tablo)
    g2 = DM.Alici(M2)
    V = DM.hucre_uyeleri(tablo, "V-scr", set(M2.modeller()))
    cf = [tuple(c) for c in tablo["b2_tohum_ciftleri"]]
    ka, rhoV = DM.ka_kb(g2, cf, V, P3)
    bag = {"panel": P3,
           "H_kestirim_maks_fark": max(mf(kk[h]["kestirim"], y4[h]["kestirim"]) for h in ("H1", "H2", "H3")),
           "H_ci90_maks_fark": max(mf(kk[h]["ci90"], y4[h]["ci90"]) for h in ("H1", "H2", "H3")),
           "K-a_q_maks_fark": mf(ka["q"], y2["K-a"]["q_s"]), "K-b_rho_maks_fark": mf(rhoV, y2["K-b"]["rho_s"])}
    girdi = {HT: sha256(HT), HT_A10: sha256(HT_A10), J4: sha256(J4), J2: sha256(J2), DONDURULMUS: sha256(DONDURULMUS),
             EK_BETIK: sha256(EK_BETIK), cag["b4"]["cikti"]: cag["b4"]["cikti_sha256"],
             cag["b2"]["cikti"]: cag["b2"]["cikti_sha256"]}
    out = {"etiket": ETIKET_A10, "tanim": A10_TANIM,
           "meta": meta_temel(a, {"girdi_sha256": girdi, "matris_dizinleri": {"b4": B4_MATRIS, "b2": B2_MATRIS},
                                  "bootstrap_B": A4["meta"]["bootstrap_B"], "bootstrap_tohum": A4["meta"]["bootstrap_tohum"],
                                  "panel_en_az_kullanilan": A4["meta"]["panel_en_az"]}),
           "mimari_dogrulama": mim, "cikarilan": r18, "kalan_panel": kalan, "tablo_farki": fark,
           "dondurulmus_cagrilar": cag, "varsayilan_bekci_hatasi": bekci,
           "b4_a10": y4, "b4_dondurulmus_panel": d4, "b2_a10": y2, "b2_dondurulmus_panel": d2,
           "karsilastirma": kars, "bagimsiz_yeniden_hesap": bag}
    yaz(f"{CIKTI}/a10_panel.json", out)
    print("bekci", bekci)
    print(json.dumps(DM.jsonla(kars), ensure_ascii=False, indent=0)[:2500])
    print("bagimsiz", bag)
    for h in ("H1", "H2", "H3"):
        print(h, y4[h]["kestirim"], y4[h]["ci90"], y4[h]["ci95"], y4[h]["karar"])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mod", required=True, choices=["turetilmis", "a10_panel"])
    ap.add_argument("--B", type=int, default=2000)
    a = ap.parse_args(argv)
    if a.mod == "turetilmis":
        return turetilmis_kos(a)
    return a10_kos(a)


if __name__ == "__main__":
    main()
