#!/usr/bin/env python3
"""TR aynasi - 8: tartisma bolumu (C4, C5, C8, B1 birim, sikistirmalar)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")
T = "05_tartisma.tex"

YAMALAR = [
    # ---------- C5 + C8: saldiri ailesi tek veri kumesi, aciklik 12,3/20,7 ----------
    (T,
     r"Dört protokol, üç eğitim koşusu ve iki saldırı ailesi (PGD-10 ve MI-FGSM) "
     r"boyunca, CNN'de üretilen çekişmeli örnekler \emph{her iki CIFAR veri "
     r"kümesinde} ViT'e tersinden daha iyi transfer olmaktadır. Aynı tarifle "
     r"çekişmeli eğitimin iki mimariyi $11$ ya da $21$ puan değil yalnızca "
     r"$1{,}85$ puan ayırdığı SVHN'de ise bu artık doğru değildir: iki protokol "
     r"CNN üstünlüğü, iki protokol ViT üstünlüğü bildirmekte",
     r"Dört protokol ve üç eğitim koşusu boyunca, CNN'de üretilen çekişmeli "
     r"örnekler \emph{her iki CIFAR veri kümesinde} ViT'e tersinden daha iyi "
     r"transfer olmakta, CIFAR-10'da yön ikinci bir saldırı ailesi altında da "
     r"(MI-FGSM) korunmaktadır. Aynı tarifin iki mimariyi $12{,}3$ ya da $20{,}7$ "
     r"puan değil yalnızca $1{,}85$ puan ayırdığı SVHN'de ise bu artık doğru "
     r"değildir: iki protokol CNN üstünlüğü, iki protokol ViT üstünlüğü bildirmekte",
     "TR C5+C8 saldiri ailesi ve aciklik"),

    # ---------- yon paragrafi sikistirma ----------
    (T,
     r"Yön, mimarilerin değil eşitlenmemiş rejimin bir özelliğidir. Eşitlenmemiş "
     r"rejim içinde protokoller arasında değişen yalnızca etkinin ne kadar büyük "
     r"göründüğü ve bir eşdeğerlik testinin onu kabul edip etmediğidir; modeller "
     r"eşitlendiğinde işaret de değişmektedir. Üç hedefli analizimiz bu yön için "
     r"CNN pertürbasyonlarının özel olmasını gerektirmeyen bir okuma önermektedir: "
     r"gelen transfer her hedefin kendi beyaz kutu kırılganlığını izler (üç hedef "
     r"üzerinde $r = 0{,}986$) ve en gürbüz hedef iki aileden gelen saldırıları "
     r"neredeyse eşit soğurur.",
     r"Yön, mimarilerin değil eşitlenmemiş rejimin bir özelliğidir: modeller "
     r"eşitlenmemişken protokol yalnızca etkinin ne kadar büyük göründüğünü ve "
     r"eşdeğerliğin kabul edilip edilmediğini değiştirir, eşitlendiklerinde ise "
     r"işareti de değiştirir. Üç hedefli analizimiz bu yönü CNN "
     r"pertürbasyonlarının özel olmasını gerektirmeden okur: gelen transfer her "
     r"hedefin kendi beyaz kutu kırılganlığını izler ($r = 0{,}986$) ve en gürbüz "
     r"hedef iki aileyi de neredeyse eşit soğurur.",
     "TR yon paragrafi"),

    # ---------- B1: seyreklik cikarim birimi ----------
    (T,
     r"(Hoyer $0{,}4928$'e karşı $0{,}4561$, eşleştirilmiş $p<10^{-11}$); ama aynı "
     r"gradyanların dört mekânsal betimleyicisi",
     r"(Hoyer $0{,}4928$'e karşı $0{,}4561$, her koşuda tutarlı; örnek bazlı "
     r"$p<10^{-11}$, koşum düzeyinde düzeltmeden sonra $p=0{,}108$); ama aynı "
     r"gradyanların dört mekânsal betimleyicisi",
     "TR B1 tartisma birimi"),

    # ---------- C4: uc kat -> dort kat ----------
    (T,
     r"yani CLS yolunun yama ortalamasının üç katı kayması",
     r"yani CLS yolunun yama ortalamasının yaklaşık dört katı kayması",
     "TR C4 drift orani"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
