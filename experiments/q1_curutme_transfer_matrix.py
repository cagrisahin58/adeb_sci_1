# -*- coding: utf-8 -*-
"""Curutme zinciri (08.11.2026) icin transfer matrisi sarmalayicisi.

Bu dosya yeni bir saldiri ya da olcum kodu TASIMAZ. Ek bloklar icin yazilmis catal
experiments/q1_ek_transfer_matrix.py'yi (B8 icin c1_c3_transfer_matrix.py'den catallandi; varsayilan
bayraklarla ozgun betikle birebir ayni oldugu scripts/ek_regresyon.sh ile gosterildi) importlib ile
yukler, sha256'sini denetler ve onun main() islevini model listesi on ayarlari ve zaman asimiyla cagirir.
Dondurulmus experiments/c1_c3_transfer_matrix.py'ye dokunulmaz.

Eklenenler:
  --model-seti AD   on ayarli model listesi (asagida); ayrica --model / --rb-model aynen gecirilebilir.
      b4_20         B4'un 20 modeli (scripts/konsey_tam_zincir.sh CMD_B4 ile ayni takma adlar ve yollar)
      a22           b4_20 + Debenedetti2022Light_XCiT-M12 + Debenedetti2022Light_XCiT-L12 (A blogu)
      d28           a22 + alti yeni model (V_scrp_s2401/2402, V_IN21k_s2501/2502, R224_SWSL_s1501/1502;
                    kontrol noktasi models/q1/curutme/<takma>/<tip>/adv/adversarial_training/best.pth)
      b118_son_b3   b4_20, ama B3'un alti kosusu son kontrol noktasiyla (last.pth), ayni takma adlarla
      b118_son_tum  b4_20, ama egitilmis 12 modelin hepsi last.pth ile (C1 dahil), ayni takma adlarla
      b118_ara      birincil panel (7) + B3 kosularinin 10 epokluk ara kontrol noktalari
                    (epochs/epoch_XXX.pth; takma ad <kosu>_eXXX)
      xcit3         uc XCiT (yalniz duman)
  --eksik-atla      d28'de kontrol noktasi olmayan yeni modeli atlar (listesi meta dosyasina yazilir);
                    verilmezse eksik kontrol noktasi hatadir (kod 2).
  --zaman-asimi-s S ic zaman asimi (signal.alarm); dolarsa kod 124 ile cikar. Zincir ayrica `timeout` kullanir.
Diger butun bayraklar (--eps, --alpha, --steps, --n-samples, --seed, --cache-adv, --skip-existing,
--out-dir, --batch-size, --sources ...) catala oldugu gibi gecer. Cikti klasorune curutme_meta.json
(catal ve sarmalayici sha256'si, cozulmus model listesi, argv, UTC) yazilir.
"""
import argparse
import glob
import hashlib
import importlib.util
import io
import json
import os
import signal
import sys
from datetime import datetime, timezone
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
CATAL = KOK / "experiments" / "q1_ek_transfer_matrix.py"
OZGUN = KOK / "experiments" / "c1_c3_transfer_matrix.py"
OZGUN_SHA = "f25d9062c958a296353059639398f0a0a8eb18cd48182b1afa5ec4e3986140b7"
YENI_KOK = "models/q1/curutme"

C1 = [
    ("ResNet18_AT_s1001", "resnet18", "models/c1/resnet18_s1001/resnet18/adv/adversarial_training"),
    ("ResNet18_AT_s1002", "resnet18", "models/c1/resnet18_s1002/resnet18/adv/adversarial_training"),
    ("ResNet18_AT_s1003", "resnet18", "models/c1/resnet18_s1003/resnet18/adv/adversarial_training"),
    ("ViT_Tiny_AT_s2001", "vit_tiny", "models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training"),
    ("ViT_Tiny_AT_s2002", "vit_tiny", "models/c1/vit_tiny_s2002/vit_tiny/adv/adversarial_training"),
    ("ViT_Tiny_AT_s2003", "vit_tiny", "models/c1/vit_tiny_s2003/vit_tiny/adv/adversarial_training"),
]
B3 = [
    ("V_IN_s2101", "vit_tiny_in1k", "models/q1/konsey/V_IN_s2101/vit_tiny_in1k/adv/adversarial_training"),
    ("V_IN_s2102", "vit_tiny_in1k", "models/q1/konsey/V_IN_s2102/vit_tiny_in1k/adv/adversarial_training"),
    ("R224_IN_s1301", "resnet18_224_in1k", "models/q1/konsey/R224_IN_s1301/resnet18_224_in1k/adv/adversarial_training"),
    ("R224_IN_s1302", "resnet18_224_in1k", "models/q1/konsey/R224_IN_s1302/resnet18_224_in1k/adv/adversarial_training"),
    ("R224_scr_s1201", "resnet18_224", "models/q1/konsey/R224_scr_s1201/resnet18_224/adv/adversarial_training"),
    ("R224_scr_s1202", "resnet18_224", "models/q1/konsey/R224_scr_s1202/resnet18_224/adv/adversarial_training"),
]
PANEL7 = ["Wong2020Fast", "Engstrom2019Robustness", "Carmon2019Unlabeled", "Gowal2020Uncovering_28_10_extra",
          "Sehwag2021Proxy_R18", "Addepalli2022Efficient_RN18", "Rade2021Helper_R18_ddpm"]
XCIT_S12 = "Debenedetti2022Light_XCiT-S12"
XCIT_ML = ["Debenedetti2022Light_XCiT-M12", "Debenedetti2022Light_XCiT-L12"]
YENI6 = [
    ("V_scrp_s2401", "vit_tiny"), ("V_scrp_s2402", "vit_tiny"),
    ("V_IN21k_s2501", "vit_tiny_in21k"), ("V_IN21k_s2502", "vit_tiny_in21k"),
    ("R224_SWSL_s1501", "resnet18_224_swsl"), ("R224_SWSL_s1502", "resnet18_224_swsl"),
]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def yeni_yol(takma, tip):
    return f"{YENI_KOK}/{takma}/{tip}/adv/adversarial_training/best.pth"


def model_seti(ad, eksik_atla):
    """(model_argv, rb_argv, atlanan) dondurur."""
    mod, rb, atlanan = [], [], []

    def b4(son_b3=False, son_c1=False):
        for t, tip, d in C1:
            mod.append(f"{t}:{tip}:{d}/{'last' if son_c1 else 'best'}.pth")
        for t, tip, d in B3:
            mod.append(f"{t}:{tip}:{d}/{'last' if son_b3 else 'best'}.pth")
        rb.extend(PANEL7 + [XCIT_S12])

    if ad == "b4_20":
        b4()
    elif ad == "a22":
        b4()
        rb.extend(XCIT_ML)
    elif ad == "d28":
        b4()
        rb.extend(XCIT_ML)
        for t, tip in YENI6:
            p = yeni_yol(t, tip)
            if Path(p).exists():
                mod.append(f"{t}:{tip}:{p}")
            elif eksik_atla:
                atlanan.append(p)
            else:
                raise SystemExit(2)
    elif ad == "b118_son_b3":
        b4(son_b3=True)
    elif ad == "b118_son_tum":
        b4(son_b3=True, son_c1=True)
    elif ad == "b118_ara":
        rb.extend(PANEL7)
        for t, tip, d in B3:
            for p in sorted(glob.glob(f"{d}/epochs/epoch_*.pth")):
                ep = Path(p).stem.split("_")[1]
                mod.append(f"{t}_e{ep}:{tip}:{p}")
    elif ad == "xcit3":
        rb.extend([XCIT_S12] + XCIT_ML)
    else:
        raise SystemExit(f"bilinmeyen model seti: {ad}")
    return mod, rb, atlanan


def main():
    # allow_abbrev=False: catala gecen --model, --model-seti'nin kisaltmasi sanilmasin
    ap = argparse.ArgumentParser(add_help=True, allow_abbrev=False)
    ap.add_argument("--model-seti", default=None)
    ap.add_argument("--eksik-atla", action="store_true")
    ap.add_argument("--zaman-asimi-s", type=int, default=0)
    ap.add_argument("--yalniz-arguman", action="store_true",
                    help="yalniz cozulmus --model/--rb-model argumanlarini tek satir basar (zincir, B10 ve AA icin)")
    ap.add_argument("--yalniz-yeni", action="store_true",
                    help="--yalniz-arguman ile: yalniz alti yeni modelin --model argumanlari (AA icin)")
    a, rest = ap.parse_known_args()
    os.chdir(KOK)

    ozgun_sha = sha256(OZGUN)
    if ozgun_sha != OZGUN_SHA:
        print(f"UYARI: dondurulmus {OZGUN} sha256 {ozgun_sha} != {OZGUN_SHA}")
    mod, rb, atlanan = ([], [], [])
    if a.model_seti:
        try:
            mod, rb, atlanan = model_seti(a.model_seti, a.eksik_atla)
        except SystemExit as e:
            if e.code == 2:
                print("HATA: d28 icin yeni kontrol noktalarindan biri yok; --eksik-atla verilmedi")
            raise
    argv = []
    for m in mod:
        argv += ["--model", m]
    for r in rb:
        argv += ["--rb-model", r]
    if a.yalniz_arguman:
        if a.yalniz_yeni:
            yeni = {t for t, _ in YENI6}
            argv = [x for m in mod if m.split(":", 1)[0] in yeni for x in ("--model", m)]
        print(" ".join(argv))
        return
    argv += rest

    out_dir = None
    for i, x in enumerate(rest):
        if x == "--out-dir" and i + 1 < len(rest):
            out_dir = Path(rest[i + 1])
    meta = {"sarmalayici": "experiments/q1_curutme_transfer_matrix.py", "sarmalayici_sha256": sha256(__file__),
            "catal": str(CATAL.relative_to(KOK)), "catal_sha256": sha256(CATAL),
            "ozgun_dondurulmus_sha256": ozgun_sha, "ozgun_degismedi": ozgun_sha == OZGUN_SHA,
            "model_seti": a.model_seti, "model_argv": mod, "rb_model": rb, "atlanan_eksik": atlanan,
            "zaman_asimi_s": a.zaman_asimi_s, "catal_argv": argv,
            "torch_home": os.environ.get("TORCH_HOME"), "baslangic_utc": datetime.now(timezone.utc).isoformat()}
    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        with io.open(out_dir / "curutme_meta.json", "w", encoding="utf-8", newline="\n") as fh:
            json.dump(meta, fh, ensure_ascii=False, indent=1)
    print(f"model seti {a.model_seti}: {len(mod)} yerel + {len(rb)} RobustBench; atlanan {atlanan}")

    if a.zaman_asimi_s > 0:
        def _bitti(_s, _f):
            print(f"ZAMAN ASIMI: {a.zaman_asimi_s} s doldu", flush=True)
            sys.exit(124)
        signal.signal(signal.SIGALRM, _bitti)
        signal.alarm(a.zaman_asimi_s)

    spec = importlib.util.spec_from_file_location("q1_ek_transfer_matrix", CATAL)
    tm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tm)
    sys.argv = [str(CATAL)] + argv
    tm.main()
    if out_dir is not None:
        meta["bitis_utc"] = datetime.now(timezone.utc).isoformat()
        with io.open(out_dir / "curutme_meta.json", "w", encoding="utf-8", newline="\n") as fh:
            json.dump(meta, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
