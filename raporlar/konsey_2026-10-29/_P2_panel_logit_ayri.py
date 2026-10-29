"""P2 masa kontrolu (3): logit olceginde panel kaynak ve hedef karsitliklari ayri ayri.
Panel = 4 dis gurbuz CNN. kaynak_k = logit r(R->k) - logit r(V->k); hedef_k = logit r(k->V) - logit r(k->R).
Ayrica her modelin panel kaynak gucu S_logit(m) ve hedef duyarliligi T_logit(m) (panel uyeleri icin kendisi haric).
Girdi: results/q1/havuz_cifar10/havuz_protokoller.json."""
import io
import json
import math
import sys

d = json.load(io.open("results/q1/havuz_cifar10/havuz_protokoller.json", encoding="utf-8"))
yon = d["yonlu"]
P = ["Wong2020_PRN18", "Engstrom2019_RN50", "Carmon2019_WRN28_10", "Gowal2020_WRN28_10"]


def L(s, t, prot):
    x = yon[f"{s}->{t}"]["oranlar"][prot] / 100.0
    return math.log(x / (1 - x))


def ms(v):
    m = sum(v) / len(v)
    return m, math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))


out = {}
for prot in ["target_correct", "both_correct"]:
    ks = [L("ResNet18_AT", k, prot) - L("ViT_Tiny_AT", k, prot) for k in P]
    hs = [L(k, "ViT_Tiny_AT", prot) - L(k, "ResNet18_AT", prot) for k in P]
    S = {}
    T = {}
    for m in d["modeller"]:
        pk = [k for k in P if k != m]
        S[m] = round(sum(L(m, k, prot) for k in pk) / len(pk), 3)
        T[m] = round(sum(L(k, m, prot) for k in pk) / len(pk), 3)
    out[prot] = {"kaynak_R_eksi_V": [round(x, 4) for x in ms(ks)], "kaynak_uyeler": [round(x, 4) for x in ks],
                 "hedef_V_eksi_R": [round(x, 4) for x in ms(hs)], "hedef_uyeler": [round(x, 4) for x in hs],
                 "S_logit": S, "T_logit": T}
io.open("raporlar/konsey_2026-10-29/_P2_panel_logit_ayri.json", "w", encoding="utf-8", newline="\n").write(
    json.dumps(out, indent=1, ensure_ascii=False))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
print(json.dumps(out, indent=1, ensure_ascii=False))
