#!/usr/bin/env python3
"""E3 A KOLU (kontrollu) -- ASIMETRI yayilimi, yorunge boyunca.

NEDEN YENI BETIK. Mevcut A kolu (q1_e3_calibration.py points) her
checkpoint'te TEK YON uretiyordu: arsivlenmis kaynak -> checkpoint hedefi.
Asimetri IKI YON gerektirir, dolayisiyla o cikti duzeltilmis nicelige
(EK C) DONUSTURULEMEZ. Bu betik her checkpoint'te IKI YONU de uretir:

  ileri : P -> M(c)   arsivlenmis P saldirilari, M(c)'de SALT ILERI GECIS  (ucuz)
  geri  : M(c) -> P   M(c) uzerinde PGD uretilir, P'de degerlendirilir     (pahali)

Kontrol: c yorunge boyunca ilerlerken MIMARI CIFTI, TOHUM, VERI KUMESI ve
SALDIRI BUTCESI sabittir; degisen tek sey M(c)'nin temiz dogrulugu, yani
ciftin temiz hata FARKIDIR. B kolu (gozlemsel) bunu kontrol edemez.

MALIYET: checkpoint basina BIR PGD kosumu. --stride ile seyreltilir ve
seyreltme cikti json'una YAZILIR (sessiz kirpma yok).

Cikti: results/q1/e3_akolu/<traj>_ep<N>.json  (bir kayit = bir CIFT)
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT))
import os  # noqa: E402
os.chdir(ROOT)

from src.attacks import PGDAttack  # noqa: E402
from src.data import DATASETS, get_loaders  # noqa: E402
from src.models import ModelRegistry  # noqa: E402
from src.utils.load_model_auto import load_model_auto, infer_num_classes  # noqa: E402

EPS, ALPHA, STEPS = 8 / 255, 2 / 255, 10
PROTOKOLLER = ["raw", "target_correct", "both_correct", "successful_source"]


def set_seed(s):
    import random
    random.seed(s); np.random.seed(s); torch.manual_seed(s); torch.cuda.manual_seed_all(s)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


@torch.no_grad()
def maskeler(model, clean, adv, labels, device, bs=250):
    """(temiz-dogru, adv-yanlis) maskeleri."""
    c_ok, a_wrong = [], []
    for i in range(0, len(labels), bs):
        x, xa = clean[i:i + bs].to(device), adv[i:i + bs].to(device)
        y = labels[i:i + bs].to(device)
        c_ok.append((model(x).argmax(1) == y).cpu())
        a_wrong.append((model(xa).argmax(1) != y).cpu())
    return torch.cat(c_ok).numpy().astype(bool), torch.cat(a_wrong).numpy().astype(bool)


def uret_adv(model, clean, labels, device, bs=250):
    atk = PGDAttack(model, eps=EPS, alpha=ALPHA, steps=STEPS)
    parcalar = []
    for i in range(0, len(labels), bs):
        x, y = clean[i:i + bs].to(device), labels[i:i + bs].to(device)
        parcalar.append(atk(x, y).detach().cpu())
    return torch.cat(parcalar)


def oranlar(tc, aw, sc, sa):
    def r(m):
        return float(100 * aw[m].mean()) if m.sum() else float("nan")
    return {"raw": float(100 * aw.mean()), "target_correct": r(tc),
            "both_correct": r(tc & sc), "successful_source": r(tc & sa)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs-dir", required=True, help="taranan yorungenin epochs dizini")
    ap.add_argument("--model-type", required=True, help="taranan modelin tipi")
    ap.add_argument("--partner-ckpt", required=True, help="SABIT es modelin checkpoint'i")
    ap.add_argument("--partner-type", required=True)
    ap.add_argument("--partner-archive", required=True,
                    help="sabit es modelin ARSIVLENMIS adv ornekleri (q1_archive_adv.py)")
    ap.add_argument("--dataset", choices=sorted(DATASETS), default="cifar10")
    ap.add_argument("--trajectory-id", required=True)
    ap.add_argument("--cluster", required=True, help="kume anahtari (kume bootstrap icin)")
    ap.add_argument("--stride", type=int, default=10)
    ap.add_argument("--out-dir", default=str(ROOT / "results/q1/e3_akolu"))
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type != "cuda":
        sys.exit("CUDA yok -- A kolu CPU'da makul surede bitmez")
    set_seed(args.seed)

    # --- arsiv: sabit es modelin adv ornekleri + kendi maskeleri ---
    arc = np.load(args.partner_archive, allow_pickle=True)
    adv_P = torch.from_numpy(arc["adv_uint8"]).float() / 255.0
    labels = torch.from_numpy(arc["labels"])
    n = len(labels)
    P_clean_ok = arc["source_clean_correct"].astype(bool)
    P_adv_wrong_self = arc["source_adv_wrong"].astype(bool)   # P kendi saldirisinda yaniliyor mu

    # --- temiz goruntuler, AYNI sirada ---
    _, test_loader = get_loaders(dataset=args.dataset, data_dir="./data", test_batch_size=500)
    imgs, labs = [], []
    for x, y in test_loader:
        imgs.append(x); labs.append(y)
        if sum(t.shape[0] for t in imgs) >= n:
            break
    clean = torch.cat(imgs)[:n]
    assert (torch.cat(labs)[:n] == labels).all(), "arsiv etiketleri test sirasiyla uyusmuyor"

    # --- sabit es model ---
    P = load_model_auto(args.partner_type, args.partner_ckpt, device).eval()

    # --- taranan yorungenin checkpointleri ---
    ep_dir = Path(args.epochs_dir)
    ckpts = sorted(ep_dir.glob("epoch_*.pth"),
                   key=lambda p: int(re.search(r"epoch_(\d+)", p.name).group(1)))
    if not ckpts:
        sys.exit(f"{ep_dir}: epoch_*.pth yok")
    secilen = ckpts[::max(1, args.stride)]
    if secilen[-1] != ckpts[-1]:
        secilen.append(ckpts[-1])          # konverjan HER ZAMAN dahil
    print(f"secim: stride={args.stride} -> {len(secilen)} / {len(ckpts)} checkpoint")

    ilk = torch.load(secilen[0], map_location="cpu", weights_only=False)
    nc = infer_num_classes(ilk["model_state_dict"])
    M = ModelRegistry.get(args.model_type, num_classes=nc).to(device).eval()

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    for ck in secilen:
        ep = int(re.search(r"epoch_(\d+)", ck.name).group(1))
        hedef = out_dir / f"{args.trajectory_id}_ep{ep:04d}.json"
        if hedef.exists():
            print(f"  SKIP ep{ep}")
            continue
        M.load_state_dict(torch.load(ck, map_location="cpu", weights_only=False)["model_state_dict"])

        # ILERI: P -> M(c)   (salt ileri gecis)
        M_clean_ok, M_aw_fromP = maskeler(M, clean, adv_P, labels, device)
        ileri = oranlar(M_clean_ok, M_aw_fromP, P_clean_ok, P_adv_wrong_self)

        # GERI: M(c) -> P    (M(c) uzerinde PGD uretilir)
        adv_M = uret_adv(M, clean, labels, device)
        _, M_adv_wrong_self = maskeler(M, clean, adv_M, labels, device)
        P_clean_ok2, P_aw_fromM = maskeler(P, clean, adv_M, labels, device)
        assert np.array_equal(P_clean_ok, P_clean_ok2), \
            "P'nin temiz maskesi arsivdekinden farkli -- yukleme/on-isleme uyusmazligi"
        geri = oranlar(P_clean_ok, P_aw_fromM, M_clean_ok, M_adv_wrong_self)

        asim = {k: ileri[k] - geri[k] for k in PROTOKOLLER}
        e_M = float(100 * (1 - M_clean_ok.mean()))
        e_P = float(100 * (1 - P_clean_ok.mean()))
        kayit = {
            "kol": "A", "dataset": args.dataset, "kume": args.cluster,
            "trajectory_id": args.trajectory_id, "epoch": ep, "stride": args.stride,
            "n": int(n),
            "yon_ileri": f"{args.partner_type}->{args.model_type}@ep{ep}",
            "yon_geri": f"{args.model_type}@ep{ep}->{args.partner_type}",
            "e_hedef_ileri": e_M, "e_hedef_geri": e_P,
            "x_temiz_hata_farki": abs(e_M - e_P),
            "oranlar_ileri": ileri, "oranlar_geri": geri,
            "asimetri": {k: round(v, 4) for k, v in asim.items()},
            "y_asimetri_yayilimi": max(asim.values()) - min(asim.values()),
            "ozdeslik_artik_ileri": ileri["raw"] - (e_M + ileri["target_correct"] * (1 - e_M / 100)),
            "ozdeslik_artik_geri": geri["raw"] - (e_P + geri["target_correct"] * (1 - e_P / 100)),
        }
        hedef.write_text(json.dumps(kayit, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"  ep{ep:4d}: e_M={e_M:6.2f}  x={kayit['x_temiz_hata_farki']:6.2f}  "
              f"y={kayit['y_asimetri_yayilimi']:6.2f}  "
              f"ozdeslik_artik={kayit['ozdeslik_artik_ileri']:+.3f}/"
              f"{kayit['ozdeslik_artik_geri']:+.3f}", flush=True)


if __name__ == "__main__":
    main()
