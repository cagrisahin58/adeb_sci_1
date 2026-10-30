# -*- coding: utf-8 -*-
"""ImageNetV2 yolunun sahte veriyle uctan uca smoke sinamasi (CPU; 30.10.2026).

Konteyner /mnt/d'yi gormediginden gercek ImageNetV2 ve RobustBench ImageNet modelleri yerine:
  - /tmp altinda 1000 sinif klasorlu sahte ImageNetV2 (sinif basina 1 rastgele JPEG),
  - iki rastgele baslatilmis 1000 sinifli resnet18_224 kontrol noktasi (src/models/r224.py).
Sinananlar: --dataset imagenetv2 yukleyicisi, --eps/--alpha, --batch-size, --cache-root, --cache-f16,
onbellek adi ve yeniden kullanimi (taze kosu ile onbellekli kosu hucre hucre ayni olmali),
--onisleme-denetimi (yerel modelde yalniz ortak hat) ve B10 gradyan alt komutu.
Sonuclar anlamsizdir (rastgele agirlik); yalniz kod yolu sinanir.

  docker exec -w /workspace -e CUDA_VISIBLE_DEVICES= adeb_eval python scripts/ek_sahte_v2_smoke.py
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import torch

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))
OUT = KOK / "results" / "q1" / "ek_regresyon" / "v2_sahte"


def kos(args, log):
    cmd = [sys.executable, "-B", *args]
    r = subprocess.run(cmd, cwd=KOK, capture_output=True, text=True)
    log.write_text(r.stdout + "\n--- stderr ---\n" + r.stderr[-4000:])
    print(f"rc={r.returncode} {' '.join(args[:2])} -> {log.name}")
    if r.returncode != 0:
        print(r.stderr[-3000:])
        raise SystemExit(f"basarisiz: {log}")
    return r


def main():
    from PIL import Image
    from src.models import ModelRegistry

    tmp = Path(tempfile.mkdtemp(prefix="ek_v2_"))
    v2 = tmp / "imagenetv2" / "imagenetv2-matched-frequency-format-val"
    rng = np.random.default_rng(0)
    for c in range(1000):
        (v2 / str(c)).mkdir(parents=True)
        Image.fromarray((rng.random((40, 48, 3)) * 255).astype(np.uint8)).save(v2 / str(c) / f"{c:05d}.jpeg")
    torch.manual_seed(0)
    ck = {}
    for ad in ("SahteA", "SahteB"):
        m = ModelRegistry.get("resnet18_224", num_classes=1000)
        ck[ad] = tmp / f"{ad}.pth"
        torch.save({"model_state_dict": m.state_dict()}, ck[ad])
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    ortak = ["experiments/q1_ek_transfer_matrix.py", "--dataset", "imagenetv2", "--v2-kok", str(tmp / "imagenetv2"), "--v2-sinif-dosya", "0",
             "--n-samples", "8", "--batch-size", "4", "--eps", "4", "--alpha", "1",
             "--model", f"SahteA:resnet18_224:{ck['SahteA']}", "--model", f"SahteB:resnet18_224:{ck['SahteB']}"]
    onb = ["--cache-root", str(tmp), "--cache-adv", "onbellek"]
    kos(ortak + onb + ["--cache-f16", "--onisleme-denetimi", "--out-dir", str(OUT / "taze")], OUT / "taze.log")
    kos(ortak + onb + ["--cache-f16", "--out-dir", str(OUT / "onbellekli")], OUT / "onbellekli.log")
    kos(ortak + ["--out-dir", str(OUT / "f32_onbelleksiz")], OUT / "f32_onbelleksiz.log")
    kos(["scripts/konsey_smoke_karsilastir.py", str(OUT / "taze"), str(OUT / "onbellekli"),
         "--json", str(OUT / "karsilastirma_taze_onbellekli.json")], OUT / "karsilastirma.log")
    dosyalar = sorted(p.name for p in (tmp / "onbellek").iterdir())
    tm = json.loads((OUT / "taze" / "transfer_matrix.json").read_text())
    kos(["experiments/q1_ek_gradyan_kosinus.py", "gradyan", "--dataset", "imagenetv2", "--v2-kok", str(tmp / "imagenetv2"), "--v2-sinif-dosya", "0",
         "--n-samples", "8", "--batch-size", "4", "--model", f"SahteA:resnet18_224:{ck['SahteA']}",
         "--model", f"SahteB:resnet18_224:{ck['SahteB']}", "--cikti", str(OUT / "gradyan")], OUT / "gradyan.log")
    oz = json.loads((OUT / "gradyan" / "kosinus_ozet.json").read_text())
    arr = np.load(OUT / "onbellekli" / "per_sample_SahteA_to_SahteA.npz")
    ozet = {"onbellek_dosyalari": dosyalar,
            "onbellek_dtype": str(np.load(tmp / "onbellek" / [d for d in dosyalar if d.endswith(".npy")][0]).dtype),
            "eps_255": tm.get("eps_255"), "alpha_255": tm.get("alpha_255"), "manifest_n": tm.get("manifest_n"),
            "normalizasyon": tm.get("normalizasyon"), "on_isleme": tm.get("on_isleme"),
            "denetim_var": (OUT / "taze" / "onisleme_denetimi.json").exists(),
            "kosinus_c_tum": oz["c_tum"], "n_per_sample": int(arr["target_clean_correct"].shape[0]),
            "karsilastirma": json.loads((OUT / "karsilastirma_taze_onbellekli.json").read_text())["BIREBIR"]}
    (OUT / "ozet.json").write_text(json.dumps(ozet, indent=1))
    print(json.dumps(ozet, indent=1))
    shutil.rmtree(tmp)
    if not ozet["karsilastirma"]:
        raise SystemExit("taze ve onbellekli kosu ayni degil")


if __name__ == "__main__":
    main()
