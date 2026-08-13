"""E2 sizinti ablasyonu bolmeleri: D_core 46k + V_A 2k + V_B 2k (CIFAR-10).

Tasarim (Q1 raporu E2): clean on-egitim D_core u V_A uzerinde yapilir (V_A
GORULMUS, V_B hic gorulmemis); AT yalniz D_core uzerinde, tam butce, patience
kapali, her epoch checkpoint'li. Iki secim kurali (V_A = sizintili, V_B =
temiz) ayni yorungeye CEVRIMDISI uygulanir (scripts/q1_offline_select.py).

Uretilen dosyalar (get_loaders_with_val'in "egitimden cikarilacak indeksler"
semantigiyle):
  data/e2_exclude_for_clean.json  = V_B           (clean: D_core+V_A egitilir)
  data/e2_exclude_for_at.json     = V_A u V_B     (AT: yalniz D_core egitilir)
  data/e2_val_A.json              = V_A           (sizintili secim bolmesi)
  data/e2_val_B.json              = V_B           (temiz secim bolmesi)
"""
import json
import os
import sys

import torch

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
sys.path.insert(0, ROOT)

SPLIT_SEED = 778  # C1'in 777'sinden bilerek farkli (bagimsiz bolme)
N_TRAIN = 50000
VAL_SIZE = 2000

out_files = {
    "e2_exclude_for_clean.json": None,
    "e2_exclude_for_at.json": None,
    "e2_val_A.json": None,
    "e2_val_B.json": None,
}
if all(os.path.exists(os.path.join(ROOT, "data", f)) for f in out_files):
    print("ZATEN VAR: data/e2_*.json — degistirilmedi (idempotent)")
    raise SystemExit(0)

g = torch.Generator().manual_seed(SPLIT_SEED)
perm = torch.randperm(N_TRAIN, generator=g).tolist()
val_A = sorted(perm[:VAL_SIZE])
val_B = sorted(perm[VAL_SIZE:2 * VAL_SIZE])

payloads = {
    "e2_exclude_for_clean.json": {
        "dataset": "cifar10", "split_seed": SPLIT_SEED, "n_train_total": N_TRAIN,
        "val_size": len(val_B), "role": "E2 clean asamasi: yalniz V_B haric (V_A GORULUR)",
        "val_indices": val_B,
    },
    "e2_exclude_for_at.json": {
        "dataset": "cifar10", "split_seed": SPLIT_SEED, "n_train_total": N_TRAIN,
        "val_size": len(val_A) + len(val_B),
        "role": "E2 AT asamasi: V_A ve V_B ikisi de haric (D_core=46k)",
        "val_indices": sorted(val_A + val_B),
    },
    "e2_val_A.json": {
        "dataset": "cifar10", "split_seed": SPLIT_SEED, "n_train_total": N_TRAIN,
        "val_size": len(val_A), "role": "E2 SIZINTILI secim bolmesi (clean'de gorulmus)",
        "val_indices": val_A,
    },
    "e2_val_B.json": {
        "dataset": "cifar10", "split_seed": SPLIT_SEED, "n_train_total": N_TRAIN,
        "val_size": len(val_B), "role": "E2 TEMIZ secim bolmesi (hic gorulmemis)",
        "val_indices": val_B,
    },
}
assert not set(val_A) & set(val_B), "V_A ve V_B kesisiyor!"
for fname, payload in payloads.items():
    path = os.path.join(ROOT, "data", fname)
    with open(path, "w") as f:
        json.dump(payload, f)
    print(f"yazildi: {path} ({payload['val_size']} indeks)")
