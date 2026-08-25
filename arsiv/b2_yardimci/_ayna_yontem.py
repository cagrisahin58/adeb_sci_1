#!/usr/bin/env python3
"""EN/TR AYNA KUSURU: TR yonteminde 'Oznitelik Bozunmasi Metrikleri' YOK.

Ingilizce Bolum 3'te \\paragraph{Feature Degradation Metrics} basligi, iki
denklem (oznitelik kosinus benzerligi ve norm degisimi) ve L2 uzakligi
tanimi var. Turkce surumde bu blok HIC YOK -- oysa Turkce Bolum 4 ayni
metrikleri kullaniyor ve raporluyor. Yani Turkce surum, kullandigi
metrikleri tanimlamiyordu.

Bu kusur B2'den ONCE de vardi; sayi kapilari gormez cunku kapilar sayilari
denetler, YAPIYI degil. EN/TR ayna kontrolu (scripts/_b2_ayna_kontrol.py)
buldu: EN 8 denklem, TR 6.
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections/03_yontem.tex")
t = p.read_text(encoding="utf-8")

if "Öznitelik Bozunması Metrikleri" in t:
    print("zaten var")
    sys.exit(0)

ANKOR = ("Düz MI-FGSM~\\cite{dong2018boosting} örnekleri aynı koşuda aynı örnekler "
         "üzerinde üretilir; bu, birebir aynı bütçede eşleştirilmiş bir kontrol "
         "sağlar.")

EK = ANKOR + """

\\paragraph{Öznitelik Bozunması Metrikleri}
Çekişmeli pertürbasyonların ViT temsillerini katmanlar boyunca nasıl etkilediğini incelemek için her $\\ell$ katmanında üç metrik hesaplıyoruz. Öznitelik kosinüs benzerliği, temsilin yönünün ne ölçüde korunduğunu ölçer:
\\begin{equation}
    \\text{Benz}_\\ell = \\frac{h_\\ell(x) \\cdot h_\\ell(x_{adv})}{\\|h_\\ell(x)\\| \\|h_\\ell(x_{adv})\\|}
\\end{equation}
burada $h_\\ell$, $\\ell$ katmanındaki temsili göstermektedir. Öznitelik norm değişimi ise büyüklük etkilerini yakalar:
\\begin{equation}
    \\Delta_\\ell = \\frac{\\|h_\\ell(x_{adv})\\| - \\|h_\\ell(x)\\|}{\\|h_\\ell(x)\\|} \\times 100\\%
\\end{equation}
Öznitelik $L_2$ uzaklığı ($\\|h_\\ell(x) - h_\\ell(x_{adv})\\|_2$) mutlak sapmayı nicelemektedir."""

if t.count(ANKOR) != 1:
    print(f"BASARISIZ: ankor {t.count(ANKOR)} kez")
    sys.exit(1)
p.write_text(t.replace(ANKOR, EK, 1), encoding="utf-8")
print("TR yontemine 'Oznitelik Bozunmasi Metrikleri' eklendi")
