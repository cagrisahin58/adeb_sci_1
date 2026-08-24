#!/usr/bin/env python3
"""DEPO VAADI: makalenin verdigi sozu YERINE GETIRILEBILIR hale getirir.

Sorun (TESLIM_DURUMU §2b): makale uc yerde kaynak kod ve kontrol noktalarinin
"kabul sonrasinda herkese acik" olacagini soyluyor, ustelik iki Sonuc bolumu
bunu SIMDIKI ZAMANDA ("yayimliyoruz") yaziyor. Depo ise kapali kalacak. Boyle
birakilirsa makale, gonderim aninda dogru OLMAYAN bir cumle tasir.

Karar: vaat geri cekilmiyor, KAPSAMI yaziliyor. Kabul sonrasinda yayimlanacak
kume, makaledeki her sayiyi yeniden uretmeye YETEN kumedir:
  - analiz kodu ve tablo/sekil ureten betikler,
  - ornek bazinda degerlendirme kayitlari (per_sample_*.npz),
  - sabit dogrulama bolmesi indeksleri ve tohum listeleri.
Kontrol noktalari (~36 GB) toplu barindirmaya uygun olmadigi icin "istek
uzerine" olarak nitelenir. Bu, protokol karsilastirmasinin bagimsiz olarak
yeniden uretilmesi icin yeterlidir: dort protokolun tamami ornek bazinda
maskelerden hesaplanmaktadir.
"""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
hata, yazilan = [], []


def yama(rel, ciftler, imza):
    p = ROOT / rel
    t = orig = p.read_text(encoding="utf-8")
    if imza in t:
        return
    for eski, yeni, ad in ciftler:
        if t.count(eski) != 1:
            hata.append(f"{rel} :: {ad}: {t.count(eski)} eslesme")
            return
        t = t.replace(eski, yeni, 1)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        yazilan.append(rel)


# ------------------------------------------------------- EN erisilebilirlik
EN_ESKI = ("The source code for the analysis pipeline and trained model checkpoints "
           "will be made publicly available upon acceptance.")
EN_YENI = ("Upon acceptance we will publish the analysis pipeline, the scripts that "
           "generate every table and figure in this paper, the per-sample evaluation "
           "records, the fixed validation-split indices and the seed lists, which "
           "together reproduce every number reported here; the four conditioning "
           "protocols are all computed from the per-sample records, so the protocol "
           "comparison can be repeated without retraining. Trained checkpoints total "
           "about $36$~GB and are available from the authors on request.")

EN_YORUM_ESKI = ("% TODO(submission): repo URL — kabul sonrasi (veya gonderimde anonim depo ile)\n"
                 "% asagidaki cumleye gercek URL eklenecek. Erisebilirlik dili uc yerde de\n"
                 '% "will be made publicly available upon acceptance" olarak birlestirildi.')
EN_YORUM_YENI = ("% TODO(submission): repo URL — kabul sonrasi (veya gonderimde anonim depo ile)\n"
                 "% asagidaki cumleye gercek URL eklenecek.\n"
                 "% 2026-08-25: vaat KAPSAMLANDI. Yayimlanacak kume makaledeki her sayiyi\n"
                 "% yeniden uretmeye yeter (analiz kodu + ornek bazinda kayitlar + bolme\n"
                 "% indeksleri + tohumlar); kontrol noktalari (~36 GB) istek uzerine.\n"
                 "% Uc yerdeki dil ayni: gelecek zaman, ayni kapsam.")

yama("paper/manuscript/main.tex",
     [(EN_YORUM_ESKI, EN_YORUM_YENI, "EN yorum"), (EN_ESKI, EN_YENI, "EN beyan")],
     "available from the authors on request")

# ------------------------------------------------------- TR erisilebilirlik
TR_ESKI = ("Analiz hattının kaynak kodu, eğitilmiş model kontrol noktaları, örnek "
           "bazında değerlendirme kayıtları ve tüm analiz betikleri kabul sonrasında "
           "herkese açık hâle getirilecektir.")
TR_YENI = ("Kabul sonrasında analiz hattını, bu makaledeki her tabloyu ve şekli üreten "
           "betikleri, örnek bazında değerlendirme kayıtlarını, sabit doğrulama bölmesi "
           "indekslerini ve tohum listelerini yayımlayacağız; bunlar burada raporlanan "
           "her sayıyı yeniden üretmeye yetmektedir, çünkü dört koşullama protokolünün "
           "tamamı örnek bazındaki kayıtlardan hesaplanmaktadır ve protokol "
           "karşılaştırması yeniden eğitim gerektirmeden tekrarlanabilmektedir. "
           "Eğitilmiş kontrol noktaları yaklaşık $36$~GB tutmaktadır ve yazarlardan "
           "istek üzerine sağlanmaktadır.")

yama("paper/manuscript_tr/main.tex", [(TR_ESKI, TR_YENI, "TR beyan")],
     "istek üzerine sağlanmaktadır")

# ------------------------------------------------------------- EN Sonuc
EN_S_ESKI = ("We release the full pipeline, per-sample logs, and analysis scripts so "
             "that the protocol comparison can be reproduced and extended.")
EN_S_YENI = ("The pipeline, the per-sample logs and the analysis scripts will be "
             "released on acceptance so that the protocol comparison can be reproduced "
             "and extended.")
yama("paper/manuscript/sections/06_conclusion.tex",
     [(EN_S_ESKI, EN_S_YENI, "EN sonuc")], "will be\nreleased on acceptance")

# ------------------------------------------------------------- TR Sonuc
TR_S_ESKI = ("Protokol karşılaştırmasının yeniden üretilip genişletilebilmesi için tam "
             "boru hattını, örnek bazında kayıtları ve analiz betiklerini yayımlıyoruz.")
TR_S_YENI = ("Protokol karşılaştırmasının yeniden üretilip genişletilebilmesi için tam "
             "boru hattı, örnek bazında kayıtlar ve analiz betikleri kabul sonrasında "
             "yayımlanacaktır.")
yama("paper/manuscript_tr/sections/06_sonuc.tex",
     [(TR_S_ESKI, TR_S_YENI, "TR sonuc")], "kabul sonrasında yayımlanacaktır")

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("yazilan:", *yazilan, sep="\n  ")
