#!/usr/bin/env python3
"""B.8: CIFAR-100'de secim bandi -- VEKIL degil GERCEK TEST uzerinde.

BORC (E1_PILOT_KAPISI B.8 · IS-6a). Makalede su niteleme duruyor: E1'in
on-kayitli bantlari 0,22-0,48 puan marjla tuttu, oysa secim protokolu tek
basina raporlanan sayiyi 1,58-2,85 puan oynatiyor. Ama o genlik CIFAR-10'da
(E2) olculmustu; CIFAR-100 icin dogrudan olcum yoktu.

NEDEN DOGRUDAN E2 IZGARASI KOSULAMAZ. E2 izgarasi UC serbestlik derecesi tarar:
secici BOLME (V_B/V_C) x patience x yumusatma = 18 hucre. A/B/C bolmeleri E2'ye
(sizinti ablasyonu) OZGUDUR; CIFAR-100 tek bolme kullanmistir. Dolayisiyla
CIFAR-100'de BOLME boyutu YOKTUR.

DOGRU KARSILASTIRMA. Iki veri kumesinde de AYNI iki boyut taranir:
    patience (0, 10, 20)  x  yumusatma (k = 1, 3, 5)  =  9 hucre
CIFAR-10 icin bu, HER BOLME ICIN AYRI hesaplanir; CIFAR-100 icin tek bolme
uzerinde. Boylece "9 hucrelik yayilim" iki kumede AYNI NICELIKTIR.
E2'nin 18 hucrelik yayilimiyla KARSILASTIRILMAZ ve cikti bunu yazar.

Girdi:
  CIFAR-100 val : models/q1/cifar100/<arch>_s<seed>/.../epochs/metrics.jsonl
  CIFAR-100 test: results/q1/cifar100/testcurve/testcurve_<arch>_s<seed>.npz
  CIFAR-10      : results/q1/e2/ (mevcut E2 artefaktlari)
Cikti: results/q1/b8_secim_bandi.json
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT / "scripts"))
from q1_offline_select import simulate_selection  # noqa: E402
from q1_e2_grid import smooth  # noqa: E402

MIN_DELTA = 0.1
PATIENCES = [0, 10, 20]
KERNELS = [1, 3, 5]
TOHUM = {"cifar100": {"resnet18": [1001, 1002, 1003], "vit_tiny": [2001, 2002, 2003]},
         "cifar10": {"resnet18": [1001, 1002, 1003], "vit_tiny": [2001, 2002, 2003]}}


def hucre(epochs, val_adv, val_clean, test_adv, patience, k):
    adv = smooth(val_adv, k, "edge")
    cln = smooth(val_clean, k, "edge")
    sel, _, _ = simulate_selection(list(zip(epochs.tolist(), cln.tolist(), adv.tolist())),
                                   patience=patience, min_delta=MIN_DELTA)
    if sel is None:
        return None
    i = int(np.where(epochs == sel)[0][0])
    return {"patience": patience, "k": k, "secilen_epok": int(sel),
            "test_adv": round(float(test_adv[i]), 4)}


def izgara9(epochs, val_adv, val_clean, test_adv):
    hs = [hucre(epochs, val_adv, val_clean, test_adv, p, k)
          for p in PATIENCES for k in KERNELS]
    hs = [h for h in hs if h]
    if len(hs) < 2:
        return None
    v = np.array([h["test_adv"] for h in hs])
    return {"n_hucre": len(hs), "yayilim": round(float(v.max() - v.min()), 4),
            "sd": round(float(v.std(ddof=1)), 4),
            "min": float(v.min()), "max": float(v.max()),
            "essiz_epok": sorted({h["secilen_epok"] for h in hs}), "hucreler": hs}


def c100_yorunge(arch, seed):
    m = ROOT / f"models/q1/cifar100/{arch}_s{seed}/{arch}/adv/adversarial_training/epochs/metrics.jsonl"
    tc = ROOT / f"results/q1/cifar100/testcurve/testcurve_{arch}_s{seed}.npz"
    if not m.exists() or not tc.exists():
        return None
    rows = []
    for line in m.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        if d.get("adv_acc") is not None:
            rows.append((int(d["epoch"]), float(d.get("clean_acc", np.nan)), float(d["adv_acc"])))
    rows.sort()
    z = np.load(tc)
    te_ep = z["epochs"].astype(int)
    ep = np.array([r[0] for r in rows])
    # val ve test epok dizileri ORTAK kesisimle hizalanir (test --save-every ile
    # seyrek olabilir); hizalanmazsa sessizce YANLIS epok okunurdu.
    ortak = np.intersect1d(ep, te_ep)
    if ortak.size < 4:
        return None
    # BUTUNLUK: kesik yazilmis (0 bayt) bir kontrol noktasi test egrisinde
    # SESSIZ bir delik birakiyordu; intersect1d onu gorunmez kiliyordu ve
    # yumusatma penceresi delikli izgarada komsu olmayan epoklari komsu
    # sayiyordu. Delik artik bildiriliyor.
    _delik = sorted(set(range(int(ortak.min()), int(ortak.max()) + 1))
                    - set(int(e) for e in ortak))
    if _delik:
        print(f"  UYARI epok deligi {tc.name}: {_delik} "
              f"(yumusatma penceresi bu noktalarda kayiktir)")
    vi = np.searchsorted(ep, ortak)
    ti = np.searchsorted(te_ep, ortak)
    return (ortak,
            np.array([rows[j][2] for j in vi]),
            np.array([rows[j][1] for j in vi]),
            z["adv_acc"].astype(float)[ti])


def c10_yorunge(arch, seed, split):
    tc = ROOT / f"results/q1/e2/testcurve_{arch}_s{seed}.npz"
    vc = ROOT / f"results/q1/e2/select_{arch}_s{seed}_val{split}_valcurve.npz"
    if not tc.exists() or not vc.exists():
        return None
    z, v = np.load(tc), np.load(vc)
    return (z["epochs"].astype(int),
            100.0 * v["adv_mask"].mean(axis=1),
            100.0 * v["clean_mask"].mean(axis=1),
            z["adv_acc"].astype(float))


sonuc = {
    "uretildi_utc": datetime.now(timezone.utc).isoformat(),
    "NICELIK": "9 hucrelik (patience x yumusatma) secim yayilimi, GERCEK test "
               "PGD-10 uzerinde. E2'nin 18 hucrelik (bolme x patience x "
               "yumusatma) yayilimiyla KARSILASTIRILMAZ -- bolme boyutu "
               "CIFAR-100'de YOKTUR.",
    "izgara": {"patience": PATIENCES, "yumusatma_k": KERNELS, "hucre": 9,
               "yumusatma_konvansiyonu": "kenar-dolgulu merkezi hareketli ortalama"},
    "veri_kumeleri": {},
}

# --- CIFAR-100 (tek bolme) ---
c100 = {}
for arch, seeds in TOHUM["cifar100"].items():
    for s in seeds:
        t = c100_yorunge(arch, s)
        if t is None:
            continue
        g = izgara9(*t)
        if g:
            c100[f"{arch}_s{s}"] = g
if c100:
    yay = [v["yayilim"] for v in c100.values()]
    sonuc["veri_kumeleri"]["cifar100"] = {
        "bolme": "tek (E1 protokolu)", "yorungeler": c100,
        "yayilim_araligi": [min(yay), max(yay)], "yayilim_ort": round(float(np.mean(yay)), 4)}

# --- CIFAR-10 (BOLME BASINA ayri; boylece 9 hucre / 9 hucre) ---
c10 = {}
for arch, seeds in TOHUM["cifar10"].items():
    for s in seeds:
        for sp in ("B", "C"):
            t = c10_yorunge(arch, s, sp)
            if t is None:
                continue
            g = izgara9(*t)
            if g:
                c10[f"{arch}_s{s}_val{sp}"] = g
if c10:
    yay = [v["yayilim"] for v in c10.values()]
    sonuc["veri_kumeleri"]["cifar10"] = {
        "bolme": "V_B ve V_C AYRI (her biri 9 hucre)", "yorungeler": c10,
        "yayilim_araligi": [min(yay), max(yay)], "yayilim_ort": round(float(np.mean(yay)), 4)}

a = sonuc["veri_kumeleri"].get("cifar100")
b = sonuc["veri_kumeleri"].get("cifar10")
if a and b:
    sonuc["HUKUM"] = (
        f"CIFAR-100'de 9 hucrelik secim yayilimi {a['yayilim_araligi'][0]}-"
        f"{a['yayilim_araligi'][1]} puan (ort {a['yayilim_ort']}); ayni nicelik "
        f"CIFAR-10'da bolme basina {b['yayilim_araligi'][0]}-{b['yayilim_araligi'][1]} "
        f"puan (ort {b['yayilim_ort']}). Bu, makaledeki nitelemeyi CIFAR-10 "
        "olcumune dayanmaktan cikarip CIFAR-100'un KENDI olcumune baglar.")
elif a:
    sonuc["HUKUM"] = "Yalniz CIFAR-100 olculebildi; CIFAR-10 artefaktlari eksik."
else:
    sonuc["HUKUM"] = ("CIFAR-100 test egrileri HENUZ YOK (q1_e2_test_curve.py "
                      "--dataset cifar100 kosuyor olabilir). Bu bir BASARISIZLIK DEGILDIR.")

out = ROOT / "results/q1/b8_secim_bandi.json"
out.write_text(json.dumps(sonuc, indent=2, ensure_ascii=False), encoding="utf-8")
for ds, v in sonuc["veri_kumeleri"].items():
    print(f"{ds:9s} ({v['bolme']}): {len(v['yorungeler'])} yorunge  "
          f"yayilim {v['yayilim_araligi'][0]}-{v['yayilim_araligi'][1]} puan "
          f"(ort {v['yayilim_ort']})")
print()
print("HUKUM:", sonuc["HUKUM"])
print(f"-> {out}")
