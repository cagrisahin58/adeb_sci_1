"""rev2 C1: Ortak sabit validasyon bolmesi uret (leak fix).

CIFAR-10 egitim setinden (50k) 2000 indekslik SABIT validasyon kumesi.
Egitim seed'lerinden bagimsizdir (split seed 777, tek seferlik); ayni dosya
hem clean pretraining hem adversarial fine-tuning tarafindan kullanilir,
boylece validasyon ornekleri hicbir egitim asamasinda gorulmez.

Çalıştırma: docker exec adeb_eval python /workspace/experiments/rev2/make_val_split.py
Çıktı: data/val_split_indices.json
"""
import json
import os

import torch

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
OUT = os.path.join(ROOT, "data/val_split_indices.json")

SPLIT_SEED = 777
N_TRAIN = 50000
VAL_SIZE = 2000

if os.path.exists(OUT):
    with open(OUT) as f:
        existing = json.load(f)
    print(f"ZATEN VAR: {OUT} (split_seed={existing.get('split_seed')}, "
          f"n={len(existing['val_indices'])}) — degistirilmedi (idempotent)")
    raise SystemExit(0)

generator = torch.Generator().manual_seed(SPLIT_SEED)
perm = torch.randperm(N_TRAIN, generator=generator).tolist()
val_indices = sorted(perm[:VAL_SIZE])

payload = {
    "split_seed": SPLIT_SEED,
    "n_train_total": N_TRAIN,
    "val_size": VAL_SIZE,
    "note": "rev2 C1 ortak sabit val bolmesi; clean pretraining VE adversarial "
            "fine-tuning bu ornekleri egitimden cikarir (leak fix). Egitim "
            "seed'lerinden bagimsizdir.",
    "val_indices": val_indices,
}
with open(OUT, "w") as f:
    json.dump(payload, f)
print(f"yazildi: {OUT} ({VAL_SIZE} indeks, split_seed={SPLIT_SEED})")
