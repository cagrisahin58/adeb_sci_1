#!/usr/bin/env python3
"""a2'de RASTGELE AKISLARI AYIRIR.

Bulgu (2026-08-25 gerileme kontrolu): tek bir modul duzeyi RNG'yi butun
bootstrap'lar ve permutasyon testi paylasiyordu. Bes'inci (tani amacli)
protokolu eklemek, ondan SONRA gelen permutasyon testinin cektigi sayilari
kaydirdi ve SVHN'de p 0,10465 -> 0,10665 oynadi. Sayi zararsizdi, mekanizma
degildi: bir alt-akis istatistigi, yukarida kac nicelik hesaplandigina
BAGLI OLMAMALIDIR.

Cozum: her tuketici kendi akisini alir; akis, ana tohum ile tuketicinin
ADINDAN turetilir. Boylece bir protokol eklemek/cikarmak baska hicbir
istatistigi oynatmaz ve her sayi tek basina yeniden uretilebilir.
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/experiments/rev2/a2_transfer_protocols.py")
t = p.read_text(encoding="utf-8")

if "_akis(" in t:
    print("zaten yamali")
    sys.exit(0)

CIFTLER = [
    ("RNG = np.random.default_rng(42)",
     '''SEED = 42


def _akis(*etiket):
    """Tuketici adina baglanmis BAGIMSIZ rastgele akis.

    Tek bir paylasilan RNG kullanilirsa, yukarida fazladan bir bootstrap
    kosmak asagidaki permutasyon testinin sayilarini kaydirir. Ad-tabanli
    turetme bunu imkansiz kilar; her sayi tek basina yeniden uretilebilir.
    """
    anahtar = zlib.crc32("|".join(str(e) for e in etiket).encode())
    return np.random.default_rng([SEED, anahtar])''',
     "RNG tanimi"),

    ('''def rate_ci(fool_mask, cond_mask):
    idx = np.flatnonzero(cond_mask)
    vals = fool_mask[idx].astype(float)
    n = len(vals)
    boots = np.empty(N_BOOT)
    for b in range(N_BOOT):
        boots[b] = vals[RNG.integers(0, n, n)].mean()''',
     '''def rate_ci(fool_mask, cond_mask, etiket):
    rng = _akis("rate_ci", etiket)
    idx = np.flatnonzero(cond_mask)
    vals = fool_mask[idx].astype(float)
    n = len(vals)
    boots = np.empty(N_BOOT)
    for b in range(N_BOOT):
        boots[b] = vals[rng.integers(0, n, n)].mean()''',
     "rate_ci"),

    ('''        "CNN_to_ViT": rate_ci(f_cv, c_cv),
        "ViT_to_CNN": rate_ci(f_vc, c_vc),''',
     '''        "CNN_to_ViT": rate_ci(f_cv, c_cv, f"{protocol}/CNN_to_ViT"),
        "ViT_to_CNN": rate_ci(f_vc, c_vc, f"{protocol}/ViT_to_CNN"),''',
     "rate_ci cagrilari"),

    ('''# paired bootstrap CI
boots = np.empty(N_BOOT)
for b in range(N_BOOT):
    boots[b] = d[RNG.integers(0, n, n)].mean()''',
     '''# paired bootstrap CI -- KENDI akisi
_rng_boot = _akis("both_correct_paired", "bootstrap")
boots = np.empty(N_BOOT)
for b in range(N_BOOT):
    boots[b] = d[_rng_boot.integers(0, n, n)].mean()''',
     "paired bootstrap"),

    ('''signs = RNG.integers(0, 2, size=(N_PERM, n)) * 2 - 1''',
     '''_rng_perm = _akis("both_correct_paired", "permutation")
signs = _rng_perm.integers(0, 2, size=(N_PERM, n)) * 2 - 1''',
     "permutasyon"),

    ('''import json
import math
import os''',
     '''import json
import math
import os
import zlib''',
     "zlib import"),
]

for eski, yeni, ad in CIFTLER:
    if t.count(eski) != 1:
        print(f"YAMA BASARISIZ ({ad}): {t.count(eski)} eslesme")
        sys.exit(1)
    t = t.replace(eski, yeni, 1)

p.write_text(t, encoding="utf-8")
print("yamalandi: a2 rastgele akislari ayrildi")
