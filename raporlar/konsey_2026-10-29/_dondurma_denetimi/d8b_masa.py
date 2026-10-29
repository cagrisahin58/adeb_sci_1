#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
K = "/home/firat/projects/adeb_sci_1/"
d = json.load(open(K + "results/q1/konsey_masa/konsey_masa_cozumlemeleri.json"))
m = d["1_havuz_model_tablosu"]["modeller"]
print("ViT kaynak_acigi_R_eksi_m_yari_log:", json.dumps(m["ViT_Tiny_AT_s2001"]["kaynak_acigi_R_eksi_m_yari_log"], ensure_ascii=False))
print("ViT diger anahtarlar:", list(m["ViT_Tiny_AT_s2001"].keys()))
for olc in ["yari_log", "tam_log", "yari_logit", "yari_oran"]:
    rv = m["ViT_Tiny_AT_s2001"][olc]["rho"]
    rr = m["ResNet18_AT_s1001"][olc]["rho"]
    print(olc, "rho_V - rho_R =", rv - rr, " sigma_R =", m["ResNet18_AT_s1001"][olc]["sigma"], " sigma_V =", m["ViT_Tiny_AT_s2001"][olc]["sigma"])

# 0,061 degeri JSON'da nerede gecer
def ara(o, yolu=""):
    if isinstance(o, dict):
        for k, v in o.items():
            ara(v, yolu + "." + k if yolu else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            ara(v, yolu + "." + str(i))
    elif isinstance(o, float):
        if 0.0605 <= abs(o) < 0.0625 or 0.9265 <= abs(o) < 0.9285:
            print("  ", yolu, "=", o)

for f in ["results/q1/konsey_masa/konsey_masa_cozumlemeleri.json", "results/q1/konsey_masa/konsey_ayrisim_masa.json", "results/q1/konsey_sentez_r_tau_masa.json"]:
    print("== ", f)
    o = json.load(open(K + f))
    # noktalar listesini atla
    if "noktalar" in str(type(o)):
        pass
    ara(o)

s = json.load(open(K + "results/q1/konsey_sentez_r_tau_masa.json"))
print("sentez havuz_tohum1:", json.dumps(s["havuz_tohum1"], ensure_ascii=False)[:1500])
for k, v in s["kumeler"].items():
    for orn in v:
        if isinstance(v[orn], dict) and "log_tau" in v[orn]:
            print(k, orn, "log_tau sd_kosum", v[orn]["log_tau"].get("sd_kosum"), "r sd", v[orn].get("r", {}).get("sd_kosum"))
