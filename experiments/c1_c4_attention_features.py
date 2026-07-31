"""C4: n=1000 oznitelik kaymasi + attention analizi (C1 kontrol noktalari).

Genisletmeler (rev2 plani C4):
  * n=1000 ornek (onceki: 100)
  * ViT oznitelik agregasyonunun iki varyanti: CLS-only ve token-mean
  * blok cikisi (block output) kontrolu, MLP alt-blok ciktisinin yaninda
  * attention entropi + CLS attention yer degistirmesi, katman basina %95 GA
  * saldirida basarili/basarisiz ornekler ayri raporlanir
  * ResNet katman profili ayni n ile

Cikti: results/c1_c4/pair{N}/c4_summary.json (+ per-layer CSV)
Kullanim: python experiments/c1_c4_attention_features.py --pairs 1 2 3 [--n-samples 1000]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.attacks import PGDAttack  # noqa: E402
from src.data import get_cifar10_loaders  # noqa: E402
from src.models import ModelRegistry  # noqa: E402
from src.utils.checkpoint import load_model_weights  # noqa: E402

EPS, ALPHA, STEPS = 8 / 255, 2 / 255, 10
PAIRS = {1: (1001, 2001), 2: (1002, 2002), 3: (1003, 2003)}


def set_seed(seed):
    import random

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def load(model_type, path, device):
    m = ModelRegistry.get(model_type)
    load_model_weights(m, path, device)
    return m.to(device).eval()


def boot_ci(x, n_boot=2000, seed=42):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float)
    if x.size == 0:
        return [float("nan"), float("nan")]
    means = np.array([x[rng.integers(0, x.size, x.size)].mean() for _ in range(n_boot)])
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def cosine_rows(a, b):
    """Ornek bazina kosinus benzerligi (a,b: (B, D))."""
    return F.cosine_similarity(a, b, dim=1).cpu().numpy()


def collect_features(model, images, hooks_spec):
    """hooks_spec: {ad: modul} -> {ad: (B, ...) tensor}"""
    store = {}
    handles = []
    for name, module in hooks_spec.items():
        def mk(n):
            def hook(_m, _i, out):
                store[n] = out.detach()
            return hook
        handles.append(module.register_forward_hook(mk(name)))
    with torch.no_grad():
        logits = model(images)
    for h in handles:
        h.remove()
    return store, logits


def vit_modules(model):
    """timm ViT sarmalayicisindan blok, MLP alt-blok modullerini toplar."""
    blocks = model.model.blocks
    spec = {}
    for i, blk in enumerate(blocks):
        spec[f"block{i}"] = blk
        spec[f"block{i}.mlp"] = blk.mlp
    return spec


def resnet_modules(model):
    spec = {}
    net = model.model if hasattr(model, "model") else model
    for stage in ("layer1", "layer2", "layer3", "layer4"):
        st = getattr(net, stage, None)
        if st is None:
            continue
        for j, blk in enumerate(st):
            spec[f"{stage}.{j}"] = blk
    return spec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", type=int, nargs="+", default=[1, 2, 3])
    ap.add_argument("--n-samples", type=int, default=1000)
    ap.add_argument("--batch", type=int, default=50)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    for pair in args.pairs:
        rs, vs = PAIRS[pair]
        out_dir = Path(f"results/c1_c4/pair{pair}")
        out_dir.mkdir(parents=True, exist_ok=True)
        if (out_dir / "c4_summary.json").exists():
            print(f"cift {pair}: artefakt mevcut, atlandi")
            continue
        set_seed(args.seed)

        vit = load("vit_tiny", f"models/c1/vit_tiny_s{vs}/vit_tiny/adv/adversarial_training/best.pth", device)
        rnet = load("resnet18", f"models/c1/resnet18_s{rs}/resnet18/adv/adversarial_training/best.pth", device)
        _, loader = get_cifar10_loaders(data_dir="./data", test_batch_size=args.batch)

        acc = {
            "vit": {"cos_cls": {}, "cos_mean": {}, "cos_block": {}, "norm": {}, "attn_entropy_clean": [],
                    "attn_entropy_adv": [], "attn_disp": [], "success": []},
            "resnet": {"cos": {}, "norm": {}, "success": []},
        }
        seen = 0
        for images, labels in loader:
            if seen >= args.n_samples:
                break
            if seen + labels.size(0) > args.n_samples:
                k = args.n_samples - seen
                images, labels = images[:k], labels[:k]
            images, labels = images.to(device), labels.to(device)

            for tag, model, mod_fn in (("vit", vit, vit_modules), ("resnet", rnet, resnet_modules)):
                atk = PGDAttack(model, eps=EPS, alpha=ALPHA, steps=STEPS)
                adv = atk(images, labels)
                spec = mod_fn(model)
                fc, logit_c = collect_features(model, images, spec)
                fa, logit_a = collect_features(model, adv, spec)
                ok_clean = (logit_c.argmax(1) == labels)
                flipped = ok_clean & (logit_a.argmax(1) != labels)
                acc[tag]["success"].append(flipped.cpu().numpy())

                for name in spec:
                    a, b = fc[name], fa[name]
                    if a.dim() == 3:  # (B, tokens, D) - ViT
                        flat_a, flat_b = a.flatten(1), b.flatten(1)
                        key = "cos_block" if ".mlp" not in name else "cos_cls"
                        # CLS ve token-ortalama varyantlari yalniz MLP alt-bloklari icin
                        if ".mlp" in name:
                            acc[tag]["cos_cls"].setdefault(name, []).append(cosine_rows(a[:, 0], b[:, 0]))
                            acc[tag]["cos_mean"].setdefault(name, []).append(
                                cosine_rows(a[:, 1:].mean(1), b[:, 1:].mean(1)))
                            acc[tag].setdefault("cos_flat", {}).setdefault(name, []).append(cosine_rows(flat_a, flat_b))
                        else:
                            acc[tag]["cos_block"].setdefault(name, []).append(cosine_rows(flat_a, flat_b))
                        acc[tag]["norm"].setdefault(name, []).append(
                            ((flat_b.norm(dim=1) - flat_a.norm(dim=1)) / flat_a.norm(dim=1) * 100).cpu().numpy())
                    else:  # (B, C, H, W) - CNN
                        flat_a, flat_b = a.flatten(1), b.flatten(1)
                        acc[tag]["cos"].setdefault(name, []).append(cosine_rows(flat_a, flat_b))
                        acc[tag]["norm"].setdefault(name, []).append(
                            ((flat_b.norm(dim=1) - flat_a.norm(dim=1)) / flat_a.norm(dim=1) * 100).cpu().numpy())

                if tag == "vit" and hasattr(model, "get_attention_maps"):
                    with torch.no_grad():
                        ca = model.get_attention_maps(images)
                        aa = model.get_attention_maps(adv)
                    if isinstance(ca, dict):
                        acc["vit"]["attn_entropy_clean"].append(ca["entropy"].cpu().numpy())
                        acc["vit"]["attn_entropy_adv"].append(aa["entropy"].cpu().numpy())
                        cm, am = ca["cls_maps"], aa["cls_maps"]  # (B, L, 14, 14)
                        d = (am - cm).flatten(2).abs().sum(-1) / 2.0  # katman basina toplam varyasyon
                        acc["vit"]["attn_disp"].append(d.cpu().numpy())
                del atk, adv, fc, fa
                torch.cuda.empty_cache()
            seen += labels.size(0)
            print(f"  cift {pair}: {seen}/{args.n_samples}", flush=True)

        def summarize(vals):
            v = np.concatenate(vals)
            return {"mean": float(v.mean()), "std": float(v.std(ddof=1)), "ci95": boot_ci(v), "n": int(v.size)}

        vit_success = np.concatenate(acc["vit"]["success"])
        res_success = np.concatenate(acc["resnet"]["success"])
        summary = {
            "pair": pair, "n_samples": seen, "seed": args.seed,
            "vit": {
                "cos_cls": {k: summarize(v) for k, v in acc["vit"]["cos_cls"].items()},
                "cos_token_mean": {k: summarize(v) for k, v in acc["vit"]["cos_mean"].items()},
                "cos_flat_all_tokens": {k: summarize(v) for k, v in acc["vit"].get("cos_flat", {}).items()},
                "cos_block_output": {k: summarize(v) for k, v in acc["vit"]["cos_block"].items()},
                "norm_change_pct": {k: summarize(v) for k, v in acc["vit"]["norm"].items()},
                "attack_success_rate": float(vit_success.mean() * 100),
            },
            "resnet": {
                "cos": {k: summarize(v) for k, v in acc["resnet"]["cos"].items()},
                "norm_change_pct": {k: summarize(v) for k, v in acc["resnet"]["norm"].items()},
                "attack_success_rate": float(res_success.mean() * 100),
            },
        }
        if acc["vit"]["attn_entropy_clean"]:
            ec = np.stack(acc["vit"]["attn_entropy_clean"])  # (batches, L)
            ea = np.stack(acc["vit"]["attn_entropy_adv"])
            disp = np.concatenate(acc["vit"]["attn_disp"])  # (N, L)
            summary["vit"]["attention"] = {
                "entropy_clean_mean": ec.mean(0).tolist(),
                "entropy_adv_mean": ea.mean(0).tolist(),
                "entropy_delta_mean": (ea - ec).mean(0).tolist(),
                "displacement_mean": disp.mean(0).tolist(),
                "displacement_ci95": [boot_ci(disp[:, l]) for l in range(disp.shape[1])],
                "n_batches": int(ec.shape[0]),
            }

        # Saldirida basarili / basarisiz ayrimi (MLP alt-bloklari, tum-token duzlestirme)
        split = {}
        for name, chunks in acc["vit"].get("cos_flat", {}).items():
            v = np.concatenate(chunks)
            split[name] = {
                "flipped": {"mean": float(v[vit_success].mean()), "n": int(vit_success.sum())} if vit_success.any() else None,
                "not_flipped": {"mean": float(v[~vit_success].mean()), "n": int((~vit_success).sum())},
            }
        summary["vit"]["cos_by_attack_outcome"] = split
        split_r = {}
        for name, chunks in acc["resnet"]["cos"].items():
            v = np.concatenate(chunks)
            split_r[name] = {
                "flipped": {"mean": float(v[res_success].mean()), "n": int(res_success.sum())} if res_success.any() else None,
                "not_flipped": {"mean": float(v[~res_success].mean()), "n": int((~res_success).sum())},
            }
        summary["resnet"]["cos_by_attack_outcome"] = split_r

        with open(out_dir / "c4_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        print(f"cift {pair} kaydedildi: {out_dir}/c4_summary.json")


if __name__ == "__main__":
    main()
