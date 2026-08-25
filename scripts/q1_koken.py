#!/usr/bin/env python3
"""IS-6(h): Q1 bas artefaktlarinin KOKEN bilgisi.

Sorun: E1'in tasiyici artefaktlarinda koken bilgisi YOKTU -- ne uretim
tarihi, ne git SHA, ne tohum listesi, ne kutuphane surumu. Kiyas:
`results/q1/e2/e2_report.json` icinde `generated_utc` var. Koken bilgisi
olmayan bir sayi, alti ay sonra "hangi kodla uretildi" sorusuna cevap
veremez ve K1'in ruhuna aykiridir.

Cozum: artefaktlar DEGISTIRILMEZ (bayt degisimi eski karsilastirmalari
bozar); yaninda bir KOKEN kutugu uretilir. Her bas artefakt icin sha256,
boyut, degistirilme zamani; ayrica depo SHA'si, dal, kirlilik durumu ve
calisma zamani surumleri.

Kullanim: docker exec -w /workspace adeb_eval python scripts/q1_koken.py
Cikti   : results/q1/KOKEN.json
"""
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"

# Disariya cikan sayilari TASIYAN artefaktlar
BAS_ARTEFAKTLAR = [
    "results/q1/e1_cifar100_summary.json",
    "results/q1/cifar100/transfer/e1_transfer_summary.json",
    "results/q1/c3_precision.json",
    "results/q1/variance_ratio.json",
    "results/q1/e3_coverage.json",
    "results/q1/e3_xekseni_test.json",
    "results/q1/e3_bosluk_kontrol.json",
    "results/q1/ozdeslik_kontrol.json",
    "results/q1/e3_spread_teshis.json",
    "results/q1/e3_asimetri_fit.json",
    # B2 (2026-08-25): makalede RAPORLANAN duyarliliklarin kaynaklari
    "results/q1/e3_asimetri_fit_svhnli.json",
    "results/rev2_blockA/a2_transfer_protocols.json",
    "results/q1/e3_surucu_ayristirma.json",
    "results/q1/e3_iki_kol_fit.json",
    "results/q1/e7_svhn_summary.json",
    "results/q1/svhn/transfer/e7_transfer_summary.json",
    "results/q1/b8_secim_bandi.json",
    "results/q1/cifar10_l2/e6_aa_l2_summary.json",
    "results/q1/cifar10_l2/e6_onkestirim.json",
    "results/q1/cifar10_l2/transfer/e6_l2_transfer_summary.json",
    "results/q1/e2/e2_report.json",
    "results/q1/e2/e2_grid.json",
    "results/c1_seeds/c1_seed_summary.json",
    "results/c1_transfer/c1_transfer_summary.json",
    "results/c1_c3/c3_summary.json",
    # --- makaleye dogrudan sayi tasiyan, daha once deftere girmemis olanlar ---
    "results/c1_eval_summary.json",              # Tablo I
    "results/c1_behavior_summary.json",          # MI-FGSM
    "results/c1_c45_summary.json",               # uzamsal + suruklenme + flip
    "results/c1_statval/statistical_validation.json",   # saldiri-tohumu varyansi
    "results/stat_addendum/stat_addendum.json",  # native ViT kontrol noktasi
    "results/rev2_blockA/a3_gradient_paired.json",      # Tablo VIII native sutunu
    "results/rev2_blockA/a3_per_sample.npz",            # ayni sutunun ham degerleri
    "results/c1_c2/pair1/tgr_summary.json",
    "results/c1_c2/pair2/tgr_summary.json",
    "results/c1_c2/pair3/tgr_summary.json",
    "results/c1_a5/pair1/a5_tsne_quant.json",
    "results/c1_a5/pair2/a5_tsne_quant.json",
    "results/c1_a5/pair3/a5_tsne_quant.json",
    "results/c1_c4/pair1/c4_summary.json",
    "results/c1_c4/pair2/c4_summary.json",
    "results/c1_c4/pair3/c4_summary.json",
    "results/c1_c5/pair1/c5_spatial.json",
    "results/c1_c5/pair2/c5_spatial.json",
    "results/c1_c5/pair3/c5_spatial.json",
]

TOHUMLAR = {
    "cifar10 (C1/E2)": {"resnet18": [1001, 1002, 1003], "vit_tiny": [2001, 2002, 2003]},
    "cifar100 (E1)": {"resnet18": [1001, 1002, 1003], "vit_tiny": [2001, 2002, 2003]},
    "svhn (E7-kisa)": {"resnet18": [1001, 1002], "vit_tiny": [2001, 2002]},
    "degerlendirme": {"attack_seed": 42, "attack_seed_ablasyon": [42, 123, 456]},
}


def sh(*cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=str(ROOT))
        return r.stdout.strip() or None
    except Exception:
        return None


def sha256(p, blok=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while True:
            b = fh.read(blok)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def surumler():
    out = {}
    try:
        import torch
        out["torch"] = torch.__version__
        out["cuda"] = getattr(torch.version, "cuda", None)
        out["cudnn"] = torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else None
        if torch.cuda.is_available():
            out["gpu"] = torch.cuda.get_device_name(0)
    except Exception as e:
        out["torch_hata"] = str(e)
    for mod in ("numpy", "timm", "scipy", "torchvision"):
        try:
            out[mod] = __import__(mod).__version__
        except Exception:
            out[mod] = None
    try:
        import robustbench  # noqa: F401
        out["robustbench"] = "mevcut"
    except Exception:
        out["robustbench"] = None
    return out


def _depo():
    """Git bilgisi. DIKKAT: git YOKSA "temiz" DEMEK YANLIS OLUR.

    Ilk surum bool(sh(...)) kullaniyordu; git konteynerde bulunmadiginda
    sh() None donuyor ve bool(None)=False, yani "calisma agaci temiz" gibi
    gorunuyordu. Bu SESSIZ YANLIS DEGERDIR. Artik okunamayan alan null
    kalir ve git_okunabildi bayragi durumu acikca soyler.
    """
    # ONCE ortam degiskenleri: git ANA MAKINEDE var, torch KONTEYNERDE.
    # scripts/q1_koken.sh git bilgisini ana makineden okuyup buraya gecirir,
    # boylece tek artefakt hem git hem calisma zamani bilgisini tasir.
    import os as _os
    if _os.environ.get("KOKEN_GIT_SHA"):
        _kirli = _os.environ.get("KOKEN_GIT_KIRLI")
        return {"git_okunabildi": True,
                "kaynak": "ana makine (q1_koken.sh)",
                "git_sha": _os.environ["KOKEN_GIT_SHA"],
                "git_kisa": _os.environ.get("KOKEN_GIT_KISA"),
                "dal": _os.environ.get("KOKEN_GIT_DAL"),
                "son_commit_tarihi": _os.environ.get("KOKEN_GIT_TARIH"),
                "calisma_agaci_kirli_mi": (None if _kirli is None else _kirli == "1")}
    sha = sh("git", "rev-parse", "HEAD")
    if sha is None:
        return {"git_okunabildi": False,
                "git_sha": None, "git_kisa": None, "dal": None,
                "son_commit_tarihi": None, "calisma_agaci_kirli_mi": None,
                "not": "git bu ortamda calistirilamadi (ornegin konteynerde "
                       "git yok); alanlar BILINMIYOR, temiz DEGIL."}
    durum = sh("git", "status", "--porcelain")
    return {"git_okunabildi": True,
            "git_sha": sha,
            "git_kisa": sh("git", "rev-parse", "--short", "HEAD"),
            "dal": sh("git", "rev-parse", "--abbrev-ref", "HEAD"),
            "son_commit_tarihi": sh("git", "log", "-1", "--format=%cI"),
            "calisma_agaci_kirli_mi": bool(durum)}


dosyalar, eksik = {}, []
for rel in BAS_ARTEFAKTLAR:
    p = ROOT / rel
    if not p.exists():
        eksik.append(rel)
        continue
    st = p.stat()
    dosyalar[rel] = {
        "sha256": sha256(p),
        "bayt": st.st_size,
        "degistirilme_utc": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat(),
    }

koken = {
    "uretildi_utc": datetime.now(timezone.utc).isoformat(),
    "aciklama": "Q1 bas artefaktlarinin koken kutugu. Artefaktlarin KENDISI "
                "degistirilmez; bu dosya onlarin yanindaki kanittir (IS-6h).",
    "depo": _depo(),
    "tohumlar": TOHUMLAR,
    "calisma_zamani": surumler(),
    "artefaktlar": dosyalar,
    "eksik_artefaktlar": eksik,
    "not": "eksik_artefaktlar bos degilse o deneyler henuz kosulmamistir "
           "(ornegin E7/SVHN veya E6/L2 ciktilari).",
}

out = ROOT / "results/q1/KOKEN.json"
out.write_text(json.dumps(koken, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"KOKEN kutugu: {len(dosyalar)} artefakt kaydedildi, {len(eksik)} eksik")
if koken["depo"]["git_okunabildi"]:
    print(f"  git {koken['depo']['git_kisa']} ({koken['depo']['dal']})"
          f"  kirli={koken['depo']['calisma_agaci_kirli_mi']}")
else:
    print("  git BILGISI OKUNAMADI -- bu betigi ANA MAKINEDE (WSL) kosun:")
    print("    python3 scripts/q1_koken.py")
print(f"  torch {koken['calisma_zamani'].get('torch')}  cuda {koken['calisma_zamani'].get('cuda')}")
if eksik:
    print("  eksik:", ", ".join(eksik))
print(f"-> {out}")
