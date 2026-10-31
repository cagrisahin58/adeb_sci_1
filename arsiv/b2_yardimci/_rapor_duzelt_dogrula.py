# Salt okur: 09_sonuc_b2_b6.md dogrulayici bulgularinin kaynaktan denetimi (31.10.2026)
import json, csv, sys
sys.stdout.reconfigure(encoding="utf-8")

def yukle(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

J4 = yukle("results/q1/konsey_ayrisim_b4.json")
J5 = yukle("results/q1/konsey_ayrisim_b5.json")

print("== Bulgu 1: AT epok suresi / pilot ==")
pilot = {"V_IN": 125.8, "R224_IN": 142.7, "R224_scr": 142.5}
with open("results/q1/konsey_b3_defter.tsv", encoding="utf-8") as f:
    satirlar = list(csv.reader(f, delimiter="\t"))
for i, r in enumerate(satirlar, start=1):
    if i == 1:
        continue
    if r[3] in ("AT", "temiz"):
        ad = r[2]
        s = float(r[4]); e = float(r[5])
        t = s / e
        if r[3] == "AT":
            anah = "_".join(ad.split("_")[:-1])
            print(f"DF {i} {ad} {r[3]} sure={s:.0f} epok={e:.0f} s/epok={t:.2f} pilot={pilot[anah]} kat={t/pilot[anah]:.3f} bas={r[0]} bit={r[1]} mib={r[8]} kul={r[9]}")
        else:
            print(f"DF {i} {ad} {r[3]} bas={r[0]} bit={r[1]} mib={r[8]} kul={r[9]}")

print("== Bulgu 2: H3 logit ve oran ==")
d = J4["b4"]["duyarlilik"]
for olcek in ("yari_logit", "yari_oran"):
    print(olcek, json.dumps(d[olcek]["H3"], ensure_ascii=False))
print("birincil H3", json.dumps(J4["b4"]["F_B4"]["karsitliklar"]["H3"], ensure_ascii=False)[:800])

print("== Bulgu 3: B5 IN cifti ==")
b = J5["b5"]["betimsel"]["R224-IN_V-IN"]
print({k: b[k] for k in b if k in ("G_PGD", "G_best", "oran")})

print("== Bulgu 6: S1 sigma ==")
print(json.dumps(J4["b4"]["ikincil"]["S1"]["sigma"], ensure_ascii=False)[:1500])
