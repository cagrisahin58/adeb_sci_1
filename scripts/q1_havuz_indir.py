"""Faz 2.2 (LeCun plani): genisletilmis CIFAR-10 havuzu icin RobustBench modellerini indirir
(models/robustbench_zoo). Egitim yok. Konteynerde: docker exec -w /workspace adeb_eval python scripts/q1_havuz_indir.py
"""
import time

import torch
from robustbench.utils import load_model

MODELLER = [
    "Standard",                       # standart egitimli WRN-28-10 (temiz 94.78, gurbuz 0) -> p standart hedefte
    "Wong2020Fast",                   # PreActResNet-18, FGSM-AT
    "Engstrom2019Robustness",         # ResNet-50, PGD-AT
    "Carmon2019Unlabeled",            # WRN-28-10, yari gozetimli
    "Debenedetti2022Light_XCiT-S12",  # XCiT-S12 (dönüştürücü)
    "Gowal2020Uncovering_28_10_extra",# WRN-28-10 (makaledeki referans)
]
for ad in MODELLER:
    t = time.time()
    try:
        m = load_model(model_name=ad, dataset="cifar10", threat_model="Linf", model_dir="models/robustbench_zoo")
        n = sum(p.numel() for p in m.parameters()) / 1e6
        print(f"OK   {ad:36s} {n:6.1f}M param  {time.time()-t:5.1f}s")
        del m
        torch.cuda.empty_cache()
    except Exception as e:  # noqa: BLE001
        print(f"HATA {ad}: {type(e).__name__}: {str(e)[:200]}")
