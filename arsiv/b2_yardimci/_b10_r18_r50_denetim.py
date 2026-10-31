# -*- coding: utf-8 -*-
"""B10 ImageNetV2 R18-R50 kosinus denetimi (31.10.2026). Salt okur: results/q1 altina yazmaz.

Zincirdeki yolu aynen kullanir: experiments/q1_ek_gradyan_kosinus.py modulunu import eder, onun _modul
yukleyicisiyle q1_ek_transfer_matrix'i alir; set_seed(42) -> load_wrn(imagenetv2) -> v2_loaders(data/imagenetv2,
2000, 25, BicubicRes256Crop224, 10) -> _iter_batches -> girdi_gradyani -> cift_kosinus. Ilk 100 goruntu.
Cikti: arsiv/b2_yardimci/_b10_denetim_cikti/denetim.json
"""
import hashlib
import importlib.util
import json
import os
import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

KOK = Path("/workspace")
OUT = KOK / "arsiv/b2_yardimci/_b10_denetim_cikti"
OUT.mkdir(parents=True, exist_ok=True)
KAYIT = KOK / "results/q1/konsey_b10_gradyan/imagenetv2"
N = 100

spec = importlib.util.spec_from_file_location("q1_ek_gradyan_kosinus", KOK / "experiments/q1_ek_gradyan_kosinus.py")
b10 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b10)
tm = b10._modul("q1_ek_transfer_matrix", "q1_ek_transfer_matrix.py")

RB = [("Salman2020Do_R18", "IN_Salman2020Do_R18"), ("Salman2020Do_R50", "IN_Salman2020Do_R50"),
      ("Salman2020Do_50_2", "IN_Salman2020Do_50_2"), ("Engstrom2019Robustness", "IN_Engstrom2019Robustness"),
      ("Singh2023Revisiting_ConvNeXt-T-ConvStem", "IN_Singh_ConvNeXt-T-CvSt"),
      ("Singh2023Revisiting_ConvNeXt-B-ConvStem", "IN_Singh_ConvNeXt-B-CvSt")]
CIFTLER = [("IN_Salman2020Do_R18", "IN_Salman2020Do_R50"), ("IN_Salman2020Do_R18", "IN_Salman2020Do_50_2"),
           ("IN_Salman2020Do_R50", "IN_Engstrom2019Robustness"), ("IN_Singh_ConvNeXt-T-CvSt", "IN_Singh_ConvNeXt-B-CvSt")]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def r(v, k=5):
    return None if v is None else round(float(v), k)


rapor = {"betik": "arsiv/b2_yardimci/_b10_r18_r50_denetim.py", "n": N}
ozet = json.loads((KAYIT / "kosinus_ozet.json").read_text())
rapor["b10_betik_sha256_simdi"] = sha256(KOK / "experiments/q1_ek_gradyan_kosinus.py")
rapor["b10_betik_sha256_kayit"] = ozet["betik_sha256"]
rapor["b10_betik_ayni"] = rapor["b10_betik_sha256_simdi"] == ozet["betik_sha256"]

# ---------------- yukleme (zincirle ayni sira: seed, modeller, veri) ----------------
t0 = time.time()
tm.set_seed(42)
device = torch.device("cuda")
torch.cuda.synchronize()
models, yukleme = {}, {}
for rb, alias in RB:
    ck = KOK / "models/robustbench_zoo/imagenet/Linf" / f"{rb}.pt"
    var_once = ck.exists()
    mt_once = os.stat(ck).st_mtime if var_once else None
    t = time.time()
    m = tm.load_wrn(device, dataset="imagenetv2", rb_name=rb).eval()
    for p in m.parameters():
        p.requires_grad_(False)
    models[alias] = m
    yukleme[alias] = {"rb_ad": rb, "ckpt": str(ck), "ckpt_gercek": os.path.realpath(ck),
                      "ckpt_vardi": var_once, "mtime_degismedi": (os.stat(ck).st_mtime == mt_once) if var_once else None,
                      "ckpt_bayt": os.path.getsize(ck), "yukleme_s": round(time.time() - t, 2)}
print("modeller yuklendi", round(time.time() - t0, 1), "s", flush=True)

# model kimligi
kimlik = {}
for alias in ["IN_Salman2020Do_R18", "IN_Salman2020Do_R50"]:
    m = models[alias]
    inner = m.model if hasattr(m, "model") else m
    conv1 = inner.conv1.weight.detach().float()
    norm_buf = {k: v.flatten().tolist() for k, v in m.named_buffers() if k.split(".")[-1] in ("mean", "std")}
    kimlik[alias] = {"id": id(m), "sinif": type(m).__name__, "ic_sinif": type(inner).__name__,
                     "parametre_sayisi": int(sum(p.numel() for p in m.parameters())),
                     "katman_sayisi_layer1": len(inner.layer1), "fc_girdi": inner.fc.in_features,
                     "conv1_sekil": list(conv1.shape), "conv1_toplam": r(conv1.sum(), 6),
                     "conv1_norm": r(conv1.norm(), 6), "conv1_ilk5": [r(v, 6) for v in conv1.flatten()[:5].tolist()],
                     "normalizasyon_tamponlari": norm_buf, "ilk_param_ptr": m.parameters().__next__().data_ptr()}
p18 = {p.data_ptr() for p in models["IN_Salman2020Do_R18"].parameters()}
p50 = {p.data_ptr() for p in models["IN_Salman2020Do_R50"].parameters()}
kimlik["ortak_parametre_tensoru"] = len(p18 & p50)
kimlik["id_farkli"] = kimlik["IN_Salman2020Do_R18"]["id"] != kimlik["IN_Salman2020Do_R50"]["id"]
for alias in ["IN_Salman2020Do_R18", "IN_Salman2020Do_R50"]:
    yukleme[alias]["ckpt_sha256"] = sha256(yukleme[alias]["ckpt"])
rapor["yukleme"] = yukleme
rapor["kimlik"] = kimlik

t = time.time()
(_, loader), manifest = tm.v2_loaders("data/imagenetv2", 2000, 25, "BicubicRes256Crop224", 10)
rapor["veri"] = {"liste_sha256": manifest["liste_sha256"], "kayit_liste_sha256": ozet["imagenetv2_liste_sha256"],
                 "liste_ayni": manifest["liste_sha256"] == ozet["imagenetv2_liste_sha256"],
                 "yukleme_s": round(time.time() - t, 1)}
mf = json.loads((KOK / "results/q1/konsey_b8_imagenetv2/matris/imagenetv2_manifest.json").read_text())
rapor["veri"]["b8_manifest_liste_sha256"] = mf.get("liste_sha256")
rapor["veri"]["ilk100_dosyalar_b8_manifestle_ayni"] = [d["yol"] for d in manifest["dosyalar"][:N]] == [d["yol"] for d in mf["dosyalar"][:N]]
rapor["veri"]["ilk100_ilk_son"] = [manifest["dosyalar"][0]["yol"], manifest["dosyalar"][N - 1]["yol"]]

# ---------------- gradyanlar ----------------
names = [a for _, a in RB]
torch.cuda.synchronize()
tg = time.time()
Gs = {n: [] for n in names}
oks = {n: [] for n in names}
preds = {n: [] for n in names}
cos_l, nr_l = [], []
xs, ys = [], []
for _s, x, y in tm._iter_batches(loader, N):
    x, y = x.to(device), y.to(device)
    G = []
    for n in names:
        g = b10.girdi_gradyani(models[n], x, y)
        G.append(g)
        Gs[n].append(g.cpu())
        with torch.no_grad():
            pr = models[n](x).argmax(1)
        preds[n].append(pr.cpu())
        oks[n].append((pr == y).cpu())
    c, nr = b10.cift_kosinus(torch.stack(G))
    cos_l.append(c.cpu().double())
    nr_l.append(nr.cpu())
    xs.append(x.cpu())
    ys.append(y.cpu())
# ozdeslik: R18 gradyanini ilk batch icin yeniden al
x0, y0 = xs[0].to(device), ys[0].to(device)
g18b = b10.girdi_gradyani(models["IN_Salman2020Do_R18"], x0, y0).cpu()
g50b = b10.girdi_gradyani(models["IN_Salman2020Do_R50"], x0, y0).cpu()
torch.cuda.synchronize()
gpu_s = time.time() - tg
cos = torch.cat(cos_l, 0).numpy()
nr = torch.cat(nr_l, 1).numpy()
G = {n: torch.cat(Gs[n], 0).double() for n in names}
OK = {n: torch.cat(oks[n]).numpy() for n in names}
PR = {n: torch.cat(preds[n]).numpy() for n in names}

# ---------------- kayitla karsilastirma ----------------
z = np.load(KAYIT / "kosinus.npz")
kn = list(z["modeller"])
kc = [tuple(int(v) for v in c) for c in z["ciftler"]]
kcos = z["cos"].astype(np.float64)
benim = list(combinations(range(len(names)), 2))
kars = {}
for a, b in CIFTLER:
    i, j = names.index(a), names.index(b)
    pi = benim.index((min(i, j), max(i, j)))
    ki, kj = kn.index(a), kn.index(b)
    pk = kc.index((min(ki, kj), max(ki, kj)))
    v, kv = cos[:, pi], kcos[:N, pk]
    kars[f"{a}|{b}"] = {"yeni_ort100": r(v.mean()), "yeni_sd100": r(v.std()), "kayit_ort100": r(kv.mean()),
                        "kayit_sd100": r(kv.std()), "kayit_ort2000": r(kcos[:, pk].mean()),
                        "kayit_c_tum": r(ozet["c_tum"][ki][kj]),
                        "goruntu_maks_mutlak_fark": r(np.abs(v - kv).max(), 6),
                        "yeni_min": r(v.min()), "yeni_maks": r(v.max())}
rapor["karsilastirma"] = kars
kn_norm = z["norm"][:, :N]
kok_ = z["temiz_dogru"][:, :N]
rapor["norm_ve_dogruluk"] = {n: {"norm_ort_yeni": r(nr[k].mean()), "norm_ort_kayit": r(kn_norm[kn.index(n)].mean()),
                                 "norm_maks_goreli_fark": r(np.max(np.abs(nr[k] - kn_norm[kn.index(n)]) / kn_norm[kn.index(n)]), 7),
                                 "norm_medyan_yeni": r(np.median(nr[k])),
                                 "temiz_dogru100_yeni": r(100 * OK[n].mean(), 2),
                                 "temiz_dogru100_kayit": r(100 * kok_[kn.index(n)].mean(), 2),
                                 "dogru_maskesi_ayni": bool((OK[n] == kok_[kn.index(n)]).all()),
                                 "temiz_dogru2000_kayit": ozet["temiz_dogruluk_yuzde"][n]}
                             for k, n in enumerate(names)}

# ---------------- teshis ----------------


def cosv(A, B):
    return (F.normalize(A, dim=1) * F.normalize(B, dim=1)).sum(1)


g18, g50 = G["IN_Salman2020Do_R18"], G["IN_Salman2020Do_R50"]
tes = {}
tes["oz_kosinus_R18_ayni_girdi_ikinci_gecis"] = [r(cosv(g18b.double(), g18[:25]).min(), 7), r(cosv(g18b.double(), g18[:25]).max(), 7)]
tes["oz_kosinus_R50_ayni_girdi_ikinci_gecis"] = [r(cosv(g50b.double(), g50[:25]).min(), 7), r(cosv(g50b.double(), g50[:25]).max(), 7)]
tes["oz_kosinus_R18_R18"] = r(cosv(g18, g18).mean(), 7)
kay = {}
for a, b in CIFTLER:
    A, B = G[a], G[b]
    eslesik = cosv(A, B)
    kayik = [cosv(A, torch.roll(B, s, 0)).mean().item() for s in (1, 7, 50)]
    kay[f"{a}|{b}"] = {"eslesik_ort": r(eslesik.mean()), "kaydirilmis_ort_s1_s7_s50": [r(v) for v in kayik]}
tes["kaydirilmis_indeks"] = kay
# ortalama gradyan goruntusu (birim normlu gradyanlarin ortalamasi)
ortg = {}
for n in names:
    u = F.normalize(G[n], dim=1)
    mvec = u.mean(0)
    ortg[n] = mvec
    tes.setdefault("ortalama_gradyan_normu", {})[n] = r(mvec.norm())
    tes.setdefault("kanal_ortalamasi_x1e4", {})[n] = [r(1e4 * v, 4) for v in G[n].view(N, 3, -1).mean((0, 2)).tolist()]
tes["ortalama_gradyan_kosinusu_R18_R50"] = r(F.cosine_similarity(ortg["IN_Salman2020Do_R18"], ortg["IN_Salman2020Do_R50"], dim=0))
tes["ortalama_gradyan_kosinusu_R18_50_2"] = r(F.cosine_similarity(ortg["IN_Salman2020Do_R18"], ortg["IN_Salman2020Do_50_2"], dim=0))
# ortalama bileseni cikarilmis kosinus
u18 = F.normalize(g18, dim=1); u50 = F.normalize(g50, dim=1)
tes["ortalama_cikarilmis_kosinus_R18_R50"] = r(cosv(u18 - u18.mean(0), u50 - u50.mean(0)).mean())
# yogunlasma: norm^2'nin en buyuk %1 ogede payi
for n in names:
    e = G[n] ** 2
    k = int(0.01 * e.shape[1])
    tes.setdefault("enerji_payi_en_buyuk_yuzde1", {})[n] = r((e.topk(k, dim=1).values.sum(1) / e.sum(1)).mean(), 4)
# frekans bandlarina gore kosinus ayrisimi (Parseval): c = sum_band Re<F_i, F_j> / (|g_i||g_j|)
H = W = 224
fy = torch.fft.fftfreq(H).abs().view(H, 1); fx = torch.fft.fftfreq(W).abs().view(1, W)
rad = torch.maximum(fy, fx)  # 0 .. 0.5 (Nyquist)
bantlar = [(0, 1 / 32), (1 / 32, 1 / 16), (1 / 16, 1 / 8), (1 / 8, 1 / 4), (1 / 4, 0.5001)]


def bant(A):
    return torch.fft.fft2(A.view(N, 3, H, W))


FA = {n: bant(G[n]) for n in ["IN_Salman2020Do_R18", "IN_Salman2020Do_R50", "IN_Salman2020Do_50_2", "IN_Engstrom2019Robustness"]}
frek = {}
for n, Fn in FA.items():
    tot = (Fn.abs() ** 2).sum((1, 2, 3))
    frek[n] = {"enerji_payi": [r(((Fn.abs() ** 2) * ((rad >= lo) & (rad < hi))).sum((1, 2, 3)).div(tot).mean(), 4) for lo, hi in bantlar]}
for a, b in [("IN_Salman2020Do_R18", "IN_Salman2020Do_R50"), ("IN_Salman2020Do_R18", "IN_Salman2020Do_50_2"),
             ("IN_Salman2020Do_R50", "IN_Engstrom2019Robustness"), ("IN_Salman2020Do_R18", "IN_Engstrom2019Robustness"),
             ("IN_Salman2020Do_R50", "IN_Salman2020Do_50_2")]:
    Fa, Fb = FA[a], FA[b]
    den = torch.sqrt((Fa.abs() ** 2).sum((1, 2, 3)) * (Fb.abs() ** 2).sum((1, 2, 3)))
    katki, bkos = [], []
    for lo, hi in bantlar:
        msk = (rad >= lo) & (rad < hi)
        num = ((Fa * Fb.conj()).real * msk).sum((1, 2, 3))
        katki.append(r((num / den).mean()))
        bden = torch.sqrt(((Fa.abs() ** 2) * msk).sum((1, 2, 3)) * ((Fb.abs() ** 2) * msk).sum((1, 2, 3)))
        bkos.append(r((num / bden).mean()))
    frek[f"{a}|{b}"] = {"bant_katkisi_toplam_kosinusa": katki, "bant_ici_kosinus": bkos}
tes["frekans"] = {"bantlar_nyquist_0.5": [[lo, min(hi, 0.5)] for lo, hi in bantlar], **frek}
# alcak geciren (8x8 ortalama havuz) kosinus
def lp(A, k=8):
    return F.avg_pool2d(A.view(N, 3, H, W).float(), k).flatten(1).double()
tes["alcak_gecirgen_8x8_kosinus"] = {f"{a}|{b}": r(cosv(lp(G[a]), lp(G[b])).mean()) for a, b in CIFTLER}
# tahmin uyumu
tes["tahmin_uyumu_yuzde"] = {f"{a}|{b}": r(100 * (PR[a] == PR[b]).mean(), 2) for a, b in CIFTLER}
# isaret uyumu (sign(g) eslesme orani; 0.5 = bagimsiz)
tes["isaret_uyumu"] = {f"{a}|{b}": r((torch.sign(G[a]) == torch.sign(G[b])).double().mean()) for a, b in CIFTLER}
rapor["teshis"] = tes
rapor["gpu_gradyan_s"] = round(gpu_s, 2)
rapor["toplam_s"] = round(time.time() - t0, 1)
rapor["cihaz"] = torch.cuda.get_device_name(0)
rapor["torch"] = torch.__version__
(OUT / "denetim.json").write_text(json.dumps(rapor, indent=1, ensure_ascii=False))
torch.save({n: ortg[n].float().view(3, H, W) for n in names}, OUT / "ortalama_gradyan.pt")
print(json.dumps(rapor, indent=1, ensure_ascii=False))
