#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plan 12 ve ON_KAYIT 1'deki masa sayilarini kaynak JSON'dan yeniden oku."""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
K = "/home/firat/projects/adeb_sci_1/"
d = json.load(open(K + "results/q1/konsey_masa/konsey_masa_cozumlemeleri.json"))


def yol(obj, p):
    for k in p.split("."):
        if isinstance(obj, list):
            obj = obj[int(k)]
        else:
            obj = obj[k]
    return obj


def goster(p, obj=d):
    try:
        v = yol(obj, p)
        if isinstance(v, (dict, list)):
            s = json.dumps(v, ensure_ascii=False)
            print(p, "=", s[:700])
        else:
            print(p, "=", v)
    except Exception as e:
        print(p, "HATA", type(e).__name__, e)


print("ust anahtarlar:", list(d.keys()))
h = d["1_havuz_model_tablosu"]
print("havuz anahtarlar:", list(h.keys()))
print("modeller:", list(h["modeller"].keys()))
goster("1_havuz_model_tablosu.modeller.ViT_Tiny_AT_s2001")
goster("1_havuz_model_tablosu.jackknife_aralik.ViT_Tiny_AT_s2001")
for m in h["modeller"]:
    try:
        print(m, "yari_log.rho", h["modeller"][m]["yari_log"]["rho"], "yari_logit.rho", h["modeller"][m]["yari_logit"]["rho"])
    except Exception as e:
        print(m, "rho HATA", e)
for k in ["panel", "panel_uyeleri", "P"]:
    if k in h:
        print("panel:", h[k])
print("--- 2_hodge_r ---")
hr = d["2_hodge_r"]
print("anahtarlar:", list(hr.keys()))
goster("2_hodge_r.yari_log.G_potansiyel_payi")
goster("2_hodge_r.yari_log.RV_cifti")
goster("2_hodge_r.yari_logit.RV_cifti")
goster("2_hodge_r.yari_logit.G_potansiyel_payi")
print("--- 3_mahmood ---")
goster("3_mahmood.etiket")
print("3_mahmood anahtarlar:", list(d["3_mahmood"].keys()))
print("--- 4_potansiyel_payi ---")
print("anahtarlar:", list(d["4_potansiyel_payi"].keys()))
goster("4_potansiyel_payi.ozet.svhn_linf_secilen.r.degerler")
goster("4_potansiyel_payi.ozet.svhn_linf_secilen")
print("--- 5 ---")
print(list(d.get("5_onerme3_h_olcegi", {}).keys()))

print("=== konsey_ayrisim_masa.json ===")
a = json.load(open(K + "results/q1/konsey_masa/konsey_ayrisim_masa.json"))
print("anahtarlar:", list(a.keys()))
def ara(o, hedef, yolu=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yeni = yolu + "." + k if yolu else k
            if hedef in k:
                s = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
                print("  ", yeni, "=", str(s)[:300])
            ara(v, hedef, yeni)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            ara(v, hedef, yolu + "." + str(i))
for hedef in ["regresyon", "gecti", "simetrik_oran", "potansiyel_payi"]:
    print("ara:", hedef)
    ara(a, hedef)

print("=== delta_kaynagi.json ===")
print(json.dumps(json.load(open(K + "results/q1/konsey_masa/_dogrulayici/delta_kaynagi.json")), ensure_ascii=False)[:800])
print("=== _p3_carpimsal_yasa_masa havuz_AT7 ===")
p3 = json.load(open(K + "results/q1/konsey_masa/_p3_carpimsal_yasa_masa.json"))
goster("havuz_AT7.log_tau_simetri_ihlali_rms", p3)
goster("A_kolu", p3)
print("=== sentez ===")
s = json.load(open(K + "results/q1/konsey_sentez_r_tau_masa.json"))
print("anahtarlar:", list(s.keys()))
print(json.dumps(s, ensure_ascii=False)[:2500])
print("=== d5 temiz referans ===")
print(json.dumps(json.load(open(K + "results/q1/konsey_smoke/_dogrulayici/d5_temiz_referans.json")), ensure_ascii=False))
print("=== sahte 2x2 ===")
ss = json.load(open(K + "results/q1/konsey_sahte_2x2_sinama.json"))
goster("b2.b2.F_B2.K-b.degerler", ss)
goster("b2.b2.F_B2.K-a.q", ss)
goster("b5_yolu.b5.birincil_C1-R32_V-scr", ss)
print("=== kc3 ===")
kc = json.load(open(K + "results/q1/_konsey_sahte/sahte_b2_kc3.json"))
ara(kc, "yeniden")
