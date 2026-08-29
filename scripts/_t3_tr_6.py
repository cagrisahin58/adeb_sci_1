#!/usr/bin/env python3
"""TR aynasi - 6: giris ve sonuc (manset ayristirmasi, null sayisi, provenans)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")

YAMALAR = [
    # ---------- C1: dordu de null ----------
    ("01_giris.tex",
     r"ölçekten bağımsız seyreklik farkları mekânsal lokalite farkına karşılık "
     r"gelmemektedir; dört mekânsal ölçütten üçü sıfır sonuç vermiştir.",
     r"ölçekten bağımsız seyreklik farkları mekânsal lokalite farkına karşılık "
     r"gelmemektedir; dört mekânsal ölçütün dördü de sıfır sonuç vermiştir.",
     "TR C1 null sayisi"),

    # ---------- A1: giris ayristirmasi ----------
    ("01_giris.tex",
     r"ölçülen mimariler arası transfer asimetrisi dört yerleşik koşullama "
     r"protokolü boyunca $+4{,}4$ ile $+19{,}4$ puan arasında değişmektedir; bu "
     r"4,4 katlık bir yayılımdır, buna karşılık her iki mimariyi sıfırdan yeniden "
     r"eğitmek aynı niceliği $1{,}5$ puandan az oynatmaktadır.",
     r"ölçülen mimariler arası transfer asimetrisi dört koşullama protokolü "
     r"boyunca $+4{,}4$ ile $+19{,}4$ puan arasında değişmektedir; bu 4,4 katlık "
     r"bir yayılımdır, buna karşılık her iki mimariyi sıfırdan yeniden eğitmek "
     r"aynı niceliği $1{,}5$ puandan az oynatmaktadır. Ardından bu yayılımı tek "
     r"bir sayı olarak bırakmak yerine ayrıştırıyoruz: $5{,}80$ puanı farklı bir "
     r"niceliği kestiren bir protokolden, $5{,}30$ puanı koşullamayı büsbütün "
     r"bırakmaktan (türettiğimiz bir özdeşlik bunu kapalı formda düzeltmektedir) "
     r"ve $3{,}91$ puanı ikisi de savunulabilir iki protokol arasındaki takdirden "
     r"gelmektedir; sonuncusu bile yeniden eğitmenin etkisinin iki katından "
     r"fazladır.",
     "TR A1 giris ayristirmasi"),

    # ---------- A1: sonuc ayristirmasi ----------
    ("06_sonuc.tex",
     r"mimariler arası transfer asimetrisi dört yerleşik koşullama protokolü "
     r"boyunca $+4{,}4$ ile $+19{,}4$ puan arasında değişmektedir; bu, 4,4 katlık "
     r"bir yayılımdır. Buna karşılık her iki mimariyi sıfırdan yeniden eğitmek "
     r"aynı niceliği $1{,}5$ puandan az oynatmaktadır. Protokol, bir eşdeğerlik "
     r"testinin kabul mü ret mi edileceğine karar vermektedir.",
     r"mimariler arası transfer asimetrisi dört koşullama protokolü boyunca "
     r"$+4{,}4$ ile $+19{,}4$ puan arasında değişmekte, buna karşılık her iki "
     r"mimariyi sıfırdan yeniden eğitmek aynı niceliği $1{,}5$ puandan az "
     r"oynatmaktadır. Bu $15{,}01$ puanlık yayılım üç parçaya ayrılmaktadır: "
     r"$5{,}80$ puan farklı bir estimand, $5{,}30$ puan bir özdeşliğin kapalı "
     r"formda düzelttiği pay ve $3{,}91$ puan ikisi de savunulabilir iki protokol "
     r"arasındaki gerçek takdir; bir raporlama ölçütünün ele alması gereken de "
     r"sonuncusudur.",
     "TR A1 sonuc ayristirmasi"),

    # ---------- sonuc: "literaturde yaygin uc iddia" provenansi ----------
    ("06_sonuc.tex",
     r"Bu literatürde yaygın üç iddia doğrudan ölçümden sağ çıkamamıştır: "
     r"çekişmeli eğitilmiş CNN gradyanları daha seyrektir ama mekânsal olarak daha "
     r"lokalize değildir; CLS dikkat entropisi $n=1000$'de $L_\infty$ saldırısı "
     r"altında değişmemektedir; dönüştürücüye özgü bir transfer saldırısı bu "
     r"rejimde transfer kazancı sağlamamaktadır.",
     r"Üç okuma doğrudan ölçümden sağ çıkamamıştır: çekişmeli eğitilmiş CNN "
     r"gradyanları daha seyrektir ama mekânsal olarak daha lokalize değildir; CLS "
     r"dikkat entropisi $n=1000$'de $L_\infty$ saldırısı altında değişmemektedir; "
     r"dönüştürücüye özgü bir transfer saldırısı bu rejimde transfer kazancı "
     r"sağlamamaktadır. Bunlardan yalnızca üçüncüsü yayımlanmış bir iddiadır; ilk "
     r"ikisi kendi önceki şekillerimizin davet ettiği doğal okumalardır ve onları "
     r"öyle sınıyoruz.",
     "TR sonuc iddia provenansi"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
