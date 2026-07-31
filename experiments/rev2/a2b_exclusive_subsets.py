"""Yardimci: dislayici-altkume oranlari (mekanizma cumleleri icin kesin sayilar)."""
import json
import os

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")


def load(name):
    with np.load(os.path.join(ROOT, os.environ.get("A2B_IN_DIR", "results/transfer_analysis_run3"), name)) as z:
        return {k: z[k].copy() for k in z.files}


v2c = load("per_sample_ViT_Tiny_AT_to_ResNet18_AT.npz")
c2v = load("per_sample_ResNet18_AT_to_ViT_Tiny_AT.npz")

both = v2c["target_clean_correct"] & v2c["source_clean_correct"]

# ViT->CNN: hedef(CNN) clean-dogru ama kaynak(ViT) clean-yanlis altkume
excl_cnn = v2c["target_clean_correct"] & ~v2c["source_clean_correct"]
# CNN->ViT: hedef(ViT) clean-dogru ama kaynak(CNN) clean-yanlis altkume
excl_vit = c2v["target_clean_correct"] & ~c2v["source_clean_correct"]

out = {
    "n_both_correct": int(both.sum()),
    "ViT_to_CNN": {
        "n_excl_target_only": int(excl_cnn.sum()),
        "fooling_on_excl": round(float(v2c["target_adv_wrong"][excl_cnn].mean() * 100), 1),
        "fooling_on_both": round(float(v2c["target_adv_wrong"][both].mean() * 100), 2),
    },
    "CNN_to_ViT": {
        "n_excl_target_only": int(excl_vit.sum()),
        "fooling_on_excl": round(float(c2v["target_adv_wrong"][excl_vit].mean() * 100), 1),
        "fooling_on_both": round(float(c2v["target_adv_wrong"][both].mean() * 100), 2),
    },
}
print(json.dumps(out, indent=1))
out_path = os.environ.get("A2B_OUT", os.path.join(ROOT, "results/rev2_blockA/a2b_exclusive_subsets.json"))
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    json.dump(out, f, indent=1)
