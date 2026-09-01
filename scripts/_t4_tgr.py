#!/usr/bin/env python3
"""1.3: TGR uyarlamasinin sapmalari ACIKCA beyan edilir.

Kodda dogrulanan (experiments/c1_c2_tgr.py):
  - TEK TIP gamma = 0.5, uc yolun (dikkat, QKV, MLP) hepsinde ayni
  - her (ornek, kanal) icin jetonlar arasinda TEK maksimum ve TEK minimum
    girdi sifirlaniyor (satir/sutun degil, tek hucre)
Metin gamma'yi ve butceyi zaten beyan ediyordu; sifirlama semasini ve
"negatif sonuc UYARLAMAYI baglar" kaydini beyan etmiyordu.

DIKKAT: ozgun TGR'nin yol-basina katsayilarini BIRINCI ELDEN dogrulamadim;
bu yuzden metin ozgun yonteme dair sayisal bir iddia KURMUYOR, yalnizca
kendi uygulamamizi tarif edip sonucun kapsamini siniriyor.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

EN = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")
TR = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")

if not uygula([
    ("03_methodology.tex",
     r"Our implementation adapts the method to our CIFAR-10 ViT wrapper and to "
     r"the budget used throughout this paper ($\eps=8/255$, $\alpha=2/255$, 10 "
     r"steps, momentum 1.0) instead of the original ImageNet defaults; we "
     r"therefore report it as an adaptation.",
     r"Our implementation adapts the method to our CIFAR-10 ViT wrapper and to "
     r"the budget used throughout this paper ($\eps=8/255$, $\alpha=2/255$, 10 "
     r"steps, momentum 1.0) instead of the original ImageNet defaults. Two "
     r"further details of our version should be stated, because the result we "
     r"report from it is negative. We apply a single $\gamma=0.5$ to all three "
     r"paths rather than tuning it per path, and we zero one maximum and one "
     r"minimum entry per (sample, channel) across tokens rather than whole "
     r"token rows and columns. We did not replicate the published "
     r"regularization scheme exactly, so the negative result below bounds this "
     r"adaptation and not the method as published; a replication with the "
     r"original scheme would be needed to extend it.",
     "1.3 EN TGR sapma beyani"),
], EN):
    sys.exit(1)

if not uygula([
    ("03_yontem.tex",
     r"Gerçeklememiz yöntemi CIFAR-10 ViT sarmalayıcımıza ve bu makale boyunca "
     r"kullanılan bütçeye ($\eps=8/255$, $\alpha=2/255$, 10 adım, momentum "
     r"1,0) uyarlamaktadır; özgün ImageNet varsayılanları kullanılmamıştır ve "
     r"bu yüzden bir uyarlama olarak raporlanmaktadır.",
     r"Gerçeklememiz yöntemi CIFAR-10 ViT sarmalayıcımıza ve bu makale boyunca "
     r"kullanılan bütçeye ($\eps=8/255$, $\alpha=2/255$, 10 adım, momentum "
     r"1,0) uyarlamaktadır; özgün ImageNet varsayılanları kullanılmamıştır. "
     r"Sürümümüzün iki ayrıntısı daha "
     r"yazılmalıdır, çünkü ondan bildirdiğimiz sonuç negatiftir. Üç yolun "
     r"hepsine yol-başına ayarlamak yerine tek bir $\gamma=0{,}5$ uyguluyor ve "
     r"jetonlar arasında her (örnek, kanal) için tek bir maksimum ile tek bir "
     r"minimum girdiyi sıfırlıyoruz; bütün jeton satır ve sütunlarını değil. "
     r"Yayımlanmış düzenlileştirme şemasını birebir yeniden gerçeklemedik, "
     r"dolayısıyla aşağıdaki negatif sonuç bu uyarlamayı bağlar, yayımlanmış "
     r"hâliyle yöntemi değil; onu genişletmek için özgün şemayla bir yineleme "
     r"gerekir.",
     "1.3 TR TGR sapma beyani"),
], TR):
    sys.exit(1)
