"""06_ek_deney_tasarim.md: B8, B9, B10 sure ve indirme kestirimi. Girdi _ek_flop_olcumu.json.
Is modeli: kaynak basina 10 adim PGD (ileri+geri yaklasik 3 ileri gecis) = 30 F_kaynak; her kaynagin ornekleri
K hedefte bir kez ileri gecer = K * toplam F; temiz gecis = toplam F. Toplam FLOP = n * SUM_F * (30 + K + 1).
Etkin hiz iki kalibrasyondan: (a) 8x8 havuz matrisi 13,5 dk (00_durum_dosyasi.md satir 94, zaman damgalarindan
turetilmis), (b) 224 girdili ResNet-18 kaynak basina 1,15 dk (01_oneri_P3_kuram_olcum.md satir 57, n = 10000)."""
import io, json
from pathlib import Path
K = Path(__file__).resolve().parent
F = {k: v["gflop"] for k, v in json.load(open(K / "_ek_flop_olcumu.json"))["modeller"].items() if "gflop" in v}
P = {k: v["fp32_MB"] for k, v in json.load(open(K / "_ek_flop_olcumu.json"))["modeller"].items() if "fp32_MB" in v}

havuz = ["c1_resnet18", "c1_vit_tiny", "rb_prn18", "rb_resnet50_cifar", "rb_wrn28_10", "rb_wrn28_10", "rb_wrn28_10", "rb_xcit_s12_cifar10"]
S_h = sum(F[m] for m in havuz)
hiz_a = 1e4 * S_h * 1e9 * (30 + 8 + 1) / (13.5 * 60)
hiz_b = 1e4 * F["c1_resnet18_224"] * 1e9 * 30 / (1.15 * 60)

def blok(modeller, n):
    S = sum(F[m] for m in modeller); Kk = len(modeller)
    W = n * S * 1e9 * (30 + Kk + 1)
    return {"model_sayisi": Kk, "toplam_gflop": round(S, 3), "n": n, "toplam_flop": W,
            "dk_hiz_a": round(W / hiz_a / 60, 1), "dk_hiz_b": round(W / hiz_b / 60, 1)}

b8 = ["tv_resnet18", "tv_resnet50", "tv_resnet50", "tv_wide_resnet50_2", "tv_wide_resnet50_2", "ra_wrn101_2",
      "convnext_t_cvst", "convnext_b_cvst", "timm_convnext_base",
      "vit_s_cvst", "vit_b_cvst", "timm_swin_base_patch4_window7_224", "timm_vit_base_patch16_224",
      "timm_xcit_small_12_p16_224"]
b9 = ["c1_resnet18"] * 3 + ["c1_vit_tiny"] * 3 + ["rb_prn18"] * 3 + ["rb_wrn34_10_c100", "rb_dmwrn28_10_c100",
      "rb_dmwrn28_10_c100", "rb_wrn34_10_c100", "rb_xcit_s12_cifar10", "rb_wrn28_10"]
b4_c10 = ["c1_resnet18"] * 3 + ["c1_vit_tiny"] * 3 + ["rb_prn18", "rb_resnet50_cifar", "rb_wrn28_10", "rb_wrn28_10",
          "rb_prn18", "rb_prn18", "rb_prn18", "rb_xcit_s12_cifar10"] + ["c1_vit_tiny"] * 2 + ["c1_resnet18_224"] * 4
out = {"kalibrasyon": {"havuz_toplam_gflop": round(S_h, 3), "etkin_hiz_a_TFLOPs": round(hiz_a / 1e12, 1),
                       "etkin_hiz_b_TFLOPs": round(hiz_b / 1e12, 1)},
       "oran_224_resnet18_e_gore": {m: round(F[m] / F["c1_resnet18_224"], 2) for m in
                                    ["tv_resnet50", "vit_s_cvst", "tv_wide_resnet50_2", "timm_swin_base_patch4_window7_224",
                                     "timm_vit_base_patch16_224", "ra_wrn101_2"]},
       "B8_n1000": blok(b8, 1000), "B8_n500": blok(b8, 500),
       "B9_n10000": blok(b9, 10000),
       "B10_gradyan_dk_hiz_b": {k: round(n * sum(F[m] for m in L) * 1e9 * 3 / hiz_b / 60, 2) for k, L, n in
                                [("imagenet_n1000", b8, 1000), ("cifar100_n10000", b9, 10000), ("cifar10_b4_n10000", b4_c10, 10000)]},
       "B8_indirme_fp32_MB": round(sum(P[m] for m in b8), 1),
       "B9_indirme_fp32_MB_pang_haric": round(sum(P[m] for m in ["rb_prn18"] * 3 + ["rb_wrn34_10_c100", "rb_dmwrn28_10_c100",
                                              "rb_wrn34_10_c100", "rb_xcit_s12_cifar10", "rb_wrn28_10"]), 1),
       "veri_bayt": {"imagenette2-320": 341663724, "imagewoof2-320": 328387740}}
out["toplam_indirme_MB"] = round(out["B8_indirme_fp32_MB"] + out["B9_indirme_fp32_MB_pang_haric"] +
                                 sum(out["veri_bayt"].values()) / 1e6, 1)
with io.open(K / "_ek_sure_kestirimi.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(json.dumps(out, indent=1))
