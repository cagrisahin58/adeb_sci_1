"""Salt okur: 09_sonuc_b2_b6 raporundaki turetilmis sayilar (yalniz dondurulmus JSON'lardan aritmetik)."""
import json
import math
import sys

sys.stdout.reconfigure(encoding="utf-8")
b2 = json.load(open("results/q1/konsey_ayrisim_b2.json", encoding="utf-8"))
b4 = json.load(open("results/q1/konsey_ayrisim_b4.json", encoding="utf-8"))
b5 = json.load(open("results/q1/konsey_ayrisim_b5.json", encoding="utf-8"))

h = b4["b4"]["F_B4"]["karsitliklar"]
r = h["H3"]["hucre_ort"]
scr = r["V-scr"] - r["R224-scr"]
inn = r["V-IN"] - r["R224-IN"]
print("rho satir farki scr (V-scr - R224-scr):", scr)
print("rho satir farki IN (V-IN - R224-IN):", inn)
print("rho etkilesim (IN satiri - scr satiri):", inn - scr)
s = h["H2"]["hucre_ort"]
print("sigma basl. etkisi V (V-IN - V-scr):", s["V-IN"] - s["V-scr"])
print("sigma basl. etkisi R (R224-IN - R224-scr):", s["R224-IN"] - s["R224-scr"])
print("sigma A_IN (V-IN - R224-IN):", s["V-IN"] - s["R224-IN"])
for k in ("H1", "H2", "H3"):
    c = h[k]["ci90"]
    print(k, "ci90 yari genislik:", (c[1] - c[0]) / 2)
sv = b4["b4"]["F_B4"]["degerler"]["sigma"]["V-IN"]
print("V-IN sigma tohum farki:", abs(sv[0] - sv[1]))
om = b4["b4"]["F_B4"]["degerler"]["omega"]
for c, v in om.items():
    print("w = exp(omega)", c, [round(math.exp(x), 3) for x in v])
# B2 tur ici
ki = b2["b2"]["F_B2"]["K-c"]["log_tau_tur_ici"]
print("ViT tur ici log tau ort:", sum(ki.values()) / len(ki))
ri = b2["b2"]["tur_ici_resnet_log_tau"]
print("ResNet tur ici log tau ort:", sum(ri.values()) / len(ri))
sg = b2["b2"]["F_B2"]["K-c"]["sigma_V"]
print("ViT sigma ort:", sum(sg.values()) / len(sg))
# B5
k = b5["b5"]["birincil_C1-R32_V-scr"]["kaynaklar"]
for m, v in k.items():
    st = v["S_tam"]
    if "tgr" in st:
        print(m, "tgr - pgd:", st["tgr"] - st["pgd"], "mi - pgd:", st["mi"] - st["pgd"])
    else:
        print(m, "mi - pgd:", st["mi"] - st["pgd"])
k2 = b5["b5"]["betimsel"]["R224-IN_V-IN"]["kaynaklar"]
for m in ("V_IN_s2101", "V_IN_s2102"):
    st = k2[m]["S_tam"]
    print(m, "tgr - pgd:", st["tgr"] - st["pgd"], "mi - pgd:", st["mi"] - st["pgd"])
# AT epok sureleri (defter sure_s / epok)
for ad, sure, ep in [("V_IN_s2101", 5628, 38), ("R224_IN_s1301", 7050, 36), ("R224_scr_s1201", 13126, 42), ("V_IN_s2102", 12530, 47), ("R224_IN_s1302", 6766, 37), ("R224_scr_s1202", 8685, 58)]:
    print("AT s/epok", ad, round(sure / ep, 1))
