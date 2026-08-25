#!/usr/bin/env python3
"""Uc yeni kaynagin TURKCE ayna yerlestirmesi."""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections/02_ilgili_calismalar.tex")
t = p.read_text(encoding="utf-8")

if "yu2025reliable" in t:
    print("zaten yapilmis")
    sys.exit(0)

CIFTLER = [
    ("protokol seçimlerini açık hâle getirmektedir~\\cite{zhao2025revisiting}.",
     "protokol seçimlerini açık hâle getirmektedir~\\cite{zhao2025revisiting}. "
     "Yakın tarihli iki kıyaslama da aynı yönde ilerlemektedir: "
     "TA-Bench~\\cite{li2023tabench} otuzu aşkın transfer saldırısını ortak bir vekil "
     "ve kurban model havuzu üzerinde standartlaştırmakta, Yu vd.~\\cite{yu2025reliable} "
     "ise transfer edilebilirliğin tek bir mimari ailesi içinde ölçüldüğünde dizgesel "
     "olarak abartıldığını bildirmekte ve buna karşılık üç değerlendirme protokolü "
     "önermektedir. Her ikisi de puanlama kuralını sabit tutup saldırıyı ve model "
     "havuzunu değiştirmektedir. Bu makale bunun tersini yapmaktadır: modeller, veri "
     "ve saldırı bütçesi sabittir, yalnızca puanlama kuralı değişmektedir; bu da "
     "protokolün kendi katkısını yalıtmakta ve ortaya çıkan kestirimler arasındaki "
     "aritmetik bağıntıyı yazmayı mümkün kılmaktadır.",
     "TR protokol kiyaslamalari"),

    ("Bu transfer örüntülerini anlamak, gürbüz topluluk sistemleri geliştirmek ve "
     "gerçek dünya saldırı senaryolarını değerlendirmek için önemlidir.",
     "Waseda vd.~\\cite{waseda2023closer} transfer sonuçlarını bir adım daha "
     "ayırmakta, hedefin kaynağın tam olarak aynı hatasını tekrarlayıp "
     "tekrarlamadığına göre sınıflandırmakta ve her iki durumun birbirine yakın "
     "modeller arasında bile görüldüğünü bildirmektedir. Bu transfer örüntülerini "
     "anlamak, gürbüz topluluk sistemleri geliştirmek ve gerçek dünya saldırı "
     "senaryolarını değerlendirmek için önemlidir.",
     "TR waseda"),
]

for eski, yeni, ad in CIFTLER:
    if t.count(eski) != 1:
        print(f"BASARISIZ ({ad}): {t.count(eski)} eslesme")
        sys.exit(1)
    t = t.replace(eski, yeni, 1)

p.write_text(t, encoding="utf-8")
print("TR ayna yazildi")
