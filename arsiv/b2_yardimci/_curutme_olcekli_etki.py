# -*- coding: utf-8 -*-
"""Curutme (ikinci tur): (1) CNN'ler arasi sigma yayilimiyla olceklenmis etki buyuklugu (V-scr, V-IN, XCiT z
degerleri; H1'in CNN SD'si cinsinden buyuklugu); (2) uc bilesenli belirsizlik: hiyerarsik bootstrap (tohum +
goruntu) SD'si ile panel jackknife SE'sinin birlesimi (K-b, q, H1, H2, H3). Kesifsel, on kayit disi."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _curutme_ortak as O  # noqa: E402

K = O.K
Q = O.KOK / "results/q1"


def main():
    M, t, P, P2 = O.yukle(*O.C10)
    g = K.Alici(M)
    sig = {m: O.md(g, O.f_log, m, P)["sigma"] for m in M.modeller()}
    hucre_ort = {h: float(np.mean([sig[m] for m in O.hucre(t, M, h)]))
                 for h in ["V-scr", "V-IN", "R224-scr", "R224-IN", "C1-R32"]}
    panel = {c: sig[c] for c in P}
    birim = list(panel.values()) + [hucre_ort["C1-R32"], hucre_ort["R224-scr"], hucre_ort["R224-IN"]]
    sd_panel = float(np.std(list(panel.values()), ddof=1))
    sd_birim = float(np.std(birim, ddof=1))
    ort_birim = float(np.mean(birim))
    z = {}
    for ad, v in (("V-scr", hucre_ort["V-scr"]), ("V-IN", hucre_ort["V-IN"]),
                  ("XCiT", float(np.mean([sig[c] for c in P2])))):
        z[ad] = {"sigma": v, "z_cnn_10_birim": (v - ort_birim) / sd_birim}
    H1 = hucre_ort["V-scr"] - hucre_ort["R224-scr"]
    olcekli = {"H1_kestirim": H1, "H1_bolu_sd_cnn_10_birim": H1 / sd_birim, "H1_bolu_sd_panel_7": H1 / sd_panel,
               "panel_sigma": panel, "panel_aralik": [min(panel.values()), max(panel.values())],
               "sd_panel_7": sd_panel, "sd_cnn_10_birim": sd_birim, "ort_cnn_10_birim": ort_birim,
               "hucre_ort": hucre_ort, "z": z,
               "not": "10 birim: yedi panel uyesi (kendi disarida birakmali sigma) ve kendi uc CNN hucresinin ortalamasi; "
                      "tohumlar hucre ortalamasina indirildi."}
    # uc bilesenli belirsizlik
    ay = json.loads((Q / "curutme_2026-11-07/ayrisim.json").read_text(encoding="utf-8"))["g_panel_rastgele_etki"]
    bs10 = json.loads((Q / "konsey_ek_masa/bootstrap_cifar10.json").read_text(encoding="utf-8"))
    hb4 = json.loads((Q / "konsey_ayrisim_b4.json").read_text(encoding="utf-8"))["b4"]["duyarlilik"]["hiyerarsik_bootstrap"]
    uc = {}
    # K-b: bootstrap sd dogrudan; q ve H'ler icin %90 araliktan sd = genislik / (2*1.645)
    kaynak = {"rho_V": bs10["K-b"]["bootstrap"]["ci90"], "q": bs10["K-a"]["bootstrap"]["ci90"],
              "H1": hb4["H1"]["ci90"], "H2": hb4["H2"]["ci90"], "H3": hb4["H3"]["ci90"]}
    for k_, ci in kaynak.items():
        sd_h = (ci[1] - ci[0]) / (2 * 1.645)
        sd_p = ay[k_]["se_panel_jackknife"]
        nokta = ay[k_]["tam"]
        se = float(np.sqrt(sd_h ** 2 + sd_p ** 2))
        uc[k_] = {"nokta": nokta, "sd_hiyerarsik_bootstrap_ci90den": sd_h, "se_panel_jackknife": sd_p,
                  "se_uc_bilesen": se, "ci90_uc_bilesen": [nokta - 1.645 * se, nokta + 1.645 * se],
                  "panel_jk_varyans_payi": sd_p ** 2 / se ** 2}
    uc["K-b_band_icinde"] = bool(uc["rho_V"]["ci90_uc_bilesen"][0] > -0.10 and uc["rho_V"]["ci90_uc_bilesen"][1] < 0.10)
    uc["H3_band_icinde"] = bool(uc["H3"]["ci90_uc_bilesen"][0] > -0.10 and uc["H3"]["ci90_uc_bilesen"][1] < 0.10)
    uc["not"] = ("Hiyerarsik bootstrap tohum ve goruntuyu, panel jackknife panel uyeligini tasir; bilesenler bagimsiz "
                 "sayilarak kareler toplami alindi (normal yaklasim). K-b ve q bootstrap'i M11.1, H'ler B4 duyarliligi.")
    O.yaz("olcekli_etki", {"olcekli_etki": olcekli, "uc_bilesenli_belirsizlik": uc}, __file__)


if __name__ == "__main__":
    main()
