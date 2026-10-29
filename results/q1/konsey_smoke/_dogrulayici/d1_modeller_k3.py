"""Celisik dogrulayici, D1: K3 girdi hatti, normalizasyon, agirlik yukleme.

B1 kod raporunun smoke testlerinden bagimsiz: kaynak safetensors dosyasini
dogrudan okuyup her govde tensorunu modele yuklenenle karsilastirir.
Cikti: results/q1/konsey_smoke/_dogrulayici/d1_modeller_k3.json
"""
import json
import sys
from pathlib import Path

import torch
import torch.nn as nn

sys.path.insert(0, "/workspace")
from safetensors.torch import load_file  # noqa: E402

from src.models import ModelRegistry  # noqa: E402
from src.models.r224 import ResizeNormalize, load_imagenet_init  # noqa: E402
from src.utils.checkpoint import load_model_weights  # noqa: E402

out = {}
torch.manual_seed(0)
x = torch.rand(4, 3, 32, 32)

vscr = ModelRegistry.get("vit_tiny", num_classes=10).eval()
rscr = ModelRegistry.get("resnet18_224", num_classes=10).eval()
rin = ModelRegistry.get("resnet18_224_in1k", num_classes=10).eval()
vin = ModelRegistry.get("vit_tiny_in1k", num_classes=10).eval()

# 1) K3: R224-scr ile V-scr girdi hatti
out["vscr_resize_tipi"] = type(vscr.resize).__name__
out["rscr_resize_tipi"] = type(rscr.resize).__name__
out["vscr_resize_repr"] = repr(vscr.resize)
out["rscr_resize_repr"] = repr(rscr.resize)
out["rscr_vscr_resize_torch_equal"] = bool(torch.equal(vscr.resize(x), rscr.resize(x)))
out["rscr_state_dict_resize_anahtarlari"] = [k for k in rscr.state_dict() if k.startswith("resize")]
out["vscr_state_dict_resize_anahtarlari"] = [k for k in vscr.state_dict() if k.startswith("resize")]
# R224-scr ileri gecisi: model.model(upsample(x)) ile ayni mi (gizli normalizasyon yok)
with torch.no_grad():
    up = nn.functional.interpolate(x, size=(224, 224), mode="bilinear", align_corners=False)
    out["rscr_forward_eq_elle_upsample"] = bool(torch.allclose(rscr(x), rscr.model(up), atol=0, rtol=0))
    out["vscr_forward_eq_elle_upsample"] = bool(torch.allclose(vscr(x), vscr.model(up), atol=0, rtol=0))

# 2) IN normalizasyonu yalniz IN tiplerinde
for ad, m in (("resnet18_224_in1k", rin), ("vit_tiny_in1k", vin)):
    rz = m.resize
    d = {"resize_tipi": type(rz).__name__,
         "normalize": bool(getattr(rz, "normalize", False)),
         "mean": [round(float(v), 6) for v in rz.mean.flatten()],
         "std": [round(float(v), 6) for v in rz.std.flatten()],
         "state_dict_resize_anahtarlari": [k for k in m.state_dict() if k.startswith("resize")]}
    mean = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)
    with torch.no_grad():
        elle = m.model((up - mean) / std)
        d["forward_eq_elle_norm_maxabs"] = float((m(x) - elle).abs().max())
        if hasattr(m.model, "forward_features") and ad == "vit_tiny_in1k":
            d["get_features_normli_maxabs"] = float(
                (m.get_features(x) - m.model.forward_features((up - mean) / std)).abs().max())
    out[ad] = d
out["vscr_resize_normalize_var_mi"] = isinstance(vscr.resize, ResizeNormalize)
out["rscr_resize_normalize_var_mi"] = isinstance(rscr.resize, ResizeNormalize)

# V-IN mimarisi V-scr ile ayni mi (model.model anahtar ve sekilleri)
a = {k: tuple(v.shape) for k, v in vscr.model.state_dict().items()}
b = {k: tuple(v.shape) for k, v in vin.model.state_dict().items()}
out["vin_vscr_govde_ayni"] = a == b
out["vin_govde_anahtar_sayisi"] = len(b)

# 3) Agirlik yukleme: kaynak safetensors ile tensor tensor karsilastirma
def bagimsiz_yukleme(model, init_key, tip, dosya, bas):
    rep = load_imagenet_init(model, init_key, tip)
    src = load_file(dosya)
    tgt = model.model.state_dict()
    esit, farkli, eksik_hedefte, bas_atlanan = 0, [], [], []
    for k, v in src.items():
        if k == bas or k.startswith(bas + "."):
            bas_atlanan.append(k)
            continue
        if k not in tgt:
            eksik_hedefte.append(k)
            continue
        if tgt[k].shape == v.shape and torch.equal(tgt[k].cpu().to(v.dtype), v):
            esit += 1
        else:
            farkli.append(k)
    hedef_kaynakta_yok = [k for k in tgt if k not in src and not k.startswith(bas)]
    return {
        "rapor_n_loaded": rep["n_loaded"], "rapor_n_target_keys": rep["n_target_keys"],
        "rapor_missing_nonhead": rep["missing_nonhead"],
        "rapor_unexpected_nonhead": rep["unexpected_nonhead"],
        "rapor_shape_mismatch": rep["shape_mismatch"],
        "rapor_head_keys_skipped": rep["head_keys_skipped"],
        "rapor_norm_matches_cfg": rep["norm_matches_cfg"],
        "rapor_source_sha256_ilk12": (rep["source_sha256"] or "")[:12],
        "bagimsiz_kaynak_anahtar_sayisi": len(src),
        "bagimsiz_govde_esit_tensor": esit,
        "bagimsiz_govde_farkli": farkli,
        "bagimsiz_kaynakta_olup_hedefte_olmayan": eksik_hedefte,
        "bagimsiz_hedefte_olup_kaynakta_olmayan_bas_disi": hedef_kaynakta_yok,
        "bagimsiz_bas_atlanan": bas_atlanan,
        "hedef_bas_sekli": [tuple(tgt[k].shape) for k in tgt if k.startswith(bas)],
    }


out["yukleme_deit"] = bagimsiz_yukleme(
    vin, "deit_tiny_in1k", "vit_tiny_in1k",
    "models/timm_agirliklar/deit_tiny_patch16_224.fb_in1k/model.safetensors", "head")
out["yukleme_resnet18_a1"] = bagimsiz_yukleme(
    rin, "resnet18_a1_in1k", "resnet18_224_in1k",
    "models/timm_agirliklar/resnet18.a1_in1k/model.safetensors", "fc")

# 4) Uyumsuz tip reddi (K3 demeti)
red = {}
for init_key, tip, m in (("resnet18_a1_in1k", "resnet18_224", rscr),
                         ("deit_tiny_in1k", "vit_tiny", vscr),
                         ("deit_tiny_in1k", "resnet18_224_in1k", rin)):
    try:
        load_imagenet_init(m, init_key, tip)
        red[f"{init_key}->{tip}"] = "KABUL EDILDI (beklenmez)"
    except ValueError as e:
        red[f"{init_key}->{tip}"] = "ValueError"
out["uyumsuz_tip_reddi"] = red

# 5) Normalizasyonlu checkpoint normalizasyonsuz tipe strict yukleme
try:
    ModelRegistry.get("resnet18_224", num_classes=10).load_state_dict(rin.state_dict(), strict=True)
    out["in_ckpt_scr_tipine_strict"] = "YUKLENDI (beklenmez)"
except RuntimeError as e:
    out["in_ckpt_scr_tipine_strict"] = "RuntimeError: " + str(e).splitlines()[0][:160]

# 6) Smoke checkpoint'leri tasarlanan tiple yukleniyor mu (load_model_weights)
ck = {}
for tip, p in (("vit_tiny_in1k", "models/q1/konsey_smoke/v_in/vit_tiny_in1k/clean/best.pth"),
               ("resnet18_224_in1k", "models/q1/konsey_smoke/r_in/resnet18_224_in1k/clean/best.pth"),
               ("resnet18_224", "models/q1/konsey_smoke/r_scr/resnet18_224/clean/best.pth")):
    m = ModelRegistry.get(tip, num_classes=10)
    try:
        load_model_weights(m, p, "cpu")
        sd = torch.load(p, map_location="cpu", weights_only=False)
        sd = sd.get("model_state_dict", sd)
        ck[tip] = {"yuklendi": True, "resize_anahtarlari": [k for k in sd if k.startswith("resize")]}
    except Exception as e:  # noqa: BLE001
        ck[tip] = {"yuklendi": False, "hata": str(e)[:200]}
out["smoke_ckpt_yukleme"] = ck

Path("results/q1/konsey_smoke/_dogrulayici/d1_modeller_k3.json").write_text(
    json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(out, indent=1, ensure_ascii=False))
