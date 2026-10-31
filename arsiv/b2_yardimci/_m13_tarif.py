# -*- coding: utf-8 -*-
"""Y1 (fig:design_recipe) icin makine okunur tasarim ve egitim tarifi: results/q1/konsey_b3_tarif.json.

Her deger bir kaynaktan okunur (31.10.2026, deney-takibi):
  - gercekten kosulan komut satirlari: logs/konsey_zincir.log 'BASLA <takma> temiz|AT' satirlari (B3 alti kosu),
    scripts/run_c1_pipeline.sh (C1 V-scr ve C1-R32 komutlari; komut sablonu);
  - komut sablonlari: scripts/konsey_b3_kuyruk.sh temiz_cmd/at_cmd (gercek komutla bayrak bayrak karsilastirilir);
  - varsayilanlar: cli/train.py click secenekleri, src/training/trainer.py, src/training/adversarial_trainer.py,
    src/defenses/adversarial_training.py, src/data/datasets.py, src/models/*.py;
  - egitim gunluklerinin baslik satirlari (Epochs/LR/Batch, eniyileyici satiri) capraz denetim icin;
  - ON_KAYIT_2026-10-29.md §3 tablo satirlari ve AT tarifi paragrafi (metin karsiligi);
  - results/q1/konsey_pilot_zaman.json secilen_tavan; data/val_split_indices.json val_size.
Gerceklesen epok sayilari foy M9.1'de (B3) ve M8.14'te (C1) oldugu icin burada tekrarlanmaz; foy satir referansi verilir.
Calistirma: depo kokunden `python3 arsiv/b2_yardimci/_m13_tarif.py` (WSL ya da konteyner; yalniz standart kutuphane).
"""
import re
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _m13_ortak as O  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
CIKTI = "results/q1/konsey_b3_tarif.json"
KUY = "scripts/konsey_b3_kuyruk.sh"
ZL = "logs/konsey_zincir.log"
RC1 = "scripts/run_c1_pipeline.sh"
CLI = "cli/train.py"
TR = "src/training/trainer.py"
ATR = "src/training/adversarial_trainer.py"
ATD = "src/defenses/adversarial_training.py"
DS = "src/data/datasets.py"
OK = "raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md"
HT = "raporlar/konsey_2026-10-29/hucre_tablosu.json"
PZ = "results/q1/konsey_pilot_zaman.json"
VAL = "data/val_split_indices.json"
MODELLER = ("src/models/vit.py", "src/models/resnet.py", "src/models/r224.py")
ALIAS = {"-m": "model", "-e": "epochs", "-b": "batch_size", "-o": "output_dir", "-p": "pretrained", "-d": "defense"}
B3_TAKMA = ()  # main() icinde zincir gunlugunun BASLA satirlarindan, kosu sirasiyla doldurulur


def k(rel, n):
    return f"{rel}:{n}"


# --- komut ayristirma --------------------------------------------------------------------------
def bayraklar(cmd):
    t = shlex.split(cmd)
    i = t.index("train")
    alt = t[i + 1]
    out, j = {}, i + 2
    while j < len(t):
        a = t[j]
        if a.startswith("-"):
            ad = ALIAS.get(a, a.lstrip("-").replace("-", "_"))
            if j + 1 < len(t) and not t[j + 1].startswith("-"):
                out[ad] = t[j + 1]
                j += 2
            else:
                out[ad] = True
                j += 1
        else:
            j += 1
    return alt, out


def zincir_komutlari():
    """logs/konsey_zincir.log: '[...] BASLA <takma> <asama> (...): <komut> --resume' satirlari."""
    L = O.satirlar(ZL)
    out = {}
    for n, s in enumerate(L, 1):
        m = re.match(r"\[([0-9: -]+)\] BASLA (\S+) (temiz|AT) \(([^)]*)\): (python -m cli\.main .*)$", s)
        if m:
            out[(m.group(2), m.group(3))] = {"komut": m.group(5), "kaynak": k(ZL, n), "kip": m.group(4)}
    return out


def kuyruk_sablonu(hucre, asama):
    L = O.satirlar(KUY)
    if asama == "temiz":
        n = O.bul(KUY, f'{hucre}) echo "python -m cli.main train clean')
        s = re.search(r'echo "(.*)" ;;', L[n - 1]).group(1)
    else:
        n = O.bul(KUY, 'echo "python -m cli.main train adversarial')
        s = re.search(r'echo "(.*)"', L[n - 1]).group(1)
    return s, n


def c1_komutu(desen):
    """run_c1_pipeline.sh icinde ters bolu ile devam eden cok satirli komut."""
    L = O.satirlar(RC1)
    n = O.bul(RC1, desen)
    parca, i = [], n
    while True:
        s = L[i - 1].strip()
        parca.append(s.rstrip("\\").strip())
        if not s.endswith("\\"):
            break
        i += 1
    return " ".join(parca), n, i


# --- varsayilanlar ------------------------------------------------------------------------------
def cli_varsayilanlari():
    L = O.satirlar(CLI)
    d_clean = O.bul(CLI, "def clean(")
    d_adv = O.bul(CLI, "def adversarial(")
    bloklar, cur = [], None
    for n, s in enumerate(L, 1):
        if s.startswith("@click.option("):
            if cur:
                bloklar.append(cur)
            cur = [n, s]
        elif cur and (s.startswith("@") or s.startswith("def ")):
            bloklar.append(cur)
            cur = None
        elif cur:
            cur[1] += " " + s.strip()
    out = {"clean": {}, "adversarial": {}}
    for n, s in bloklar:
        adlar = re.findall(r'"(--[a-z0-9-]+)"', s)
        dm = re.search(r"default=([^,)]+(?:\([^)]*\))?)", s)
        if not adlar or not dm:
            continue
        ad = adlar[0].lstrip("-").replace("-", "_")
        hedef = "clean" if n < d_clean else ("adversarial" if n < d_adv else None)
        if hedef:
            out[hedef][ad] = {"ifade": dm.group(1).strip().strip('"'), "kaynak": k(CLI, n)}
    return out


def model_siniflari():
    out = {}
    for rel in MODELLER:
        L = O.satirlar(rel)
        for n, s in enumerate(L, 1):
            m = re.match(r'@register_model\("([^"]+)"\)', s)
            if m:
                c = re.match(r"class (\w+)\(", L[n])
                if c:
                    out[m.group(1)] = {"sinif": c.group(1), "kaynak": k(rel, n + 1)}
    return out


def vit_mi(sinif):
    """trainer.py ile ayni kural (kaynak satiri kayitta)."""
    a = sinif.lower()
    return "vit" in a or "vision" in a or "transformer" in a


def gunluk_basligi(rel):
    """Egitim gunlugunun ilk 'Epochs:' satiri ve eniyileyici satiri (capraz denetim)."""
    L = O.satirlar(rel)
    o = {}
    for n, s in enumerate(L[:40], 1):
        if "Epochs:" in s and "epochs_satiri" not in o:
            o["epochs_satiri"] = {"kaynak": k(rel, n), "metin": s.strip()}
        if s.startswith("Using ") and "optimizer" in s and "eniyileyici_satiri" not in o:
            o["eniyileyici_satiri"] = {"kaynak": k(rel, n), "metin": s.strip()}
        if s.startswith("Optimizer: ") and "optimizer_satiri" not in o:
            o["optimizer_satiri"] = {"kaynak": k(rel, n), "metin": s.strip()}
        if "Early stopping enabled" in s and "erken_durma_satiri" not in o:
            o["erken_durma_satiri"] = {"kaynak": k(rel, n), "metin": s.strip()}
        if s.startswith("INIT_WEIGHTS_RAPORU ") and "init" not in o:
            import json
            o["init"] = {"kaynak": k(rel, n), **json.loads(s[len("INIT_WEIGHTS_RAPORU "):])}
    return o


# --- kanitlar (tek yerde) -----------------------------------------------------------------------
KAN = {
    "is_vit": O.kanit(TR, "is_vit = 'vit' in model_name"),
    "temiz_vit_lr_tavani": O.kanit(TR, "effective_lr = min(lr, ", r"min\(lr, ([0-9.e-]+)\)"),
    "temiz_adamw_zorla": O.kanit(TR, "optim.AdamW(self.model.parameters(), lr=lr, weight_decay=", r"weight_decay=([0-9.]+)"),
    "temiz_adamw_auto_wd": O.kanit(TR, "weight_decay=0.05,", r"weight_decay=([0-9.]+)", sira=0),
    "temiz_sgd_momentum": O.kanit(TR, "momentum: float = ", r"= ([0-9.]+)"),
    "temiz_sgd_wd": O.kanit(TR, "weight_decay: float = ", r"= ([0-9.e-]+)"),
    "temiz_cosine": O.kanit(TR, "T_max=epochs,"),
    "at_adamw_zorla": O.kanit(ATR, "optim.AdamW(self.model.parameters(), lr=lr, weight_decay=", r"weight_decay=([0-9.]+)"),
    "at_adamw_auto_wd": O.kanit(ATR, "weight_decay=0.05,", r"weight_decay=([0-9.]+)", sira=0),
    "at_vit_lr": O.kanit(ATR, "effective_lr = min(lr, vit_lr_cap)"),
    "at_is_vit": O.kanit(ATR, "is_vit = 'vit' in model_name"),
    "at_sgd_momentum": O.kanit(ATR, "momentum: float = ", r"= ([0-9.]+)"),
    "at_sgd_wd": O.kanit(ATR, "weight_decay: float = ", r"= ([0-9.e-]+)"),
    "at_cosine": O.kanit(ATR, "self.optimizer, T_max=epochs,"),
    "at_min_delta": O.kanit(ATR, "min_delta: float = ", r"= ([0-9.]+)"),
    "at_min_delta_kullanim": O.kanit(ATR, "adv_acc > self.best_adv_acc + self.min_delta"),
    "at_savunma_kurulumu": O.kanit(ATR, "self.defense = AdversarialTraining("),
    "mix_ratio": O.kanit(ATD, "mix_ratio: float = ", r"= ([0-9.]+)"),
    "karisik_kayip": O.kanit(ATD, "loss = (1 - self.mix_ratio) * loss_clean + self.mix_ratio * loss_adv"),
    "random_start": O.kanit(ATD, "random_start: bool = ", r"= (\w+)", tip=lambda x: x == "True"),
    "artirma_crop": O.kanit(DS, 'aug = [T.RandomCrop(spec["img_size"], padding=', r"padding=([0-9]+)", tip=int),
    "artirma_flip": O.kanit(DS, "aug.append(T.RandomHorizontalFlip())"),
    "cifar10_spec": O.kanit(DS, '"img_size": 32, "flip": True', sira=0),
    "vit_upsample": O.kanit("src/models/vit.py", 'self.resize = nn.Upsample(size=(224, 224), mode="bilinear"', sira=0),
    "vit_timm": O.kanit("src/models/vit.py", '"vit_tiny_patch16_224",'),
    "r224_resize_norm": O.kanit("src/models/r224.py", 'self.up = nn.Upsample(size=(size, size), mode="bilinear"'),
    "r224_timm": O.kanit("src/models/r224.py", 'timm.create_model("resnet18", pretrained=False'),
    "r224_buyutme": O.kanit("src/models/r224.py", "self.resize = ResizeNormalize(", r"ResizeNormalize\((\d+),", tip=int, sira=0),
    "resnet32_kok": O.kanit("src/models/resnet.py", "First conv layer uses 3x3 kernel"),
    "init_deit": O.kanit("src/models/r224.py", '"deit_tiny_in1k": ('),
    "init_r18a1": O.kanit("src/models/r224.py", '"resnet18_a1_in1k": ('),
    "ok_vscr": O.kanit(OK, "| V-scr | ViT-Tiny"),
    "ok_vin": O.kanit(OK, "| V-IN | aynı mimari"),
    "ok_rscr": O.kanit(OK, "| R224-scr | timm `resnet18`"),
    "ok_rin": O.kanit(OK, "| R224-IN | timm `resnet18`"),
    "ok_at": O.kanit(OK, "AT tarifi bütün hücrelerde"),
    "ok_yakinsama": O.kanit(OK, "Yakınsamış model: C1 seçim kuralıyla"),
}
_r = O.satirlar("src/models/resnet.py")
KAN["resnet32_normalizasyon_yok"] = {
    "dosya": "src/models/resnet.py",
    "denetim": "dosyada 'normaliz', 'Normalize', '.mean', '.std' ve 'Upsample' geciyor mu (buyuk/kucuk harf duyarsiz)",
    "eslesen_satir_sayisi": sum(1 for s in _r if re.search(r"normaliz|\.mean|\.std|upsample", s, re.I))}


def eniyileyici(asama, f, sinif, cli):
    """Komut bayraklarindan ve kod varsayilanlarindan eniyileyici, lr, wd, momentum."""
    opt = f.get("optimizer", cli["optimizer"]["ifade"])
    lr = float(f.get("lr", cli["lr"]["ifade"]))
    on = "temiz" if asama == "temiz" else "at"
    if opt == "adamw":
        kn = KAN[f"{on}_adamw_zorla"]
        return {"eniyileyici": "AdamW", "secim": "--optimizer adamw (zorla)", "lr_etkin": lr,
                "agirlik_azaltma": kn["deger"], "kaynak": k(kn["dosya"], kn["satir"])}
    if opt != "auto":
        raise SystemExit(f"beklenmeyen eniyileyici {opt}")
    v = vit_mi(sinif)
    kv = KAN["is_vit" if on == "temiz" else "at_is_vit"]
    if v:
        if on == "temiz":
            tavan = KAN["temiz_vit_lr_tavani"]["deger"]
            kt = KAN["temiz_vit_lr_tavani"]
        else:
            tavan = O.kesir(cli["vit_lr_cap"]["ifade"])
            kt = {"dosya": CLI, "satir": int(cli["vit_lr_cap"]["kaynak"].rsplit(":", 1)[1])}
        kw = KAN[f"{on}_adamw_auto_wd"]
        return {"eniyileyici": "AdamW", "secim": f"--optimizer auto; sinif {sinif} ViT kuralina uyar",
                "lr_etkin": min(lr, tavan), "vit_lr_tavani": tavan, "agirlik_azaltma": kw["deger"],
                "kaynak": f"{k(kv['dosya'], kv['satir'])}; {k(kw['dosya'], kw['satir'])}; {k(kt['dosya'], kt['satir'])}"}
    km, kw = KAN[f"{on}_sgd_momentum"], KAN[f"{on}_sgd_wd"]
    return {"eniyileyici": "SGD", "secim": f"--optimizer auto; sinif {sinif} ViT kuralina uymaz", "lr_etkin": lr,
            "momentum": km["deger"], "agirlik_azaltma": kw["deger"],
            "kaynak": f"{k(kv['dosya'], kv['satir'])}; {k(km['dosya'], km['satir'])}; {k(kw['dosya'], kw['satir'])}"}


def asama_ozeti(asama, cmd, kaynak, cli, siniflar):
    alt, f = bayraklar(cmd)
    c = cli["clean" if asama == "temiz" else "adversarial"]
    beklenen = "clean" if asama == "temiz" else "adversarial"
    if alt != beklenen:
        raise SystemExit(f"{kaynak}: alt komut {alt} != {beklenen}")
    model = f["model"]
    sinif = siniflar[model]["sinif"]

    def deger(ad, tip=float):
        if ad in f:
            return tip(f[ad]), f"komut ({kaynak})"
        return tip(O.kesir(c[ad]["ifade"])) if tip is float else tip(c[ad]["ifade"]), f"varsayilan ({c[ad]['kaynak']})"

    ep, ep_k = deger("epochs", int)
    lr, lr_k = deger("lr")
    b, b_k = deger("batch_size", int)
    o = {"komut": cmd, "komut_kaynagi": kaynak, "model_anahtari": model, "model_sinifi": sinif,
         "model_sinifi_kaynagi": siniflar[model]["kaynak"],
         "epok_bayragi": ep, "epok_kaynagi": ep_k, "lr_bayragi": lr, "lr_kaynagi": lr_k,
         "batch": b, "batch_kaynagi": b_k, "tohum": int(f["seed"]),
         "dogrulama_bolmesi": f.get("val_indices"),
         **{"eniyileyici_" + x: y for x, y in eniyileyici(asama, f, sinif, c).items()}}
    if asama == "temiz":
        sc = f.get("lr_schedule", c["lr_schedule"]["ifade"])
        o["lr_cizelgesi"] = {"tur": sc, "T_max_epok": ep if sc == "cosine" else None,
                             "kaynak": (f"komut ({kaynak})" if "lr_schedule" in f else f"varsayilan ({c['lr_schedule']['kaynak']})")
                             + f"; {k(KAN['temiz_cosine']['dosya'], KAN['temiz_cosine']['satir'])}"}
        o["baslatma_bayragi"] = f.get("init_weights", c["init_weights"]["ifade"])
        o["baslatma_kaynagi"] = f"komut ({kaynak})" if "init_weights" in f else f"varsayilan ({c['init_weights']['kaynak']})"
    else:
        st = int(f["stop_epoch"]) if "stop_epoch" in f else int(c["stop_epoch"]["ifade"])
        o["lr_cizelgesi"] = {"tur": "cosine", "T_max_epok": ep,
                             "kaynak": f"{k(KAN['at_cosine']['dosya'], KAN['at_cosine']['satir'])} (lr_warmup varsayilan "
                                       f"{c['lr_warmup']['ifade']}, {c['lr_warmup']['kaynak']})"}
        o["epok_tavani"] = st if st > 0 else ep
        o["epok_tavani_kaynagi"] = (f"--stop-epoch komut ({kaynak})" if st > 0 else
                                    f"--stop-epoch yok (varsayilan {c['stop_epoch']['ifade']}, {c['stop_epoch']['kaynak']}); tavan = -e")
        pt, pt_k = deger("patience", int)
        o["sabir"], o["sabir_kaynagi"] = pt, pt_k
        o["savunma"] = f.get("defense", c["defense"]["ifade"])
        for ad in ("eps", "alpha"):
            v = O.kesir(c[ad]["ifade"]) if ad not in f else float(f[ad])
            o[ad] = v
            o[ad + "_x255"] = v * 255
            o[ad + "_ifade"] = c[ad]["ifade"] if ad not in f else f[ad]
            o[ad + "_kaynagi"] = f"komut ({kaynak})" if ad in f else f"varsayilan ({c[ad]['kaynak']})"
        st_, st_k = deger("steps", int)
        o["pgd_adim"], o["pgd_adim_kaynagi"] = st_, st_k
        gc, gc_k = deger("grad_clip")
        o["gradyan_kirpma"], o["gradyan_kirpma_kaynagi"] = gc, gc_k
        o["kaydet_her"] = int(f["save_every"]) if "save_every" in f else int(c["save_every"]["ifade"])
    return o


C1_KOMIT = "77ae259"
C1_ZAMAN = "TIMING.md"
C1_YENI_SECENEKLER = ("--optimizer", "--lr-schedule", "--init-weights", "--grad-clip", "--stop-epoch", "--save-every",
                      "--vit-lr-cap", "--lr-warmup")


def kosu_ani_kodu(hucreler, ortak, siniflar_bugun):
    """31.10.2026 bulgu 6. C1 hucrelerinin (V-scr, C1-R32) tarif degerleri bugunku kod satirlarindan okunmustur; kosular
    77ae259'daki kodla yapilmistir. Bu islev ayni degerleri 'git show 77ae259:<yol>' metninden yeniden okur, bugunku
    tarifle karsilastirir ve kosu aninin 77ae259 oldugunun dayanaklarini yazar (salt okur git)."""
    import datetime as dt
    import os
    c = C1_KOMIT

    def G(rel):
        return f"git:{c}:{rel}"

    tam = O.git("rev-parse", c).strip()
    c_utc_s, c_baslik = O.git("log", "-1", "--format=%cI%n%s", c).strip().split("\n", 1)
    c_utc = dt.datetime.fromisoformat(c_utc_s).astimezone(dt.timezone.utc)
    izlenen = [CLI, TR, ATR, ATD, DS, RC1, *MODELLER]
    sonraki = O.git("log", "--reverse", "--format=%h %cI", f"{c}..HEAD", "--", *izlenen).strip().split("\n")[0]
    s_h, s_t = sonraki.split(" ", 1)
    s_utc = dt.datetime.fromisoformat(s_t).astimezone(dt.timezone.utc)
    rc1_son = O.git("log", "-1", "--format=%h", "--", RC1).strip()
    c_dosyalari = O.git("show", "--name-only", "--format=", c).split()
    # TIMING.md (run_c1_pipeline.sh'in yazdigi adim sureleri); saat dilimi gunluk mtime'iyla denetlenir
    adim = {}
    for n, s in enumerate(O.satirlar(C1_ZAMAN), 1):
        m = re.match(r"\| (C1_(clean|at)_(resnet|vit)_(\d+)) \| (\d+)s \| ([0-9-]+ [0-9:]+) \|", s)
        if m:
            bit = dt.datetime.fromisoformat(m.group(6)).replace(tzinfo=dt.timezone.utc)
            adim[m.group(1)] = {"sure_s": int(m.group(5)), "bitis_utc": bit, "kaynak": k(C1_ZAMAN, n)}
    farklar = []
    for ad_, x in adim.items():
        p = O.KOK / "logs" / f"{ad_}.log"
        if p.exists():
            farklar.append(abs((dt.datetime.fromtimestamp(os.stat(p).st_mtime, dt.timezone.utc) - x["bitis_utc"]).total_seconds()))
    ilk = min(adim.values(), key=lambda x: x["bitis_utc"] - dt.timedelta(seconds=x["sure_s"]))
    ilk_bas = ilk["bitis_utc"] - dt.timedelta(seconds=ilk["sure_s"])
    son = max(adim.values(), key=lambda x: x["bitis_utc"])
    val_once = any('"--val-indices"' in s for s in O.satirlar(f"git:{c}^:{CLI}"))
    val_simdi = any('"--val-indices"' in s for s in O.satirlar(G(CLI)))
    dayanak = {
        "commit": tam, "commit_utc": c_utc.isoformat(), "commit_basligi": c_baslik,
        "run_c1_pipeline_son_degistiren_commit": rc1_son,
        "commit_ile_degisen_dosyalar": c_dosyalari,
        "egitim_dosyalari_commitle_degismedi": not any(x in c_dosyalari for x in (TR, ATR, ATD, *MODELLER)),
        "val_indices_secenegi": {"77ae259_oncesi": val_once, "77ae259": val_simdi,
                                 "not": "C1 komutlari --val-indices tasir; secenek cli/train.py'ye bu commit'le eklenmistir"},
        "zaman_kaynagi": C1_ZAMAN, "zaman_kaynagi_utc_denetimi_en_buyuk_fark_s": max(farklar) if farklar else None,
        "zaman_kaynagi_utc_denetimi": f"{len(farklar)} adimda TIMING.md bitis saati (UTC kabul) ile gunluk mtime'i karsilastirildi",
        "ilk_C1_egitim_adimi_baslangic_utc": ilk_bas.isoformat(), "ilk_adim_kaynagi": ilk["kaynak"],
        "ilk_adim_baslangici_commit_eksi_s": round((ilk_bas - c_utc).total_seconds()),
        "son_C1_egitim_adimi_bitis_utc": son["bitis_utc"].isoformat(), "son_adim_kaynagi": son["kaynak"],
        "izlenen_dosyalari_sonra_degistiren_ilk_commit": {"commit": s_h, "utc": s_utc.isoformat()},
        "son_egitim_adimi_sonraki_committen_once": son["bitis_utc"] < s_utc,
        "izlenen_dosyalar": izlenen,
        "not": ("Ilk C1 egitim adimi commit zamanindan ilk_adim_baslangici_commit_eksi_s saniye farkla, yani commit'ten "
                "hemen once baslamistir (commit mesaji kosularin kuyruga alindigini yazar); --val-indices secenegi bu commit'le geldiginden ve egitim dosyalari (trainer, "
                "adversarial_trainer, savunma, modeller) bu commit'te degismediginden kosu anindaki kod 77ae259 icerigidir. "
                "Son C1 egitim adimi izlenen dosyalari degistiren bir sonraki commit'ten once bitmistir.")}

    def kod(rel):
        L = O.satirlar(G(rel))
        r = {"model_adi": O.kanit(G(rel), "model_name = model.__class__.__name__.lower()"),
             "is_vit": O.kanit(G(rel), "is_vit = 'vit' in model_name"),
             "vit_lr_tavani": O.kanit(G(rel), "effective_lr = min(lr, ", r"min\(lr, ([0-9.e-]+)\)"),
             "adamw_wd": O.kanit(G(rel), "weight_decay=0.05,", r"weight_decay=([0-9.]+)", sira=0),
             "adamw_yazdir": O.kanit(G(rel), 'print(f"Using AdamW optimizer for ViT'),
             "sgd": O.kanit(G(rel), "self.optimizer = optim.SGD("),
             "sgd_momentum": O.kanit(G(rel), "momentum: float = ", r"= ([0-9.]+)"),
             "sgd_wd": O.kanit(G(rel), "weight_decay: float = ", r"= ([0-9.e-]+)"),
             "cosine": O.kanit(G(rel), "T_max=epochs,")}
        b = O.bul(G(rel), "self.scheduler = scheduler or")
        r["sgd_dalinda_yazdirma_yok"] = not any("print(" in L[i - 1] for i in range(r["sgd"]["satir"], b))
        r["sgd_dali_araligi"] = f"{G(rel)}:{r['sgd']['satir']}-{b - 1}"
        return r

    kt, ka = kod(TR), kod(ATR)
    kc = {"gradyan_kirpma": O.kanit(G(ATR), "clip_grad_norm_(self.model.parameters(), max_norm=", r"max_norm=([0-9.]+)"),
          "min_delta": O.kanit(G(ATR), "min_delta: float = ", r"= ([0-9.]+)"),
          "mix_ratio": O.kanit(G(ATD), "mix_ratio: float = ", r"= ([0-9.]+)"),
          "random_start": O.kanit(G(ATD), "random_start: bool = ", r"= (\w+)", tip=lambda x: x == "True"),
          "eps": O.kanit(G(CLI), '@click.option("--eps"', r"default=([0-9./]+)", tip=O.kesir),
          "alpha": O.kanit(G(CLI), '@click.option("--alpha"', r"default=([0-9./]+)", tip=O.kesir),
          "steps": O.kanit(G(CLI), '@click.option("--steps"', r"default=([0-9]+)", tip=int)}
    cli77 = O.satirlar(G(CLI))
    yok = [x for x in C1_YENI_SECENEKLER if not any(f'"{x}"' in s for s in cli77)]
    sinif77 = {}
    for rel in MODELLER:
        try:
            L = O.satirlar(G(rel))
        except SystemExit:
            continue
        for n, s in enumerate(L, 1):
            m = re.match(r'@register_model\("([^"]+)"\)', s)
            cm = re.match(r"class (\w+)\(", L[n]) if m and n < len(L) else None
            if cm:
                sinif77[m.group(1)] = {"sinif": cm.group(1), "kaynak": f"{G(rel)}:{n + 1}"}

    def kk_(o):
        return f"{o['dosya']}:{o['satir']}"

    out = {}
    for h in ("V-scr", "C1-R32"):
        satirlar_ = []
        gozlem = {}
        for a, o in hucreler[h]["kosular"]["sablon"].items():
            K_ = kt if a == "temiz" else ka
            s77 = sinif77[o["model_anahtari"]]
            v77 = vit_mi(s77["sinif"])

            def ekle(ad, kosu, kaynak, bugun, bkaynak, ayni=None):
                satirlar_.append({"asama": a, "ad": ad, "kosu_ani": kosu, "kosu_ani_kaynagi": kaynak, "bugunku_tarif": bugun,
                                  "bugunku_kaynak": bkaynak, "ayni": (kosu == bugun) if ayni is None else ayni})
            ekle("model_sinifi", s77["sinif"], s77["kaynak"], o["model_sinifi"], o["model_sinifi_kaynagi"])
            ekle("eniyileyici", "AdamW" if v77 else "SGD", f"{kk_(K_['model_adi'])}; {kk_(K_['is_vit'])}",
                 o["eniyileyici_eniyileyici"], o["eniyileyici_kaynak"])
            if v77:
                ekle("lr_etkin", min(o["lr_bayragi"], K_["vit_lr_tavani"]["deger"]), kk_(K_["vit_lr_tavani"]),
                     o["eniyileyici_lr_etkin"], o["eniyileyici_kaynak"])
                ekle("agirlik_azaltma", K_["adamw_wd"]["deger"], kk_(K_["adamw_wd"]), o["eniyileyici_agirlik_azaltma"],
                     o["eniyileyici_kaynak"])
            else:
                ekle("lr_etkin", o["lr_bayragi"], f"komut ({o['komut_kaynagi']}); {kk_(K_['sgd'])}", o["eniyileyici_lr_etkin"],
                     o["eniyileyici_kaynak"])
                ekle("momentum", K_["sgd_momentum"]["deger"], kk_(K_["sgd_momentum"]), o.get("eniyileyici_momentum"),
                     o["eniyileyici_kaynak"])
                ekle("agirlik_azaltma", K_["sgd_wd"]["deger"], kk_(K_["sgd_wd"]), o["eniyileyici_agirlik_azaltma"],
                     o["eniyileyici_kaynak"])
            ekle("lr_cizelgesi", f"cosine, T_max = -e ({o['epok_bayragi']})", kk_(K_["cosine"]),
                 f"{o['lr_cizelgesi']['tur']}, T_max {o['lr_cizelgesi']['T_max_epok']}", o["lr_cizelgesi"]["kaynak"],
                 ayni=o["lr_cizelgesi"]["tur"] == "cosine" and o["lr_cizelgesi"]["T_max_epok"] == o["epok_bayragi"])
            if a == "temiz":
                ekle("baslatma", "rastgele (--init-weights secenegi yok)", f"{G(CLI)} (secenek listesi)",
                     o["baslatma_bayragi"], o["baslatma_kaynagi"],
                     ayni="--init-weights" in yok and o["baslatma_bayragi"] == "none")
            else:
                ekle("epok_tavani", f"-e ({o['epok_bayragi']}); --stop-epoch secenegi yok", f"{G(CLI)} (secenek listesi)",
                     o["epok_tavani"], o["epok_tavani_kaynagi"],
                     ayni="--stop-epoch" in yok and o["epok_tavani"] == o["epok_bayragi"])
                for ad in ("eps", "alpha"):
                    ekle(ad, kc[ad]["deger"], kk_(kc[ad]), o[ad], o[ad + "_kaynagi"])
                ekle("pgd_adim", kc["steps"]["deger"], kk_(kc["steps"]), o["pgd_adim"], o["pgd_adim_kaynagi"])
                ekle("gradyan_kirpma", kc["gradyan_kirpma"]["deger"], kk_(kc["gradyan_kirpma"]) + " (sabit kod)",
                     o["gradyan_kirpma"], o["gradyan_kirpma_kaynagi"])
                ekle("mix_ratio", kc["mix_ratio"]["deger"], kk_(kc["mix_ratio"]), ortak["at_kaybi"]["mix_ratio"], "ortak.at_kaybi")
                ekle("pgd_rastgele_baslangic", kc["random_start"]["deger"], kk_(kc["random_start"]),
                     ortak["at_kaybi"]["pgd_rastgele_baslangic"], "ortak.at_kaybi")
                ekle("erken_durma_min_delta", kc["min_delta"]["deger"], kk_(kc["min_delta"]),
                     ortak["erken_durma"]["min_delta_puan"], "ortak.erken_durma")
            gl = o.get("gunlukler", {})
            var = {t: (g.get("eniyileyici_satiri") or {}).get("kaynak") for t, g in gl.items()}
            if all(var.values()):
                gozlem[a] = {"durum": "gunlukte gozlendi", "gunluk_satirlari": var}
            else:
                gozlem[a] = {"durum": "gunlukte eniyileyici satiri yok; eniyileyici koddan cikarilmistir",
                             "gunluk_satirlari": var,
                             "kod": (f"{K_['sgd_dali_araligi']} (SGD dali; yazdirma yok: {K_['sgd_dalinda_yazdirma_yok']}); "
                                     f"momentum {kk_(K_['sgd_momentum'])}; agirlik azaltma {kk_(K_['sgd_wd'])}"),
                             "not": ("SGD, momentum ve agirlik azaltma bu hucrede gunlukten okunmamis, kosu anindaki kodun "
                                     "(77ae259) eniyileyici kuralindan cikarilmistir; gunlukteki 'Epochs/LR' satiri ve "
                                     "AdamW satirinin yoklugu bu cikarimla tutarlidir.")}
        out[h] = {"commit": tam, "commit_kisa": c, "dayanak": dayanak, "karsilastirma": satirlar_,
                  "hepsi_ayni": all(x["ayni"] for x in satirlar_),
                  "kosu_aninda_olmayan_cli_secenekleri": yok,
                  "eniyileyici_gozlemi": gozlem,
                  "not": ("Bu hucrenin kosular.sablon.* alanlarindaki 'varsayilan (...)' kaynaklari bugunku kod satirlarini "
                          "gosterir. Kosu anindaki kod 77ae259'dur; bugun var olan secenekler listesi "
                          "(kosu_aninda_olmayan_cli_secenekleri) o surumde yoktu ve davranis sabit kodla belirleniyordu. "
                          "'karsilastirma' her degeri 77ae259 metninden yeniden okur ve bugunku tarifle karsilastirir.")}
    return out


def main():
    global B3_TAKMA
    cli = cli_varsayilanlari()
    siniflar = model_siniflari()
    zk = zincir_komutlari()
    B3_TAKMA = tuple(dict.fromkeys(t for (t, a) in sorted(zk, key=lambda x: int(zk[x]["kaynak"].rsplit(":", 1)[1]))))
    img = int(re.search(r'"img_size": (\d+)', KAN["cifar10_spec"]["metin"]).group(1))
    upv = int(re.search(r"size=\((\d+), \d+\)", KAN["vit_upsample"]["metin"]).group(1))
    upr = KAN["r224_buyutme"]["deger"]
    if upv != upr:
        raise SystemExit(f"ViT ve R224 buyutme boyutu farkli: {upv} {upr}")
    hat = f"{img}->{upv} bilinear buyutme"
    ht = O.jyukle(HT)
    pz = O.jyukle(PZ)
    vi = O.jyukle(VAL)
    tohum = {}
    for m, x in ht["modeller"].items():
        tohum.setdefault(x.get("hucre"), []).append(x.get("tohum"))

    hucreler = {}
    # --- B3: alti kosu, gercek komutlar zincir gunlugunden; sablonla bayrak bayrak karsilastirma
    for h, okn in (("V-IN", "ok_vin"), ("R224-scr", "ok_rscr"), ("R224-IN", "ok_rin")):
        hk = h.replace("-", "_")
        takmalar = [t for t in B3_TAKMA if t.startswith(hk + "_s")]
        kosular = {}
        for t in takmalar:
            kosu = {}
            for a in ("temiz", "AT"):
                z = zk[(t, a)]
                kosu[a] = asama_ozeti("temiz" if a == "temiz" else "at", z["komut"], z["kaynak"], cli, siniflar)
                sab, sn = kuyruk_sablonu(hk, "temiz" if a == "temiz" else "at")
                g = bayraklar(z["komut"])[1]
                s = bayraklar(sab.replace("$(at_lr \"$t\")", g.get("lr", "")).replace("$cap", g.get("stop_epoch", ""))
                              .replace("$VAL", g.get("val_indices", "")).replace("$t", t).replace("$m", g["model"])
                              .replace("$s", g["seed"]))[1]
                s.pop("resume", None)
                g.pop("resume", None)
                kosu[a]["kuyruk_sablonu"] = k(KUY, sn)
                kosu[a]["sablonla_ayni_bayraklar"] = s == g
                if s != g:
                    kosu[a]["sablon_farki"] = {x: (s.get(x), g.get(x)) for x in set(s) | set(g) if s.get(x) != g.get(x)}
                log = f"logs/konsey_b3/{t}_{'temiz' if a == 'temiz' else 'AT'}.log"
                kosu[a]["gunluk"] = gunluk_basligi(log)
            kosular[t] = kosu
        # hucre ozeti: iki kosuda tohum disinda ayni olmali
        ilk = kosular[takmalar[0]]

        def _deger(o):
            if isinstance(o, dict):
                return {x: _deger(y) for x, y in o.items()
                        if "kaynag" not in x and "kaynak" not in x and x not in ("komut", "tohum", "gunluk")}
            return o

        ayni = all(_deger(kosular[t][a]) == _deger(ilk[a]) for t in takmalar for a in ("temiz", "AT"))
        if not ayni:
            for t in takmalar:
                for a in ("temiz", "AT"):
                    x_, y_ = _deger(kosular[t][a]), _deger(ilk[a])
                    if x_ != y_:
                        print("FARK", t, a, {z: (x_.get(z), y_.get(z)) for z in set(x_) | set(y_) if x_.get(z) != y_.get(z)})
        hucreler[h] = {"blok": "B3 (yeni)", "on_kayit_satiri": k(OK, KAN[okn]["satir"]),
                       "on_kayit_metni": KAN[okn]["metin"], "tohumlar": [int(kosular[t]["temiz"]["tohum"]) for t in takmalar],
                       "takma_adlar": takmalar, "kosular_tohum_disinda_ozdes": ayni, "kosular": kosular}
    # --- C1: V-scr ve C1-R32 (run_c1_pipeline.sh; tohumlar hucre tablosundan)
    for h, md, okn in (("V-scr", "vit_tiny", "ok_vscr"), ("C1-R32", "resnet18", None)):
        kosu = {}
        for a, desen in (("temiz", f"train clean -m {md} "), ("AT", f"train adversarial -m {md} ")):
            cmd, n1, n2 = c1_komutu(desen)
            ornek_tohum = sorted(tohum[h])[0]
            cmd_t = re.sub(r'"?\$(RSEED|VSEED)"?', str(ornek_tohum), cmd).replace("${RSEED}", str(ornek_tohum)) \
                .replace("${VSEED}", str(ornek_tohum))
            kosu[a] = asama_ozeti("temiz" if a == "temiz" else "at", cmd_t, f"{RC1}:{n1}-{n2}", cli, siniflar)
            kosu[a]["komut_sablonu"] = cmd
            kosu[a]["tohum"] = None
            kosu[a]["tohum_notu"] = f"sablonda $RSEED/$VSEED; tohumlar hucre tablosundan ({HT} modeller.<m>.tohum)"
            gl = {}
            for t in sorted(tohum[h]):
                ad = ("C1_clean_" if a == "temiz" else "C1_at_") + ("vit" if md == "vit_tiny" else "resnet") + f"_{t}.log"
                gl[str(t)] = gunluk_basligi("logs/" + ad)
            kosu[a]["gunlukler"] = gl
        hucreler[h] = {"blok": "C1 (mevcut)" + (", kopru (S1, B2)" if h == "C1-R32" else ""),
                       "on_kayit_satiri": k(OK, KAN[okn]["satir"]) if okn else None,
                       "on_kayit_metni": KAN[okn]["metin"] if okn else None,
                       "hucre_tablosu_tanimi": ht["hucreler"][h], "tohumlar": sorted(tohum[h]), "kosular": {"sablon": kosu}}
    # girdi hatti ve baslatma (kod kanitlari)
    girdi = {
        "V-scr": {"model": "timm vit_tiny_patch16_224", "girdi": hat, "normalizasyon": "yok",
                  "baslatma": "rastgele",
                  "kaynak": [k("src/models/vit.py", KAN["vit_timm"]["satir"]), k("src/models/vit.py", KAN["vit_upsample"]["satir"]),
                             k(OK, KAN["ok_vscr"]["satir"])]},
        "V-IN": {"model": "timm vit_tiny_patch16_224", "girdi": hat,
                 "normalizasyon": "model ici ImageNet (pretrained_cfg)", "baslatma": "deit_tiny_patch16_224.fb_in1k",
                 "kaynak": [k("src/models/r224.py", KAN["r224_resize_norm"]["satir"]), k("src/models/r224.py", KAN["init_deit"]["satir"]),
                            k(OK, KAN["ok_vin"]["satir"])]},
        "R224-scr": {"model": "timm resnet18", "girdi": hat, "normalizasyon": "yok", "baslatma": "rastgele",
                     "kaynak": [k("src/models/r224.py", KAN["r224_timm"]["satir"]), k(OK, KAN["ok_rscr"]["satir"])]},
        "R224-IN": {"model": "timm resnet18", "girdi": hat,
                    "normalizasyon": "model ici ImageNet (pretrained_cfg)", "baslatma": "resnet18.a1_in1k",
                    "kaynak": [k("src/models/r224.py", KAN["init_r18a1"]["satir"]), k(OK, KAN["ok_rin"]["satir"])]},
        "C1-R32": {"model": "CIFAR ResNet-18 (3x3 kok, maxpool yok)", "girdi": f"{img}x{img} (buyutme yok)",
                   "normalizasyon": "yok (resnet.py'de normalizasyon ve buyutme satiri sayisi "
                                    f"{KAN['resnet32_normalizasyon_yok']['eslesen_satir_sayisi']})",
                   "baslatma": "rastgele", "kaynak": [k("src/models/resnet.py", KAN["resnet32_kok"]["satir"]), HT + " hucreler.C1-R32"]},
    }
    for h in girdi:
        hucreler[h]["girdi_hatti"] = girdi[h]
    # IN normalizasyon degerleri: temiz gunlugunun INIT_WEIGHTS_RAPORU satiri
    for h, t in (("V-IN", "V_IN_s2101"), ("R224-IN", "R224_IN_s1301")):
        ini = hucreler[h]["kosular"][t]["temiz"]["gunluk"].get("init", {})
        hucreler[h]["girdi_hatti"]["imagenet_ortalama"] = ini.get("pretrained_cfg_mean")
        hucreler[h]["girdi_hatti"]["imagenet_sd"] = ini.get("pretrained_cfg_std")
        hucreler[h]["girdi_hatti"]["norm_cfg_ile_ayni"] = ini.get("norm_matches_cfg")
        hucreler[h]["girdi_hatti"]["agirlik_dosyasi_sha256"] = ini.get("source_sha256")
        hucreler[h]["girdi_hatti"]["yuklenen_anahtar"] = f"{ini.get('n_loaded')}/{ini.get('n_target_keys')}"
        hucreler[h]["girdi_hatti"]["init_kaynak"] = ini.get("kaynak")

    vn = len(vi["val_indices"])
    ortak = {
        "veri": {"egitim_kumesi": "cifar10", "dogrulama_bolmesi_dosyasi": VAL, "dogrulama_n": vn,
                 "dogrulama_n_kaynagi": f"{VAL} len(val_indices); val_size alani {vi.get('val_size')}",
                 "artirma": f"RandomCrop(32, padding={KAN['artirma_crop']['deger']}) + RandomHorizontalFlip + ToTensor",
                 "artirma_kaynagi": f"{k(DS, KAN['artirma_crop']['satir'])}; {k(DS, KAN['artirma_flip']['satir'])}; "
                                    f"{k(DS, KAN['cifar10_spec']['satir'])}"},
        "at_kaybi": {"tur": "karisik kayip: (1 - mix_ratio) * CE(temiz) + mix_ratio * CE(PGD)",
                     "mix_ratio": KAN["mix_ratio"]["deger"], "pgd_rastgele_baslangic": KAN["random_start"]["deger"],
                     "kaynak": f"{k(ATD, KAN['karisik_kayip']['satir'])}; {k(ATD, KAN['mix_ratio']['satir'])}; "
                               f"{k(ATD, KAN['random_start']['satir'])}; savunma kurulumu bu iki degeri gecmez "
                               f"({k(ATR, KAN['at_savunma_kurulumu']['satir'])})"},
        "erken_durma": {"olcut": "dogrulama PGD dogrulugu en iyi + min_delta (puan)", "min_delta_puan": KAN["at_min_delta"]["deger"],
                        "kaynak": f"{k(ATR, KAN['at_min_delta']['satir'])}; {k(ATR, KAN['at_min_delta_kullanim']['satir'])}"},
        "secim_kurali": {"metin": KAN["ok_yakinsama"]["metin"], "kaynak": k(OK, KAN["ok_yakinsama"]["satir"])},
        "at_tavani_pilot": {"secilen_tavan": pz["secilen_tavan"], "kaynak": f"{PZ} secilen_tavan",
                            "on_kayit": k(OK, KAN["ok_at"]["satir"])},
        "on_kayit_at_tarifi": {"metin_basi": KAN["ok_at"]["metin"][:200], "kaynak": k(OK, KAN["ok_at"]["satir"])},
    }
    # Denetimler
    den = {}
    b3_tavan = {hucreler[h]["kosular"][t]["AT"]["epok_tavani"] for h in ("V-IN", "R224-scr", "R224-IN")
                for t in hucreler[h]["takma_adlar"]}
    den["B3_AT_tavani_pilotla_ayni"] = b3_tavan == {pz["secilen_tavan"]}
    den["B3_komutlar_kuyruk_sablonuyla_ayni"] = all(hucreler[h]["kosular"][t][a]["sablonla_ayni_bayraklar"]
                                                   for h in ("V-IN", "R224-scr", "R224-IN") for t in hucreler[h]["takma_adlar"]
                                                   for a in ("temiz", "AT"))
    den["B3_hucre_ici_kosular_tohum_disinda_ozdes"] = all(hucreler[h]["kosular_tohum_disinda_ozdes"] for h in ("V-IN", "R224-scr", "R224-IN"))
    # gunluk basliklari ile cozumlenen deger (Epochs, LR) uyusuyor mu
    uy = []
    for h in hucreler:
        for t, kosu in hucreler[h]["kosular"].items():
            for a, o in kosu.items():
                gl = o.get("gunlukler") or {"-": o.get("gunluk", {})}
                for tt, g in gl.items():
                    s = (g.get("epochs_satiri") or {}).get("metin", "")
                    m = re.search(r"Epochs: (\d+), LR: ([0-9.e-]+)", s)
                    if m:
                        uy.append(int(m.group(1)) == o["epok_bayragi"] and float(m.group(2)) == o["lr_bayragi"])
                    e = (g.get("eniyileyici_satiri") or {}).get("metin", "")
                    if e:
                        uy.append(("AdamW" in e) == (o["eniyileyici_eniyileyici"] == "AdamW"))
    den["gunluk_basliklari_cozumlenen_degerlerle_ayni"] = {"denetlenen": len(uy), "uyusan": sum(uy)}
    den["AT_eps_alpha_adim_hucreler_arasi_ayni"] = len({(o["eps"], o["alpha"], o["pgd_adim"]) for h in hucreler
                                                         for kosu in hucreler[h]["kosular"].values() for a, o in kosu.items()
                                                         if a == "AT"}) == 1

    # Gerceklesen epoklar: foy satir referanslari (tekrar edilmez)
    foy = {"foy_sha256": O.sha(O.FOY),
           "B3_gerceklesen_epoklar": {t: {x: y for x, y in O.foy_tablo_hucresi("### M9.1", f"| {t} |", "AT epok (kosulan)",
                                                                                 sira=0).items() if x != "deger"}
                                     for t in B3_TAKMA},
           "B3_tablo_basligi": O.foy_satiri("### M9.1", "| Takma ad | Hucre | Tohum | Temiz epok | AT epok (kosulan)"),
           "C1_son_kontrol_noktasi_epoklari_bolumu": O.foy_satiri("### M8.14", "### M8.14"),
           "B3_toplam_egitim_suresi": O.foy_satiri("### M9.1", "Defterdeki temiz ve AT asama surelerinin toplami"),
           "not": "deger alanlari bilerek bos; sayilar foyun gosterilen satirlarindadir"}

    # 31.10.2026 bulgu 6: C1 hucreleri (V-scr, C1-R32) icin kosu anindaki kod surumu ve bugunku tarifle karsilastirma
    kak = kosu_ani_kodu(hucreler, ortak, siniflar)
    for h in ("V-scr", "C1-R32"):
        hucreler[h]["kosu_ani_kodu"] = kak[h]
    den["C1_kosu_ani_kodu_bugunku_tarifle_ayni"] = all(kak[h]["hepsi_ayni"] for h in ("V-scr", "C1-R32"))

    # 31.10.2026 bulgu 7: AT tavani cumlesi tam alinti; V-scr tavani 100 ve gerceklesen durma epoklari B3 tavaninin altinda
    n_at = KAN["ok_at"]["satir"]
    m_ = re.search(r"(AT tavanı \d+ epoktur ve [^.]*\.)", O.satirlar(OK)[n_at - 1])
    if not m_:
        raise SystemExit(f"{OK}:{n_at}: AT tavani cumlesi bulunamadi")
    satir_h = {"V-scr": "ok_vscr", "V-IN": "ok_vin", "R224-scr": "ok_rscr", "R224-IN": "ok_rin"}
    ortak["at_tavani_on_kayit_cumlesi"] = {
        "alinti": m_.group(1), "kaynak": k(OK, n_at),
        "on_kayit_tablosunda_mevcut_isaretli_hucreler": [h for h, x in satir_h.items() if "mevcut" in KAN[x]["metin"]],
        "on_kayit_tablosunda_yeni_hucreler": [h for h, x in satir_h.items() if "mevcut" not in KAN[x]["metin"]],
        "tablo_satirlari": {h: k(OK, KAN[x]["satir"]) for h, x in satir_h.items()},
        "not": ("Cumle aynen alintilanmistir. On kayit hucre tablosunda V-scr satiri 'mevcut C1' olarak isaretlidir; 80 "
                "tavani B3'te kosulan hucrelere (yukaridaki 'yeni' listesi, alti kosu) uygulanmistir "
                "(denetimler.B3_AT_tavani_pilotla_ayni). V-scr AT'si C1 tarifiyle (-e 100, --stop-epoch yok) kosulmustur; "
                "bkz. denetimler.V_scr_AT_tavani_ve_gerceklesen_durma.")}
    vs = hucreler["V-scr"]["kosular"]["sablon"]["AT"]
    durma = {str(t): O.foy_tablo_hucresi("### M8.14", f"| ViT-Tiny AT | {t} |", "Durma epogu")
             for t in sorted(hucreler["V-scr"]["tohumlar"])}
    den["V_scr_AT_tavani_ve_gerceklesen_durma"] = {
        "V_scr_AT_tavani": vs["epok_tavani"], "V_scr_AT_tavani_kaynagi": vs["epok_tavani_kaynagi"],
        "V_scr_lr_cizelgesi_T_max": vs["lr_cizelgesi"]["T_max_epok"],
        "B3_AT_tavani": pz["secilen_tavan"], "B3_AT_tavani_kaynagi": f"{PZ} secilen_tavan",
        "gerceklesen_durma_epoklari_B3_tavaninin_altinda": all(int(x["deger"]) < pz["secilen_tavan"] for x in durma.values()),
        "foy_bolum": "M8.14", "foy_sutun": "Durma epogu",
        "foy_satirlari": {t: x["foy_satiri"] for t, x in durma.items()},
        "foy_satir_metni_sha256": {t: x["satir_metni_sha256"] for t, x in durma.items()},
        "not": ("Durma epoklari bu dosyaya kopyalanmaz (foy M8.14 satirlari). V-scr'nin AT tavani B3 tavanindan buyuktur, "
                "ancak uc tohumun her biri erken durmayla B3 tavanindan once durmustur; kosinus cizelgesi her iki tarifte "
                "T_max = 100 oldugundan B3 tavani V-scr kosularinin hicbirinde baglayici olmazdi.")}
    foy["C1_V_scr_durma_epoklari"] = {t: {"foy_satiri": x["foy_satiri"], "satir_metni_sha256": x["satir_metni_sha256"]}
                                      for t, x in durma.items()}
    govde = {"ortak": ortak, "hucreler": hucreler, "denetimler": den, "foy_referanslari": foy,
             "kanitlar": KAN}
    O.yaz(CIKTI, govde, __file__, "Y1 fig:design_recipe kaynagi: 2x2 tasarim ve egitim tarifi (B3 ve C1)",
          "Her hucre icin baslatma, girdi hatti, normalizasyon, temiz asama ve AT asamasi; degerler gercek komut "
          "satirlarindan ve kod varsayilanlarindan, kaynak satirlariyla. Gerceklesen epoklar foy M9.1/M8.14'te.")


if __name__ == "__main__":
    main()
