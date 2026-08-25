#!/usr/bin/env python3
"""A kolunda KONTROL NOKTASI BASINA tohumlama.

Bulgu (2026-08-25): PGD'nin random_start'i tarama boyunca TEK bir akistan
cekiyordu. Sonuc: bir kontrol noktasinin sayisi, ondan once kac kontrol
noktasi tarandigina bagliydi. Olculdu -- ayni yorunge stride=10 ve stride=50
ile tarandiginda ep1 birebir tutuyor (ilk cagri), ep51 ve ep100 tutmuyor
(raw'da 0,16 puana kadar). Yani yayimlanan bir noktayi yeniden uretmek icin
AYNI stride'i bilmek gerekiyordu; bu, yeniden uretilebilirlik hakkinda olan
bir makalede kabul edilemez.

Duzeltme: her kontrol noktasi, (yorunge, epok) ikilisinden turetilen kendi
tohumunu alir. Ayni epok, hangi stride ile tarandigindan BAGIMSIZ olarak
ayni sayiyi verir.
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/scripts/q1_e3_akolu.py")
t = p.read_text(encoding="utf-8")

if "_ck_tohum" in t:
    print("zaten yamali")
    sys.exit(0)

CIFTLER = [
    ("import argparse\nimport json\nimport re\nimport sys",
     "import argparse\nimport json\nimport re\nimport sys\nimport zlib",
     "zlib import"),

    ('''def set_seed(s):''',
     '''def _ck_tohum(taban, trajectory_id, epoch):
    """(yorunge, epok)'a baglanmis SABIT tohum.

    Tarama sirasindan bagimsiz olmasi sart: aksi halde ayni epok farkli
    stride'larda farkli sayi verir (bkz. betik basligi).
    """
    anahtar = zlib.crc32(f"{trajectory_id}|{epoch}".encode())
    return int((taban * 1_000_003 + anahtar) % (2 ** 31 - 1))


def set_seed(s):''',
     "tohum fonksiyonu"),

    ('''        M.load_state_dict(torch.load(ck, map_location="cpu", weights_only=False)["model_state_dict"])''',
     '''        M.load_state_dict(torch.load(ck, map_location="cpu", weights_only=False)["model_state_dict"])
        # Bu kontrol noktasinin PGD random_start'i YALNIZ (yorunge, epok)'a
        # bagli olsun; tarama sirasina bagli OLMASIN.
        set_seed(_ck_tohum(args.seed, args.trajectory_id, ep))''',
     "kontrol noktasi tohumu"),

    ('''            "kol": "A", "dataset": args.dataset, "kume": args.cluster,''',
     '''            "kol": "A", "dataset": args.dataset, "kume": args.cluster,
            "ck_tohum": _ck_tohum(args.seed, args.trajectory_id, ep),''',
     "kayitta tohum"),
]

for eski, yeni, ad in CIFTLER:
    if t.count(eski) != 1:
        print(f"YAMA BASARISIZ ({ad}): {t.count(eski)} eslesme")
        sys.exit(1)
    t = t.replace(eski, yeni, 1)

p.write_text(t, encoding="utf-8")
print("yamalandi: A kolu kontrol noktasi basina tohumlaniyor")
