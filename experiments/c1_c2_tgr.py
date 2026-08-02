"""C2: TGR (Token Gradient Regularization) ile ViT kaynakli transfer saldirisi.

Yontem: Zhang vd. (CVPR 2023) "Transferable Adversarial Attacks on Vision
Transformers with Token Gradient Regularization" (repo: jpzhang1810/TGR).
Fikir: ViT'in dikkat/QKV/MLP ara gradyanlarinda uc degerli JETONLAR, saldiri
yonunde asiri varyans yaratir ve transfer edilebilirligi dusurur. TGR, geri
yayilim sirasinda her katmanda uc degerli jeton konumlarinin gradyanini
sifirlar; taban saldiri MI-FGSM'dir.

BU BIR UYARLAMADIR (ozgun kod ImageNet/224 icindir):
  * kaynak CIFAR-10 ViT-Tiny sarmalayicimiz (32->224 buyutme model ICINDE)
  * butce makale protokolu: eps=8/255, alpha=2/255, 10 adim (ImageNet
    varsayilanlari DEGIL)
  * timm'in fused attention yolu, dikkat gradyanini gorebilmek icin gecici
    olarak kapatilir

Ayni kosuda kontrol olarak duz MI-FGSM da uretilir; TGR'nin katkisi ayni
butce altinda dogrudan olculur.

Cikti: results/c1_c2/pair{N}/ (per-sample npz + tgr_summary.json)
Kullanim: python experiments/c1_c2_tgr.py --pairs 1 2 3 [--n-samples 10000]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data import get_cifar10_loaders  # noqa: E402
from src.models import ModelRegistry  # noqa: E402
from src.utils.checkpoint import load_model_weights  # noqa: E402

EPS, ALPHA, STEPS, MU = 8 / 255, 2 / 255, 10, 1.0
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


GAMMA = 0.5  # ozgun TGR'deki gradyan olcekleme katsayisi


def _tgr_regularize(grad, gamma=GAMMA):
    """TGR'nin cekirdek islemi (ozgun kodun semantigi).

    grad: (B, N, C). HER (ornek, kanal) icin, jetonlar arasinda gradyani en
    buyuk ve en kucuk olan TEK girdiyi sifirlar. Yani bir jetonun tum kanal
    gradyani degil, kanal basina birer uc deger silinir; boylece sinyal yolu
    korunur, yalniz uc jeton katkilari bastirilir.
    """
    if grad is None or grad.dim() != 3 or grad.shape[1] < 3:
        return grad
    out = grad * gamma
    top = out.argmax(dim=1, keepdim=True)   # (B, 1, C)
    bot = out.argmin(dim=1, keepdim=True)   # (B, 1, C)
    out = out.scatter(1, top, 0.0)
    out = out.scatter(1, bot, 0.0)
    return out


def _tgr_regularize_attn(grad, gamma=GAMMA):
    """Dikkat agirliklarinin gradyani icin TGR (ozgun koddaki attn_tgr).

    grad: (B, H, N, N). Her (ornek, kafa) icin jeton-jeton izgarasindaki en
    buyuk ve en kucuk gradyanli tek konumu sifirlar.
    """
    if grad is None or grad.dim() != 4:
        return grad
    b, h, n, m = grad.shape
    out = (grad * gamma).reshape(b, h, n * m)
    top = out.argmax(dim=2, keepdim=True)
    bot = out.argmin(dim=2, keepdim=True)
    out = out.scatter(2, top, 0.0).scatter(2, bot, 0.0)
    return out.reshape(b, h, n, m)


class TGRHooks:
    """ViT bloklarina geri-yayilim kancalari takar (attn ciktisi, qkv, mlp)."""

    def __init__(self, model):
        self.model = model
        self.handles = []
        self.saved_fused = []

    def __enter__(self):
        blocks = self.model.model.blocks
        for blk in blocks:
            self.saved_fused.append(getattr(blk.attn, "fused_attn", None))
            if hasattr(blk.attn, "fused_attn"):
                blk.attn.fused_attn = False

            # Ozgun TGR uc yere mudahale eder: dikkat agirliklari (attn_tgr),
            # QKV yolu (v_tgr) ve MLP (mlp_tgr). Kancalar modulun GIRDISINE
            # gore gradyani, yani geriye akmaya devam eden tensoru degistirir.
            # NOT: attn.proj BILEREK kancalanmaz; hem ozgun yontemde yok, hem
            # de bu yolda kanca dondurmek gradyan zincirini kopariyor.
            self.handles.append(blk.attn.attn_drop.register_full_backward_hook(self._hook_attn))
            self.handles.append(blk.attn.qkv.register_full_backward_hook(self._hook))
            self.handles.append(blk.mlp.fc2.register_full_backward_hook(self._hook))
        return self

    @staticmethod
    def _hook(_module, grad_input, grad_output):
        if not grad_input:
            return None
        gi = grad_input[0]
        if gi is None or gi.dim() != 3 or gi.shape[1] < 3:
            return None
        return (_tgr_regularize(gi),) + tuple(grad_input[1:])

    @staticmethod
    def _hook_attn(_module, grad_input, grad_output):
        if not grad_input:
            return None
        gi = grad_input[0]
        if gi is None or gi.dim() != 4:
            return None
        return (_tgr_regularize_attn(gi),) + tuple(grad_input[1:])

    def __exit__(self, *exc):
        for h in self.handles:
            h.remove()
        blocks = self.model.model.blocks
        for blk, flag in zip(blocks, self.saved_fused):
            if flag is not None:
                blk.attn.fused_attn = flag
        self.handles.clear()


def mifgsm(model, x, y, use_tgr=False, eps=EPS, alpha=ALPHA, steps=STEPS, mu=MU):
    """MI-FGSM; use_tgr=True ise TGR kancalari acik geri yayilim yapilir."""
    loss_fn = nn.CrossEntropyLoss()
    adv = x.clone().detach()
    momentum = torch.zeros_like(x)
    ctx = TGRHooks(model) if use_tgr else None
    if ctx is not None:
        ctx.__enter__()
    try:
        for _ in range(steps):
            adv.requires_grad_(True)
            loss = loss_fn(model(adv), y)
            grad = torch.autograd.grad(loss, adv)[0]
            grad = grad / grad.abs().flatten(1).mean(1).view(-1, 1, 1, 1).clamp_min(1e-12)
            momentum = mu * momentum + grad
            adv = adv.detach() + alpha * momentum.sign()
            adv = torch.min(torch.max(adv, x - eps), x + eps).clamp(0, 1).detach()
    finally:
        if ctx is not None:
            ctx.__exit__()
    return adv


def boot_ci(mask, n_boot=10000, seed=42):
    rng = np.random.default_rng(seed)
    v = np.asarray(mask, dtype=float)
    if v.size == 0:
        return [float("nan"), float("nan")]
    b = np.array([v[rng.integers(0, v.size, v.size)].mean() for _ in range(n_boot)])
    return [round(float(np.percentile(b, 2.5) * 100), 2), round(float(np.percentile(b, 97.5) * 100), 2)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", type=int, nargs="+", default=[1, 2, 3])
    ap.add_argument("--n-samples", type=int, default=10000)
    ap.add_argument("--batch", type=int, default=50)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    for pair in args.pairs:
        rs, vs = PAIRS[pair]
        out_dir = Path(f"results/c1_c2/pair{pair}")
        out_dir.mkdir(parents=True, exist_ok=True)
        if (out_dir / "tgr_summary.json").exists():
            print(f"cift {pair}: artefakt mevcut, atlandi")
            continue
        set_seed(args.seed)

        src = load("vit_tiny", f"models/c1/vit_tiny_s{vs}/vit_tiny/adv/adversarial_training/best.pth", device)
        tgt = load("resnet18", f"models/c1/resnet18_s{rs}/resnet18/adv/adversarial_training/best.pth", device)
        _, loader = get_cifar10_loaders(data_dir="./data", test_batch_size=args.batch)

        acc = {k: [] for k in ("src_clean_ok", "tgt_clean_ok",
                               "tgr_src_wrong", "tgr_tgt_wrong",
                               "mi_src_wrong", "mi_tgt_wrong")}
        seen = 0
        for images, labels in loader:
            if seen >= args.n_samples:
                break
            if seen + labels.size(0) > args.n_samples:
                k = args.n_samples - seen
                images, labels = images[:k], labels[:k]
            images, labels = images.to(device), labels.to(device)

            adv_tgr = mifgsm(src, images, labels, use_tgr=True)
            adv_mi = mifgsm(src, images, labels, use_tgr=False)
            with torch.no_grad():
                acc["src_clean_ok"].append((src(images).argmax(1) == labels).cpu().numpy())
                acc["tgt_clean_ok"].append((tgt(images).argmax(1) == labels).cpu().numpy())
                acc["tgr_src_wrong"].append((src(adv_tgr).argmax(1) != labels).cpu().numpy())
                acc["tgr_tgt_wrong"].append((tgt(adv_tgr).argmax(1) != labels).cpu().numpy())
                acc["mi_src_wrong"].append((src(adv_mi).argmax(1) != labels).cpu().numpy())
                acc["mi_tgt_wrong"].append((tgt(adv_mi).argmax(1) != labels).cpu().numpy())
            seen += labels.size(0)
            if seen % 1000 == 0:
                print(f"  cift {pair}: {seen}/{args.n_samples}", flush=True)

        A = {k: np.concatenate(v) for k, v in acc.items()}
        np.savez(out_dir / "per_sample_tgr.npz", **A)

        both = A["src_clean_ok"] & A["tgt_clean_ok"]
        res = {"pair": pair, "seed": args.seed, "n_samples": int(seen),
               "attack_budget": {"eps": EPS, "alpha": ALPHA, "steps": STEPS, "momentum": MU},
               "source": "ViT_Tiny_AT", "target": "ResNet18_AT",
               "note": "TGR uyarlamasi; taban saldiri MI-FGSM. Kontrol: ayni butcede duz MI-FGSM."}
        for tag in ("tgr", "mi"):
            res[tag] = {
                "whitebox_source_fooling_raw": round(float(100 * A[f"{tag}_src_wrong"].mean()), 2),
                "transfer_raw": round(float(100 * A[f"{tag}_tgt_wrong"].mean()), 2),
                "transfer_target_correct": round(float(100 * A[f"{tag}_tgt_wrong"][A["tgt_clean_ok"]].mean()), 2),
                "transfer_target_correct_ci95": boot_ci(A[f"{tag}_tgt_wrong"][A["tgt_clean_ok"]]),
                "transfer_both_correct": round(float(100 * A[f"{tag}_tgt_wrong"][both].mean()), 2),
                "transfer_both_correct_ci95": boot_ci(A[f"{tag}_tgt_wrong"][both]),
                "n_target_correct": int(A["tgt_clean_ok"].sum()),
                "n_both_correct": int(both.sum()),
            }
        res["tgr_minus_mi_target_correct"] = round(
            res["tgr"]["transfer_target_correct"] - res["mi"]["transfer_target_correct"], 2)
        res["tgr_minus_mi_both_correct"] = round(
            res["tgr"]["transfer_both_correct"] - res["mi"]["transfer_both_correct"], 2)

        # Esli McNemar (ayni ornekler, iki saldiri): TGR mi MI mi daha cok deviriyor?
        t, m = A["tgr_tgt_wrong"][both], A["mi_tgt_wrong"][both]
        b_only, c_only = int((t & ~m).sum()), int((m & ~t).sum())
        try:
            from scipy.stats import binomtest

            p = float(binomtest(min(b_only, c_only), b_only + c_only, 0.5).pvalue) if (b_only + c_only) else 1.0
        except Exception:
            p = float("nan")
        res["mcnemar_both_correct"] = {"tgr_only": b_only, "mi_only": c_only, "p_exact": p}

        with open(out_dir / "tgr_summary.json", "w") as f:
            json.dump(res, f, indent=2)
        print(json.dumps({k: res[k] for k in ("tgr", "mi", "tgr_minus_mi_target_correct",
                                              "tgr_minus_mi_both_correct", "mcnemar_both_correct")}, indent=1))
        print(f"cift {pair} kaydedildi: {out_dir}/tgr_summary.json")

        del src, tgt
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
