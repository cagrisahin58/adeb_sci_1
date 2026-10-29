"""RobustBench model_dicts listesini okur; indirme yapmaz. Konsey durum dosyasi icin."""
import json, os, sys
try:
    import robustbench
    from robustbench.model_zoo import model_dicts
    from robustbench.model_zoo.enums import BenchmarkDataset, ThreatModel
except Exception as e:
    print("robustbench import hatasi:", repr(e)); sys.exit(0)
print("robustbench surumu:", getattr(robustbench, "__version__", "?"))
out = {}
for ds in [BenchmarkDataset.cifar_10, BenchmarkDataset.cifar_100]:
    for tm in [ThreatModel.Linf, ThreatModel.L2]:
        try:
            d = model_dicts[ds][tm]
        except KeyError:
            continue
        rows = []
        for name, spec in d.items():
            m = spec.get("model")
            try:
                if callable(m) and not isinstance(m, type):
                    arch = getattr(m, "__name__", None) or type(m).__name__
                    if arch == "<lambda>":
                        import inspect
                        try:
                            arch = inspect.getsource(m).strip().split("lambda:")[-1].strip()[:90]
                        except Exception:
                            arch = "lambda"
                else:
                    arch = getattr(m, "__name__", str(m))
            except Exception as e:
                arch = "?"
            rows.append((name, arch))
        out[f"{ds.value}/{tm.value}"] = rows
        print(f"\n### {ds.value} {tm.value}: {len(rows)} model")
        for n, a in rows:
            print(f"{n}\t{a}")
# yerel onbellek
for root in ["/workspace/models", os.path.expanduser("~/.cache"), "/root/.cache", "/workspace/.cache"]:
    if os.path.isdir(root):
        for dp, dn, fn in os.walk(root):
            for f in fn:
                if f.endswith((".pt", ".pth")) and ("Debenedetti" in f or "XCiT" in f or "xcit" in f):
                    p = os.path.join(dp, f)
                    print("YEREL:", p, os.path.getsize(p))
json.dump(out, open("/workspace/raporlar/konsey_2026-10-29/_rb_liste.json", "w"), indent=1)
