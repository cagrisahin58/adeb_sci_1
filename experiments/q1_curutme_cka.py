# -*- coding: utf-8 -*-
"""Curutme G blogu (08.11.2026): modeller arasi dogrusal CKA (Kornblith ve ark. 2019, arXiv 1905.00414).

Tanim: her model icin siniflandirici basinin girdisi (son nn.Linear katmaninin girdisi; out_features =
sinif sayisi olan son dogrusal katman) oznitelik olarak alinir. Iki modelin ayni goruntulerdeki oznitelik
matrisleri X (n x d1), Y (n x d2) sutun ortalamalari cikarilarak merkezlenir ve
    CKA(X, Y) = ||Y^T X||_F^2 / (||X^T X||_F ||Y^T Y||_F)
hesaplanir (dogrusal cekirdek, oznitelik uzayi formulu).

Iki matris uretilir:
  temiz : CIFAR-10 testinin ilk n goruntusu (varsayilan 5000), egitim kipi kapali (eval), [0, 1] uzayi.
  pgd   : PGD-10 ornekleri. i ve j cifti icin CKA_pgd_ij = 1/2 [CKA(f_i(X_i), f_j(X_i)) + CKA(f_i(X_j), f_j(X_j))],
          X_k = k kaynaginin onbellekteki PGD-10 (eps 8/255, alpha 2/255, tohum 42) ornekleri (ilk n_pgd
          goruntu, varsayilan 1000). Onbellek D blogu matrisinin --cache-adv klasorudur; onbellegi olmayan
          kaynak bu matristen cikarilir ve listelenir.
Cikti klasorune, q1_ek_gradyan_kosinus.py 'mantel' alt komutunun okudugu semayla iki dosya yazilir:
cka_temiz_ozet.json ve cka_pgd_ozet.json ('modeller', 'c_tum' = CKA matrisi, 'log_gradyan_normu_ort' =
0 yer tutucusu; Mantel'in gradyan normlu kismi surumu bu dosyalarda anlamsizdir ve raporlanmaz). Boylece B10
Mantel islevleri aynen kullanilir ("c_ij yerine CKA_ij", 02_deney_adaylari.json G.cozumleme_yeniden_kullanim).

Kullanim (konteyner, depo koku):
  python experiments/q1_curutme_cka.py --model-seti d28 --eksik-atla --n 5000 --n-pgd 1000 \\
      --onbellek /mnt/d/adeb_sci_1_veri/onbellek/curutme_pgd10_e8 --cikti results/q1/curutme_2026-11-08/G
"""
import argparse
import hashlib
import importlib.util
import io
import json
import os
import signal
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

KOK = Path(__file__).resolve().parents[1]


def _modul(ad, dosya):
    spec = importlib.util.spec_from_file_location(ad, KOK / "experiments" / dosya)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def son_dogrusal(model, n_sinif):
    import torch.nn as nn
    aday = [m for m in model.modules() if isinstance(m, nn.Linear) and m.out_features == n_sinif]
    if not aday:
        raise RuntimeError("siniflandirici basi (son nn.Linear) bulunamadi")
    return aday[-1]


def oznitelik(model, x, bas, bs=250):
    import torch
    tut = {}

    def kanca(_m, inp, _out):
        tut["f"] = inp[0].detach().flatten(1).float()

    h = bas.register_forward_hook(kanca)
    out = []
    try:
        with torch.no_grad():
            for s in range(0, x.shape[0], bs):
                model(x[s:s + bs])
                out.append(tut["f"].double().cpu())
    finally:
        h.remove()
    F = torch.cat(out).numpy()
    return F - F.mean(0, keepdims=True)


def cka(X, Y, xx=None, yy=None):
    xy = np.linalg.norm(Y.T @ X) ** 2
    xx = xx if xx is not None else np.linalg.norm(X.T @ X)
    yy = yy if yy is not None else np.linalg.norm(Y.T @ Y)
    return float(xy / (xx * yy))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-seti", default="d28")
    ap.add_argument("--eksik-atla", action="store_true")
    ap.add_argument("--model", action="append", default=None, metavar="AD:TIP:YOL",
                    help="verilirse --model-seti yerine yalniz bu yerel modeller (duman sinamasi icin)")
    ap.add_argument("--rb-model", action="append", default=None, metavar="AD",
                    help="--model ile birlikte: RobustBench CIFAR-10 modelleri (duman sinamasi icin)")
    ap.add_argument("--n", type=int, default=5000)
    ap.add_argument("--n-pgd", type=int, default=1000)
    ap.add_argument("--onbellek", required=True, help="D blogu matrisinin --cache-adv klasoru")
    ap.add_argument("--onbellek-eki", default="__pgd_linf_s10_n10000_seed42_cifar10.npy")
    ap.add_argument("--cikti", required=True)
    ap.add_argument("--zaman-asimi-s", type=int, default=0)
    a = ap.parse_args()
    os.chdir(KOK)
    if a.zaman_asimi_s > 0:
        signal.signal(signal.SIGALRM, lambda *_: (print("ZAMAN ASIMI", flush=True), sys.exit(124)))
        signal.alarm(a.zaman_asimi_s)

    import torch
    sar = _modul("q1_curutme_transfer_matrix", "q1_curutme_transfer_matrix.py")
    tm = _modul("q1_ek_transfer_matrix", "q1_ek_transfer_matrix.py")
    tm.set_seed(42)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if a.model:
        mod, rb, atlanan = list(a.model), list(a.rb_model or []), []
        a.model_seti = "elle (--model)"
    else:
        mod, rb, atlanan = sar.model_seti(a.model_seti, a.eksik_atla)
    models = {}
    for spec in mod:
        n, tip, yol = spec.split(":", 2)
        models[n] = tm.load_local(tip, yol, device).eval()
    for r in rb:
        models[r] = tm.load_wrn(device, dataset="cifar10", rb_name=r).eval()
    adlar = list(models)
    baslar = {n: son_dogrusal(m, 10) for n, m in models.items()}

    _, loader = tm.get_loaders(dataset="cifar10", data_dir="./data", test_batch_size=250)
    xs, ys = [], []
    for _s, x, y in tm._iter_batches(loader, a.n):
        xs.append(x)
        ys.append(y)
    X = torch.cat(xs)[:a.n].to(device)

    # temiz
    F = {n: oznitelik(models[n], X, baslar[n]) for n in adlar}
    G = {n: np.linalg.norm(F[n].T @ F[n]) for n in adlar}
    K = len(adlar)
    C = np.eye(K)
    for i in range(K):
        for j in range(i + 1, K):
            C[i, j] = C[j, i] = cka(F[adlar[i]], F[adlar[j]], G[adlar[i]], G[adlar[j]])
    del F

    # PGD: kaynak k'nin ornekleri uzerinde butun modellerin oznitelikleri
    kaynaklar = [n for n in adlar if (Path(a.onbellek) / f"{n}{a.onbellek_eki}").exists()]
    eksik_onb = [n for n in adlar if n not in kaynaklar]
    Kp = len(kaynaklar)
    Cp = np.eye(Kp)
    yari = {}  # (k, i, j) -> CKA(f_i(X_k), f_j(X_k))
    for k in kaynaklar:
        adv = np.load(Path(a.onbellek) / f"{k}{a.onbellek_eki}", mmap_mode="r")[:a.n_pgd]
        Xk = torch.from_numpy(np.ascontiguousarray(adv)).to(device)
        Fk = {n: oznitelik(models[n], Xk, baslar[n]) for n in kaynaklar}
        Gk = {n: np.linalg.norm(Fk[n].T @ Fk[n]) for n in kaynaklar}
        for i in range(Kp):
            for j in range(i + 1, Kp):
                if k in (kaynaklar[i], kaynaklar[j]):
                    yari[(k, i, j)] = cka(Fk[kaynaklar[i]], Fk[kaynaklar[j]], Gk[kaynaklar[i]], Gk[kaynaklar[j]])
        del Fk, Xk
    for i in range(Kp):
        for j in range(i + 1, Kp):
            Cp[i, j] = Cp[j, i] = 0.5 * (yari[(kaynaklar[i], i, j)] + yari[(kaynaklar[j], i, j)])

    out_dir = Path(a.cikti)
    out_dir.mkdir(parents=True, exist_ok=True)
    ortak = {"betik": "experiments/q1_curutme_cka.py", "betik_sha256": sha256(__file__),
             "veri_kumesi": "cifar10", "model_seti": a.model_seti, "atlanan_eksik": atlanan,
             "uretildi_utc": datetime.now(timezone.utc).isoformat(),
             "not": "c_tum = dogrusal CKA; log_gradyan_normu_ort yer tutucudur (0), gradyan normlu kismi Mantel raporlanmaz"}
    oz_t = dict(ortak, n=a.n, modeller=adlar, c_tum=C.tolist(),
                log_gradyan_normu_ort={n: 0.0 for n in adlar},
                tanim="CKA_ij = dogrusal CKA, siniflandirici basi girdisi, CIFAR-10 testinin ilk n temiz goruntusu")
    oz_p = dict(ortak, n=a.n_pgd, modeller=kaynaklar, c_tum=Cp.tolist(), onbellek=a.onbellek,
                onbellegi_olmayan=eksik_onb, log_gradyan_normu_ort={n: 0.0 for n in kaynaklar},
                tanim="CKA_pgd_ij = 1/2 [CKA(f_i(X_i), f_j(X_i)) + CKA(f_i(X_j), f_j(X_j))], X_k k'nin PGD-10 ornekleri")
    for ad, oz in (("cka_temiz_ozet.json", oz_t), ("cka_pgd_ozet.json", oz_p)):
        with io.open(out_dir / ad, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(oz, fh, ensure_ascii=False, indent=1)
        print("yazildi", out_dir / ad)


if __name__ == "__main__":
    main()
