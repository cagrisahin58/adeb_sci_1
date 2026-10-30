# -*- coding: utf-8 -*-
"""B10: temiz goruntude modeller arasi girdi gradyani kosinusu ve log tau ile Mantel sinamasi (30.10.2026).

Fable karari E3: c_ij (i ve j modellerinin ayni temiz goruntude dogru etiketli capraz entropi kaybinin
girdiye gore gradyanlari arasindaki kosinusun goruntuler uzerinden ortalamasi) log tau_ij'yi uc veri
kumesinde ongoruyor mu. Hakemin iki degisikligi uygulanir: model duzeyi ana etkiler ayrica ele alinir
(ana etkileri cikarilmis artiklarla Mantel ve kovaryat matrisli kismi Mantel) ve Zhang ve ark.
(arXiv 2307.07873, "Why Does Little Robustness Help? A Further Step Towards Understanding Adversarial
Transferability", IEEE S&P 2024, DOI 10.1109/SP54263.2024.00010; export.arxiv.org API ile 30.10.2026'da
dogrulandi) oncul olarak anilir. Demontis ve ark. (arXiv 1809.02861) gradyan hizalanmasi cercevesidir.

Iki alt komut:
  gradyan : modelleri yukler (q1_ek_transfer_matrix.py'nin yukleyicileri), her goruntude her modelin
            girdi gradyanini alir (eval kipi, fp32, [0,1] piksel uzayi, model ici normalizasyon dahil),
            cift basina goruntu kosinuslerini biriktirir. Gradyanlar saklanmaz. Cikti: kosinus.npz
            (goruntu x cift kosinus float16, model x goruntu gradyan normu, temiz dogru maskesi) ve
            kosinus_ozet.json (c matrisi: butun goruntuler; duyarlilik: iki model de temiz dogru).
  mantel  : kosinus_ozet.json ile transfer matrisi klasorlerinden (dondurulmus q1_konsey_ayrisim.py'nin
            islevleri, sha256 denetimiyle) bolunmus yari log tau matrisini kurar; ortak modellerde
            sirasiz ciftler uzerinde Spearman istatistigiyle Mantel (ortak etiket permutasyonu, tek
            yonlu, H1: pozitif), ana etkileri cikarilmis artiklarla Mantel ve kismi Mantel (kovaryatlar:
            omega = log w toplam ve fark matrisleri; istege bagli log gradyan normu) uygular.

Kullanim (konteyner; GPU isi, kisa):
  python experiments/q1_ek_gradyan_kosinus.py gradyan --dataset cifar100 --n-samples 10000 \\
      --model C100_ResNet18_AT_s1001:resnet18:models/q1/cifar100/resnet18_s1001/resnet18/adv/adversarial_training/best.pth \\
      --rb-model Rice2020Overfitting ... --cikti results/q1/konsey_b10_gradyan/cifar100
  python experiments/q1_ek_gradyan_kosinus.py mantel --kosinus results/q1/konsey_b10_gradyan/cifar100/kosinus_ozet.json \\
      --matris-dizini results/q1/konsey_b9_c100/matris --veri-kumesi cifar100 --cikti results/q1/konsey_b10_gradyan/mantel_cifar100.json
"""
import argparse
import hashlib
import importlib.util
import io
import json
import sys
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy import stats

KOK = Path(__file__).resolve().parents[1]
PERM_VARSAYILAN = 9999  # ek on kayit §6.2: 9999 permutasyon, p = (1 + #)/10000
TOHUM = 20261030


def _modul(ad, dosya):
    spec = importlib.util.spec_from_file_location(ad, KOK / "experiments" / dosya)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sha256(yol):
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ----------------------------------------------------------------------------------------------
# Gradyan kosinusu
# ----------------------------------------------------------------------------------------------
def girdi_gradyani(model, x, y):
    """Goruntu basina dogru etiketli CE kaybinin girdiye gore gradyani (B, D). Eval kipinde ornekler
    bagimsiz oldugundan toplam kaybin gradyani goruntu basina gradyanlardir."""
    import torch
    import torch.nn.functional as F

    x = x.detach().clone().requires_grad_(True)
    loss = F.cross_entropy(model(x), y, reduction="sum")
    (g,) = torch.autograd.grad(loss, x)
    return g.flatten(1)


def cift_kosinus(G):
    """G: (K, B, D) -> (B, K(K-1)/2) kosinus (sira: combinations(range(K), 2)), (K, B) norm.
    Normu sifir olan gradyanda kosinus NaN."""
    import torch

    norm = G.norm(dim=2)  # (K, B)
    Gn = G / norm.clamp_min(1e-30).unsqueeze(2)
    K = G.shape[0]
    cs = []
    for i, j in combinations(range(K), 2):
        c = (Gn[i] * Gn[j]).sum(1)
        c = torch.where((norm[i] > 0) & (norm[j] > 0), c, torch.full_like(c, float("nan")))
        cs.append(c)
    return torch.stack(cs, 1), norm


def gradyan(a):
    import torch

    tm = _modul("q1_ek_transfer_matrix", "q1_ek_transfer_matrix.py")
    tm.set_seed(a.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    models, specs = {}, {}
    for spec in (a.model or []):
        name, mtype, mpath = spec.split(":", 2)
        models[name] = tm.load_local(mtype, mpath, device).eval()
        specs[name] = (mtype, mpath)
    for spec in (a.rb_model or []):
        rb_name, _, alias = spec.partition(":")
        models[alias or rb_name] = tm.load_wrn(device, dataset=a.dataset, rb_name=rb_name).eval()
        specs[alias or rb_name] = ("robustbench", rb_name)
    for m in models.values():
        for p in m.parameters():
            p.requires_grad_(False)
    names = list(models)
    if len(names) < 2:
        raise SystemExit("en az iki model gerekir")
    manifest = None
    if a.dataset == "imagenetv2":
        (_, loader), manifest = tm.v2_loaders(a.v2_kok, a.n_samples, a.batch_size, a.in_onisleme,
                                               a.v2_sinif_dosya or None)
    else:
        _, loader = tm.get_loaders(dataset=a.dataset, data_dir="./data", test_batch_size=a.batch_size)
    cos_l, norm_l, ok_l = [], [], []
    for _s, x, y in tm._iter_batches(loader, a.n_samples):
        x, y = x.to(device), y.to(device)
        G, ok = [], []
        for n in names:
            G.append(girdi_gradyani(models[n], x, y))
            with torch.no_grad():
                ok.append((models[n](x).argmax(1) == y).cpu())
        c, nr = cift_kosinus(torch.stack(G))
        cos_l.append(c.cpu().numpy().astype(np.float16))
        norm_l.append(nr.cpu().numpy().astype(np.float32))
        ok_l.append(torch.stack(ok).numpy())
        del G
    cos = np.concatenate(cos_l, 0)          # (n, P)
    norm = np.concatenate(norm_l, 1)        # (K, n)
    ok = np.concatenate(ok_l, 1)            # (K, n)
    ciftler = list(combinations(range(len(names)), 2))
    C = np.eye(len(names))
    C_dogru = np.eye(len(names))
    n_dogru = {}
    for p, (i, j) in enumerate(ciftler):
        v = cos[:, p].astype(np.float64)
        C[i, j] = C[j, i] = float(np.nanmean(v))
        m = ok[i] & ok[j]
        C_dogru[i, j] = C_dogru[j, i] = float(np.nanmean(v[m])) if m.any() else float("nan")
        n_dogru[f"{names[i]}|{names[j]}"] = int(m.sum())
    out_dir = Path(a.cikti)
    out_dir.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out_dir / "kosinus.npz", cos=cos, norm=norm, temiz_dogru=ok,
                        modeller=np.array(names), ciftler=np.array(ciftler))
    ozet = {"betik": "experiments/q1_ek_gradyan_kosinus.py", "betik_sha256": sha256(__file__),
            "veri_kumesi": a.dataset, "n": int(cos.shape[0]), "modeller": names,
            "model_specs": {n: list(specs[n]) for n in names},
            "c_tum": C.tolist(), "c_iki_model_dogru": C_dogru.tolist(), "n_iki_model_dogru": n_dogru,
            "log_gradyan_normu_ort": {n: float(np.mean(np.log(np.maximum(norm[k], 1e-30))))
                                      for k, n in enumerate(names)},
            "temiz_dogruluk_yuzde": {n: round(100.0 * float(ok[k].mean()), 2) for k, n in enumerate(names)},
            "nan_kosinus_sayisi": int(np.isnan(cos.astype(np.float32)).sum()),
            "tanim": "c_ij = ort_x cos(grad_x CE(f_i(x), y), grad_x CE(f_j(x), y)); eval, fp32, [0,1] uzayi",
            "uretildi_utc": datetime.now(timezone.utc).isoformat()}
    if manifest is not None:
        ozet["imagenetv2_liste_sha256"] = manifest["liste_sha256"]
        ozet["on_isleme"] = manifest["onisleme"]
    (out_dir / "kosinus_ozet.json").write_text(json.dumps(ozet, indent=1))
    print("yazildi:", out_dir / "kosinus_ozet.json")
    return ozet


# ----------------------------------------------------------------------------------------------
# Mantel ve kismi Mantel (numpy/scipy)
# ----------------------------------------------------------------------------------------------
def ust_ucgen(A):
    i, j = np.triu_indices(A.shape[0], 1)
    return A[i, j]


def sira(v):
    return stats.rankdata(v)


def ana_etki_artik(A):
    """Simetrik matrisin kosegen disi ogelerine A_ij = mu + a_i + a_j toplamsal modelini en kucuk
    kareyle oturtur, artik matrisi doner (kosegen 0). Etiket permutasyonuna esdegisken."""
    K = A.shape[0]
    i, j = np.triu_indices(K, 1)
    X = np.zeros((len(i), K + 1))
    X[:, 0] = 1.0
    X[np.arange(len(i)), 1 + i] = 1.0
    X[np.arange(len(i)), 1 + j] = 1.0
    y = A[i, j]
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ beta
    R = np.zeros_like(A, dtype=float)
    R[i, j] = e
    R[j, i] = e
    return R


def _artik(v, Z):
    if Z is None:
        return v - v.mean()
    X = np.column_stack([np.ones(len(v))] + [z for z in Z])
    beta, *_ = np.linalg.lstsq(X, v, rcond=None)
    return v - X @ beta


def _kor(a, b):
    sa, sb = np.std(a), np.std(b)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(np.mean((a - a.mean()) * (b - b.mean())) / (sa * sb))


def mantel(X, Y, Z=None, perm=PERM_VARSAYILAN, tohum=TOHUM, rank=True):
    """Mantel (Z yoksa) ya da kismi Mantel (Z: kovaryat matrisleri listesi) sinamasi.
    Istatistik: sira donusumlu (Spearman) ust ucgen vektorlerinde, Z'ye gore artiklanmis korelasyon.
    Permutasyon: X'in satir ve sutunlari ortak permute edilir (Legendre ve Legendre 2012, kismi Mantel
    icin 'ham X permutasyonu'); Y ve Z sabittir. p_tek = (1 + #{r* >= r}) / (perm + 1)."""
    X, Y = np.asarray(X, float), np.asarray(Y, float)
    K = X.shape[0]
    if K < 4:
        return {"K": K, "not": "K < 4: sinama tanimsiz"}
    f = sira if rank else (lambda v: v)
    y = f(ust_ucgen(Y))
    zs = None if not Z else [f(ust_ucgen(np.asarray(z, float))) for z in Z]
    ry = _artik(y, zs)

    def ist(Xm):
        return _kor(_artik(f(ust_ucgen(Xm)), zs), ry)

    r0 = ist(X)
    if not np.isfinite(r0):
        return {"K": K, "istatistik": r0, "not": "istatistik tanimsiz (sabit vektor)", "p_tek": None, "p_iki": None}
    rng = np.random.default_rng(tohum)
    dist = np.empty(perm)
    for b in range(perm):
        p = rng.permutation(K)
        dist[b] = ist(X[np.ix_(p, p)])
    ok = np.isfinite(dist)
    return {"K": K, "cift_sayisi": int(K * (K - 1) // 2), "istatistik": r0, "perm": perm, "tohum": tohum,
            "p_tek": float((1 + np.sum(dist[ok] >= r0)) / (ok.sum() + 1)),
            "p_iki": float((1 + np.sum(np.abs(dist[ok]) >= abs(r0))) / (ok.sum() + 1)),
            "perm_ort": float(np.nanmean(dist)), "perm_sd": float(np.nanstd(dist)),
            "kovaryat_sayisi": 0 if not Z else len(Z), "sira_donusumu": rank}


def log_tau_matrisi(dizinler, modeller, kestirim="yari"):
    """Dondurulmus betigin islevleriyle (sha256 denetimli) log tau matrisi ve omega = log w (tam)."""
    ek = _modul("q1_ek_ayrisim", "q1_ek_ayrisim.py")
    dm = ek.dondurulmus()
    M = ek.matris_yukle(dizinler)
    g = dm.Alici(M)
    f = dm.olcek_f("log")
    var = [m for m in modeller if M.var(m, m) and all(M.var(m, c) and M.var(c, m) for c in modeller if c != m)]
    K = len(var)
    T = np.zeros((K, K))
    for a_, b_ in combinations(range(K), 2):
        v = dm.ort_yapi(lambda wa, Ta: dm.tau_ij(g, f, var[a_], var[b_], wa, Ta), kestirim)
        T[a_, b_] = T[b_, a_] = v
    om = np.array([float(f(g(m, m, "tam"))) for m in var])
    return var, T, om, M


def mantel_kos(a):
    oz = json.loads(Path(a.kosinus).read_text())
    names = oz["modeller"]
    C_full = np.asarray(oz["c_iki_model_dogru" if a.duyarlilik_dogru else "c_tum"], float)
    esl = json.loads(Path(a.esleme).read_text()) if a.esleme else {}
    names_m = [esl.get(n, n) for n in names]
    var, T, om, M = log_tau_matrisi(a.matris_dizini, names_m)
    idx = [names_m.index(v) for v in var]
    C = C_full[np.ix_(idx, idx)]
    lgn = np.array([oz["log_gradyan_normu_ort"][names[k]] for k in idx])
    Z_om = [om[:, None] + om[None, :], np.abs(om[:, None] - om[None, :])]
    Z_gn = Z_om + [lgn[:, None] + lgn[None, :]]
    s = {"ham": mantel(C, T, None, a.perm),
         "ana_etki_artik": mantel(ana_etki_artik(C), ana_etki_artik(T), None, a.perm),
         "kismi_omega": mantel(C, T, Z_om, a.perm),
         "kismi_omega_gradnorm": mantel(C, T, Z_gn, a.perm)}
    out = {"veri_kumesi": a.veri_kumesi, "betik": "experiments/q1_ek_gradyan_kosinus.py",
           "betik_sha256": sha256(__file__), "kosinus_ozet": a.kosinus, "kosinus_ozet_sha256": sha256(a.kosinus),
           "matris_dizinleri": a.matris_dizini, "girdi_sha256": M.kaynaklar,
           "c_turu": "iki_model_dogru" if a.duyarlilik_dogru else "tum",
           "modeller_ortak": var, "dislanan": [n for n in names_m if n not in var],
           "c_matrisi": C.tolist(), "log_tau_matrisi": T.tolist(), "omega_log_w": om.tolist(),
           "log_gradyan_normu": lgn.tolist(), "sinamalar": s,
           "not": ("Birincil: ham Mantel (Spearman, tek yonlu, pozitif). Ana etki artigi ve kismi Mantel "
                   "model duzeyi ana etkileri (gurbuzluk duzeyi, gradyan buyuklugu ve algisal hizalanma "
                   "gibi model ozellikleri) ayiklar. Yorum ek on kayda gore yapilir."),
           "uretildi_utc": datetime.now(timezone.utc).isoformat()}
    if a.sinama:
        out["SINAMA_SONUC_DEGIL"] = True
    Path(a.cikti).parent.mkdir(parents=True, exist_ok=True)
    with io.open(a.cikti, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("yazildi:", a.cikti, {k: (round(v.get("istatistik", float("nan")), 3), v.get("p_tek")) for k, v in s.items()})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="komut", required=True)
    g = sub.add_parser("gradyan")
    g.add_argument("--dataset", required=True, choices=["cifar10", "cifar100", "svhn", "imagenetv2"])
    g.add_argument("--model", action="append", default=None, metavar="AD:TIP:YOL")
    g.add_argument("--rb-model", action="append", default=None, metavar="AD[:TAKMA_AD]")
    g.add_argument("--n-samples", type=int, default=10000)
    g.add_argument("--batch-size", type=int, default=50)
    g.add_argument("--seed", type=int, default=42)
    g.add_argument("--v2-kok", default="data/imagenetv2")
    g.add_argument("--v2-sinif-dosya", type=int, default=10)
    g.add_argument("--in-onisleme", default="BicubicRes256Crop224", choices=["BicubicRes256Crop224", "Res256Crop224"],
                   help="ImageNetV2 ortak hatti (ek on kayit §5.2; varsayilan bicubic)")
    g.add_argument("--cikti", required=True)
    m = sub.add_parser("mantel")
    m.add_argument("--kosinus", required=True)
    m.add_argument("--matris-dizini", action="append", required=True)
    m.add_argument("--veri-kumesi", required=True)
    m.add_argument("--esleme", default=None, help="kosinus takma adi -> matris takma adi JSON")
    m.add_argument("--perm", type=int, default=PERM_VARSAYILAN)
    m.add_argument("--duyarlilik-dogru", action="store_true", help="c'yi iki modelin de dogru oldugu goruntulerle al")
    m.add_argument("--sinama", action="store_true")
    m.add_argument("--cikti", required=True)
    a = ap.parse_args(argv)
    return gradyan(a) if a.komut == "gradyan" else mantel_kos(a)


if __name__ == "__main__":
    main()
