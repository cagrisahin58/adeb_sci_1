"""11_sonuc_b8_b10 raporu icin salt okur yardimci (konteynerde, numpy ile): B8 ve B9 kosegeni.
Hicbir dosya yazmaz. Depo kokunden: docker exec -w /workspace adeb_eval python arsiv/b2_yardimci/_ek_rapor_kosegen.py
Her model icin beyaz kutu (kosegen) npz'den temiz dogruluk, PGD-10 dogrulugu (temiz dogru ve saldiri sonrasi dogru),
w (hedef-dogru payda uzerinde kandirma orani) ve sayimlar; transfer_matrix.json ust alanlariyla karsilastirma.
"""
import json
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

for ad, M in [("B9", "results/q1/konsey_b9_c100/matris"), ("B8", "results/q1/konsey_b8_imagenetv2/matris")]:
    tm = json.load(open(f"{M}/transfer_matrix.json"))
    print(f"\n== {ad} {M}")
    for k in ["pair", "seed", "n_samples", "eps", "alpha", "steps", "attack", "dataset", "ek_betik", "ek_betik_sha256",
              "eps_255", "alpha_255", "batch_size", "cache_f16", "on_isleme", "manifest_liste_sha256", "manifest_n",
              "per_source_seed", "cache_adv", "normalizasyon"]:
        if k in tm:
            print(f"  meta {k} = {json.dumps(tm[k], ensure_ascii=False)[:200]}")
    td = tm.get("temiz_dogruluk", {})
    modeller = tm["models"]
    print("  model sayisi:", len(modeller))
    ilk = None
    for m in modeller:
        d = np.load(f"{M}/per_sample_{m}_to_{m}.npz")
        if ilk is None:
            ilk = {k: (d[k].shape, str(d[k].dtype)) for k in d.keys()}
            print("  npz anahtarlari:", ilk)
        cc = d["target_clean_correct"].astype(bool)
        aw = d["target_adv_wrong"].astype(bool)
        n = aw.shape[0]
        temiz = cc.mean() * 100
        pgd = (cc & ~aw).mean() * 100
        w = (aw & cc).sum() / cc.sum() * 100
        r = tm["results"][f"{m}->{m}"]
        print(f"  {m}: n={n} temiz={temiz:.2f} ({int(cc.sum())}) pgd10_dogru={pgd:.2f} ({int((cc & ~aw).sum())}) "
              f"w={w:.2f} | tm: target_clean_acc={r['target_clean_acc']} cond_fooling={r['cond_fooling']} "
              f"n_cond={r['n_cond']} raw_fooling={r['raw_fooling']} | tm.temiz_dogruluk={td.get(m)}")
