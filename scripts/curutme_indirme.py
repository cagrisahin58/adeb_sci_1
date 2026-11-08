# -*- coding: utf-8 -*-
"""Curutme zinciri indirme adimi (08.11.2026): A ve C bloklarinin agirliklari.

Konteynerde, depo kokunden ve su ortam degiskenleriyle kosar (zincir betigi export eder):
  TORCH_HOME=/mnt/d/adeb_sci_1_veri/onbellek/torch   HF_HOME=/mnt/d/adeb_sci_1_veri/onbellek/hf

Yaptiklari (idempotent; dosya varsa yalniz dogrular):
  1. XCiT-S12/M12/L12 (RobustBench cifar10 Linf, Debenedetti ve ark. 2022): S12 depodaki kopyadan
     (models/robustbench_zoo/cifar10/Linf/Debenedetti2022Light_XCiT-S12.pth.tar) torch hub onbellegine
     konur; M12 ve L12 RobustBench'in kendi yukleyicisiyle (timm + GitHub surum adresi) indirilir.
  2. timm agirliklari vit_tiny_patch16_224.augreg_in21k_ft_in1k (apache-2.0) ve
     resnet18.fb_swsl_ig1b_ft_in1k (CC-BY-NC-4.0; DAGITILMAZ) HF hub'dan indirilir, D diskinde
     /mnt/d/adeb_sci_1_veri/models/timm_agirliklar/<ad>/model.safetensors altina kopyalanir ve depoda
     models/timm_agirliklar/<ad> sembolik bagi kurulur (src/models/r224.py LOCAL_WEIGHT_DIR bu yolu okur;
     boylece INIT_WEIGHTS_RAPORU kaynak dosyanin sha256'sini yazar).
  3. Manipulasyon denetimi (02_deney_adaylari.json C1.manipulasyon_denetimi): yerel dosyanin sha256'si
     HF LFS ozetiyle eslesmeli; yeni agirligin mevcut IN-1k agirligindan (deit_tiny / resnet18.a1)
     farkli oldugu (bas disi ortak anahtarlarda fark normu > 0) kayda gecer.
Cikti: results/q1/curutme_2026-11-08/indirme_sha256.txt (sha256sum bicimi) ve indirme_denetimi.json.
Cikis kodu: 0 hepsi tamam; 3 sha256 uyusmazligi ya da fark normu 0; 4 indirme hatasi.
"""
import hashlib
import io
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
os.chdir(KOK)
CIKTI = KOK / "results" / "q1" / "curutme_2026-11-08"
D_TIMM = Path("/mnt/d/adeb_sci_1_veri/models/timm_agirliklar")
XCIT = {
    "Debenedetti2022Light_XCiT-S12": "debenedetti2022light-xcit-s-cifar10-linf.pth.tar",
    "Debenedetti2022Light_XCiT-M12": "debenedetti2022light-xcit-m-cifar10-linf.pth.tar",
    "Debenedetti2022Light_XCiT-L12": "debenedetti2022light-xcit-l-cifar10-linf.pth.tar",
}
# yeni agirlik -> (karsilastirma agirligi, lisans)
TIMM = {
    "vit_tiny_patch16_224.augreg_in21k_ft_in1k": ("deit_tiny_patch16_224.fb_in1k", "apache-2.0"),
    "resnet18.fb_swsl_ig1b_ft_in1k": ("resnet18.a1_in1k", "cc-by-nc-4.0 (agirlik dagitilmaz)"),
}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    import torch

    for d in ("TORCH_HOME", "HF_HOME"):
        print(f"{d}={os.environ.get(d)}")
    CIKTI.mkdir(parents=True, exist_ok=True)
    kayit = {"uretildi_utc": datetime.now(timezone.utc).isoformat(), "torch_hub": torch.hub.get_dir(),
             "hf_home": os.environ.get("HF_HOME"), "xcit": {}, "timm": {}, "hatalar": []}
    satirlar = []

    # 1. XCiT
    hub = Path(torch.hub.get_dir()) / "checkpoints"
    hub.mkdir(parents=True, exist_ok=True)
    s12_yerel = KOK / "models/robustbench_zoo/cifar10/Linf/Debenedetti2022Light_XCiT-S12.pth.tar"
    if not (hub / XCIT["Debenedetti2022Light_XCiT-S12"]).exists() and s12_yerel.exists():
        shutil.copy2(s12_yerel, hub / XCIT["Debenedetti2022Light_XCiT-S12"])
        print("S12 depodaki kopyadan hub onbellegine kondu")
    from robustbench.utils import load_model
    for ad, dosya in XCIT.items():
        try:
            m = load_model(model_name=ad, dataset="cifar10", threat_model="Linf",
                           model_dir="models/robustbench_zoo")
            n_param = sum(p.numel() for p in m.parameters())
            del m
        except Exception as e:  # noqa: BLE001
            kayit["hatalar"].append(f"{ad}: {e!r}")
            print("HATA", ad, e)
            continue
        p = hub / dosya
        s = sha256(p)
        kayit["xcit"][ad] = {"dosya": str(p), "bayt": p.stat().st_size, "sha256": s, "param": n_param}
        satirlar.append(f"{s}  {p}")
        print(ad, s, p.stat().st_size, n_param)
    if (s12_yerel.exists() and "Debenedetti2022Light_XCiT-S12" in kayit["xcit"]):
        kayit["xcit"]["Debenedetti2022Light_XCiT-S12"]["depodaki_kopya_ile_ayni"] = (
            sha256(s12_yerel) == kayit["xcit"]["Debenedetti2022Light_XCiT-S12"]["sha256"])

    # 2-3. timm
    from huggingface_hub import HfApi, hf_hub_download
    from safetensors.torch import load_file
    api = HfApi()
    for ad, (karsi, lisans) in TIMM.items():
        repo = f"timm/{ad}"
        try:
            onb = hf_hub_download(repo_id=repo, filename="model.safetensors")
        except Exception as e:  # noqa: BLE001
            kayit["hatalar"].append(f"{ad}: indirme {e!r}")
            print("HATA", ad, e)
            continue
        hedef_dir = D_TIMM / ad
        hedef_dir.mkdir(parents=True, exist_ok=True)
        hedef = hedef_dir / "model.safetensors"
        if not hedef.exists() or sha256(hedef) != sha256(onb):
            shutil.copy2(onb, hedef)
        bag = KOK / "models" / "timm_agirliklar" / ad
        if bag.is_symlink() or bag.exists():
            bag_durum = f"var ({os.readlink(bag) if bag.is_symlink() else 'gercek klasor'})"
        else:
            bag.parent.mkdir(parents=True, exist_ok=True)
            os.symlink(str(hedef_dir), str(bag))
            bag_durum = f"kuruldu -> {hedef_dir}"
        s = sha256(hedef)
        try:
            info = api.get_paths_info(repo, ["model.safetensors"], expand=True)[0]
            hf_sha = getattr(getattr(info, "lfs", None), "sha256", None)
            hf_boyut = getattr(info, "size", None)
        except Exception as e:  # noqa: BLE001
            hf_sha, hf_boyut = None, None
            kayit["hatalar"].append(f"{ad}: HF LFS ozeti okunamadi {e!r}")
        # bas disi ortak anahtarlarda fark normu (yeni - mevcut IN-1k agirligi)
        karsi_p = KOK / "models" / "timm_agirliklar" / karsi / "model.safetensors"
        fark = None
        n_ortak = 0
        if karsi_p.exists():
            a_sd, b_sd = load_file(str(hedef)), load_file(str(karsi_p))
            kare = 0.0
            for k, v in a_sd.items():
                if k.startswith(("head", "fc.")) or k not in b_sd or b_sd[k].shape != v.shape:
                    continue
                kare += float(((v.float() - b_sd[k].float()) ** 2).sum())
                n_ortak += 1
            fark = kare ** 0.5
        import timm
        cfg = timm.models.get_pretrained_cfg(ad)
        kayit["timm"][ad] = {"hf_repo": repo, "lisans": lisans, "hf_onbellek": onb, "d_kopya": str(hedef),
                             "depo_bagi": bag_durum, "bayt": hedef.stat().st_size, "sha256": s,
                             "hf_lfs_sha256": hf_sha, "hf_boyut": hf_boyut,
                             "sha256_hf_ile_ayni": (s == hf_sha) if hf_sha else None,
                             "karsilastirma_agirligi": karsi, "bas_disi_ortak_anahtar": n_ortak,
                             "fark_normu": fark, "pretrained_cfg_mean": list(cfg.mean),
                             "pretrained_cfg_std": list(cfg.std)}
        satirlar.append(f"{s}  {hedef}")
        print(ad, s, "HF", hf_sha, "fark", fark, "mean", cfg.mean, "std", cfg.std)

    with io.open(CIKTI / "indirme_sha256.txt", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# curutme indirme adimi " + kayit["uretildi_utc"] + " (scripts/curutme_indirme.py)\n")
        fh.write("\n".join(satirlar) + "\n")
    with io.open(CIKTI / "indirme_denetimi.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(kayit, fh, ensure_ascii=False, indent=1)
    print("yazildi", CIKTI / "indirme_sha256.txt", CIKTI / "indirme_denetimi.json")

    if kayit["hatalar"] and (len(kayit["xcit"]) < 3 or len(kayit["timm"]) < 2):
        sys.exit(4)
    for ad, v in kayit["timm"].items():
        if v["sha256_hf_ile_ayni"] is False or not v["fark_normu"]:
            print("DENETIM KALDI", ad)
            sys.exit(3)
    sys.exit(0)


if __name__ == "__main__":
    main()
