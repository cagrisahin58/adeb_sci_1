"""EK BLOKLAR (B8, B9, B10) ICIN CATAL: experiments/c1_c3_transfer_matrix.py'nin kopyasi (30.10.2026).

Ozgun betik (sha256 f25d9062c958a296353059639398f0a0a8eb18cd48182b1afa5ec4e3986140b7) B4/B5 icin
dondurulmustur ve DEGISTIRILMEZ (fable karari E5). Bu catal ozgun betigin butun bayraklarini aynen
tasir; varsayilan bayraklarla ozgun betikle hucre hucre ve ornek ornek ayni ciktiyi vermesi
scripts/ek_regresyon.sh ile denetlenir. Ek bayraklar (hicbiri verilmezse eski davranis):
  --eps E, --alpha A    Linf yaricap ve adim, 255 cinsinden (or. --eps 4 --alpha 1). Verilmezse
        EPS = 8/255, ALPHA = 2/255. Yalniz --eps verilirse alpha = eps/4 (CIFAR orani).
  --batch-size B        degerlendirme ve saldiri grubu (varsayilan 50 = ozgun sabit).
  --cache-root KOK      --cache-adv goreli ise KOK/<cache-adv> kullanilir (or. D diski).
  --cache-f16           onbellek perturbasyonu (adv - x) float16 saklar (yaricap disina tasmamasi
        icin adv = clamp(x + clamp(delta, -eps, eps), 0, 1) ile geri kurulur). Ilk kosu da hedefleri
        bu geri kurulmus ornekle degerlendirir; boylece onbellekli ve taze kosu ayni sonucu verir.
  Onbellek dosya adi: --eps/--alpha verilince '_e{eps}_a{alpha}', --cache-f16 ile '_f16' eki alir;
        eski onbellek adlari ve meta sozlugu varsayilanlarda degismez.
  --dataset imagenetv2  ImageNetV2 MatchedFrequency (Recht ve ark. 2019, arXiv 1902.10811), klasor
        adlari 0-999 sinif indeksidir. Secim: her sinif klasorunde dosya adlarinin sirali ilk k'si,
        k = ceil(n/1000); sira (sinif, dosya adi). n = 2000'de sinif basina 2 goruntu, bolunmus yari
        kestiriminde her yariya sinif basina bir goruntu duser. On isleme ortak hattir (varsayilan
        robustbench.data.PREPROCESSINGS['BicubicRes256Crop224'], ek on kayit §5.2; --in-onisleme
        Res256Crop224 ile bilinear);
        goruntuler bir kez tensore cevrilir. Normalizasyon EKLENMEZ: RobustBench ImageNet modelleri
        kendi degerlendirmesinde [0, 1] girdi alir (robustbench.utils.load_model; normalize_model
        sarmalayicisi modelin icindedir ya da modelde hic yoktur). Model ici normalizasyon envanteri
        transfer_matrix.json'a yazilir. Secilen dosyalarin listesi ve sha256'lari cikti klasorunde
        imagenetv2_manifest.json'a, ozeti transfer_matrix.json'a yazilir.
  --v2-kok DIZIN        ImageNetV2 koku (varsayilan data/imagenetv2; tek alt klasor varsa ona iner).
  --v2-sinif-dosya K    her sinif klasorunde tam K dosya olmali (varsayilan 10; 0 kapatir, sahte veri icin).
  --in-onisleme AD      BicubicRes256Crop224 (varsayilan, ek on kayit §5.2) ya da Res256Crop224 (bilinear).
        Yalniz --dataset imagenetv2'de kullanilir; CIFAR yolunu ve onbellek adini etkilemez.
  --onisleme-denetimi   (yalniz imagenetv2) her RobustBench modelinin temiz dogrulugunu ortak hatta ve
        modelin kendi RobustBench on islemesinde ayni dosyalarda olcer, onisleme_denetimi.json yazar.
        --yalniz-denetim ile matris kosulmaz.
  --rb-model AD[:TAKMA_AD]  dataset imagenetv2 iken RobustBench 'imagenet' Linf modelleri yuklenir;
        varsayilan referans (WRN_28_10) imagenetv2'de hic eklenmez.

--- Ozgun betigin belgesi ---
C3: WRN-28-10 dahil 3x3 transfer matrisi (C1 kontrol noktalari).

Amac: transfer asimetrisinin, hedefin temiz hata orani tarafindan ne kadar
aciklandigini olcmek. Uc model (ResNet-18 AT, ViT-Tiny AT, WRN-28-10) icin
ham ve kosullu (target-correct) yaniltma oranlari, ornek bazinda kayitla.

Cikti: results/c1_c3/pair{N}/ (per-sample npz + matrix json)
Kullanim: python experiments/c1_c3_transfer_matrix.py --pairs 1 2 3 [--n-samples 10000]

Konsey B1 genisletmesi (29.10.2026). VARSAYILANLAR ESKI DAVRANISI BIREBIR
KORUR (regresyon: results/q1/konsey_smoke/regresyon/). Yeni bayraklar:
  --attack {pgd,mi,tgr}  pgd = eski PGD (varsayilan). mi = MI-PGD/MI-FGSM,
        foy M8.4 ayarlari (mu=1.0, alpha=eps/steps -> 10 adimda eps/10,
        rastgele baslangic yok, L1-toplam normalizasyonu;
        experiments/run_c_addenda.py::mifgsm ile ayni). tgr = TGR,
        experiments/c1_c2_tgr.py::mifgsm(use_tgr=True) dogrudan cagrilir
        (C2 ayarlari: alpha=2/255, mu=1.0); YALNIZ ViT kaynaklarinda
        (vit_tiny, vit_tiny_in1k, vit_small), digerleri kaynak olarak atlanir.
  --steps N             saldiri adim sayisi (varsayilan 10).
  --sources AD ...      yalniz bu takma adlar kaynak olur; hepsi hedef kalir
                        (varsayilan: hepsi kaynak, kare matris).
  --cache-adv DIR       kaynak basina cekismeli ornekleri DIR'e kaydeder
        (float32 .npy + meta .json), varsa yeniden kullanir. Onbellek
        acikken her kaynaktan ONCE set_seed(seed) cagrilir; boylece bir
        kaynagin ornekleri kaynak sirasindan ve listedeki diger modellerden
        bagimsizdir (B2 onbellegi B4'te gecerli kalir). Bu yuzden onbellekli
        kosu, onbelleksiz eski kosuyla PGD rastgele baslangici bakimindan
        bit duzeyinde ayni degildir; kendi icinde tekrarlanabilirdir.
  --skip-existing       hucre bazinda: cikti klasorunde per_sample_{src}_to_{tgt}.npz
        varsa o hucre yeniden hesaplanmaz (dosyadaki hedef-temiz maskesi
        yeni hesaplananla birebir ayni olmak zorunda); butun hucreleri
        hazir kaynak hic saldirilmaz. transfer_matrix.json sonda butun
        hucrelerden yeniden yazilir. Bayrak yoksa eski davranis: json varsa
        kosu tumden atlanir.
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.attacks import PGDAttack, PGDL2Attack  # noqa: E402
from src.data import DATASETS, get_loaders  # noqa: E402
from src.models import ModelRegistry  # noqa: E402
from src.utils.load_model_auto import load_model_auto  # noqa: E402

EPS = 8 / 255
ALPHA = 2 / 255
STEPS = 10
# E6 (L2 tehdit modeli) on-kayitli degerleri -- E6_ON_KAYIT.md §1
EPS_L2 = 0.5
STEPS_L2 = 10
ALPHA_L2 = 2.5 * EPS_L2 / STEPS_L2  # = 0.125
PAIRS = {1: (1001, 2001), 2: (1002, 2002), 3: (1003, 2003)}
# MI-PGD (foy M8.4): mu=1.0, alpha = eps/steps
MI_MU = 1.0
# TGR yalniz timm ViT bloklu sarmalayicilarda (self.model.blocks)
VIT_TYPES = {"vit_tiny", "vit_tiny_in1k", "vit_small"}
# timm yoluyla yuklenen RobustBench modellerinin torch hub onbellek dosyasi;
# konteyner onbellegi silinirse models/robustbench_zoo'daki kopyadan geri konur
RB_TIMM_CACHE = {
    "Debenedetti2022Light_XCiT-S12": "debenedetti2022light-xcit-s-cifar10-linf.pth.tar",
}
# EK: (model, robustbench veri kumesi) anahtarli; ozgun sozluk yalniz cifar10 dosya adini tasir
RB_TIMM_CACHE_DS = {
    ("Debenedetti2022Light_XCiT-S12", "cifar10"): "debenedetti2022light-xcit-s-cifar10-linf.pth.tar",
    ("Debenedetti2022Light_XCiT-S12", "cifar100"): "debenedetti2022light-xcit-s-cifar100-linf.pth.tar",
    ("Debenedetti2022Light_XCiT-S12", "imagenet"): "debenedetti2022light-xcit-s-imagenet-linf.pth.tar",
}
EK_DATASETS = ("imagenetv2",)
RB_DS = {"imagenetv2": "imagenet"}  # bizim veri kumesi adi -> RobustBench veri kumesi adi


def set_seed(seed):
    import random

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def load_local(model_type, path, device):
    # num_classes checkpoint'ten otomatik (CIFAR-100 destegi)
    return load_model_auto(model_type, path, device)


def _restore_rb_timm_cache(rb_name, dataset):
    """timm yolundan yuklenen RobustBench modeli (XCiT) icin hub onbellegi
    eksikse depodaki kopyayi (models/robustbench_zoo/<ds>/Linf/<ad>.pth.tar)
    hub onbellegine geri koyar. Dosya varsa hicbir sey yapmaz."""
    fname = RB_TIMM_CACHE_DS.get((rb_name, dataset))
    if fname is None:
        return
    hub = Path(torch.hub.get_dir()) / "checkpoints" / fname
    local = Path("models/robustbench_zoo") / dataset / "Linf" / f"{rb_name}.pth.tar"
    if not hub.exists() and local.exists():
        import shutil

        hub.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(local, hub)
        print(f"  {rb_name}: hub onbellegi depodaki kopyadan geri kondu ({local})")


def load_wrn(device, dataset="cifar10", rb_name=None):
    """RobustBench referans modeli. CIFAR-100 icin Pang2022Robustness_WRN28_10
    (dogrulama hukmu: 1M sentetik veri, Gowal2020_extra ile yapisal tutarli)."""
    from robustbench.utils import load_model

    defaults = {"cifar10": "Gowal2020Uncovering_28_10_extra",
                "cifar100": "Pang2022Robustness_WRN28_10"}
    name = rb_name or defaults.get(dataset)
    if name is None:
        raise ValueError(f"{dataset} icin RobustBench referansi yok (SVHN: kendi "
                         f"DenseNet-121 referansimiz kullanilir, bkz. Q1 raporu 4.2)")
    dataset = RB_DS.get(dataset, dataset)  # EK: imagenetv2 -> imagenet
    _restore_rb_timm_cache(name, dataset)
    model = load_model(model_name=name, dataset=dataset, threat_model="Linf",
                       model_dir="models/robustbench_zoo")
    return model.to(device).eval()


# ----------------------------------------------------------------------------------------------
# EK: ImageNetV2 MatchedFrequency yukleyici ve normalizasyon envanteri
# ----------------------------------------------------------------------------------------------
def _v2_goruntu_koku(kok):
    kok = Path(kok)
    if not kok.exists():
        raise SystemExit(f"ImageNetV2 koku yok: {kok} (scripts/ek_indir.py ile indirin; konteynerde "
                         f"/mnt/d baglamasi gerekir, 07_disk_D_plani.md §4)")
    alt = [p for p in kok.iterdir() if p.is_dir()]
    if len(alt) == 1 and not alt[0].name.isdigit():
        kok = alt[0]
    return kok


def v2_secim(kok, n_samples, sinif_dosya=None):
    """(goreli yol, etiket) listesi: her sinif klasorunun sirali ilk k dosyasi, sira (sinif, ad)."""
    import math

    kok = _v2_goruntu_koku(kok)
    siniflar = sorted([p for p in kok.iterdir() if p.is_dir() and p.name.isdigit()], key=lambda p: int(p.name))
    adlar = [int(p.name) for p in siniflar]
    if adlar != list(range(1000)):
        raise SystemExit(f"{kok}: sinif klasorleri 0-999 degil ({len(adlar)} klasor)")
    k = math.ceil(n_samples / 1000)
    secim = []
    for p in siniflar:
        dosyalar = sorted(f.name for f in p.iterdir() if f.is_file())
        if sinif_dosya and len(dosyalar) != sinif_dosya:  # ek on kayit §5.1: her klasorde 10 dosya
            raise SystemExit(f"{p}: {len(dosyalar)} dosya, {sinif_dosya} bekleniyor (ek on kayit §5.1); durduruldu")
        if len(dosyalar) < k:
            raise SystemExit(f"{p}: {len(dosyalar)} dosya, sinif basina {k} isteniyor")
        secim += [(f"{p.name}/{f}", int(p.name)) for f in dosyalar[:k]]
    return kok, secim[:n_samples] if len(secim) > n_samples else secim


def v2_onisleme(ad):
    from robustbench.data import PREPROCESSINGS

    return PREPROCESSINGS[ad]


def v2_tensor(kok, secim, onisleme):
    from PIL import Image

    xs = []
    for rel, _ in secim:
        with Image.open(kok / rel) as im:
            xs.append(onisleme(im.convert("RGB")))
    return torch.stack(xs), torch.tensor([y for _, y in secim], dtype=torch.long)


def v2_loaders(kok, n_samples, batch_size, onisleme_adi, sinif_dosya=None):
    """get_loaders ile ayni arayuz: (None, test_loader) ve manifest sozlugu."""
    from torch.utils.data import DataLoader, TensorDataset

    kok, secim = v2_secim(kok, n_samples, sinif_dosya)
    x, y = v2_tensor(kok, secim, v2_onisleme(onisleme_adi))
    h = hashlib.sha256()
    dosyalar = []
    for rel, lab in secim:
        s = _sha256(kok / rel)
        dosyalar.append({"yol": rel, "etiket": lab, "sha256": s})
        h.update(f"{rel}\t{lab}\t{s}\n".encode())
    manifest = {"kok": str(kok), "secim_kurali": "sinif klasoru basina sirali ilk ceil(n/1000) dosya; sira (sinif, ad)",
                "onisleme": onisleme_adi, "n": len(secim), "tensor_sekli": list(x.shape),
                "liste_sha256": h.hexdigest(), "dosyalar": dosyalar}
    loader = DataLoader(TensorDataset(x, y), batch_size=batch_size, shuffle=False, num_workers=0)
    return (None, loader), manifest


def normalizasyon_envanteri(model):
    """Model icinde girdi normalizasyonu yapan katmanlar (betimsel; karar icin degil)."""
    adlar = sorted({type(m).__name__ for m in model.modules() if "normaliz" in type(m).__name__.lower()})
    ic = []
    for m in model.modules():
        for at in ("mu", "sigma", "mean", "std"):
            v = getattr(m, at, None)
            if isinstance(v, torch.Tensor) and v.numel() == 3:
                ic.append(f"{type(m).__name__}.{at}")
    return {"normalizasyon_katmanlari": adlar, "uc_kanalli_mean_std_tamponlari": sorted(set(ic)),
            "model_ici_normalizasyon_var": bool(adlar or ic)}


# Ek on kayit §5.5 esikleri (ON_KAYIT_EK_B8_B10_2026-10-30.md):
# (i) kendi hatta temiz dogruluk >= %25 VE >= 0,6 x RobustBench temiz dogrulugu;
# (ii) |ortak - kendi| <= 5 puan; 3 < |fark| <= 5 matriste kalir ama isaretlenir (S8-4 duyarliligi).
DEN_ALT_SINIR = 25.0
DEN_RB_KAT = 0.6
DEN_FARK_EN_COK = 5.0
DEN_FARK_ISARET = 3.0
# RobustBench ImageNet Linf temiz dogruluklari (model_info/imagenet/Linf/<ad>.json, clean_acc,
# 30.10.2026'da okundu; kopyalar raporlar/konsey_2026-10-29/_ek_denetim/dis/rb/in_<ad>.json; ek §5.3 tablosu).
RB_IN_TEMIZ = {
    "Salman2020Do_R18": 52.92, "Salman2020Do_R50": 64.02, "Salman2020Do_50_2": 68.46,
    "Engstrom2019Robustness": 62.56, "Chen2024Data_WRN_50_2": 68.76, "Peng2023Robust": 73.44,
    "Singh2023Revisiting_ConvNeXt-T-ConvStem": 72.72, "Singh2023Revisiting_ViT-S-ConvStem": 72.56,
    "Singh2023Revisiting_ConvNeXt-B-ConvStem": 75.90, "Singh2023Revisiting_ViT-B-ConvStem": 76.30,
    "Liu2023Comprehensive_ConvNeXt-B": 76.02, "Liu2023Comprehensive_Swin-B": 76.16,
    "Mo2022When_ViT-B": 68.38, "Debenedetti2022Light_XCiT-S12": 72.34, "Wong2020Fast": 55.62,
}


def denetim_karari(kendi, ortak, rb_temiz):
    """Ek on kayit §5.5 kurali; tek model icin. Donus: karar sozlugu.
    karar: 'gecti' | 'gecti_isaretli' | 'kaldi' | 'hesaplanamadi'."""
    if kendi is None or ortak is None:
        return {"karar": "hesaplanamadi", "neden": "kendi ya da ortak hat dogrulugu yok"}
    esik_i = DEN_ALT_SINIR if rb_temiz is None else max(DEN_ALT_SINIR, DEN_RB_KAT * rb_temiz)
    i_gecti = kendi >= esik_i
    fark = abs(ortak - kendi)
    ii_gecti = fark <= DEN_FARK_EN_COK
    isaret = ii_gecti and fark > DEN_FARK_ISARET
    if not (i_gecti and ii_gecti):
        karar = "kaldi"
    else:
        karar = "gecti_isaretli" if isaret else "gecti"
    r = {"karar": karar, "esik_i": round(esik_i, 4), "i_gecti": bool(i_gecti), "mutlak_fark_puan": round(fark, 2),
         "ii_gecti": bool(ii_gecti), "isaretli_3_5": bool(isaret), "rb_temiz": rb_temiz}
    if rb_temiz is None:
        r["uyari"] = "RobustBench temiz dogrulugu tabloda yok; (i) yalniz %25 ile uygulandi"
    return r


def onisleme_denetimi(models, specs, kok, secim, ortak_adi, batch_size, device):
    """Ortak hat ile modelin kendi RobustBench on islemesinde temiz dogruluk (ayni dosyalar) ve ek on kayit
    §5.5 kuralinin karari (denetim_karari)."""
    from robustbench.data import get_preprocessing
    from robustbench.model_zoo.enums import BenchmarkDataset, ThreatModel

    x_o, y = v2_tensor(kok, secim, v2_onisleme(ortak_adi))
    out = {}
    for n, m in models.items():
        stype, sref = specs[n]
        rec = {"model": sref}
        if stype == "robustbench":
            tf = get_preprocessing(BenchmarkDataset("imagenet"), ThreatModel("Linf"), sref, None)
            rec["kendi_onisleme"] = repr(tf).replace("\n", " ")
            x_k, _ = v2_tensor(kok, secim, tf)
        else:
            x_k = None
        for etiket, x in (("ortak", x_o), ("kendi", x_k)):
            if x is None:
                continue
            dogru = 0
            with torch.no_grad():
                for i in range(0, len(y), batch_size):
                    dogru += int((m(x[i:i + batch_size].to(device)).argmax(1).cpu() == y[i:i + batch_size]).sum())
            rec[f"temiz_dogruluk_{etiket}"] = round(100.0 * dogru / len(y), 2)
        if "temiz_dogruluk_kendi" in rec:
            rec["fark_puan"] = round(rec["temiz_dogruluk_ortak"] - rec["temiz_dogruluk_kendi"], 2)
        rec["esik"] = denetim_karari(rec.get("temiz_dogruluk_kendi"), rec.get("temiz_dogruluk_ortak"),
                                     RB_IN_TEMIZ.get(sref) if stype == "robustbench" else None)
        out[n] = rec
    return {"ortak_onisleme": ortak_adi, "n": len(y), "modeller": out,
            "kalan": sorted(k for k, v in out.items() if v["esik"]["karar"] == "kaldi"),
            "isaretli": sorted(k for k, v in out.items() if v["esik"]["karar"] == "gecti_isaretli"),
            "not": ("Esik kurali ek on kayit §5.5 (ON_KAYIT_EK_B8_B10_2026-10-30.md): (i) kendi hatta 1000 sinifli "
                    "temiz dogruluk >= %25 ve >= RobustBench temiz dogrulugunun 0,6 kati; (ii) |ortak - kendi| <= 5 "
                    "puan; 3 ile 5 puan arasi matriste kalir ve isaretlenir. 'kaldi' alan model matristen cikar "
                    "(P8 uyesiyse yedek IN_Wong2020Fast ayni denetimle girer; cift uyesiyse cift duzeyi "
                    "niceliklerden cikar). Sonuc T gorulmeden sapma kaydina yazilir.")}


def mifgsm_m84(model, images, labels, eps=EPS, steps=STEPS, mu=MI_MU):
    """MI-FGSM / MI-PGD, foy M8.4 ayarlari. experiments/run_c_addenda.py::mifgsm
    (C22) ile birebir ayni islem: alpha = eps/steps; g <- mu*g + grad/||grad||_1;
    x <- x + alpha*sign(g); eps topuna ve [0,1]'e izdusum; rastgele baslangic yok."""
    loss_fn = nn.CrossEntropyLoss(reduction="sum")
    alpha = eps / steps
    x0 = images.detach()
    x = x0.clone()
    g = torch.zeros_like(x)
    for _ in range(steps):
        x = x.detach().requires_grad_(True)
        loss = loss_fn(model(x), labels)
        grad = torch.autograd.grad(loss, x)[0]
        grad = grad / (grad.abs().flatten(1).sum(dim=1).view(-1, 1, 1, 1) + 1e-12)
        g = mu * g + grad
        x = x.detach() + alpha * g.sign()
        x = x0 + torch.clamp(x - x0, -eps, eps)
        x = torch.clamp(x, 0, 1)
    return x.detach()


_TGR_MOD = None


def _tgr_module():
    """experiments/c1_c2_tgr.py'yi dosya yolundan yukler (TGR kodu tek kaynak)."""
    global _TGR_MOD
    if _TGR_MOD is None:
        p = Path(__file__).resolve().parent / "c1_c2_tgr.py"
        spec = importlib.util.spec_from_file_location("c1_c2_tgr", p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _TGR_MOD = mod
    return _TGR_MOD


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _iter_batches(loader, n_samples):
    """Eski dongunun birebir aynisi: ilk n_samples ornegi batch batch verir."""
    seen = 0
    for images, labels in loader:
        if seen >= n_samples:
            break
        if seen + labels.size(0) > n_samples:
            keep = n_samples - seen
            images, labels = images[:keep], labels[:keep]
        yield seen, images, labels
        seen += labels.size(0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", type=int, nargs="+", default=[1, 2, 3])
    ap.add_argument("--n-samples", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--dataset", choices=sorted(DATASETS) + list(EK_DATASETS), default="cifar10")
    ap.add_argument("--rb-ref", type=str, default=None,
                    help="RobustBench referans model adi (varsayilan: kume standardi)")
    ap.add_argument("--model", action="append", default=None, metavar="AD:TIP:YOL",
                    help="PAIRS yerine acik model listesi (tekrarlanabilir); "
                         "verilirse tek kosu yapilir ve --out-dir kullanilir")
    ap.add_argument("--out-dir", type=str, default=None)
    # 2026-10-04 (LeCun plani Faz 2): birden cok RobustBench modeli, kendi adiyla.
    # AD[:TAKMA_AD]; verilirse VARSAYILAN referans (WRN_28_10) otomatik EKLENMEZ,
    # havuz tamamen acik listeden kurulur. Yalniz --model ile birlikte anlamli.
    ap.add_argument("--rb-model", action="append", default=None, metavar="AD[:TAKMA_AD]",
                    help="RobustBench modeli ekle (tekrarlanabilir); varsayilan referansi kapatir")
    # E6: tehdit modeli ekseni. VARSAYILAN linf -> eski davranis birebir korunur.
    ap.add_argument("--norm", choices=["linf", "l2"], default="linf")
    # Konsey B1 (29.10.2026): varsayilanlar eski davranis
    ap.add_argument("--attack", choices=["pgd", "mi", "tgr"], default="pgd")
    ap.add_argument("--steps", type=int, default=None,
                    help="Saldiri adim sayisi (varsayilan: 10)")
    ap.add_argument("--sources", nargs="+", default=None, metavar="AD",
                    help="Yalniz bu takma adlar kaynak olur (hepsi hedef kalir)")
    ap.add_argument("--cache-adv", type=str, default=None, metavar="DIR",
                    help="Kaynak basina cekismeli ornek onbellegi (kaydet / yeniden kullan)")
    ap.add_argument("--skip-existing", action="store_true",
                    help="Hucre bazinda: npz'si olan hucreyi yeniden hesaplama")
    # EK (30.10.2026): varsayilanlar ozgun davranis
    ap.add_argument("--eps", type=float, default=None, help="Linf yaricap, 255 cinsinden (varsayilan 8)")
    ap.add_argument("--alpha", type=float, default=None, help="Linf adim, 255 cinsinden (varsayilan 2; yalniz --eps ise eps/4)")
    ap.add_argument("--batch-size", type=int, default=50)
    ap.add_argument("--cache-root", type=str, default=None,
                    help="--cache-adv goreli ise bu kokun altina yazilir")
    ap.add_argument("--cache-f16", action="store_true",
                    help="onbellekte perturbasyonu float16 sakla (yari disk)")
    ap.add_argument("--v2-kok", type=str, default="data/imagenetv2")
    ap.add_argument("--v2-sinif-dosya", type=int, default=10,
                    help="her sinif klasorunde beklenen dosya sayisi (ImageNetV2: 10); 0 denetimi kapatir")
    ap.add_argument("--in-onisleme", choices=["BicubicRes256Crop224", "Res256Crop224"], default="BicubicRes256Crop224",
                    help="ImageNetV2 ortak hatti (ek on kayit §5.2; varsayilan bicubic)")
    ap.add_argument("--onisleme-denetimi", action="store_true")
    ap.add_argument("--yalniz-denetim", action="store_true")
    args = ap.parse_args()
    ek_eps = args.eps is not None or args.alpha is not None
    if args.norm == "l2":
        if ek_eps:
            raise SystemExit("--eps/--alpha yalniz --norm linf ile tanimli")
        atk_cls, atk_eps, atk_alpha, atk_steps = PGDL2Attack, EPS_L2, ALPHA_L2, STEPS_L2
    else:
        atk_cls, atk_eps, atk_alpha, atk_steps = PGDAttack, EPS, ALPHA, STEPS
        if args.eps is not None:
            atk_eps = args.eps / 255
            atk_alpha = (args.alpha if args.alpha is not None else args.eps / 4) / 255
        elif args.alpha is not None:
            atk_alpha = args.alpha / 255
    if args.cache_f16 and not args.cache_adv:
        raise SystemExit("--cache-f16 yalniz --cache-adv ile anlamli")
    if args.cache_adv and args.cache_root and not Path(args.cache_adv).is_absolute():
        args.cache_adv = str(Path(args.cache_root) / args.cache_adv)
    if (args.onisleme_denetimi or args.yalniz_denetim) and args.dataset != "imagenetv2":
        raise SystemExit("--onisleme-denetimi yalniz --dataset imagenetv2 ile")
    if args.dataset == "imagenetv2" and not args.model and not args.rb_model:
        raise SystemExit("imagenetv2: --rb-model (ya da --model) listesi gerekir")
    if args.steps is not None:
        atk_steps = args.steps
    if args.attack != "pgd" and args.norm != "linf":
        raise SystemExit("--attack mi/tgr yalniz --norm linf ile tanimli")
    if args.attack == "mi":
        atk_alpha = atk_eps / atk_steps
    elif args.attack == "tgr":
        atk_alpha = _tgr_module().ALPHA
    konsey_mode = (args.attack != "pgd" or args.steps is not None or args.sources
                   or args.cache_adv or args.skip_existing)
    if args.skip_existing and not args.cache_adv:
        # Onbelleksiz devamda yarida kalan satir ilk kosudakinden farkli cekismeli
        # orneklerle tamamlanir (kaynak basina tohum yalniz onbellekte atilir);
        # source_adv_wrong eski, target_adv_wrong yeni orneklerden gelir.
        raise SystemExit("--skip-existing yalniz --cache-adv ile birlikte kullanilabilir "
                         "(yarida kalan satirin ayni cekismeli orneklerle tamamlanmasi icin)")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # Referans model: SVHN'de RobustBench yok -> --model listesine ucuncu bir
    # spec olarak kendi referansimiz (or. DenseNet121_ref:densenet121:...) verilir
    # ve WRN otomatik eklenmez. PAIRS modunda referans zorunludur.
    has_rb = bool(args.rb_ref) or args.dataset in ("cifar10", "cifar100")
    if args.rb_model:
        has_rb = False  # acik RobustBench listesi verildi; varsayilan referans eklenmez
    ek_ds = args.dataset in EK_DATASETS
    if ek_ds and not args.rb_ref:
        has_rb = False  # EK: imagenetv2'de varsayilan referans yok
    wrn = load_wrn(device, dataset=args.dataset, rb_name=args.rb_ref) if has_rb else None
    custom = bool(args.model) or ek_ds  # EK: imagenetv2 yalniz --rb-model listesiyle de tek kosu
    if wrn is None and not custom:
        raise SystemExit(f"{args.dataset}: RobustBench referansi yok; PAIRS modu "
                         f"kullanilamaz. --model ile acik liste (referans dahil) verin.")

    # Q1: --model AD:TIP:YOL verilirse PAIRS yerine acik listeyle TEK kosu
    if custom:
        runs = [("custom", None, None)]
    else:
        runs = [(f"pair{p}",) + PAIRS[p] for p in args.pairs]

    for run_tag, rs, vs in runs:
        if custom:
            out_dir = Path(args.out_dir or f"results/q1/{args.dataset}/c3_matrix")
        else:
            out_dir = Path(f"results/c1_c3/{run_tag}")
        out_dir.mkdir(parents=True, exist_ok=True)
        if (out_dir / "transfer_matrix.json").exists() and not args.skip_existing:
            print(f"{run_tag}: artefakt mevcut, atlandi")
            continue

        set_seed(args.seed)
        specs = {}  # takma ad -> (tip, yol/ad); onbellek meta ve TGR uygunlugu icin
        if custom:
            models = {}
            for spec in (args.model or []):
                name, mtype, mpath = spec.split(":", 2)
                models[name] = load_local(mtype, mpath, device)
                specs[name] = (mtype, mpath)
            if wrn is not None:
                models["WRN_28_10"] = wrn
                specs["WRN_28_10"] = ("robustbench", args.rb_ref or "default")
            for spec in (args.rb_model or []):
                rb_name, _, alias = spec.partition(":")
                models[alias or rb_name] = load_wrn(device, dataset=args.dataset, rb_name=rb_name)
                specs[alias or rb_name] = ("robustbench", rb_name)
        else:
            rp = f"models/c1/resnet18_s{rs}/resnet18/adv/adversarial_training/best.pth"
            vp = f"models/c1/vit_tiny_s{vs}/vit_tiny/adv/adversarial_training/best.pth"
            models = {
                "ResNet18_AT": load_local("resnet18", rp, device),
                "ViT_Tiny_AT": load_local("vit_tiny", vp, device),
                "WRN_28_10": wrn,
            }
            specs = {"ResNet18_AT": ("resnet18", rp), "ViT_Tiny_AT": ("vit_tiny", vp),
                     "WRN_28_10": ("robustbench", args.rb_ref or "default")}
        names = list(models)

        # Kaynak listesi (varsayilan: hepsi)
        sources = list(names)
        if args.sources:
            unknown = [s for s in args.sources if s not in models]
            if unknown:
                raise SystemExit(f"--sources bilinmeyen takma ad: {unknown}; mevcut: {names}")
            sources = [n for n in names if n in args.sources]
        if args.attack == "tgr":
            skipped = [s for s in sources if specs[s][0] not in VIT_TYPES]
            if skipped:
                print(f"TGR yalniz ViT kaynaklarinda; kaynak olarak atlanan: {skipped}")
            sources = [s for s in sources if specs[s][0] in VIT_TYPES]
            if not sources:
                raise SystemExit("TGR icin ViT kaynagi yok")

        # Hucre meta: --skip-existing farkli ayarla uretilmis hucreleri karistirmasin
        cell_cfg = {"attack": args.attack, "norm": args.norm, "eps": atk_eps,
                    "alpha": atk_alpha, "steps": atk_steps, "seed": args.seed,
                    "n_samples": args.n_samples, "dataset": args.dataset,
                    "per_source_seed": bool(args.cache_adv)}
        # EK: yalniz yeni bayraklarda eklenir (eski onbellek ve hucre metasi gecerli kalir)
        if args.batch_size != 50:
            cell_cfg["batch_size"] = args.batch_size
        if args.cache_f16:
            cell_cfg["cache_dtype"] = "float16_delta"
        if ek_ds:
            cell_cfg["onisleme"] = args.in_onisleme
        if konsey_mode:
            meta_path = out_dir / "cells_meta.json"
            if meta_path.exists():
                old_cfg = json.loads(meta_path.read_text())
                if args.skip_existing and old_cfg != cell_cfg:
                    raise SystemExit(f"{meta_path}: klasordeki hucreler farkli ayarla "
                                     f"uretilmis: {old_cfg} != {cell_cfg}")
            meta_path.write_text(json.dumps(cell_cfg, indent=2))

        v2_manifest = None
        if ek_ds:
            (_, test_loader), v2_manifest = v2_loaders(args.v2_kok, args.n_samples, args.batch_size,
                                                       args.in_onisleme, args.v2_sinif_dosya or None)
            (out_dir / "imagenetv2_manifest.json").write_text(json.dumps(v2_manifest, indent=1))
            print(f"ImageNetV2: n={v2_manifest['n']} liste_sha256={v2_manifest['liste_sha256'][:16]} "
                  f"onisleme={args.in_onisleme}")
            if args.onisleme_denetimi or args.yalniz_denetim:
                kok_, secim_ = v2_secim(args.v2_kok, args.n_samples, args.v2_sinif_dosya or None)
                den = onisleme_denetimi(models, specs, kok_, secim_, args.in_onisleme, args.batch_size, device)
                den["normalizasyon"] = {n: normalizasyon_envanteri(m) for n, m in models.items()}
                (out_dir / "onisleme_denetimi.json").write_text(json.dumps(den, indent=1))
                for n, r in den["modeller"].items():
                    print(f"  denetim {n}: ortak={r.get('temiz_dogruluk_ortak')} kendi={r.get('temiz_dogruluk_kendi')} "
                          f"karar={r['esik']['karar']}")
                if args.yalniz_denetim:
                    print(f"yalniz denetim: {out_dir / 'onisleme_denetimi.json'}")
                    return
        else:
            _, test_loader = get_loaders(dataset=args.dataset, data_dir="./data", test_batch_size=args.batch_size)

        # Once tum modellerin temiz-dogru maskeleri (ayni ornek sirasi)
        clean_ok = {n: [] for n in names}
        labels_all = []
        for _s, images, labels in _iter_batches(test_loader, args.n_samples):
            images, labels = images.to(device), labels.to(device)
            with torch.no_grad():
                for n in names:
                    clean_ok[n].append((models[n](images).argmax(1) == labels).cpu().numpy())
            labels_all.append(labels.cpu().numpy())
        clean_ok = {n: np.concatenate(v) for n, v in clean_ok.items()}
        print(f"{run_tag} temiz dogruluk: " + ", ".join(f"{n}={100 * clean_ok[n].mean():.2f}" for n in names))

        def cell_file(s, t):
            return out_dir / f"per_sample_{s}_to_{t}.npz"

        def load_cell(s, t):
            d = np.load(cell_file(s, t))
            if not np.array_equal(d["target_clean_correct"], clean_ok[t]):
                raise SystemExit(f"{cell_file(s, t)}: hedef temiz maskesi bu kosuyla "
                                 f"uyusmuyor (farkli n ya da model); --skip-existing kullanilamaz")
            return d

        results = {}
        for src in sources:
            if args.skip_existing:
                todo = [t for t in names if not cell_file(src, t).exists()]
            else:
                todo = list(names)
            if not todo:
                print(f"  {src}: butun hucreler mevcut, kaynak atlandi")
                for tgt in names:
                    d = load_cell(src, tgt)
                    aw, cond = d["target_adv_wrong"], d["target_clean_correct"]
                    results[f"{src}->{tgt}"] = {
                        "raw_fooling": round(float(100 * aw.mean()), 2),
                        "cond_fooling": round(float(100 * aw[cond].mean()), 2),
                        "n_cond": int(cond.sum()),
                        "target_clean_acc": round(float(100 * cond.mean()), 2),
                    }
                continue
            fwd = list(todo)
            if src not in fwd and not cell_file(src, src).exists():
                fwd.append(src)
            fwd = [n for n in names if n in fwd]  # model sirasini koru

            # Cekismeli ornek kaynagi: onbellek ya da saldiri
            cached_adv = None
            cache_file = cache_meta_file = None
            src_meta = None
            if args.cache_adv:
                cdir = Path(args.cache_adv)
                cdir.mkdir(parents=True, exist_ok=True)
                stem = (f"{src}__{args.attack}_{args.norm}_s{atk_steps}_n{args.n_samples}"
                        f"_seed{args.seed}_{args.dataset}")
                if ek_eps:  # EK: farkli eps'li ornekler eski onbellege karismasin
                    stem += f"_e{atk_eps * 255:g}_a{atk_alpha * 255:g}"
                if args.batch_size != 50:
                    stem += f"_b{args.batch_size}"
                if args.cache_f16:
                    stem += "_f16"
                cache_file, cache_meta_file = cdir / f"{stem}.npy", cdir / f"{stem}.json"
                stype, sref = specs[src]
                src_meta = dict(cell_cfg, source=src, source_type=stype, source_ref=sref,
                                source_sha256=(_sha256(sref) if stype != "robustbench" else None))
                if cache_file.exists() and cache_meta_file.exists():
                    old = json.loads(cache_meta_file.read_text())
                    if old != src_meta:
                        raise SystemExit(f"{cache_meta_file}: onbellek meta uyusmuyor "
                                         f"({old} != {src_meta})")
                    cached_adv = torch.from_numpy(np.load(cache_file))
                    print(f"  {src}: onbellekten {tuple(cached_adv.shape)}")
                else:
                    set_seed(args.seed)  # kaynak basina tohum: sira bagimsiz onbellek

            if cached_adv is None:
                if args.attack == "pgd":
                    attack = atk_cls(models[src], eps=atk_eps, alpha=atk_alpha, steps=atk_steps)
                elif args.attack == "mi":
                    models[src].eval()

                    def attack(x, y, _m=models[src]):
                        return mifgsm_m84(_m, x, y, eps=atk_eps, steps=atk_steps)
                else:
                    models[src].eval()
                    tgr = _tgr_module()

                    def attack(x, y, _m=models[src]):
                        return tgr.mifgsm(_m, x, y, use_tgr=True, eps=atk_eps,
                                          alpha=atk_alpha, steps=atk_steps, mu=tgr.MU)
            else:
                attack = None
            adv_store = [] if (args.cache_adv and cached_adv is None) else None

            adv_wrong = {n: [] for n in fwd}
            for s0, images, labels in _iter_batches(test_loader, args.n_samples):
                images, labels = images.to(device), labels.to(device)
                if args.cache_f16:
                    # EK: onbellek perturbasyonu float16 tutar; taze ve onbellekli yol ayni geri kurulmus
                    # ornegi kullanir (yaricapa ve [0,1]'e yeniden izdusum).
                    if attack is not None:
                        delta = (attack(images, labels) - images).detach().to(torch.float16)
                    else:
                        delta = cached_adv[s0:s0 + labels.size(0)].to(device)
                    if adv_store is not None:
                        adv_store.append(delta.cpu().numpy())
                    adv = torch.clamp(images + torch.clamp(delta.float(), -atk_eps, atk_eps), 0, 1)
                elif attack is not None:
                    adv = attack(images, labels)
                else:
                    adv = cached_adv[s0:s0 + labels.size(0)].to(device)
                if adv_store is not None and not args.cache_f16:
                    adv_store.append(adv.detach().cpu().numpy().astype(np.float32))
                with torch.no_grad():
                    for n in fwd:
                        adv_wrong[n].append((models[n](adv).argmax(1) != labels).cpu().numpy())
            if adv_store is not None:
                arr = np.concatenate(adv_store)
                tmp = cache_file.with_name(cache_file.name + ".tmp.npy")
                np.save(tmp, arr)
                tmp.replace(cache_file)
                cache_meta_file.write_text(json.dumps(src_meta, indent=2))
                print(f"  {src}: onbellege yazildi {cache_file} {arr.shape}")
            # Kaynagin KENDI cekismeli orneklerine kanip kanmadigi (kosegen).
            # a2_transfer_protocols'un successful_source protokolu bunu ister;
            # sema boylece C1 artefaktlariyla ayni dort anahtara sahip olur.
            if src in adv_wrong:
                src_aw = np.concatenate(adv_wrong[src])
            else:
                src_aw = load_cell(src, src)["target_adv_wrong"]
            for tgt in names:
                if tgt in adv_wrong:
                    aw = np.concatenate(adv_wrong[tgt])
                    cond = clean_ok[tgt]
                else:
                    d = load_cell(src, tgt)
                    aw, cond = d["target_adv_wrong"], d["target_clean_correct"]
                results[f"{src}->{tgt}"] = {
                    "raw_fooling": round(float(100 * aw.mean()), 2),
                    "cond_fooling": round(float(100 * aw[cond].mean()), 2),
                    "n_cond": int(cond.sum()),
                    "target_clean_acc": round(float(100 * cond.mean()), 2),
                }
                if tgt in adv_wrong:
                    np.savez(cell_file(src, tgt),
                             target_clean_correct=cond, target_adv_wrong=aw,
                             source_clean_correct=clean_ok[src],
                             source_adv_wrong=src_aw)
                print(f"  {src}->{tgt}: raw={results[f'{src}->{tgt}']['raw_fooling']:.2f} "
                      f"cond={results[f'{src}->{tgt}']['cond_fooling']:.2f}"
                      + ("" if tgt in adv_wrong else " (mevcut hucre)"))
            del attack, cached_adv
            torch.cuda.empty_cache()

        out = {"pair": run_tag, "seed": args.seed, "n_samples": args.n_samples,
               "eps": atk_eps, "alpha": atk_alpha, "steps": atk_steps,
               "norm": args.norm,
               "models": names, "results": results}
        if konsey_mode:
            # Yalniz yeni bayraklar kullanildiginda eklenir (eski sema korunur)
            out.update({"attack": args.attack, "sources": sources,
                        "cache_adv": args.cache_adv, "per_source_seed": bool(args.cache_adv),
                        "model_specs": {n: list(specs[n]) for n in names}})
        # EK: yalniz ek bayraklarda eklenir
        if ek_eps or args.batch_size != 50 or args.cache_f16 or ek_ds:
            out.update({"ek_betik": "experiments/q1_ek_transfer_matrix.py",
                        "ek_betik_sha256": _sha256(Path(__file__)),
                        "eps_255": atk_eps * 255, "alpha_255": atk_alpha * 255,
                        "batch_size": args.batch_size, "cache_f16": bool(args.cache_f16),
                        "model_specs": {n: list(specs[n]) for n in names}})
        if ek_ds:
            out.update({"dataset": args.dataset, "on_isleme": args.in_onisleme,
                        "manifest_liste_sha256": v2_manifest["liste_sha256"],
                        "manifest_n": v2_manifest["n"], "v2_kok": v2_manifest["kok"],
                        "normalizasyon": {n: normalizasyon_envanteri(models[n]) for n in names},
                        "temiz_dogruluk": {n: round(float(100 * clean_ok[n].mean()), 2) for n in names}})
        with open(out_dir / "transfer_matrix.json", "w") as f:
            json.dump(out, f, indent=2)
        print(f"{run_tag} kaydedildi: {out_dir}")


if __name__ == "__main__":
    main()
