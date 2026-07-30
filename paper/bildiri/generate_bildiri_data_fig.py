"""Bildiri veri figuru (fig_b4_data_adv.pdf):
  Ust serit: CIFAR-10'un 10 sinifindan birer ornek (veri tanitimi)
  Alt iki satir: her modelin KENDI white-box PGD-10 saldirisiyla
    clean(tahmin) | pertürbasyon (x10) | adversarial(tahmin)
  Ornek secimi: clean-dogru VE saldirinin sinifi degistirdigi ilk ornek.

Çalıştırma: docker exec adeb_eval python /workspace/paper/bildiri/generate_bildiri_data_fig.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import torch
import torch.nn.functional as F

# Repo koku: bu dosya paper/bildiri/ altinda oldugundan iki ust dizin.
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from src.attacks.pgd import PGDAttack  # noqa: E402
from src.data import get_cifar10_loaders  # noqa: E402
from src.models import ModelRegistry  # noqa: E402
from src.utils.checkpoint import load_model_weights  # noqa: E402

OUT = os.path.join(ROOT, "paper/bildiri/figures/fig_b4_data_adv.pdf")
CLASSES = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]

torch.manual_seed(42)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MODELS = {
    "ResNet-18 (AT)": ("resnet18", "models/resnet18/adv/at_run3/resnet18/adv/adversarial_training/best.pth"),
    "ViT-Tiny (AT)": ("vit_tiny", "models/vit_tiny/adv/at_run3/vit_tiny/adv/adversarial_training/best.pth"),
}

_, test_loader = get_cifar10_loaders(data_dir="./data", test_batch_size=200)
images, labels = next(iter(test_loader))
images, labels = images.to(device), labels.to(device)

# --- Ust serit icin: her siniftan ilk ornek ---------------------------------
strip = {}
for img, lab in zip(images, labels):
    c = int(lab)
    if c not in strip:
        strip[c] = img.cpu()
    if len(strip) == 10:
        break

# --- Saldiri ornekleri -------------------------------------------------------
rows = []
for name, (mtype, mpath) in MODELS.items():
    model = ModelRegistry.get(mtype)
    load_model_weights(model, mpath, device)
    model = model.to(device).eval()
    atk = PGDAttack(model, eps=8 / 255, alpha=2 / 255, steps=10)
    adv = atk.attack(images, labels)
    with torch.no_grad():
        p_clean = F.softmax(model(images), 1)
        p_adv = F.softmax(model(adv), 1)
    pred_c, conf_c = p_clean.argmax(1), p_clean.max(1)[0]
    pred_a, conf_a = p_adv.argmax(1), p_adv.max(1)[0]
    ok = (pred_c == labels) & (pred_a != labels)
    idx = int(torch.nonzero(ok)[0])
    rows.append({
        "name": name,
        "clean": images[idx].cpu(),
        "adv": adv[idx].detach().cpu(),
        "pert": (adv[idx] - images[idx]).detach().cpu(),
        "pc": (CLASSES[int(pred_c[idx])], float(conf_c[idx])),
        "pa": (CLASSES[int(pred_a[idx])], float(conf_a[idx])),
    })
    del model
    torch.cuda.empty_cache()
    print(f"{name}: ornek {idx}: {rows[-1]['pc'][0]} -> {rows[-1]['pa'][0]}")

# --- Cizim -------------------------------------------------------------------
plt.rcParams.update({"font.size": 8, "figure.dpi": 150, "savefig.bbox": "tight"})
fig = plt.figure(figsize=(5.2, 4.6))
gs = GridSpec(3, 10, figure=fig, height_ratios=[1.0, 1.9, 1.9], hspace=0.45, wspace=0.1)

for c in range(10):
    ax = fig.add_subplot(gs[0, c])
    ax.imshow(strip[c].permute(1, 2, 0).numpy(), interpolation="nearest")
    ax.set_title(CLASSES[c], fontsize=6.2, pad=2)
    ax.axis("off")

def show(ax, img, title):
    ax.imshow(np.clip(img.permute(1, 2, 0).numpy(), 0, 1), interpolation="nearest")
    ax.set_title(title, fontsize=8, pad=3)
    ax.axis("off")

for r, row in enumerate(rows, start=1):
    ax1 = fig.add_subplot(gs[r, 0:3])
    show(ax1, row["clean"], f"clean: {row['pc'][0]} ({row['pc'][1]*100:.0f}%)")
    ax2 = fig.add_subplot(gs[r, 3:6])
    pert = row["pert"]
    pert_vis = (pert * 10 + 0.5)
    show(ax2, pert_vis, "perturbation ($\\times$10)")
    ax3 = fig.add_subplot(gs[r, 6:9])
    show(ax3, row["adv"], f"adversarial: {row['pa'][0]} ({row['pa'][1]*100:.0f}%)")
    axl = fig.add_subplot(gs[r, 9])
    axl.text(0.1, 0.5, row["name"].replace(" (AT)", "\n(AT)"), fontsize=8, fontweight="bold",
             va="center", rotation=90)
    axl.axis("off")

fig.savefig(OUT)
print(f"kaydedildi: {OUT}")
