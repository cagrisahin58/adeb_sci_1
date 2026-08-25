#!/usr/bin/env python3
"""TESLIM_DURUMU'na 2026-08-25 kararlarini isler."""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/results/q1_research/TESLIM_DURUMU.md")
t = p.read_text(encoding="utf-8")

if "2026-08-25 KARARLARI" in t:
    print("zaten islenmis")
    sys.exit(0)

ESKI = "Karar verilene kadar metin OLDUĞU GİBİ duruyor; sessizce değiştirilmedi."
YENI = """**KAPANDI (2026-08-25): 1. seçenek uygulandı.** Vaat geri çekilmedi,
**kapsamı yazıldı.** Kabul sonrasında yayımlanacak küme, makaledeki her sayıyı
yeniden üretmeye yetendir: analiz hattı, her tabloyu ve şekli üreten betikler,
örnek bazında değerlendirme kayıtları, sabit doğrulama bölmesi indeksleri ve
tohum listeleri. Dört koşullama protokolünün tamamı örnek bazındaki kayıtlardan
hesaplandığı için protokol karşılaştırması **yeniden eğitim gerektirmeden**
tekrarlanabilir. Kontrol noktaları (~36 GB) "istek üzerine" olarak nitelendi.

Yol boyunca ikinci bir kusur çıktı: iki Sonuç bölümü vaadi **şimdiki zamanda**
("yayımlıyoruz") yazıyordu; depo kapalıyken bu, gönderim anında doğru olmayan
bir cümledir. Dört yerin dördü de gelecek zamana ve aynı kapsama çekildi.

---

## 2c. 2026-08-25 KARARLARI

| # | Karar | Gerekçe |
|---|---|---|
| 8 | **B2: kod düzeltildi, metin değil** | Makalenin kendi Tartışma bölümü bu protokolü "zaten işe yaramış bir saldırının ne kadar taşındığı" diye tanımlıyor; gevşek maske o soruyu yanıtlamıyordu. Ayrıntı ve kalan iş: `B2_DURUM.md` |
| 9 | **SVHN, B kolu uydurmasına girmiyor** | `E3_YENIDEN_TASARIM.md` EK E.1/E.5 bileşimi ön-kayıtla sabitliyor; sonucu gördükten sonra değiştirmek K5'i bozardı. Duyarlılık olarak raporlanacak |
| 10 | **Üç kaynak eklendi** | TA-Bench (NeurIPS 2023), Waseda vd. (WACV 2023), Yu vd. (SaTML 2025, s. 797-810) — künyeleri arXiv/DBLP'den doğrulandı |
| 11 | **Depo: kabul sonrası kapsamlı açılım** | yukarıya bakınız |

**Makale şu anda kendi kapısından GEÇMİYOR** ve bu bilerek böyle: A kolu
yeniden koşulana kadar H1/H2 muhafızları kırmızı kalır."""

if t.count(ESKI) != 1:
    print(f"BASARISIZ: {t.count(ESKI)} eslesme")
    sys.exit(1)

p.write_text(t.replace(ESKI, YENI, 1), encoding="utf-8")
print("TESLIM_DURUMU guncellendi")
