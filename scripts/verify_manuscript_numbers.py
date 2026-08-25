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
for p, lbl in (("raw", "ham"), ("target_correct", "hedef-dogru"),
               ("both_correct", "her-ikisi-dogru"), ("successful_source", "basarili-kaynak")):
    chk(f"E7 {lbl} CNN->ViT", _prot[p]["CNN_to_ViT"]["mean"])
    chk(f"E7 {lbl} ViT->CNN", _prot[p]["ViT_to_CNN"]["mean"])
    chk(f"E7 {lbl} fark", abs(_prot[p]["diff"]["mean"]))
chk("E7 protokol yayilimi", e7t["protocol_spread_pp"]["mean"])
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
if en_missing or tr_missing or not LANGS["TR"].strip():
    print("SONUC: KALDI -- metinde bulunamayan sayi var (ya da TR okunamadi).")
    _sys.exit(1)
print("SONUC: GECTI -- tum tasiyici sayilar iki dilde de artefaktla tutuyor.")
_sys.exit(0)
