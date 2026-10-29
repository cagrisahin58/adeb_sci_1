"""Konsey B1 smoke: transfer matrisindeki MI-PGD ve TGR yollarinin kaynak
uygulamalarla birebir ayni ornek urettigini sinar (bir batch, 50 ornek).
  MI : experiments/c1_c3_transfer_matrix.py::mifgsm_m84  vs  experiments/run_c_addenda.py::mifgsm
  TGR: matristeki cagri (tgr.mifgsm use_tgr=True, C2 ayarlari) vs c1_c2_tgr.mifgsm dogrudan
"""
import importlib.util
import json
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    from src.data import get_loaders
    from src.utils.load_model_auto import load_model_auto

    dev = torch.device("cuda")
    tm = load("tm", ROOT / "experiments/c1_c3_transfer_matrix.py")
    ad = load("ad", ROOT / "experiments/run_c_addenda.py")
    tg = load("tg", ROOT / "experiments/c1_c2_tgr.py")
    _, loader = get_loaders(dataset="cifar10", data_dir="./data", test_batch_size=50)
    x, y = next(iter(loader))
    x, y = x.to(dev), y.to(dev)
    res = {}
    r = load_model_auto("resnet18", "models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth", dev)
    a1 = tm.mifgsm_m84(r, x, y, eps=tm.EPS, steps=10)
    a2 = ad.mifgsm(r, x, y)
    res["mi_birebir"] = bool(torch.equal(a1, a2))
    res["mi_max_fark"] = float((a1 - a2).abs().max())
    res["mi_linf"] = float((a1 - x).abs().max())
    res["mi_alpha"] = tm.EPS / 10
    res["addenda_eps"] = float(ad.EPS)
    v = load_model_auto("vit_tiny", "models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth", dev)
    tgr_mod = tm._tgr_module()
    b1 = tgr_mod.mifgsm(v, x, y, use_tgr=True, eps=tm.EPS, alpha=tgr_mod.ALPHA, steps=10, mu=tgr_mod.MU)
    b2 = tg.mifgsm(v, x, y, use_tgr=True)
    b3 = tg.mifgsm(v, x, y, use_tgr=False)
    res["tgr_birebir"] = bool(torch.equal(b1, b2))
    res["tgr_mi_den_farkli"] = bool(not torch.equal(b2, b3))
    res["tgr_linf"] = float((b1 - x).abs().max())
    res["GECTI"] = res["mi_birebir"] and res["tgr_birebir"] and res["tgr_mi_den_farkli"]
    print(json.dumps(res, indent=1))
    Path("results/q1/konsey_smoke/mi_tgr_esitlik.json").write_text(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
