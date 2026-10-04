"""CIFAR-10 test kumesinin ilk dort goruntusunu 2x2 kucuk resim izgarasi olarak kaydeder
(genel bakis semasi icin gercek ornekler; en yakin komsu buyutme, 32 -> 96 px).
Konteynerde: docker exec -w /workspace adeb_eval python paper/figures/overview/cifar_thumbs.py
"""
import json

import numpy as np
from PIL import Image
from torchvision import datasets

ds = datasets.CIFAR10(root="./data", train=False, download=False)
idx = [0, 1, 2, 3]
S, G = 96, 6  # kenar, bosluk
canvas = Image.new("RGB", (2 * S + G, 2 * S + G), (255, 255, 255))
labels = []
for k, i in enumerate(idx):
    img, y = ds[i]
    labels.append({"index": i, "label": ds.classes[y]})
    big = img.resize((S, S), Image.NEAREST)
    canvas.paste(big, ((k % 2) * (S + G), (k // 2) * (S + G)))
out = "paper/figures/overview/cifar_thumbs.png"
canvas.save(out)
with open("paper/figures/overview/cifar_thumbs.kanit.json", "w", encoding="utf-8") as fh:
    json.dump({"kaynak": "torchvision CIFAR10 test, indices 0-3", "ornekler": labels,
               "buyutme": "nearest, 32->96 px"}, fh, indent=1, ensure_ascii=False)
print(out, labels)
