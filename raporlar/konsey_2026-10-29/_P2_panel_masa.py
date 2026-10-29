"""P2 masa kontrolu: sabit panel karsisinda kaynak gucu S(m) ve hedef duyarliligi T(m).

Girdi yalniz results/q1/havuz_cifar10/havuz_protokoller.json (karantina disi, C1 sonrasi).
S(m, P) = mean_{k in P, k != m} r(m -> k); T(m, P) = mean_{k in P, k != m} r(k -> m).
Panel P = dis gurbuz CNN'ler (Wong2020_PRN18, Engstrom2019_RN50, Carmon2019_WRN28_10, Gowal2020_WRN28_10).
Iki model arasindaki kaynak karsitligi d_k = r(a->k) - r(b->k), k in P; ortalama, SD (ddof=1), t (df = |P|-1).
Model gerektirmez; toplamsal uydurma ya da etkilesimsizlik varsayimi yoktur.
Calistirma: python raporlar/konsey_2026-10-29/_P2_panel_masa.py  (depo kokunden; numpy gerekmez)
"""
import io
import json
import math
import sys

KAYNAK = "results/q1/havuz_cifar10/havuz_protokoller.json"
CIKTI = "raporlar/konsey_2026-10-29/_P2_panel_masa.json"
PANEL = ["Wong2020_PRN18", "Engstrom2019_RN50", "Carmon2019_WRN28_10", "Gowal2020_WRN28_10"]
PROTOKOLLER = ["raw", "target_correct", "both_correct"]

d = json.load(io.open(KAYNAK, encoding="utf-8"))
modeller = d["modeller"]
yon = d["yonlu"]


def r(s, t, prot):
    return yon[f"{s}->{t}"]["oranlar"][prot]


def ort_sd(xs):
    n = len(xs)
    m = sum(xs) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1)) if n > 1 else float("nan")
    return m, sd


out = {"kaynak": KAYNAK, "panel": PANEL, "tanim": __doc__.strip(), "S": {}, "T": {}, "karsitlik": {}}
for prot in PROTOKOLLER:
    out["S"][prot] = {}
    out["T"][prot] = {}
    for m in modeller:
        hedefler = [k for k in PANEL if k != m]
        s_vals = [r(m, k, prot) for k in hedefler]
        t_vals = [r(k, m, prot) for k in hedefler]
        out["S"][prot][m] = {"ort": round(sum(s_vals) / len(s_vals), 3), "n_panel": len(hedefler),
                             "degerler": [round(v, 3) for v in s_vals]}
        out["T"][prot][m] = {"ort": round(sum(t_vals) / len(t_vals), 3), "n_panel": len(hedefler),
                             "degerler": [round(v, 3) for v in t_vals]}
    # ResNet18_AT ile ViT_Tiny_AT arasinda panel karsitliklari (panel her ikisinin de disinda)
    a, b = "ResNet18_AT", "ViT_Tiny_AT"
    dk_s = [r(a, k, prot) - r(b, k, prot) for k in PANEL]
    dk_t = [r(k, b, prot) - r(k, a, prot) for k in PANEL]
    ms, ss = ort_sd(dk_s)
    mt, st = ort_sd(dk_t)
    cift = r(a, b, prot) - r(b, a, prot)
    out["karsitlik"][prot] = {
        "kaynak_karsitligi_R_eksi_V": {"ort": round(ms, 3), "sd_panel": round(ss, 3),
                                       "t_df3": round(ms / (ss / math.sqrt(len(PANEL))), 2),
                                       "degerler": [round(v, 3) for v in dk_s]},
        "hedef_karsitligi_V_eksi_R": {"ort": round(mt, 3), "sd_panel": round(st, 3),
                                      "t_df3": round(mt / (st / math.sqrt(len(PANEL))), 2),
                                      "degerler": [round(v, 3) for v in dk_t]},
        "panel_ongorusu_asimetri": round(ms + mt, 3),
        "gozlenen_cift_asimetrisi_R_to_V_eksi_V_to_R": round(cift, 3),
        "fark_gozlenen_eksi_ongoru": round(cift - ms - mt, 3),
        "ViT_kaynak_XCiT_hedef": round(r(b, "Debenedetti2022_XCiT_S12", prot), 3),
        "ResNet_kaynak_XCiT_hedef": round(r(a, "Debenedetti2022_XCiT_S12", prot), 3),
    }

io.open(CIKTI, "w", encoding="utf-8", newline="\n").write(json.dumps(out, indent=1, ensure_ascii=False))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
for prot in PROTOKOLLER:
    print("==", prot)
    for m in modeller:
        print(f"  {m:28s} S={out['S'][prot][m]['ort']:7.2f}  T={out['T'][prot][m]['ort']:7.2f}  (n_panel={out['S'][prot][m]['n_panel']})")
    print("  karsitlik:", json.dumps(out["karsitlik"][prot], ensure_ascii=False))
