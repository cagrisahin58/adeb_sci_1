# -*- coding: utf-8 -*-
"""Ek bloklar icin cozumleme sarmalayicisi (B8, B9, B10; 30.10.2026).

Dondurulmus experiments/q1_konsey_ayrisim.py DEGISTIRILMEDEN ice aktarilir; yuklemeden once sha256'si
DONDURULMUS_SHA ile karsilastirilir, farkliysa betik durur. Ek on kayit taslagi:
raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md (§4.2, §5.6, §6.2-6.3); fable kararlari E1-E7.

  --mod b9  : B2'nin birebir CIFAR-100 yinelemesi (E1). Dondurulmus betigin main() islevi
              '--mod b2' ile, yalniz yeni hucre tablosuyla cagrilir; cikti dosyasi dondurulmus betigin
              kendi ciktisidir ve dokunulmaz. Sarmalayici ayrica <cikti>.sarmalayici.json yazar
              (betik ve tablo ozetleri, model basina temiz dogruluk; ViT-Tiny CIFAR-100 karistiricisi
              icin betimsel).
  --mod b8  : ImageNetV2 paneli (E2). Holm ailesi YOK; betimsel, aralikli, kesifsel. Dondurulmus betigin
              islevleriyle (Alici, model_duzeyi, model_tablosu) bolunmus yari log olcekte sigma, rho, omega
              (w) tablosu ve cift basina A^sigma_k = sigma(donusturucu_k) - sigma(CNN_k). Ciftler tablonun
              b2_tohum_ciftleri alanindan; IN satiri Singh ciftleri (1, 2), Liu (3) ayri scr satiri.
              Goruntu bootstrap'i B = 2000, tohum 20261030, ortak agirlik; iki ciftte t araligi kurulmaz.
              Ek on kayit §5.6'nin betimsel etiketleri uretilir (karar degildir).
  --mod b10 : q1_ek_gradyan_kosinus.py mantel ciktilarini (veri kumesi basina bir JSON) birlestirir;
              F_B10 = 3 veri kumesi x {ham, ana etki artigi} alti sinama, Holm (dondurulmus holm_aile),
              ek on kayit §6.3 karar kurallari; kismi Mantel kovaryat surumleri kesifsel.

Kullanim (konteyner, depo koku):
  python experiments/q1_ek_ayrisim.py --mod b9 --matris-dizini results/q1/konsey_b9_c100/matris \\
      --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu_b9.json --cikti results/q1/konsey_b9_c100/b9_b2.json
  python experiments/q1_ek_ayrisim.py --mod b8 --matris-dizini results/q1/konsey_b8_imagenetv2/matris \\
      --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu_b8.json --cikti results/q1/konsey_b8_imagenetv2/b8_betimsel.json
  python experiments/q1_ek_ayrisim.py --mod b10 --mantel results/q1/konsey_b10_gradyan/mantel_*.json \\
      --cikti results/q1/konsey_b10_gradyan/b10_aile.json
"""
import argparse
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
OZGUN_MATRIS = KOK / "experiments" / "c1_c3_transfer_matrix.py"
OZGUN_MATRIS_SHA = "f25d9062c958a296353059639398f0a0a8eb18cd48182b1afa5ec4e3986140b7"
BEKLENTI_A_SIGMA_IN = -0.10  # dondurulmus H1 (A^s_scr <= -0,20) + H2 (I^s >= +0,10)
PERM_ON_KAYIT = 9999  # ek on kayit §6.2 (B10 Mantel permutasyon sayisi)

_DM = None


def sha256(yol):
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def dondurulmus(yol=DONDURULMUS, beklenen=DONDURULMUS_SHA):
    """Dondurulmus cozumleme betigini sha256 denetimiyle modul olarak yukler (bir kez)."""
    global _DM
    if _DM is not None:
        return _DM
    s = sha256(yol)
    if s != beklenen:
        raise SystemExit(f"DONDURULMUS BETIK DEGISMIS: {yol} sha256 {s} != {beklenen}; durduruldu")
    spec = importlib.util.spec_from_file_location("q1_konsey_ayrisim_dondurulmus", yol)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _DM = mod
    return mod


def meta(a, ek=None):
    m = {"sarmalayici": "experiments/q1_ek_ayrisim.py", "sarmalayici_sha256": sha256(__file__),
         "dondurulmus_betik_sha256_dogrulandi": DONDURULMUS_SHA,
         "ozgun_matris_betigi_sha256_simdi": sha256(OZGUN_MATRIS) if OZGUN_MATRIS.exists() else None,
         "ozgun_matris_betigi_degismedi": (sha256(OZGUN_MATRIS) == OZGUN_MATRIS_SHA) if OZGUN_MATRIS.exists() else None,
         "mod": a.mod, "uretildi_utc": datetime.now(timezone.utc).isoformat(), "numpy": np.__version__}
    if getattr(a, "hucre_tablosu", None):
        m["hucre_tablosu"] = a.hucre_tablosu
        m["hucre_tablosu_sha256"] = sha256(a.hucre_tablosu)
    if ek:
        m.update(ek)
    return m


def yaz(yol, obj):
    dm = dondurulmus()
    Path(yol).parent.mkdir(parents=True, exist_ok=True)
    with io.open(yol, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(dm.jsonla(obj), fh, ensure_ascii=False, indent=1)
    print("yazildi:", yol)


def matris_yukle(dizinler, tablo=None):
    dm = dondurulmus()
    M = dm.Matris()
    esl_tum = (tablo or {}).get("dizin_takma_ad_esleme", {})
    for dz in dizinler:
        key = str(dz).replace("\\", "/").rstrip("/")
        esl = next((v for k, v in esl_tum.items() if key.endswith(k.rstrip("/"))), None)
        M.ekle(dz, esl)
    return M


def temiz_dogruluklar(M):
    """Her hedefin temiz dogrulugu (yuzde), herhangi bir kaynak dosyasindan (maskeler tutarli olmali)."""
    out = {}
    for (s, t), d in M.h.items():
        if t not in out:
            out[t] = round(100.0 * float(d["tc"].mean()), 2)
    return out


# ----------------------------------------------------------------------------------------------
# B9
# ----------------------------------------------------------------------------------------------
def b9(a):
    dm = dondurulmus()
    argv = ["--mod", "b2", "--hucre-tablosu", a.hucre_tablosu, "--cikti", a.cikti,
            "--bootstrap", str(a.bootstrap), "--panel-en-az", str(a.panel_en_az)]
    for d in a.matris_dizini:
        argv += ["--matris-dizini", d]
    if a.sinama:
        argv.append("--sinama")
    sonuc = dm.main(argv)
    tablo = dm.tablo_oku(a.hucre_tablosu)
    M = matris_yukle(a.matris_dizini, tablo)
    td = temiz_dogruluklar(M)
    yan = {"meta": meta(a, {"dondurulmus_cagri_argv": argv, "dondurulmus_cikti": a.cikti,
                            "dondurulmus_cikti_sha256": sha256(a.cikti)}),
           "temiz_dogruluk_yuzde": td,
           "karistirici_notu": ("E1: C1 ViT-Tiny CIFAR-100 temiz dogrulugu panelden belirgin dusuktur; w ve "
                                "hedef-dogru payda farkli bir alt kumeye dayanir. Sinirlilik olarak yazilir; "
                                "bu dosya yalniz bu kosudaki temiz dogruluklari betimsel verir."),
           "dondurulmus_ozet": {"panel": sonuc.get("panel"), "hata": sonuc.get("hata"),
                                "karar": (sonuc.get("b2") or {}).get("F_B2", {}).get("karar")}}
    if a.sinama:
        yan["SINAMA_SONUC_DEGIL"] = True
    yaz(str(a.cikti) + ".sarmalayici.json", yan)
    return yan


# ----------------------------------------------------------------------------------------------
# B8
# ----------------------------------------------------------------------------------------------
def b8_ciftler(tablo, mevcut, in_ciftleri, scr_ciftleri):
    """Ciftler hucre tablosunun b2_tohum_ciftleri alanindan (dondurulmus sema); cift numarasi CNN
    uyesinin 'tohum' alanidir. Ek on kayit §5.6: IN satiri = Singh ciftleri (1, 2), scr satiri = Liu (3)."""
    out = []
    for cnn, vit in tablo.get("b2_tohum_ciftleri", []):
        k = tablo["modeller"][cnn].get("tohum")
        satir = "IN" if k in in_ciftleri else ("scr" if k in scr_ciftleri else "diger")
        out.append({"cift": k, "cnn": cnn, "donusturucu": vit, "satir": satir,
                    "mevcut": cnn in mevcut and vit in mevcut})
    return out


def b8_etiket(est, ci90, ci95, cift_degerleri, esik, delta):
    """Ek on kayit §5.6 betimsel etiketleri (karar degildir); sirali denetim."""
    if ci90 is None:
        return "hesaplanamadi"
    if ci90[0] > -delta and ci90[1] < delta:
        return "IN satirinda ihmal edilebilir mimari farki" if esik == -0.10 else "ihmal edilebilir mimari farki"
    if est <= esik and all(v < 0 for v in cift_degerleri) and ci90[1] < 0:
        return "beklentiyle uyumlu"
    if est > 0 and ci95[0] > 0:
        return "ters yon"
    return "belirsiz"


def b8(a):
    dm = dondurulmus()
    tablo = dm.tablo_oku(a.hucre_tablosu)
    M = matris_yukle(a.matris_dizini, tablo)
    mevcut = set(M.modeller())
    P, P2, eksik = dm.paneller(tablo, mevcut)
    out = {"etiket": "KESIFSEL / BETIMSEL: IN satirinin dogal olcekte kestirimi; Holm ailesi yok, karar yok",
           "meta": meta(a, {"bootstrap_B": a.bootstrap, "bootstrap_tohum": a.bootstrap_tohum}),
           "veri": {"n_goruntu": M.n, "modeller": sorted(mevcut), "hucre_sayisi": len(M.h),
                    "tutarlilik": M.tutarlilik(), "cakismalar": M.cakisma,
                    "tablo_disi_modeller": sorted(mevcut - set(tablo["modeller"])),
                    "girdi_sha256": M.kaynaklar},
           "panel": {"birincil": P, "birincil_eksik": eksik, "ikincil": P2}}
    if a.sinama:
        out["SINAMA_SONUC_DEGIL"] = True
    if len(P) < a.panel_en_az:
        out["hata"] = f"birincil panelde {len(P)} uye var; en az {a.panel_en_az} gerekir"
        yaz(a.cikti, out)
        return out
    g = dm.Alici(M)
    mt = dm.model_tablosu(g, sorted(mevcut & set(tablo["modeller"])), P, M)
    td = temiz_dogruluklar(M)
    ozet = {}
    for m, r in mt.items():
        if "eksik_hucreler" in r:
            ozet[m] = r
            continue
        b = r["yari_log"]
        ozet[m] = {"sigma": b["sigma"], "rho": b["rho"], "S": b["S"], "omega_log_w": b["omega"],
                   "w_yuzde": float(np.exp(b["omega"])), "temiz_dogruluk_yuzde": td.get(m),
                   "hucre": tablo["modeller"].get(m, {}).get("hucre"), "panel_n": b["panel_n"],
                   "sigma_logit": r["yari_logit"]["sigma"], "rho_logit": r["yari_logit"]["rho"],
                   "sigma_tam": r["tam_log"]["sigma"], "rho_tam": r["tam_log"]["rho"]}
    out["model_tablosu_ozet"] = ozet
    out["model_tablosu_tam"] = mt
    ciftler = b8_ciftler(tablo, mevcut, a.in_ciftleri, a.scr_ciftleri)
    W = dm.bootstrap_agirlik(M.n, a.bootstrap, np.random.default_rng(a.bootstrap_tohum))
    gb = dm.Alici(M, W)
    cift_out, satirlar = [], {}
    for c in ciftler:
        rec = dict(c)
        if not c["mevcut"]:
            rec["durum"] = "eksik model"
            cift_out.append(rec)
            continue
        try:
            sv = dm.model_duzeyi(g, c["donusturucu"], P)
            sc = dm.model_duzeyi(g, c["cnn"], P)
            svl = dm.model_duzeyi(g, c["donusturucu"], P, "logit")
            scl = dm.model_duzeyi(g, c["cnn"], P, "logit")
            bv = dm.model_duzeyi(gb, c["donusturucu"], P)["sigma"]
            bc = dm.model_duzeyi(gb, c["cnn"], P)["sigma"]
        except KeyError as e:
            rec["durum"] = f"eksik hucre: {e}"
            cift_out.append(rec)
            continue
        A = float(sv["sigma"] - sc["sigma"])
        dist = np.asarray(bv - bc, float)
        rec.update({"A_sigma": A, "A_sigma_logit": float(svl["sigma"] - scl["sigma"]),
                    "A_rho": float(sv["rho"] - sc["rho"]),
                    "A_omega_log_w": float(sv["omega"] - sc["omega"]),
                    "goruntu_bootstrap_ci90": [float(np.percentile(dist, 5)), float(np.percentile(dist, 95))],
                    "goruntu_bootstrap_ci95": [float(np.percentile(dist, 2.5)), float(np.percentile(dist, 97.5))],
                    "durum": "hesaplandi"})
        cift_out.append(rec)
        satirlar.setdefault(c["satir"], []).append((c["cift"], A, dist))
    out["ciftler"] = cift_out

    def ozetle(kayit, esik):
        if not kayit:
            return {"not": "hesaplanan cift yok"}
        As = [A for _, A, _ in kayit]
        mb = np.mean(np.vstack([d for _, _, d in kayit]), axis=0)
        ci90 = [float(np.percentile(mb, 5)), float(np.percentile(mb, 95))]
        ci95 = [float(np.percentile(mb, 2.5)), float(np.percentile(mb, 97.5))]
        o = {"ciftler": [k for k, _, _ in kayit], "cift_degerleri": As, "kestirim": float(np.mean(As)),
             "goruntu_bootstrap": {"B": a.bootstrap, "tohum": a.bootstrap_tohum, "ci90": ci90, "ci95": ci95,
                                   "not": "ortak goruntu agirliklari; cift kumesi sabit; yalniz goruntu belirsizligi"},
             "beklenti_esigi": esik,
             "betimsel_etiket": b8_etiket(float(np.mean(As)), ci90, ci95, As, esik, dm.DELTA),
             "nokta_beklenti_esiginde_ya_da_altinda": bool(np.mean(As) <= esik)}
        if len(As) == 2:
            o["iki_cift_farki"] = float(As[1] - As[0])
            o["not"] = "iki ciftle df 1; ciftler arasi t araligi kurulmaz (ek on kayit §5.6)"
        elif len(As) > 2:
            o["t_araligi_ciftler_uzerinden"] = dm.tek_orneklem(As)
        return o

    out["A_sigma_IN"] = {"tanim": "A^sigma_IN = ort_k [sigma(donusturucu_k) - sigma(CNN_k)], P8, bolunmus yari, log; "
                                  "IN satiri yalniz --in-ciftleri (varsayilan Singh 1, 2)",
                         "beklenti": f"<= {BEKLENTI_A_SIGMA_IN}, iki ciftte de negatif (dondurulmus H1+H2; karar degil)",
                         **ozetle(satirlar.get("IN", []), BEKLENTI_A_SIGMA_IN)}
    out["A_sigma_scr_Liu"] = {"tanim": "ayni nicelik --scr-ciftleri icin (varsayilan Liu 3); 2x2'nin scr satiri",
                              "beklenti": "<= -0,20 (H1'in ongorulen buyuklugu; karar degil)",
                              **ozetle(satirlar.get("scr", []), -0.20)}
    rho_ayri = {}
    for m in tablo["modeller"]:
        if tablo["modeller"][m].get("hucre") == "V-scr" and m in ozet and "rho" in ozet[m]:
            rho_ayri[m] = {"rho": ozet[m]["rho"], "sigma": ozet[m]["sigma"]}
    out["donusturucu_rho_ayri_ayri"] = rho_ayri
    try:
        out["hodge_r_kesifsel"] = dm.hodge_r(g, M, sorted(mevcut))
    except Exception as e:  # noqa: BLE001
        out["hodge_r_kesifsel"] = {"hata": repr(e)}
    yaz(a.cikti, out)
    return out


# ----------------------------------------------------------------------------------------------
# B10 aile birlestirme
# ----------------------------------------------------------------------------------------------
def b10(a):
    dm = dondurulmus()
    kayit = {}
    for y in a.mantel:
        d = json.loads(Path(y).read_text(encoding="utf-8"))
        kayit[d.get("veri_kumesi", Path(y).stem)] = {"dosya": y, "sha256": sha256(y), "d": d}
    adlar = sorted(kayit)
    out = {"meta": meta(a), "veri_kumeleri": adlar}
    # F_B10 (ek on kayit §6.2-6.3): veri kumesi x {ham, ana etki artigi}; alti sinama, Holm
    aile, pler = [], []
    for k in adlar:
        for anahtar, ad, ongoru in (("ham", "H10", 0.50), ("ana_etki_artik", "H10k", 0.30)):
            s = kayit[k]["d"].get("sinamalar", {}).get(anahtar, {})
            aile.append({"sinama": f"{ad}-{k}", "istatistik": s.get("istatistik"), "p_tek_ham": s.get("p_tek"),
                         "perm": s.get("perm"), "ongorulen_buyukluk": ongoru})
            pler.append(s.get("p_tek"))
    adj, p1 = dm.holm_aile(pler)
    for x, ph in zip(aile, adj):
        x["p_holm"] = ph
        r, p = x["istatistik"], x["p_tek_ham"]
        if r is None or p is None or not np.isfinite(r):
            x["karar"] = "hesaplanamadi"
        elif r <= 0.20 and p >= 0.20:
            x["karar"] = "curutuldu"
        elif ph < dm.ALFA:
            x["karar"] = "destek"
        else:
            x["karar"] = "kararsiz"
        x["ongorulen_buyukluk_tuttu"] = bool(r is not None and np.isfinite(r) and r >= x["ongorulen_buyukluk"])
    out["F_B10"] = {"sinamalar": aile, "aile_buyuklugu": len(aile), "p_1_sayilan": [aile[i]["sinama"] for i in p1],
                    "kural": "ek on kayit §6.3: (i) kestirim <= 0,20 ve ham p >= 0,20 ise curutuldu; "
                             "(ii) Holm sonrasi p < 0,05 ise destek; (iii) kalan kararsiz"}
    if len(adlar) != 3:
        out["F_B10"]["uyari"] = f"aile uc veri kumesi bekler, {len(adlar)} verildi"
    farkli_perm = sorted({x["sinama"] for x in aile if x["perm"] != PERM_ON_KAYIT})
    if farkli_perm:  # ek on kayit §6.2: 9999 permutasyon; farkliysa sapma kaydina yazilmali
        out["F_B10"]["perm_uyarisi"] = f"{PERM_ON_KAYIT} disinda permutasyonla uretilmis sinamalar: {farkli_perm}"
    for anahtar in ("kismi_omega", "kismi_omega_gradnorm"):
        out[f"kesifsel_{anahtar}"] = {k: kayit[k]["d"].get("sinamalar", {}).get(anahtar) for k in adlar}
    out["girdiler"] = {k: {"dosya": v["dosya"], "sha256": v["sha256"]} for k, v in kayit.items()}
    if a.sinama:
        out["SINAMA_SONUC_DEGIL"] = True
    yaz(a.cikti, out)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mod", required=True, choices=["b8", "b9", "b10"])
    ap.add_argument("--matris-dizini", action="append", default=[])
    ap.add_argument("--hucre-tablosu", default=None)
    ap.add_argument("--mantel", nargs="*", default=[])
    ap.add_argument("--cikti", required=True)
    ap.add_argument("--bootstrap", type=int, default=2000)
    ap.add_argument("--panel-en-az", type=int, default=5)
    ap.add_argument("--bootstrap-tohum", type=int, default=20261030, help="B8 goruntu bootstrap'i (ek on kayit §5.6)")
    ap.add_argument("--in-ciftleri", type=int, nargs="*", default=[1, 2])
    ap.add_argument("--scr-ciftleri", type=int, nargs="*", default=[3])
    ap.add_argument("--sinama", action="store_true")
    a = ap.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    if a.mod in ("b8", "b9") and (not a.matris_dizini or not a.hucre_tablosu):
        raise SystemExit("--matris-dizini ve --hucre-tablosu gerekir")
    if a.mod == "b10" and not a.mantel:
        raise SystemExit("--mantel JSON listesi gerekir")
    return {"b8": b8, "b9": b9, "b10": b10}[a.mod](a)


if __name__ == "__main__":
    main()
