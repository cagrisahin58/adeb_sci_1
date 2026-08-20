#!/usr/bin/env python3
"""E3 kantil kapsamasi tanisi — ON-KAYITLI SECIMIN KAC NOKTA URETTIGI.

E3'un on-kaydi her yorungeden CLEAN_TARGETS kantillerine gore ~6 checkpoint
secmeyi ongoruyordu (>=12 yorunge x 6 = ~72 nokta). Ancak secim
`chosen[ep] = ck` bicimindedir: birden fazla hedef ayni epoga duserse
girdiler SESSIZCE TEK NOKTAYA COKER.

Bu betik, q1_e3_calibration.cmd_points ile AYNI secim mantigini uygular ama
model yuklemez / GPU kullanmaz: yalniz metrics.jsonl okuyup kac AYRI
checkpoint secilecegini ve yorungenin temiz-dogruluk araligini raporlar.

Kullanim:
  docker exec -w /workspace adeb_eval python scripts/q1_e3_coverage.py
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OUT = ROOT / "results" / "q1" / "e3_coverage.json"


def clean_targets():
    """q1_e3_calibration.CLEAN_TARGETS — kaynaktan okunur, kopyalanmaz."""
    import re

    src = (ROOT / "scripts" / "q1_e3_calibration.py").read_text(encoding="utf-8")
    m = re.search(r"CLEAN_TARGETS\s*=\s*\[([^\]]*)\]", src)
    if not m:
        raise RuntimeError("CLEAN_TARGETS bulunamadi")
    vals = []
    for tok in m.group(1).split(","):
        tok = tok.strip()
        if not tok:
            continue
        vals.append(None if tok == "None" else float(tok))
    return vals


def select(entries, targets):
    """cmd_points ile ayni mantik: chosen[epoch] = ckpt (dict -> cokme)."""
    chosen = {}
    mapping = {}
    for tgt in targets:
        if tgt is None:
            ep = entries[-1][0]
        else:
            ep = min(((abs(c - tgt), e) for e, c in entries if c is not None))[1]
        chosen[ep] = True
        mapping[str(tgt)] = ep
    return sorted(chosen), mapping


# Yorunge kokleri: yeni bir asama eklendiginde (E5 -> cifar10, E7 -> svhn)
# BURAYA da eklenmelidir, yoksa kapsama sessizce eksik hesaplanir.
TRAJ_ROOTS = ["models/q1/e2", "models/q1/cifar100", "models/q1/svhn", "models/q1/cifar10"]


def find_trajectories(require_complete=True):
    """metrics.jsonl iceren epochs/ dizinleri.

    BITMISLIK KAPISI (require_complete): egitim SURERKEN kosulursa yarim
    yorungeler kapsamayi carpitir. Bu betik bir kez tam bunu yapti: s1003
    2 checkpoint'teyken kosuldu ve 11 yorunge/33 nokta raporladi; egitim
    bitince gercek deger 12/38 cikti ve BAYAT sayilar iki karar belgesine
    gecti. Kanit: epochs/ dizininin UST dizininde TRAINING_COMPLETE dosyasi.
    """
    out, skipped = [], []
    for base in TRAJ_ROOTS:
        p = ROOT / base
        if not p.exists():
            continue
        for m in sorted(p.rglob("epochs/metrics.jsonl")):
            marker = m.parent.parent / "TRAINING_COMPLETE"
            if require_complete and not marker.exists():
                skipped.append(str(m.parent.relative_to(ROOT)))
                continue
            out.append(m)
    if skipped:
        print("UYARI: %d yorunge BITMEMIS sayildi ve DISLANDI "
              "(TRAINING_COMPLETE yok):" % len(skipped))
        for sp in skipped:
            print("   -", sp)
    return out


def main():
    targets = clean_targets()
    print("CLEAN_TARGETS =", targets)
    rows = []
    for mfile in find_trajectories():
        entries = []
        for line in mfile.read_text().splitlines():
            if not line.strip():
                continue
            d = json.loads(line)
            if d.get("clean_acc") is not None:
                entries.append((d["epoch"], float(d["clean_acc"])))
        if not entries:
            continue
        entries.sort()
        cleans = [c for _, c in entries]
        eps, mapping = select(entries, targets)
        rows.append({
            "yorunge": str(mfile.parent.relative_to(ROOT)),
            "n_checkpoint": len(entries),
            "temiz_min": round(min(cleans), 2),
            "temiz_max": round(max(cleans), 2),
            "temiz_hata_araligi": [round(100 - max(cleans), 2), round(100 - min(cleans), 2)],
            "hedef_sayisi": len(targets),
            "AYRI_NOKTA": len(eps),
            "secilen_epoklar": eps,
            "hedef_epok_eslesmesi": mapping,
        })
        print("%-58s ckpt=%3d temiz %.2f-%.2f -> AYRI NOKTA %d/%d"
              % (rows[-1]["yorunge"], rows[-1]["n_checkpoint"],
                 rows[-1]["temiz_min"], rows[-1]["temiz_max"],
                 rows[-1]["AYRI_NOKTA"], len(targets)))

    toplam_beklenen = len(rows) * len(targets)
    toplam_gercek = sum(r["AYRI_NOKTA"] for r in rows)
    tum_ckpt = sum(r["n_checkpoint"] for r in rows)
    hata_min = min((r["temiz_hata_araligi"][0] for r in rows), default=None)
    hata_max = max((r["temiz_hata_araligi"][1] for r in rows), default=None)

    ozet = {
        "BITMISLIK_KAPISI": "yalniz TRAINING_COMPLETE tasiyan yorungeler dahil",
        "clean_targets": [("konverjan" if t is None else t) for t in targets],
        "n_yorunge": len(rows),
        "beklenen_nokta": toplam_beklenen,
        "GERCEK_AYRI_NOKTA": toplam_gercek,
        "cokme_orani_yuzde": (round((1 - toplam_gercek / toplam_beklenen) * 100, 1)
                              if toplam_beklenen else None),
        "TUM_CHECKPOINT_KULLANILSA": tum_ckpt,
        "temiz_hata_kapsamasi": [hata_min, hata_max],
        "yorungeler": rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(ozet, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n=== OZET ===")
    print("yorunge sayisi          :", ozet["n_yorunge"])
    print("beklenen nokta          :", ozet["beklenen_nokta"])
    print("GERCEK ayri nokta       :", ozet["GERCEK_AYRI_NOKTA"],
          "(cokme %%%s)" % ozet["cokme_orani_yuzde"])
    print("tum checkpoint kullanilsa:", ozet["TUM_CHECKPOINT_KULLANILSA"])
    print("temiz HATA kapsamasi    : %%%.2f - %%%.2f" % (hata_min, hata_max))
    print("yazildi:", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
