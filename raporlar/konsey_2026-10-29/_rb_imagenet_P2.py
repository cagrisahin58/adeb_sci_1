"""P2 (dis gecerlilik) icin: RobustBench ImageNet ve CIFAR katalog girdilerini mimari adiyla listeler.
Indirme yapmaz; yalniz model_dicts sozlugunu okur."""
import json
import inspect
import sys

try:
    import robustbench
    from robustbench.model_zoo import model_dicts
    from robustbench.model_zoo.enums import BenchmarkDataset, ThreatModel
except Exception as e:  # pragma: no cover
    print("robustbench import hatasi:", repr(e))
    sys.exit(0)

print("robustbench surumu:", getattr(robustbench, "__version__", "?"))
out = {}
for ds in [BenchmarkDataset.imagenet]:
    for tm in [ThreatModel.Linf, ThreatModel.L2, ThreatModel.corruptions]:
        try:
            d = model_dicts[ds][tm]
        except KeyError:
            continue
        rows = []
        for name, spec in d.items():
            m = spec.get("model")
            try:
                src = inspect.getsource(m).strip() if callable(m) else str(m)
                src = " ".join(src.split())[:160]
            except Exception:
                src = getattr(m, "__name__", type(m).__name__)
            gdrive = spec.get("gdrive_id", "")
            prep = spec.get("preprocessing", "")
            rows.append([name, src, str(prep)])
        out[f"{ds.value}/{tm.value}"] = rows
        print(f"\n### {ds.value} {tm.value}: {len(rows)} model")
        for n, a, p in rows:
            print(f"{n}\t{p}\t{a}")

json.dump(out, open("/workspace/raporlar/konsey_2026-10-29/_rb_imagenet_P2.json", "w"), indent=1)
