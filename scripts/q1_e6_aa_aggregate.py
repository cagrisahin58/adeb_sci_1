#!/usr/bin/env python3
"""E6: AutoAttack-L2 sonuclarini uc tohum cifti uzerinden toplulastirir.

Girdi : results/q1/cifar10_l2/aa_pair{1,2,3}/autoattack_summary.json
Cikti : results/q1/cifar10_l2/e6_aa_l2_summary.json

BEYAN EDILEN KAPSAM FARKI (E6_ON_KAYIT §1): PGD-L2 TAM test kumesinde
(n=10.000), AutoAttack-L2 ise n=5.000'de kosulmustur. Bu bir tutarsizlik
DEGIL, on-kayitli bir butce indirimidir; iki sayi ayni cumlede ayni ornek
kumesinden geliyormus gibi SUNULMAZ. Bu yuzden temiz dogruluk da HER IKI
kapsamda ayri raporlanir: AA'nin 5.000'lik altkumesindeki temiz dogruluk,
tam kumedekinden birkac yuzde ondaligi farkli olabilir ve bu BEKLENIR.

BAGLAYICI CERCEVE (E6_ON_KAYIT §0): modeller L-infinity ile EGITILMISTIR.
Bu sayilar L2-EGITILMIS referanslarla KARSILASTIRILAMAZ.
"""
import json
import statistics as st
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
L2 = ROOT / "results/q1/cifar10_l2"


def sd(x):
    return round(float(st.stdev(x)), 3) if len(x) > 1 else None


pairs, eksik = [], []
for p in (1, 2, 3):
    f = L2 / f"aa_pair{p}/autoattack_summary.json"
    if not f.exists():
        eksik.append(f"pair{p}")
        continue
    pairs.append((p, json.loads(f.read_text(encoding="utf-8"))))

if not pairs:
    raise SystemExit(f"HATA: hicbir AA-L2 ozeti yok (eksik: {eksik})")

modeller = {}
for p, d in pairs:
    for r in d["results"]:
        modeller.setdefault(r["model"], {"robust": [], "clean": [], "ciftler": []})
        modeller[r["model"]]["robust"].append(r["robust_accuracy"])
        modeller[r["model"]]["clean"].append(r["clean_accuracy"])
        modeller[r["model"]]["ciftler"].append(p)

ozet = {}
for m, v in modeller.items():
    ozet[m] = {
        "n_cift": len(v["robust"]),
        "aa_l2_robust": {"ort": round(float(st.mean(v["robust"])), 2),
                         "sd": sd(v["robust"]), "degerler": v["robust"]},
        "temiz_5000_altkumede": {"ort": round(float(st.mean(v["clean"])), 2),
                                 "sd": sd(v["clean"]), "degerler": v["clean"]},
        "ciftler": v["ciftler"],
    }

mcnemar = [{"cift": p,
            "a": d["mcnemar_robust"]["model_a"], "b": d["mcnemar_robust"]["model_b"],
            "yalniz_a_dogru": d["mcnemar_robust"]["a_only_correct"],
            "yalniz_b_dogru": d["mcnemar_robust"]["b_only_correct"],
            "p": d["mcnemar_robust"]["p_value"]}
           for p, d in pairs]

sonuc = {
    "uretildi_utc": datetime.now(timezone.utc).isoformat(),
    "norm": "L2", "eps": 0.5, "n_samples": pairs[0][1]["n_samples"],
    "KAPSAM_BEYANI": "AutoAttack-L2 n=5.000 (on-kayitli butce indirimi, "
                     "E6_ON_KAYIT §1); PGD-L2 ise TAM test kumesinde n=10.000. "
                     "Iki sayi ayni ornek kumesinden gelmez ve oyle sunulmaz.",
    "BAGLAYICI_CERCEVE": "Modeller L-infinity ile EGITILMISTIR; bu sayilar "
                         "L2-EGITILMIS referanslarla KARSILASTIRILAMAZ.",
    "modeller": ozet,
    "mcnemar_gurbuz": mcnemar,
    "eksik_ciftler": eksik,
}
if eksik:
    sonuc["UYARI"] = (f"{len(eksik)} cift EKSIK ({eksik}); toplulastirma "
                      "TAMAMLANMAMIS veriyle yapildi ve boyle raporlanmalidir.")

out = L2 / "e6_aa_l2_summary.json"
out.write_text(json.dumps(sonuc, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"AutoAttack-L2 (eps={sonuc['eps']}, n={sonuc['n_samples']}), "
      f"{len(pairs)}/3 cift")
for m, v in ozet.items():
    r, c = v["aa_l2_robust"], v["temiz_5000_altkumede"]
    print(f"  {m:14s} gurbuz {r['ort']:6.2f} +/- {r['sd'] if r['sd'] is not None else 0:.2f}"
          f"   temiz(5k) {c['ort']:6.2f}   degerler {r['degerler']}")
print("  McNemar:", ", ".join(f"cift{x['cift']} p={x['p']:.2e}" for x in mcnemar))
if eksik:
    print(" ", sonuc["UYARI"])
print(f"-> {out}")
