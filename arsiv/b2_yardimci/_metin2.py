#!/usr/bin/env python3
"""B2 metin guncellemesi -- 2/n: iki-surucu paragrafi (B kolu) + SVHN duyarliligi."""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
hata, yazilan = [], []


def yama(rel, ciftler, imza):
    p = ROOT / rel
    t = orig = p.read_text(encoding="utf-8")
    if imza in t:
        print(f"  atlandi: {rel}")
        return
    for eski, yeni, ad in ciftler:
        n = t.count(eski)
        if n != 1:
            hata.append(f"{rel} :: {ad}: {n} eslesme")
            return
        t = t.replace(eski, yeni, 1)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        yazilan.append(rel)


# =============================== INGILIZCE ===============================
EN_EGIM_E = "(slope $-0.567$, cluster-bootstrap CI $[-0.757, -0.451]$)"
EN_EGIM_Y = "(slope $-0.528$, cluster-bootstrap CI $[-0.664, -0.418]$)"

EN_UC_E = ("The successful-source rate is the smallest of the four in $12$ of $18$ "
           "pairs and the largest in $2$ more, so it is the extreme in $14$, and the "
           "widest protocol pair is always target-correct against successful-source "
           "($19.68$ points on average).")
EN_UC_Y = ("The successful-source rate is the smallest of the four in $12$ of $18$ "
           "pairs and the largest in $4$ more, so it is the extreme in $16$, and the "
           "widest protocol pair is always target-correct against successful-source "
           "($23.77$ points on average).")

EN_KUYRUK_E = ("so it contributes a second and partly opposing term.")
EN_KUYRUK_Y = (
    "so it contributes a second and partly opposing term. The pool for this fit is "
    "the one fixed in the pre-registration, which assigns the SVHN pair to an "
    "independent consistency check rather than to the fitted points. Adding its two "
    "directions, whose clean-error gap of under two points falls in an otherwise "
    "unoccupied band of the $x$ axis, moves the four-protocol slope to $-0.133$ with "
    "a cluster-bootstrap CI of $[-0.570, +0.469]$ that includes zero, while the "
    "three-protocol slope keeps both its sign and its interval. We report the "
    "sensitivity rather than absorb it, because it shows how thinly the "
    "four-protocol slope is supported.")

yama("paper/manuscript/sections/04_experiments.tex",
     [(EN_EGIM_E, EN_EGIM_Y, "EN egim"),
      (EN_UC_E, EN_UC_Y, "EN uc sayilari"),
      (EN_KUYRUK_E, EN_KUYRUK_Y, "EN SVHN duyarliligi")],
     "The pool for this fit is the one fixed in the pre-registration")

# ================================ TURKCE =================================
TR_EGIM_E = "(eğim $-0{,}567$, küme bootstrap GA $[-0{,}757;\\ -0{,}451]$)"
TR_EGIM_Y = "(eğim $-0{,}528$, küme bootstrap GA $[-0{,}664;\\ -0{,}418]$)"

TR_UC_E = ("Başarılı kaynak oranı $18$ çiftin $12$'sinde dördün en küçüğü, $2$ çiftte "
           "daha en büyüğüdür; yani $14$ çiftte uçtur ve en geniş protokol çifti her "
           "zaman hedef doğru ile başarılı kaynak arasındadır (ortalama $19{,}68$ puan).")
TR_UC_Y = ("Başarılı kaynak oranı $18$ çiftin $12$'sinde dördün en küçüğü, $4$ çiftte "
           "daha en büyüğüdür; yani $16$ çiftte uçtur ve en geniş protokol çifti her "
           "zaman hedef doğru ile başarılı kaynak arasındadır (ortalama $23{,}77$ puan).")

TR_KUYRUK_E = ("ve dolayısıyla ikinci, kısmen ters yönlü bir terim katmaktadır.")
TR_KUYRUK_Y = (
    "ve dolayısıyla ikinci, kısmen ters yönlü bir terim katmaktadır. Bu uydurmanın "
    "havuzu ön kayıtta sabitlenen havuzdur; ön kayıt SVHN çiftini uydurulan noktalara "
    "değil bağımsız bir tutarlılık kontrolüne atamaktadır. Temiz hata farkı iki puanın "
    "altında kalan ve $x$ ekseninin başka türlü boş olan bir bandına düşen iki SVHN "
    "yönü eklendiğinde dört protokollü eğim $-0{,}133$'e gitmekte ve küme bootstrap "
    "güven aralığı $[-0{,}570;\\ +0{,}469]$ sıfırı içermektedir; üç protokollü eğim ise "
    "hem işaretini hem aralığını korumaktadır. Bu duyarlılığı içeri almak yerine "
    "raporluyoruz, çünkü dört protokollü eğimin ne kadar ince bir dayanağı olduğunu "
    "göstermektedir.")

yama("paper/manuscript_tr/sections/04_deneyler.tex",
     [(TR_EGIM_E, TR_EGIM_Y, "TR egim"),
      (TR_UC_E, TR_UC_Y, "TR uc sayilari"),
      (TR_KUYRUK_E, TR_KUYRUK_Y, "TR SVHN duyarliligi")],
     "Bu uydurmanın havuzu ön kayıtta sabitlenen havuzdur")

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("yazilan:", *yazilan, sep="\n  ")
