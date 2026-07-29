"""A5: t-SNE iddialarinin nicellestirilmesi (rev2 BLOK A).

Ilk 500 test orneginde her iki modelin penultimate feature'lari icin:
- silhouette skoru (clean ve adversarial, gercek etiketlerle)
- clean-fit kNN (k=5) ile adversarial feature'larin etiket tutarliligi
- sinif-merkezi kayma normu (feature-norm'a gore normalize)
- intra/inter-class mesafe orani (clean ve adversarial)

Iki saldiri tasarimi ayri raporlanir:
  whitebox : her model KENDI PGD-10 saldirisiyla (dogru per-mimari iddia icin)
  transfer : CNN'de uretilen saldiri her iki modele (mevcut t-SNE figurunun tasarimi)

Çalıştırma: docker exec adeb_eval python /workspace/experiments/rev2/a5_tsne_quant.py
Çıktı: results/rev2_blockA/a5_tsne_quant.json
"""
import json
import os
import sys

import numpy as np
import torch

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from sklearn.metrics import silhouette_score  # noqa: E402
from sklearn.neighbors import KNeighborsClassifier  # noqa: E402

from src.attacks.pgd import PGDAttack  # noqa: E402
from src.data import get_cifar10_loaders  # noqa: E402
from src.models import ModelRegistry  # noqa: E402
from src.utils.checkpoint import load_model_weights  # noqa: E402

OUT_DIR = os.path.join(ROOT, "results/rev2_blockA")
os.makedirs(OUT_DIR, exist_ok=True)

SEED = 42
N_SAMPLES = 500

torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)
np.random.seed(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MODELS = {
    "ResNet18_AT": ("resnet18", "models/resnet18/adv/at_run3/resnet18/adv/adversarial_training/best.pth"),
    "ViT_Tiny_AT": ("vit_tiny", "models/vit_tiny/adv/at_run3/vit_tiny/adv/adversarial_training/best.pth"),
}

_, test_loader = get_cifar10_loaders(data_dir="./data", test_batch_size=100)
imgs, lbls = [], []
for x, y in test_loader:
    imgs.append(x)
    lbls.append(y)
    if sum(t.shape[0] for t in imgs) >= N_SAMPLES:
        break
images = torch.cat(imgs)[:N_SAMPLES].to(device)
labels = torch.cat(lbls)[:N_SAMPLES].to(device)
labels_np = labels.cpu().numpy()

models = {}
for name, (mtype, mpath) in MODELS.items():
    m = ModelRegistry.get(mtype)
    load_model_weights(m, mpath, device)
    models[name] = m.to(device).eval()


def get_features(model, x):
    feats = []
    with torch.no_grad():
        for i in range(0, x.shape[0], 100):
            b = x[i : i + 100]
            if hasattr(model, "get_features"):
                f = model.get_features(b)
            elif hasattr(model, "model") and hasattr(model.model, "forward_features"):
                f = model.model.forward_features(b)
            else:
                f = model(b)
            feats.append(f.reshape(f.shape[0], -1).cpu())
    return torch.cat(feats).numpy()


def adv_of(model, x, y):
    atk = PGDAttack(model, eps=8 / 255, alpha=2 / 255, steps=10)
    out = []
    for i in range(0, x.shape[0], 100):
        out.append(atk.attack(x[i : i + 100], y[i : i + 100]).detach())
    return torch.cat(out)


def quantify(clean_f, adv_f, y):
    res = {}
    res["silhouette_clean"] = round(float(silhouette_score(clean_f, y)), 3)
    res["silhouette_adv"] = round(float(silhouette_score(adv_f, y)), 3)
    knn = KNeighborsClassifier(n_neighbors=5).fit(clean_f, y)
    res["knn_clean_fit_adv_consistency"] = round(float((knn.predict(adv_f) == y).mean()), 3)
    res["knn_clean_fit_clean_consistency"] = round(float((knn.predict(clean_f) == y).mean()), 3)
    # sinif-merkezi kaymasi (ortalama feature normuna gore normalize)
    shifts, intra_c, intra_a = [], [], []
    for c in np.unique(y):
        mask = y == c
        mu_c = clean_f[mask].mean(0)
        mu_a = adv_f[mask].mean(0)
        shifts.append(np.linalg.norm(mu_a - mu_c))
        intra_c.append(np.linalg.norm(clean_f[mask] - mu_c, axis=1).mean())
        intra_a.append(np.linalg.norm(adv_f[mask] - adv_f[mask].mean(0), axis=1).mean())
    feat_scale = float(np.linalg.norm(clean_f, axis=1).mean())
    res["centroid_shift_rel"] = round(float(np.mean(shifts)) / feat_scale, 4)
    # intra/inter orani
    mus = np.stack([clean_f[y == c].mean(0) for c in np.unique(y)])
    inter = np.linalg.norm(mus[:, None, :] - mus[None, :, :], axis=-1)
    inter_mean = float(inter[np.triu_indices(len(mus), k=1)].mean())
    res["intra_inter_ratio_clean"] = round(float(np.mean(intra_c)) / inter_mean, 3)
    mus_a = np.stack([adv_f[y == c].mean(0) for c in np.unique(y)])
    inter_a = np.linalg.norm(mus_a[:, None, :] - mus_a[None, :, :], axis=-1)
    inter_a_mean = float(inter_a[np.triu_indices(len(mus_a), k=1)].mean())
    res["intra_inter_ratio_adv"] = round(float(np.mean(intra_a)) / inter_a_mean, 3)
    return res


report = {"seed": SEED, "n_samples": N_SAMPLES, "attack": "PGD-10 eps=8/255 alpha=2/255", "designs": {}}

adv_cnn = adv_of(models["ResNet18_AT"], images, labels)
adv_vit = adv_of(models["ViT_Tiny_AT"], images, labels)

for design, adv_map in [
    ("whitebox", {"ResNet18_AT": adv_cnn, "ViT_Tiny_AT": adv_vit}),
    ("transfer_cnn_crafted", {"ResNet18_AT": adv_cnn, "ViT_Tiny_AT": adv_cnn}),
]:
    report["designs"][design] = {}
    for name, model in models.items():
        cf = get_features(model, images)
        af = get_features(model, adv_map[name])
        report["designs"][design][name] = quantify(cf, af, labels_np)

report["notes"] = [
    "Mevcut fig_tsne_features ViT paneli CNN'de uretilen saldirilarla (transfer_cnn_crafted tasarimi) cizilmistir;",
    "per-mimari iddialar icin dogru tasarim whitebox'tir. Caption/metin buna gore yazilmalidir.",
    "silhouette/kNN gercek etiketlerle; centroid_shift_rel ortalama clean feature normuna gore normalize.",
]

out = os.path.join(OUT_DIR, "a5_tsne_quant.json")
with open(out, "w") as f:
    json.dump(report, f, indent=1)
print(json.dumps(report, indent=1))
print(f"\nkaydedildi: {out}")
