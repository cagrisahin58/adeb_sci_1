#!/usr/bin/env python3
"""Hakem turu 3 - OZET ve MANSET (Ingilizce).

Ozet: 264 -> <=250 kelime, ozdesligin eksik carpani (1-r_cond) geri konur,
"literaturde yaygin uc iddia" fazla iddiasi duzeltilir, manset ayristirmasi
girer. Giris/ilgili calismalar/sonuc ayni ayristirmayi tasir.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

KOK = Path("/home/firat/projects/adeb_sci_1/paper/manuscript")

# ----------------------------------------------------------------- ozet
ESKI_OZ = (
    "Comparisons of adversarial robustness across architecture families report "
    "conflicting conclusions, and the disagreement is usually attributed to "
    "models, training recipes, or datasets. We show that a substantial part of "
    "it comes from the measurement protocol itself."
)
YENI_OZ = (
    "Comparisons of adversarial robustness across architecture families reach "
    "conflicting conclusions, usually attributed to models, training recipes, "
    "or datasets. We show that much of the disagreement comes from the "
    "measurement protocol itself."
)

OZ_YAMALARI = [
    (ESKI_OZ, YENI_OZ, "oz acilis"),

    ("we hold models, data, threat model and attack budget fixed and vary only "
     "how robustness and transfer are scored. Across four established "
     "conditioning protocols the measured CNN-to-ViT transfer asymmetry ranges "
     "from 4.4 to 19.4 points on CIFAR-10, whereas retraining both architectures "
     "from scratch moves the same quantity by under 1.5 points, and the protocol "
     "decides whether an equivalence test is accepted or rejected. Replicating "
     "the design on CIFAR-100 leaves the spread in the same range and preserves "
     "the sign in all twelve measurements.",

     "we fix models, data, threat model and attack budget and vary only how "
     "transfer is scored. Across four conditioning protocols the measured "
     "CNN-to-ViT transfer asymmetry ranges from 4.4 to 19.4 points on CIFAR-10, "
     "whereas retraining both architectures moves it by under 1.5 points. That "
     "15.01-point spread is not one thing: 5.80 points come from a protocol that "
     "estimates a different quantity, 5.30 from dropping conditioning altogether, "
     "and 3.91 remain as irreducible discretion between two defensible protocols. "
     "Replicating the design on CIFAR-100 preserves the sign in all twelve "
     "measurements.",
     "oz manset ayristirmasi"),

    ("A three-architecture control shows that the deviation of unconditioned from "
     "conditioned rates is algebraically equal to the target's clean error, not "
     "merely correlated with it, so raw rates are contaminated by target weakness "
     "by construction. Holding the training trajectory fixed and varying only the "
     "checkpoint-selection rule adds a fourth, almost never reported, source of "
     "variance. Three claims common in this area also fail to replicate. We close "
     "with reporting requirements for cross-architecture robustness studies.",

     "The second of those parts is exactly correctable: the deviation of "
     "unconditioned from conditioned rates equals the target's clean error scaled "
     "by one minus the conditioned rate, an identity whose premise we measure "
     "rather than assume, so raw rates are contaminated by target weakness by "
     "construction. Varying only the checkpoint-selection rule adds a fourth, "
     "almost never reported, source of variance. Three further readings fail to "
     "replicate under direct measurement, and we close with reporting "
     "requirements for cross-architecture robustness studies.",
     "oz ozdeslik ve kapanis"),
]

# ------------------------------------------------------- manset (bolumler)
BOLUM_YAMALARI = [
    ("01_introduction.tex",
     r"the measured cross-architecture transfer asymmetry ranges from $+4.4$ to "
     r"$+19.4$ points across four established conditioning protocols, a 4.4-fold "
     r"spread, whereas retraining both architectures from scratch moves the same "
     r"quantity by under $1.5$ points.",
     r"the measured cross-architecture transfer asymmetry ranges from $+4.4$ to "
     r"$+19.4$ points across four conditioning protocols, a 4.4-fold spread, "
     r"whereas retraining both architectures from scratch moves the same quantity "
     r"by under $1.5$ points. We then separate that spread rather than leave it as "
     r"one number: $5.80$ points of it come from a protocol that estimates a "
     r"different quantity, $5.30$ from dropping conditioning altogether, which an "
     r"identity we derive corrects in closed form, and $3.91$ remain as discretion "
     r"between two protocols that are both defensible, which is still more than "
     r"twice the retraining effect.",
     "giris ayristirmasi"),

    ("02_related_work.tex",
     r"and we find that the measured asymmetry moves by $15.01\pm0.84$ points "
     r"across the four protocols, a 4.4-fold spread, while retraining both "
     r"architectures moves that same quantity by under $1.5$ points.",
     r"and we find that the measured asymmetry moves by $15.01\pm0.84$ points "
     r"across the four protocols, of which $3.91$ points separate the two "
     r"protocols we endorse, while retraining both architectures moves that same "
     r"quantity by under $1.5$ points.",
     "ilgili calismalar ayristirmasi"),

    ("06_conclusion.tex",
     r"the cross-architecture transfer asymmetry ranges from $+4.4$ to $+19.4$ "
     r"points across four established conditioning protocols, a 4.4-fold spread, "
     r"whereas retraining both architectures from scratch moves that same quantity "
     r"by under $1.5$ points, and the protocol decides whether an equivalence test "
     r"is accepted or rejected.",
     r"the cross-architecture transfer asymmetry ranges from $+4.4$ to $+19.4$ "
     r"points across four conditioning protocols, whereas retraining both "
     r"architectures from scratch moves that same quantity by under $1.5$ points. "
     r"That $15.01$-point spread decomposes into $5.80$ points of a different "
     r"estimand, $5.30$ points that an identity corrects in closed form, and "
     r"$3.91$ points of genuine discretion between two defensible protocols; the "
     r"last of these is the part a reporting standard has to address.",
     "sonuc ayristirmasi"),
]

hata = []
m = (KOK / "main.tex").read_text(encoding="utf-8")
for eski, yeni, etiket in OZ_YAMALARI:
    if eski in m:
        m = m.replace(eski, yeni, 1)
        print(f"  [+] {etiket}")
    elif yeni in m:
        print(f"  [=] {etiket} zaten")
    else:
        hata.append(etiket)
if hata:
    print("BASARISIZ (ozet):", *hata, sep="\n   ")
    sys.exit(1)
(KOK / "main.tex").write_text(m, encoding="utf-8")

if not uygula(BOLUM_YAMALARI, KOK / "sections"):
    sys.exit(1)
