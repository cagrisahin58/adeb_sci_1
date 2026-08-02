"""TGR kancalarinin gradyani nasil etkiledigini olcer."""
import sys
from pathlib import Path

import torch
import torch.nn as nn

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from experiments.c1_c2_tgr import TGRHooks, load  # noqa: E402
from src.data import get_cifar10_loaders  # noqa: E402

device = torch.device("cuda")
src = load("vit_tiny", "models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth", device)
_, loader = get_cifar10_loaders(data_dir="./data", test_batch_size=8)
x, y = next(iter(loader))
x, y = x.to(device), y.to(device)


def grad_of(use_tgr):
    xx = x.clone().requires_grad_(True)
    ctx = TGRHooks(src) if use_tgr else None
    if ctx:
        ctx.__enter__()
    try:
        loss = nn.CrossEntropyLoss()(src(xx), y)
        g = torch.autograd.grad(loss, xx)[0]
    finally:
        if ctx:
            ctx.__exit__()
    return g


g0 = grad_of(False)
g1 = grad_of(True)
print("kancasiz  |g| ortalama:", float(g0.abs().mean()))
print("kancali   |g| ortalama:", float(g1.abs().mean()))
print("tamamen sifir mi:", bool((g1 == 0).all()))
print("kosinus benzerligi:", float(torch.nn.functional.cosine_similarity(
    g0.flatten(), g1.flatten(), dim=0)))
