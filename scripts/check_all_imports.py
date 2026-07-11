"""Projedeki tum ucuncu-parti importlari tarayip eksikleri raporlar."""
import ast
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
STDLIB = set(sys.stdlib_module_names)
LOCAL = {"src", "cli", "experiments", "generate_figures", "generate_from_experiments",
         "generate_advanced_figures", "paper", "scripts", "tests"}

mods = set()
for pattern in ["src/**/*.py", "cli/**/*.py", "experiments/*.py", "paper/figures/*.py"]:
    for f in ROOT.glob(pattern):
        try:
            tree = ast.parse(f.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            print(f"SYNTAX ERROR: {f}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    mods.add(a.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                mods.add(node.module.split(".")[0])

third_party = sorted(m for m in mods if m not in STDLIB and m not in LOCAL)
missing = [m for m in third_party if importlib.util.find_spec(m) is None]

print("Third-party:", " ".join(third_party))
if missing:
    print("MISSING:", " ".join(missing))
else:
    print("ALL_IMPORTS_OK")
