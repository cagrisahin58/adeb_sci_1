#!/usr/bin/env python3
"""B2 metin -- 7/n: iki-kol paragrafi (A kolu yeniden kosuldu).

Degisen sayilar (results/q1/e3_iki_kol_fit.json, kaynak e3_akolu_v2):
  A dort protokol   +0,293 -> +0,273  GA [+0,219; +0,371]
  A uc protokol     +0,672 -> +0,673  GA [+0,602; +0,727]   (pratikte AYNI)
  B dort protokol   -0,567 -> -0,528  GA [-0,664; -0,418]
  B ana cift        +0,387 -> -0,100  GA [-0,464; +0,092]   <-- ISARET DEGISTI
  kaldirac 4prot    +0,220..+0,524 -> +0,201..+0,492
  kaldirac 3prot     0,659..0,672  ->  0,661..0,673

ANLATI DEGISIYOR. Eski metin "uyusmazlik bir KONTROL etkisi degil BILESIM
etkisidir" diyor ve gerekce olarak gozlemsel kolun ayni mimari ciftine
kisitlandiginda kontrollu kolla UYUSTUGUNU gosteriyordu. Artik uyusmuyor:
kisitlanmis egim -0,100 ve GA'si kontrollu kolunkiyle ORTUSMUYOR. Bilesim
farkin BUYUK KISMINI aciklamaktadir ama KAPATMAMAKTADIR. Yazilan budur.
Uc protokollu egim uc uydurmanin ucunde de pozitif ve ortusuyor; mekanizma
iddiasinin dayandigi nicelik zaten odur.
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


EN_E = ("Excluding the successful-source protocol, the two arms give slopes of "
        "$+0.672$ (CI $[+0.601, +0.726]$) and $+0.431$ (CI $[+0.333, +0.633]$): "
        "same sign, overlapping intervals. Including it, the controlled arm gives "
        "$+0.293$ (CI $[+0.206, +0.489]$) while the observational arm gives "
        "$-0.567$ (CI $[-0.757, -0.451]$). That disagreement is a composition "
        "effect, not a control effect: the controlled arm contains no WideResNet, "
        "and restricting the observational arm to the same architecture pair yields "
        "$+0.387$ (CI $[+0.075, +0.576]$), which agrees with the controlled arm in "
        "both sign and interval. Two limits belong with this: the observational "
        "arm's negative slope is fitted across an unmeasured gap of $7.2$ points on "
        "the $x$ axis, so it compares two separated clusters rather than tracing a "
        "trend; and the controlled arm's slope survives dropping early checkpoints "
        "($+0.220$ to $+0.524$ across thresholds), with the three-protocol slope the "
        "most stable quantity of all ($0.659$ to $0.672$).")

EN_Y = ("Excluding the successful-source protocol, the two arms give slopes of "
        "$+0.673$ (CI $[+0.602, +0.727]$) and $+0.431$ (CI $[+0.333, +0.633]$): "
        "same sign, overlapping intervals. Including it, the controlled arm gives "
        "$+0.273$ (CI $[+0.219, +0.371]$) while the observational arm gives "
        "$-0.528$ (CI $[-0.664, -0.418]$). Composition accounts for most of that "
        "disagreement without closing it. The controlled arm contains no "
        "WideResNet, and restricting the observational arm to the same architecture "
        "pair moves its four-protocol slope from $-0.528$ to $-0.100$ (CI "
        "$[-0.464, +0.092]$), an interval that includes zero but still does not "
        "overlap the controlled arm's. The two arms therefore agree on the "
        "three-protocol slope and do not agree on the four-protocol one, which is "
        "the ordering the mechanism claim rests on. Two limits belong with this: "
        "the observational arm's negative slope is fitted across an unmeasured gap "
        "of $7.2$ points on the $x$ axis, so it compares two separated clusters "
        "rather than tracing a trend; and the controlled arm's slope survives "
        "dropping early checkpoints ($+0.201$ to $+0.492$ across thresholds), with "
        "the three-protocol slope the most stable quantity of all ($0.661$ to "
        "$0.673$).")

yama("paper/manuscript/sections/04_experiments.tex", [(EN_E, EN_Y, "EN iki kol")])

TR_E = ("Başarılı kaynak protokolü dışarıda bırakıldığında iki kol $+0{,}672$ "
        "(GA $[+0{,}601;\\ +0{,}726]$) ve $+0{,}431$ (GA $[+0{,}333;\\ +0{,}633]$) "
        "eğimleri vermektedir: işaret aynı, aralıklar örtüşüyor. Dahil edildiğinde "
        "kontrollü kol $+0{,}293$ (GA $[+0{,}206;\\ +0{,}489]$), gözlemsel kol "
        "$-0{,}567$ (GA $[-0{,}757;\\ -0{,}451]$) vermektedir. Bu uyuşmazlık bir "
        "kontrol etkisi değil bir bileşim etkisidir: kontrollü kol WideResNet "
        "içermez ve gözlemsel kol aynı mimari çiftine kısıtlandığında $+0{,}387$ "
        "(GA $[+0{,}075;\\ +0{,}576]$) çıkmakta, yani kontrollü kolla hem işaret hem "
        "aralık bakımından uyuşmaktadır. Bununla birlikte iki sınır yazılmalıdır: "
        "gözlemsel kolun negatif eğimi $x$ ekseninde $7{,}2$ puanlık ölçülmemiş bir "
        "boşluğun üzerinden uydurulmuştur, dolayısıyla bir eğilimi izlemek yerine "
        "birbirinden ayrık iki kümeyi karşılaştırmaktadır; kontrollü kolun eğimi ise "
        "erken kontrol noktaları çıkarıldığında ayakta kalmaktadır (eşiklere göre "
        "$+0{,}220$ ile $+0{,}524$ arasında) ve en kararlı nicelik üç protokollü "
        "eğimdir ($0{,}659$ ile $0{,}672$).")

TR_Y = ("Başarılı kaynak protokolü dışarıda bırakıldığında iki kol $+0{,}673$ "
        "(GA $[+0{,}602;\\ +0{,}727]$) ve $+0{,}431$ (GA $[+0{,}333;\\ +0{,}633]$) "
        "eğimleri vermektedir: işaret aynı, aralıklar örtüşüyor. Dahil edildiğinde "
        "kontrollü kol $+0{,}273$ (GA $[+0{,}219;\\ +0{,}371]$), gözlemsel kol "
        "$-0{,}528$ (GA $[-0{,}664;\\ -0{,}418]$) vermektedir. Bileşim, bu "
        "uyuşmazlığın büyük kısmını açıklamakta ama onu kapatmamaktadır. Kontrollü "
        "kol WideResNet içermez; gözlemsel kol aynı mimari çiftine kısıtlandığında "
        "dört protokollü eğimi $-0{,}528$'den $-0{,}100$'e gelmekte (GA "
        "$[-0{,}464;\\ +0{,}092]$), yani aralık sıfırı içermekte ama kontrollü kolun "
        "aralığıyla hâlâ örtüşmemektedir. Dolayısıyla iki kol üç protokollü eğimde "
        "uyuşmakta, dört protokollüde uyuşmamaktadır; mekanizma iddiasının "
        "dayandığı sıralama da budur. Bununla birlikte iki sınır yazılmalıdır: "
        "gözlemsel kolun negatif eğimi $x$ ekseninde $7{,}2$ puanlık ölçülmemiş bir "
        "boşluğun üzerinden uydurulmuştur, dolayısıyla bir eğilimi izlemek yerine "
        "birbirinden ayrık iki kümeyi karşılaştırmaktadır; kontrollü kolun eğimi ise "
        "erken kontrol noktaları çıkarıldığında ayakta kalmaktadır (eşiklere göre "
        "$+0{,}201$ ile $+0{,}492$ arasında) ve en kararlı nicelik üç protokollü "
        "eğimdir ($0{,}661$ ile $0{,}673$).")

yama("paper/manuscript_tr/sections/04_deneyler.tex", [(TR_E, TR_Y, "TR iki kol")])

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("yazilan:", *yazilan, sep="\n  ")
