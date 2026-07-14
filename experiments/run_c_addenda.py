#!/usr/bin/env python3
"""2026-07-10 paneli C-maddeleri (kullanici onayli GPU kosulari).

C20  ResNet-18 AT feature degradation: 8 residual blogun ciktilarinda ViT
     analiziyle ayni 3 metrik (L2 mesafe, cosine, norm degisimi); PGD-10,
     n=100, batch 20, seed 42.  -> results/c_addenda/resnet_feature_degradation.json
C21  Clean-egitimli ResNet-18 ve ViT-Tiny'de gradyan istatistikleri
     (alignment + olcek-bagimsiz sparsity); n=500, batch 50, seed 42.
     "AT alignment'i bastiriyor" hipotezinin dogrudan testi.
     -> results/c_addenda/clean_gradient_stats.json
C22  MI-FGSM (Dong et al. 2018: momentum mu=1.0, 10 adim, alpha=eps/10) ile
     kosullu transfer matrisi (AT run3 modelleri, n=10000, seed 42):
     simetrinin saldiri-dayanikliligi.  -> results/c_addenda/mifgsm_transfer.json

Idempotent: hedef artefakt varsa ilgili bolum atlanir (kesinti-guvenli).
"""

import gc
import json
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import ModelRegistry
from src.data import get_cifar10_loaders
from src.attacks import PGDAttack
from src.utils.checkpoint import load_model_weights
from src.analysis.gradient_analysis import GradientAnalyzer

ROOT = Path(__file__).parent.parent
OUT = ROOT / "results" / "c_addenda"
OUT.mkdir(parents=True, exist_ok=True)

EPS = 8 / 255
SEED = 42

AT_MODELS = {
    "ResNet18_AT": ("resnet18", "models/resnet18/adv/at_run3/resnet18/adv/adversarial_training/best.pth"),
    "ViT_Tiny_AT": ("vit_tiny", "models/vit_tiny/adv/at_run3/vit_tiny/adv/adversarial_training/best.pth"),
}
CLEAN_MODELS = {
    "ResNet18_clean": ("resnet18", "models/resnet18/clean/best.pth"),
    "ViT_Tiny_clean": ("vit_tiny", "models/vit_tiny/clean/best.pth"),
}


def set_seed(seed):
    import random
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def clear_gpu():
    gc.collect()
    torch.cuda.empty_cache()


def load_model(mtype, mpath, device):
    m = ModelRegistry.get(mtype)
    load_model_weights(m, str(ROOT / mpath), device)
    return m.to(device).eval()


# ---------------------------------------------------------------------------
# C20: ResNet-18 AT residual-blok feature degradation
# ---------------------------------------------------------------------------
def run_c20(device):
    out_file = OUT / "resnet_feature_degradation.json"
    if out_file.exists():
        print("[C20] artefakt mevcut, atlandi")
        return
    print("[C20] ResNet-18 AT feature degradation (8 residual blok, n=100)")
    set_seed(SEED)

    model = load_model(*AT_MODELS["ResNet18_AT"], device)
    attack = PGDAttack(model, eps=EPS, alpha=2 / 255, steps=10)
    _, loader = get_cifar10_loaders(data_dir=str(ROOT / "data"), test_batch_size=20)

    # torchvision resnet18 sarmali: model.model.layer{1..4}[{0,1}] = 8 BasicBlock
    inner = model.model
    targets = []
    for li, layer in enumerate([inner.layer1, inner.layer2, inner.layer3, inner.layer4], start=1):
        for bi, block in enumerate(layer):
            targets.append((f"layer{li}.{bi}", block))

    n_samples, total = 100, 0
    batch_results = []
    for images, labels in loader:
        if total >= n_samples:
            break
        if total + labels.size(0) > n_samples:
            keep = n_samples - total
            images, labels = images[:keep], labels[:keep]
        images, labels = images.to(device), labels.to(device)
        adv = attack(images, labels)

        feats = {"clean": {}, "adv": {}}
        for tag, batch_x in [("clean", images), ("adv", adv)]:
            store, hooks = feats[tag], []

            def mk(name, store=store):
                def hook(mod, inp, outp):
                    store[name] = outp.detach()
                return hook

            for name, mod in targets:
                hooks.append(mod.register_forward_hook(mk(name)))
            with torch.no_grad():
                model(batch_x)
            for h in hooks:
                h.remove()

        res = {}
        for name, _ in targets:
            c = feats["clean"][name].flatten(1)
            a = feats["adv"][name].flatten(1)
            res[name] = {
                "l2_distance": torch.norm(c - a, dim=1).mean().item(),
                "cosine_similarity": torch.nn.functional.cosine_similarity(c, a, dim=1).mean().item(),
                "norm_change_pct": (100 * (a.norm(dim=1) - c.norm(dim=1)) / c.norm(dim=1)).mean().item(),
            }
        batch_results.append(res)
        total += labels.size(0)
        print(f"  {total}/{n_samples}")

    agg = []
    for name, _ in targets:
        vals = {k: [b[name][k] for b in batch_results] for k in batch_results[0][name]}
        agg.append({"layer": name,
                    **{k: float(np.mean(v)) for k, v in vals.items()},
                    **{f"{k}_std": float(np.std(v)) for k, v in vals.items()}})
        print(f"  {name}: cos={agg[-1]['cosine_similarity']:.4f} "
              f"L2={agg[-1]['l2_distance']:.2f} norm={agg[-1]['norm_change_pct']:+.2f}%")

    json.dump({"model": "ResNet18_AT (run3)", "n_samples": n_samples, "seed": SEED,
               "attack": "PGD-10 eps=8/255", "hook_target": "BasicBlock outputs",
               "model_path": AT_MODELS["ResNet18_AT"][1],
               "feature_analysis": agg}, open(out_file, "w"), indent=2)
    del model
    clear_gpu()
    print(f"[C20] kaydedildi: {out_file}")


# ---------------------------------------------------------------------------
# C21: clean modellerde gradyan istatistikleri
# ---------------------------------------------------------------------------
def run_c21(device):
    out_file = OUT / "clean_gradient_stats.json"
    if out_file.exists():
        print("[C21] artefakt mevcut, atlandi")
        return
    print("[C21] Clean modellerde gradient alignment/sparsity (n=500)")
    set_seed(SEED)
    _, loader = get_cifar10_loaders(data_dir=str(ROOT / "data"), test_batch_size=50)

    stats_out = {}
    for name, (mtype, mpath) in CLEAN_MODELS.items():
        print(f"  {name}")
        clear_gpu()
        model = load_model(mtype, mpath, device)
        an = GradientAnalyzer(model, device)
        acc = {"hoyer": [], "gini": [], "rel": [], "align": [], "l2": []}
        total = 0
        for images, labels in loader:
            if total >= 500:
                break
            if total + labels.size(0) > 500:
                keep = 500 - total
                images, labels = images[:keep], labels[:keep]
            images, labels = images.to(device), labels.to(device)
            s = an.compute_gradient_statistics(images, labels)
            acc["hoyer"].append(s["sparsity_hoyer"])
            acc["gini"].append(s["sparsity_gini"])
            acc["rel"].append(s["sparsity_rel_threshold"])
            acc["l2"].append(s["l2_norm_mean"])
            acc["align"].append(an.compute_gradient_alignment(images, labels))
            total += labels.size(0)
        stats_out[name] = {
            "model_path": mpath, "n_samples": total,
            **{f"{k}_mean": float(np.mean(v)) for k, v in acc.items()},
            **{f"{k}_std": float(np.std(v)) for k, v in acc.items()},
        }
        print(f"    align={stats_out[name]['align_mean']:.4f}±{stats_out[name]['align_std']:.4f} "
              f"hoyer={stats_out[name]['hoyer_mean']:.4f}")
        del model, an
        clear_gpu()

    json.dump({"seed": SEED, "note": "clean-trained counterparts; per-sample loss gradients",
               "statistics": stats_out}, open(out_file, "w"), indent=2)
    print(f"[C21] kaydedildi: {out_file}")


# ---------------------------------------------------------------------------
# C22: MI-FGSM ile kosullu transfer
# ---------------------------------------------------------------------------
def mifgsm(model, images, labels, eps=EPS, steps=10, mu=1.0):
    """MI-FGSM (Dong et al., CVPR 2018): momentumlu iteratif FGSM.

    alpha = eps/steps; g_{t+1} = mu*g_t + grad/||grad||_1; x += alpha*sign(g).
    """
    loss_fn = nn.CrossEntropyLoss(reduction="sum")
    alpha = eps / steps
    x0 = images.detach()
    x = x0.clone()
    g = torch.zeros_like(x)
    for _ in range(steps):
        x = x.detach().requires_grad_(True)
        loss = loss_fn(model(x), labels)
        grad = torch.autograd.grad(loss, x)[0]
        grad = grad / (grad.abs().flatten(1).sum(dim=1).view(-1, 1, 1, 1) + 1e-12)
        g = mu * g + grad
        x = x.detach() + alpha * g.sign()
        x = x0 + torch.clamp(x - x0, -eps, eps)
        x = torch.clamp(x, 0, 1)
    return x.detach()


def run_c22(device, n_samples=10000):
    out_file = OUT / "mifgsm_transfer.json"
    if out_file.exists():
        print("[C22] artefakt mevcut, atlandi")
        return
    print(f"[C22] MI-FGSM kosullu transfer (n={n_samples})")
    set_seed(SEED)
    _, loader = get_cifar10_loaders(data_dir=str(ROOT / "data"), test_batch_size=50)

    cfg = list(AT_MODELS.items())
    results = []
    for i, (sname, (stype, spath)) in enumerate(cfg):
        clear_gpu()
        smodel = load_model(stype, spath, device)
        for j, (tname, (ttype, tpath)) in enumerate(cfg):
            if i == j:
                continue  # yalniz capraz hucreler (simetri testi)
            tmodel = load_model(ttype, tpath, device)
            tgt_clean_ok, tgt_adv_wrong = [], []
            total = 0
            for images, labels in loader:
                if total >= n_samples:
                    break
                if total + labels.size(0) > n_samples:
                    keep = n_samples - total
                    images, labels = images[:keep], labels[:keep]
                images, labels = images.to(device), labels.to(device)
                adv = mifgsm(smodel, images, labels)
                with torch.no_grad():
                    tgt_clean_ok.append((tmodel(images).argmax(1) == labels).cpu().numpy())
                    tgt_adv_wrong.append((tmodel(adv).argmax(1) != labels).cpu().numpy())
                total += labels.size(0)
                if total % 2000 == 0:
                    print(f"  {sname}->{tname}: {total}/{n_samples}")
            ok = np.concatenate(tgt_clean_ok)
            wrong = np.concatenate(tgt_adv_wrong)
            cond = wrong[ok]
            rng = np.random.default_rng(SEED)
            boot = np.array([cond[rng.integers(0, len(cond), len(cond))].mean()
                             for _ in range(10000)])
            results.append({
                "source": sname, "target": tname,
                "conditioned_fooling_rate": float(100 * cond.mean()),
                "ci95": [float(100 * np.percentile(boot, 2.5)),
                         float(100 * np.percentile(boot, 97.5))],
                "n_conditioned": int(ok.sum()), "n": int(total),
            })
            print(f"  {sname}->{tname}: cond={results[-1]['conditioned_fooling_rate']:.2f}% "
                  f"CI={results[-1]['ci95']}")
            del tmodel
            clear_gpu()
        del smodel
        clear_gpu()

    json.dump({"attack": "MI-FGSM (mu=1.0, steps=10, alpha=eps/10)", "eps": EPS,
               "seed": SEED, "model_paths": {k: v[1] for k, v in AT_MODELS.items()},
               "results": results}, open(out_file, "w"), indent=2)
    print(f"[C22] kaydedildi: {out_file}")


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    run_c21(device)   # en ucuz
    run_c20(device)
    run_c22(device)   # en uzun
    print("C_ADDENDA_COMPLETE")
