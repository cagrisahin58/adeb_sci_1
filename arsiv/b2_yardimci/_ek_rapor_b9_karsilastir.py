# Salt okur: B9 dondurulmus ciktisi ile sarmalayicinin ikinci cagrisinin ciktisini karsilastirir.
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
K = "results/q1/konsey_b9_c100/"
a = json.load(open(K + "b9_dondurulmus_b2.json", encoding="utf-8"))
b = json.load(open(K + "b9_sarmalayici_b2.json", encoding="utf-8"))


def fark(x, y, yol=""):
    out = []
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y)):
            if k not in x or k not in y:
                out.append(f"{yol}.{k}: yalniz birinde")
            else:
                out += fark(x[k], y[k], f"{yol}.{k}")
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            out.append(f"{yol}: uzunluk {len(x)} != {len(y)}")
        else:
            for i, (p, q) in enumerate(zip(x, y)):
                out += fark(p, q, f"{yol}[{i}]")
    elif x != y:
        out.append(f"{yol}: {x!r} != {y!r}")
    return out


f = fark(a, b)
print("fark sayisi:", len(f))
for s in f:
    print(" ", s)
for ad in ["b9_dondurulmus_b2.json", "b9_sarmalayici_b2.json"]:
    print(ad, hashlib.sha256(open(K + ad, "rb").read()).hexdigest())
