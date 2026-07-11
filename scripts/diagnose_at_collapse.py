"""AT run3 cokusu teshisi.

Sorular:
1. Pretrained ResNet18 val(2000) ve test uzerinde clean acc kac? (~%94 beklenir)
2. Eski (loss.backward) ve yeni (autograd.grad) PGD ayni adv ornekleri mi uretiyor?
3. Tek AT adimi (get_loss -> backward -> clip -> step, LR 0.001) sonrasi clean acc?
4. 10 AT adimi sonrasi clean acc? (cokus tek adimda mi kademeli mi)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
import torch.nn as nn

from src.models import ModelRegistry
from src.utils.checkpoint import load_model_weights
from src.data import get_cifar10_loaders_with_val
from src.defenses.adversarial_training import AdversarialTraining

device = torch.device("cuda")
torch.manual_seed(0)

train_loader, val_loader, test_loader = get_cifar10_loaders_with_val(
    data_dir="./data", batch_size=128, val_size=2000, split_seed=42)


def clean_acc(model, loader, max_batches=20):
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for i, (x, y) in enumerate(loader):
            if i >= max_batches:
                break
            x, y = x.to(device), y.to(device)
            correct += (model(x).argmax(1) == y).sum().item()
            total += y.size(0)
    return 100 * correct / total


def fresh_model():
    m = ModelRegistry.get("resnet18")
    load_model_weights(m, "models/resnet18/clean/best.pth", device)
    return m.to(device)


# --- 1. Yuklenen pretrained modelin clean acc'i
model = fresh_model()
print(f"[1] Pretrained clean acc: val={clean_acc(model, val_loader):.2f}%  "
      f"test={clean_acc(model, test_loader, 10):.2f}%")

# --- 2. Saldiri esdegerligi (eski backward-birikimli vs yeni autograd.grad)
x, y = next(iter(train_loader))
x, y = x.to(device)[:64], y.to(device)[:64]

def old_pgd(model, images, labels, eps=8/255, alpha=2/255, steps=10):
    """run2'deki orijinal implementasyon (loss.backward + images.grad)."""
    loss_fn = nn.CrossEntropyLoss()
    images = images.detach()
    original = images.clone()
    torch.manual_seed(123)
    images = images + torch.empty_like(images).uniform_(-eps, eps)
    images = torch.clamp(images, 0, 1)
    for _ in range(steps):
        images.requires_grad = True
        loss = loss_fn(model(images), labels)
        loss.backward()
        adv = images + alpha * images.grad.sign()
        delta = torch.clamp(adv - original, -eps, eps)
        images = torch.clamp(original + delta, 0, 1).detach()
    return images

def new_pgd(model, images, labels, eps=8/255, alpha=2/255, steps=10):
    """M10 duzeltmeli implementasyon (autograd.grad)."""
    loss_fn = nn.CrossEntropyLoss()
    images = images.detach()
    original = images.clone()
    torch.manual_seed(123)
    images = images + torch.empty_like(images).uniform_(-eps, eps)
    images = torch.clamp(images, 0, 1)
    for _ in range(steps):
        images = images.detach().requires_grad_(True)
        loss = loss_fn(model(images), labels)
        grad = torch.autograd.grad(loss, images)[0]
        adv = images + alpha * grad.sign()
        delta = torch.clamp(adv - original, -eps, eps)
        images = torch.clamp(original + delta, 0, 1).detach()
    return images

model.eval()
model.zero_grad()
adv_old = old_pgd(model, x, y)
leftover = sum(p.grad.abs().sum().item() for p in model.parameters() if p.grad is not None)
model.zero_grad()
adv_new = new_pgd(model, x, y)
print(f"[2] adv_old vs adv_new max fark: {(adv_old - adv_new).abs().max().item():.3e} "
      f"(0 olmali) | eski yontemin param.grad kirliligi: {leftover:.1f}")

# --- 3-4. AT adimlari sonrasi cokus takibi
model = fresh_model()
defense = AdversarialTraining(model=model, eps=8/255, alpha=2/255, steps=10, device=device)
optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9, weight_decay=5e-4)

model.train()
it = iter(train_loader)
for step in range(10):
    xb, yb = next(it)
    xb, yb = xb.to(device), yb.to(device)
    optimizer.zero_grad()
    loss = defense.get_loss(model, xb, yb)
    loss.backward()
    gnorm = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=10.0)
    optimizer.step()
    if step in (0, 1, 4, 9):
        acc = clean_acc(model, val_loader, 5)
        model.train()
        print(f"[3] step {step + 1}: loss={loss.item():.4f} gradnorm={gnorm:.2f} "
              f"clean(val500)={acc:.2f}%")

print("DIAG_DONE")
