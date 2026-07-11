"""AT cokusu teshisi 2: kademeli cokus + BN running-stats zehirlenmesi testi.

300 batch temiz AT kosar; her 50 batch'te:
  - eval-mode val acc (BN running stats ile)  -> cokuyorsa ve
  - BN-yenilemeli val acc (running stats'i clean batch'lerle tazeleyip)  -> saglamsa
  cokusun parametrelerde degil BN istatistiklerinde oldugu kanitlanir.
"""
import sys
import copy
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch

from src.models import ModelRegistry
from src.utils.checkpoint import load_model_weights
from src.data import get_cifar10_loaders_with_val
from src.defenses.adversarial_training import AdversarialTraining

device = torch.device("cuda")
torch.manual_seed(0)

train_loader, val_loader, _ = get_cifar10_loaders_with_val(
    data_dir="./data", batch_size=128, val_size=2000, split_seed=42)


def val_acc(model, max_batches=10):
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for i, (x, y) in enumerate(val_loader):
            if i >= max_batches:
                break
            x, y = x.to(device), y.to(device)
            correct += (model(x).argmax(1) == y).sum().item()
            total += y.size(0)
    return 100 * correct / total


def val_acc_bn_refreshed(model, refresh_batches=20, max_batches=10):
    """BN running stats'i temiz egitim goruntuleriyle tazeleyip olc (kopyada)."""
    m = copy.deepcopy(model)
    for mod in m.modules():
        if isinstance(mod, torch.nn.modules.batchnorm._BatchNorm):
            mod.reset_running_stats()
    m.train()
    with torch.no_grad():
        for i, (x, _) in enumerate(train_loader):
            if i >= refresh_batches:
                break
            m(x.to(device))
    acc = val_acc(m, max_batches)
    del m
    return acc


model = ModelRegistry.get("resnet18")
load_model_weights(model, "models/resnet18/clean/best.pth", device)
model = model.to(device)

defense = AdversarialTraining(model=model, eps=8/255, alpha=2/255, steps=10, device=device)
optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9, weight_decay=5e-4)

print(f"batch 0: eval-val={val_acc(model):.2f}%")

model.train()
running = 0.0
it = iter(train_loader)
for step in range(1, 301):
    try:
        xb, yb = next(it)
    except StopIteration:
        it = iter(train_loader)
        xb, yb = next(it)
    xb, yb = xb.to(device), yb.to(device)

    optimizer.zero_grad()
    loss = defense.get_loss(model, xb, yb)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=10.0)
    optimizer.step()
    running += loss.item()

    if step % 50 == 0:
        ev = val_acc(model)
        bn = val_acc_bn_refreshed(model)
        print(f"batch {step}: loss(avg50)={running / 50:.3f} "
              f"eval-val={ev:.2f}%  BN-yenilemeli-val={bn:.2f}%")
        running = 0.0
        model.train()

print("DIAG2_DONE")
