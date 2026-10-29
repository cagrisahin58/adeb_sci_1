"""Konsey B6 maskeleme kurali (ON_KAYIT §5 B6): PGD-10 ile AutoAttack farki.

AA, test kumesinin ilk n goruntusunde kosar (experiments/run_autoattack_run2.py).
PGD-10 dogrulugu ayni ilk n goruntude, transfer matrisinin kosegen hucresinden
(per_sample_{m}_to_{m}.npz, target_adv_wrong) hesaplanir; B4 kosegeninin tamami
(10000 goruntu) KULLANILMAZ, cunku farkli orneklemi karsilastirmak olur.
Ayni orneklem, iki ciktinin temiz-dogru maskeleri karsilastirilarak denetlenir.

Kullanim (konteynerde, /workspace):
  python scripts/konsey_b6_maskeleme.py --aa-dizini results/q1/konsey_b6_aa \
      --matris-dizini results/q1/konsey_b4_matris --n 1000 \
      --cikti results/q1/konsey_b6_maskeleme.json
Cikti: model basina PGD ve AA dogrulugu, fark, isaret; '--maskeleme-isaretli'
icin hazir arguman dizgisi.
"""
import argparse
import json
from pathlib import Path

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aa-dizini", required=True)
    ap.add_argument("--matris-dizini", required=True)
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--esik", type=float, default=10.0, help="PGD - AA farki (puan); asan isaretlenir")
    ap.add_argument("--maske-tolerans", type=float, default=0.01,
                    help="Temiz maske uyusmazligi orani bunu asarsa ayni orneklem sayilmaz")
    ap.add_argument("--cikti", required=True)
    a = ap.parse_args()

    aa_dir, mx_dir = Path(a.aa_dizini), Path(a.matris_dizini)
    summ = json.loads((aa_dir / "autoattack_summary.json").read_text())
    tm = json.loads((mx_dir / "transfer_matrix.json").read_text())
    saldiri = tm.get("attack", "pgd")
    if saldiri != "pgd" or tm.get("steps") != 10:
        raise SystemExit(f"{mx_dir}: matris PGD-10 degil (attack={saldiri}, steps={tm.get('steps')})")

    out = {"aa_dizini": str(aa_dir), "matris_dizini": str(mx_dir), "n": a.n, "esik_puan": a.esik,
           "pgd_kaynagi": "per_sample_{m}_to_{m}.npz target_adv_wrong, ilk n goruntu",
           "aa_kaynagi": "per_sample_{m}.npz robust_correct, ilk n goruntu",
           "modeller": {}, "hatalar": []}
    for r in summ["results"]:
        m = r["model"]
        aa_f = aa_dir / f"per_sample_{m}.npz"
        mx_f = mx_dir / f"per_sample_{m}_to_{m}.npz"
        if not aa_f.exists() or not mx_f.exists():
            out["hatalar"].append(f"{m}: dosya yok ({aa_f if not aa_f.exists() else mx_f})")
            continue
        aa, mx = np.load(aa_f), np.load(mx_f)
        n_aa, n_mx = len(aa["robust_correct"]), len(mx["target_adv_wrong"])
        if n_aa < a.n or n_mx < a.n:
            out["hatalar"].append(f"{m}: orneklem kisa (AA {n_aa}, matris {n_mx}, istenen {a.n})")
            continue
        n = a.n
        aa_rob = aa["robust_correct"][:n].astype(bool)
        aa_cl = aa["clean_correct"][:n].astype(bool)
        mx_cl = mx["target_clean_correct"][:n].astype(bool)
        pgd_rob = ~mx["target_adv_wrong"][:n].astype(bool)
        uyusmaz = int((aa_cl != mx_cl).sum())
        pgd_acc, aa_acc = 100.0 * pgd_rob.mean(), 100.0 * aa_rob.mean()
        fark = pgd_acc - aa_acc
        kayit = {
            "pgd10_dogruluk": round(float(pgd_acc), 2),
            "aa_dogruluk": round(float(aa_acc), 2),
            "fark_puan": round(float(fark), 2),
            "isaretli": bool(fark > a.esik),
            "temiz_dogruluk_aa": round(float(100.0 * aa_cl.mean()), 2),
            "temiz_dogruluk_matris": round(float(100.0 * mx_cl.mean()), 2),
            "temiz_maske_uyusmazligi": uyusmaz,
            "aa_robust_pgd_yanilmis": int((aa_rob & ~pgd_rob).sum()),
        }
        if uyusmaz > a.maske_tolerans * n:
            out["hatalar"].append(f"{m}: temiz maskeler {uyusmaz}/{n} goruntude farkli; "
                                  f"ayni orneklem/model degil")
            kayit["isaretli"] = None
        out["modeller"][m] = kayit
    isaretli = [m for m, k in out["modeller"].items() if k["isaretli"]]
    out["isaretli"] = isaretli
    out["maskeleme_isaretli_arg"] = ("--maskeleme-isaretli " + " ".join(isaretli)) if isaretli else ""
    Path(a.cikti).parent.mkdir(parents=True, exist_ok=True)
    Path(a.cikti).write_text(json.dumps(out, indent=2, ensure_ascii=False))
    for m, k in out["modeller"].items():
        print(f"{m}: PGD10={k['pgd10_dogruluk']:.2f} AA={k['aa_dogruluk']:.2f} fark={k['fark_puan']:+.2f} "
              f"isaretli={k['isaretli']} maske_uyusmaz={k['temiz_maske_uyusmazligi']}")
    for h in out["hatalar"]:
        print("HATA:", h)
    print(f"isaretli: {isaretli or 'yok'} -> {a.cikti}")
    if out["hatalar"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
