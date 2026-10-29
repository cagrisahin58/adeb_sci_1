"""Konsey B1 zaman pilotu ve bekci kurali (KONSEY_PLANI.md §4 B3).

Her hucre icin (V_IN = vit_tiny_in1k, R224_IN = resnet18_224_in1k,
R224_scr = resnet18_224) gercek egitim bilesenleriyle olcum:
  * AT: 5 isinma + 50 olculen iterasyon, batch 64, AdversarialTraining
    (karisik kayip, PGD-10, eps 8/255, alpha 2/255), AdamW lr 1e-3 wd 0.05,
    gradyan kirpma 10 (AdversarialTrainer ile ayni adimlar)
  * temiz: 5 isinma + 50 olculen iterasyon, batch 128, AdamW
  * epok sonu degerlendirmesi: 2000 orneklik sabit val bolmesinde temiz
    ileri gecis (tam) ve PGD-10 (5 batch x 100 olculur, 20 batch'e olceklenir)
Epok suresi = iterasyon suresi x epok basina iterasyon (48000 egitim ornegi:
AT 750, temiz 375) + degerlendirme suresi. Veri yukleyici (num_workers=2) ve
ileri/geri gecis olcume dahildir.

Bekci: W(cap) = sum_kosular [temiz_epok x t_temiz + cap x t_AT] / 3600;
kosular V_IN x2 (30 temiz epok), R224_IN x2 (30), R224_scr x2 (200).
Egitim payi 38.15 sa. W(80) <= pay ise 80, degilse W(70), degilse W(60);
hicbiri tutmazsa egitim baslamaz. Ayrica R224 AT epogu > 365 s ise egitim
baslamaz (plan §10 risk tablosu).

Kullanim (konteynerde, depo kokunden; her cagri < 5 dk):
  python scripts/konsey_pilot_zaman.py --hucre V_IN
  python scripts/konsey_pilot_zaman.py --hucre R224_IN
  python scripts/konsey_pilot_zaman.py --hucre R224_scr
  python scripts/konsey_pilot_zaman.py --birlestir
Cikti: results/q1/konsey_pilot_zaman_parca_<hucre>.json ve
results/q1/konsey_pilot_zaman.json
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

HUCRE = {"V_IN": "vit_tiny_in1k", "R224_IN": "resnet18_224_in1k", "R224_scr": "resnet18_224"}
TEMIZ_EPOK = {"V_IN": 30, "R224_IN": 30, "R224_scr": 200}
KOSU_SAYISI = 2
PAY_SA = 38.15
CAPS = (80, 70, 60)
R224_AT_ESIK_S = 365.0
N_TRAIN = 48000
AT_BATCH, CLEAN_BATCH = 64, 128
N_WARM, N_MEAS = 5, 50
VAL_N, VAL_BATCH, VAL_PGD_BATCHES = 2000, 100, 5
OUT = Path("results/q1/konsey_pilot_zaman.json")


def nvsmi():
    """nvidia-smi anlik durumu (konteyner icinden); erisilemezse None."""
    q = ("nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu "
         "--format=csv,noheader,nounits")
    try:
        out = subprocess.run(q.split(), capture_output=True, text=True, timeout=10).stdout.strip()
        name, mu, mt, ut = [s.strip() for s in out.split(",")]
        procs = subprocess.run(
            ["nvidia-smi", "--query-compute-apps=pid,used_memory", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=10).stdout.strip()
        return {"zaman": time.strftime("%Y-%m-%d %H:%M:%S"), "gpu": name,
                "bellek_kullanilan_mib": int(mu), "bellek_toplam_mib": int(mt),
                "kullanim_yuzde": int(ut), "surecler": procs or "(listelenmedi)"}
    except Exception as e:  # noqa: BLE001
        return {"hata": f"{type(e).__name__}: {e}"}


def idle_util(n=5):
    """Kendi isimiz baslamadan once n saniye GPU kullanimi ornekle (baska is var mi)."""
    vals = []
    for _ in range(n):
        s = nvsmi()
        if "kullanim_yuzde" in s:
            vals.append(s["kullanim_yuzde"])
        time.sleep(1)
    return vals


def olc(hucre):
    from src.data import get_loaders_with_val
    from src.defenses.adversarial_training import AdversarialTraining
    from src.models import ModelRegistry

    dev = torch.device("cuda")
    torch.manual_seed(0)
    once = nvsmi()
    bos = idle_util()
    model = ModelRegistry.get(HUCRE[hucre], num_classes=10).to(dev)
    res = {"hucre": hucre, "tip": HUCRE[hucre], "nvidia_smi_once": once,
           "baska_is_kullanim_ornekleri_yuzde": bos}

    def timed_loop(loader, step_fn, n_warm, n_meas):
        it = iter(loader)
        for _ in range(n_warm):
            x, y = next(it)
            step_fn(x.to(dev, non_blocking=True), y.to(dev, non_blocking=True))
        torch.cuda.synchronize()
        t0 = time.perf_counter()
        for _ in range(n_meas):
            x, y = next(it)
            step_fn(x.to(dev, non_blocking=True), y.to(dev, non_blocking=True))
        torch.cuda.synchronize()
        return (time.perf_counter() - t0) / n_meas

    # --- AT iterasyonu (AdversarialTrainer.train_epoch ile ayni adimlar)
    tr_at, val_loader, _ = get_loaders_with_val(
        dataset="cifar10", data_dir="./data", batch_size=AT_BATCH,
        val_indices_path="data/val_split_indices.json")
    defense = AdversarialTraining(model=model, eps=8 / 255, alpha=2 / 255, steps=10, device=dev)
    opt = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.05)

    def at_step(x, y):
        model.train()
        opt.zero_grad()
        loss = defense.get_loss(model, x, y)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=10.0)
        opt.step()

    t_at_iter = timed_loop(tr_at, at_step, N_WARM, N_MEAS)
    res["nvidia_smi_at_sonrasi"] = nvsmi()

    # --- epok sonu degerlendirme: temiz (tam val) + PGD-10 (5 batch -> 20)
    model.eval()
    torch.cuda.synchronize()
    t0 = time.perf_counter()
    with torch.no_grad():
        for x, y in val_loader:
            model(x.to(dev)).argmax(1)
    torch.cuda.synchronize()
    t_val_clean = time.perf_counter() - t0
    vit = iter(val_loader)
    x, y = next(vit)
    defense.generate_adversarial(x.to(dev), y.to(dev))  # isinma
    torch.cuda.synchronize()
    t0 = time.perf_counter()
    for _ in range(VAL_PGD_BATCHES):
        x, y = next(vit)
        adv = defense.generate_adversarial(x.to(dev), y.to(dev))
        with torch.no_grad():
            model(adv).argmax(1)
    torch.cuda.synchronize()
    t_val_pgd = (time.perf_counter() - t0) / VAL_PGD_BATCHES * (VAL_N // VAL_BATCH)

    # --- temiz iterasyon
    tr_cl, _, _ = get_loaders_with_val(
        dataset="cifar10", data_dir="./data", batch_size=CLEAN_BATCH,
        val_indices_path="data/val_split_indices.json")
    crit = nn.CrossEntropyLoss()
    opt2 = optim.AdamW(model.parameters(), lr=1e-4, weight_decay=0.05)

    def cl_step(x, y):
        model.train()
        opt2.zero_grad()
        crit(model(x), y).backward()
        opt2.step()

    t_cl_iter = timed_loop(tr_cl, cl_step, N_WARM, N_MEAS)
    res["nvidia_smi_sonra"] = nvsmi()

    at_iters, cl_iters = -(-N_TRAIN // AT_BATCH), -(-N_TRAIN // CLEAN_BATCH)
    res.update({
        "at_iterasyon_s": round(t_at_iter, 4), "temiz_iterasyon_s": round(t_cl_iter, 4),
        "val_temiz_s": round(t_val_clean, 2), "val_pgd10_s_olceklenmis": round(t_val_pgd, 2),
        "at_iterasyon_epok": at_iters, "temiz_iterasyon_epok": cl_iters,
        "t_at_epok_s": round(t_at_iter * at_iters + t_val_clean + t_val_pgd, 1),
        "t_temiz_epok_s": round(t_cl_iter * cl_iters + t_val_clean, 1),
        "tepe_bellek_gib": round(torch.cuda.max_memory_allocated() / 2**30, 2),
    })
    return res


def birlestir():
    parca = {}
    for h in HUCRE:
        p = Path(f"results/q1/konsey_pilot_zaman_parca_{h}.json")
        if not p.exists():
            raise SystemExit(f"eksik parca: {p}")
        parca[h] = json.loads(p.read_text())
    t_at = {h: parca[h]["t_at_epok_s"] for h in HUCRE}
    t_cl = {h: parca[h]["t_temiz_epok_s"] for h in HUCRE}

    def W(cap):
        s = sum(KOSU_SAYISI * (TEMIZ_EPOK[h] * t_cl[h] + cap * t_at[h]) for h in HUCRE)
        return s / 3600.0

    w = {cap: round(W(cap), 2) for cap in CAPS}
    tavan = next((cap for cap in CAPS if W(cap) <= PAY_SA), None)
    t_R = max(t_at["R224_IN"], t_at["R224_scr"])
    r224_asim = t_R > R224_AT_ESIK_S
    baslamaz = tavan is None or r224_asim

    # Paylasim uyarisi: olcum anlarinda baska is var miydi
    uyarilar = []
    for h in HUCRE:
        ornek = parca[h].get("baska_is_kullanim_ornekleri_yuzde") or []
        once = parca[h].get("nvidia_smi_once", {})
        if ornek and max(ornek) > 10:
            uyarilar.append(f"{h}: olcumden once GPU kullanimi {ornek} (%); baska is calisiyordu, "
                            f"olcum SISMIS olabilir")
        if once.get("bellek_kullanilan_mib", 0) > 1024:
            uyarilar.append(f"{h}: olcumden once {once['bellek_kullanilan_mib']} MiB bellek baska "
                            f"surecte (histo-sparse-adv olabilir); kullanim orneklerine bakiniz")
    sisme = any("SISMIS" in u for u in uyarilar)

    out = {
        "tarih": time.strftime("%Y-%m-%d %H:%M:%S"),
        "yontem": ("50 olculen iterasyon (5 isinma), AT batch 64, temiz batch 128; epok = "
                   "iterasyon x (48000/batch) + val temiz + val PGD-10 (5/20 batch olceklenmis)"),
        "t_V_at_epok_s": t_at["V_IN"], "t_V_temiz_epok_s": t_cl["V_IN"],
        "t_R_at_epok_s": t_R, "t_R224_IN_at_epok_s": t_at["R224_IN"],
        "t_R224_scr_at_epok_s": t_at["R224_scr"],
        "t_Rc_temiz_epok_s": max(t_cl["R224_IN"], t_cl["R224_scr"]),
        "t_R224_IN_temiz_epok_s": t_cl["R224_IN"], "t_R224_scr_temiz_epok_s": t_cl["R224_scr"],
        "W_sa": {str(k): v for k, v in w.items()},
        "egitim_payi_sa": PAY_SA,
        "secilen_tavan": tavan,
        "r224_at_epok_esigi_s": R224_AT_ESIK_S,
        "r224_esik_asildi": r224_asim,
        "egitim_baslamaz": baslamaz,
        "kural": ("W(80)<=38.15 -> 80; degilse W(70) -> 70; degilse W(60) -> 60; hicbiri "
                  "tutmazsa ya da R224 AT epogu > 365 s ise egitim baslamaz, karar kullaniciya"),
        "kosu_basina_beklenen_sa_tavanda": (
            {h: round((TEMIZ_EPOK[h] * t_cl[h] + tavan * t_at[h]) / 3600, 2) for h in HUCRE}
            if tavan else None),
        "c1_vit_karsilastirma": ("C1 ViT AT epogu 179-182 s (TIMING.md), E2 medyan ust 219 s "
                                 "(KONSEY_PLANI §4); t_V bu aralikla karsilastirilmali"),
        "paylasim_uyarilari": uyarilar,
        "olcum_sismis_olabilir": sisme,
        # Ters yonlu risk: pilot bos GPU'da olculdu; egitim sirasinda GPU
        # paylasilirsa epok uzar. Dayanak: logs/Q1_e2_at_vit_tiny_2001.log,
        # epok 1 tqdm 686/688 iterasyon 03:39'da (yaklasik 0.32 s/iterasyon,
        # batch 64), bu pilotta V_IN 0.16 s/iterasyon.
        "paylasimda_iki_kat_yavaslama_W_sa": {str(k): round(2 * v, 2) for k, v in w.items()},
        "paylasim_notu": ("Pilot bos GPU'da olculdu. E2 kampanyasinda ayni ViT-Tiny AT iterasyonu "
                          "yaklasik 0.32 s idi (logs/Q1_e2_at_vit_tiny_2001.log); egitim GPU "
                          "paylasilarak kosulursa sureler iki katina cikabilir ve tavan 80'de "
                          "W pay 38.15 sa'i asar. Bekci kurali pilot degerine baglidir (plan "
                          "§4 B3); defterdeki gercek sureler izlenmelidir."),
        "parcalar": parca,
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps({k: out[k] for k in ("t_V_at_epok_s", "t_V_temiz_epok_s", "t_R_at_epok_s",
                                          "t_Rc_temiz_epok_s", "W_sa", "secilen_tavan",
                                          "egitim_baslamaz", "paylasim_uyarilari")},
                     indent=1, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hucre", choices=list(HUCRE))
    ap.add_argument("--birlestir", action="store_true")
    a = ap.parse_args()
    if a.birlestir:
        birlestir()
        return
    if not a.hucre:
        raise SystemExit("--hucre ya da --birlestir")
    res = olc(a.hucre)
    p = Path(f"results/q1/konsey_pilot_zaman_parca_{a.hucre}.json")
    p.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps({k: res[k] for k in ("hucre", "at_iterasyon_s", "temiz_iterasyon_s",
                                          "val_temiz_s", "val_pgd10_s_olceklenmis",
                                          "t_at_epok_s", "t_temiz_epok_s", "tepe_bellek_gib",
                                          "baska_is_kullanim_ornekleri_yuzde")}, indent=1))


if __name__ == "__main__":
    main()
