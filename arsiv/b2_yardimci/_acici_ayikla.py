#!/usr/bin/env python3
"""PARAGRAF BASI KISA ACICILARI ayiklar (kullanici talimati).

Yontem: kisa acici cumle, kendisinden sonraki cumleye KATILIR. Boylece
paragraf mini-baslikla degil icerikle baslar. Hicbir sayi, atif ya da
\\ref degismez; paragraf SAYISI da degismez, yani EN/TR ayna korunur.
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


# =============================== INGILIZCE ===============================
yama("paper/manuscript/sections/01_introduction.tex", [
    ("The literature answers this question inconsistently. Bai et al.",
     "The literature answers this question inconsistently: Bai et al.", "EN 1"),
    ("This paper makes a different observation. Even when the models, the data, "
     "the threat model, and the attack budget are all held fixed, the conclusion "
     "still depends on",
     "This paper makes a different observation, which is that even when the "
     "models, the data, the threat model, and the attack budget are all held "
     "fixed, the conclusion still depends on", "EN 2"),
    ("Our contributions are as follows. We first quantify protocol sensitivity. "
     "On identical models and data,",
     "Our first contribution is to quantify protocol sensitivity. On identical "
     "models and data,", "EN 3"),
    ("We report three negative results. Scale-invariant sparsity differences do "
     "not correspond to spatial localization differences,",
     "Three of the results we report are negative: scale-invariant sparsity "
     "differences do not correspond to spatial localization differences,",
     "EN 4"),
])

yama("paper/manuscript/sections/04_experiments.tex", [
    ("What is stable is the direction. CNN-crafted examples transfer better",
     "What is stable is the direction: CNN-crafted examples transfer better",
     "EN 5"),
    ("The two arms agree on three protocols. We calibrate the protocol spread "
     "against the clean-error gap in two ways that fail differently.",
     "We calibrate the protocol spread against the clean-error gap in two ways "
     "that fail differently, and they agree on three of the four protocols.",
     "EN 6"),
    ("One registered endpoint was missed. We predicted clean accuracy in the",
     "One registered endpoint was missed: we predicted clean accuracy in the",
     "EN 7"),
    ("Class composition does not manufacture the asymmetry. Because conditioning "
     "changes which samples enter the denominator, it also changes the class mix, "
     "and an asymmetry could in principle be a composition artifact.",
     "Because conditioning changes which samples enter the denominator, it also "
     "changes the class mix, so an asymmetry could in principle be a composition "
     "artifact; it is not.", "EN 8"),
    ("Two qualifications belong with this result. First, the two adversarial "
     "bands held with margins of",
     "Two qualifications belong with this result, the first being that the two "
     "adversarial bands held with margins of", "EN 9"),
    ("All three registered predictions hold. The protocol spread is",
     "All three registered predictions hold: the protocol spread is", "EN 10"),
    ("Two results follow. First, the two architectures differ less in",
     "Two results follow, the first being that the two architectures differ less "
     "in", "EN 11"),
    ("We state the conclusion narrowly. Our setting differs from the one TGR was "
     "designed for",
     "We state the conclusion narrowly, because our setting differs from the one "
     "TGR was designed for", "EN 12"),
    ("A counterweight belongs immediately next to it. On CIFAR-100 the epoch",
     "A counterweight belongs immediately next to it: on CIFAR-100 the epoch",
     "EN 13"),
])

yama("paper/manuscript/sections/05_discussion.tex", [
    ("The central result is an ordering of dispersions. Measured on the transfer "
     "asymmetry itself,",
     "The central result is an ordering of dispersions: measured on the transfer "
     "asymmetry itself,", "EN 14"),
    ("Sparsity is not spatial locality. Adversarially trained CNN gradients "
     "concentrate",
     "Sparsity is not spatial locality: adversarially trained CNN gradients "
     "concentrate", "EN 15"),
])

yama("paper/manuscript/sections/06_conclusion.tex", [
    ("The measurement dominates. On identical adversarially trained ResNet-18",
     "The measurement dominates: on identical adversarially trained ResNet-18",
     "EN 16"),
])

# ================================ TURKCE =================================
yama("paper/manuscript_tr/sections/01_giris.tex", [
    ("Literatür bu soruya tutarsız yanıtlar vermektedir. Bai vd.",
     "Literatür bu soruya tutarsız yanıtlar vermektedir: Bai vd.", "TR 1"),
    ("Bu makale farklı bir gözlemde bulunmaktadır. Modeller, veri, tehdit modeli "
     "ve saldırı bütçesinin tamamı sabit tutulduğunda bile sonuç,",
     "Bu makale farklı bir gözlemde bulunmaktadır: modeller, veri, tehdit modeli "
     "ve saldırı bütçesinin tamamı sabit tutulduğunda bile sonuç,", "TR 2"),
    ("Katkılarımız şunlardır. Önce protokol duyarlılığını niceliyoruz. Aynı "
     "modeller ve aynı veri üzerinde,",
     "İlk katkımız protokol duyarlılığını nicelemektir. Aynı modeller ve aynı "
     "veri üzerinde,", "TR 3"),
    ("Üç negatif sonuç raporluyoruz. Ölçekten bağımsız seyreklik farkları",
     "Raporladığımız sonuçların üçü negatiftir: ölçekten bağımsız seyreklik "
     "farkları", "TR 4"),
])

yama("paper/manuscript_tr/sections/04_deneyler.tex", [
    ("Kararlı olan yöndür. CNN'de üretilen örnekler",
     "Kararlı olan yöndür: CNN'de üretilen örnekler", "TR 5"),
    ("İki kol üç protokolde uyuşmaktadır. Protokol yayılımını temiz hata farkına "
     "karşı, farklı biçimlerde hata veren iki yolla kalibre ediyoruz.",
     "Protokol yayılımını temiz hata farkına karşı, farklı biçimlerde hata veren "
     "iki yolla kalibre ediyoruz; iki yol dört protokolün üçünde uyuşmaktadır.",
     "TR 6"),
    ("Kayıtlı uç noktalardan biri tutmamıştır. Çekişmeli eğitilmiş ViT için",
     "Kayıtlı uç noktalardan biri tutmamıştır: çekişmeli eğitilmiş ViT için",
     "TR 7"),
    ("Sınıf bileşimi asimetriyi üretmemektedir. Koşullama, paydaya hangi "
     "örneklerin gireceğini değiştirdiği için sınıf karışımını da değiştirir; "
     "ilkece bir asimetri bileşim artefaktı olabilir.",
     "Koşullama, paydaya hangi örneklerin gireceğini değiştirdiği için sınıf "
     "karışımını da değiştirir; dolayısıyla bir asimetri ilkece bileşim artefaktı "
     "olabilir, ama değildir.", "TR 8"),
    ("Bu sonuçla birlikte okunması gereken iki niteleme vardır. Birincisi, iki "
     "çekişmeli band",
     "Bu sonuçla birlikte okunması gereken iki niteleme vardır; birincisi, iki "
     "çekişmeli bandın", "TR 9"),
    ("Kayıtlı üç ön kestirimin üçü de tutmaktadır. Protokol yayılımı",
     "Kayıtlı üç ön kestirimin üçü de tutmaktadır: protokol yayılımı", "TR 10"),
    ("Bundan iki sonuç çıkmaktadır. Birincisi, iki mimari hasarın",
     "Bundan çıkan iki sonuçtan birincisi, iki mimarinin hasarın", "TR 11"),
    ("Sonucu dar tutuyoruz. Kurulumumuz, TGR'nin tasarlandığı kurulumdan",
     "Sonucu dar tutuyoruz, çünkü kurulumumuz TGR'nin tasarlandığı kurulumdan",
     "TR 12"),
    ("Hemen yanına bir karşı ağırlık konmalıdır. CIFAR-100'de kendi",
     "Hemen yanına bir karşı ağırlık konmalıdır: CIFAR-100'de kendi", "TR 13"),
])

yama("paper/manuscript_tr/sections/05_tartisma.tex", [
    ("Merkezî sonuç bir yayılım sıralamasıdır. Transfer asimetrisinin kendisi",
     "Merkezî sonuç bir yayılım sıralamasıdır: transfer asimetrisinin kendisi",
     "TR 14"),
    ("Seyreklik mekânsal lokalite değildir. Çekişmeli eğitilmiş CNN gradyanları",
     "Seyreklik mekânsal lokalite değildir: çekişmeli eğitilmiş CNN gradyanları",
     "TR 15"),
])

yama("paper/manuscript_tr/sections/06_sonuc.tex", [
    ("Ölçüm hükmediyor. Özdeş çekişmeli eğitilmiş ResNet-18",
     "Ölçüm hükmediyor: özdeş çekişmeli eğitilmiş ResNet-18", "TR 16"),
])

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("yazilan:", *yazilan, sep="\n  ")
