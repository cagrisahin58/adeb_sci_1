#!/usr/bin/env python3
"""EN ozeti 263 -> <=250 kelime. Yalniz ifade sikilastirmasi, iddia degismez."""
import re
import sys
from pathlib import Path

P = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/main.tex")
t = P.read_text(encoding="utf-8")

YAMALAR = [
    ("reach conflicting conclusions, usually attributed to models, training "
     "recipes, or datasets. We show that much of the disagreement comes from "
     "the measurement protocol itself.",
     "reach conflicting conclusions, usually attributed to models, training "
     "recipes, or datasets. We show that much of it comes from the measurement "
     "protocol itself."),

    ("and a validation split held out before any training, we fix models",
     "and a validation split held out before training, we fix models"),

    ("That 15.01-point spread is not one thing: 9.21 points separate the "
     "unconditioned rate from the target-correct rate and an identity we derive "
     "removes them in closed form, while 5.79 points come from a protocol that "
     "estimates a different quantity. What survives the correction is 3.91 "
     "points of discretion between the two protocols we endorse. The identity "
     "states that the deviation of unconditioned from conditioned rates equals "
     "the target's clean error scaled by one minus the conditioned rate, and we "
     "measure its premise rather than assume it.",

     "That 15.01-point spread is not one thing: an identity we derive removes "
     "9.21 points of it in closed form, and 5.79 points come from a protocol "
     "that estimates a different quantity. What survives is 3.91 points of "
     "discretion between the two protocols we endorse. The identity equates the "
     "deviation of unconditioned from conditioned rates with the target's clean "
     "error scaled by one minus the conditioned rate, on a premise we measure "
     "rather than assume."),

    ("Replicating the design on CIFAR-100 preserves the sign in all twelve "
     "measurements.",
     "Replicating on CIFAR-100 preserves the sign in all twelve measurements."),

    ("adds a fourth, almost never reported, source of variance.",
     "adds a fourth, rarely reported, source of variance."),
]

hata = []
for eski, yeni in YAMALAR:
    if eski in t:
        t = t.replace(eski, yeni, 1)
    elif yeni not in t:
        hata.append(eski[:60])
if hata:
    print("BASARISIZ:", *hata, sep="\n   ")
    sys.exit(1)

P.write_text(t, encoding="utf-8")
oz = re.search(r"\\begin\{abstract\}(.+?)\\end\{abstract\}", t, re.DOTALL).group(1)
print(f"EN ozet: {len(oz.split())} kelime")
