"""Konsey B3 kuyrugu yardimcisi: ON_KAYIT §4 denetimleri ve pilot okuma.

Alt komutlar (konteynerde, /workspace):
  tavan --pilot JSON          secilen tavani basar; egitim_baslamaz ise 'YOK'
  temiz --takma AD            IN kosusunun temiz asama denetimi (ON_KAYIT §4):
                              temiz asamanin ILK EPOGU sonundaki val dogrulugu,
                              ayni mimarinin rastgele baslatmali hucresinin ilk
                              epok val dogrulugu ortalamasindan en az 5 puan
                              yuksek olmali (29.10 dogrulayici duzeltmesi: son
                              epok dogruluklari tavana yakin oldugundan dogru
                              yuklenmis modelde de 5 puan tutmayabilirdi).
                              IN kosusunun ilk epogu: last.pth 'history.test_acc[0]'
                              (yoksa logs/konsey_b3/<AD>_temiz.log 'Epoch 1/').
                              V_IN referansi: logs/C1_clean_vit_200[123].log 'Epoch 1/'.
                              R224_IN referansi: en az bir epogu biten R224_scr
                              temiz asamalarinin last.pth history.test_acc[0];
                              yoksa ERTELENDI.
                              Son epok/best dogruluklari yalniz betimsel basilir.
                              Cikti tek satir: GECTI|KALDI|ERTELENDI|HATA <aciklama>
  cokus --takma AD            AT 5. epok val PGD dogrulugu < %15 mi (AT cokus kurali).
                              Cikti: BEKLE|TAMAM|COKUS <deger>
  ozet --takma AD --tavan N   AT ozeti: secilen epok, kosulan epok, kirpilma isareti
"""
import argparse
import json
import re
from pathlib import Path

import torch

TIP = {"V_IN": "vit_tiny_in1k", "R224_IN": "resnet18_224_in1k", "R224_scr": "resnet18_224"}
ROOT = Path("models/q1/konsey")


def hucre(takma):
    return takma.rsplit("_s", 1)[0]


def ckdir(takma, asama):
    t = TIP[hucre(takma)]
    sub = "clean" if asama == "temiz" else "adv/adversarial_training"
    return ROOT / takma / t / sub


def acc_of(p):
    ck = torch.load(p, map_location="cpu", weights_only=False)
    return float(ck.get("accuracy"))


def cmd_tavan(a):
    d = json.loads(Path(a.pilot).read_text())
    if d.get("egitim_baslamaz") or d.get("secilen_tavan") is None:
        print("YOK")
    else:
        print(int(d["secilen_tavan"]))


EPOK1 = re.compile(r"Epoch 1/\d+ - Train Loss: [0-9.]+, Train Acc: [0-9.]+%, Test Acc: ([0-9.]+)%")
ESIK_PUAN = 5.0


def ilk_epok_gecmis(ck_dir):
    """last.pth gecmisinden ilk epok val dogrulugu (yoksa None)."""
    last = Path(ck_dir) / "last.pth"
    if not last.exists():
        return None
    ck = torch.load(last, map_location="cpu", weights_only=False)
    ta = (ck.get("history") or {}).get("test_acc") or []
    return float(ta[0]) if ta else None


def ilk_epok_log(log):
    """Egitim logundaki 'Epoch 1/N ... Test Acc' satiri (son eslesme; devam halinde yineleme)."""
    p = Path(log)
    if not p.exists():
        return None
    m = EPOK1.findall(p.read_text(encoding="utf-8", errors="replace"))
    return float(m[-1]) if m else None


def cmd_temiz(a):
    h = hucre(a.takma)
    if h not in ("V_IN", "R224_IN"):
        print("GECTI denetim yalniz IN hucrelerinde")
        return
    d = ckdir(a.takma, "temiz")
    v1 = ilk_epok_gecmis(d)
    v1_kaynak = "last.pth history.test_acc[0]"
    if v1 is None:
        v1 = ilk_epok_log(f"logs/konsey_b3/{a.takma}_temiz.log")
        v1_kaynak = f"logs/konsey_b3/{a.takma}_temiz.log Epoch 1"
    if v1 is None:
        print(f"HATA {a.takma} ilk epok val dogrulugu okunamadi ({d}/last.pth gecmisi ve log yok)")
        return
    son = acc_of(d / "best.pth") if (d / "best.pth").exists() else float("nan")
    if h == "V_IN":
        logs = sorted(Path("logs").glob("C1_clean_vit_200[123].log"))
        refs = [x for x in (ilk_epok_log(p) for p in logs) if x is not None]
        kaynak = "C1 ViT-Tiny temiz ilk epok, " + " ".join(p.name for p in logs)
        if len(refs) != 3:
            print(f"HATA {a.takma} C1 ViT-Tiny referansi eksik: {len(refs)}/3 log okundu ({kaynak})")
            return
    else:
        refs, adlar = [], []
        for p in sorted(ROOT.glob("R224_scr_s*/resnet18_224/clean")):
            x = ilk_epok_gecmis(p)
            if x is not None:
                refs.append(x)
                adlar.append(p.parts[-3])
        kaynak = "R224_scr temiz ilk epok, " + (" ".join(adlar) or "-")
    if not refs:
        print(f"ERTELENDI {a.takma} ilk_epok_val={v1:.2f}; referans ({kaynak}) henuz yok")
        return
    ref = sum(refs) / len(refs)
    durum = "GECTI" if v1 >= ref + ESIK_PUAN else "KALDI"
    print(f"{durum} {a.takma} ilk_epok_val={v1:.2f} ({v1_kaynak}) ref={ref:.2f} "
          f"(n={len(refs)}, {kaynak}) fark={v1 - ref:+.2f} esik=+{ESIK_PUAN:.0f}; "
          f"betimsel best_val={son:.2f}")


def cmd_cokus(a):
    last = ckdir(a.takma, "at") / "last.pth"
    if not last.exists():
        print("BEKLE last.pth yok")
        return
    ck = torch.load(last, map_location="cpu", weights_only=False)
    adv = (ck.get("history") or {}).get("adv_acc") or []
    if len(adv) < 5:
        print(f"BEKLE {len(adv)} epok")
        return
    v = float(adv[4])
    print(f"{'COKUS' if v < 15.0 else 'TAMAM'} {v:.2f}")


def cmd_ozet(a):
    d = ckdir(a.takma, "at")
    best = torch.load(d / "best.pth", map_location="cpu", weights_only=False)
    marker = dict(ln.split("=", 1) for ln in (d / "TRAINING_COMPLETE").read_text().split())
    sec = int(best["epoch"]) + 1
    kirp = sec >= a.tavan - 5
    print(f"secilen_epok={sec} kosulan_epok={marker.get('epochs_run')} "
          f"erken_durma={marker.get('early_stopped')} tavanda_durdu={marker.get('stopped_at_cap')} "
          f"val_pgd={float(best['accuracy']):.2f} kirpilmis_olabilir={kirp}")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="k", required=True)
    p = sp.add_parser("tavan"); p.add_argument("--pilot", required=True); p.set_defaults(f=cmd_tavan)
    p = sp.add_parser("temiz"); p.add_argument("--takma", required=True); p.set_defaults(f=cmd_temiz)
    p = sp.add_parser("cokus"); p.add_argument("--takma", required=True); p.set_defaults(f=cmd_cokus)
    p = sp.add_parser("ozet"); p.add_argument("--takma", required=True)
    p.add_argument("--tavan", type=int, required=True); p.set_defaults(f=cmd_ozet)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
