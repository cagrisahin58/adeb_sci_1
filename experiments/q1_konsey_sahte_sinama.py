# -*- coding: utf-8 -*-
"""q1_konsey_ayrisim.py icin uctan uca kod sinamasi (SAHTE 2x2). SONUC DEGILDIR.

C1 modellerinin mevcut matrisleri (results/c1_c3/pair1-3: secilen kontrol noktasi; results/q1/son_kontrol_noktasi/
pair1-3: son kontrol noktasi) gecici takma adlarla 2x2 hucrelerine yerlestirilir. Panel yalniz bu klasorlerde
ortak olan Gowal2020Uncovering_28_10_extra'dir (tek uye; --panel-en-az 1). Amac kod yolunun uctan uca
calistigini, eksik hucrelerin dogru raporlandigini ve istatistik yardimcilarinin bilinen degerleri
verdigini gostermektir.
Cikti: results/q1/konsey_sahte_2x2_sinama.json (en ust anahtar SINAMA_SONUC_DEGIL: true)
"""
import io
import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "experiments"))
sys.path.insert(0, str(KOK))
import q1_konsey_ayrisim as A  # noqa: E402

CIKTI = KOK / "results" / "q1" / "konsey_sahte_2x2_sinama.json"
ARA = KOK / "results" / "q1" / "_konsey_sahte"
G = "Gowal2020Uncovering_28_10_extra"

esleme = {}
for k in (1, 2, 3):
    esleme[f"results/c1_c3/pair{k}"] = {"ResNet18_AT": f"Rb{k}", "ViT_Tiny_AT": f"Vb{k}", "WRN_28_10": G}
    esleme[f"results/q1/son_kontrol_noktasi/pair{k}"] = {"ResNet18_AT": f"Rl{k}", "ViT_Tiny_AT": f"Vl{k}", "WRN_28_10": G}
ad = {"Vb1": "ViT_Tiny_AT_s2001", "Vb2": "ViT_Tiny_AT_s2002", "Vb3": "ViT_Tiny_AT_s2003",
      "Rb1": "SAHTE_R224_scr_a", "Rb2": "SAHTE_R224_scr_b",
      "Vl1": "SAHTE_V_IN_a", "Vl2": "SAHTE_V_IN_b",
      "Rl1": "SAHTE_R224_IN_a", "Rl2": "SAHTE_R224_IN_b",
      "Rb3": "ResNet18_AT_s1003", "Rl3": "SAHTE_C1R32_b",
      "Vl3": "SAHTE_ikincil_Vl3"}
for d in esleme.values():
    for k, v in list(d.items()):
        d[k] = ad.get(v, v)
gercek = {"Vb": "C1 ViT secilen", "Rb": "C1 ResNet secilen", "Vl": "C1 ViT son", "Rl": "C1 ResNet son"}


def m(h, tohum, kaynak, panel=False, ik=False):
    return {"hucre": h, "tohum": tohum, "aile": "SAHTE", "birincil_panel": panel, "ikincil_panel": ik,
            "gercek_kimlik": kaynak}


tablo = {
    "SINAMA_SONUC_DEGIL": True,
    "aciklama": "SAHTE hucre tablosu: yalniz kod sinamasi icin; gercek_kimlik alani modelin ne oldugunu soyler.",
    "modeller": {
        "ViT_Tiny_AT_s2001": m("V-scr", 2001, "C1 ViT s2001 best"),
        "ViT_Tiny_AT_s2002": m("V-scr", 2002, "C1 ViT s2002 best"),
        "ViT_Tiny_AT_s2003": m("V-scr", 2003, "C1 ViT s2003 best"),
        "SAHTE_V_IN_a": m("V-IN", 1, "C1 ViT s2001 son kontrol noktasi"),
        "SAHTE_V_IN_b": m("V-IN", 2, "C1 ViT s2002 son kontrol noktasi"),
        "SAHTE_R224_scr_a": m("R224-scr", 1, "C1 ResNet s1001 best"),
        "SAHTE_R224_scr_b": m("R224-scr", 2, "C1 ResNet s1002 best"),
        "SAHTE_R224_IN_a": m("R224-IN", 1, "C1 ResNet s1001 son kontrol noktasi"),
        "SAHTE_R224_IN_b": m("R224-IN", 2, "C1 ResNet s1002 son kontrol noktasi"),
        "ResNet18_AT_s1003": m("C1-R32", 1003, "C1 ResNet s1003 best"),
        "SAHTE_C1R32_b": m("C1-R32", 1004, "C1 ResNet s1003 son kontrol noktasi"),
        "SAHTE_ikincil_Vl3": m("ikincil_panel", None, "C1 ViT s2003 son kontrol noktasi", ik=True),
        G: m("panel", None, "RobustBench Gowal2020 (C1 C3 referansi)", panel=True),
    },
    "b2_tohum_ciftleri": [["ResNet18_AT_s1003", "ViT_Tiny_AT_s2003"], ["SAHTE_C1R32_b", "ViT_Tiny_AT_s2001"]],
    "s4_ciftleri": [["SAHTE_R224_scr_a", "ViT_Tiny_AT_s2001"], ["SAHTE_R224_scr_b", "ViT_Tiny_AT_s2002"],
                    ["SAHTE_R224_IN_a", "SAHTE_V_IN_a"], ["SAHTE_R224_IN_b", "SAHTE_V_IN_b"]],
    "dizin_takma_ad_esleme": esleme,
}


def birim_sinamalari():
    out = {}
    # Holm: bilinen ornek
    adj = A.holm([0.01, 0.04, 0.03])
    out["holm"] = {"girdi": [0.01, 0.04, 0.03], "cikti": adj, "beklenen": [0.03, 0.06, 0.06],
                   "gecti": bool(np.allclose(adj, [0.03, 0.06, 0.06]))}
    # Birlesik varyansli iki hucre karsitligi = scipy ttest_ind (esit varyans)
    rng = np.random.default_rng(1)
    a, b = rng.normal(0, 1, 3), rng.normal(0.5, 1, 2)
    k = A.karsitlik({"a": list(a), "b": list(b)}, {"a": 1.0, "b": -1.0}, ["a", "b"])
    t = stats.ttest_ind(a, b, equal_var=True)
    out["birlesik_t"] = {"karsitlik_p_iki": k["p_iki"], "scipy_p": float(t.pvalue),
                         "gecti": bool(abs(k["p_iki"] - t.pvalue) < 1e-12)}
    w = stats.ttest_ind(a, b, equal_var=False)
    se = k["welch"]["se"]
    pw = 2 * (1 - stats.t.cdf(abs(k["kestirim"] / se), k["welch"]["df"]))
    out["welch"] = {"p": float(pw), "scipy_p": float(w.pvalue), "gecti": bool(abs(pw - w.pvalue) < 1e-10)}
    # Etkilesim carpani 3,2,2,2 hucrelerde sqrt(1/3 + 3/2) (ON_KAYIT §5)
    d = {"V-scr": [0, 1, 2], "V-IN": [0, 1], "R224-scr": [0, 1], "R224-IN": [0, 1]}
    kk = A.karsitlik(d, A.K_H2, A.HUC4)
    out["etkilesim_carpani"] = {"carpan": kk["carpan"], "beklenen": float(np.sqrt(1 / 3 + 3 / 2)), "df": kk["df"],
                                "gecti": bool(abs(kk["carpan"] - np.sqrt(1 / 3 + 3 / 2)) < 1e-12 and kk["df"] == 5)}
    # TOST: 90% aralik +-delta icindeyse TOST p < 0,05 (esdegerlik)
    x = A.tek_orneklem([0.01, -0.02, 0.015, 0.0])
    p, _, _ = A.tost_p(x["ort"], x["se"], x["df"])
    out["tost_aralik_denkligi"] = {"ci90": x["ci90"], "tost_p": p,
                                   "gecti": bool((p < 0.05) == A.icinde(x["ci90"]))}
    # --- 29.10 dogrulayici duzeltmeleri: karar kurallarinin ayrikligi (sentetik sayilar, SONUC DEGIL) ---
    # Holm ailesinde hesaplanamayan p = 1 sayilir, aile buyuklugu 3 kalir
    adj, p1 = A.holm_aile([0.01, float("nan"), 0.02])
    out["holm_eksik_p_1"] = {"cikti": adj, "beklenen": [0.03, 1.0, 0.04], "p1_indeks": p1,
                             "gecti": bool(np.allclose(adj, [0.03, 1.0, 0.04]) and p1 == [1])}
    # H1: anlamli ama +-0,10 icinde (dogrulayicinin ornegi) -> curutuldu (esdeger), bolge O2
    rho0 = {h: [0.001 * i for i in range(n)] for h, n in (("V-scr", 3), ("R224-scr", 2), ("V-IN", 2), ("R224-IN", 2))}
    s1 = {"V-scr": [-0.80, -0.81, -0.79], "R224-scr": [-0.74, -0.745], "V-IN": [-0.70, -0.705], "R224-IN": [-0.60, -0.605]}
    k1 = A.b4_karsitliklar(s1, rho0)
    kr1 = A.b4_karar(k1, k1)
    out["H1_ortusme_ayrik"] = {"A_sigma_scr": k1["H1"]["kestirim"], "ci90": k1["H1"]["ci90"], "p_holm": kr1["p_holm"][0],
                               "karar": kr1["H1"], "bolge": kr1["sonuc_bolgesi"],
                               "gecti": bool(kr1["H1"] == "curutuldu (esdeger)" and kr1["sonuc_bolgesi"] == "O2")}
    # H2: anlamli ama +-0,10 icinde -> curutuldu (esdeger); H1 destek -> bolge O3 (tek bolge)
    s2 = {"V-scr": [-0.80, -0.805, -0.795], "R224-scr": [-0.60, -0.601], "V-IN": [-0.65, -0.651], "R224-IN": [-0.50, -0.501]}
    k2 = A.b4_karsitliklar(s2, rho0)
    kr2 = A.b4_karar(k2, k2)
    out["H2_ortusme_ayrik"] = {"I_sigma": k2["H2"]["kestirim"], "ci90": k2["H2"]["ci90"], "p_holm": kr2["p_holm"][1],
                               "H1": kr2["H1"], "H2": kr2["H2"], "H3": kr2["H3"], "bolge": kr2["sonuc_bolgesi"],
                               "gecti": bool(kr2["H2"] == "curutuldu (esdeger)" and kr2["sonuc_bolgesi"] == "O3")}
    # Sonuc haritasi: butun etiket bilesimlerinde tam bir bolge
    E1 = ["destek", "curutuldu (esdeger)", "curutuldu (ters yon)", "kararsiz", "hesaplanamadi"]
    E2 = E1 + ["kararsiz (logit olceginde isaret tersine donuyor)"]
    E3 = ["destek (esdeger, Holm sonrasi TOST p < 0,05)", "curutuldu", "kararsiz", "hesaplanamadi"]
    say, bolgeler = 0, set()
    for a in E1:
        for b in E2:
            for c in E3:
                for nh in (False, True):
                    sb = A.sonuc_bolgesi(a, b, c, nh and b == "curutuldu (ters yon)")
                    assert isinstance(sb["bolge"], str)
                    bolgeler.add(sb["bolge"])
                    say += 1
    out["sonuc_haritasi_kapsam"] = {"bilesim": say, "bolgeler": sorted(bolgeler), "gecti": True}
    # K-b: negatif yonde buyuk ve anlamli -> curutuldu (negatif yon)
    kb = A.tek_orneklem([-0.20, -0.21, -0.19])
    kb["tost_p"] = A.tost_p(kb["ort"], kb["se"], kb["df"])[0]
    kr = A.b2_karar({"D": [0.4, 0.4, 0.4], "payda_kucuk_tohumlar": []}, A.tek_orneklem([0.9, 0.92, 0.91]), kb,
                    {}, [0.01, 1.0, 1.0], A.DELTA)
    out["K-b_negatif_curutme"] = {"karar": kr["K-b"], "gecti": bool(kr["K-b"] == "curutuldu (negatif yon)")}
    # K-a: bir tohumda D_s <= 0,10 -> kararsiz (payda kucuk)
    kr = A.b2_karar({"D": [0.4, 0.05, 0.4], "payda_kucuk_tohumlar": [1]}, A.tek_orneklem([0.9, 3.0, 0.91]), kb,
                    {}, [1.0, 1.0, 1.0], A.DELTA)
    out["K-a_payda_kurali"] = {"karar": kr["K-a"], "gecti": kr["K-a"].startswith("kararsiz (payda")}
    return out


def main():
    ARA.mkdir(parents=True, exist_ok=True)
    ty = ARA / "sahte_hucre_tablosu.json"
    with io.open(ty, "w", encoding="utf-8", newline="\n") as f:
        json.dump(tablo, f, ensure_ascii=False, indent=1)
    dz = []
    for k in (1, 2, 3):
        dz += ["--matris-dizini", f"results/c1_c3/pair{k}", "--matris-dizini", f"results/q1/son_kontrol_noktasi/pair{k}"]
    sonuc = {"SINAMA_SONUC_DEGIL": True,
             "aciklama": "Kod sinamasi. Hucre etiketleri SAHTEDIR; sayilar hicbir hipotez icin kanit degildir.",
             "sahte_hucre_tablosu": str(ty.relative_to(KOK)), "birim_sinamalari": birim_sinamalari()}
    for mod in ("b2", "b4"):
        c = ARA / f"sahte_{mod}.json"
        r = A.main(["--mod", mod, *dz, "--hucre-tablosu", str(ty), "--cikti", str(c), "--panel-en-az", "1", "--sinama"])
        sonuc[mod] = json.loads(c.read_text(encoding="utf-8"))
    # K-c kod yolu: tek klasorde (C1 cift 1) ResNet ve ViT'yi ayni sahte "V-scr" hucresine koyarak tur ici
    # hucre ve hiyerarsik bootstrap yolunu calistir.
    t3 = {"SINAMA_SONUC_DEGIL": True, "aciklama": "K-c kod yolu sinamasi; SAHTE",
          "modeller": {"SAHTE_Va": m("V-scr", 1, "C1 ViT s2001 best"), "SAHTE_Vb": m("V-scr", 2, "C1 ResNet s1001 best"),
                       G: m("panel", None, "RobustBench Gowal2020", panel=True)},
          "b2_tohum_ciftleri": [],
          "dizin_takma_ad_esleme": {"results/c1_c3/pair1": {"ViT_Tiny_AT": "SAHTE_Va", "ResNet18_AT": "SAHTE_Vb",
                                                            "WRN_28_10": G}}}
    ty3 = ARA / "sahte_hucre_tablosu_kc.json"
    with io.open(ty3, "w", encoding="utf-8", newline="\n") as f:
        json.dump(t3, f, ensure_ascii=False, indent=1)
    c = ARA / "sahte_b2_kc.json"
    A.main(["--mod", "b2", "--matris-dizini", "results/c1_c3/pair1", "--hucre-tablosu", str(ty3), "--cikti", str(c),
            "--panel-en-az", "1", "--sinama"])
    sonuc["b2_kc_yolu"] = json.loads(c.read_text(encoding="utf-8"))
    # B5 kod yolu (29.10 dogrulayici duzeltmesi): C1 secilen kontrol noktasi matrisleri "pgd", son kontrol
    # noktasi matrisleri SAHTE olarak "mi" etiketlenir; gercek bir MI-PGD sonucu DEGILDIR.
    t5 = {"SINAMA_SONUC_DEGIL": True, "aciklama": "B5 kod yolu sinamasi; SAHTE saldiri etiketi",
          "modeller": {G: m("panel", None, "RobustBench Gowal2020", panel=True)},
          "dizin_takma_ad_esleme": {}, "dizin_saldiri_esleme": {}}
    dz5 = []
    for k in (1, 2, 3):
        t5["modeller"][f"ResNet18_AT_s100{k}"] = dict(m("C1-R32", 1000 + k, f"C1 ResNet s100{k}"), aile="CNN")
        t5["modeller"][f"ViT_Tiny_AT_s200{k}"] = dict(m("V-scr", 2000 + k, f"C1 ViT s200{k}"), aile="ViT")
        for d, sal in ((f"results/c1_c3/pair{k}", "pgd"), (f"results/q1/son_kontrol_noktasi/pair{k}", "mi")):
            t5["dizin_takma_ad_esleme"][d] = {"ResNet18_AT": f"ResNet18_AT_s100{k}", "ViT_Tiny_AT": f"ViT_Tiny_AT_s200{k}",
                                             "WRN_28_10": G}
            t5["dizin_saldiri_esleme"][d] = sal
            dz5 += ["--matris-dizini", d]
    ty5 = ARA / "sahte_hucre_tablosu_b5.json"
    with io.open(ty5, "w", encoding="utf-8", newline="\n") as f:
        json.dump(t5, f, ensure_ascii=False, indent=1)
    c = ARA / "sahte_b5.json"
    A.main(["--mod", "b5", *dz5, "--hucre-tablosu", str(ty5), "--cikti", str(c), "--panel-en-az", "1", "--sinama"])
    sonuc["b5_yolu"] = json.loads(c.read_text(encoding="utf-8"))
    # B6 maskeleme kurali kod yolu: sahte V-IN'in bir uyesi isaretli -> hucre n < 2 yolu
    sonuc["b4_maskeleme_yolu"] = {}
    for isaret in ("ViT_Tiny_AT_s2003", "SAHTE_V_IN_a"):
        c = ARA / f"sahte_b4_maskeleme_{isaret}.json"
        A.main(["--mod", "b4", *dz, "--hucre-tablosu", str(ty), "--cikti", str(c), "--panel-en-az", "1", "--sinama",
                "--bootstrap", "200", "--maskeleme-isaretli", isaret])
        sonuc["b4_maskeleme_yolu"][isaret] = json.loads(c.read_text(encoding="utf-8")).get("b4", {}).get(
            "F_B4", {}).get("maskeleme_kurali")
    # Ozdeslik denetimi: K-a'da D = simetrik + yonlu
    ka = sonuc["b2"].get("b2", {}).get("F_B2", {}).get("K-a", {})
    sonuc["ozdeslik_artik_max_Ka"] = ka.get("ozdeslik_artik_max")
    with io.open(CIKTI, "w", encoding="utf-8", newline="\n") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=1)
    print("birim:", {k: v["gecti"] for k, v in sonuc["birim_sinamalari"].items()})
    print("yazildi:", CIKTI)


if __name__ == "__main__":
    main()
