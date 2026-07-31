"""C1 per-sample npz alanlarini introspekte eder."""
import glob

import numpy as np

for path in sorted(glob.glob("results/c1_seeds/pair*/*.npz")):
    if "chunk" in path:
        continue
    d = np.load(path)
    fields = {k: (v.shape, str(v.dtype)) for k, v in d.items()}
    print(path, fields)
