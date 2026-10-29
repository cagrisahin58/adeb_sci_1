"""Tur 2 sinamasi: 'python -m cli.main train ...' cagrisinin yerine gecen sahte egitici.

Gercek egitim yapmaz; kuyrugun bekledigi dosyalari (best.pth, last.pth gecmisi,
TRAINING_COMPLETE) yazar ve cagri sirasini SAHTE_SIRA dosyasina ekler.
Ilk epok val dogruluklari SAHTE_EP1 JSON dosyasindan hucre adina gore okunur.
"""
import json
import os
import sys
from pathlib import Path

import torch

argv = sys.argv[1:]          # -m cli.main train clean|adversarial ...
mode = argv[3]
opts = {}
i = 4
while i < len(argv):
    if argv[i].startswith("-") and i + 1 < len(argv) and not argv[i + 1].startswith("-"):
        opts[argv[i]] = argv[i + 1]
        i += 2
    else:
        opts[argv[i]] = True
        i += 1
out = Path(opts["-o"])
mtype = opts["-m"]
takma = out.name
hucre = takma.rsplit("_s", 1)[0]
ep1 = json.loads(Path(os.environ["SAHTE_EP1"]).read_text())
lr = opts.get("--lr")
with open(os.environ["SAHTE_SIRA"], "a") as f:
    f.write(f"{mode} {takma} lr={lr}\n")

if mode == "clean":
    d = out / mtype / "clean"
    d.mkdir(parents=True, exist_ok=True)
    v1 = float(ep1[hucre])
    torch.save({"model_state_dict": {}, "epoch": 29, "accuracy": 95.0}, d / "best.pth")
    torch.save({"model_state_dict": {}, "epoch": 29, "accuracy": 95.0,
                "history": {"test_acc": [v1] + [95.0] * 29}}, d / "last.pth")
    (d / "TRAINING_COMPLETE").write_text("epochs_run=30\nbest_acc=95.0000\n")
else:
    d = out / mtype / "adv" / "adversarial_training"
    d.mkdir(parents=True, exist_ok=True)
    torch.save({"model_state_dict": {}, "epoch": 40, "accuracy": 45.0}, d / "best.pth")
    torch.save({"model_state_dict": {}, "epoch": 60, "accuracy": 44.0,
                "history": {"adv_acc": [30.0] * 61}}, d / "last.pth")
    (d / "TRAINING_COMPLETE").write_text("epochs_run=61\nearly_stopped=True\nstopped_at_cap=False\n")
