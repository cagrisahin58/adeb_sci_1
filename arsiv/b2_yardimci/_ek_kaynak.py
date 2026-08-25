#!/usr/bin/env python3
"""Dogrulanan uc kaynagi kunyeye ekler ve iki dilde metne yerlestirir.

Kaynaklar 2026-08-24 hakem raporunda onerilmis ama kunye ayrintilari
dogrulanamadigi icin EKLENMEMISTI. 2026-08-25'te arXiv/DBLP uzerinden
dogrulandi:

  li2023tabench   NeurIPS 2023, arXiv:2311.01323
  waseda2023closer WACV 2023, arXiv:2112.14337
  yu2025reliable  IEEE SaTML 2025, s. 797-810, arXiv:2306.08565
"""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
hata, yazilan = [], []


def yama(rel, ciftler):
    p = ROOT / rel
    t = orig = p.read_text(encoding="utf-8")
    for eski, yeni, ad in ciftler:
        if t.count(eski) != 1:
            hata.append(f"{rel} :: {ad}: {t.count(eski)} eslesme")
            return
        t = t.replace(eski, yeni, 1)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        yazilan.append(rel)


# ------------------------------------------------------------------- kunye
BIB_YENI = """@inproceedings{li2023tabench,
  author    = {Li, Qizhang and Guo, Yiwen and Zuo, Wangmeng and Chen, Hao},
  title     = {Towards Evaluating Transfer-based Attacks Systematically, Practically, and Fairly},
  booktitle = {Advances in Neural Information Processing Systems},
  volume    = {36},
  year      = {2023}
}

@inproceedings{waseda2023closer,
  author    = {Waseda, Futa and Nishikawa, Sosuke and Le, Trung-Nghia and Nguyen, Huy H. and Echizen, Isao},
  title     = {Closer Look at the Transferability of Adversarial Examples: How They Fool Different Models Differently},
  booktitle = {IEEE/CVF Winter Conference on Applications of Computer Vision},
  pages     = {1360--1368},
  year      = {2023}
}

@inproceedings{yu2025reliable,
  author    = {Yu, Wenqian and Gu, Jindong and Li, Zhijiang and Torr, Philip},
  title     = {Reliable Evaluation of Adversarial Transferability},
  booktitle = {IEEE Conference on Secure and Trustworthy Machine Learning (SaTML)},
  pages     = {797--810},
  year      = {2025}
}

@article{zhao2025revisiting,"""

yama("paper/manuscript/references.bib",
     [("@article{zhao2025revisiting,", BIB_YENI, "uc kunye")])

# ------------------------------------------------------------- Ingilizce metin
EN_ESKI = ("recent evaluation guidelines make such protocol choices explicit~"
           "\\cite{zhao2025revisiting}.")
EN_YENI = (
    "recent evaluation guidelines make such protocol choices explicit~"
    "\\cite{zhao2025revisiting}. Two recent benchmarks move in the same direction: "
    "TA-Bench~\\cite{li2023tabench} standardizes the comparison of more than thirty "
    "transfer attacks over a common pool of substitute and victim models, and Yu et "
    "al.~\\cite{yu2025reliable} report that transferability is systematically "
    "overestimated when it is measured across a single architecture family and "
    "propose three evaluation protocols in response. Both hold the scoring rule fixed "
    "and vary the attack and the model pool. We do the opposite: the models, the data "
    "and the attack budget are fixed, and only the scoring rule changes, which "
    "isolates the contribution of the protocol itself and makes it possible to state "
    "the arithmetic relation between the resulting estimates.")

EN2_ESKI = ("Understanding these transfer patterns is crucial for developing robust "
            "ensemble systems and evaluating real-world attack scenarios.")
EN2_YENI = ("Waseda et al.~\\cite{waseda2023closer} separate transfer outcomes further, "
            "by whether the target reproduces the source's exact error or fails in a "
            "different way, and report that both occur even between closely related "
            "models. Understanding these transfer patterns is crucial for developing "
            "robust ensemble systems and evaluating real-world attack scenarios.")

yama("paper/manuscript/sections/02_related_work.tex",
     [(EN_ESKI, EN_YENI, "EN protokol kiyaslamalari"),
      (EN2_ESKI, EN2_YENI, "EN waseda")])

# ---------------------------------------------------------------- Turkce metin
TR_ESKI = ("son degerlendirme kilavuzlari bu protokol secimlerini acikca ortaya "
           "koymaktadir~\\cite{zhao2025revisiting}.")
TR_YENI = (
    "son degerlendirme kilavuzlari bu protokol secimlerini acikca ortaya "
    "koymaktadir~\\cite{zhao2025revisiting}. Yakin tarihli iki kiyaslama da ayni "
    "yonde ilerlemektedir: TA-Bench~\\cite{li2023tabench} otuzu askin transfer "
    "saldirisini ortak bir vekil ve kurban model havuzu uzerinde standartlastirmakta, "
    "Yu ve ark.~\\cite{yu2025reliable} ise transfer edilebilirligin tek bir mimari "
    "ailesi icinde olculdugunde dizgesel olarak abartildigini bildirmekte ve buna "
    "karsilik uc degerlendirme protokolu onermektedir. Her ikisi de puanlama kuralini "
    "sabit tutup saldiriyi ve model havuzunu degistirmektedir. Biz bunun tersini "
    "yapiyoruz: modeller, veri ve saldiri butcesi sabittir, yalnizca puanlama kurali "
    "degismektedir; bu da protokolun kendi katkisini yalitmakta ve ortaya cikan "
    "kestirimler arasindaki aritmetik bagintiyi yazmayi mumkun kilmaktadir.")

TR2_ESKI = ("Bu transfer oruntulerini anlamak, gurbuz topluluk sistemleri gelistirmek "
            "ve gercek dunya saldiri senaryolarini degerlendirmek icin kritiktir.")
TR2_YENI = ("Waseda ve ark.~\\cite{waseda2023closer} transfer sonuclarini bir adim daha "
            "ayirmakta, hedefin kaynagin tam olarak ayni hatasini tekrarlayip "
            "tekrarlamadigina gore siniflandirmakta ve her iki durumun birbirine yakin "
            "modeller arasinda bile gorulduğunu bildirmektedir. Bu transfer oruntulerini "
            "anlamak, gurbuz topluluk sistemleri gelistirmek ve gercek dunya saldiri "
            "senaryolarini degerlendirmek icin kritiktir.")

yama("paper/manuscript_tr/sections/02_ilgili_calismalar.tex",
     [(TR_ESKI, TR_YENI, "TR protokol kiyaslamalari"),
      (TR2_ESKI, TR2_YENI, "TR waseda")])

if hata:
    print("BASARISIZ -- kismi yazma olabilir:", *hata, sep="\n  ")
    sys.exit(1)
print("yazilan:", *yazilan, sep="\n  ")
