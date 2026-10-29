"""P2 masa kontrolu (2): sabit dis CNN paneline dayali dis-orneklem ongorusu, oran ve logit olceginde.

Cift hucreleri (ResNet18_AT <-> ViT_Tiny_AT) uydurmaya girmez. Panelin her uyesi k icin
ongoru_k = [g(R->k) - g(V->k)] + [g(k->V) - g(k->R)], g = oran ya da logit(oran/100).
Simetrik ya da yonlu aile terimi (CNN paneli icin) bu toplamda sadelesir; geriye kalan fark
yalniz bu cifte ozgu yonlu etkilesimdir. Ayrica her dis CNN cifti (a, b) icin ayni ongoru
(panel = kalan dis CNN'ler) hesaplanir: cifte ozgu terimin CNN-CNN ciftlerindeki dagilimi.
Girdi: results/q1/havuz_cifar10/havuz_protokoller.json. Calistirma: depo kokunden python.
"""
import io
import itertools
import json
import math
import sys

KAYNAK = "results/q1/havuz_cifar10/havuz_protokoller.json"
CIKTI = "raporlar/konsey_2026-10-29/_P2_panel_logit.json"
DIS = ["Wong2020_PRN18", "Engstrom2019_RN50", "Carmon2019_WRN28_10", "Gowal2020_WRN28_10",
       "Debenedetti2022_XCiT_S12"]
d = json.load(io.open(KAYNAK, encoding="utf-8"))
yon = d["yonlu"]


def g(s, t, prot, olcek):
    x = yon[f"{s}->{t}"]["oranlar"][prot] / 100.0
    if olcek == "oran":
        return 100.0 * x
    x = min(max(x, 1e-4), 1 - 1e-4)
    return math.log(x / (1 - x))


def tahmin(a, b, panel, prot, olcek):
    vals = []
    for k in panel:
        vals.append((g(a, k, prot, olcek) - g(b, k, prot, olcek)) + (g(k, b, prot, olcek) - g(k, a, prot, olcek)))
    return sum(vals) / len(vals), vals


out = {"kaynak": KAYNAK, "tanim": __doc__.strip(), "sonuc": {}}
for prot in ["target_correct", "both_correct", "raw"]:
    for olcek in ["oran", "logit"]:
        key = f"{prot}/{olcek}"
        res = {}
        # 1) Hedef cift, panel = 4 dis CNN (XCiT haric) ve 5 dis model (XCiT dahil)
        for pad, panel in [("4_dis_CNN", DIS[:4]), ("5_dis_model", DIS)]:
            on, vals = tahmin("ResNet18_AT", "ViT_Tiny_AT", panel, prot, olcek)
            goz = g("ResNet18_AT", "ViT_Tiny_AT", prot, olcek) - g("ViT_Tiny_AT", "ResNet18_AT", prot, olcek)
            res[f"R_V_panel_{pad}"] = {"ongoru": round(on, 4), "gozlenen": round(goz, 4),
                                       "artik": round(goz - on, 4), "uye_ongoruleri": [round(v, 4) for v in vals]}
        # 2) Dis CNN ciftleri: her cift icin panel = kalan dis CNN'ler + ResNet18_AT (ViT haric)
        cnn = DIS[:4] + ["ResNet18_AT"]
        artiklar = []
        for a, b in itertools.combinations(cnn, 2):
            panel = [k for k in cnn if k not in (a, b)]
            on, _ = tahmin(a, b, panel, prot, olcek)
            goz = g(a, b, prot, olcek) - g(b, a, prot, olcek)
            artiklar.append({"cift": f"{a}/{b}", "ongoru": round(on, 4), "gozlenen": round(goz, 4),
                             "artik": round(goz - on, 4)})
        res["CNN_CNN_ciftleri"] = artiklar
        abs_art = [abs(x["artik"]) for x in artiklar]
        res["CNN_CNN_mutlak_artik_ozet"] = {"n": len(abs_art), "en_buyuk": round(max(abs_art), 4),
                                           "ortalama": round(sum(abs_art) / len(abs_art), 4)}
        out["sonuc"][key] = res

io.open(CIKTI, "w", encoding="utf-8", newline="\n").write(json.dumps(out, indent=1, ensure_ascii=False))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
for key, res in out["sonuc"].items():
    print("==", key)
    for pad in ["R_V_panel_4_dis_CNN", "R_V_panel_5_dis_model"]:
        print("  ", pad, res[pad])
    print("   CNN-CNN |artik| ozet:", res["CNN_CNN_mutlak_artik_ozet"])
