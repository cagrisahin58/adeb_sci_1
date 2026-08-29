#!/usr/bin/env python3
"""TR ozeti butun olarak degistirir (EN ile ayni icerik, <=250 kelime).

Duzeltilenler: (1) ozdesligin eksik carpani (1-r_kos) geri konur,
(2) manset ayristirmasi girer, (3) "bu alanda yaygin uc iddia" fazla
iddiasi "uc okuma"ya cekilir.
"""
import re
import sys
from pathlib import Path

P = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/main.tex")

YENI = """\\begin{abstract}
Mimari aileleri arasındaki çekişmeli gürbüzlük karşılaştırmaları birbiriyle çelişen sonuçlar bildirmekte ve bu anlaşmazlık genellikle modellere, eğitim tariflerine ya da veri kümelerine bağlanmaktadır. Bu çalışmada, anlaşmazlığın büyük kısmının ölçüm protokolünün kendisinden geldiğini gösteriyoruz. Mimari başına üç eğitim koşumu, örnek bazında kayıtla tam test kümesi değerlendirmesi ve her eğitimden önce ayrılmış bir doğrulama bölmesi kullanan çekişmeli eğitilmiş ResNet-18 ve ViT-Tiny çiftlerinde modelleri, veriyi, tehdit modelini ve saldırı bütçesini sabit tutup yalnızca transferin nasıl puanlandığını değiştiriyoruz. Dört koşullama protokolü altında ölçülen CNN'den ViT'e transfer asimetrisi CIFAR-10'da $4{,}4$ ile $19{,}4$ puan arasında değişmekte, oysa iki mimariyi yeniden eğitmek aynı büyüklüğü $1{,}5$ puandan az oynatmaktadır. Bu $15{,}01$ puanlık yayılım tek bir şey değildir: $5{,}80$ puanı farklı bir niceliği kestiren bir protokolden, $5{,}30$ puanı koşullamayı büsbütün bırakmaktan ve $3{,}91$ puanı ikisi de savunulabilir iki protokol arasındaki indirgenemez takdirden gelmektedir. Ortadaki pay tam olarak düzeltilebilir: koşulsuz oranın koşullu orandan sapması, hedefin temiz hatasının bir eksi koşullu oranla ölçeklenmiş hâline eşittir ve bu özdeşliğin öncülünü varsaymak yerine ölçüyoruz. Tasarımın CIFAR-100'de yinelenmesi on iki ölçümün tamamında işareti korumaktadır. Aynı tarifin iki mimariyi temiz doğrulukta $1{,}85$ puan ayırdığı SVHN'de ise protokol yalnızca büyüklüğe değil işarete de karar vermektedir: iki protokol CNN, ikisi ViT üstünlüğü bildirmektedir. Yalnızca kontrol noktası seçim kuralını değiştirmek, neredeyse hiç raporlanmayan dördüncü bir varyans kaynağı eklemektedir. Üç okuma daha doğrudan ölçüm altında yinelenmemekte; çalışmayı mimariler arası gürbüzlük çalışmaları için raporlama gereklilikleriyle kapatıyoruz.
\\end{abstract}"""

t = P.read_text(encoding="utf-8")
yeni_t, n = re.subn(r"\\begin\{abstract\}.*?\\end\{abstract\}", lambda _: YENI,
                    t, count=1, flags=re.DOTALL)
if n != 1:
    sys.exit("BASARISIZ: TR ozet blogu bulunamadi")
P.write_text(yeni_t, encoding="utf-8")
govde = re.search(r"\\begin\{abstract\}(.+?)\\end\{abstract\}", YENI, re.DOTALL).group(1)
print(f"TR ozet yazildi: {len(govde.split())} kelime")
