"""Celisik dogrulayici, D3: MI-PGD ve TGR'nin uctan uca bagimsiz sinamasi.

Matris betiginin --attack mi / --attack tgr ciktilarini (n=100, iki C1 modeli
+ varsayilan WRN referansi), referans kaynaklardan bagimsiz hesaplanan
cekismeli orneklerle ornek ornek karsilastirir:
  MI  : experiments/run_c_addenda.py icindeki mifgsm (foy M8.4 kaynagi C22),
        ast ile kaynaktan cikarilip calistirilir (modul yan etkisi olmadan)
  TGR : experiments/c1_c2_tgr.py::mifgsm(use_tgr=True), C2'deki varsayilan
        cagri bicimiyle (eps, alpha, steps, mu verilmeden)
Kullanim: python d3_mi_tgr_bagimsiz.py MI_KLASORU TGR_KLASORU CIKTI_JSON
"""
import ast
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, "/workspace")
from robustbench.utils import load_model  # noqa: E402

from src.data import get_loaders  # noqa: E402
from src.models import ModelRegistry  # noqa: E402
from src.utils.checkpoint import load_model_weights  # noqa: E402

mi_dir, tgr_dir, cikti = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
dev = torch.device("cuda")
EPS = 8 / 255
N = 100

# run_c_addenda.mifgsm'i kaynaktan cikar
src_txt = Path("experiments/run_c_addenda.py").read_text()
fn = next(n for n in ast.parse(src_txt).body if isinstance(n, ast.FunctionDef) and n.name == "mifgsm")
ns = {"torch": torch, "nn": nn, "EPS": EPS}
exec(compile(ast.Module(body=[fn], type_ignores=[]), "run_c_addenda_mifgsm", "exec"), ns)
mifgsm_c22 = ns["mifgsm"]

spec = importlib.util.spec_from_file_location("c1_c2_tgr_ref", "experiments/c1_c2_tgr.py")
tgr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tgr)


def yerel(tip, yol):
    m = ModelRegistry.get(tip, num_classes=10)
    load_model_weights(m, yol, dev)
    return m.to(dev).eval()


modeller = {
    "ResNet18_AT_s1001": yerel("resnet18", "models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth"),
    "ViT_Tiny_AT_s2001": yerel("vit_tiny", "models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth"),
    "WRN_28_10": load_model(model_name="Gowal2020Uncovering_28_10_extra", dataset="cifar10",
                            threat_model="Linf", model_dir="models/robustbench_zoo").to(dev).eval(),
}
_, loader = get_loaders(dataset="cifar10", data_dir="./data", test_batch_size=50)
batches = []
seen = 0
for x, y in loader:
    if seen >= N:
        break
    batches.append((x, y))
    seen += y.size(0)


def satirlar(saldiri, kaynak):
    aw = {t: [] for t in modeller}
    for x, y in batches:
        x, y = x.to(dev), y.to(dev)
        adv = saldiri(modeller[kaynak], x, y)
        linf = float((adv - x).abs().max())
        with torch.no_grad():
            for t, m in modeller.items():
                aw[t].append((m(adv).argmax(1) != y).cpu().numpy())
    return {t: np.concatenate(v) for t, v in aw.items()}, linf


sonuc = {}
for ad, klasor, kaynaklar, saldiri in (
        ("MI", mi_dir, ["ResNet18_AT_s1001", "ViT_Tiny_AT_s2001", "WRN_28_10"],
         lambda m, x, y: mifgsm_c22(m, x, y, eps=EPS, steps=10, mu=1.0)),
        ("TGR", tgr_dir, ["ViT_Tiny_AT_s2001"],
         lambda m, x, y: tgr.mifgsm(m, x, y, use_tgr=True))):
    j = json.loads((klasor / "transfer_matrix.json").read_text())
    s = {"json_attack": j.get("attack"), "json_alpha": j.get("alpha"), "json_steps": j.get("steps"),
         "json_sources": j.get("sources"), "hucreler": {}}
    for k in kaynaklar:
        if not (klasor / f"per_sample_{k}_to_{k}.npz").exists():
            s["hucreler"][k] = "matriste bu kaynak yok"
            continue
        ref, linf = satirlar(saldiri, k)
        s["hucreler"][k + "_linf_max"] = linf
        for t in modeller:
            d = np.load(klasor / f"per_sample_{k}_to_{t}.npz")
            s["hucreler"][f"{k}->{t}"] = {
                "farkli_ornek": int((d["target_adv_wrong"] != ref[t]).sum()),
                "matris_yaniltma_sayisi": int(d["target_adv_wrong"].sum()),
                "bagimsiz_yaniltma_sayisi": int(ref[t].sum())}
    sonuc[ad] = s

# TGR, duz MI-FGSM'den (ayni ayarlar, kancasiz) farkli mi
duz, _ = satirlar(lambda m, x, y: tgr.mifgsm(m, x, y, use_tgr=False), "ViT_Tiny_AT_s2001")
tg, _ = satirlar(lambda m, x, y: tgr.mifgsm(m, x, y, use_tgr=True), "ViT_Tiny_AT_s2001")
sonuc["TGR_duz_MI_farki"] = {t: int((duz[t] != tg[t]).sum()) for t in modeller}
# TGR matrisinde CNN kaynaklari atlanmis mi
sonuc["TGR_matris_kaynak_dosyalari"] = sorted({p.name.split("_to_")[0] for p in tgr_dir.glob("per_sample_*.npz")})
cikti.write_text(json.dumps(sonuc, indent=1, ensure_ascii=False))
print(json.dumps(sonuc, indent=1, ensure_ascii=False))
