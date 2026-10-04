"""RobustBench havuzundaki modellerin kaynak makaleleri icin bib girdileri (2026-10-04).
Dogrulama: arXiv ozet sayfalari (baslik + yazar listesi) ana oturumca cekildi:
  1905.13736 Carmon, Raghunathan, Schmidt, Liang, Duchi, "Unlabeled Data Improves Adversarial Robustness" (NeurIPS 2019)
  2001.03994 Wong, Rice, Kolter, "Fast is better than free: Revisiting adversarial training" (ICLR 2020)
Engstrom ve ark. 'robustness' kutuphanesi: GitHub deposu (RobustBench'in Engstrom2019Robustness kaydinin kaynagi).
Kullanim: python3 arsiv/b2_yardimci/_bib_havuz_ekle.py  (depo kokunden); tekrar calistirmaya karsi guvenli.
"""
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path(__file__).resolve().parents[2] / "paper/manuscript/references.bib"
t = io.open(P, encoding="utf-8").read()

GIRDILER = {
    "carmon2019unlabeled": """@inproceedings{carmon2019unlabeled,
  author       = {Carmon, Yair and Raghunathan, Aditi and Schmidt, Ludwig and Liang, Percy and Duchi, John C.},
  title        = {Unlabeled Data Improves Adversarial Robustness},
  booktitle    = {Advances in Neural Information Processing Systems ({NeurIPS})},
  volume       = {32},
  year         = {2019},
  eprint       = {1905.13736},
  archiveprefix = {arXiv}
}
""",
    "wong2020fast": """@inproceedings{wong2020fast,
  author       = {Wong, Eric and Rice, Leslie and Kolter, J. Zico},
  title        = {Fast is Better than Free: Revisiting Adversarial Training},
  booktitle    = {Proc. International Conference on Learning Representations ({ICLR})},
  year         = {2020},
  eprint       = {2001.03994},
  archiveprefix = {arXiv}
}
""",
    "engstrom2019robustness": """@misc{engstrom2019robustness,
  author       = {Engstrom, Logan and Ilyas, Andrew and Salman, Hadi and Santurkar, Shibani and Tsipras, Dimitris},
  title        = {Robustness ({Python} Library)},
  howpublished = {\\url{https://github.com/MadryLab/robustness}},
  year         = {2019}
}
""",
}

eklenen = []
for k, g in GIRDILER.items():
    if f"@{{{k}," in t or f"{{{k}," in t:
        print("ZATEN", k)
        continue
    t = t.rstrip("\n") + "\n\n% RobustBench havuzu modelleri (2026-10-04, arXiv kimlikleri dogrulandi)\n" + g if not eklenen else t + "\n" + g
    eklenen.append(k)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("eklendi:", eklenen)
