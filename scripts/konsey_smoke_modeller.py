"""Konsey B1 smoke: sarmalayicilar, agirlik yukleme raporu, normalizasyon ve
girdi hatti esligi (< 1 dk, CPU yeter). Cikti: results/q1/konsey_smoke/modeller.json

    docker exec -w /workspace adeb_eval python scripts/konsey_smoke_modeller.py
"""
import json
import sys
from pathlib import Path

import torch
import torch.nn as nn

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.models import ModelRegistry  # noqa: E402
from src.models.r224 import ResizeNormalize, imagenet_norm_from_cfg, load_imagenet_init  # noqa: E402
from src.utils.load_model_auto import load_model_auto  # noqa: E402

OUT = Path("results/q1/konsey_smoke/modeller.json")


def main():
    torch.manual_seed(0)
    rap = {"testler": {}}
    T = rap["testler"]
    x = torch.rand(4, 3, 32, 32)

    vscr = ModelRegistry.get("vit_tiny", num_classes=10).eval()
    r_scr = ModelRegistry.get("resnet18_224", num_classes=10).eval()
    r_in = ModelRegistry.get("resnet18_224_in1k", num_classes=10).eval()
    v_in = ModelRegistry.get("vit_tiny_in1k", num_classes=10).eval()

    # 1) Girdi hatti: R224-scr'nin buyutmesi V-scr ile ayni mi, normalizasyon yok mu
    up_v, up_r = vscr.resize, r_scr.resize
    T["r224_scr_girdi_hatti_vscr_ile_ayni"] = {
        "vscr_resize": repr(up_v), "r224_scr_resize": repr(up_r),
        "ayni_tip_ve_ayar": (type(up_v) is type(up_r) and repr(up_v) == repr(up_r)),
        "cikti_birebir": bool(torch.equal(up_v(x), up_r(x))),
        "r224_scr_tampon_sayisi": len([k for k in r_scr.state_dict() if k.startswith("resize.")]),
        "vscr_tampon_sayisi": len([k for k in vscr.state_dict() if k.startswith("resize.")]),
    }
    T["r224_scr_girdi_hatti_vscr_ile_ayni"]["GECTI"] = (
        T["r224_scr_girdi_hatti_vscr_ile_ayni"]["ayni_tip_ve_ayar"]
        and T["r224_scr_girdi_hatti_vscr_ile_ayni"]["cikti_birebir"]
        and T["r224_scr_girdi_hatti_vscr_ile_ayni"]["r224_scr_tampon_sayisi"] == 0)

    # 2) V-IN mimarisi V-scr ile ayni mi (govde anahtar ve sekilleri)
    sv = {k: tuple(v.shape) for k, v in vscr.model.state_dict().items()}
    si = {k: tuple(v.shape) for k, v in v_in.model.state_dict().items()}
    T["v_in_mimari_vscr_ile_ayni"] = {"GECTI": sv == si, "anahtar_sayisi": len(sv),
                                       "parametre_vscr": vscr.count_parameters(),
                                       "parametre_v_in": v_in.count_parameters()}

    # 3) Agirlik yukleme raporlari
    for mtype, model, key in (("vit_tiny_in1k", v_in, "deit_tiny_in1k"),
                              ("resnet18_224_in1k", r_in, "resnet18_a1_in1k")):
        before = {k: v.clone() for k, v in model.model.state_dict().items()}
        rep = load_imagenet_init(model, key, mtype)
        changed = sum(not torch.equal(before[k], v) for k, v in model.model.state_dict().items())
        rep["degisen_tensor_sayisi"] = changed
        rep["GECTI"] = (not rep["missing_nonhead"] and not rep["unexpected_nonhead"]
                        and not rep["shape_mismatch"] and rep["norm_matches_cfg"])
        T[f"agirlik_yukleme_{key}"] = rep
    # Uyumsuz tip reddediliyor mu (K3 korumasi)
    try:
        load_imagenet_init(r_scr, "resnet18_a1_in1k", "resnet18_224")
        T["uyumsuz_tip_reddi"] = {"GECTI": False}
    except ValueError as e:
        T["uyumsuz_tip_reddi"] = {"GECTI": True, "mesaj": str(e)[:200]}

    # 4) Normalizasyon degerleri ve gercekten uygulandigi
    for mtype, model, cfgname in (("vit_tiny_in1k", v_in, "deit_tiny_patch16_224.fb_in1k"),
                                  ("resnet18_224_in1k", r_in, "resnet18.a1_in1k")):
        mean, std = imagenet_norm_from_cfg(cfgname)
        rz = model.resize
        manual = (nn.functional.interpolate(x, size=(224, 224), mode="bilinear",
                                            align_corners=False)
                  - torch.tensor(mean).view(1, 3, 1, 1)) / torch.tensor(std).view(1, 3, 1, 1)
        with torch.no_grad():
            same_fwd = torch.allclose(model(x), model.model(manual), atol=1e-5)
        T[f"normalizasyon_{mtype}"] = {
            "pretrained_cfg_mean": list(mean), "pretrained_cfg_std": list(std),
            "sarmalayici_mean": [float(v) for v in rz.mean.flatten()],
            "sarmalayici_std": [float(v) for v in rz.std.flatten()],
            "ileri_gecis_elle_normalizasyonla_ayni": bool(same_fwd),
            "checkpointte_tampon": [k for k in model.state_dict() if k.startswith("resize.")],
            "GECTI": isinstance(rz, ResizeNormalize) and bool(same_fwd) and all(
                abs(a - b) < 1e-6 for a, b in zip(
                    [float(v) for v in rz.mean.flatten()] + [float(v) for v in rz.std.flatten()],
                    list(mean) + list(std))),
        }

    # 5) Cikis sekilleri ve parametre sayilari
    with torch.no_grad():
        T["cikis_sekilleri"] = {n: list(m(x).shape) for n, m in
                                (("resnet18_224", r_scr), ("resnet18_224_in1k", r_in),
                                 ("vit_tiny_in1k", v_in))}
    T["cikis_sekilleri"]["GECTI"] = all(v == [4, 10] for v in T["cikis_sekilleri"].values())
    rap["parametre"] = {"resnet18_224": r_scr.count_parameters(),
                        "vit_tiny_in1k": v_in.count_parameters(),
                        "vit_tiny": vscr.count_parameters()}

    # 6) Kayit/yukleme turu: load_model_auto yeni tiplerde ve normalizasyon
    #    tamponu strict yuklemeyi koruyor mu
    tmp = Path("results/q1/konsey_smoke/_tmp_ckpt.pth")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model_state_dict": r_in.state_dict()}, tmp)
    m2 = load_model_auto("resnet18_224_in1k", str(tmp), "cpu")
    with torch.no_grad():
        ok_round = torch.equal(m2(x), r_in(x))
    try:
        load_model_auto("resnet18_224", str(tmp), "cpu")
        strict_ok = False
    except RuntimeError:
        strict_ok = True
    tmp.unlink()
    T["kayit_yukleme_turu"] = {"GECTI": bool(ok_round and strict_ok),
                               "ayni_cikti": bool(ok_round),
                               "normalizasyonlu_ckpt_scr_tipine_yuklenmez": strict_ok}

    # 7) Eski tip hala ayni yukleniyor mu (C1 ViT kontrol noktasi)
    p = "models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth"
    m = load_model_auto("vit_tiny", p, "cpu")
    T["c1_vit_yukleme"] = {"GECTI": isinstance(m.resize, nn.Upsample), "yol": p}

    rap["hepsi_gecti"] = all(v.get("GECTI", False) for v in T.values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rap, indent=2, ensure_ascii=False))
    print(json.dumps({k: v.get("GECTI") for k, v in T.items()}, indent=1))
    print("HEPSI_GECTI", rap["hepsi_gecti"])


if __name__ == "__main__":
    main()
