"""C1 kontrol noktalariyla istatistiksel dogrulama (saldiri-baslatma rastgeleligi).

NOT: Bu analiz yalnizca saldiri baslatma rastgeleligini olcer; egitim tohumu
varyansi artik C1'in 3 bagimsiz kosusuyla ayrica raporlanir. Ilk cift (1001/2001)
uzerinden kosulur; egitim varyansi icin c1_seed_summary.json kullanilir.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import torch  # noqa: E402

import experiments.run_all_analyses_run2 as R  # noqa: E402
from scripts.c1_transfer_rerun import paths  # noqa: E402

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    R.RUN2_MODELS.clear()
    R.RUN2_MODELS.update(paths(1))
    R.run_statistical_validation(device)
