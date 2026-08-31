#!/usr/bin/env python3
"""TUR 4 FAZ 2 - A bolumu (Ingilizce).

2.1 Kol karsilastirmasi GERI CEKILEN havuza dayaniyordu. On kayitli
    havuzda B kolunun araligi A kolununkini KAPSIYOR; "dort protokolde
    uyusmuyorlar" hukmu orada yanlis (olcum: scripts/_t4_kol_dogrula.py).
1.2 ViT derinlik profili MLP alt-blogunda olculmustu; siniflandirici son
    BLOK cikisinin CLS'ini okur. Kod duzeltildi, analiz yeniden kosuldu
    (scripts/_t4_c4_yeniden.sh). Yeni seri Tablo VII'ye ve anlatiya girer.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

S = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")

YAMALAR = [
    # ================= 2.1: kol karsilastirmasi =================
    ("04_experiments.tex",
     r"Excluding the successful-source protocol, the two arms give slopes of "
     r"$+0.673$ (CI $[+0.602, +0.727]$) and $+0.431$ (CI $[+0.333, +0.633]$): "
     r"same sign, overlapping intervals. Including it, the controlled arm gives "
     r"$+0.273$ (CI $[+0.219, +0.371]$) while the observational arm gives "
     r"$-0.528$ (CI $[-0.664, -0.418]$). Composition accounts for most of that "
     r"disagreement without closing it. The controlled arm contains no "
     r"WideResNet, and restricting the observational arm to the same "
     r"architecture pair moves its four-protocol slope from $-0.528$ to "
     r"$-0.100$ (CI $[-0.464, +0.092]$), an interval that includes zero but "
     r"still does not overlap the controlled arm's. The two arms therefore "
     r"agree on the three-protocol slope and do not agree on the four-protocol "
     r"one, which is the ordering the mechanism claim rests on.",

     r"Excluding the successful-source protocol, the two arms agree: $+0.673$ "
     r"(CI $[+0.602, +0.727]$) in the controlled arm against $+0.470$ (CI "
     r"$[+0.361, +0.665]$) in the observational arm on the pre-registered pool, "
     r"same sign and overlapping intervals. The four-protocol slope, which we "
     r"withdrew above, supports no comparison either way: on the pre-registered "
     r"pool the observational interval $[-0.570, +0.469]$ contains the "
     r"controlled arm's $[+0.219, +0.371]$ entirely, so the arms neither agree "
     r"nor disagree there in any informative sense. We record the post-hoc "
     r"contrast only to show what the pool choice does. Dropping SVHN moves the "
     r"observational four-protocol slope to $-0.528$ (CI $[-0.664, -0.418]$), "
     r"which does not overlap the controlled arm, and restricting that pool to "
     r"the matched architecture pair moves it to $-0.100$ (CI $[-0.464, "
     r"+0.092]$); a quantity this sensitive to which pairs enter the fit is not "
     r"one a mechanism claim can rest on. The agreement that does carry the "
     r"claim is the three-protocol one, and it holds in every pool we fit.",
     "2.1 kol karsilastirmasi"),

    # ================= 1.2: derinlik anlatisi =================
    ("04_experiments.tex",
     r"In the ViT the drift is gradual and shallow: similarity declines "
     r"steadily to a minimum around blocks 8 to 10 and then recovers toward the "
     r"output, while feature norms stay within 0.7\% of their clean values "
     r"throughout, so the perturbation rotates the representation instead of "
     r"rescaling it.",
     r"In the ViT the drift is gradual and shallow: similarity declines "
     r"monotonically to a minimum at block 11 and recovers slightly at the "
     r"output, while feature norms stay within $0.45\%$ of their clean values "
     r"throughout, so the perturbation rotates the representation instead of "
     r"rescaling it.",
     "1.2 derinlik anlatisi"),

    ("04_experiments.tex",
     r"Second, the aggregation choice changes the measured profile "
     r"substantially. At their respective minima the CLS pathway drifts about "
     r"four times as far as the patch-token mean ($0.9343$ versus $0.9840$, a "
     r"ratio of $4.1$ in $1-\cos$), and the two summaries even place the "
     r"minimum at different depths (block 10 versus block 8). Since the CLS "
     r"token is what the classifier reads, this is not a nuisance but a result: "
     r"the perturbation concentrates on the classification pathway while the "
     r"average patch representation is comparatively preserved. It also means "
     r"that layer-wise drift curves from different papers are not directly "
     r"comparable unless the aggregation is stated.",

     r"Second, the aggregation choice changes the measured profile "
     r"substantially. At their respective minima the CLS pathway drifts about "
     r"three times as far as the patch-token mean ($0.9604$ versus $0.9870$, a "
     r"ratio of $3.05$ in $1-\cos$), and the two summaries place the minimum at "
     r"different depths (block 11 versus block 9). Since the CLS token at the "
     r"block output is what the classifier reads, this is not a nuisance but a "
     r"result: the perturbation concentrates on the classification pathway "
     r"while the average patch representation is comparatively preserved. The "
     r"tensor the summary is taken from matters as much as the aggregation. "
     r"Read at the MLP sub-block output instead of the residual block output, "
     r"the same three summaries give a CLS minimum of $0.9343$ at block 10, a "
     r"patch-token minimum of $0.9840$ at block 8 and a ratio of $4.12$: the "
     r"drift looks larger, the depths reorder, and the sub-block is not the "
     r"tensor the classifier reads. Layer-wise drift curves from different "
     r"papers are therefore not comparable unless both the aggregation and the "
     r"tensor are stated.",
     "1.2 toplulastirma paragrafi"),

    # ================= 1.2: Tablo VII (blok cikisi degerleri) =================
    ("04_experiments.tex",
     r"\caption{Block-wise clean-to-adversarial cosine similarity under each "
     r"model's own white-box PGD-10 attack ($n$=1000 per run; mean$\pm$std over "
     r"three runs). ViT columns differ only in how a block's tokens are "
     r"aggregated.}",
     r"\caption{Block-wise clean-to-adversarial cosine similarity under each "
     r"model's own white-box PGD-10 attack ($n$=1000 per run; mean over three "
     r"runs). All summaries are taken at the residual block output, so the ViT "
     r"and CNN columns are measured at equivalent points; the ViT columns "
     r"differ only in how a block's tokens are aggregated. Figures for the MLP "
     r"sub-block output are given in the text.}",
     "1.2 tablo basligi"),

    ("04_experiments.tex",
     "1 & 0.9993 & 0.9989 & 0.9942 & layer1.0 & 0.9951 \\\\\n"
     "2 & 0.9910 & 0.9957 & 0.9868 & layer1.1 & 0.9918 \\\\\n"
     "3 & 0.9785 & 0.9928 & 0.9821 & layer2.0 & 0.9879 \\\\\n"
     "4 & 0.9709 & 0.9877 & 0.9734 & layer2.1 & 0.9853 \\\\\n"
     "5 & 0.9652 & 0.9870 & 0.9719 & layer3.0 & 0.9753 \\\\\n"
     "6 & 0.9596 & 0.9873 & 0.9712 & layer3.1 & 0.9607 \\\\\n"
     "7 & 0.9497 & 0.9870 & 0.9698 & layer4.0 & \\textbf{0.8777} \\\\\n"
     "8 & 0.9414 & \\textbf{0.9840} & \\textbf{0.9663} & layer4.1 & 0.9108 \\\\\n"
     "9 & 0.9353 & 0.9850 & 0.9675 & & \\\\\n"
     "10 & \\textbf{0.9343} & 0.9877 & 0.9696 & & \\\\\n"
     "11 & 0.9352 & 0.9912 & 0.9753 & & \\\\\n"
     "12 & 0.9779 & 0.9955 & 0.9884 & & \\\\",

     "1 & 0.9993 & 0.9980 & 0.9927 & layer1.0 & 0.9951 \\\\\n"
     "2 & 0.9950 & 0.9959 & 0.9901 & layer1.1 & 0.9918 \\\\\n"
     "3 & 0.9902 & 0.9940 & 0.9881 & layer2.0 & 0.9879 \\\\\n"
     "4 & 0.9873 & 0.9919 & 0.9861 & layer2.1 & 0.9853 \\\\\n"
     "5 & 0.9845 & 0.9904 & 0.9847 & layer3.0 & 0.9753 \\\\\n"
     "6 & 0.9814 & 0.9894 & 0.9835 & layer3.1 & 0.9607 \\\\\n"
     "7 & 0.9782 & 0.9885 & 0.9826 & layer4.0 & \\textbf{0.8777} \\\\\n"
     "8 & 0.9743 & 0.9875 & 0.9816 & layer4.1 & 0.9108 \\\\\n"
     "9 & 0.9703 & \\textbf{0.9870} & 0.9809 & & \\\\\n"
     "10 & 0.9661 & 0.9872 & 0.9805 & & \\\\\n"
     "11 & \\textbf{0.9604} & 0.9874 & \\textbf{0.9803} & & \\\\\n"
     "12 & 0.9663 & 0.9915 & 0.9837 & & \\\\",
     "1.2 tablo satirlari"),

    # ================= tartisma =================
    ("05_discussion.tex",
     r"since the CLS pathway drifts about four times as far as the patch-token "
     r"mean",
     r"since the CLS pathway drifts about three times as far as the patch-token "
     r"mean",
     "1.2 tartisma orani"),
]

if not uygula(YAMALAR, S):
    sys.exit(1)
