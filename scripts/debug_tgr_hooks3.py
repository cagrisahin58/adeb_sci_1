"""Hangi kanca/islem gradyani olduruyor? Kademeli test."""
import sys
from pathlib import Path

import torch
import torch.nn as nn

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from experiments.c1_c2_tgr import _tgr_regularize, load  # noqa: E402
from src.data import get_cifar10_loaders  # noqa: E402

device = torch.device("cuda")
src = load("vit_tiny", "models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth", device)
_, loader = get_cifar10_loaders(data_dir="./data", test_batch_size=8)
x, y = next(iter(loader))
x, y = x.to(device), y.to(device)


def make_hook(op):
    def hook(_m, gi, _go):
        if not gi or gi[0] is None or gi[0].dim() != 3:
            return None
        return (op(gi[0]),) + tuple(gi[1:])
    return hook


def run(label, modules, op, unfuse=False):
    handles, saved = [], []
    if unfuse:
        for b in src.model.blocks:
            saved.append(b.attn.fused_attn)
            b.attn.fused_attn = False
    for m in modules:
        handles.append(m.register_full_backward_hook(make_hook(op)))
    xx = x.clone().requires_grad_(True)
    try:
        g = torch.autograd.grad(nn.CrossEntropyLoss()(src(xx), y), xx)[0]
    finally:
        for h in handles:
            h.remove()
        if unfuse:
            for b, f in zip(src.model.blocks, saved):
                b.attn.fused_attn = f
    print(f"{label:44s} |g|={float(g.abs().mean()):.3e} sifir={bool((g == 0).all())}")


B = src.model.blocks
run("kancasiz", [], None) if False else None
run("sadece unfuse, kanca yok", [], lambda t: t, unfuse=True)
run("mlp.fc2 x12, sadece *0.5", [b.mlp.fc2 for b in B], lambda t: t * 0.5)
run("mlp.fc2 x12, tgr", [b.mlp.fc2 for b in B], _tgr_regularize)
run("qkv x12, tgr", [b.attn.qkv for b in B], _tgr_regularize)
run("proj x12, tgr", [b.attn.proj for b in B], _tgr_regularize)
run("qkv+proj+fc2 x12, tgr", [m for b in B for m in (b.attn.qkv, b.attn.proj, b.mlp.fc2)], _tgr_regularize)
run("qkv+proj+fc2 x12, tgr + unfuse", [m for b in B for m in (b.attn.qkv, b.attn.proj, b.mlp.fc2)],
    _tgr_regularize, unfuse=True)
