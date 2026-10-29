# -*- coding: utf-8 -*-
"""Bagimsiz yeniden hesabi SENTEZ, AYRISIM (betik ciktisi) ve MASA ile karsilastirir."""
import io
import json
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

B = json.load(open("results/q1/konsey_masa/_dogrulayici/bagimsiz_yeniden_hesap.json", encoding="utf-8"))
S = json.load(open("results/q1/konsey_sentez_r_tau_masa.json", encoding="utf-8"))
A = json.load(open("results/q1/konsey_masa/konsey_ayrisim_masa.json", encoding="utf-8"))
A2 = json.load(open("results/q1/konsey_masa/_dogrulayici/dogrulayici_ayrisim_masa.json", encoding="utf-8"))
M = json.load(open("results/q1/konsey_masa/konsey_masa_cozumlemeleri.json", encoding="utf-8"))

satir = []


def k(ad, bag, ref, kaynak):
    satir.append({"nicelik": ad, "bagimsiz": bag, "referans": ref, "fark": None if ref is None else bag - ref,
                  "kaynak": kaynak})


h = B["havuz"]
print("transfer_matrix.json cond_fooling ile en buyuk fark (2 ondalik):", B["havuz_T_transfer_matrix_json_ile_en_buyuk_fark"],
      "hucre", B["havuz_hucre_sayisi"])
hs = S["havuz_tohum1"]
k("w_ViT", h["w"]["ViT_Tiny_AT"], None, "")
k("w_ResNet", h["w"]["ResNet18_AT"], None, "")
for m, sk in (("ViT_Tiny_AT", "ViT_Tiny_AT"), ("ResNet18_AT", "ResNet18_AT"), ("Debenedetti2022_XCiT_S12", "Debenedetti2022_XCiT_S12")):
    k(f"sigma_{m} (tam, log)", h["tam_log"][m]["sigma"], hs[sk]["log_tau_ort"], f"SENTEZ havuz_tohum1.{sk}.log_tau_ort")
    k(f"rho_{m} (tam, log)", h["tam_log"][m]["rho"], hs[sk]["r_ort"], f"SENTEZ havuz_tohum1.{sk}.r_ort")
ay = h["tam_log"]["ayrisim_R_eksi_V"]
ka = hs["kaynak_acigi_ayristirma_log"]
for a, b in (("D", "toplam"), ("simetrik_pay", "simetrik_pay"), ("yonlu_pay", "yonlu_pay"), ("q", "simetrik_oran")):
    k(f"havuz kaynak acigi {a} (tam, log)", ay[a], ka[b], f"SENTEZ havuz_tohum1.kaynak_acigi_ayristirma_log.{b}")
k("havuz ozdeslik artigi (tam)", ay["ozdeslik_artik"], 0.0, "tanim geregi 0")
k("panel ici log tau ort", h["panel_ici_log_tau_ort_tam"], hs["panel_ici_log_tau"]["ort"], "SENTEZ havuz_tohum1.panel_ici_log_tau.ort")
k("r_RV havuz (tam)", h["RV_cifti_tam"]["r"], hs["ResNet18_ViT_cifti"]["r"], "SENTEZ havuz_tohum1.ResNet18_ViT_cifti.r")
# Bolunmus yari, on kayit tanimlari
bn = A["havuz_on_kayit_tanimlari"]["b2_nokta_tohum1"]
ayy = h["yari_log"]["ayrisim_R_eksi_V"]
for a in ("D", "simetrik_pay", "yonlu_pay", "q"):
    k(f"havuz {a} (yari, log)", ayy[a], bn["yari_log"][a], f"AYRISIM havuz_on_kayit_tanimlari.b2_nokta_tohum1.yari_log.{a}")
k("rho_V (yari, log)", h["yari_log"]["ViT_Tiny_AT"]["rho"], bn["yari_log"]["rho_V"], "AYRISIM ...yari_log.rho_V")
k("rho_V (yari, logit)", h["yari_logit"]["ViT_Tiny_AT"]["rho"], bn["yari_logit"]["rho_V"], "AYRISIM ...yari_logit.rho_V")
k("q (yari, logit)", h["yari_logit"]["ayrisim_R_eksi_V"]["q"], bn["yari_logit"]["q"], "AYRISIM ...yari_logit.q")
k("rho_V - rho_R (yari, logit)", h["yari_logit"]["ViT_Tiny_AT"]["rho"] - h["yari_logit"]["ResNet18_AT"]["rho"], None, "04 rapor: -0,095")
k("rho_V - rho_R (yari, log)", h["yari_log"]["ViT_Tiny_AT"]["rho"] - h["yari_log"]["ResNet18_AT"]["rho"], None, "04 rapor: +0,061")
k("sigma_V (yari, logit)", h["yari_logit"]["ViT_Tiny_AT"]["sigma"], None, "04 rapor tablo: -1,534")
k("rho_R (yari, logit)", h["yari_logit"]["ResNet18_AT"]["rho"], None, "04 rapor tablo: -0,170")
# jackknife
qs = [v["q"] for v in h["jackknife_yari_log"].values()]
k("jackknife q min", min(qs), 0.919, "04 rapor (1) metni")
k("jackknife q max", max(qs), 0.935, "04 rapor (1) metni")
# tablo 1 karsilastirmasi MASA
t1m = M["1_havuz_model_tablosu"]["modeller"]
ters = {"ResNet18_AT": "ResNet18_AT_s1001", "ViT_Tiny_AT": "ViT_Tiny_AT_s2001", "Wong2020_PRN18": "Wong2020Fast",
        "Engstrom2019_RN50": "Engstrom2019Robustness", "Carmon2019_WRN28_10": "Carmon2019Unlabeled",
        "Debenedetti2022_XCiT_S12": "Debenedetti2022Light_XCiT-S12", "Gowal2020_WRN28_10": "Gowal2020Uncovering_28_10_extra"}
mx = 0.0
for m, d in h["tablo1_yari_log"].items():
    mm = t1m[ters[m]]
    yl = mm["yari_log"]
    mx = max(mx, abs(d["sigma"] - yl["sigma"]), abs(d["rho"] - yl["rho"]))
    if "D" in d:
        ka_ = mm["kaynak_acigi_R_eksi_m_yari_log"]
        for a, b in (("D", "D"), ("simetrik_pay", "simetrik_pay"), ("yonlu_pay", "yonlu_pay"), ("q", "simetrik_oran")):
            if b in ka_:
                mx = max(mx, abs(d[a] - ka_[b]))
            else:
                print("MASA anahtar yok:", m, b, list(ka_)[:10])
k("04 tablo (1) yedi model sigma, rho, D, paylar, q en buyuk |fark|", mx, 0.0, "MASA 1_havuz_model_tablosu.modeller")
# C1 kumeleri
for ad in ("c10_c1_secilen", "c10_son_kontrol_noktasi", "c100_c1_secilen"):
    b, s = B["kumeler"][ad], S["kumeler"][ad]
    k(f"{ad} r ort (tam)", b["r_tam"]["ort"], s["tam_orneklem"]["r"]["ort"], f"SENTEZ kumeler.{ad}.tam_orneklem.r.ort")
    k(f"{ad} r sd (tam)", b["r_tam"]["sd"], s["tam_orneklem"]["r"]["sd_kosum"], f"SENTEZ ...r.sd_kosum")
    k(f"{ad} log_tau ort (tam)", b["log_tau_tam"]["ort"], s["tam_orneklem"]["log_tau"]["ort"], "SENTEZ ...log_tau.ort")
    k(f"{ad} log_tau sd (tam)", b["log_tau_tam"]["sd"], s["tam_orneklem"]["log_tau"]["sd_kosum"], "SENTEZ ...log_tau.sd_kosum")
    k(f"{ad} potansiyel payi ort", b["pot_payi_tam"]["ort"], s["tam_orneklem"]["potansiyel_payi"]["ort"], "SENTEZ ...potansiyel_payi.ort")
    k(f"{ad} r ort (yari)", b["r_yari"]["ort"], s["bolunmus_yari"]["r"]["ort"], "SENTEZ ...bolunmus_yari.r.ort")
    k(f"{ad} log_tau ort (yari)", b["log_tau_yari"]["ort"], s["bolunmus_yari"]["log_tau"]["ort"], "SENTEZ ...bolunmus_yari.log_tau.ort")
# Betik ciktisi ile dogrulayici kosusu ayni mi (zaman damgasi haric)


def duz(x, o=""):
    out = {}
    if isinstance(x, dict):
        for a, v in x.items():
            out.update(duz(v, f"{o}.{a}" if o else a))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            out.update(duz(v, f"{o}[{i}]"))
    else:
        out[o] = x
    return out


d1, d2 = duz(A), duz(A2)
farkli = [a for a in set(d1) | set(d2) if d1.get(a) != d2.get(a) and not a.startswith("meta.")]
farkli = [a for a in farkli if "dizin" not in a]
print("AYRISIM (06:22) ile dogrulayici kosusu arasinda farkli anahtar (meta/dizin haric):", len(farkli), farkli[:10])
print("regresyon (dogrulayici kosusu):", A2["regresyon"]["karsilastirilan"], A2["regresyon"]["en_buyuk_mutlak_fark"], A2["regresyon"]["gecti"])
for s_ in satir:
    f = s_["fark"]
    print(f"{s_['nicelik']:<60} {s_['bagimsiz']:+.6f}  ref {('' if s_['referans'] is None else format(s_['referans'], '+.6f')):>10}  "
          f"fark {('' if f is None else format(f, '+.2e'))}  {s_['kaynak']}")
with io.open("results/q1/konsey_masa/_dogrulayici/karsilastirma.json", "w", encoding="utf-8", newline="\n") as fh:
    json.dump({"satirlar": satir, "ayrisim_ile_dogrulayici_kosusu_farkli_anahtar": farkli}, fh, ensure_ascii=False, indent=1)
