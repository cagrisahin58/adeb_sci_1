#!/usr/bin/env python3
"""Hakem turu 3 - OLGUSAL duzeltmeler (Ingilizce).

Her yama imza kontrollu ve YINELENEBILIR: hedef metin yoksa ve yeni metin
zaten varsa "zaten" der, ikisi de yoksa BASARISIZ olur. Kismi yazim olmaz;
tum eslesmeler dogrulandiktan SONRA dosyalar yazilir.

Defter: results/q1_research/HAKEM_TURU3_DEFTER.md bolum C.
"""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")

# (dosya, eski, yeni, etiket)
YAMALAR = [
    # ---- C1: giris govdeyle celisiyor (dordu de null) ----
    ("01_introduction.tex",
     r"on four spatial measures of which three are null",
     r"on all four spatial measures",
     "C1 null sayisi"),

    # ---- C2: her-ikisi-dogru McNemar p siniri tam kumeden odunc ----
    ("04_experiments.tex",
     r"the CNN leads by 13.8 and 10.7 points (McNemar $p<10^{-84}$ in every run).",
     r"the CNN leads by 13.8 and 10.7 points (McNemar $p<10^{-67}$ in every run; "
     r"the bound is computed on this subset and is weaker than the full-test-set "
     r"bound quoted above, which is what the larger denominator buys).",
     "C2 McNemar siniri"),

    # ---- C7: 0.80 bir oran, dogruluk degil ----
    ("04_experiments.tex",
     r"Seed-level variation is small throughout for the adversarially trained pair, "
     r"at most 0.80 points on any reported accuracy, so the ordering",
     r"Seed-level variation is small throughout for the adversarially trained pair, "
     r"at most 0.55 points on any reported accuracy, so the ordering",
     "C7 0.80 -> 0.55"),

    # ---- C6: MI-FGSM butcesi acikca yazilmali ----
    ("04_experiments.tex",
     r"and also under the momentum-based MI-FGSM~\cite{dong2018boosting} "
     r"($19.07\pm0.33$ versus $15.42\pm0.52\%$ target-correct), so the effect",
     r"and also under the momentum-based MI-FGSM~\cite{dong2018boosting} "
     r"($19.07\pm0.33$ versus $15.42\pm0.52\%$ target-correct; this bidirectional "
     r"check uses the attack's own default step of $\alpha=\eps/10$, not the "
     r"$\alpha=2/255$ used elsewhere, which is why its ViT$\rightarrow$CNN figure "
     r"differs slightly from the matched-budget value in Table~\ref{tab:tgr}), "
     r"so the effect",
     "C6 MI-FGSM butcesi"),

    # ---- C3: sekil gondermesi yanlis + C3 fazlaligi kaldirilir ----
    ("04_experiments.tex",
     r"Figure~\ref{fig:feature_degradation} shows the clean and adversarial CLS "
     r"attention for a representative sample together with the per-layer entropy "
     r"curves; the two entropy curves lie on top of each other, which is the "
     r"visual form of the null result reported above.",
     r"In Figure~\ref{fig:feature_degradation} the clean and adversarial entropy "
     r"curves lie on top of each other, which is the visual form of the null "
     r"result reported above.",
     "C3 sekil gondermesi"),

    # ---- C4: uc kat -> dort kat ----
    ("05_discussion.tex",
     r"since the CLS pathway drifts three times as far as the patch-token mean",
     r"since the CLS pathway drifts about four times as far as the patch-token mean",
     "C4 drift orani"),

    # ---- C5 + C8: MI-FGSM tek veri kumesi, temiz aciklik 12,3 ----
    ("05_discussion.tex",
     r"Across four protocols, three training runs, and two attack families "
     r"(PGD-10 and MI-FGSM), adversarial examples crafted on the CNN transfer "
     r"better to the ViT than the reverse \emph{on both CIFAR datasets}. On SVHN, "
     r"where adversarial training under the same recipe leaves the two "
     r"architectures $1.85$ points apart in clean accuracy rather than $11$ or $21$,",
     r"Across four protocols and three training runs, adversarial examples crafted "
     r"on the CNN transfer better to the ViT than the reverse \emph{on both CIFAR "
     r"datasets}, and on CIFAR-10 the direction also holds under a second attack "
     r"family (MI-FGSM). On SVHN, where adversarial training under the same recipe "
     r"leaves the two architectures $1.85$ points apart in clean accuracy rather "
     r"than $12.3$ or $20.7$,",
     "C5+C8 saldiri ailesi ve aciklik"),

    # ---- C9: basarili-kaynak "established" atifsiz ----
    ("03_methodology.tex",
     r"we additionally report two established alternatives: the \emph{both-correct} "
     r"protocol, which conditions on samples that both the source and the target "
     r"classify correctly~\cite{mahmood2021robustness, ravikumar2023trend}, and the "
     r"\emph{successful-source} protocol, which conditions on target-correct samples "
     r"whose attack succeeded on the source in the white-box sense.",
     r"we additionally report two alternatives: the \emph{both-correct} protocol, "
     r"which conditions on samples that both the source and the target classify "
     r"correctly~\cite{mahmood2021robustness, ravikumar2023trend}, and the "
     r"\emph{successful-source} protocol, which conditions on target-correct samples "
     r"whose attack succeeded on the source in the white-box sense. The first is "
     r"established in the cited sense; for the second we know of no single canonical "
     r"reference, and we include it because it is the protocol implied whenever a "
     r"transfer rate is reported over ``successful'' adversarial examples.",
     "C9 basarili-kaynak atfi"),

    # ---- C11, C12: Ingiliz imlasi ----
    ("04_experiments.tex", r"Neighbourhood clustering", r"Neighborhood clustering",
     "C11 imla"),
    ("04_experiments.tex", r"This behaviour is consistent with the mechanism",
     r"This behavior is consistent with the mechanism", "C12 imla"),

    # ---- C13: "the first being" AI kalintisi ----
    ("04_experiments.tex",
     r"Two qualifications belong with this result, the first being that the two "
     r"adversarial bands held with margins of",
     r"Two qualifications belong with this result. The two adversarial bands held "
     r"with margins of",
     "C13 uslup"),
]


def uygula(yamalar, kok):
    dosyalar = {}
    hata = []
    atlanan = []
    for ad, eski, yeni, etiket in yamalar:
        p = kok / ad
        t = dosyalar.get(ad) or p.read_text(encoding="utf-8")
        if eski in t:
            t = t.replace(eski, yeni, 1)
            dosyalar[ad] = t
            print(f"  [+] {etiket}  ({ad})")
        elif yeni in t:
            atlanan.append(etiket)
            dosyalar.setdefault(ad, t)
        else:
            hata.append(f"{etiket} ({ad}): ne eski ne yeni metin bulundu")
            dosyalar.setdefault(ad, t)
    if hata:
        print("\nBASARISIZ - hicbir dosya yazilmadi:")
        for h in hata:
            print("   ", h)
        return False
    for ad, t in dosyalar.items():
        (kok / ad).write_text(t, encoding="utf-8")
    if atlanan:
        print(f"  [=] zaten uygulanmis: {', '.join(atlanan)}")
    print(f"\n{len(dosyalar)} dosya yazildi.")
    return True


# Diger _t3_* betikleri `uygula`yi buradan ice aktarir; ice aktarma
# YAN ETKISIZ olmali, yoksa sonraki gecislerin degistirdigi metinler
# uzerinde bu yamalar yeniden aranir ve yanlis yere BASARISIZ olur.
if __name__ == "__main__":
    if not uygula(YAMALAR, ROOT):
        sys.exit(1)
