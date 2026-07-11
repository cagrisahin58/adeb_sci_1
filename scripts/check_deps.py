"""Ortam bagimlilik kontrolu (pipeline oncesi)."""
import importlib

MODULES = ["torch", "torchvision", "timm", "autoattack", "robustbench",
           "sklearn", "pandas", "matplotlib", "click", "tqdm", "numpy"]

missing = []
for m in MODULES:
    try:
        importlib.import_module(m)
        print(f"{m} OK")
    except ImportError as e:
        print(f"{m} MISSING ({e})")
        missing.append(m)

if missing:
    print("\nMISSING:", " ".join(missing))
else:
    print("\nALL_DEPS_OK")
