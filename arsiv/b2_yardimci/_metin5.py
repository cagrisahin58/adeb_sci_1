#!/usr/bin/env python3
"""B2 metin -- 5/n: 'en genis protokol cifti HER ZAMAN ...' iddiasi.

Olculdu: 18 yon ciftinin 13'unde dogru. Bes ihlalin hepsi CIFAR-100'dedir ve
orada uc, koşulsuz orandir. 'Her zaman' yazilamaz; olculen yazilir.
"""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
hata, yazilan = [], []


def yama(rel, ciftler):
    p = ROOT / rel
    t = orig = p.read_text(encoding="utf-8")
    for eski, yeni, ad in ciftler:
        if eski not in t and yeni in t:
            continue
        if t.count(eski) != 1:
            hata.append(f"{rel} :: {ad}: {t.count(eski)} eslesme")
            return
        t = t.replace(eski, yeni, 1)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        yazilan.append(rel)


yama("paper/manuscript/sections/04_experiments.tex", [(
    "and the widest protocol pair is always target-correct against "
    "successful-source ($23.77$ points on average).",
    "The protocol pair with the largest average gap is target-correct against "
    "successful-source ($23.77$ points), and it is the widest pair in $13$ of the "
    "$18$ directions; in the remaining five, all on CIFAR-100, the unconditioned "
    "rate is the far end instead.",
    "EN en genis cift")])

yama("paper/manuscript_tr/sections/04_deneyler.tex", [(
    "ve en geniş protokol çifti her zaman hedef doğru ile başarılı kaynak "
    "arasındadır (ortalama $23{,}77$ puan).",
    "Ortalama açıklığı en büyük olan protokol çifti hedef doğru ile başarılı "
    "kaynak arasındadır ($23{,}77$ puan) ve bu çift $18$ yönün $13$'ünde en "
    "geniştir; kalan beşinde, ki hepsi CIFAR-100'dedir, uçtaki protokol koşulsuz "
    "orandır.",
    "TR en genis cift")])

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("yazilan:", *yazilan, sep="\n  ")
