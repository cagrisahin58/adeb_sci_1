# -*- coding: utf-8 -*-
"""Hakem paneli sonrasi masa cozumlemeleri (31.10.2026; GPU gerekmez).

Hakem paneli (raporlar/hakem_konsey_2026-10-31/birlesik.md, mercek_istatistik.md) uc eksik cozumleme istedi:

  --mod bootstrap   ON_KAYIT_2026-10-29.md §5 "Duyarliliklar" listesindeki hiyerarsik bootstrap (hucre icinde
                    kosular yerine koyarak, goruntuler butun hucrelerde ortak bootstrap agirligiyla, B = 2000)
                    K-a ve K-b icin; dondurulmus betik bunu B2'de yalniz K-c icin uretmisti. K-c ayni yontemle
                    ve ayni RNG sirasiyla yeniden uretilir ve dondurulmus JSON'daki araligla karsilastirilir.
                    Veri: cifar10 (B2, results/q1/konsey_b2_panel) | cifar100 (B9, results/q1/konsey_b9_c100/matris).
                    Etiket: on kayitli, sonradan uretildi (31.10.2026, hakem paneli sonrasi).
  --mod mantel_aile Ek on kayit (ON_KAYIT_EK_B8_B10_2026-10-30.md) §6.4 S10-3: ayni aileden olma gostergesini
                    (CNN-CNN, donusturucu-donusturucu, karma) model ana etkilerine ek ortak degisken alan kismi
                    Mantel; uc veri kumesi; 9999 permutasyon, tohum 20261030 (ek §6.2). Ek §6.2'nin ham ve ana
                    etki artikli istatistikleri bagimsiz kodla yeniden uretilir ve mantel_<veri>.json ile 1e-6
                    icinde karsilastirilir. Etiket: on kayitli (ek §6.4, kesifsel oncelik), sonradan uretildi.
  --mod kesifsel    Kesifsel: aile ici kisitli permutasyonla Mantel; aile ayiklamali artik Spearman (sira
                    olcegi; 11_sonuc_b8_b10.md §7 yontemi) ve permutasyon p'si; yalniz CNN-CNN ciftlerinde artik
                    Spearman (iki tanim); ImageNetV2'de Salman R18-R50 ciftinin c ve log tau degeri, matrisin en
                    kucuk c_ij'si. Etiket: kesifsel.

Dondurulmus betik (experiments/q1_konsey_ayrisim.py) importlib ile, sha256 denetimiyle yuklenir ve hicbir
islevi degistirilmeden kullanilir. Hicbir sayi elle yazilmaz; her cikti JSON'u girdi dosyalarinin sha256'sini,
yontem tanimini, tohumu ve permutasyon/bootstrap sayisini tasir.

Kullanim (konteyner, depo kokunden):
  python -B experiments/q1_ek_masa.py --mod bootstrap --veri cifar10
  python -B experiments/q1_ek_masa.py --mod bootstrap --veri cifar100
  python -B experiments/q1_ek_masa.py --mod mantel_aile
  python -B experiments/q1_ek_masa.py --mod kesifsel
  --sinama : mantel_aile ve kesifsel kiplerinde gercek veri yerine yapay matrislerle kod sinamasi
             (cikti SINAMA_SONUC_DEGIL tasir; --cikti ile results disina yazilmalidir).
"""
import argparse
import hashlib
import importlib.util
import io
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy import stats

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

KOK = Path(__file__).resolve().parents[1]
DONDURULMUS = "experiments/q1_konsey_ayrisim.py"
DONDURULMUS_SHA = "4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389"   # ON_KAYIT Dondurma eki (a)
HT = {"cifar10": "raporlar/konsey_2026-10-29/hucre_tablosu.json",
      "cifar100": "raporlar/konsey_2026-10-29/hucre_tablosu_b9.json",
      "imagenetv2": "raporlar/konsey_2026-10-29/hucre_tablosu_b8.json"}
MATRIS = {"cifar10": "results/q1/konsey_b2_panel", "cifar100": "results/q1/konsey_b9_c100/matris"}
DONDURULMUS_CIKTI = {"cifar10": "results/q1/konsey_ayrisim_b2.json",
                     "cifar100": "results/q1/konsey_b9_c100/b9_dondurulmus_b2.json"}
MANTEL = "results/q1/konsey_b10_gradyan/mantel_{}.json"
VERI_MANTEL = ("cifar10", "cifar100", "imagenetv2")
CIKTI = "results/q1/konsey_ek_masa"
PERM = 9999            # ek on kayit §6.2
MANTEL_TOHUM = 20261030  # ek on kayit §6.2
DONUSTURUCU = ("ViT", "XCiT", "Swin")
ETIKET_OK = "on kayitli, sonradan uretildi (31.10.2026, hakem paneli sonrasi)"
ETIKET_KES = "kesifsel"
R18, R50 = "IN_Salman2020Do_R18", "IN_Salman2020Do_R50"
TOL = 1e-6


def sha256(yol):
    h = hashlib.sha256()
    with open(KOK / yol if not Path(yol).is_absolute() else yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def oku(yol):
    return json.loads((KOK / yol).read_text(encoding="utf-8"))


_DM = None


def dondurulmus():
    """Dondurulmus cozumleme betigini sha256 denetimiyle modul olarak yukler."""
    global _DM
    if _DM is None:
        s = sha256(DONDURULMUS)
        if s != DONDURULMUS_SHA:
            raise SystemExit(f"DONDURULMUS BETIK DEGISMIS: {DONDURULMUS} sha256 {s} != {DONDURULMUS_SHA}; durduruldu")
        spec = importlib.util.spec_from_file_location("q1_konsey_ayrisim_dondurulmus", KOK / DONDURULMUS)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _DM = mod
    return _DM


def meta_temel(a, ek=None):
    m = {"betik": "experiments/q1_ek_masa.py", "betik_sha256": sha256(Path(__file__).resolve()),
         "dondurulmus_betik": DONDURULMUS, "dondurulmus_betik_sha256_dogrulandi": DONDURULMUS_SHA,
         "mod": a.mod, "uretildi_utc": datetime.now(timezone.utc).isoformat(), "numpy": np.__version__,
         "scipy": __import__("scipy").__version__, "argv": sys.argv[1:]}
    if ek:
        m.update(ek)
    return m


def yaz(yol, obj):
    dm = dondurulmus()
    p = KOK / yol if not Path(yol).is_absolute() else Path(yol)
    p.parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(dm.jsonla(obj), fh, ensure_ascii=False, indent=1)
    print("yazildi:", yol)


def maks_fark(a, b):
    a = np.asarray(a, float).ravel()
    b = np.asarray(b, float).ravel()
    return float(np.max(np.abs(a - b))) if a.size else 0.0


# ==============================================================================================
# (1) Hiyerarsik bootstrap: K-a, K-b (yeni) ve K-c (dogrulama)
# ==============================================================================================
BOOT_TANIM = (
    "ON_KAYIT §5 Duyarliliklar: 'hiyerarsik bootstrap (hucre icinde kosular, goruntuler ortak, B = 2000)'. Uygulama: "
    "(i) goruntu bootstrap agirliklari W (n x B) dondurulmus bootstrap_agirlik() ile bir kez cekilir ve butun hucrelerde, "
    "butun modellerde ve uc nicelikte (K-a, K-b, K-c) ortaktir; her kopyada sigma, rho ve S dondurulmus model_duzeyi() "
    "ile bolunmus yari, log olcek ve birincil panel P uzerinden agirlikli oranlardan hesaplanir. (ii) K-c icin tohumlar "
    "dondurulmus b2_coz() dongusuyle birebir cekilir (V-scr icinde yerine koyarak; ozdes tohum ciftleri disarida; yalniz "
    "tek farkli tohum iceren ornek yeniden cekilir). (iii) Ardindan ayni RNG ile her kopyada once C1-R32 hucresinin, sonra "
    "V-scr hucresinin kosulari hucre icinde yerine koyarak cekilir (sR, sV; her biri hucre buyuklugu kadar). K-a: k'inci "
    "cift (R[sR[k]], V[sV[k]]), q_k = [sigma(R) - sigma(V)] / [S(R) - S(V)], istatistik ort_k q_k. K-b: ort_i rho(V[sV[i]]). "
    "Aralik yuzdelik (%90: 5-95, %95: 2,5-97,5; np.percentile dogrusal aradegerleme), K-c ile ayni. Bootstrap p: K-a "
    "(1 + #{ort q* <= 0,50})/(B + 1); K-b TOST max[(1 + #{rho* <= -delta})/(B + 1), (1 + #{rho* >= +delta})/(B + 1)]; "
    "K-c dondurulmus tanim. Karar karsilastirmasi: dondurulmus b2_karar() kurallari, t araliklari ve t p'leri yerine "
    "bootstrap araliklari ve bootstrap p'leri konarak (Holm, aile buyuklugu 3) yeniden uygulanir; nokta kestirimleri "
    "degismez. Duyarlilik varyanti (cift_duzeyi): kosu ciftleri birim olarak cekilir (sR cift indeksi olarak kullanilir).")
TOHUM_KAYNAGI = ("ON_KAYIT_2026-10-29.md bootstrap tohumu belirtmez; dondurulmus betigin BOOT_TOHUM sabiti kullanildi "
                 "(dondurulmus K-c bootstrap'iyla ayni tohum ve ayni RNG akisi; W ilk cekim, K-c tohum cekimleri ikinci, "
                 "K-a/K-b tohum cekimleri ucuncu)")


def matris_yukle(dm, veri, tablo):
    M = dm.Matris()
    esl_tum = tablo.get("dizin_takma_ad_esleme", {})
    dz = MATRIS[veri]
    key = str(dz).replace("\\", "/").rstrip("/")
    esl = next((v for k, v in esl_tum.items() if key.endswith(k.rstrip("/"))), None)
    M.ekle(dz, esl)
    return M


def yuzdelik(x):
    x = np.asarray(x, float)
    return ([float(np.percentile(x, 5)), float(np.percentile(x, 95))],
            [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))])


def bootstrap_kos(a):
    dm = dondurulmus()
    veri = a.veri
    if veri not in MATRIS:
        raise SystemExit("--mod bootstrap icin --veri cifar10 ya da cifar100")
    B = a.B
    tablo = dm.tablo_oku(KOK / HT[veri])
    J = oku(DONDURULMUS_CIKTI[veri])
    if J["meta"]["hucre_tablosu_sha256"] != sha256(HT[veri]):
        raise SystemExit("hucre tablosu dondurulmus ciktidakiyle ayni degil")
    if J["meta"]["betik_sha256"] != DONDURULMUS_SHA:
        raise SystemExit("dondurulmus cikti baska bir betik surumuyle uretilmis")
    M = matris_yukle(dm, veri, tablo)
    mevcut = set(M.modeller())
    P, P2, eksik = dm.paneller(tablo, mevcut)
    if P != J["panel"]["birincil"]:
        raise SystemExit(f"panel uyusmuyor: {P} != {J['panel']['birincil']}")
    R = dm.hucre_uyeleri(tablo, "C1-R32", mevcut)
    V = dm.hucre_uyeleri(tablo, "V-scr", mevcut)
    ciftler = [tuple(c) for c in tablo.get("b2_tohum_ciftleri", []) if c[0] in mevcut and c[1] in mevcut]
    F = J["b2"]["F_B2"]
    # ---- nokta kestirimleri (dondurulmus islevler) ve dondurulmus JSON ile esitlik
    g = dm.Alici(M)
    ka, rhoV = dm.ka_kb(g, ciftler, V, P)
    kat = dm.tek_orneklem(ka["q"])
    kb = dm.tek_orneklem(rhoV)
    kb["tost_p"], kb["tost_p_alt"], kb["tost_p_ust"] = dm.tost_p(kb["ort"], kb["se"], kb["df"])
    ic, sig = dm.kc_nokta(g, V, P)
    Dw = float(np.mean(list(ic.values())) - np.mean(list(sig.values())))
    nokta_dog = {
        "K-a.q": maks_fark(ka["q"], F["K-a"]["q"]),
        "K-a.D": maks_fark(ka["D"], F["K-a"]["D"]),
        "K-a.sinama.ort": maks_fark(kat["ort"], F["K-a"]["sinama"]["ort"]),
        "K-a.sinama.ci90": maks_fark(kat["ci90"], F["K-a"]["sinama"]["ci90"]),
        "K-a.sinama.ci95": maks_fark(kat["ci95"], F["K-a"]["sinama"]["ci95"]),
        "K-b.degerler": maks_fark(kb["degerler"], F["K-b"]["degerler"]),
        "K-b.ort": maks_fark(kb["ort"], F["K-b"]["ort"]),
        "K-b.ci90": maks_fark(kb["ci90"], F["K-b"]["ci90"]),
        "K-b.ci95": maks_fark(kb["ci95"], F["K-b"]["ci95"]),
        "K-b.tost_p": maks_fark(kb["tost_p"], F["K-b"]["tost_p"]),
        "K-c.Delta_w": maks_fark(Dw, F["K-c"]["Delta_w"]),
    }
    nokta_esit = all(v <= 1e-12 for v in nokta_dog.values())
    if not nokta_esit:
        raise SystemExit(f"nokta kestirimleri dondurulmus JSON'la ayni degil: {nokta_dog}")
    # ---- RNG akisi: dondurulmus main() ile ayni tohum; b2_coz'da ilk cekim W, sonra K-c dongusu
    rng = np.random.default_rng(dm.BOOT_TOHUM)
    W = dm.bootstrap_agirlik(M.n, B, rng)
    gb = dm.Alici(M, W)
    icb, sigb = dm.kc_nokta(gb, V, P)
    dist_kc = []
    yeniden = 0
    for kb_i in range(B):          # dondurulmus b2_coz() K-c dongusunun birebir kopyasi
        while True:
            sec = rng.integers(0, len(V), len(V))
            ciftb = [(V[i], V[j]) for x, i in enumerate(sec) for j in sec[x + 1:] if i != j]
            if ciftb:
                break
            yeniden += 1
        vi = np.mean([icb[tuple(sorted((u, v), key=V.index))][kb_i] for u, v in ciftb])
        vs = np.mean([sigb[V[i]][kb_i] for i in sec])
        dist_kc.append(vi - vs)
    dist_kc = np.array(dist_kc)
    kc90, kc95 = yuzdelik(dist_kc)
    p_kc = float((1 + (dist_kc <= 0).sum()) / (B + 1))
    fb = F["K-c"]["bootstrap"]
    kc_dog = {"ci90": maks_fark(kc90, fb["ci90"]), "ci95": maks_fark(kc95, fb["ci95"]),
              "p_tek_H0_Delta_le_0": maks_fark(p_kc, F["K-c"]["p_tek_H0_Delta_le_0"]),
              "yeniden_cekilen_tek_tohumlu_ornek": int(yeniden) - int(fb["yeniden_cekilen_tek_tohumlu_ornek"])}
    kc_esit = (kc_dog["ci90"] <= 1e-12 and kc_dog["ci95"] <= 1e-12 and kc_dog["p_tek_H0_Delta_le_0"] <= 1e-12
               and kc_dog["yeniden_cekilen_tek_tohumlu_ornek"] == 0)
    # ---- K-a ve K-b: model duzeyi bootstrap vektorleri (ayni W)
    md = {m: dm.model_duzeyi(gb, m, P) for m in R + V}
    nR, nV, nC = len(R), len(V), len(ciftler)
    if not (nR == nV == nC):
        raise SystemExit(f"hucre buyuklukleri esit degil: R {nR}, V {nV}, cift {nC}")
    cift_idx = [(R.index(r), V.index(v)) for r, v in ciftler]
    q_boot, rho_boot, q_cift, rho_cift = np.empty(B), np.empty(B), np.empty(B), np.empty(B)
    D_kucuk, D_kucuk_cift = 0, 0
    for b in range(B):
        sR = rng.integers(0, nR, nR)
        sV = rng.integers(0, nV, nV)
        qs, Ds = [], []
        for k in range(nC):
            r_, v_ = R[sR[k]], V[sV[k]]
            D = float(md[r_]["S"][b] - md[v_]["S"][b])
            Ds.append(D)
            qs.append(float(md[r_]["sigma"][b] - md[v_]["sigma"][b]) / D)
        D_kucuk += int(any(not (d > dm.DELTA) for d in Ds))
        q_boot[b] = np.mean(qs)
        rho_boot[b] = np.mean([float(md[V[i]]["rho"][b]) for i in sV])
        # varyant: kosu ciftleri birim (sR cift indeksi)
        qc, Dc, rc = [], [], []
        for k in sR:
            ri, vi_ = cift_idx[k]
            D = float(md[R[ri]]["S"][b] - md[V[vi_]]["S"][b])
            Dc.append(D)
            qc.append(float(md[R[ri]]["sigma"][b] - md[V[vi_]]["sigma"][b]) / D)
            rc.append(float(md[V[vi_]]["rho"][b]))
        D_kucuk_cift += int(any(not (d > dm.DELTA) for d in Dc))
        q_cift[b] = np.mean(qc)
        rho_cift[b] = np.mean(rc)

    def p_ka(x):
        return float((1 + (x <= 0.5).sum()) / (B + 1))

    def p_tost(x, d):
        pa = float((1 + (x <= -d).sum()) / (B + 1))
        pu = float((1 + (x >= d).sum()) / (B + 1))
        return max(pa, pu), pa, pu

    qa90, qa95 = yuzdelik(q_boot)
    rb90, rb95 = yuzdelik(rho_boot)
    tp, tpa, tpu = p_tost(rho_boot, dm.DELTA)
    tp06 = p_tost(rho_boot, dm.DELTA_DUY)[0]
    qc90, qc95 = yuzdelik(q_cift)
    rc90, rc95 = yuzdelik(rho_cift)
    # ---- karar: dondurulmus b2_karar kurallari, aralik ve p yerine bootstrap
    ka_k = {"payda_kucuk_tohumlar": F["K-a"]["payda_kucuk_tohumlar"],
            "ongoru_her_tohumda_q_ge_0.75": F["K-a"]["ongoru_her_tohumda_q_ge_0.75"]}
    kc_k = {"bootstrap": {"ci90": kc90}, "ongoru_Delta_ge_0.30": F["K-c"]["ongoru_Delta_ge_0.30"]}
    pa_b = p_ka(q_boot) if not F["K-a"]["payda_kucuk_tohumlar"] else float("nan")
    pler_b = [pa_b, tp, p_kc]
    adj_b, _ = dm.holm_aile(pler_b)
    karar_b = dm.b2_karar(ka_k, {"ci90": qa90}, {"ci90": rb90, "ci95": rb95, "ort": kb["ort"]}, kc_k, adj_b, dm.DELTA)
    adj_b06, _ = dm.holm_aile([pa_b, tp06, p_kc])
    karar_b06 = dm.b2_karar(ka_k, {"ci90": qa90}, {"ci90": rb90, "ci95": rb95, "ort": kb["ort"]}, kc_k, adj_b06,
                            dm.DELTA_DUY)
    kd = F["karar"]
    kd06 = F["duyarlilik_delta_0.06"]["karar"]
    karsi = {s: {"dondurulmus": kd[s], "bootstrap_araligiyla": karar_b[s], "degisti": kd[s] != karar_b[s]}
             for s in ("K-a", "K-b", "K-c")}
    karsi06 = {s: {"dondurulmus": kd06[s], "bootstrap_araligiyla": karar_b06[s], "degisti": kd06[s] != karar_b06[s]}
               for s in ("K-a", "K-b", "K-c")}
    girdi = dict(M.kaynaklar)
    girdi[DONDURULMUS_CIKTI[veri]] = sha256(DONDURULMUS_CIKTI[veri])
    girdi[HT[veri]] = sha256(HT[veri])
    girdi[DONDURULMUS] = sha256(DONDURULMUS)
    out = {
        "etiket": ETIKET_OK,
        "meta": meta_temel(a, {"veri": veri, "blok": "B2" if veri == "cifar10" else "B9", "matris_dizini": MATRIS[veri],
                               "hucre_tablosu": HT[veri], "dondurulmus_cikti": DONDURULMUS_CIKTI[veri],
                               "B": B, "bootstrap_tohum": int(dm.BOOT_TOHUM), "tohum_kaynagi": TOHUM_KAYNAGI,
                               "delta": dm.DELTA, "delta_duyarlilik": dm.DELTA_DUY, "alfa": dm.ALFA,
                               "n_goruntu": M.n, "girdi_sha256": girdi}),
        "tanim": BOOT_TANIM,
        "hucreler": {"C1-R32": R, "V-scr": V}, "tohum_ciftleri": [list(c) for c in ciftler], "panel": P,
        "dogrulama": {"nokta_kestirimleri_dondurulmus_json_ile_maks_fark": nokta_dog, "nokta_esit": nokta_esit,
                      "K-c_yeniden_uretim_maks_fark": kc_dog, "K-c_esit": kc_esit,
                      "tutarlilik": M.tutarlilik(), "cakismalar": M.cakisma},
        "K-a": {"nokta_ort_q": kat["ort"], "q_s": ka["q"], "D_s": ka["D"],
                "t_ci90": kat["ci90"], "t_ci95": kat["ci95"], "t_p_tek_H0_q_le_0.5": F["K-a"]["p_tek_H0_q_le_0.5"],
                "bootstrap": {"ci90": qa90, "ci95": qa95, "ort": float(q_boot.mean()), "sd": float(q_boot.std(ddof=1)),
                              "p_tek_H0_q_le_0.5": pa_b, "D_le_0.10_kopya_sayisi": D_kucuk},
                "cift_duzeyi_varyant": {"ci90": qc90, "ci95": qc95, "sd": float(q_cift.std(ddof=1)),
                                        "D_le_0.10_kopya_sayisi": D_kucuk_cift}},
        "K-b": {"nokta_ort_rho": kb["ort"], "rho_s": kb["degerler"], "t_ci90": kb["ci90"], "t_ci95": kb["ci95"],
                "t_tost_p": kb["tost_p"],
                "bootstrap": {"ci90": rb90, "ci95": rb95, "ort": float(rho_boot.mean()), "sd": float(rho_boot.std(ddof=1)),
                              "tost_p": tp, "tost_p_alt": tpa, "tost_p_ust": tpu, "tost_p_delta_0.06": tp06,
                              "ci90_delta_icinde": bool(dm.icinde(rb90, -dm.DELTA, dm.DELTA)),
                              "ci95_sifiri_disliyor": bool(rb95[0] > 0 or rb95[1] < 0)},
                "cift_duzeyi_varyant": {"ci90": rc90, "ci95": rc95, "sd": float(rho_cift.std(ddof=1)),
                                        "ci90_delta_icinde": bool(dm.icinde(rc90, -dm.DELTA, dm.DELTA))}},
        "K-c": {"Delta_w": Dw, "dondurulmus_bootstrap": {"ci90": fb["ci90"], "ci95": fb["ci95"],
                                                         "yeniden_cekilen": fb["yeniden_cekilen_tek_tohumlu_ornek"],
                                                         "p": F["K-c"]["p_tek_H0_Delta_le_0"]},
                "yeniden_bootstrap": {"ci90": kc90, "ci95": kc95, "yeniden_cekilen": int(yeniden), "p": p_kc}},
        "karar": {"kural": "dondurulmus b2_karar(); t araliklari ve t p'leri yerine bootstrap araliklari ve p'leri",
                  "p_ham_bootstrap": pler_b, "p_holm_bootstrap": adj_b, "p_holm_dondurulmus": F["p_holm"],
                  "karsilastirma": karsi, "degisen": [s for s, v in karsi.items() if v["degisti"]],
                  "delta_0.06": {"p_holm_bootstrap": adj_b06, "karsilastirma": karsi06,
                                 "degisen": [s for s, v in karsi06.items() if v["degisti"]]},
                  "bootstrap_karar_tam": karar_b},
    }
    yaz(a.cikti or f"{CIKTI}/bootstrap_{veri}.json", out)
    print(json.dumps({"K-a_boot90": qa90, "K-b_boot90": rb90, "K-b_boot95": rb95, "K-c_esit": kc_esit,
                      "degisen": out["karar"]["degisen"]}, ensure_ascii=False))
    return out


# ==============================================================================================
# Mantel yardimcilari (bagimsiz kod; ek §6.2 tanimi)
# ==============================================================================================
def ust(A):
    i, j = np.triu_indices(A.shape[0], 1)
    return np.asarray(A, float)[i, j]


def pearson(a, b):
    a = np.asarray(a, float) - np.mean(a)
    b = np.asarray(b, float) - np.mean(b)
    d = math.sqrt(float(a @ a) * float(b @ b))
    return float(a @ b) / d if d > 0 else float("nan")


def spearman(a, b):
    return pearson(stats.rankdata(a), stats.rankdata(b))


def tasarim_ana_etki(K):
    """Sirasiz ciftler (ust ucgen sirasi) icin X_ij = mu + a_i + a_j tasarim matrisi."""
    i, j = np.triu_indices(K, 1)
    X = np.zeros((len(i), K + 1))
    X[:, 0] = 1.0
    X[np.arange(len(i)), 1 + i] = 1.0
    X[np.arange(len(i)), 1 + j] = 1.0
    return X


def artik_yapici(X):
    """En kucuk kareler artik izdusumu I - X X^+ (rank eksikligine dayanikli)."""
    return np.eye(X.shape[0]) - X @ np.linalg.pinv(X)


def ciftten_matris(v, K):
    i, j = np.triu_indices(K, 1)
    A = np.zeros((K, K))
    A[i, j] = v
    A[j, i] = v
    return A


def aile_gostergeleri(gruplar):
    """gruplar: model basina 'CNN' ya da 'donusturucu'. Ust ucgen sirasinda CC, TT, karma gostergeleri."""
    K = len(gruplar)
    i, j = np.triu_indices(K, 1)
    g = np.array(gruplar)
    cc = ((g[i] == "CNN") & (g[j] == "CNN")).astype(float)
    tt = ((g[i] == "donusturucu") & (g[j] == "donusturucu")).astype(float)
    return cc, tt, 1.0 - cc - tt


def permutasyon(stat_fn, K, perm, tohum, gruplar_idx=None):
    """stat_fn(p): p etiket permutasyonu (np.ix_(p, p) ile uygulanir). gruplar_idx verilirse permutasyon yalniz
    gruplar icinde yapilir (her grubun indeksleri sabit sirada, gruplar sabit sirada). p_tek = (1 + #{r* >= r})/(perm + 1)."""
    r0 = stat_fn(np.arange(K))
    rng = np.random.default_rng(tohum)
    dist = np.empty(perm)
    for b in range(perm):
        if gruplar_idx is None:
            p = rng.permutation(K)
        else:
            p = np.arange(K)
            for gi in gruplar_idx:
                p[gi] = gi[rng.permutation(len(gi))]
        dist[b] = stat_fn(p)
    ok = np.isfinite(dist)
    return {"istatistik": r0, "perm": perm, "tohum": tohum,
            "p_tek": float((1 + np.sum(dist[ok] >= r0)) / (ok.sum() + 1)),
            "p_iki": float((1 + np.sum(np.abs(dist[ok]) >= abs(r0))) / (ok.sum() + 1)),
            "perm_ort": float(np.nanmean(dist)), "perm_sd": float(np.nanstd(dist))}


def veri_yukle(veri, sinama=False):
    """mantel_<veri>.json: c_matrisi, log_tau_matrisi, modeller_ortak; aile hucre tablosundan."""
    if sinama:
        rng = np.random.default_rng({"cifar10": 1, "cifar100": 2, "imagenetv2": 3}[veri])
        K = {"cifar10": 12, "cifar100": 10, "imagenetv2": 9}[veri]
        gr = ["CNN"] * (K - 4) + ["donusturucu"] * 4
        a_ = rng.normal(size=K)
        Z = rng.normal(size=(K, K))
        Z = (Z + Z.T) / 2
        C = 0.3 + 0.1 * (a_[:, None] + a_[None, :]) + 0.05 * Z
        T = -0.8 + 0.2 * (a_[:, None] + a_[None, :]) + 0.3 * Z + 0.05 * rng.normal(size=(K, K))
        T = (T + T.T) / 2
        np.fill_diagonal(C, 1.0)
        np.fill_diagonal(T, 0.0)
        adlar = [f"SAHTE_{k}" for k in range(K)]
        return {"adlar": adlar, "C": C, "T": T, "gruplar": gr, "aile": gr, "J": None, "girdi": {}}
    yol = MANTEL.format(veri)
    J = oku(yol)
    tablo = oku(HT[veri])
    adlar = J["modeller_ortak"]
    aile = [tablo["modeller"][m]["aile"] for m in adlar]
    bilinmeyen = sorted({x for x in aile if x != "CNN" and x not in DONUSTURUCU})
    if bilinmeyen:
        raise SystemExit(f"{veri}: siniflanamayan aile {bilinmeyen}")
    gr = ["CNN" if x == "CNN" else "donusturucu" for x in aile]
    C = np.asarray(J["c_matrisi"], float)
    T = np.asarray(J["log_tau_matrisi"], float)
    simetri = {"c_maks_asimetri": maks_fark(C, C.T), "log_tau_maks_asimetri": maks_fark(T, T.T)}
    return {"adlar": adlar, "C": C, "T": T, "gruplar": gr, "aile": aile, "J": J, "simetri": simetri,
            "girdi": {yol: sha256(yol), HT[veri]: sha256(HT[veri])}}


# ==============================================================================================
# (2) S10-3 aile gostergeli kismi Mantel
# ==============================================================================================
S10_3_TANIM = (
    "Ek on kayit §6.4 S10-3: 'ayni aileden olma gostergesini (CNN-CNN, donusturucu-donusturucu, karma) ek ortak degisken "
    "alan kismi Mantel'. Uygulama (ek §6.2 kismi istatistiginin dogal uzantisi): sirasiz ciftler uzerinde her matris "
    "(c ve log tau ayri ayri) X_ij = mu + a_i + a_j + b_CC*CC_ij + b_TT*TT_ij + e_ij modeliyle deger olceginde en kucuk "
    "kareler ile kestirilir (karma ciftler referans; aile: hucre tablosundaki 'aile' alani, CNN = CNN, ViT/XCiT/Swin = "
    "donusturucu); istatistik e(c) ile e(log tau) arasindaki Spearman korelasyonudur. Permutasyon (birincil, ek §6.2'deki "
    "'kismi istatistikte c artik matrisi' kuralinin aynisi; Smouse, Long ve Sokal 1986 artik permutasyonu): e(c) artik "
    "matrisinin satir ve sutunlari ortak permute edilir, e(log tau) sabit; 9999 permutasyon, tohum 20261030, "
    "p_tek = (1 + #{r* >= r})/(perm + 1). Duyarlilik: ham c matrisi permute edilip sabit tasarima gore yeniden "
    "artiklanir (Legendre ve Legendre 2012 'ham X permutasyonu'; gradyan betiginin kismi Mantel semasi).")
OZEL_62 = ("Ek §6.2 yeniden uretimi: ham = Spearman(ust c, ust log tau), c'nin satir/sutun ortak permutasyonu; "
           "ana_etki_artik = e_ij artiklari (X_ij = mu + a_i + a_j, deger olceginde en kucuk kareler) arasinda Spearman, "
           "c artik matrisinin ortak permutasyonu; 9999 permutasyon, tohum 20261030 (her sinama kendi RNG'siyle). Kod "
           "gradyan betiginden bagimsizdir (I - X X^+ izdusumu, scipy rankdata, Pearson).")


def ana_etki_artik_matrisi(A):
    K = A.shape[0]
    return ciftten_matris(artik_yapici(tasarim_ana_etki(K)) @ ust(A), K)


def mantel_aile_kos(a):
    out = {"etiket": "on kayitli (ek on kayit §6.4, kesifsel oncelik), sonradan uretildi (31.10.2026, hakem paneli sonrasi)",
           "tanim_S10_3": S10_3_TANIM, "tanim_6_2_yeniden_uretim": OZEL_62, "tolerans": TOL, "veri": {}}
    girdi = {}
    for veri in VERI_MANTEL:
        d = veri_yukle(veri, a.sinama)
        girdi.update(d["girdi"])
        C, T, gr = d["C"], d["T"], d["gruplar"]
        K = C.shape[0]
        X0 = tasarim_ana_etki(K)
        R0 = artik_yapici(X0)
        cc, tt, km = aile_gostergeleri(gr)
        X1 = np.column_stack([X0, cc, tt])
        R1 = artik_yapici(X1)
        yT = ust(T)
        # ek §6.2 yeniden uretim
        ham = permutasyon(lambda p: spearman(ust(C[np.ix_(p, p)]), yT), K, a.perm, MANTEL_TOHUM)
        EC0 = ana_etki_artik_matrisi(C)
        eT0 = R0 @ yT
        aea = permutasyon(lambda p: spearman(ust(EC0[np.ix_(p, p)]), eT0), K, a.perm, MANTEL_TOHUM)
        # S10-3 birincil: deger olceginde ana etki + aile gostergesi artiklari; c artik matrisi permute
        EC1 = ciftten_matris(R1 @ ust(C), K)
        eT1 = R1 @ yT
        s103 = permutasyon(lambda p: spearman(ust(EC1[np.ix_(p, p)]), eT1), K, a.perm, MANTEL_TOHUM)
        # S10-3 duyarlilik: ham c permute, sabit tasarimla yeniden artiklama
        s103h = permutasyon(lambda p: spearman(R1 @ ust(C[np.ix_(p, p)]), eT1), K, a.perm, MANTEL_TOHUM)
        rk = {"rank_X_ana_etki": int(np.linalg.matrix_rank(X0)), "rank_X_ana_etki_aile": int(np.linalg.matrix_rank(X1))}
        kayit = {"K": K, "cift_sayisi": int(K * (K - 1) // 2), "modeller": d["adlar"], "aile": d["aile"], "grup": gr,
                 "cift_turu_sayilari": {"CNN-CNN": int(cc.sum()), "donusturucu-donusturucu": int(tt.sum()),
                                        "karma": int(km.sum())},
                 "tasarim_rank": rk,
                 "yeniden_uretim_6_2": {"ham": ham, "ana_etki_artik": aea},
                 "S10_3": s103, "S10_3_duyarlilik_ham_c_permutasyonu": s103h}
        if d["J"] is not None:
            S = d["J"]["sinamalar"]
            kars = {}
            for ad, yeni in (("ham", ham), ("ana_etki_artik", aea)):
                eski = S[ad]
                fk = {k: abs(float(yeni[k]) - float(eski[k])) for k in ("istatistik", "p_tek", "p_iki", "perm_ort", "perm_sd")}
                kars[ad] = {"maks_fark": max(fk.values()), "farklar": fk, "esit_1e-6": max(fk.values()) <= TOL,
                            "json_perm": eski.get("perm"), "json_tohum": eski.get("tohum")}
            kayit["mantel_json_karsilastirma"] = kars
            kayit["simetri"] = d["simetri"]
        out["veri"][veri] = kayit
        print(veri, {k: (round(v["istatistik"], 4), v["p_tek"]) for k, v in
                     (("ham", ham), ("ana_etki_artik", aea), ("S10_3", s103), ("S10_3_h", s103h))})
    out["meta"] = meta_temel(a, {"perm": a.perm, "tohum": MANTEL_TOHUM, "tohum_kaynagi": "ek on kayit §6.2 (20261030)",
                                 "girdi_sha256": girdi})
    if a.sinama:
        out["SINAMA_SONUC_DEGIL"] = True
    if not a.sinama:
        out["yeniden_uretim_hepsi_esit_1e-6"] = all(
            v["esit_1e-6"] for d_ in out["veri"].values() for v in d_["mantel_json_karsilastirma"].values())
    yaz(a.cikti or f"{CIKTI}/mantel_aile.json", out)
    return out


# ==============================================================================================
# (3) Kesifsel
# ==============================================================================================
KES_TANIM = {
    "aile_ici_kisitli_permutasyon": (
        "Ek §6.2'nin ham ve ana_etki_artik istatistikleri ayni; permutasyon yalniz ayni grup icinde (CNN modelleri kendi "
        "aralarinda, donusturuculer kendi aralarinda) yapilir; grup sirasi CNN, donusturucu; her grupta indeksler artan "
        "sirada; 9999 permutasyon, tohum 20261030; p_tek = (1 + #{r* >= r})/(perm + 1). Kisitli permutasyon sayisi "
        "n_CNN! x n_donusturucu! olarak raporlanir."),
    "aile_ayiklamali_artik_spearman_sira": (
        "11_sonuc_b8_b10.md §7 yontemi: ana etki artiklari e(c), e(log tau) (deger olceginde) siraya cevrilir; siralar "
        "[1, CC, TT] (gostergelerin siralari) uzerine en kucuk kareyle ayiklanir; istatistik ayiklanmis siralar arasindaki "
        "Pearson (sira kismi korelasyonu). Permutasyon: e(c) artik matrisi ortak permute edilir, e(log tau) ve gostergeler "
        "sabit (gradyan betiginin kismi Mantel semasi); 9999, tohum 20261030. 'deger_olcegi_farki' = bu istatistik eksi "
        "mantel_aile.json S10_3 istatistigi (ayni veri; ayiklama deger olceginde)."),
    "cnn_cnn_artik_spearman": (
        "(i) tam_matris_artigi: butun modellerle kestirilmis ana etki artiklari yalniz CNN-CNN ciftlerine sinirlanir; "
        "Spearman; p: e(c) artik matrisinin CNN blogunda CNN etiketleri ortak permute edilir. (ii) cnn_alt_matrisi: "
        "toplamsal model yalniz CNN alt matrisinde yeniden kestirilir; Spearman; Mantel p ayni bicimde. 9999, tohum 20261030."),
    "r18_r50_ve_en_kucuk_c": (
        "mantel_imagenetv2.json c_matrisi ve log_tau_matrisi'nden IN_Salman2020Do_R18 ile IN_Salman2020Do_R50 hucresi; "
        "sira = kosegen disi sirasiz ciftlerdeki artan sira (1 = en kucuk); en kucuk c_ij ve onu veren cift; her veri kumesi."),
}


def kesifsel_kos(a):
    out = {"etiket": ETIKET_KES, "tanim": KES_TANIM, "veri": {}}
    girdi = {}
    for veri in VERI_MANTEL:
        d = veri_yukle(veri, a.sinama)
        girdi.update(d["girdi"])
        C, T, gr, adlar = d["C"], d["T"], d["gruplar"], d["adlar"]
        K = C.shape[0]
        idx_cnn = np.array([k for k in range(K) if gr[k] == "CNN"])
        idx_don = np.array([k for k in range(K) if gr[k] == "donusturucu"])
        gidx = [g_ for g_ in (idx_cnn, idx_don) if len(g_) > 0]
        yT = ust(T)
        R0 = artik_yapici(tasarim_ana_etki(K))
        EC0 = ciftten_matris(R0 @ ust(C), K)
        eT0 = R0 @ yT
        kayit = {"K": K, "n_CNN": int(len(idx_cnn)), "n_donusturucu": int(len(idx_don)),
                 "kisitli_permutasyon_sayisi": int(math.factorial(len(idx_cnn)) * math.factorial(len(idx_don)))}
        # (a) aile ici kisitli permutasyon
        kayit["aile_ici_kisitli_permutasyon"] = {
            "ham": permutasyon(lambda p: spearman(ust(C[np.ix_(p, p)]), yT), K, a.perm, MANTEL_TOHUM, gidx),
            "ana_etki_artik": permutasyon(lambda p: spearman(ust(EC0[np.ix_(p, p)]), eT0), K, a.perm, MANTEL_TOHUM, gidx)}
        # (b) aile ayiklamali artik Spearman (sira olcegi, §7 yontemi)
        cc, tt, _ = aile_gostergeleri(gr)
        Zs = np.column_stack([np.ones(len(cc)), stats.rankdata(cc), stats.rankdata(tt)])
        Rz = artik_yapici(Zs)
        ry = Rz @ stats.rankdata(eT0)
        sira = permutasyon(lambda p: pearson(Rz @ stats.rankdata(ust(EC0[np.ix_(p, p)])), ry), K, a.perm, MANTEL_TOHUM)
        X1 = np.column_stack([tasarim_ana_etki(K), cc, tt])
        R1 = artik_yapici(X1)
        deger = spearman(R1 @ ust(C), R1 @ yT)
        kayit["aile_ayiklamali_artik_spearman_sira"] = dict(sira, deger_olcegi_istatistigi=deger,
                                                             deger_olcegi_farki=sira["istatistik"] - deger)
        # (c) yalniz CNN-CNN artik Spearman
        i_, j_ = np.triu_indices(K, 1)
        if len(idx_cnn) >= 4:
            sub = np.ix_(idx_cnn, idx_cnn)
            ECs, ETs = EC0[sub], ciftten_matris(eT0, K)[sub]
            tam = permutasyon(lambda p: spearman(ust(ECs[np.ix_(p, p)]), ust(ETs)), len(idx_cnn), a.perm, MANTEL_TOHUM)
            Cs, Ts = C[sub], T[sub]
            Rs = artik_yapici(tasarim_ana_etki(len(idx_cnn)))
            ECa = ciftten_matris(Rs @ ust(Cs), len(idx_cnn))
            eTa = Rs @ ust(Ts)
            alt = permutasyon(lambda p: spearman(ust(ECa[np.ix_(p, p)]), eTa), len(idx_cnn), a.perm, MANTEL_TOHUM)
            ham_cnn = spearman(ust(Cs), ust(Ts))
            kayit["cnn_cnn_artik_spearman"] = {"n_CNN": int(len(idx_cnn)), "cift_sayisi": int(len(idx_cnn) * (len(idx_cnn) - 1) // 2),
                                               "tam_matris_artigi": tam, "cnn_alt_matrisi": alt,
                                               "cnn_cnn_ham_spearman": ham_cnn}
        # (d) R18-R50 ve en kucuk c
        cv = ust(C)
        tv = ust(T)
        sira_c = stats.rankdata(cv, method="min")
        sira_t = stats.rankdata(tv, method="min")
        k_min = int(np.argmin(cv))
        en = {"en_kucuk_c": float(cv[k_min]), "en_kucuk_c_cifti": [adlar[i_[k_min]], adlar[j_[k_min]]],
              "en_kucuk_c_ciftinin_log_tau": float(tv[k_min])}
        o2 = np.argsort(cv)
        en["ikinci_en_kucuk_c"] = float(cv[o2[1]])
        en["ikinci_en_kucuk_c_cifti"] = [adlar[i_[o2[1]]], adlar[j_[o2[1]]]]
        en["en_buyuk_kosegen_disi_c"] = float(cv.max())
        if R18 in adlar and R50 in adlar:
            a_, b_ = adlar.index(R18), adlar.index(R50)
            k_ = int(np.where(((i_ == min(a_, b_)) & (j_ == max(a_, b_))))[0][0])
            en["R18_R50"] = {"c": float(C[a_, b_]), "log_tau": float(T[a_, b_]), "c_sirasi_artan": int(sira_c[k_]),
                             "log_tau_sirasi_artan": int(sira_t[k_]), "cift_sayisi": int(len(cv)),
                             "c_simetrik_hucre": float(C[b_, a_]), "log_tau_simetrik_hucre": float(T[b_, a_]),
                             "ana_etki_artigi_c": float(EC0[a_, b_]),
                             "ana_etki_artigi_log_tau": float(ciftten_matris(eT0, K)[a_, b_])}
        kayit["c_ozet"] = en
        out["veri"][veri] = kayit
        print(veri, "kisitli", {k: (round(v["istatistik"], 4), v["p_tek"]) for k, v in kayit["aile_ici_kisitli_permutasyon"].items()},
              "sira", round(sira["istatistik"], 4), sira["p_tek"],
              "cnn", {k: round(v["istatistik"], 4) for k, v in kayit.get("cnn_cnn_artik_spearman", {}).items()
                      if isinstance(v, dict)})
    out["meta"] = meta_temel(a, {"perm": a.perm, "tohum": MANTEL_TOHUM, "tohum_kaynagi": "ek on kayit §6.2 (20261030)",
                                 "girdi_sha256": girdi})
    if a.sinama:
        out["SINAMA_SONUC_DEGIL"] = True
    yaz(a.cikti or f"{CIKTI}/kesifsel.json", out)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mod", required=True, choices=["bootstrap", "mantel_aile", "kesifsel"])
    ap.add_argument("--veri", choices=["cifar10", "cifar100"])
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--perm", type=int, default=PERM)
    ap.add_argument("--cikti")
    ap.add_argument("--sinama", action="store_true")
    a = ap.parse_args(argv)
    if a.sinama and (a.mod == "bootstrap" or not a.cikti or a.cikti.startswith("results")):
        raise SystemExit("--sinama yalniz mantel_aile/kesifsel ile ve results disina --cikti ile")
    if a.mod == "bootstrap":
        return bootstrap_kos(a)
    dondurulmus()   # jsonla icin; sha denetimi
    if a.mod == "mantel_aile":
        return mantel_aile_kos(a)
    return kesifsel_kos(a)


if __name__ == "__main__":
    main()
