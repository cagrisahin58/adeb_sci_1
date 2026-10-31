"""Salt okur: 11_sonuc_b8_b10.md dogrulayici bulgularinin kanitini yeniden okur (31.10.2026)."""
import json

R = "results/q1/"
# Bulgu 7: ImageNetV2 donusturucu-donusturucu c ortalamasi (mantel_imagenetv2.json c_matrisi, aile HT8)
m = json.load(open(R + "konsey_b10_gradyan/mantel_imagenetv2.json"))
mod = m["modeller_ortak"]
C = m["c_matrisi"]
ht = json.load(open("raporlar/konsey_2026-10-29/hucre_tablosu_b8.json"))["modeller"]
don = [ht[x]["aile"] != "CNN" for x in mod]
gr = {"CNN-CNN": [], "DON-DON": [], "karma": []}
for i in range(len(mod)):
    for j in range(i + 1, len(mod)):
        k = "DON-DON" if don[i] and don[j] else ("CNN-CNN" if not don[i] and not don[j] else "karma")
        gr[k].append(C[i][j])
for k, v in gr.items():
    print(f"IN {k}: n={len(v)} ort={sum(v)/len(v):.6f}")
print("IN c[0][1]", mod[0], mod[1], C[0][1])
ko = json.load(open(R + "konsey_b10_gradyan/imagenetv2/kosinus_ozet.json"))
print("KOIN c_tum[0][1]", ko["c_tum"][0][1], ko.get("modeller", [None, None])[:2] if isinstance(ko.get("modeller"), list) else "")

# Bulgu 8: OD normalizasyon taramasi
od = json.load(open(R + "konsey_b8_imagenetv2/denetim/onisleme_denetimi.json"))
for k, v in od.get("normalizasyon", {}).items():
    print("OD norm", k, v.get("model_ici_normalizasyon_var") if isinstance(v, dict) else v)

# Bulgu 2: J4 V-IN rho ortalamasi, J2 logit rho
j4 = json.load(open(R + "konsey_ayrisim_b4.json"))
print("J4 H3 hucre_ort", j4["b4"]["F_B4"]["karsitliklar"]["H3"].get("hucre_ort"))
j2 = json.load(open(R + "konsey_ayrisim_b2.json"))
print("J2 yari_logit rho_V ort", j2["b2"]["duyarlilik"]["yari_logit"]["rho_V"]["ort"])

# Bulgu 5: J9 logit ve oran
j9 = json.load(open(R + "konsey_b9_c100/b9_dondurulmus_b2.json"))
d = j9["b2"]["duyarlilik"]
print("J9 yari_logit rho_V", d["yari_logit"]["rho_V"].get("ort"), d["yari_logit"]["rho_V"].get("ci95"))
print("J9 yari_oran rho_V", d["yari_oran"]["rho_V"].get("ort"), d["yari_oran"]["rho_V"].get("ci95"))
print("J9 meta uretildi", j9["meta"]["uretildi_utc"])
j8 = json.load(open(R + "konsey_b8_imagenetv2/b8_dondurulmus_b2.json"))
print("J8 meta uretildi", j8["meta"]["uretildi_utc"])

# Bulgu 4: Liu satiri
b8 = json.load(open(R + "konsey_b8_imagenetv2/b8_betimsel.json"))
L = b8["A_sigma_scr_Liu"]
print("Liu", L.get("kestirim"), L.get("goruntu_bootstrap", {}).get("ci90"), L.get("beklenti_esigi"), L.get("betimsel_etiket"))
