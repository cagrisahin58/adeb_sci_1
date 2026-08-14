"""E2 sizinti ablasyonu bolmeleri: D_core 44k + V_A 2k + V_B 2k + V_C 2k (CIFAR-10).

Tasarim (Q1 raporu E2 + baslatma-oncesi denetim guncellemesi 2026-08-14):
clean on-egitim V_A'yi GORUR (sizinti tedavisi), V_B ve V_C'yi gormez; AT
yalniz D_core uzerinde, tam butce, patience kapali, her epoch checkpoint'li.
UC secim kurali ayni yorungeye CEVRIMDISI uygulanir (q1_offline_select.py):
  V_A = sizintili secim  (clean on-egitimde gorulmus)
  V_B = temiz secim      (hic gorulmemis)
  V_C = negatif kontrol  (hic gorulmemis) -> V_B-vs-V_C farki iki esit-temiz
        bolme arasindaki SAF secim-gurultusu tabanini olcer; V_A-vs-V_B
        sizinti etkisi bu tabana karsi okunur. Egitim basladiktan sonra
        eklenemez (D_core'u degistirir) - bu yuzden bastan dahil.

Uretilen dosyalar (get_loaders_with_val'in "egitimden cikarilacak indeksler"
semantigiyle; hepsi atomik yazilir, en son e2_val_C.json -> pipeline guard'i):
  data/e2_exclude_for_clean.json  = V_B u V_C        (clean: D_core+V_A egitilir)
  data/e2_exclude_for_at.json     = V_A u V_B u V_C  (AT: yalniz D_core=44k)
  data/e2_val_A.json / _B / _C    = secim bolmeleri (2'ser bin)
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

out_names = [
    "e2_exclude_for_clean.json",
    "e2_exclude_for_at.json",
    "e2_val_A.json",
    "e2_val_B.json",
    "e2_val_C.json",  # en son yazilir; pipeline guard'i bu dosya
]
if all(os.path.exists(os.path.join(ROOT, "data", f)) for f in out_names):
    print("ZATEN VAR: data/e2_*.json — degistirilmedi (idempotent)")
    raise SystemExit(0)

g = torch.Generator().manual_seed(SPLIT_SEED)
perm = torch.randperm(N_TRAIN, generator=g).tolist()
val_A = sorted(perm[:VAL_SIZE])
val_B = sorted(perm[VAL_SIZE:2 * VAL_SIZE])
val_C = sorted(perm[2 * VAL_SIZE:3 * VAL_SIZE])

payloads = {
    "e2_exclude_for_clean.json": {
        "dataset": "cifar10", "split_seed": SPLIT_SEED, "n_train_total": N_TRAIN,
        "val_size": len(val_B) + len(val_C),
        "role": "E2 clean asamasi: V_B ve V_C haric (V_A GORULUR - sizinti tedavisi)",
        "val_indices": sorted(val_B + val_C),
    },
    "e2_exclude_for_at.json": {
        "dataset": "cifar10", "split_seed": SPLIT_SEED, "n_train_total": N_TRAIN,
        "val_size": len(val_A) + len(val_B) + len(val_C),
        "role": "E2 AT asamasi: V_A, V_B, V_C ucu de haric (D_core=44k)",
        "val_indices": sorted(val_A + val_B + val_C),
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
    "e2_val_C.json": {
        "dataset": "cifar10", "split_seed": SPLIT_SEED, "n_train_total": N_TRAIN,
        "val_size": len(val_C),
        "role": "E2 NEGATIF KONTROL bolmesi (hic gorulmemis; V_B-vs-V_C = gurultu tabani)",
        "val_indices": val_C,
    },
}
assert not set(val_A) & set(val_B), "V_A ve V_B kesisiyor!"
assert not set(val_A) & set(val_C), "V_A ve V_C kesisiyor!"
assert not set(val_B) & set(val_C), "V_B ve V_C kesisiyor!"
assert set(payloads["e2_exclude_for_at.json"]["val_indices"]) == \
    set(val_A) | set(val_B) | set(val_C), "exclude_for_at != V_A u V_B u V_C"
assert set(payloads["e2_exclude_for_clean.json"]["val_indices"]) == \
    set(val_B) | set(val_C), "exclude_for_clean != V_B u V_C"

for fname in out_names:  # sirali: guard dosyasi (val_C) en son
    path = os.path.join(ROOT, "data", fname)
    with open(path + ".tmp", "w") as f:
        json.dump(payloads[fname], f)
    os.replace(path + ".tmp", path)
    print(f"yazildi: {path} ({payloads[fname]['val_size']} indeks)")
