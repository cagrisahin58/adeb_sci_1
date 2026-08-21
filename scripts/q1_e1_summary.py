#!/usr/bin/env python3
"""Q1 ozet artefakti (E1/CIFAR-100 ve E7/SVHN) — ortalama/sd + secim yolu.

Veri kumesi --dataset ile secilir; bayrak verilmezse davranis eskisiyle
BIREBIR aynidir (cifar100, 3 tohum).

Kaynaklar (hicbiri elle girilmez):
  results/q1/cifar100/<arch>_s<seed>/pgd_summary_<arch>.json  -> test clean/PGD
  models/q1/cifar100/<arch>_s<seed>/.../epochs/metrics.jsonl  -> val egrisi,
      en iyi epok, durma epogu, plato istatistikleri

Cikti: results/q1/e1_cifar100_summary.json

NOT: sd her yerde ddof=1 (makale boyunca kullanilan tanim).
"""

import argparse
import json
import pathlib
import statistics as st

ROOT = pathlib.Path(__file__).resolve().parents[1]

_ap = argparse.ArgumentParser()
_ap.add_argument("--dataset", default="cifar100", choices=["cifar100", "svhn", "cifar10"])
_ap.add_argument("--out", default=None)
_args = _ap.parse_args()
DS = _args.dataset

# Tohum listeleri veri kumesine gore: E7 KISA surum 2 tohumdur (K-01).
_TOHUMLAR = {
    "cifar100": {"resnet18": [1001, 1002, 1003], "vit_tiny": [2001, 2002, 2003]},
    "cifar10": {"resnet18": [1001, 1002, 1003], "vit_tiny": [2001, 2002, 2003]},
    "svhn": {"resnet18": [1001, 1002], "vit_tiny": [2001, 2002]},
}
_VARSAYILAN_CIKTI = {"cifar100": "e1_cifar100_summary.json",
                     "svhn": "e7_svhn_summary.json",
                     "cifar10": "c1_cifar10_summary.json"}
OUT = pathlib.Path(_args.out) if _args.out else (
    ROOT / "results" / "q1" / _VARSAYILAN_CIKTI[DS])
ARCHS = _TOHUMLAR[DS]
MIN_DELTA = 0.1          # trainer'in erken durdurma esigi
PLATEAU_FROM = 3         # plato istatistigi bu epoktan itibaren


def sd(x):
    return float(st.stdev(x)) if len(x) > 1 else None


def read_curve(arch, seed):
    base = ROOT / "models" / "q1" / DS / f"{arch}_s{seed}" / arch / "adv"
    m = base / "adversarial_training" / "epochs" / "metrics.jsonl"
    if not m.exists():
        return None
    rows = []
    for line in m.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        if d.get("adv_acc") is not None:
            rows.append((int(d["epoch"]), float(d.get("clean_acc", float("nan"))),
                         float(d["adv_acc"])))
    if not rows:
        return None
    rows.sort()
    return rows


def best_epoch(rows):
    """Trainer'in secim kurali: adv > best + min_delta (mandal/ratchet)."""
    best_v, best_e = -1e9, None
    for e, _c, a in rows:
        if a > best_v + MIN_DELTA:
            best_v, best_e = a, e
    return best_e, best_v


AA_MODEL = {"resnet18": "ResNet18_AT", "vit_tiny": "ViT_Tiny_AT"}
SEED_TO_PAIR = {1001: 1, 1002: 2, 1003: 3, 2001: 1, 2002: 2, 2003: 3}


def read_aa(arch, seed):
    """AutoAttack ozetinden bu mimari/tohum icin gurbuz dogruluk."""
    pair = SEED_TO_PAIR.get(seed)
    if pair is None:
        return None
    # VERI KUMESI SIZINTISI DUZELTILDI: bu yol "cifar100" diye civiliydi ve
    # --dataset svhn verildiginde CIFAR-100 AutoAttack sonuclarini okuyup
    # SVHN etiketiyle raporluyordu. E7-KISA on-kayitli olarak AutoAttack
    # ICERMEZ; dosya bulunmayinca None doner ve ozet AA alanini BOS birakir.
    f = ROOT / "results" / "q1" / DS / f"pair{pair}" / "autoattack_summary.json"
    if not f.exists():
        return None
    d = json.loads(f.read_text(encoding="utf-8"))
    for r in d.get("results", []):
        if r.get("model") == AA_MODEL.get(arch):
            return float(r["robust_accuracy"])
    return None


def read_test(arch, seed):
    p = ROOT / "results" / "q1" / DS / f"{arch}_s{seed}" / f"pgd_summary_{arch}.json"
    if not p.exists():
        return None
    d = json.loads(p.read_text(encoding="utf-8"))
    return {"clean": float(d["clean_acc"]), "pgd10": float(d["pgd10_acc"]),
            "n": int(d.get("n", -1)), "ckpt": d.get("ckpt")}


def main():
    out = {"dataset": DS, "min_delta": MIN_DELTA,
           "sd_tanimi": "ornek sd (ddof=1)", "mimariler": {}}

    for arch, seeds in ARCHS.items():
        per = {}
        for s in seeds:
            t = read_test(arch, s)
            rows = read_curve(arch, s)
            if t is None or rows is None:
                per[str(s)] = {"durum": "EKSIK",
                               "test_var_mi": t is not None,
                               "egri_var_mi": rows is not None}
                continue
            be, bv = best_epoch(rows)
            aa = read_aa(arch, s)
            plateau = [a for e, _c, a in rows if e >= PLATEAU_FROM]
            per[str(s)] = {
                "test_clean": round(t["clean"], 2),
                "test_pgd10": round(t["pgd10"], 2),
                "test_autoattack": (round(aa, 2) if aa is not None else None),
                "test_n": t["n"],
                "val_en_iyi_adv": round(bv, 2),
                "en_iyi_epok": be,
                "durma_epogu": rows[-1][0],
                "plato_ep%d+" % PLATEAU_FROM: {
                    "min": round(min(plateau), 2), "max": round(max(plateau), 2),
                    "genislik": round(max(plateau) - min(plateau), 2),
                    "sd": round(st.stdev(plateau), 3) if len(plateau) > 1 else None,
                    "ort": round(st.mean(plateau), 2),
                    "secilen_ort_uzakligi_sd": (
                        round((bv - st.mean(plateau)) / st.stdev(plateau), 2)
                        if len(plateau) > 1 and st.stdev(plateau) > 0 else None
                    ),
                },
            }

        done = [v for v in per.values() if "test_clean" in v]
        agg = None
        if done:
            cl = [v["test_clean"] for v in done]
            pg = [v["test_pgd10"] for v in done]
            aal = [v["test_autoattack"] for v in done if v.get("test_autoattack") is not None]
            be = [v["en_iyi_epok"] for v in done]
            de = [v["durma_epogu"] for v in done]
            agg = {
                "n_tohum": len(done),
                "test_clean": {"ort": round(st.mean(cl), 2), "sd": (round(sd(cl), 3) if sd(cl) else None),
                               "degerler": cl},
                "test_pgd10": {"ort": round(st.mean(pg), 2), "sd": (round(sd(pg), 3) if sd(pg) else None),
                               "degerler": pg},
                "test_autoattack": ({"ort": round(st.mean(aal), 2),
                                     "sd": (round(sd(aal), 3) if sd(aal) else None),
                                     "degerler": aal} if aal else None),
                "en_iyi_epok": {"degerler": be, "aciklik": max(be) - min(be)},
                "durma_epogu": {"degerler": de, "aciklik": max(de) - min(de)},
            }
        out["mimariler"][arch] = {"tohumlar": per, "ozet": agg}

    # SECIM YOLU vs SONUC karsitligi (E2 tartismasinin CIFAR-100 ayagi)
    kars = {}
    for arch, d in out["mimariler"].items():
        a = d["ozet"]
        if not a or a["n_tohum"] < 2:
            continue
        kars[arch] = {
            "en_iyi_epok_acikligi": a["en_iyi_epok"]["aciklik"],
            "durma_epogu_acikligi": a["durma_epogu"]["aciklik"],
            "test_pgd10_sd": a["test_pgd10"]["sd"],
            "test_clean_sd": a["test_clean"]["sd"],
        }
    out["SECIM_YOLU_vs_SONUC"] = {
        "aciklama": (
            "Tohumlar FARKLI epoklarda zirve yapip FARKLI epoklarda duruyor "
            "(secim yolu oynak) ama test sonucu ne kadar oynuyor? Bu, E2'nin "
            "secim-piyangosu bulgusuna KARSI-KANIT adayidir. DIKKAT: E2 ayni "
            "yorungeye farkli SECIM PROTOKOLLERI uyguluyordu; burada her tohumun "
            "kendi yorungesi ve kendi dogal durma noktasi var. AYNI deney DEGIL; "
            "E2 muadili olcum icin tek yorungeye cevrimdisi izgara gerekir "
            "(E1_PILOT_KAPISI.md B.8: kod henuz YOK)."
        ),
        "mimariler": kars,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    for arch, d in out["mimariler"].items():
        a = d["ozet"]
        if not a:
            print(f"{arch}: veri yok")
            continue
        print(f"\n{arch} (n={a['n_tohum']})")
        print(f"  test clean : {a['test_clean']['ort']} +/- {a['test_clean']['sd']}  {a['test_clean']['degerler']}")
        print(f"  test PGD-10: {a['test_pgd10']['ort']} +/- {a['test_pgd10']['sd']}  {a['test_pgd10']['degerler']}")
        if a.get("test_autoattack"):
            aa_ = a["test_autoattack"]
            print(f"  test AA    : {aa_['ort']} +/- {aa_['sd']}  {aa_['degerler']}")
        print(f"  en iyi epok: {a['en_iyi_epok']['degerler']} (aciklik {a['en_iyi_epok']['aciklik']})")
        print(f"  durma epogu: {a['durma_epogu']['degerler']} (aciklik {a['durma_epogu']['aciklik']})")
    print("\nyazildi:", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
