#!/usr/bin/env python3
"""B2 metin -- 6/n: Tartisma bolumundeki iki nitel iddia.

(a) CIFAR-100 yayilimi artik CIFAR-10'un ALTINDA; "temiz dogruluk farkindan
    gecen mekanizmayla tutarlidir" gerekcesi bu haliyle fazla guclu. Olculen
    sey yazilir: mekanizma etkinin BUYUKLUGUNU ongoruyor, veri kumeleri
    arasindaki SIRALAMASINI ongormuyor.
(b) L2 yayilimi "ayni buyuklukte" DEGIL (10,92'ye karsi 15,01). Ayakta kalan
    sey buyuklugun esitligi degil, etkinin YOK OLMAMASIDIR -- ki on-kaydin
    sinadigi da tam olarak budur.
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


yama("paper/manuscript/sections/05_discussion.tex", [
    ("and the sign is preserved in all twelve measurements "
     "(Section~\\ref{subsec:cifar100}), which is consistent with a mechanism that "
     "runs through the clean-accuracy difference between targets rather than "
     "through anything CIFAR-specific.",
     "and the sign is preserved in all twelve measurements "
     "(Section~\\ref{subsec:cifar100}). The effect is therefore not CIFAR-specific, "
     "but its size does not follow the clean-accuracy gap across datasets: "
     "CIFAR-100 has by far the larger gap and the slightly smaller spread. The "
     "mechanism we propose predicts that a gap produces a spread, not how the "
     "spread orders between datasets.",
     "EN C100 gerekce"),
    ("We evaluated the same checkpoints under an $L_2$ budget and the protocol "
     "spread survived at the same size (Section~\\ref{subsec:l2})",
     "We evaluated the same checkpoints under an $L_2$ budget and the protocol "
     "spread survived, at $10.92$ against $15.01$ points "
     "(Section~\\ref{subsec:l2})",
     "EN L2 ayni buyukluk"),
])

yama("paper/manuscript_tr/sections/05_tartisma.tex", [
    ("ve işaret on iki ölçümün tamamında korunmaktadır "
     "(Bölüm~\\ref{subsec:cifar100}); bu, CIFAR'a özgü bir şeyden değil hedefler "
     "arasındaki temiz doğruluk farkından geçen bir mekanizmayla tutarlıdır.",
     "ve işaret on iki ölçümün tamamında korunmaktadır "
     "(Bölüm~\\ref{subsec:cifar100}). Dolayısıyla etki CIFAR'a özgü değildir; ancak "
     "büyüklüğü veri kümeleri arasında temiz doğruluk farkını izlememektedir: "
     "CIFAR-100'de fark açık ara daha büyük, yayılım ise bir miktar daha küçüktür. "
     "Önerdiğimiz mekanizma bir farkın bir yayılım ürettiğini öngörmekte, "
     "yayılımın veri kümeleri arasında nasıl sıralanacağını öngörmemektedir.",
     "TR C100 gerekce"),
    ("Aynı kontrol noktalarını bir $L_2$ bütçesi altında değerlendirdik ve protokol "
     "yayılımı aynı büyüklükte ayakta kaldı (Bölüm~\\ref{subsec:l2})",
     "Aynı kontrol noktalarını bir $L_2$ bütçesi altında değerlendirdik ve protokol "
     "yayılımı ayakta kaldı; $15{,}01$ puana karşı $10{,}92$ puan "
     "(Bölüm~\\ref{subsec:l2})",
     "TR L2 ayni buyukluk"),
])

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("yazilan:", *yazilan, sep="\n  ")
