"""E3: protokol-yayilimi kalibrasyon egrisi - nokta uretimi + regresyon.

Tezin omurgasi (Q1 raporu E3): x = hedefin temiz hatasi, y1 = ham-kosullu
sapma, y2 = 4-protokol yayilimi. Noktalar uc kaynaktan gelir:
  (a) E1/E2 yorunge checkpoint'leri (save_every ile kayitli; TEMIZ-DOGRULUK
      KANTILLERINE gore secilir - on-kayitli kriter asagida),
  (b) butce-eslesmis dogrulama kosulari,
  (c) dogal cesitlilik (final modeller, WRN, E5 cifti).

ON-KAYIT (kosumdan once sabitlendi; p-hacking'e karsi):
  Kantil kriteri: her yorungeden, temiz-dogrulugu {%40, %50, %60, %70, %80,
  konverjan} hedeflerine EN YAKIN checkpoint'ler alinir (ayni checkpoint iki
  hedefe en yakinsa bir kez sayilir). Istatistik: OLS y = b0 + b1 x;
  yorunge-duzeyi KUME bootstrap (B=10.000) ile b1 ve r GA'lari; dogrusal
  olmama kontrolu karesel terim; gurbuz dogruluk kovaryat olarak coklu
  regresyona eklenir.

Iki alt komut:
  points  : bir hedef-yorungenin checkpoint'lerini arsivlenmis kaynak
            saldirilariyla degerlendirir (salt ileri gecis) -> nokta json'lari
  fit     : tum nokta json'larini toplar, kume bootstrap regresyonu kosar

Kullanim:
  python scripts/q1_e3_calibration.py points \
      --epochs-dir models/q1/e2/resnet18_s1001/.../epochs \
      --model-type resnet18 --dataset cifar10 \
      --adv-archive results/q1/adv_archive/vit_tiny_s2001_pgd10.npz \
      --trajectory-id e2_rn18_s1001_from_vit \
      --out-dir results/q1/e3_points
  python scripts/q1_e3_calibration.py fit \
      --points-dir results/q1/e3_points --out results/q1/e3_fit.json
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
import os
os.chdir(ROOT)

from src.data import DATASETS, get_loaders  # noqa: E402
from src.models import ModelRegistry  # noqa: E402
from src.utils.load_model_auto import infer_num_classes  # noqa: E402

CLEAN_TARGETS = [40.0, 50.0, 60.0, 70.0, 80.0, None]  # None = konverjan (son ckpt)


@torch.no_grad()
def eval_target(model, clean_images, adv_images, labels, device, bs=200):
    """Hedef modelde temiz-dogru ve adv-yanlis maskeleri (salt ileri gecis)."""
    clean_ok, adv_wrong = [], []
    for lo in range(0, len(labels), bs):
        hi = min(lo + bs, len(labels))
        xb = clean_images[lo:hi].to(device)
        ab = adv_images[lo:hi].to(device)
        yb = labels[lo:hi].to(device)
        clean_ok.append((model(xb).argmax(1) == yb).cpu().numpy())
        adv_wrong.append((model(ab).argmax(1) != yb).cpu().numpy())
    return np.concatenate(clean_ok), np.concatenate(adv_wrong)


def protocol_rates(clean_ok, adv_wrong, src_clean_ok, src_adv_wrong):
    """4 protokol orani + ham-kosullu sapma + yayilim."""
    def rate(mask):
        return float(100 * adv_wrong[mask].mean()) if mask.sum() else float("nan")
    raw = float(100 * adv_wrong.mean())
    tc = rate(clean_ok)
    bc = rate(clean_ok & src_clean_ok)
    ss = rate(clean_ok & src_adv_wrong)
    vals = [raw, tc, bc, ss]
    return {
        "raw": raw, "target_correct": tc, "both_correct": bc, "successful_source": ss,
        "raw_minus_cond": raw - tc,
        "spread": max(vals) - min(vals),
    }


def cmd_points(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    arc = np.load(args.adv_archive, allow_pickle=True)
    adv = torch.from_numpy(arc["adv_uint8"]).float() / 255.0
    labels = torch.from_numpy(arc["labels"])
    src_adv_wrong = arc["source_adv_wrong"].astype(bool)

    # Temiz goruntuleri ayni sirayla yukle
    _, test_loader = get_loaders(dataset=args.dataset, data_dir="./data",
                                 test_batch_size=500)
    imgs, labs = [], []
    for x, y in test_loader:
        imgs.append(x); labs.append(y)
        if sum(t.shape[0] for t in imgs) >= len(labels):
            break
    clean_images = torch.cat(imgs)[:len(labels)]
    assert (torch.cat(labs)[:len(labels)] == labels).all(), \
        "arsiv etiketleri test sirasiyla uyusmuyor"

    # Kaynak temiz-dogru maskesi: arsiv v2'de dogrudan var; eski arsivler icin
    # --src-clean-mask ile pgd_per_sample npz'inden alinabilir.
    if "source_clean_correct" in arc:
        src_clean_ok = arc["source_clean_correct"].astype(bool)
    elif args.src_clean_mask:
        src_clean_ok = np.load(args.src_clean_mask)["clean_correct"].astype(bool)
    else:
        raise SystemExit("Arsivde source_clean_correct yok ve --src-clean-mask "
                         "verilmedi; both_correct hesaplanamaz.")

    ep_dir = Path(args.epochs_dir)
    ckpts = sorted(ep_dir.glob("epoch_*.pth"),
                   key=lambda p: int(re.search(r"epoch_(\d+)", p.name).group(1)))
    if not ckpts:
        raise FileNotFoundError(f"{ep_dir}: epoch_*.pth yok")

    # metrics.jsonl'den temiz dogruluklar (kantil secimi icin); eksik epoch'lar
    # icin checkpoint payload'indaki clean_acc/test_acc'e dusulur. NOT (on-kayit
    # belgesi): kantil secimi VAL temiz dogruluguyla, regresyon x'i TEST temiz
    # hatasiyla yapilir; E1 yorungelerinde "konverjan" = erken-durma epoch'u,
    # E2'de (patience=0) tam-butce son epoch'tur.
    metr = {}
    mfile = ep_dir / "metrics.jsonl"
    if mfile.exists():
        for line in mfile.read_text().splitlines():
            d = json.loads(line)
            metr[d["epoch"]] = d.get("clean_acc")

    entries = []
    for ck in ckpts:
        ep = int(re.search(r"epoch_(\d+)", ck.name).group(1))
        clean = metr.get(ep)
        if clean is None:
            payload = torch.load(ck, map_location="cpu", weights_only=False)
            clean = payload.get("clean_acc", payload.get("test_acc"))
        entries.append((ep, clean, ck))

    # --- SECIM ---
    # ON-KAYITLI kantil kriteri TERK EDILDI (E3_YENIDEN_TASARIM §1): 12 yorunge
    # x 6 hedef = 72 hedef yalniz 38 AYRI NOKTA uretiyordu (%47,2 cokme), cunku
    # birden fazla hedef ayni epoga dusuyordu. Artik varsayilan TUM
    # checkpointlerdir; --stride ile seyreltilebilir ve seyreltme kayda gecer.
    # Eski davranis --quantile-mode ile hala erisilebilir (karsilastirma icin).
    if args.quantile_mode:
        chosen = {}
        skipped_targets = []
        for tgt in CLEAN_TARGETS:
            if tgt is None:
                ep, _, ck = entries[-1]
            else:
                known = [(abs(c - tgt), ep, ck) for ep, c, ck in entries if c is not None]
                if not known:
                    skipped_targets.append(tgt)
                    continue
                _, ep, ck = min(known)
            chosen[ep] = ck
        if skipped_targets:
            raise SystemExit(
                f"HATA: {ep_dir} icin clean_acc verisi yok; {skipped_targets} kantil "
                f"hedefleri atlanacakti. Sessiz tek-nokta yorungesi kabul edilmez; "
                f"metrics.jsonl'i veya checkpoint payload'larini kontrol edin.")
        secim_kipi = "kantil (ESKI)"
        print(f"kantil secimi: {sorted(chosen)} ({len(chosen)} checkpoint)")
    else:
        sec = entries[::max(1, args.stride)]
        # son checkpoint (konverjan) HER ZAMAN dahil -- yorungenin ucu duser
        if entries and sec[-1][0] != entries[-1][0]:
            sec.append(entries[-1])
        chosen = {ep: ck for ep, _c, ck in sec}
        secim_kipi = f"tum-checkpoint (stride={args.stride})"
        print(f"secim: {secim_kipi} -> {len(chosen)} / {len(entries)} checkpoint")

    first = torch.load(next(iter(chosen.values())), map_location="cpu", weights_only=False)
    nc = infer_num_classes(first["model_state_dict"])
    model = ModelRegistry.get(args.model_type, num_classes=nc).to(device).eval()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for ep in sorted(chosen):
        payload = torch.load(chosen[ep], map_location="cpu", weights_only=False)
        model.load_state_dict(payload["model_state_dict"])
        clean_ok, adv_wrong = eval_target(model, clean_images, adv, labels, device)
        rates = protocol_rates(clean_ok, adv_wrong, src_clean_ok, src_adv_wrong)
        _e = float(100 * (1 - clean_ok.mean()))
        # OZDESLIK SAGLAMASI (EK B.5): ham = e + kos*(1-e) beklenir.
        # Artik sifirdan anlamli sapiyorsa "temiz-yanlis ornekler saldiri
        # altinda yanlis kalir" onculu bozulmus demektir; bu KENDI BASINA
        # raporlanmasi gereken bir bulgudur.
        _ham_tahmin = _e + rates["target_correct"] * (1 - _e / 100.0)
        point = {
            "trajectory_id": args.trajectory_id,
            "arm": args.arm,
            "secim_kipi": secim_kipi,
            "stride": (None if args.quantile_mode else args.stride),
            "epoch": ep,
            "target_clean_acc": float(100 * clean_ok.mean()),
            "target_clean_err": _e,
            "source_archive": str(args.adv_archive),
            "dataset": args.dataset,
            "ozdeslik_ham_tahmin": _ham_tahmin,
            "ozdeslik_artik": rates["raw"] - _ham_tahmin,
            **rates,
        }
        fname = out_dir / f"{args.trajectory_id}_ep{ep:03d}.json"
        with open(fname, "w") as f:
            json.dump(point, f, indent=1)
        print(f"  ep{ep:3d}: clean {point['target_clean_acc']:5.2f}  "
              f"raw-cond {point['raw_minus_cond']:5.2f}  spread {point['spread']:5.2f}")


def cmd_fit(args):
    pts = []
    for p in sorted(Path(args.points_dir).glob("*.json")):
        pts.append(json.load(open(p)))
    if len(pts) < 6:
        raise SystemExit(f"cok az nokta ({len(pts)}); once points komutunu kosun")

    # KOLLAR AYRI (E3_YENIDEN_TASARIM §B.3): havuzlanmis uydurma URETILMEZ.
    # Kod duzeyinde de uretilemez: asagidaki dongu yalniz kol alt kumeleri
    # uzerinde calisir, "hepsi" diye bir kol YOKTUR.
    kollar = sorted({p.get("arm", "?") for p in pts})
    if "?" in kollar:
        raise SystemExit("HATA: bazi noktalarda 'arm' alani yok. Kol etiketi "
                         "olmadan kollari ayirmak imkansiz; points komutunu "
                         "--arm ile yeniden kosun.")

    def cluster_bootstrap(y, x, traj, uniq, B=10000, seed=42):
        """Yorunge-duzeyi kume bootstrap: noktalar bagimsiz DEGIL (on-kayit).

        Serbestlik derecesini NOKTA sayisi degil YORUNGE sayisi belirler;
        yeniden orneklem yorunge duzeyinde yapilir.
        """
        rng = np.random.default_rng(seed)
        slopes, rs = [], []
        for _ in range(B):
            take = rng.choice(uniq, size=len(uniq), replace=True)
            idx = np.concatenate([np.flatnonzero(traj == t) for t in take])
            if len(set(x[idx])) < 3:
                continue
            b1, b0 = np.polyfit(x[idx], y[idx], 1)
            slopes.append(b1)
            rs.append(np.corrcoef(x[idx], y[idx])[0, 1])
        if not slopes:
            return ([float("nan")] * 2, [float("nan")] * 2)
        return (np.percentile(slopes, [2.5, 97.5]).tolist(),
                np.percentile(rs, [2.5, 97.5]).tolist())

    out = {
        "HAVUZLAMA": "YAPILMADI -- kollar ayri raporlanir (E3_YENIDEN_TASARIM B.3). "
                     "Manset iki kolun EGIMLERININ UYUSMASIDIR, ortak bir uydurma degil.",
        "BIRINCIL_NICELIK": "spread (4 protokolun urettigi asimetri yayilimi). "
                            "raw_minus_cond IKINCILDIR: ozdeslikle turetilebilir "
                            "oldugu icin saglama gorevi gorur (EK B).",
        "kollar": {},
    }
    for kol in kollar:
        alt = [p for p in pts if p.get("arm") == kol]
        if len(alt) < 6:
            out["kollar"][kol] = {"n_points": len(alt), "DURUM": "COK AZ NOKTA, uydurulmadi"}
            continue
        x = np.array([p["target_clean_err"] for p in alt])
        traj = np.array([p["trajectory_id"] for p in alt])
        uniq = sorted(set(traj))
        artik = np.array([p.get("ozdeslik_artik", float("nan")) for p in alt])
        kol_out = {
            "n_points": len(alt),
            "n_trajectories": len(uniq),
            "SERBESTLIK_DERECESI_NOTU":
                f"Cikarim {len(uniq)} YORUNGE uzerinden kume bootstrap iledir. "
                f"n={len(alt)} nokta SERBESTLIK DERECESI DEGILDIR; metinde "
                f"'n={len(alt)} nokta' seklinde sunmak sahte kesinlik verir.",
            "clean_err_range": [float(x.min()), float(x.max())],
            "ozdeslik_artik_puan": {
                "mutlak_ort": float(np.nanmean(np.abs(artik))),
                "mutlak_max": float(np.nanmax(np.abs(artik))),
            },
        }
        for label, key in (("spread", "spread"), ("raw_minus_cond", "raw_minus_cond")):
            y = np.array([p[key] for p in alt])
            b1, b0 = np.polyfit(x, y, 1)
            r = float(np.corrcoef(x, y)[0, 1])
            q = np.polyfit(x, y, 2)
            resid_lin = float(np.mean((np.polyval([b1, b0], x) - y) ** 2))
            resid_quad = float(np.mean((np.polyval(q, x) - y) ** 2))
            ci_b1, ci_r = cluster_bootstrap(y, x, traj, uniq)
            kol_out[label] = {
                "slope": float(b1), "intercept": float(b0), "pearson_r": r,
                "slope_ci95_cluster_bootstrap": ci_b1,
                "r_ci95_cluster_bootstrap": ci_r,
                "mse_linear": resid_lin, "mse_quadratic": resid_quad,
            }
        out["kollar"][kol] = kol_out

    # iki kol da uydurulduysa EGIM UYUSMASI (manset) raporlanir
    uygun = [k for k, v in out["kollar"].items() if "spread" in v]
    if len(uygun) == 2:
        a, b = uygun
        sa = out["kollar"][a]["spread"]["slope"]
        sb = out["kollar"][b]["spread"]["slope"]
        ca = out["kollar"][a]["spread"]["slope_ci95_cluster_bootstrap"]
        cb = out["kollar"][b]["spread"]["slope_ci95_cluster_bootstrap"]
        ortusuyor = not (ca[1] < cb[0] or cb[1] < ca[0])
        out["EGIM_UYUSMASI"] = {
            "kol_" + a: {"egim": sa, "GA": ca},
            "kol_" + b: {"egim": sb, "GA": cb},
            "GA_ortusuyor_mu": bool(ortusuyor),
            "yorum": ("Iki kolun egimleri ortusuyor: kontrollu ve gozlemsel "
                      "kanit ayni yonu veriyor."
                      if ortusuyor else
                      "Iki kolun egimleri ORTUSMUYOR. Bu, gozlemsel koldaki "
                      "karistiriciların etkisine isarettir ve RAPORLANMALIDIR "
                      "(K8); havuzlama yine YAPILMAZ."),
        }
    else:
        out["EGIM_UYUSMASI"] = {"DURUM": f"iki kol da uydurulamadi (uygun: {uygun})"}

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=1, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("points")
    p1.add_argument("--epochs-dir", required=True)
    p1.add_argument("--model-type", required=True)
    p1.add_argument("--dataset", choices=sorted(DATASETS), default="cifar10")
    p1.add_argument("--adv-archive", required=True,
                    help="q1_archive_adv.py ciktisi (kaynak sabit)")
    p1.add_argument("--src-clean-mask", default=None,
                    help="Kaynagin pgd_per_sample_*.npz'i (clean_correct maskesi)")
    p1.add_argument("--trajectory-id", required=True)
    p1.add_argument("--out-dir", required=True)
    # E3_YENIDEN_TASARIM §B.3: kol etiketi ZORUNLU. A = kontrollu (yorunge-ici,
    # cift uyesi sabit), B = gozlemsel (mimari/tohum/veri kumesi degisiyor).
    p1.add_argument("--arm", required=True, choices=["A", "B"],
                    help="A=kontrollu (yorunge-ici)  B=gozlemsel")
    p1.add_argument("--stride", type=int, default=1,
                    help="her N. checkpoint (1=hepsi). Seyreltme nokta json'una yazilir.")
    p1.add_argument("--quantile-mode", action="store_true",
                    help="ESKI on-kayitli kantil secimi (terk edildi; yalniz karsilastirma icin)")
    p2 = sub.add_parser("fit")
    p2.add_argument("--points-dir", required=True)
    p2.add_argument("--out", required=True)
    args = ap.parse_args()
    if args.cmd == "points":
        cmd_points(args)
    else:
        cmd_fit(args)


if __name__ == "__main__":
    main()
