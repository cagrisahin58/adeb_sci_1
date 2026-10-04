"""Yayilim-temiz fark veri betigi icin artefakt yapilarini yazar (salt okur)."""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open("results/c1_transfer/c1_transfer_summary.json"))
print("c1_transfer keys:", list(d.keys()))
p = d["protocols"]["raw"]
print("raw:", {k: (v if not isinstance(v, dict) else list(v.keys())) for k, v in p.items()})
print("spread:", d["protocol_spread_pp"])
s = json.load(open("results/c1_seeds/c1_seed_summary.json"))
print("seeds keys:", list(s.keys()))
for k in ("runs", "per_run", "pairs", "kosular"):
    if k in s:
        r = s[k]
        print(k, type(r).__name__, (list(r.keys())[:6] if isinstance(r, dict) else json.dumps(r[0])[:300]))
e1 = json.load(open("results/q1/e1_cifar100_summary.json"))
print("e1 keys:", list(e1.keys())[:10])
m = e1.get("mimariler") or {}
for k, v in m.items():
    print(" e1", k, list(v.keys())[:8], json.dumps(v.get("ozet", {}))[:300])
e7 = json.load(open("results/q1/e7_svhn_summary.json"))
for k, v in e7["mimariler"].items():
    print(" e7", k, json.dumps(v.get("ozet", {}))[:300])
e6 = json.load(open("results/q1/cifar10_l2/e6_aa_l2_summary.json"))
print("e6 keys:", list(e6.keys())[:12])
