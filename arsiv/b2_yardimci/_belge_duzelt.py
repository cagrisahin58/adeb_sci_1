#!/usr/bin/env python3
"""Denetimin buldugu IKI BAYAT BELGE tablosunu duzeltir.

CLAUDE.md'nin "C1 SONRASI (gecerli)" tablosu ve TESLIM_DURUMU'nun bildiri
denetim tablosu B2 sonrasi guncellenmemisti. Ikisi de "tek kaynak
C1_REFERANS_FOYU.md" diyor ama fooyle celisiyorlardi; ustelik TESLIM_DURUMU
tablosunun HER IKI sutunu da bayat oldugu icin "tutuyor" hukmu artik hicbir
seyi dogrulamiyordu.
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


yama("CLAUDE.md", [
    ("| Transfer (her ikisi dogru) | fark +8,27+/-0,23 · bootstrap GA "
     "[7,33; 9,21] · isaret-cevirme p ~ 0 | ayni |",
     "| Transfer (her ikisi dogru) | fark +8,27+/-0,23 · bootstrap GA "
     "[7,33; 9,22] · isaret-cevirme p ~ 0 | ayni |", "CLAUDE GA"),
    ("| Protokol yayilimi | 10,45+/-0,76 puan (en buyuk/en kucuk tahmin "
     "orani ~3,3x) | ayni |",
     "| Protokol yayilimi | 15,01+/-0,84 puan (en buyuk/en kucuk tahmin "
     "orani ~4,4 kat) | ayni |\n"
     "| Basarili kaynak (B2 sonrasi) | fark +19,37+/-1,27 · maske: hedef-dogru "
     "VE kaynak-temizde-dogru VE kaynak-adv-yanlis | `src/analysis/protokoller.py` |",
     "CLAUDE yayilim"),
])

yama("results/q1_research/TESLIM_DURUMU.md", [
    ("| Protokol aralığı | +4,4 ile +14,6 | 4,36 ile 14,60 | tutuyor |\n"
     "| Protokol oranı | 3,3 kat | 14,60/4,36 = 3,35 | tutuyor |",
     "| Protokol aralığı | +4,4 ile +19,4 | 4,36 ile 19,37 | tutuyor |\n"
     "| Protokol oranı | 4,4 kat | 19,37/4,36 = 4,44 | tutuyor |\n"
     "| Başarılı kaynak (tablo) | +19,37 / ‡ +11,17 | aynı | tutuyor |\n"
     "\n"
     "> Bu tablo 2026-08-25'te B2 düzeltmesine göre yenilendi. Önceki hâli hem\n"
     "> bildirinin hem artefaktın eski değerlerini taşıyordu; iki sütun birden\n"
     "> bayat olduğu için \"tutuyor\" hükmü hiçbir şeyi doğrulamıyordu. Artık\n"
     "> denetim elle değil `scripts/bildiri_tutarlilik.py` ile yapılıyor ve o\n"
     "> kapı otoriter değerleri ARTEFAKTTAN okuyor.", "TESLIM bildiri tablosu"),
])

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("yazilan:", *yazilan, sep="\n  ")
