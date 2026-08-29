#!/usr/bin/env python3
"""TR aynasi - 9: ilgili calismalar (A3 Yu, manset ayristirmasi, sikistirma)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")
I = "02_ilgili_calismalar.tex"

YAMALAR = [
    # ---------- A3: Yu ve ark. dogru nitelendirme ----------
    (I,
     r"Yu vd.~\cite{yu2025reliable} ise transfer edilebilirliğin tek bir mimari "
     r"ailesi içinde ölçüldüğünde dizgesel olarak abartıldığını bildirmekte ve "
     r"buna karşılık üç değerlendirme protokolü önermektedir. Her ikisi de "
     r"puanlama kuralını sabit tutup saldırıyı ve model havuzunu değiştirmektedir. "
     r"Bu makale bunun tersini yapmaktadır: modeller, veri ve saldırı bütçesi "
     r"sabittir, yalnızca puanlama kuralı değişmektedir; bu da protokolün kendi "
     r"katkısını yalıtmakta ve ortaya çıkan kestirimler arasındaki aritmetik "
     r"bağıntıyı yazmayı mümkün kılmaktadır.",

     r"Yu vd.~\cite{yu2025reliable} ise transfer edilebilirliğin tek bir mimari "
     r"ailesi içinde ölçüldüğünde dizgesel olarak abartıldığını bildirmekte ve çok "
     r"hedefli bir sonucun nasıl puanlandığında ayrışan üç değerlendirme protokolü "
     r"önermektedir: topluluğu tek bir hedef saymak, kaç hedefin kandırıldığını "
     r"saymak ve hepsinin kandırılmasını istemek. TA-Bench puanlama kuralını sabit "
     r"tutup saldırıyı ve model havuzunu değiştirmekte; Yu vd.\ puanlama kuralını "
     r"hedef toplulaştırma ekseninde değiştirmektedir. Bu makale ise onu koşullama "
     r"ekseninde değiştirmektedir: modeller, veri ve saldırı bütçesi sabittir; bu "
     r"da koşullama kümesinin kendi katkısını yalıtmakta ve ortaya çıkan "
     r"kestirimler arasındaki aritmetik bağıntıyı yazmayı mümkün kılmaktadır.",
     "TR A3 Yu ve ark."),

    # ---------- A1: manset ayristirmasi ----------
    (I,
     r"ölçülen asimetrinin dört protokol boyunca $15{,}01\pm0{,}84$ puan "
     r"oynadığını buluyoruz; bu, 4,4 katlık bir yayılımdır. Buna karşılık her iki "
     r"mimariyi yeniden eğitmek aynı niceliği $1{,}5$ puandan az oynatmaktadır.",
     r"ölçülen asimetrinin dört protokol boyunca $15{,}01\pm0{,}84$ puan "
     r"oynadığını buluyoruz; bunun $3{,}91$ puanı onayladığımız iki protokolü "
     r"birbirinden ayırmaktadır. Buna karşılık her iki mimariyi yeniden eğitmek "
     r"aynı niceliği $1{,}5$ puandan az oynatmaktadır.",
     "TR A1 ilgili calismalar"),

    # ---------- tekrar sikistirmasi (giriste zaten var) ----------
    (I,
     r"Her birini doğrudan ölçüyoruz ve hiçbiri bizim kurulumumuzda geçerli "
     r"çıkmıyor; bu sonuçları raporluyoruz, çünkü protokole duyarlı bir "
     r"karşılaştırmanın kaldıramayacağı şey tam da bu türden test edilmemiş bir "
     r"varsayımdır.",
     r"Her birini doğrudan ölçüyoruz ve hiçbiri bizim kurulumumuzda geçerli "
     r"çıkmıyor; protokole duyarlı bir karşılaştırmanın kaldıramayacağı şey tam da "
     r"bu türden test edilmemiş bir varsayımdır.",
     "TR uc iddia sikistirma"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
