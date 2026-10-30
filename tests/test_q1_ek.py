# -*- coding: utf-8 -*-
"""Ek bloklar (B8, B9, B10) kodunun CPU birim sinamalari (30.10.2026).

Konteynerde GPU'ya dokunmadan:
  docker exec -w /workspace -e CUDA_VISIBLE_DEVICES= adeb_eval python -m pytest -q -p no:cacheprovider -o addopts="" tests/test_q1_ek.py
Sahte veriyle calisir; gercek sonuc uretmez.
"""
import importlib.util
import json
import math
import shutil
import sys
import tempfile
from itertools import combinations
from pathlib import Path

import numpy as np
import pytest

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))


def _mod(ad, dosya):
    spec = importlib.util.spec_from_file_location(ad, KOK / "experiments" / dosya)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


GK = _mod("q1_ek_gradyan_kosinus", "q1_ek_gradyan_kosinus.py")
EK = _mod("q1_ek_ayrisim_t", "q1_ek_ayrisim.py")


def _sim(K, rng, f):
    A = np.zeros((K, K))
    for i, j in combinations(range(K), 2):
        A[i, j] = A[j, i] = f(i, j)
    return A


# ---------------------------------------------------------------------------- Mantel
def test_mantel_pozitif_iliski_yakalanir():
    rng = np.random.default_rng(0)
    K = 12
    z = rng.normal(size=(K, 2))
    D = np.linalg.norm(z[:, None] - z[None], axis=2)
    X = -D + 0.1 * _sim(K, rng, lambda i, j: rng.normal())
    Y = -D + 0.1 * _sim(K, rng, lambda i, j: rng.normal())
    r = GK.mantel(X, Y, perm=999)
    assert r["istatistik"] > 0.7 and r["p_tek"] < 0.01


def test_mantel_bagimsizda_birinci_tur_hata_kontrol_altinda():
    rng = np.random.default_rng(1)
    K, red = 8, 0
    R = 200
    for t in range(R):
        X = _sim(K, rng, lambda i, j: rng.normal())
        Y = _sim(K, rng, lambda i, j: rng.normal())
        red += GK.mantel(X, Y, perm=199, tohum=t)["p_tek"] < 0.05
    assert red / R < 0.10, red / R


def test_mantel_ortak_etiket_permutasyonuna_degismez():
    rng = np.random.default_rng(2)
    K = 9
    X = _sim(K, rng, lambda i, j: rng.normal())
    Y = _sim(K, rng, lambda i, j: rng.normal())
    p = rng.permutation(K)
    a = GK.mantel(X, Y, perm=10)["istatistik"]
    b = GK.mantel(X[np.ix_(p, p)], Y[np.ix_(p, p)], perm=10)["istatistik"]
    assert abs(a - b) < 1e-12


def test_ana_etki_artigi_toplamsal_matrisi_sifirlar():
    rng = np.random.default_rng(3)
    K = 7
    a = rng.normal(size=K)
    A = 0.3 + a[:, None] + a[None, :]
    np.fill_diagonal(A, 0)
    assert np.abs(GK.ana_etki_artik(A)).max() < 1e-10


def test_ana_etki_karistiricisi_ham_mantelde_var_artikta_yok():
    """Iki matris yalniz ortak model ana etkisi tasiyorsa (or. gurbuzluk duzeyi) ham Mantel anlamli,
    ana etki artigi ve kismi Mantel anlamsiz olmalidir (hakemin E3 itirazinin sinamasi)."""
    rng = np.random.default_rng(4)
    K = 14
    s = rng.normal(size=K)
    X = _sim(K, rng, lambda i, j: s[i] + s[j] + 0.3 * rng.normal())
    Y = _sim(K, rng, lambda i, j: s[i] + s[j] + 0.3 * rng.normal())
    ham = GK.mantel(X, Y, perm=999)
    art = GK.mantel(GK.ana_etki_artik(X), GK.ana_etki_artik(Y), perm=999)
    kis = GK.mantel(X, Y, [s[:, None] + s[None, :]], perm=999)
    assert ham["p_tek"] < 0.01
    assert art["p_tek"] > 0.05 and kis["p_tek"] > 0.05, (art, kis)


def test_ana_etki_artigi_cift_duzeyi_iliskiyi_korur():
    rng = np.random.default_rng(5)
    K = 14
    s = rng.normal(size=K)
    z = rng.normal(size=(K, 2))
    D = np.linalg.norm(z[:, None] - z[None], axis=2)
    X = _sim(K, rng, lambda i, j: s[i] + s[j] - D[i, j] + 0.1 * rng.normal())
    Y = _sim(K, rng, lambda i, j: 2 * s[i] + 2 * s[j] - D[i, j] + 0.1 * rng.normal())
    art = GK.mantel(GK.ana_etki_artik(X), GK.ana_etki_artik(Y), perm=999)
    assert art["p_tek"] < 0.01


def test_mantel_K_kucukse_tanimsiz():
    assert "not" in GK.mantel(np.eye(3), np.eye(3), perm=5)


# ---------------------------------------------------------------------------- gradyan kosinusu
def test_girdi_gradyani_dogrusal_modelde_analitik_degere_esit():
    import torch

    torch.manual_seed(0)
    lin = torch.nn.Sequential(torch.nn.Flatten(), torch.nn.Linear(12, 5))
    x = torch.rand(6, 3, 2, 2)
    y = torch.randint(0, 5, (6,))
    g = GK.girdi_gradyani(lin, x, y)
    W = lin[1].weight.detach()
    p = torch.softmax(lin(x), 1).detach()
    e = torch.nn.functional.one_hot(y, 5).float()
    assert torch.allclose(g, (p - e) @ W, atol=1e-6)


def test_cift_kosinus_ozdes_ve_ters_model():
    import torch

    torch.manual_seed(1)
    G1 = torch.randn(4, 30)
    G = torch.stack([G1, G1 * 3.0, -G1, torch.zeros_like(G1)])
    c, nr = GK.cift_kosinus(G)
    pairs = list(combinations(range(4), 2))
    assert torch.allclose(c[:, pairs.index((0, 1))], torch.ones(4), atol=1e-6)
    assert torch.allclose(c[:, pairs.index((0, 2))], -torch.ones(4), atol=1e-6)
    assert torch.isnan(c[:, pairs.index((0, 3))]).all()
    assert torch.allclose(nr[1], 3 * nr[0])


# ---------------------------------------------------------------------------- dondurulmus betik
def test_dondurulmus_betik_sha_denetimi_degisiklikte_durur(tmp_path):
    kopya = tmp_path / "q1_konsey_ayrisim.py"
    shutil.copy(EK.DONDURULMUS, kopya)
    with open(kopya, "a") as f:
        f.write("\n# degisiklik\n")
    eski = EK._DM
    EK._DM = None
    try:
        with pytest.raises(SystemExit):
            EK.dondurulmus(yol=kopya)
    finally:
        EK._DM = eski
    assert EK.sha256(EK.DONDURULMUS) == EK.DONDURULMUS_SHA


def _sahte_matris(dizin, adlar, n=400, tohum=0, guc=None):
    """Hedef-dogru gostergeleri tasiyan sahte per_sample npz klasoru (ozgun sema)."""
    rng = np.random.default_rng(tohum)
    dizin.mkdir(parents=True, exist_ok=True)
    tc = {m: rng.random(n) < 0.8 for m in adlar}
    guc = guc or {m: 0.3 + 0.4 * rng.random() for m in adlar}
    sa = {}
    for s in adlar:
        for t in adlar:
            p = guc[s] if s == t else guc[s] * guc[t]
            aw = rng.random(n) < p
            if s == t:
                sa[s] = aw
    for s in adlar:
        for t in adlar:
            p = guc[s] if s == t else 0.5 * guc[s] * (0.5 + guc[t])
            aw = sa[s] if s == t else rng.random(n) < p
            np.savez(dizin / f"per_sample_{s}_to_{t}.npz", target_clean_correct=tc[t], target_adv_wrong=aw,
                     source_clean_correct=tc[s], source_adv_wrong=sa[s])
    (dizin / "transfer_matrix.json").write_text(json.dumps({"models": adlar}))
    return tc


def test_log_tau_matrisi_formulle_ayni(tmp_path):
    adlar = ["A", "B", "C", "D", "E"]
    d = tmp_path / "m"
    _sahte_matris(d, adlar)
    var, T, om, M = GK.log_tau_matrisi([str(d)], adlar)
    assert var == adlar

    def oran(s, t, alt):
        z = np.load(d / f"per_sample_{s}_to_{t}.npz")
        idx = np.arange(len(z["target_clean_correct"]))
        m = {"tam": np.ones_like(idx, bool), "cift": idx % 2 == 0, "tek": idx % 2 == 1}[alt]
        tc, aw = z["target_clean_correct"][m], z["target_adv_wrong"][m]
        return 100.0 * aw[tc].mean()

    for a, b in combinations(range(5), 2):
        i, j = adlar[a], adlar[b]
        v = []
        for wa, Ta in (("cift", "tek"), ("tek", "cift")):
            v.append(0.5 * (math.log(oran(i, j, Ta)) + math.log(oran(j, i, Ta))
                            - math.log(oran(i, i, wa)) - math.log(oran(j, j, wa))))
        assert abs(T[a, b] - np.mean(v)) < 1e-12
    assert abs(om[0] - math.log(oran("A", "A", "tam"))) < 1e-12


def test_mantel_kos_uctan_uca(tmp_path):
    adlar = [f"M{k}" for k in range(6)]
    d = tmp_path / "m"
    _sahte_matris(d, adlar, n=300, tohum=7)
    rng = np.random.default_rng(8)
    C = np.eye(6) + _sim(6, rng, lambda i, j: rng.random())
    oz = {"modeller": adlar, "c_tum": C.tolist(), "c_iki_model_dogru": C.tolist(),
          "log_gradyan_normu_ort": {m: 0.0 for m in adlar}}
    kp = tmp_path / "kosinus_ozet.json"
    kp.write_text(json.dumps(oz))
    out = GK.main(["mantel", "--kosinus", str(kp), "--matris-dizini", str(d), "--veri-kumesi", "sahte",
                   "--perm", "50", "--sinama", "--cikti", str(tmp_path / "mantel.json")])
    assert np.isfinite(out["sinamalar"]["ham"]["istatistik"])
    assert out["SINAMA_SONUC_DEGIL"] and set(out["sinamalar"]) == {"ham", "ana_etki_artik", "kismi_omega",
                                                                      "kismi_omega_gradnorm"}


# ---------------------------------------------------------------------------- B8 / B9 sarmalayici
def _tablo_b9(yol, R, V, P):
    mod = {}
    for k, r in enumerate(R):
        mod[r] = {"hucre": "C1-R32", "tohum": 1001 + k, "aile": "CNN", "birincil_panel": False, "ikincil_panel": False}
    for k, v in enumerate(V):
        mod[v] = {"hucre": "V-scr", "tohum": 2001 + k, "aile": "ViT", "birincil_panel": False, "ikincil_panel": False}
    for p in P:
        mod[p] = {"hucre": "panel", "tohum": None, "aile": "CNN", "birincil_panel": True, "ikincil_panel": False}
    yol.write_text(json.dumps({"modeller": mod, "b2_tohum_ciftleri": [[r, v] for r, v in zip(R, V)]}))


def test_b9_dondurulmus_b2_yolunu_cagirir(tmp_path):
    R, V, P = ["R1", "R2", "R3"], ["V1", "V2", "V3"], ["P1", "P2", "P3", "P4", "P5"]
    d = tmp_path / "m"
    _sahte_matris(d, R + V + P, n=300, tohum=11)
    tb = tmp_path / "t.json"
    _tablo_b9(tb, R, V, P)
    cikti = tmp_path / "b9.json"
    yan = EK.main(["--mod", "b9", "--matris-dizini", str(d), "--hucre-tablosu", str(tb), "--cikti", str(cikti),
                   "--bootstrap", "50", "--sinama"])
    sonuc = json.loads(cikti.read_text())
    assert sonuc["meta"]["betik_sha256"] == EK.DONDURULMUS_SHA
    assert sonuc["SINAMA_SONUC_DEGIL"] and "F_B2" in sonuc["b2"]
    assert yan["meta"]["dondurulmus_cikti_sha256"] == EK.sha256(cikti)
    assert set(yan["temiz_dogruluk_yuzde"]) == set(R + V + P)


def test_b8_betimsel_A_sigma_dondurulmus_islevlerle_tutarli(tmp_path):
    P = [f"P{k}" for k in range(6)]
    C, T = ["C1", "C2", "C3"], ["T1", "T2", "T3"]
    d = tmp_path / "m"
    _sahte_matris(d, P + C + T, n=400, tohum=13)
    mod = {p: {"hucre": "panel", "tohum": None, "birincil_panel": True, "ikincil_panel": False} for p in P}
    for k in range(3):
        mod[C[k]] = {"hucre": "C1-R32", "tohum": k + 1, "birincil_panel": False, "ikincil_panel": False}
        mod[T[k]] = {"hucre": "V-scr", "tohum": k + 1, "birincil_panel": False, "ikincil_panel": False}
    tb = tmp_path / "t8.json"
    tb.write_text(json.dumps({"modeller": mod, "b2_tohum_ciftleri": [[C[k], T[k]] for k in range(3)]}))
    out = EK.main(["--mod", "b8", "--matris-dizini", str(d), "--hucre-tablosu", str(tb),
                   "--cikti", str(tmp_path / "b8.json"), "--bootstrap", "60", "--sinama"])
    dm = EK.dondurulmus()
    M = EK.matris_yukle([str(d)])
    g = dm.Alici(M)
    bek = [dm.model_duzeyi(g, T[k], P)["sigma"] - dm.model_duzeyi(g, C[k], P)["sigma"] for k in range(3)]
    for k, c in enumerate(out["ciftler"]):
        assert abs(c["A_sigma"] - bek[k]) < 1e-12
        assert c["goruntu_bootstrap_ci90"][0] <= c["goruntu_bootstrap_ci90"][1]
    A = out["A_sigma_IN"]
    assert A["ciftler"] == [1, 2] and abs(A["kestirim"] - (bek[0] + bek[1]) / 2) < 1e-12
    assert abs(A["iki_cift_farki"] - (bek[1] - bek[0])) < 1e-12 and "t_araligi_ciftler_uzerinden" not in A
    assert A["goruntu_bootstrap"]["tohum"] == 20261030 and A["betimsel_etiket"] in (
        "IN satirinda ihmal edilebilir mimari farki", "beklentiyle uyumlu", "ters yon", "belirsiz")
    assert out["A_sigma_scr_Liu"]["ciftler"] == [3] and out["A_sigma_scr_Liu"]["beklenti_esigi"] == -0.20


def test_b8_etiket_kurallari():
    f = EK.b8_etiket
    assert f(-0.02, [-0.05, 0.03], [-0.06, 0.04], [-0.01, -0.03], -0.10, 0.10).startswith("IN satirinda ihmal")
    assert f(-0.30, [-0.45, -0.15], [-0.5, -0.1], [-0.2, -0.4], -0.10, 0.10) == "beklentiyle uyumlu"
    assert f(-0.30, [-0.45, -0.15], [-0.5, -0.1], [0.1, -0.7], -0.10, 0.10) == "belirsiz"
    assert f(0.30, [0.15, 0.45], [0.1, 0.5], [0.2, 0.4], -0.10, 0.10) == "ters yon"


def test_b10_aile_alti_sinama_ve_kurallar(tmp_path):
    yollar = []
    for k, (r, p) in enumerate([(0.6, 0.0001), (0.1, 0.5), (0.35, 0.03)]):
        d = {"veri_kumesi": f"vk{k}", "sinamalar": {"ham": {"istatistik": r, "p_tek": p, "perm": 9999},
                                                     "ana_etki_artik": {"istatistik": r / 2, "p_tek": min(1, p * 4), "perm": 9999}}}
        y = tmp_path / f"m{k}.json"
        y.write_text(json.dumps(d))
        yollar.append(str(y))
    out = EK.main(["--mod", "b10", "--mantel", *yollar, "--cikti", str(tmp_path / "b10.json"), "--sinama"])
    s = {x["sinama"]: x for x in out["F_B10"]["sinamalar"]}
    assert out["F_B10"]["aile_buyuklugu"] == 6 and "perm_uyarisi" not in out["F_B10"]
    assert s["H10-vk0"]["karar"] == "destek" and s["H10-vk1"]["karar"] == "curutuldu"
    assert s["H10-vk2"]["karar"] == "kararsiz"
    assert abs(s["H10-vk0"]["p_holm"] - 0.0006) < 1e-12


# ---------------------------------------------------------------------------- ImageNetV2 yukleyici
@pytest.fixture(scope="module")
def sahte_v2():
    from PIL import Image

    kok = Path(tempfile.mkdtemp()) / "imagenetv2"
    ic = kok / "imagenetv2-matched-frequency-format-val"
    rng = np.random.default_rng(0)
    for c in range(1000):
        (ic / str(c)).mkdir(parents=True)
        for k in range(2):
            arr = (rng.random((20, 24, 3)) * 255).astype(np.uint8)
            Image.fromarray(arr).save(ic / str(c) / f"{k:02d}{c:04d}.jpeg")
    yield kok
    shutil.rmtree(kok.parent)


def test_v2_secim_sinif_sirali_ve_belirlenimci(sahte_v2):
    TM = _mod("q1_ek_transfer_matrix", "q1_ek_transfer_matrix.py")
    kok, s = TM.v2_secim(sahte_v2, 2000, sinif_dosya=2)
    assert len(s) == 2000 and [y for _, y in s[:4]] == [0, 0, 1, 1]
    assert s[0][0] == "0/000000.jpeg" and s[1][0] == "0/010000.jpeg"
    # bolunmus yari: her yariya sinif basina bir goruntu
    ys = np.array([y for _, y in s])
    assert (np.bincount(ys[0::2], minlength=1000) == 1).all() and (np.bincount(ys[1::2], minlength=1000) == 1).all()
    _, s2 = TM.v2_secim(sahte_v2, 2000)
    assert s == s2
    with pytest.raises(SystemExit):
        TM.v2_secim(sahte_v2, 2000, sinif_dosya=10)


def test_v2_loader_robustbench_onislemesiyle_ayni(sahte_v2):
    import torch
    from PIL import Image
    from robustbench.data import PREPROCESSINGS

    TM = _mod("q1_ek_transfer_matrix", "q1_ek_transfer_matrix.py")
    (_, ld), man = TM.v2_loaders(sahte_v2, 6, 4, "Res256Crop224")
    x, y = next(iter(ld))
    assert tuple(x.shape) == (4, 3, 224, 224) and float(x.min()) >= 0 and float(x.max()) <= 1
    kok = TM._v2_goruntu_koku(sahte_v2)
    ref = PREPROCESSINGS["Res256Crop224"](Image.open(kok / man["dosyalar"][0]["yol"]).convert("RGB"))
    assert torch.equal(x[0], ref)
    assert man["n"] == 6 and len(man["liste_sha256"]) == 64


def test_f16_onbellek_geri_kurulumu_yaricap_icinde():
    import torch

    torch.manual_seed(0)
    eps = 4 / 255
    x = torch.rand(8, 3, 16, 16)
    adv = torch.clamp(x + torch.empty_like(x).uniform_(-eps, eps), 0, 1)
    d = (adv - x).to(torch.float16)
    rec = torch.clamp(x + torch.clamp(d.float(), -eps, eps), 0, 1)
    assert float((rec - x).abs().max()) <= eps + 1e-7
    assert float((rec - adv).abs().max()) < 2e-5
    assert float(rec.min()) >= 0 and float(rec.max()) <= 1



# ---------------------------------------------------------------------------- ek on kayitla uyum
def _argparse_varsayilan(dosya, bayrak):
    """Betigin kaynak kodundan add_argument(bayrak, default=...) degerini okur (main calistirilmaz)."""
    import ast

    agac = ast.parse((KOK / "experiments" / dosya).read_text(encoding="utf-8"))
    for d in ast.walk(agac):
        if (isinstance(d, ast.Call) and getattr(d.func, "attr", None) == "add_argument" and d.args
                and isinstance(d.args[0], ast.Constant) and d.args[0].value == bayrak):
            for k in d.keywords:
                if k.arg == "default":
                    return ast.literal_eval(k.value) if not isinstance(k.value, ast.Name) else k.value.id
    raise AssertionError(f"{dosya}: {bayrak} bulunamadi")


def test_varsayilanlar_ek_on_kayitla_uyumlu():
    """ON_KAYIT_EK_B8_B10_2026-10-30.md: §6.2 9999 permutasyon ve tohum 20261030; §5.2 bicubic ortak hat;
    §5.6 IN satiri Singh ciftleri (1, 2), Liu (3) ayri scr satiri; §6.2 F_B10 alti sinama (ayri sinamada)."""
    import inspect

    assert GK.PERM_VARSAYILAN == 9999 and GK.TOHUM == 20261030
    assert inspect.signature(GK.mantel).parameters["perm"].default == 9999
    assert _argparse_varsayilan("q1_ek_gradyan_kosinus.py", "--perm") == "PERM_VARSAYILAN"
    assert _argparse_varsayilan("q1_ek_transfer_matrix.py", "--in-onisleme") == "BicubicRes256Crop224"
    assert _argparse_varsayilan("q1_ek_gradyan_kosinus.py", "--in-onisleme") == "BicubicRes256Crop224"
    assert _argparse_varsayilan("q1_ek_ayrisim.py", "--in-ciftleri") == [1, 2]
    assert _argparse_varsayilan("q1_ek_ayrisim.py", "--scr-ciftleri") == [3]
    assert _argparse_varsayilan("q1_ek_ayrisim.py", "--bootstrap") == 2000
    assert _argparse_varsayilan("q1_ek_ayrisim.py", "--bootstrap-tohum") == 20261030
    assert EK.BEKLENTI_A_SIGMA_IN == -0.10


def test_v2_loader_bicubic_robustbench_tanimiyla_ayni(sahte_v2):
    import torch
    from PIL import Image
    from robustbench.data import PREPROCESSINGS

    TM = _mod("q1_ek_transfer_matrix", "q1_ek_transfer_matrix.py")
    (_, ld), man = TM.v2_loaders(sahte_v2, 4, 4, "BicubicRes256Crop224")
    x, _ = next(iter(ld))
    kok = TM._v2_goruntu_koku(sahte_v2)
    im = Image.open(kok / man["dosyalar"][0]["yol"]).convert("RGB")
    assert torch.equal(x[0], PREPROCESSINGS["BicubicRes256Crop224"](im))
    assert not torch.equal(x[0], PREPROCESSINGS["Res256Crop224"](im))  # hat gercekten bicubic
    assert man["onisleme"] == "BicubicRes256Crop224"


def test_onisleme_denetimi_esikleri_ek_5_5():
    """Ek on kayit §5.5: (i) kendi >= %25 ve >= 0,6 x RobustBench temiz; (ii) |fark| <= 5; 3-5 isaretli."""
    TM = _mod("q1_ek_transfer_matrix", "q1_ek_transfer_matrix.py")
    assert (TM.DEN_ALT_SINIR, TM.DEN_RB_KAT, TM.DEN_FARK_EN_COK, TM.DEN_FARK_ISARET) == (25.0, 0.6, 5.0, 3.0)
    rb = TM.RB_IN_TEMIZ["Salman2020Do_R18"]
    assert rb == 52.92 and round(TM.DEN_RB_KAT * rb, 2) == 31.75  # ek §5.5: en zayif uye icin esik 31,75
    k = TM.denetim_karari
    assert k(31.80, 31.80, rb)["karar"] == "gecti"
    assert k(31.70, 31.70, rb)["karar"] == "kaldi"            # 0,6 kat esigi
    assert k(24.90, 24.90, None)["karar"] == "kaldi"          # %25 alt siniri
    assert k(25.00, 25.00, None)["karar"] == "gecti"
    assert k(60.0, 57.0, 70.0)["karar"] == "gecti"            # fark tam 3: isaretsiz
    assert k(60.0, 56.0, 70.0)["karar"] == "gecti_isaretli"   # 3 < fark <= 5
    assert k(60.0, 55.0, 70.0)["karar"] == "gecti_isaretli"   # fark tam 5
    assert k(60.0, 54.9, 70.0)["karar"] == "kaldi"            # fark > 5
    assert k(55.0, 60.5, 70.0)["karar"] == "kaldi"            # mutlak fark (ortak daha iyi de olsa)
    assert k(None, 50.0, 70.0)["karar"] == "hesaplanamadi"
    assert len(TM.RB_IN_TEMIZ) == 15


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q", "-p", "no:cacheprovider"]))
