"""Yayilim-temiz fark sekli icin veri (LeCun plani, 2026-10-04).

Her yonsuz model cifti icin: |temiz dogruluk farki| (puan), dort ve uc protokol yayilimi (puan), protokol
basina asimetri, grup etiketi. Kaynaklar (hepsi results/c1_* ve results/q1/*):
  - CIFAR-10 AT ciftleri (3): results/c1_transfer/c1_transfer_summary.json (+ temiz: c1_seeds)
  - CIFAR-100 AT ciftleri (3): results/q1/cifar100/transfer/e1_transfer_summary.json (+ e1_cifar100_summary)
  - SVHN AT ciftleri (2): results/q1/svhn/transfer/e7_transfer_summary.json (+ e7_svhn_summary)
  - CIFAR-10 L2 (3): results/q1/cifar10_l2/transfer/e6_l2_transfer_summary.json (temiz = CIFAR-10 AT)
  - 3x3 matris WRN ciftleri (CIFAR-10, 3 cift): results/c1_c3/pair*/havuz_protokoller.json
  - temiz egitilmis ciftler + Standard WRN: results/q1/temiz_ciftler/pair*/havuz_protokoller.json
  - son kontrol noktasi ciftleri: results/q1/son_kontrol_noktasi/pair*/havuz_protokoller.json
  - genisletilmis havuz: results/q1/havuz_cifar10/havuz_protokoller.json
(havuz_protokoller.json dosyalari experiments/q1_havuz_analiz.py ile uretilir.)
Cikti: results/q1/fig_yayilim_temiz_fark_veri.json
Konteynerde: docker exec -w /workspace adeb_eval python scripts/fig_yayilim_temiz_fark_veri.py
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PROT = ("raw", "target_correct", "both_correct", "successful_source")
KAYNAK = {}


def jl(rel):
    p = ROOT / rel
    KAYNAK[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return json.loads(p.read_text(encoding="utf-8"))


def yay(asim):
    v4 = [asim[p] for p in PROT]
    v3 = [asim[p] for p in PROT[:3]]
    return max(v4) - min(v4), max(v3) - min(v3)


noktalar = []


def ozetten(rel_t, grup, temiz_a, temiz_b, etiket_a, etiket_b, n_cift):
    """e*_transfer_summary semasi: protocols[p]['diff']['values'] (A->B eksi B->A, A=CNN)."""
    t = jl(rel_t)
    for i in range(n_cift):
        asim = {p: float(t["protocols"][p]["diff"]["values"][i]) for p in PROT}
        y4, y3 = yay(asim)
        tc_ab = float(t["protocols"]["target_correct"]["CNN_to_ViT"]["values"][i])
        tc_ba = float(t["protocols"]["target_correct"]["ViT_to_CNN"]["values"][i])
        e_a, e_b = 100.0 - temiz_a[i], 100.0 - temiz_b[i]  # a = CNN (kaynak A->B'de hedef B)
        noktalar.append({
            "grup": grup, "cift": i + 1, "modeller": [etiket_a, etiket_b],
            "temiz_a": temiz_a[i], "temiz_b": temiz_b[i], "temiz_fark_mutlak": abs(temiz_a[i] - temiz_b[i]),
            "asimetri": asim, "yayilim_dort": y4, "yayilim_uc": y3,
            **ozdeslik_alanlari(asim, e_a, e_b, tc_ab, tc_ba),
            "hedef_egitimi": "AT/AT", "kaynak": rel_t,
        })


def ozdeslik_alanlari(asim, e_a, e_b, tc_ab, tc_ba):
    """Ozdeslik (p=1) ongorusu: (raw-tc) asimetri farki = e_B(1-tc_AB/100) - e_A(1-tc_BA/100).
    Uc-protokol yayilimi, bc arada kaldiginda bu farkin mutlak degerine esittir."""
    ongoru = e_b * (1 - tc_ab / 100.0) - e_a * (1 - tc_ba / 100.0)
    return {
        "raw_eksi_tc_asimetri_olculen": asim["raw"] - asim["target_correct"],
        "raw_eksi_tc_asimetri_ozdeslik_ongorusu_p1": ongoru,
        "ozdeslik_ongorusu_mutlak": abs(ongoru),
        "bas_kaynak_eksi_bc_asimetri": asim["successful_source"] - asim["both_correct"],
    }


# CIFAR-10 AT (3 cift)
seeds = jl("results/c1_seeds/c1_seed_summary.json")["pairs"]
c10_rn = [p["resnet"]["clean"] for p in seeds]
c10_vt = [p["vit"]["clean"] for p in seeds]
ozetten("results/c1_transfer/c1_transfer_summary.json", "CIFAR-10 Linf, AT cifti", c10_rn, c10_vt, "ResNet-18 AT", "ViT-Tiny AT", 3)
# CIFAR-100 (3)
e1 = jl("results/q1/e1_cifar100_summary.json")["mimariler"]
ozetten("results/q1/cifar100/transfer/e1_transfer_summary.json", "CIFAR-100 Linf, AT cifti",
        e1["resnet18"]["ozet"]["test_clean"]["degerler"], e1["vit_tiny"]["ozet"]["test_clean"]["degerler"],
        "ResNet-18 AT", "ViT-Tiny AT", 3)
# SVHN (2)
e7 = jl("results/q1/e7_svhn_summary.json")["mimariler"]
ozetten("results/q1/svhn/transfer/e7_transfer_summary.json", "SVHN Linf, AT cifti",
        e7["resnet18"]["ozet"]["test_clean"]["degerler"], e7["vit_tiny"]["ozet"]["test_clean"]["degerler"],
        "ResNet-18 AT", "ViT-Tiny AT", 2)
# CIFAR-10 L2 (3; ayni kontrol noktalari)
ozetten("results/q1/cifar10_l2/transfer/e6_l2_transfer_summary.json", "CIFAR-10 L2, AT cifti", c10_rn, c10_vt,
        "ResNet-18 AT", "ViT-Tiny AT", 3)


def havuzdan(rel_dir, grup, hedef_egitimi, cift_no=None, atla_ciftler=()):
    f = ROOT / rel_dir / "havuz_protokoller.json"
    if not f.exists():
        print("YOK (atlandi):", f)
        return
    h = jl(str(Path(rel_dir) / "havuz_protokoller.json"))
    for c in h["ciftler"]:
        a, b = c["cift"]
        if tuple(sorted((a, b))) in {tuple(sorted(x)) for x in atla_ciftler}:
            continue
        yab, yba = h["yonlu"][f"{a}->{b}"], h["yonlu"][f"{b}->{a}"]
        noktalar.append({
            "grup": grup, "cift": cift_no, "modeller": [a, b],
            "temiz_a": h["temiz_dogruluk"][a], "temiz_b": h["temiz_dogruluk"][b],
            "temiz_fark_mutlak": c["temiz_dogruluk_farki_mutlak"],
            "asimetri": c["asimetri_ileri_eksi_geri"], "yayilim_dort": c["yayilim_dort_protokol"],
            "yayilim_uc": c["yayilim_uc_protokol_bas_kaynak_haric"],
            **ozdeslik_alanlari(c["asimetri_ileri_eksi_geri"], 100.0 - h["temiz_dogruluk"][a],
                                100.0 - h["temiz_dogruluk"][b], yab["oranlar"]["target_correct"],
                                yba["oranlar"]["target_correct"]),
            "p_ab": yab["p_adv_yanlis_verili_temiz_yanlis"], "p_ba": yba["p_adv_yanlis_verili_temiz_yanlis"],
            "hedef_egitimi": hedef_egitimi, "kaynak": str(Path(rel_dir) / "havuz_protokoller.json"),
        })


# 3x3 matrisin WRN ciftleri (ResNet-ViT cifti c1_transfer'den zaten var -> atla)
for i in (1, 2, 3):
    havuzdan(f"results/c1_c3/pair{i}", "CIFAR-10 Linf, WRN-28-10 referansiyla", "AT/AT", i,
             atla_ciftler=[("ResNet18_AT", "ViT_Tiny_AT")])
for i in (1, 2, 3):
    havuzdan(f"results/q1/temiz_ciftler/pair{i}", "CIFAR-10 Linf, standart egitimli modeller", "standart/standart", i)
for i in (1, 2, 3):
    havuzdan(f"results/q1/son_kontrol_noktasi/pair{i}", "CIFAR-10 Linf, son kontrol noktasi", "AT/AT", i)
# Havuzdaki ResNet18_AT, ViT_Tiny_AT ve Gowal2020_WRN28_10, C1 cift 1 ve WRN referansiyla AYNI kontrol
# noktalari; bu uc cift yukarida zaten sayildi -> havuzda atlanir (cift sayimi yok).
havuzdan("results/q1/havuz_cifar10", "CIFAR-10 Linf, RobustBench havuzu", "karisik", None,
         atla_ciftler=[("ResNet18_AT", "ViT_Tiny_AT"), ("ResNet18_AT", "Gowal2020_WRN28_10"),
                       ("ViT_Tiny_AT", "Gowal2020_WRN28_10")])

x = np.array([n["temiz_fark_mutlak"] for n in noktalar])
y4 = np.array([n["yayilim_dort"] for n in noktalar])
y3 = np.array([n["yayilim_uc"] for n in noktalar])


def ols(x, y):
    A = np.vstack([x, np.ones_like(x)]).T
    (m, b), *_ = np.linalg.lstsq(A, y, rcond=None)
    r = float(np.corrcoef(x, y)[0, 1])
    return float(m), float(b), r


def spearman(x, y):
    rx, ry = np.argsort(np.argsort(x)), np.argsort(np.argsort(y))
    return float(np.corrcoef(rx, ry)[0, 1])


ozet = {}
for ad, yy in (("dort_protokol", y4), ("uc_protokol_bas_kaynak_haric", y3)):
    m, b, r = ols(x, yy)
    gruplar = sorted({n["grup"] for n in noktalar})
    birak = {}
    for g in gruplar:
        mk = np.array([n["grup"] != g for n in noktalar])
        if mk.sum() >= 3 and np.ptp(x[mk]) > 0:
            birak[g] = round(ols(x[mk], yy[mk])[0], 3)
    ozet[ad] = {"egim": m, "kesisim": b, "pearson_r": r, "spearman_rho": spearman(x, yy), "n_cift": int(len(x)),
                "grup_birak_egimleri": birak,
                "NOT": "ciftler modelleri ve kosulari paylasir; n_cift serbestlik derecesi DEGILDIR, "
                       "grup-birak egimleri duyarlilik icindir"}

# ozdeslik ongorusu ile olculen (raw - tc) asimetri farki: parite
olc = np.array([n["raw_eksi_tc_asimetri_olculen"] for n in noktalar])
ong = np.array([n["raw_eksi_tc_asimetri_ozdeslik_ongorusu_p1"] for n in noktalar])
ozet["ozdeslik_paritesi"] = {
    "n": int(len(olc)), "mutlak_sapma_max": float(np.abs(olc - ong).max()),
    "mutlak_sapma_ort": float(np.abs(olc - ong).mean()), "pearson_r": float(np.corrcoef(olc, ong)[0, 1]),
    "NOT": "p=1 yaklasikligi; sapma = e_B(1-p_AB) - e_A(1-p_BA) terimidir",
}
uc_vs_ozdeslik = np.array([abs(n["raw_eksi_tc_asimetri_olculen"]) for n in noktalar])
ozet["uc_protokol_yayilimi_vs_raw_tc_farki"] = {
    "esit_cift_sayisi_1e-9": int((np.abs(y3 - uc_vs_ozdeslik) < 1e-9).sum()), "n": int(len(y3)),
    "NOT": "uc-protokol yayilimi, bc arada kaldiginda |raw-tc| asimetri farkina esittir (hukum M1)",
}
cikti = {
    "uretildi_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "aciklama": "Her nokta bir yonsuz model cifti: |temiz dogruluk farki| ve protokol yayilimi (puan). "
                "Asimetri = ilk model eksi ikinci model yonu farki.",
    "kaynaklar": KAYNAK, "n_nokta": len(noktalar), "gruplar": sorted({n["grup"] for n in noktalar}),
    "egim": ozet, "noktalar": noktalar,
}
out = ROOT / "results/q1/fig_yayilim_temiz_fark_veri.json"
out.write_text(json.dumps(cikti, indent=1, ensure_ascii=False), encoding="utf-8")
print("yazildi:", out, "| nokta:", len(noktalar))
for g in sorted({n["grup"] for n in noktalar}):
    pts = [n for n in noktalar if n["grup"] == g]
    print(f"  {g:48s} n={len(pts):2d}  temiz_fark {min(p['temiz_fark_mutlak'] for p in pts):5.2f}-{max(p['temiz_fark_mutlak'] for p in pts):5.2f}"
          f"  yayilim4 {min(p['yayilim_dort'] for p in pts):5.2f}-{max(p['yayilim_dort'] for p in pts):5.2f}")
print("egim:", {k: (round(v["egim"], 3), round(v["pearson_r"], 3), round(v["spearman_rho"], 3))
                for k, v in ozet.items() if "egim" in v})
print("ozdeslik paritesi:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in ozet["ozdeslik_paritesi"].items() if k != "NOT"})
