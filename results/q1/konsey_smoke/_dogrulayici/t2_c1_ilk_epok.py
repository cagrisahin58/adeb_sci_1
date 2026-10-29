"""Tur 2: C1 temiz loglarindan epok basina val (Test Acc) dogrulugu."""
import glob
import json
import re

pat = re.compile(r"Epoch (\d+)/(\d+) - Train Loss: [0-9.]+, Train Acc: [0-9.]+%, Test Acc: ([0-9.]+)%")
out = {}
for f in sorted(glob.glob("logs/C1_clean_vit_200*.log") + glob.glob("logs/C1_clean_resnet_100*.log")):
    txt = open(f, encoding="utf-8", errors="replace").read()
    ep = {}
    for m in pat.finditer(txt):
        ep[int(m.group(1))] = float(m.group(3))
    out[f] = {"n_epok": len(ep), "ep1": ep.get(1), "ep2": ep.get(2), "ep5": ep.get(5),
              "ep30": ep.get(30), "son": ep.get(max(ep)) if ep else None}
print(json.dumps(out, indent=1))
