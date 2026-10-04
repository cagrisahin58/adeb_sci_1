"""Makaledeki tasiyici sayilarin artefaktlarla tutarliligini denetler.

Her kontrol: (aciklama, artefaktdan hesaplanan deger, metinde gecmesi beklenen dize).
Metinde bulunamayan veya artefaktla uyusmayan her sey RAPOR EDILIR.

IKI DIL: EN (paper/manuscript) ve TR (paper/manuscript_tr) AYRI AYRI denetlenir.
DIKKAT -- `{,}` makrosu iki dilde FARKLI anlama gelir:
  EN : binlik ayraci   ->  10{,}000  = 10000   => "{,}" SILINIR
  TR : ondalik ayraci  ->  10{,}45   = 10.45   => "{,}" NOKTAYA cevrilir
Ayni normalleştirmeyi iki dile uygulamak sessiz "EKSIK" raporlari uretir.
"""
import json
import re
from pathlib import Path

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"

EN_FILES = ["main.tex", "sections/01_introduction.tex", "sections/02_related_work.tex",
            "sections/03_methodology.tex", "sections/04_experiments.tex",
            "sections/05_discussion.tex", "sections/06_conclusion.tex"]
TR_FILES = ["main.tex", "sections/01_giris.tex", "sections/02_ilgili_calismalar.tex",
            "sections/03_yontem.tex", "sections/04_deneyler.tex",
            "sections/05_tartisma.tex", "sections/06_sonuc.tex"]


def read_lang(base, files):
    parts = []
    for p in files:
        f = ROOT / base / p
        if f.exists():
            parts.append(f.read_text(encoding="utf-8"))
    return "\n".join(parts)


def norm_en(t):
    # EN: {,} binlik ayracidir -> sil. Sonra kalan virgulleri de sil.
    return t.replace("{,}", "").replace(",", "")


def norm_tr(t):
    # TR ondalik ayraci IKI bicimde yaziliyor ve IKISI DE GECERLI:
    #   $13{,}57$ -> matematik kipinde zorunlu ({,} bosluk sorununu onler)
    #   0,0378    -> METIN kipinde (tablo hucreleri) dogru Turkce yazim
    # Denetleyici ikisini de tanimak zorunda; aksi halde dogru sayilari
    # "TR'de eksik" diye raporlar (bu hata bir kez yapildi).
    # Sira onemli: once binlik ayraci ("10.000"), sonra {,}, sonra ciplak virgul.
    t = re.sub(r"(?<=\d)\.(?=\d{3}(?!\d))", "", t)
    t = t.replace("{,}", ".")
    return re.sub(r"(?<=\d),(?=\d)", ".", t)


LANGS = {
    "EN": norm_en(read_lang("paper/manuscript", EN_FILES)),
    "TR": norm_tr(read_lang("paper/manuscript_tr", TR_FILES)),
}


def jl(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


seed = jl("results/c1_seeds/c1_seed_summary.json")["aggregate"]
tr = jl("results/c1_transfer/c1_transfer_summary.json")
c3 = jl("results/c1_c3/c3_summary.json")
beh = jl("results/c1_behavior_summary.json")
c45 = jl("results/c1_c45_summary.json")
c2 = [jl(f"results/c1_c2/pair{p}/tgr_summary.json") for p in (1, 2, 3)]
vr = jl("results/q1/variance_ratio.json")
c3p = jl("results/q1/c3_precision.json")
e3s = jl("results/q1/e3_surucu_ayristirma.json")
e7 = jl("results/q1/e7_svhn_summary.json")
e7t = jl("results/q1/svhn/transfer/e7_transfer_summary.json")
e3f = jl("results/q1/e3_iki_kol_fit.json")
b8 = jl("results/q1/b8_secim_bandi.json")
e6 = jl("results/q1/cifar10_l2/e6_aa_l2_summary.json")
e6t = jl("results/q1/cifar10_l2/transfer/e6_l2_transfer_summary.json")
e6o = jl("results/q1/cifar10_l2/e6_onkestirim.json")
e1 = jl("results/q1/e1_cifar100_summary.json")
e1t = jl("results/q1/cifar100/transfer/e1_transfer_summary.json")
e2g = jl("results/q1/e2/e2_grid.json")
a2b = [jl(f"results/q1/cifar100/transfer/pair{p}/a2b_class_balance_cifar100.json")
       for p in (1, 2, 3)]


def ms(v):
    a = np.asarray(v, dtype=float)
    return a.mean(), a.std(ddof=1)


CHECKS = []


def chk(label, value, nd=2):
    CHECKS.append((label, f"{value:.{nd}f}"))


# --- mevcut kontroller (C1) ---
chk("AA ResNet", seed["resnet"]["aa"]["mean"])
chk("AA ViT", seed["vit"]["aa"]["mean"])
chk("kos. yaniltma PGD ResNet", seed["resnet"]["cond_fooling_pgd"]["mean"])
chk("kos. yaniltma PGD ViT", seed["vit"]["cond_fooling_pgd"]["mean"])
chk("kos. yaniltma AA ResNet", seed["resnet"]["cond_fooling_aa"]["mean"])
chk("kos. yaniltma AA ViT", seed["vit"]["cond_fooling_aa"]["mean"])
chk("hedef-dogru fark", tr["protocols"]["target_correct"]["diff"]["mean"])
chk("her-ikisi-dogru fark", tr["protocols"]["both_correct"]["diff"]["mean"])
chk("basarili-kaynak fark", tr["protocols"]["successful_source"]["diff"]["mean"])
chk("protokol yayilimi", tr["protocol_spread_pp"]["mean"])
chk("C3 r", c3["raw_minus_cond_vs_target_error"]["pearson_r"], 3)
chk("C3 gelen-transfer r", c3["incoming_transfer_vs_own_vulnerability"]["pearson_r"], 3)
# --- YENI (2026-08-20, IS-1 nitelemesi): kesinlik nitelemesinin tasidigi sayilar.
# r = 0,997 alti KOSEGEN-DISI yonden gelir ama o alti yon yalniz UC HEDEFTEN;
# metin artik hedef duzeyi degeri de veriyor. Ikisi de denetlenmeli (K1).
chk("C3 egim (0,762)", c3["raw_minus_cond_vs_target_error"]["slope"], 3)
# NOT: hedef-duzeyi r (0,9985) kontrolu KALDIRILDI. §4.2.1 artik iliskiyi
# korelasyon olarak degil OZDESLIK olarak sunuyor; o sayi metinde yok.
# Yerine ozdesligin TASIYICI sayilari denetleniyor.
_oz = jl("results/q1/ozdeslik_kontrol.json")["ozet"]
chk("ozdeslik P(aw|cw) min", _oz["P_advyanlis_verili_temizyanlis"]["min"], 3)
chk("ozdeslik P(aw|cw) max", _oz["P_advyanlis_verili_temizyanlis"]["max"], 3)
chk("ozdeslik artik max (puan)", _oz["ARTIK_puan"]["mutlak_max"], 2)
chk("ozdeslik artik ort (puan)", _oz["ARTIK_puan"]["mutlak_ort"], 3)
chk("ozdeslik artik/sapma max %", _oz["artigin_sapmaya_orani_yuzde"]["max"], 2)
chk("Hoyer ResNet", beh["gradient"]["ResNet18_AT"]["sparsity_hoyer"]["mean"], 4)
chk("Hoyer ViT", beh["gradient"]["ViT_Tiny_AT"]["sparsity_hoyer"]["mean"], 4)
chk("alan50 ResNet", c45["spatial"]["energy_area_50pct"]["resnet"][0], 4)
chk("alan50 ViT", c45["spatial"]["energy_area_50pct"]["vit"][0], 4)
chk("TGR hedef-dogru", ms([d["tgr"]["transfer_target_correct"] for d in c2])[0])
chk("MI hedef-dogru", ms([d["mi"]["transfer_target_correct"] for d in c2])[0])
chk("ResNet layer4.0 kosinus", c45["resnet_drift"]["layer4.0"]["cos"][0], 4)

# --- YENI: varyans siralamasi sayilari (2026-08-17 "yirmi kat" duzeltmesi) ---
# Bu sayilar duzeltme sirasinda metne girdi ve o zamana kadar HICBIRI
# denetlenmiyordu; drift'i tam burada yakalamak gerekiyor.
pay = vr["PAY_protokol_etkisi"]
payda = vr["PAYDA_kosum_etkisi_AYNI_NICELIK"]
# NOT: protokol etkisi sd (4,82) metinde ANILMIYOR (yeniden yazimda cikarildi),
# bu yuzden kontrol edilmez. Artefaktta durur: variance_ratio.json.
chk("protokol ort. acikligi (10,24)", vr["PAY_10_45_vs_10_24"]["protokol_ortalamalari_acikligi"])
chk("kosum sd min (0,23)", payda["sd_min"])
chk("kosum sd max (1,48)", payda["sd_max"])
chk("oran alt (3,3)", vr["ORAN_ACIKLIGI"]["min"], 1)
chk("oran ust (22,7)", vr["ORAN_ACIKLIGI"]["max"], 1)
chk("benzeri-benzeriyle oran (20,9)",
    vr["ORAN_TANIMA_DUYARLI"]["sd_vs_sd"]["degerler"]["both_correct"], 1)
# tablo Fark sutunu sd'leri
for prot, lbl in [("raw", "ham"), ("target_correct", "hedef-dogru"),
                  ("both_correct", "her-ikisi-dogru"), ("successful_source", "basarili-kaynak")]:
    chk(f"tablo Fark sd {lbl}", payda["sd_protokol_bazli"][prot])

# --- YENI (2026-08-20, IS-2): E1 (CIFAR-100) + E2 (ckpt secimi) ---
# Bu sayilar makaleye bu oturumda girdi; hicbiri denetlenmiyordu.
for arch, lbl in (("resnet18", "ResNet"), ("vit_tiny", "ViT")):
    o = e1["mimariler"][arch]["ozet"]
    chk(f"E1 temiz {lbl}", o["test_clean"]["ort"])
    chk(f"E1 PGD {lbl}", o["test_pgd10"]["ort"])
    chk(f"E1 AA {lbl}", o["test_autoattack"]["ort"])
for prot, lbl in (("raw", "ham"), ("target_correct", "hedef-dogru"),
                  ("both_correct", "her-ikisi-dogru"), ("successful_source", "basarili-kaynak")):
    chk(f"E1 fark {lbl}", e1t["protocols"][prot]["diff"]["mean"])
chk("E1 protokol yayilimi (13,58)", e1t["protocol_spread_pp"]["mean"])
# CIFAR-100 karistirici: egim ve iki r degeri (kesinlik nitelemesiyle birlikte)
_c100 = c3p["veri_kumeleri"]["cifar100"]
chk("E1 karistirici egim (0,656)", _c100["RAPOR_EDILEN_n6"]["egim"], 3)
chk("E1 karistirici r n=6 (0,931)", _c100["RAPOR_EDILEN_n6"]["pearson_r"], 3)
chk("E1 karistirici r n=3 (0,974)", _c100["HEDEF_DUZEYI_n3"]["pearson_r"], 3)
# hedef temiz hatalarinin CAKISMASI: ucuncu on-kestirimin neden sinanamadigi
chk("E1 cakisik hedef hatasi A", sorted(_c100["hedef_temiz_hatasi"])[0])
chk("E1 cakisik hedef hatasi B", sorted(_c100["hedef_temiz_hatasi"])[1])
# sinif bilesimi: hedef-dogru protokolunde uc tohumun bilesim etkisi
for i, d in enumerate(a2b, start=1):
    chk(f"E1 bilesim etkisi t{i}", d["protokoller"]["target_correct"]["AYRISTIRMA"]["bilesim_etkisi"], 3)
# E2 secim protokolu yayilimi -- MUTLAK, oran DEGIL (K2)
for arch, lbl in (("resnet18", "ResNet"), ("vit_tiny", "ViT")):
    lo, hi = e2g["mimariler"][arch]["protokol_yayilim_araligi"]
    chk(f"E2 secim yayilimi alt {lbl}", lo)
    chk(f"E2 secim yayilimi ust {lbl}", hi)
# E2 oran DUYARLILIGI (mansette degil, govdede): referans secimine bagli aralik
for arch, lbl in (("resnet18", "ResNet"), ("vit_tiny", "ViT")):
    rd = e2g["mimariler"][arch]["REFERANS_DUYARLILIGI"]
    chk(f"E2 oran alt {lbl}", rd["oran_min"], 2)
    chk(f"E2 oran ust {lbl}", rd["oran_max"], 2)
# E2 karsi-agirligi: secim YOLU oynak, SONUC degil
chk("E2 karsi-agirlik epok acikligi",
    e1["mimariler"]["resnet18"]["ozet"]["en_iyi_epok"]["aciklik"], 0)
chk("E2 karsi-agirlik test sd", e1["mimariler"]["resnet18"]["ozet"]["test_pgd10"]["sd"])

# --- YENI (2026-08-21, E3): protokol yayiliminin IKI surucusu ---
# 4 protokol yayilimi ciftin temiz hata farkiyla AZALIYOR, basarili-kaynak
# cikarilinca ARTIYOR. Isareti ceviren tek protokol odur.
_A, _B = e3s["A_dort_protokol"], e3s["B_basarili_kaynak_HARIC"]
chk("E3 4-protokol egim", abs(_A["egim"]), 3)
chk("E3 4-protokol GA alt", abs(_A["egim_GA95"][0]), 3)
chk("E3 4-protokol GA ust", abs(_A["egim_GA95"][1]), 3)
chk("E3 3-protokol egim", _B["egim"], 3)
chk("E3 3-protokol GA alt", _B["egim_GA95"][0], 3)
chk("E3 3-protokol GA ust", _B["egim_GA95"][1], 3)
chk("E3 en genis protokol cifti",
    e3s["protokol_cifti_ortalama_aciklik"]["target_correct vs successful_source"]["ort_aciklik"])

# --- YENI (2026-08-21): E7 (SVHN) mutlak + protokol sayilari ---
for arch, lbl in (("resnet18", "ResNet"), ("vit_tiny", "ViT")):
    o = e7["mimariler"][arch]["ozet"]
    chk(f"E7 temiz {lbl}", o["test_clean"]["ort"])
    chk(f"E7 temiz sd {lbl}", o["test_clean"]["sd"])
    chk(f"E7 PGD {lbl}", o["test_pgd10"]["ort"])
_prot = e7t["protocols"]
# 2026-10-04 (hakem paneli, mercek D Y1/Y9): Tablo 6 yerine protokol x ayar table*
# (tab:protocol_settings). SVHN'de iki cift AYRI AYRI basilir (SD yok), yon bazinda
# oranlar artik tabloda degil; fark ortalamalari metinde kalir.
_PROTS = (("raw", "ham"), ("target_correct", "hedef-dogru"),
          ("both_correct", "her-ikisi-dogru"), ("successful_source", "basarili-kaynak"))
for p, lbl in _PROTS:
    chk(f"E7 {lbl} fark", abs(_prot[p]["diff"]["mean"]))
    for k, v in enumerate(_prot[p]["diff"]["values"], 1):
        chk(f"E7 {lbl} fark cift{k}", abs(v))
chk("E7 protokol yayilimi", e7t["protocol_spread_pp"]["mean"])
for k, v in enumerate(e7t["protocol_spread_pp"]["values"], 1):
    chk(f"E7 yayilim cift{k}", v)
# Ayni tablonun CIFAR-100 ve L2 sutunlari: fark ort, SD ve yayilim
e1t = jl("results/q1/cifar100/transfer/e1_transfer_summary.json")
for tag, d in (("E1", e1t), ("E6", e6t)):
    for p, lbl in _PROTS:
        chk(f"{tag} {lbl} fark", abs(d["protocols"][p]["diff"]["mean"]))
        chk(f"{tag} {lbl} fark sd", d["protocols"][p]["diff"]["std"])
    chk(f"{tag} protokol yayilimi", d["protocol_spread_pp"]["mean"])
    chk(f"{tag} yayilim sd", d["protocol_spread_pp"]["std"])
_bcp = e7t["both_correct_paired"]
chk("E7 esli GA alt", abs(_bcp["ci_low"]["mean"]))
chk("E7 esli GA ust", _bcp["ci_high"]["mean"])
chk("E7 permutasyon p", _bcp["perm_p_max"], 3)

# --- E3 iki kol nihai egimleri ---
_A = e3f["kollar"]["A"]
_B = e3f["kollar"]["B"]
_Ba = e3f["kollar"]["B_ana_cift"]
for ad, blok, ek in (("A 4prot", _A["dort_protokol"], ""), ("A 3prot", _A["uc_protokol_bas_kaynak_haric"], ""),
                     ("B 4prot", _B["dort_protokol"], ""), ("B 3prot", _B["uc_protokol_bas_kaynak_haric"], ""),
                     ("Bana 4prot", _Ba["dort_protokol"], "")):
    chk(f"E3 {ad} egim", abs(blok["egim"]), 3)
    chk(f"E3 {ad} GA alt", abs(blok["egim_GA95"][0]), 3)
    chk(f"E3 {ad} GA ust", abs(blok["egim_GA95"][1]), 3)
chk("E3 A kolu nokta sayisi", _A["n_nokta"], 0)

# --- YENI (2026-08-21, B.8): CIFAR-100'un KENDI secim bandi ---
# 9 hucre (sabir x yumusatma). E2'nin 18 hucrelik degeriyle KARISTIRILMAMALI:
# CIFAR-100'de bolme boyutu yoktur.
for ds, lbl in (("cifar100", "C100"), ("cifar10", "C10")):
    v = b8["veri_kumeleri"][ds]
    chk(f"B8 {lbl} yayilim alt", v["yayilim_araligi"][0])
    chk(f"B8 {lbl} yayilim ust", v["yayilim_araligi"][1])
chk("B8 C100 yayilim ort", b8["veri_kumeleri"]["cifar100"]["yayilim_ort"])

# --- YENI (2026-08-21, E6/L2) ---
for arch, lbl in (("resnet18", "ResNet"), ("vit_tiny", "ViT")):
    v = e6["modeller_pgd_l2"][arch]
    chk(f"E6 PGD-L2 {lbl}", v["pgd_l2"]["ort"])
    chk(f"E6 PGD-L2 sd {lbl}", v["pgd_l2"]["sd"])
    chk(f"E6 temiz tam {lbl}", v["temiz_tam_kume"]["ort"])
for m, lbl in (("ResNet18_AT", "ResNet"), ("ViT_Tiny_AT", "ViT")):
    v = e6["modeller_autoattack_l2"][m]
    chk(f"E6 AA-L2 {lbl}", v["aa_l2_robust"]["ort"])
    chk(f"E6 AA-L2 sd {lbl}", v["aa_l2_robust"]["sd"])
    chk(f"E6 temiz 5k {lbl}", v["temiz_5000_altkumede"]["ort"])
for p, lbl in (("raw", "ham"), ("target_correct", "hedef-dogru"),
               ("both_correct", "her-ikisi-dogru"), ("successful_source", "basarili-kaynak")):
    d = e6t["protocols"][p]["diff"]
    chk(f"E6 L2 fark {lbl}", d["mean"])
    chk(f"E6 L2 fark sd {lbl}", d["std"])
chk("E6 L2 protokol yayilimi", e6t["protocol_spread_pp"]["mean"])
chk("E6 O1 egim", e6o["O1_yon"]["egim"], 3)
# KALDIRILDI (2026-08-25): Bolum 4.6 korelasyon YERINE egimi raporlamaya
# karar verdi ("we report the slope rather than a correlation ..."), yani
# bu sayi metinde YOK. Kontrol yalniz oznitelik tablosundaki 0.9990 icinde
# eslesip geciyordu. Kararin AYAKTA oldugunu iddia kapisi denetliyor (I1).
# chk("E6 O1 r", e6o["O1_yon"]["pearson_r"], 3)

# --- rapor ---
def tam_eslesme(val, txt):
    """SAYI SINIRINA bagli eslesme sayisi.

    Ciplak `val in txt` yetmez: '19.37' dizesi '119.37' icinde de gecer ve
    manset sayiya rakam eklense bile kapi GECER (2026-08-25 denetimi bunu
    olctu). Ayrica bazi kontroller YALNIZ daha uzun bir sayinin icinde
    eslesip hic dogrulanmadan 'OK' aliyordu. Bu yuzden eslesmenin oncesinde
    ve sonrasinda rakam ya da ondalik ayraci OLMAMALIDIR.
    """
    return len(re.findall(r"(?<![\d.,])" + re.escape(val) + r"(?![\d])", txt))


# --- T3: hakem turu 3'te metne giren sayilar ---
# Manset artik tek bir yayilim degil, UC BITISIK ACIKLIK olarak raporlaniyor.
# Acikliklar protokol ortalamalarindan TUREVDIR; yuvarlanmis tablo
# degerlerinden degil HAM degerlerden hesaplanmalidir (once yuvarlanmislardan
# turetilmis ve 5,30/5,80 yazilmisti; dogrusu 5,31/5,79).
_pd = {k: v["diff"]["mean"] for k, v in tr["protocols"].items()}
chk("T3 aciklik hedef-dogru->her-ikisi-dogru",
    _pd["both_correct"] - _pd["target_correct"])
# Tur 4: Denklem 1 HEDEF-DOGRU orani baglar, dolayisiyla kapali formda
# kapattigi aciklik ham <-> hedef-dogru'dur (9,21). Tur 3'te yanlislikla
# her-ikisi-dogru <-> ham (5,31) acikligi ozdeslige atfedilmisti.
chk("T4 OZDESLIK TERIMI (ham - hedef-dogru)", _pd["raw"] - _pd["target_correct"])
chk("T3 aciklik ham->basarili-kaynak", _pd["successful_source"] - _pd["raw"])

# Her-ikisi-dogru GA'si TANIMLI BIR YORDAM DEGILDIR: makale artik uc tohumun
# kendi araliklarini ve kosumlar arasi t araligini ayri ayri veriyor.
_bcp = tr["both_correct_paired"]
for _i, (_a, _u) in enumerate(zip(_bcp["ci_low"]["values"],
                                  _bcp["ci_high"]["values"])):
    chk(f"T3 tohum{_i+1} GA alt", _a)
    chk(f"T3 tohum{_i+1} GA ust", _u)
_d3 = np.array(_bcp["diff_pp"]["values"])
_t = 4.302652729911275  # t(0,975; sd=2)
_yari = _t * _d3.std(ddof=1) / np.sqrt(len(_d3))
chk("T3 kosumlar arasi t alt", _d3.mean() - _yari)
chk("T3 kosumlar arasi t ust", _d3.mean() + _yari)

# Gradyan seyrekligi KOSUM duzeyinde raporlaniyor (ornek duzeyi degil).
# Tablo VIII'in kendi basligi cikarimin kosum duzeyinde oldugunu soyluyor;
# iddia da orada kurulmali.
import glob as _glob


def _grad_cift(_key):
    _R, _V = [], []
    for _p in sorted(_glob.glob(str(ROOT / "results/c1_gradient/pair*"))):
        _f = Path(_p) / "gradient_summary.json"
        if not _f.exists():
            continue
        _o = json.loads(_f.read_text(encoding="utf-8"))

        def _bul(_x, _m):
            if isinstance(_x, dict):
                if _m in _x and isinstance(_x[_m], dict):
                    _v = _x[_m].get(_key)
                    if isinstance(_v, dict):
                        return _v.get("mean")
                    if _v is not None:
                        return _v
                for _y in _x.values():
                    _r = _bul(_y, _m)
                    if _r is not None:
                        return _r
            return None
        _a, _b = _bul(_o, "ResNet18_AT"), _bul(_o, "ViT_Tiny_AT")
        if _a is not None and _b is not None:
            _R.append(_a); _V.append(_b)
    return np.array(_R), np.array(_V)


try:
    from scipy import stats as _st
    _hamp = {}
    for _ad, _k in (("Hoyer", "sparsity_hoyer"), ("Gini", "sparsity_gini"),
                    ("Frac", "sparsity_rel_threshold"),
                    ("Hiz", "gradient_alignment")):
        _R, _V = _grad_cift(_k)
        if len(_R) >= 2:
            _hamp[_ad] = float(_st.ttest_rel(_R, _V).pvalue)
    if len(_hamp) == 4:
        chk("T3 kosum p Gini", _hamp["Gini"], 3)
        chk("T3 kosum p Frac", _hamp["Frac"], 3)
        chk("T3 kosum p Hoyer", _hamp["Hoyer"], 3)
        chk("T3 kosum p hizalanma", _hamp["Hiz"], 4)
        _sk = sorted((v for k, v in _hamp.items() if k != "Hiz"))
        _onceki, _holm = 0.0, []
        for _i, _p in enumerate(_sk):
            _onceki = max(_onceki, min(1.0, (len(_sk) - _i) * _p))
            _holm.append(_onceki)
        chk("T3 kosum Holm (uc olcu)", max(_holm), 3)
except ImportError:
    pass


# --- T4: CIFAR-100 ayrisimi ---
# CIFAR-100'de kosulsuz oran dordun EN BUYUGUDUR; iki-parcali bolumleme
# orada gecerli degildir ve yayilimin TAMAMI ozdeslik payidir. Metin bunu
# soyluyor; kapi da denetler.
try:
    _c100p = jl("results/q1/cifar100/transfer/e1_transfer_summary.json")["protocols"]

    def _dg100(k):
        _v = _c100p[k]
        return _v["diff"]["mean"] if isinstance(_v, dict) and "diff" in _v else _v

    chk("T4 C100 artik (her-ikisi - hedef-dogru)",
        _dg100("both_correct") - _dg100("target_correct"))
    chk("T4 C100 yayilim = ozdeslik payi",
        _dg100("raw") - _dg100("target_correct"))
except Exception as _e:
    print(f"  [uyari] C100 ayrisimi hesaplanamadi: {_e}")

# --- T4: blok cikisi derinlik profili ---
# ViT ozetleri artik ARTIK BLOK CIKISINDA aliniyor (siniflandiricinin
# okudugu tensor). Onceki surumde CLS yalniz .mlp alt-blogunda
# hesaplaniyordu ve Tablo VII denk olmayan nicelikleri karsilastiriyordu.
try:
    import glob as _g2
    _c4 = [json.loads(Path(_f).read_text(encoding="utf-8"))
           for _f in sorted(_g2.glob(str(ROOT / "results/c1_c4/pair*/c4_summary.json")))]

    def _blokser(_key):
        _yig = []
        for _d in _c4:
            _o = {}
            for _k, _v in _d["vit"].get(_key, {}).items():
                if _k.startswith("block") and ".mlp" not in _k:
                    _o[int(_k[5:])] = _v["mean"]
            if _o:
                _yig.append([_o[_i] for _i in sorted(_o)])
        return np.array(_yig).mean(0) if _yig else None

    _cls = _blokser("cos_block_cls")
    _pm = _blokser("cos_block_token_mean")
    _al = _blokser("cos_block_output")
    if _cls is not None and _pm is not None:
        chk("T4 blok CLS minimumu", float(_cls.min()), 4)
        chk("T4 blok yama-ort minimumu", float(_pm.min()), 4)
        chk("T4 blok tum-jeton minimumu", float(_al.min()), 4)
        chk("T4 CLS/yama kayma orani",
            float((1 - _cls.min()) / (1 - _pm.min())), 2)
except Exception as _e:
    print(f"  [uyari] blok cikisi serisi okunamadi: {_e}")

# --- 2026-10-04 (LeCun turu): YENI tablolar (tab:source_target, tab:external_pool),
# yeni sekil (fig:spread_clean_gap) ve yeni metin sayilari. Kaynaklar, referans
# foyunun (results/C1_REFERANS_FOYU.md) ayni bolumlerini ureten artefaktlardir.
# Bu kontroller YALNIZ EN metninde aranir: TR aynasi ikinci geciste yazilacak.
# TR esitlendiginde bu satirlar chk(...) bicimine cevrilmelidir (iki dil).
# Mevcut chk(...) kontrollerinin hicbiri degistirilmedi.
CHECKS_EN = []


def chk_en(label, value, nd=2):
    CHECKS_EN.append((label, f"{value:.{nd}f}"))


def _ms2(v):
    a = np.asarray(v, dtype=float)
    return float(a.mean()), float(a.std(ddof=1))


_EN_HATA = []
try:
    # Kaynak-hedef toplamsal ayristirma (foy: 'Kaynak-hedef toplamsal ayristirma')
    _KH = jl("results/q1/kaynak_hedef_ayristirma.json")["sonuc"]
    for _ds, _tg in (("CIFAR-10", "C10"), ("CIFAR-100", "C100")):
        for _pr in ("target_correct", "raw"):
            _d = _KH[_ds]["cift_basina"][_pr]
            for _al, _nd in (("kaynak_etkisi_farki_ResNet_eksi_ViT", 2), ("hedef_etkisi_farki_ViT_eksi_ResNet", 2),
                             ("asimetri_ResNettoViT_eksi_ViTtoResNet", 2), ("max_abs_artik", 2), ("R2", 4)):
                _m, _s = _ms2(_d[_al]["degerler"])
                chk_en(f"KH {_tg} {_pr} {_al} ort", abs(_m), _nd)
                chk_en(f"KH {_tg} {_pr} {_al} sd", _s, _nd)
        _d = _KH[_ds]["cift_basina"]["target_correct"]
        for _al in ("WRN_hedef_fark_ResNet_eksi_ViT", "WRN_kaynak_fark_ResNet_eksi_ViT"):
            _m, _s = _ms2(_d[_al]["degerler"])
            chk_en(f"KH {_tg} sabit WRN {_al} ort", abs(_m))
            chk_en(f"KH {_tg} sabit WRN {_al} sd", _s)
    _d = _KH["CIFAR-10"]["ozet_matris"]["target_correct"]["sabit_WRN"]
    for _al in ("WRN_hedef_ResNetten", "WRN_hedef_ViTden", "WRN_kaynak_ResNete", "WRN_kaynak_ViTe"):
        chk_en(f"KH C10 sabit WRN orani (ozet matris) {_al}", _d[_al])
    # Mahmood 8x8 uydurmalari
    for _ds, _tg in (("CIFAR-10", "C10"), ("CIFAR-100", "C100")):
        _m8 = _KH["Mahmood2021"][_ds]
        _u, _a2 = _m8["uydurma"], _m8["ayni_cins_terimli_uydurma"]["uydurma"]
        chk_en(f"Mahmood {_tg} toplamsal R2", _u["R2"], 4)
        chk_en(f"Mahmood {_tg} toplamsal max artik", _u["max_abs_artik"])
        chk_en(f"Mahmood {_tg} aile-terimli R2", _a2["R2"], 4)
        chk_en(f"Mahmood {_tg} aile-terimli max artik", _a2["max_abs_artik"])
        _F1 = _m8["aile_duzeyi_farklar"]
        _F2 = _m8["ayni_cins_terimli_uydurma"]["aile_duzeyi_farklar"]
        for _k in ["CNN_vs_ViT_hibrit_haric"] + (["ResNet_vs_ViT"] if _ds == "CIFAR-100" else []):
            for _F, _fl in ((_F1, "toplamsal"), (_F2, "aile-terimli")):
                chk_en(f"Mahmood {_tg} {_k} {_fl} kaynak", abs(_F[_k]["kaynak_etkisi_farki_CNN_eksi_ViT"]))
                chk_en(f"Mahmood {_tg} {_k} {_fl} hedef", abs(_F[_k]["hedef_etkisi_farki_ViT_eksi_CNN"]))
    # Dis veri: Mahmood, anahtar cift ve yaklasim hatasi
    _MO = jl("results/q1/dis_veri/mahmood2021_ozdeslik.json")
    _ak = _MO["anahtar_cift_BiT-M-R50x1_ViT-L-16"]["CIFAR-10"]
    _pk = [k for k in _ak if k.startswith("p=1")][0]
    chk_en("Mahmood anahtar cift protokol etkisi", abs(_ak[_pk]["protokol_etkisi_ham_eksi_bc_puan"]))
    chk_en("Mahmood anahtar cift etki araligi alt", abs(_ak[_pk]["protokol_etkisi_aralik_puan"][0]))
    chk_en("Mahmood anahtar cift etki araligi ust", abs(_ak[_pk]["protokol_etkisi_aralik_puan"][1]))
    chk_en("Mahmood anahtar cift bc asimetrisi", abs(_ak["asimetri_bc_puan"]))

    # Standart egitimli hedeflerde oncul p (temiz ciftler)
    _TC = [jl(f"results/q1/temiz_ciftler/pair{_p}/havuz_protokoller.json") for _p in (1, 2, 3)]
    _Ph, _Ah = {}, {}
    for _t in _TC:
        for _y, _v in _t["yonlu"].items():
            _s, _h = _y.split("->")
            if _s == _h:
                continue
            _Ph.setdefault(_h, []).append(_v["p_adv_yanlis_verili_temiz_yanlis"])
            _Ah.setdefault(_h, []).append(abs(_v["ozdeslik_artigi_ham_eksi_ongoru"]))
    _allp = [x for v in _Ph.values() for x in v]
    chk_en("temiz ciftler p en kucuk (4)", min(_allp), 4)
    chk_en("temiz ciftler p en kucuk (3)", min(_allp), 3)
    chk_en("temiz ciftler artik en buyuk", max(x for v in _Ah.values() for x in v))
    chk_en("Standard WRN hedef p en buyuk", max(_Ph["Standard_WRN28_10"]), 4)
    chk_en("ViT temiz hedef p en kucuk", min(_Ph["ViT_Tiny_clean"]), 4)
    chk_en("ViT temiz hedef p en buyuk", max(_Ph["ViT_Tiny_clean"]), 4)
    chk_en("ResNet temiz hedef p en kucuk", min(_Ph["ResNet18_clean"]), 4)
    chk_en("Standard WRN hedef artik en buyuk", max(_Ah["Standard_WRN28_10"]))
    chk_en("ResNet temiz hedef artik en buyuk", max(_Ah["ResNet18_clean"]))
    _tur = {}
    for _t in _TC:
        for _c in _t["ciftler"]:
            _tur.setdefault(tuple(_c["cift"]), []).append(_c)
    for _ct, _cs in _tur.items():
        _m, _s = _ms2([_c["temiz_dogruluk_farki_mutlak"] for _c in _cs])
        chk_en(f"temiz cift {_ct} temiz fark ort", _m)
        chk_en(f"temiz cift {_ct} temiz fark sd", _s)
        _m, _s = _ms2([_c["yayilim_dort_protokol"] for _c in _cs])
        chk_en(f"temiz cift {_ct} yayilim ort", _m)
        chk_en(f"temiz cift {_ct} yayilim sd", _s)

    # RobustBench havuzu
    _HV = jl("results/q1/havuz_cifar10/havuz_protokoller.json")
    _op = _HV["oncul_p_ozeti"]
    chk_en("havuz p en kucuk", _op["p_min"], 4)
    chk_en("havuz artik en buyuk", _op["ozdeslik_artigi_mutlak_max_puan"])
    chk_en("havuz AT hedef p en kucuk", min(_op["p_hedef_bazinda"][m]["p_min"]
                                           for m in _HV["modeller"] if m != "Standard_WRN28_10"), 4)
    _eg = _HV["egim_yayilim_temiz_fark"]
    for _ad, _tg in (("uc_protokol_bas_kaynak_haric", "uc"), ("dort_protokol", "dort")):
        chk_en(f"havuz egim {_tg}", abs(_eg[_ad]["egim"]), 3)
        chk_en(f"havuz egim {_tg} GA alt", abs(_eg[_ad]["egim_GA95_model_bootstrap"][0]), 3)
        chk_en(f"havuz egim {_tg} GA ust", abs(_eg[_ad]["egim_GA95_model_bootstrap"][1]), 3)
        chk_en(f"havuz egim {_tg} r", _eg[_ad]["pearson_r"], 3)
    _ta = _HV["toplamsal_kaynak_hedef_hedef_dogru"]
    chk_en("havuz toplamsal R2", _ta["R2"], 4)
    chk_en("havuz ViT_Tiny_AT kaynak etkisi", abs(_ta["kaynak_etkisi"]["ViT_Tiny_AT"]))
    chk_en("havuz ViT_Tiny_AT hedef etkisi", abs(_ta["hedef_etkisi"]["ViT_Tiny_AT"]))

    # Secim kurali: son kontrol noktasi (foy: 'Secim kuralinin asimetriye etkisi', B)
    _SK = [jl(f"results/q1/son_kontrol_noktasi/pair{_p}/havuz_protokoller.json") for _p in (1, 2, 3)]
    _sd1 = jl("results/c1_seeds/c1_seed_summary.json")["pairs"]
    _son = []
    for _i, _t in enumerate(_SK):
        _c = [c for c in _t["ciftler"] if c["cift"] == ["ResNet18_AT", "ViT_Tiny_AT"]][0]
        _td = _t["temiz_dogruluk"]
        _son.append((_c["yayilim_dort_protokol"], _c["yayilim_uc_protokol_bas_kaynak_haric"],
                     _td["ResNet18_AT"] - _td["ViT_Tiny_AT"], _c["asimetri_ileri_eksi_geri"]["target_correct"],
                     _c["asimetri_ileri_eksi_geri"]["successful_source"]))
    _son = np.array(_son)
    for _j, _ad in enumerate(("yayilim dort", "yayilim uc", "temiz fark", "tc asimetri")):
        _m, _s = _ms2(_son[:, _j])
        chk_en(f"son ckpt {_ad} ort", abs(_m))
        chk_en(f"son ckpt {_ad} sd", _s)
    chk_en("son ckpt ss asimetri ort", _son[:, 4].mean())
    chk_en("son ckpt p en kucuk", min(_t["oncul_p_ozeti"]["p_min"] for _t in _SK), 4)
    chk_en("son ckpt artik en buyuk", max(_t["oncul_p_ozeti"]["ozdeslik_artigi_mutlak_max_puan"] for _t in _SK))
    _c1y = np.array(tr["protocol_spread_pp"]["values"], dtype=float)
    _c1t = np.array([p["resnet"]["clean"] - p["vit"]["clean"] for p in _sd1], dtype=float)
    _m, _s = _ms2(_son[:, 0] - _c1y)
    chk_en("son - secilen yayilim dort ort", abs(_m))
    chk_en("son - secilen yayilim dort sd", _s)
    _m, _s = _ms2(_son[:, 2] - _c1t)
    chk_en("son - secilen temiz fark ort", abs(_m))
    chk_en("son - secilen temiz fark sd", _s)
    _m, _s = _ms2(_c1t)
    chk_en("secilen temiz fark ort", _m)
    chk_en("secilen temiz fark sd", _s)

    # Secim kurali: saklanan yorungeler (foy: 'Secim kuralinin asimetriye etkisi', A)
    _SE = jl("results/q1/secim_asimetri_etkisi.json")
    _YV = _SE["yorungeler"][_SE["kanonik_dizin"].rsplit("/", 1)[-1]]
    _grup, _c10_tf = {}, []
    for _v in _YV.values():
        if isinstance(_v["secim_ozeti"], str):
            continue
        _r, _sn = _v["secim_ozeti"]["referans_hucre"], _v["ozet"]["son"]
        _k = (_v["bilgi"]["dataset"], _v["bilgi"]["taranan_model"])
        _grup.setdefault(_k, []).append((_sn["yayilim_dort"] - _r["en_yakin_yayilim_dort"],
                                         _sn["asimetri"]["target_correct"] - _r["en_yakin_asimetri"]["target_correct"]))
        if _v["bilgi"]["dataset"] == "cifar10":
            _c10_tf += [_r["en_yakin_temiz_hata_farki_ViT_eksi_CNN"], _sn["temiz_hata_farki_ViT_eksi_CNN"]]
    chk_en("yorunge C10 temiz fark en kucuk", min(_c10_tf))
    for _k, _rows in _grup.items():
        _A = np.array(_rows)
        _m, _s = _ms2(_A[:, 0])
        chk_en(f"yorunge {_k} yayilim Delta ort", abs(_m))
        chk_en(f"yorunge {_k} yayilim Delta sd", _s)
    _A = np.array(_grup[("cifar10", "ViT-Tiny")])
    _m, _s = _ms2(_A[:, 1])
    chk_en("yorunge C10 ViT tc Delta ort", _m)
    chk_en("yorunge C10 ViT tc Delta sd", _s)

    # Kosumlar arasi aralik (C1 secilmis) ve turetilmis protokol farklari
    for _p in ("raw", "target_correct", "both_correct", "successful_source"):
        _v = np.array(tr["protocols"][_p]["diff"]["values"], dtype=float)
        chk_en(f"C1 kosumlar arasi aralik {_p}", _v.max() - _v.min())
    _T975 = 4.302652729911275
    for _tg, _sm in (("C10", tr), ("C100", e1t), ("L2", e6t)):
        _bt = (np.array(_sm["protocols"]["both_correct"]["diff"]["values"], dtype=float)
               - np.array(_sm["protocols"]["target_correct"]["diff"]["values"], dtype=float))
        _m, _s = _ms2(_bt)
        _y = _T975 * _s / np.sqrt(len(_bt))
        chk_en(f"{_tg} bc-tc ort", _m)
        chk_en(f"{_tg} bc-tc t alt", _m - _y)
        chk_en(f"{_tg} bc-tc t ust", _m + _y)
    _bt = (np.array(e7t["protocols"]["both_correct"]["diff"]["values"], dtype=float)
           - np.array(e7t["protocols"]["target_correct"]["diff"]["values"], dtype=float))
    for _i, _x in enumerate(_bt, 1):
        chk_en(f"SVHN bc-tc cift{_i}", _x)
    _ss = (np.array(tr["protocols"]["successful_source"]["diff"]["values"], dtype=float)
           - np.array(tr["protocols"]["both_correct"]["diff"]["values"], dtype=float))
    chk_en("C10 ss-bc ort", _ms2(_ss)[0])
    chk_en("C10 ss-bc sd", _ms2(_ss)[1])
    _rt = (np.array(tr["protocols"]["raw"]["diff"]["values"], dtype=float)
           - np.array(tr["protocols"]["target_correct"]["diff"]["values"], dtype=float))
    chk_en("C10 raw-tc sd", _ms2(_rt)[1])

    # Uc-protokol egimi, SVHN dahil (foy: 'Uc-protokol egimi, SVHN dahil')
    _E3 = jl("results/q1/e3_uc_protokol_svhnli_fit.json")["sonuc"]
    _u = _E3["uc_protokol_svhn_dahil"]
    chk_en("E3 SVHN dahil uc egim", _u["egim"], 3)
    chk_en("E3 SVHN dahil uc GA alt", _u["egim_GA95_kume_bootstrap"][0], 3)
    chk_en("E3 SVHN dahil uc GA ust", _u["egim_GA95_kume_bootstrap"][1], 3)
    _o = _E3["ozdeslik_terimi_abs_ham_eksi_tc_ongoru_svhn_dahil"]
    chk_en("E3 ozdeslik terimi egim", _o["egim"], 3)
    chk_en("E3 ozdeslik terimi GA alt", _o["egim_GA95_kume_bootstrap"][0], 4)
    chk_en("E3 ozdeslik terimi GA ust", _o["egim_GA95_kume_bootstrap"][1], 4)
    _dp = _E3["dort_protokol_svhn_dahil"]
    chk_en("E3 SVHN dahil dort egim", abs(_dp["egim"]), 3)
    chk_en("E3 SVHN dahil dort GA alt", abs(_dp["egim_GA95_kume_bootstrap"][0]), 3)
    chk_en("E3 SVHN dahil dort GA ust", abs(_dp["egim_GA95_kume_bootstrap"][1]), 3)

    # Dikkat entropisi TOST ve devrilen/devrilmeyen kosinus
    _C4T = jl("results/c1_c4/c4_entropy_tost.json")
    chk_en("TOST en buyuk p", max(k["p_TOST"] for k in _C4T["entropi_TOST"]["katmanlar"]), 3)
    chk_en("TOST temiz entropi en kucuk", min(k["temiz_entropi_ort"] for k in _C4T["entropi_TOST"]["katmanlar"]))
    chk_en("TOST temiz entropi en buyuk", max(k["temiz_entropi_ort"] for k in _C4T["entropi_TOST"]["katmanlar"]))
    _kd = _C4T["son_blok_kosinus_devrilen_vs_devrilmeyen"]
    chk_en("devrilen/devrilmeyen p ViT", _kd["ViT"]["eslesik_t_kosu_duzeyi"]["p_iki_yonlu"], 2)
    chk_en("devrilen/devrilmeyen p ResNet", _kd["ResNet"]["eslesik_t_kosu_duzeyi"]["p_iki_yonlu"], 3)

    # Yayilim - temiz fark iliskisi, tum ciftler (fig:spread_clean_gap)
    _FG = jl("results/q1/fig_yayilim_temiz_fark_veri.json")["egim"]
    _e = _FG["uc_protokol_bas_kaynak_haric"]
    chk_en("tum ciftler uc egim", _e["egim"], 3)
    chk_en("tum ciftler uc r", _e["pearson_r"], 3)
    chk_en("tum ciftler uc grup-birak en kucuk", min(_e["grup_birak_egimleri"].values()), 3)
    chk_en("tum ciftler uc grup-birak en buyuk", max(_e["grup_birak_egimleri"].values()), 3)
    _e = _FG["dort_protokol"]
    chk_en("tum ciftler dort egim", _e["egim"], 3)
    chk_en("tum ciftler dort r", _e["pearson_r"], 3)
    chk_en("tum ciftler parite en buyuk sapma", _FG["ozdeslik_paritesi"]["mutlak_sapma_max"])
    chk_en("tum ciftler parite ort sapma", _FG["ozdeslik_paritesi"]["mutlak_sapma_ort"])
    chk_en("tum ciftler uc=|raw-tc| sayisi", _FG["uc_protokol_yayilimi_vs_raw_tc_farki"]["esit_cift_sayisi_1e-9"], 0)
except Exception as _e_:  # anahtar degisirse kapi SESSIZCE gecmesin
    _EN_HATA.append(f"{type(_e_).__name__}: {_e_}")

rows = []
for label, val in CHECKS:
    found = {lang: (tam_eslesme(val, txt) > 0) for lang, txt in LANGS.items()}
    sayim = {lang: tam_eslesme(val, txt) for lang, txt in LANGS.items()}
    rows.append((label, val, found, sayim))

missing = 0
print(f"{'KONTROL':36s} {'DEGER':>9s}  EN   TR")
print("-" * 60)

for label, val, found, sayim in rows:
    en = "OK " if found["EN"] else "YOK"
    trk = "OK " if found["TR"] else "YOK"
    if not (found["EN"] and found["TR"]):
        missing += 1
    ek = ""
    if found["EN"] and found["TR"] and (sayim["EN"] > 3 or sayim["TR"] > 3):
        ek = f"   ({sayim['EN']}/{sayim['TR']} yerde)"
    print(f"{label:36s} {val:>9s}  {en}  {trk}{ek}")

print("-" * 60)
en_missing = sum(1 for _, _, f, _s in rows if not f["EN"])
tr_missing = sum(1 for _, _, f, _s in rows if not f["TR"])
print(f"TOPLAM={len(rows)}  EN_EKSIK={en_missing}  TR_EKSIK={tr_missing}")
if not LANGS["TR"].strip():
    print("UYARI: TR metni okunamadi (dosya adlari degismis olabilir).")

# IS-6(d): betik eksik bulsa BILE 0 ile cikiyordu -> KAPI olarak kullanilamiyordu.
# Artik eksik varsa 1 doner ve CI/kanca icinde kapi gorevi gorebilir.
import sys as _sys

# --- YALNIZ EN kontrolleri (2026-10-04, LeCun turu; TR ayna gecisinde iki dile cevrilecek) ---
print()
print(f"{'YALNIZ EN KONTROLU (yeni tablolar)':52s} {'DEGER':>9s}  EN")
print("-" * 68)
en_only_missing = 0
for label, val in CHECKS_EN:
    ok = tam_eslesme(val, LANGS["EN"]) > 0
    if not ok:
        en_only_missing += 1
    print(f"{label[:52]:52s} {val:>9s}  {'OK ' if ok else 'YOK'}")
print("-" * 68)
print(f"YALNIZ-EN TOPLAM={len(CHECKS_EN)}  EN_EKSIK={en_only_missing}")
for _h in _EN_HATA:
    print(f"KAPI HATASI (yalniz-EN blogu okunamadi): {_h}")
if en_only_missing or _EN_HATA:
    print("SONUC: KALDI -- yeni tablolardaki/metindeki bir sayi EN metninde bulunamadi ya da artefakt okunamadi.")
    _sys.exit(1)

if en_missing or tr_missing or not LANGS["TR"].strip():
    print("SONUC: KALDI -- metinde bulunamayan sayi var (ya da TR okunamadi).")
    _sys.exit(1)
print("SONUC: GECTI -- tum tasiyici sayilar iki dilde de artefaktla tutuyor.")
_sys.exit(0)
