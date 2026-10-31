"""Makaledeki tasiyici sayilarin referans foyu ve artefaktlarla tutarliligini denetler.

TASARIM (2026-10-31, konsey manseti; brif 12 §5.10, not 14). Tasiyici kumesi artik elle
tutulan bir liste DEGIL, metnin kendi `% FOY:<bolum>:<satir>` yorumlarindan turetilir.
Uc kisim vardir; ilk ikisi kapidir, ucuncusu eski listeyi FOY atiflarina baglar:

  A. FOY yorumlarindan turetilen tasiyicilar (ZORUNLU). Her ardisik yorum grubundaki FOY
     atiflari (bolum etiketi, satir listesi ve araliklar; parantez icindeki aciklama atilir)
     okunur. Grubun BLOGU, gruptan sonraki metin satirlaridir; bir sonraki FOY yorumunda ya
     da bos satirda biter (acik table/figure ortami bos satirda bitmez). Foy satirindaki ve
     bloktaki ONDALIK sayilar (bilimsel gosterim dahil; LaTeX bicim sayilari atilir) eslenir.
     "Tasinmis" esleme: esit, ya da foy degeri metnin basamak sayisina yuvarlaninca esit, ya
     da yuzde <-> oran (44.2 -> 0.442). Uc kapi:
       A1  ondalik sayi tasiyan blok, atfettigi satirlarin hicbir sayisini (ondalik ya da uc+
           basamakli tamsayi) tasimiyorsa EKSIK: yorum blogun tasimadigi satiri gosteriyor
           (eski sayi, kaymis satir numarasi, dusmus tablo). Ondalik sayisiz blok nitel
           gruptur; sekil blogu ve KAYNAK yorumlu grup yalniz bilgi.
       A2  blokta olup foyun HICBIR satirinda tasinmis hali olmayan sayi EKSIK (FOYDE YOK);
           grupta '% KAYNAK:' yorumu varsa yalniz bilgi (sayi baska kaynaga baglanmis).
       A3  KAYNAK yorumu olmayan grupta, iki ve daha cok ondalikli (ya da bilimsel) bir sayi
           atfedilen satirlarda yok ama foyun baska satirinda varsa EKSIK (ATIF EKSIK: yanlis
           sayi ya da eksik atif). Tek ondalikli sayilar (asama.blok etiketi, esik) bilgi.
     Foy disinda satir numarasi EKSIK. Hicbir sayisi blokta gecmeyen tek tek atiflar bilgi.

  B. Ana manset tasiyicilari (ZORUNLU). H1/H2/H3 kestirim ve %90 araliklari; K-a/K-b/K-c
     kestirim ve %90 araliklari (CIFAR-10 B2, CIFAR-100 B9); korunma orani ve araligi (B5);
     B6 en buyuk ve en kucuk PGD-10 - AA farki; A^sigma_IN ve araligi ile Liu cifti (B8);
     alti Mantel r (B10). Degerler JSON artefaktlarindan hesaplanir; hem foyun M9-M10
     bolumunde hem EN metninde (herhangi bir yerde) gecmelidir.

  C. Eski artefakt kontrolleri (2026-08 .. 2026-10 listesi, degistirilmedi). Bir eski
     kontrolun degeri EN metnindeki bir FOY yorumunun atfettigi bir foy satirinda geciyorsa
     o kontrol hala tasiyicidir ve ZORUNLUDUR: once o atfin blogunda, yoksa metnin herhangi
     bir yerinde aranir. Hicbir atfedilen satirda gecmeyen deger metinde varsa "korunuyor
     (FOY atfi disinda)", yoksa "dustu (brif §5.10)" diye raporlanir ve KALDI SAYILMAZ.

IKI DIL: EN (paper/manuscript) ve TR (paper/manuscript_tr) AYRI AYRI denetlenir. Dosya
listesi main.tex'teki \\input / \\InputIfFileExists satirlarindan okunur (Ek ve hesaplama
ayrintilari dahil). TR aynasi henuz esitlenmedigi icin TR sonucu varsayilan olarak
YALNIZ BILGIDIR; `--tr-zorunlu` ile kapiya katilir.
DIKKAT -- `{,}` makrosu iki dilde FARKLI anlama gelir:
  EN : binlik ayraci   ->  10{,}000  = 10000   => "{,}" SILINIR
  TR : ondalik ayraci  ->  10{,}45   = 10.45   => "{,}" NOKTAYA cevrilir
Ayni normalleştirmeyi iki dile uygulamak sessiz "EKSIK" raporlari uretir.

Cikis 0 = GECTI, 1 = KALDI. `--ayrinti` her atfin kapsanmayan sayilarini da basar.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"

_AP = argparse.ArgumentParser(description="Makale tasiyici sayi kapisi (FOY yorumlarindan turetilmis).")
_AP.add_argument("--tr-zorunlu", action="store_true", help="TR eksiklerini de kapiya kat (TR aynasi esitlendikten sonra).")
_AP.add_argument("--ayrinti", action="store_true", help="Bilgi listelerini (atif disi, kapsanmayan atif, dusen) de bas.")
_AP.add_argument("--en-dizin", default="paper/manuscript",
                 help="EN makale dizini (depo kokune gore ya da mutlak); oz-sinama gecici kopya verir.")
ARGS = _AP.parse_args()


def tex_dosyalari(base):
    """main.tex ve onun \\input / \\InputIfFileExists ile yukledigi dosyalar, yuklenme sirasiyla."""
    ana = ROOT / base / "main.tex"
    if not ana.exists():
        return []
    sira = ["main.tex"]
    for m in re.finditer(r"^[^%\n]*\\(?:input|InputIfFileExists)\{([^}]+)\}", ana.read_text(encoding="utf-8"), re.M):
        p = m.group(1).strip()
        p = p if p.endswith(".tex") else p + ".tex"
        if (ROOT / base / p).exists() and p not in sira:
            sira.append(p)
    return sira


EN_BASE, TR_BASE = ARGS.en_dizin, "paper/manuscript_tr"
EN_FILES = tex_dosyalari(EN_BASE)
TR_FILES = tex_dosyalari(TR_BASE)


def read_lang(base, files):
    parts = []
    for p in files:
        f = ROOT / base / p
        if f.exists():
            parts.append(f.read_text(encoding="utf-8"))
    return "\n".join(parts)


def sci_kanonik(s):
    """'9.00e-04' -> '9e-4'; '4.09e-05' -> '4.09e-5'. Ondalik sayiya dokunmaz."""
    if "e" not in s:
        return s
    m, e = s.split("e", 1)
    if "." in m:
        m = m.rstrip("0").rstrip(".")
    return f"{m}e{int(e)}"


def norm_sci(t):
    # 4.09\times10^{-5} -> 4.09e-5 ; 10^{-4} (carpansiz) -> 1e-4. Foyde bilimsel gosterim e-NN.
    t = re.sub(r"(\d+(?:\.\d+)?)\s*\\times\s*10\^\{?\s*([-+]?)\s*(\d+)\s*\}?",
               lambda m: sci_kanonik(f"{m.group(1)}e{m.group(2) or ''}{m.group(3)}"), t)
    return re.sub(r"(?<![\d.])10\^\{?\s*-\s*(\d+)\s*\}?", lambda m: f"1e-{int(m.group(1))}", t)


def norm_en(t):
    # EN: {,} binlik ayracidir -> sil. Sonra kalan virgulleri de sil.
    return norm_sci(t.replace("{,}", "").replace(",", ""))


def norm_tr(t):
    # TR ondalik ayraci IKI bicimde yaziliyor ve IKISI DE GECERLI:
    #   $13{,}57$ -> matematik kipinde zorunlu ({,} bosluk sorununu onler)
    #   0,0378    -> METIN kipinde (tablo hucreleri) dogru Turkce yazim
    # Denetleyici ikisini de tanimak zorunda; aksi halde dogru sayilari
    # "TR'de eksik" diye raporlar (bu hata bir kez yapildi).
    # Sira onemli: once binlik ayraci ("10.000"), sonra {,}, sonra ciplak virgul.
    t = re.sub(r"(?<=\d)\.(?=\d{3}(?!\d))", "", t)
    t = t.replace("{,}", ".")
    return norm_sci(re.sub(r"(?<=\d),(?=\d)", ".", t))


LANGS = {
    "EN": norm_en(read_lang(EN_BASE, EN_FILES)),
    "TR": norm_tr(read_lang(TR_BASE, TR_FILES)),
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
# 2026-10-04 (TR ayna gecisi): bu kontroller chk(...) bicimine cevrildi; artik
# IKI DILDE de aranir. chk_en tanimi bos kalan yalniz-EN blogu icin duruyor.
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
                chk(f"KH {_tg} {_pr} {_al} ort", abs(_m), _nd)
                chk(f"KH {_tg} {_pr} {_al} sd", _s, _nd)
        _d = _KH[_ds]["cift_basina"]["target_correct"]
        for _al in ("WRN_hedef_fark_ResNet_eksi_ViT", "WRN_kaynak_fark_ResNet_eksi_ViT"):
            _m, _s = _ms2(_d[_al]["degerler"])
            chk(f"KH {_tg} sabit WRN {_al} ort", abs(_m))
            chk(f"KH {_tg} sabit WRN {_al} sd", _s)
    _d = _KH["CIFAR-10"]["ozet_matris"]["target_correct"]["sabit_WRN"]
    for _al in ("WRN_hedef_ResNetten", "WRN_hedef_ViTden", "WRN_kaynak_ResNete", "WRN_kaynak_ViTe"):
        chk(f"KH C10 sabit WRN orani (ozet matris) {_al}", _d[_al])
    # Hakem gecisi (2026-10-04, M2): her-ikisi-dogru ve CIFAR-100 basarili-kaynak satirlari,
    # sabit-WRN karsitliklari her kosullu protokolde.
    for _ds, _tg, _prs in (("CIFAR-10", "C10", ("both_correct",)),
                           ("CIFAR-100", "C100", ("both_correct", "successful_source"))):
        for _pr in _prs:
            _d = _KH[_ds]["cift_basina"][_pr]
            for _al, _nd in (("kaynak_etkisi_farki_ResNet_eksi_ViT", 2), ("hedef_etkisi_farki_ViT_eksi_ResNet", 2),
                             ("asimetri_ResNettoViT_eksi_ViTtoResNet", 2), ("max_abs_artik", 2), ("R2", 4)):
                _m, _s = _ms2(_d[_al]["degerler"])
                chk(f"KH {_tg} {_pr} {_al} ort", abs(_m), _nd)
                chk(f"KH {_tg} {_pr} {_al} sd", _s, _nd)
            for _al in ("WRN_hedef_fark_ResNet_eksi_ViT", "WRN_kaynak_fark_ResNet_eksi_ViT"):
                _m, _s = _ms2(_d[_al]["degerler"])
                chk(f"KH {_tg} {_pr} sabit WRN {_al} ort", abs(_m))
                chk(f"KH {_tg} {_pr} sabit WRN {_al} sd", _s)
    # Mahmood 8x8 uydurmalari
    for _ds, _tg in (("CIFAR-10", "C10"), ("CIFAR-100", "C100")):
        _m8 = _KH["Mahmood2021"][_ds]
        _u, _a2 = _m8["uydurma"], _m8["ayni_cins_terimli_uydurma"]["uydurma"]
        chk(f"Mahmood {_tg} toplamsal R2", _u["R2"], 4)
        chk(f"Mahmood {_tg} toplamsal max artik", _u["max_abs_artik"])
        chk(f"Mahmood {_tg} aile-terimli R2", _a2["R2"], 4)
        chk(f"Mahmood {_tg} aile-terimli max artik", _a2["max_abs_artik"])
        _F1 = _m8["aile_duzeyi_farklar"]
        _F2 = _m8["ayni_cins_terimli_uydurma"]["aile_duzeyi_farklar"]
        for _k in ["CNN_vs_ViT_hibrit_haric"] + (["ResNet_vs_ViT"] if _ds == "CIFAR-100" else []):
            for _F, _fl in ((_F1, "toplamsal"), (_F2, "aile-terimli")):
                chk(f"Mahmood {_tg} {_k} {_fl} kaynak", abs(_F[_k]["kaynak_etkisi_farki_CNN_eksi_ViT"]))
                chk(f"Mahmood {_tg} {_k} {_fl} hedef", abs(_F[_k]["hedef_etkisi_farki_ViT_eksi_CNN"]))
    # Dis veri: Mahmood, anahtar cift ve yaklasim hatasi
    _MO = jl("results/q1/dis_veri/mahmood2021_ozdeslik.json")
    _ak = _MO["anahtar_cift_BiT-M-R50x1_ViT-L-16"]["CIFAR-10"]
    _pk = [k for k in _ak if k.startswith("p=1")][0]
    chk("Mahmood anahtar cift protokol etkisi", abs(_ak[_pk]["protokol_etkisi_ham_eksi_bc_puan"]))
    chk("Mahmood anahtar cift etki araligi alt", abs(_ak[_pk]["protokol_etkisi_aralik_puan"][0]))
    chk("Mahmood anahtar cift etki araligi ust", abs(_ak[_pk]["protokol_etkisi_aralik_puan"][1]))
    chk("Mahmood anahtar cift bc asimetrisi", abs(_ak["asimetri_bc_puan"]))
    _pkm = [k for k in _ak if k.startswith("p=p_min")][0]
    chk("Mahmood anahtar cift protokol etkisi (p_min)", abs(_ak[_pkm]["protokol_etkisi_ham_eksi_bc_puan"]))
    # Hakem gecisi: havuzda temiz dogrulugu yakin gurbuz ciftler (F3)
    _HV0 = jl("results/q1/havuz_cifar10/havuz_protokoller.json")
    for _a, _b in (("Carmon2019_WRN28_10", "Gowal2020_WRN28_10"), ("Debenedetti2022_XCiT_S12", "Gowal2020_WRN28_10"),
                   ("ResNet18_AT", "Engstrom2019_RN50")):
        _c = [c for c in _HV0["ciftler"] if c["cift"] == [_a, _b]][0]
        chk(f"havuz {_a}/{_b} temiz fark", _c["temiz_dogruluk_farki_mutlak"])
        chk(f"havuz {_a}/{_b} dort yayilim", _c["yayilim_dort_protokol"])
    # Hakem gecisi: SVHN temiz dogruluklar kosum basina ve fark (foy: Turetilmis, Temiz dogruluk farki)
    _sv = [e7["mimariler"][_m]["ozet"]["test_clean"]["degerler"] for _m in ("resnet18", "vit_tiny")]
    for _i in range(2):
        chk(f"SVHN temiz ResNet kosum{_i+1}", _sv[0][_i])
        chk(f"SVHN temiz ViT kosum{_i+1}", _sv[1][_i])
        chk(f"SVHN temiz fark kosum{_i+1}", _sv[0][_i] - _sv[1][_i])
    chk("SVHN temiz fark ort", float(np.mean(np.array(_sv[0]) - np.array(_sv[1]))))

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
    chk("temiz ciftler p en kucuk (4)", min(_allp), 4)
    chk("temiz ciftler p en kucuk (3)", min(_allp), 3)
    chk("temiz ciftler artik en buyuk", max(x for v in _Ah.values() for x in v))
    chk("Standard WRN hedef p en buyuk", max(_Ph["Standard_WRN28_10"]), 4)
    chk("ViT temiz hedef p en kucuk", min(_Ph["ViT_Tiny_clean"]), 4)
    chk("ViT temiz hedef p en buyuk", max(_Ph["ViT_Tiny_clean"]), 4)
    chk("ResNet temiz hedef p en kucuk", min(_Ph["ResNet18_clean"]), 4)
    chk("Standard WRN hedef artik en buyuk", max(_Ah["Standard_WRN28_10"]))
    chk("ResNet temiz hedef artik en buyuk", max(_Ah["ResNet18_clean"]))
    _tur = {}
    for _t in _TC:
        for _c in _t["ciftler"]:
            _tur.setdefault(tuple(_c["cift"]), []).append(_c)
    for _ct, _cs in _tur.items():
        _m, _s = _ms2([_c["temiz_dogruluk_farki_mutlak"] for _c in _cs])
        chk(f"temiz cift {_ct} temiz fark ort", _m)
        chk(f"temiz cift {_ct} temiz fark sd", _s)
        _m, _s = _ms2([_c["yayilim_dort_protokol"] for _c in _cs])
        chk(f"temiz cift {_ct} yayilim ort", _m)
        chk(f"temiz cift {_ct} yayilim sd", _s)

    # Hakem gecisi (M3): temiz ciftte toplamsal ayristirma ve sabit-Standard karsitliklari (foy M8.15)
    _ks, _hs, _as = [], [], []
    for _t in _TC:
        _ta = _t["toplamsal_kaynak_hedef_hedef_dogru"]
        _ks.append(_ta["kaynak_etkisi"]["ResNet18_clean"] - _ta["kaynak_etkisi"]["ViT_Tiny_clean"])
        _hs.append(_ta["hedef_etkisi"]["ViT_Tiny_clean"] - _ta["hedef_etkisi"]["ResNet18_clean"])
        _o = lambda y: _t["yonlu"][y]["oranlar"]["target_correct"]
        _as.append((_o("Standard_WRN28_10->ResNet18_clean"), _o("Standard_WRN28_10->ViT_Tiny_clean"),
                    _o("ResNet18_clean->Standard_WRN28_10"), _o("ViT_Tiny_clean->Standard_WRN28_10")))
    for _ad, _v in (("temiz cift kaynak farki", _ks), ("temiz cift hedef farki", _hs)):
        _m, _s = _ms2(_v)
        chk(f"{_ad} ort", abs(_m))
        chk(f"{_ad} sd", _s)
    _as = np.array(_as)
    for _j, _ad in enumerate(("Standard->ResNet", "Standard->ViT", "ResNet->Standard", "ViT->Standard")):
        chk(f"temiz cift sabit-Standard {_ad}", _as[:, _j].mean())
    chk("temiz cift sabit-Standard kaynak karsitligi", _ms2(_as[:, 2] - _as[:, 3])[0])
    chk("temiz cift sabit-Standard hedef karsitligi", _ms2(_as[:, 0] - _as[:, 1])[0])

    # RobustBench havuzu
    _HV = jl("results/q1/havuz_cifar10/havuz_protokoller.json")
    _op = _HV["oncul_p_ozeti"]
    chk("havuz p en kucuk", _op["p_min"], 4)
    chk("havuz artik en buyuk", _op["ozdeslik_artigi_mutlak_max_puan"])
    chk("havuz AT hedef p en kucuk", min(_op["p_hedef_bazinda"][m]["p_min"]
                                           for m in _HV["modeller"] if m != "Standard_WRN28_10"), 4)
    _eg = _HV["egim_yayilim_temiz_fark"]
    for _ad, _tg in (("uc_protokol_bas_kaynak_haric", "uc"), ("dort_protokol", "dort")):
        chk(f"havuz egim {_tg}", abs(_eg[_ad]["egim"]), 3)
        chk(f"havuz egim {_tg} GA alt", abs(_eg[_ad]["egim_GA95_model_bootstrap"][0]), 3)
        chk(f"havuz egim {_tg} GA ust", abs(_eg[_ad]["egim_GA95_model_bootstrap"][1]), 3)
        chk(f"havuz egim {_tg} r", _eg[_ad]["pearson_r"], 3)
    _ta = _HV["toplamsal_kaynak_hedef_hedef_dogru"]
    chk("havuz toplamsal R2", _ta["R2"], 4)
    chk("havuz ViT_Tiny_AT kaynak etkisi", abs(_ta["kaynak_etkisi"]["ViT_Tiny_AT"]))
    chk("havuz ViT_Tiny_AT hedef etkisi", abs(_ta["hedef_etkisi"]["ViT_Tiny_AT"]))

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
        chk(f"son ckpt {_ad} ort", abs(_m))
        chk(f"son ckpt {_ad} sd", _s)
    chk("son ckpt ss asimetri ort", _son[:, 4].mean())
    chk("son ckpt p en kucuk", min(_t["oncul_p_ozeti"]["p_min"] for _t in _SK), 4)
    chk("son ckpt artik en buyuk", max(_t["oncul_p_ozeti"]["ozdeslik_artigi_mutlak_max_puan"] for _t in _SK))
    _c1y = np.array(tr["protocol_spread_pp"]["values"], dtype=float)
    _c1t = np.array([p["resnet"]["clean"] - p["vit"]["clean"] for p in _sd1], dtype=float)
    _m, _s = _ms2(_son[:, 0] - _c1y)
    chk("son - secilen yayilim dort ort", abs(_m))
    chk("son - secilen yayilim dort sd", _s)
    _m, _s = _ms2(_son[:, 2] - _c1t)
    chk("son - secilen temiz fark ort", abs(_m))
    chk("son - secilen temiz fark sd", _s)
    _m, _s = _ms2(_c1t)
    chk("secilen temiz fark ort", _m)
    chk("secilen temiz fark sd", _s)

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
    chk("yorunge C10 temiz fark en kucuk", min(_c10_tf))
    for _k, _rows in _grup.items():
        _A = np.array(_rows)
        _m, _s = _ms2(_A[:, 0])
        chk(f"yorunge {_k} yayilim Delta ort", abs(_m))
        chk(f"yorunge {_k} yayilim Delta sd", _s)
    _A = np.array(_grup[("cifar10", "ViT-Tiny")])
    _m, _s = _ms2(_A[:, 1])
    chk("yorunge C10 ViT tc Delta ort", _m)
    chk("yorunge C10 ViT tc Delta sd", _s)

    # Kosumlar arasi aralik (C1 secilmis) ve turetilmis protokol farklari
    for _p in ("raw", "target_correct", "both_correct", "successful_source"):
        _v = np.array(tr["protocols"][_p]["diff"]["values"], dtype=float)
        chk(f"C1 kosumlar arasi aralik {_p}", _v.max() - _v.min())
    _T975 = 4.302652729911275
    for _tg, _sm in (("C10", tr), ("C100", e1t), ("L2", e6t)):
        _bt = (np.array(_sm["protocols"]["both_correct"]["diff"]["values"], dtype=float)
               - np.array(_sm["protocols"]["target_correct"]["diff"]["values"], dtype=float))
        _m, _s = _ms2(_bt)
        _y = _T975 * _s / np.sqrt(len(_bt))
        chk(f"{_tg} bc-tc ort", _m)
        chk(f"{_tg} bc-tc t alt", _m - _y)
        chk(f"{_tg} bc-tc t ust", _m + _y)
    _bt = (np.array(e7t["protocols"]["both_correct"]["diff"]["values"], dtype=float)
           - np.array(e7t["protocols"]["target_correct"]["diff"]["values"], dtype=float))
    for _i, _x in enumerate(_bt, 1):
        chk(f"SVHN bc-tc cift{_i}", _x)
    _ss = (np.array(tr["protocols"]["successful_source"]["diff"]["values"], dtype=float)
           - np.array(tr["protocols"]["both_correct"]["diff"]["values"], dtype=float))
    chk("C10 ss-bc ort", _ms2(_ss)[0])
    chk("C10 ss-bc sd", _ms2(_ss)[1])
    _rt = (np.array(tr["protocols"]["raw"]["diff"]["values"], dtype=float)
           - np.array(tr["protocols"]["target_correct"]["diff"]["values"], dtype=float))
    chk("C10 raw-tc sd", _ms2(_rt)[1])

    # Uc-protokol egimi, SVHN dahil (foy: 'Uc-protokol egimi, SVHN dahil')
    _E3 = jl("results/q1/e3_uc_protokol_svhnli_fit.json")["sonuc"]
    _u = _E3["uc_protokol_svhn_dahil"]
    chk("E3 SVHN dahil uc egim", _u["egim"], 3)
    chk("E3 SVHN dahil uc GA alt", _u["egim_GA95_kume_bootstrap"][0], 3)
    chk("E3 SVHN dahil uc GA ust", _u["egim_GA95_kume_bootstrap"][1], 3)
    _o = _E3["ozdeslik_terimi_abs_ham_eksi_tc_ongoru_svhn_dahil"]
    chk("E3 ozdeslik terimi egim", _o["egim"], 3)
    chk("E3 ozdeslik terimi GA alt", _o["egim_GA95_kume_bootstrap"][0], 4)
    chk("E3 ozdeslik terimi GA ust", _o["egim_GA95_kume_bootstrap"][1], 4)
    _dp = _E3["dort_protokol_svhn_dahil"]
    chk("E3 SVHN dahil dort egim", abs(_dp["egim"]), 3)
    chk("E3 SVHN dahil dort GA alt", abs(_dp["egim_GA95_kume_bootstrap"][0]), 3)
    chk("E3 SVHN dahil dort GA ust", abs(_dp["egim_GA95_kume_bootstrap"][1]), 3)

    # Dikkat entropisi TOST ve devrilen/devrilmeyen kosinus
    _C4T = jl("results/c1_c4/c4_entropy_tost.json")
    chk("TOST en buyuk p", max(k["p_TOST"] for k in _C4T["entropi_TOST"]["katmanlar"]), 3)
    chk("TOST temiz entropi en kucuk", min(k["temiz_entropi_ort"] for k in _C4T["entropi_TOST"]["katmanlar"]))
    chk("TOST temiz entropi en buyuk", max(k["temiz_entropi_ort"] for k in _C4T["entropi_TOST"]["katmanlar"]))
    _kd = _C4T["son_blok_kosinus_devrilen_vs_devrilmeyen"]
    chk("devrilen/devrilmeyen p ViT", _kd["ViT"]["eslesik_t_kosu_duzeyi"]["p_iki_yonlu"], 2)
    chk("devrilen/devrilmeyen p ResNet", _kd["ResNet"]["eslesik_t_kosu_duzeyi"]["p_iki_yonlu"], 3)

    # Yayilim - temiz fark iliskisi, tum ciftler (fig:spread_clean_gap)
    _FG = jl("results/q1/fig_yayilim_temiz_fark_veri.json")["egim"]
    _e = _FG["uc_protokol_bas_kaynak_haric"]
    chk("tum ciftler uc egim", _e["egim"], 3)
    chk("tum ciftler uc r", _e["pearson_r"], 3)
    chk("tum ciftler uc grup-birak en kucuk", min(_e["grup_birak_egimleri"].values()), 3)
    chk("tum ciftler uc grup-birak en buyuk", max(_e["grup_birak_egimleri"].values()), 3)
    _e = _FG["dort_protokol"]
    chk("tum ciftler dort egim", _e["egim"], 3)
    chk("tum ciftler dort r", _e["pearson_r"], 3)
    chk("tum ciftler parite en buyuk sapma", _FG["ozdeslik_paritesi"]["mutlak_sapma_max"])
    chk("tum ciftler parite ort sapma", _FG["ozdeslik_paritesi"]["mutlak_sapma_ort"])
    chk("tum ciftler uc=|raw-tc| sayisi", _FG["uc_protokol_yayilimi_vs_raw_tc_farki"]["esit_cift_sayisi_1e-9"], 0)
except Exception as _e_:  # anahtar degisirse kapi SESSIZCE gecmesin
    _EN_HATA.append(f"{type(_e_).__name__}: {_e_}")

# ===========================================================================================
# YENI RAPOR (2026-10-31): A FOY yorumlari, B ana manset, C eski kontroller (yalniz bilgi).
# Yukaridaki CHECKS listesi degistirilmeden hesaplanir; yalniz hukmu degisti (C kismi).
# ===========================================================================================
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

FOY_YOL = ROOT / "results/C1_REFERANS_FOYU.md"
FOY = FOY_YOL.read_text(encoding="utf-8").split("\n")   # FOY[i-1] = i. satir
_SAYI_RE = re.compile(r"(?<![A-Za-z0-9_.])[-+]?(\d+(?:\.\d+)?(?:e[-+]?\d+)?)(?![A-Za-z0-9_])")


def ondaliklar(metin):
    """Metindeki ondalik (ve bilimsel gosterimli) sayilar, isaretsiz ve kanonik, sirali ve tekil."""
    out = []
    for m in _SAYI_RE.finditer(metin):
        s = m.group(1)
        if "." in s or "e" in s:
            s = sci_kanonik(s)
            if s not in out:
                out.append(s)
    return out


def _dec(s):
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def tamsayilar(metin, en_az=100):
    """Uc ve daha cok basamakli tamsayilar (tohum, epok, goruntu sayisi): yalniz A1 kapsamasi icin."""
    return {m.group(1) for m in _SAYI_RE.finditer(metin)
            if "." not in m.group(1) and "e" not in m.group(1) and int(m.group(1)) >= en_az}


def _foy_virgul(s):
    """Foydeki alintilanmis on kayit esikleri Turkce yazilir ('q >= 0,75'): virgul -> nokta."""
    # Yalniz tek basamakli tam kisim ve bosluk/parantez/karsilastirma/isaretten sonra: '{1,2}' gibi
    # liste ve kume yazimlari ondalik sayilmaz.
    return re.sub(r"(?<=[\s(=<>~+-])(\d),(\d{1,3})(?![\d,])", r"\1.\2", s)


_FOY_SAYI = {i + 1: ondaliklar(_foy_virgul(s)) for i, s in enumerate(FOY)}
_FOY_TAM = {i + 1: tamsayilar(s) for i, s in enumerate(FOY)}
_FOY_DEC = {i: [d for d in (_dec(x) for x in v) if d is not None] for i, v in _FOY_SAYI.items()}
_FOY_TUM = sorted({d for v in _FOY_DEC.values() for d in v})


def tasinir(metin_sayi, foy_degerleri):
    """Metindeki sayi bir foy degerinin TASINMIS hali mi?

    Esit (0.10 = 0.1), ya da foy degeri metnin basamak sayisina yuvarlaninca esit (0.3893 -> 0.389),
    ya da yuzde <-> oran donusumu (44.2 -> 0.442). Bilimsel gosterimde mantis basamagina yuvarlanir."""
    v = _dec(metin_sayi)
    if v is None:
        return False
    if "e" in metin_sayi:
        for u in foy_degerleri:
            if u == v:
                return True
            if u != 0 and v != 0:
                eu, ev = u.adjusted(), v.adjusted()
                if eu == ev:
                    q = Decimal(1).scaleb(ev - max(0, len(metin_sayi.split("e")[0].split(".")[-1]) if "." in metin_sayi.split("e")[0] else 0))
                    if u.quantize(q, ROUND_HALF_UP) == v.quantize(q, ROUND_HALF_UP):
                        return True
        return False
    nd = len(metin_sayi.split(".")[1]) if "." in metin_sayi else 0
    q = Decimal(1).scaleb(-nd)
    for u in foy_degerleri:
        for w in (u, u * 100, u / 100):
            if w.quantize(q, ROUND_HALF_UP) == v:
                return True
    return False


def _bolum_basliklari():
    """Her foy satiri icin en yakin '##'/'###' basligi (yalniz rapor icin)."""
    bas, cur = {}, ""
    for i, s in enumerate(FOY, 1):
        if s.startswith("#"):
            cur = s.lstrip("#").strip()[:48]
        bas[i] = cur
    return bas


_FOY_BASLIK = _bolum_basliklari()


def foy_atiflari(yorum):
    """'% FOY:M9.5:1587,1593 (aciklama) ; 1601-1603' -> [(bolum, satir), ...].

    Bir yorum satirinda birden cok 'FOY:' olabilir; parantez icindeki aciklama atilir,
    kapanmamis parantezden sonrasi da atilir (or. '(FOY:M9.4:1551' satir sonunda kalir)."""
    atif = []
    for parca in yorum.split("FOY:")[1:]:
        p = parca
        while True:
            q = re.sub(r"\([^()]*\)", " ", p)
            if q == p:
                break
            p = q
        p = p.split("(")[0]
        bolum = ""
        for kisim in p.split(";"):
            m = re.match(r"\s*(?:(?P<b>[^:;,\d][^:;]*?)\s*:)?\s*(?P<s>\d[\d\s,\-\u2013]*)", kisim)
            if not m:
                continue
            if m.group("b"):
                bolum = m.group("b").strip()
            for tok in re.split(r"[,\s]+", m.group("s").strip()):
                if not tok:
                    continue
                r_ = re.match(r"^(\d+)[-\u2013](\d+)$", tok)
                if r_:
                    a, b = int(r_.group(1)), int(r_.group(2))
                    atif += [(bolum, n) for n in range(a, b + 1)] if b >= a else [(bolum, a)]
                elif tok.isdigit():
                    atif.append((bolum, int(tok)))
    return atif


def _nitel(yorum):
    """Yorum satiri atfin sayisiz (nitel) oldugunu soyluyor mu ('sayi ozette yok', 'sayisiz')."""
    return bool(re.search(r"\b(yok|sayisiz)\b", yorum.split("FOY:", 1)[-1]))


# LaTeX bicim sayilari (genislik, arraystretch, renk) ve atif/etiket anahtarlari sayi degildir.
_BICIM_RE = [re.compile(p) for p in (
    r"\d*\.?\d+\s*\\(?:textwidth|columnwidth|linewidth|hsize|textheight)",
    r"\\(?:renewcommand|setlength)\{?\\[A-Za-z]+\}?\{[^}]*\}",
    r"\\(?:includegraphics|resizebox|scalebox|rule|vspace|hspace)\*?(?:\[[^\]]*\])?(?:\{[^}]*\})*",
    r"\\(?:begin|end)\{[^}]*\}(?:\[[^\]]*\])?(?:\{[^}]*\})?",
    r"\\(?:ref|eqref|cite|label|cellname|url|href)\{[^}]*\}",
    r"\\(?:multicolumn|multirow)\{[^}]*\}\{[^}]*\}",
)]


def _bicimsiz(t):
    for r_ in _BICIM_RE:
        t = r_.sub(" ", t)
    return t


def gruplar(base, files, norm):
    """Her FOY yorum grubu: dosya, satir, atiflar [(bolum, satir, nitel)], KAYNAK var mi, blok metni."""
    G = []
    for f in files:
        L_ = (ROOT / base / f).read_text(encoding="utf-8").split("\n")
        i, n = 0, len(L_)
        while i < n:
            if not L_[i].lstrip().startswith("%"):
                i += 1
                continue
            j, atif, kaynak = i, [], False
            while j < n and L_[j].lstrip().startswith("%"):
                if "FOY:" in L_[j]:
                    nt = _nitel(L_[j])
                    atif += [(b, s, nt) for b, s in foy_atiflari(L_[j])]
                if "KAYNAK" in L_[j]:
                    kaynak = True
                j += 1
            if not atif:
                i = j
                continue
            blok, k, ort = [], j, 0
            while k < n:
                s = L_[k]
                if s.lstrip().startswith("%"):
                    if "FOY:" in s:
                        break
                    if "KAYNAK" in s:
                        kaynak = True
                    k += 1
                    continue
                if not s.strip() and ort <= 0:
                    break
                ort += len(re.findall(r"\\begin\{(?:table|figure)\*?\}", s)) - len(re.findall(r"\\end\{(?:table|figure)\*?\}", s))
                blok.append(re.sub(r"(?<!\\)%.*", "", s))
                k += 1
            ham = "\n".join(blok)
            G.append({"dosya": f, "satir": i + 1, "atif": atif, "kaynak": kaynak, "blok": norm(ham),
                      "sayilar": ondaliklar(norm(_bicimsiz(ham))),
                      "tamlar": tamsayilar(norm(_bicimsiz(ham))), "sekil": "\\includegraphics" in ham})
            i = j
    return G


def kisim_a(G):
    """A1 (kapi): ondalik sayi tasiyan bir blok, atfettigi foy satirlarindan en az birinin sayisini
    (ondalik, ya da tohum/epok gibi uc+ basamakli tamsayi) tasimali. Ondalik sayisi olmayan blok
    nitel gruptur (FOY yorumu sayisiz bir iddianin kaynagini gosterir) ve yalniz sayilir.
    A2 (kapi): blokta olup foyun HICBIR yerinde tasinmis hali bulunmayan ondalik sayi FOYDE YOK'tur
    (grupta KAYNAK yorumu varsa yalniz bilgi). A3 (bilgi): atfedilen satirda olmayip foyun baska
    satirinda bulunan sayilar ve hicbir sayisi blokta gecmeyen atfedilen satirlar."""
    R_ = {"grup_eksik": [], "foyde_yok": [], "kaynak_yorumlu": [], "atif_disi": [], "satir_kapsanmayan": [],
          "satir_nitel": [], "sekil_grubu": 0, "nitel_grup": 0, "atif_eksik": [], "kaynak_grup_a1": [], "gecersiz_satir": [], "atif": 0, "grup": len(G)}
    for g in G:
        yer = f"{g['dosya']}:{g['satir']}"
        gecerli = []
        for bolum, s, nt in g["atif"]:
            R_["atif"] += 1
            if not (1 <= s <= len(FOY)):
                R_["gecersiz_satir"].append((yer, bolum, s))
                continue
            gecerli.append((bolum, s, nt))
        degerler = [d for _b, s, _n in gecerli for d in _FOY_DEC[s]]
        kapsanan = [x for x in g["sayilar"] if tasinir(x, degerler)]
        tam_ortak = (g["tamlar"] & set().union(*(_FOY_TAM[s] for _b, s, _n in gecerli))) if gecerli else set()
        for bolum, s, nt in gecerli:
            if _FOY_DEC[s] and not any(tasinir(x, _FOY_DEC[s]) for x in g["sayilar"]):
                (R_["satir_nitel"] if nt else R_["satir_kapsanmayan"]).append((yer, bolum, s))
        nitel_hepsi = all(nt for _b, _s, nt in gecerli)
        if not g["sayilar"]:
            R_["nitel_grup"] += 1
        elif degerler and not kapsanan and not tam_ortak and not nitel_hepsi:
            if g["sekil"]:
                R_["sekil_grubu"] += 1
            elif g["kaynak"]:
                R_["kaynak_grup_a1"].append((yer, [s for _b, s, _n in gecerli], g["sayilar"][:8]))
            else:
                R_["grup_eksik"].append((yer, [s for _b, s, _n in gecerli], g["sayilar"][:8]))
        for x in g["sayilar"]:
            if x in kapsanan:
                continue
            if tasinir(x, _FOY_TUM):
                nd = len(x.split("e")[0].split(".")[1]) if "." in x.split("e")[0] else 0
                if not g["kaynak"] and (nd >= 2 or "e" in x):
                    R_["atif_eksik"].append((yer, x))
                else:
                    R_["atif_disi"].append((yer, x))
            elif g["kaynak"]:
                R_["kaynak_yorumlu"].append((yer, x))
            else:
                R_["foyde_yok"].append((yer, x))
    return R_


# --- B. ana manset tasiyicilari: JSON artefaktlarindan ------------------------------------
MANSET, _MANSET_HATA = [], []


def _m(etiket, deger, nd=3):
    MANSET.append((etiket, f"{abs(float(deger)):.{nd}f}"))


try:
    _b2 = jl("results/q1/konsey_ayrisim_b2.json")["b2"]["F_B2"]
    _b9 = jl("results/q1/konsey_b9_c100/b9_dondurulmus_b2.json")["b2"]["F_B2"]
    _b4 = jl("results/q1/konsey_ayrisim_b4.json")["b4"]["F_B4"]["karsitliklar"]
    _b5 = jl("results/q1/konsey_ayrisim_b5.json")["b5"]["birincil_C1-R32_V-scr"]
    _b6 = jl("results/q1/konsey_b6_maskeleme.json")["modeller"]
    _b8 = jl("results/q1/konsey_b8_imagenetv2/b8_betimsel.json")
    for _h in ("H1", "H2", "H3"):
        _m(f"{_h} kestirim (B4)", _b4[_h]["kestirim"])
        _m(f"{_h} %90 alt (B4)", _b4[_h]["ci90"][0])
        _m(f"{_h} %90 ust (B4)", _b4[_h]["ci90"][1])
    for _vk, _F in (("CIFAR-10 B2", _b2), ("CIFAR-100 B9", _b9)):
        _m(f"K-a ort q {_vk}", _F["K-a"]["sinama"]["ort"])
        _m(f"K-a %90 alt {_vk}", _F["K-a"]["sinama"]["ci90"][0])
        _m(f"K-a %90 ust {_vk}", _F["K-a"]["sinama"]["ci90"][1])
        _m(f"K-b rho(V-scr) {_vk}", _F["K-b"]["ort"])
        _m(f"K-b %90 alt {_vk}", _F["K-b"]["ci90"][0])
        _m(f"K-b %90 ust {_vk}", _F["K-b"]["ci90"][1])
        _m(f"K-c Delta_seed {_vk}", _F["K-c"]["Delta_w"])
        _m(f"K-c %90 alt {_vk}", _F["K-c"]["bootstrap"]["ci90"][0])
        _m(f"K-c %90 ust {_vk}", _F["K-c"]["bootstrap"]["ci90"][1])
    _m("korunma orani G_best/G_PGD (B5)", _b5["oran"])
    _m("korunma orani %90 alt (B5)", _b5["bootstrap"]["ci90"][0])
    _m("korunma orani %90 ust (B5)", _b5["bootstrap"]["ci90"][1])
    _fk = [v["fark_puan"] for v in _b6.values()]
    _m("B6 en buyuk PGD-10 - AA farki (puan)", max(_fk), 2)
    _m("B6 en kucuk PGD-10 - AA farki (puan)", min(_fk), 2)
    _m("A^sigma_IN (B8)", _b8["A_sigma_IN"]["kestirim"])
    _m("A^sigma_IN %90 alt (B8)", _b8["A_sigma_IN"]["goruntu_bootstrap"]["ci90"][0])
    _m("A^sigma_IN %90 ust (B8)", _b8["A_sigma_IN"]["goruntu_bootstrap"]["ci90"][1])
    _m("A^sigma_scr Liu (B8)", _b8["A_sigma_scr_Liu"]["kestirim"])
    for _vk in ("cifar10", "cifar100", "imagenetv2"):
        _ms_ = jl(f"results/q1/konsey_b10_gradyan/mantel_{_vk}.json")["sinamalar"]
        _m(f"Mantel r ham {_vk} (B10)", _ms_["ham"]["istatistik"])
        _m(f"Mantel r ana etki artik {_vk} (B10)", _ms_["ana_etki_artik"]["istatistik"])
except Exception as _e_:  # anahtar degisirse kapi SESSIZCE gecmesin
    _MANSET_HATA.append(f"{type(_e_).__name__}: {_e_}")

_M9_BAS = next((i for i, s in enumerate(FOY) if s.startswith("## M9:")), None)
_M10_SON = next((i for i, s in enumerate(FOY) if s.startswith("## Sabit dizgeler")), len(FOY))
FOY_M9_M10 = norm_en("\n".join(FOY[_M9_BAS:_M10_SON])) if _M9_BAS is not None else ""
if _M9_BAS is None:
    _MANSET_HATA.append("foyde '## M9:' basligi yok")


def kisim_b(txt):
    sat, eksik = [], 0
    for et, v in MANSET:
        f_ok = tam_eslesme(v, FOY_M9_M10) > 0
        t_ok = tam_eslesme(v, txt) > 0
        if not (f_ok and t_ok):
            eksik += 1
        sat.append((et, v, f_ok, t_ok))
    return sat, eksik


# --- C. eski kontroller: yalniz bilgi ---------------------------------------------------------
def kisim_c(txt):
    """Eski listede metinde kalan 'korunuyor', kalmayan 'dustu (brif §5.10)'. Korunan eski
    tasiyicilarin degeri A kismindaki FOY atiflariyla zaten denetlenir; burada kapi YOK."""
    sonuc = {"korunuyor": [], "dustu": []}
    for label, val in CHECKS:
        (sonuc["korunuyor"] if tam_eslesme(val, txt) > 0 else sonuc["dustu"]).append((label, val))
    return sonuc


def dil_denetimi(dil, base, files, norm):
    G = gruplar(base, files, norm) if files else []
    return G, kisim_a(G), kisim_b(LANGS[dil]), kisim_c(LANGS[dil])


def yaz_dil(dil, G, a, b, c, tam):
    sat_b, eksik_b = b
    eksik_a = len(a["grup_eksik"]) + len(a["foyde_yok"]) + len(a["atif_eksik"]) + len(a["gecersiz_satir"])
    print("=" * 78)
    print(f"[{dil}] dosyalar: {', '.join(EN_FILES if dil == 'EN' else TR_FILES) or 'YOK'}")
    print(f"[{dil}] A. FOY yorumlari: {a['grup']} grup, {a['atif']} satir atfi. EKSIK {eksik_a} "
          f"(A1 grup bloku atfedilen satirlarin hicbir sayisini tasimiyor {len(a['grup_eksik'])}; "
          f"A2 foyde yok {len(a['foyde_yok'])}; A3 atif eksik {len(a['atif_eksik'])}; "
          f"gecersiz satir no {len(a['gecersiz_satir'])})")
    for yer, bolum, s in a["gecersiz_satir"]:
        print(f"    EKSIK  {yer}  FOY:{bolum}:{s}  -- foy {len(FOY)} satir; satir numarasi disarida")
    for yer, sat, ornek in a["grup_eksik"]:
        print(f"    EKSIK  {yer}  FOY satirlari {', '.join(map(str, sat[:10]))}{' ...' if len(sat) > 10 else ''}  "
              f"-- blokta bu satirlarin hicbir sayisi yok; blok sayilari: {', '.join(ornek) or '-'}")
    for yer, x in a["foyde_yok"]:
        print(f"    EKSIK  {yer}  {x}  -- FOYDE YOK: foyun hicbir satirinda tasinmis hali yok ve grupta KAYNAK yorumu yok")
    for yer, x in a["atif_eksik"]:
        sat = [i for i, v in _FOY_DEC.items() if tasinir(x, v)]
        print(f"    EKSIK  {yer}  {x}  -- ATIF EKSIK: atfedilen foy satirlarinda yok, foyde baska satirda var "
              f"({', '.join(map(str, sat[:5]))}{' ...' if len(sat) > 5 else ''}); yanlis sayi ya da eksik FOY atfi")
    print(f"    bilgi: atif disi (foyde var, atfedilen satirda yok; tek ondalikli ya da KAYNAK yorumlu grupta) {len(a['atif_disi'])}; KAYNAK yorumlu blokta foyde "
          f"olmayan {len(a['kaynak_yorumlu'])}; hicbir sayisi blokta gecmeyen atfedilen satir {len(a['satir_kapsanmayan'])} "
          f"(nitel isaretli {len(a['satir_nitel'])}); ondalik sayisiz (nitel) grup {a['nitel_grup']}; "
          f"sekil grubu (sayilar PDF'te) {a['sekil_grubu']}; KAYNAK yorumlu grupta A1 kapsamasi yok "
          f"{len(a['kaynak_grup_a1'])}")
    if ARGS.ayrinti:
        for yer, x in a["atif_disi"]:
            sat = [i for i, v in _FOY_DEC.items() if tasinir(x, v)]
            print(f"      atif disi  {yer}  {x}  (foy satiri: {', '.join(map(str, sat[:5]))}{' ...' if len(sat) > 5 else ''})")
        for yer, x in a["kaynak_yorumlu"]:
            print(f"      KAYNAK yorumlu  {yer}  {x}")
        for yer, sat, ornek in a["kaynak_grup_a1"]:
            print(f"      KAYNAK yorumlu grup, A1 kapsamasi yok  {yer}  FOY {', '.join(map(str, sat[:6]))}; "
                  f"blok: {', '.join(ornek)}")
        for yer, bolum, s in a["satir_kapsanmayan"]:
            print(f"      kapsanmayan atif  {yer}  FOY:{bolum}:{s} [{_FOY_BASLIK.get(s, '-')}]")
    print(f"[{dil}] B. Ana manset tasiyicilari: {len(sat_b)} kalem, EKSIK {eksik_b}")
    if tam:
        for et, v, f_ok, t_ok in sat_b:
            print(f"    {'OK   ' if (f_ok and t_ok) else 'EKSIK'}  {et[:46]:46s} {v:>8s}  foy M9-M10: "
                  f"{'var' if f_ok else 'YOK'}  metin: {'var' if t_ok else 'YOK'}")
    print(f"[{dil}] C. Eski kontroller ({len(CHECKS)}, yalniz bilgi): metinde korunuyor {len(c['korunuyor'])}; "
          f"dustu (brif §5.10), kapi disi {len(c['dustu'])}")
    if tam and ARGS.ayrinti:
        for label, val in c["dustu"]:
            print(f"      dustu (brif §5.10)  {label} = {val}")
    return eksik_a + eksik_b


print(f"Foy: {FOY_YOL.relative_to(ROOT)} ({len(FOY) - 1 if FOY and FOY[-1] == '' else len(FOY)} satir)")
G_en, a_en, b_en, c_en = dil_denetimi("EN", EN_BASE, EN_FILES, norm_en)
en_eksik = yaz_dil("EN", G_en, a_en, b_en, c_en, tam=True)
if TR_FILES and LANGS["TR"].strip():
    G_tr, a_tr, b_tr, c_tr = dil_denetimi("TR", TR_BASE, TR_FILES, norm_tr)
    tr_eksik = yaz_dil("TR", G_tr, a_tr, b_tr, c_tr, tam=ARGS.tr_zorunlu)
else:
    tr_eksik = None
    print("UYARI: TR metni okunamadi (dosya adlari degismis olabilir).")

print("=" * 78)
for _h in _EN_HATA + _MANSET_HATA:
    print(f"KAPI HATASI (artefakt okunamadi): {_h}")
print(f"TOPLAM: A grup={a_en['grup']} atif={a_en['atif']}  B manset={len(MANSET)}  C eski={len(CHECKS)} "
      f"(dustu {len(c_en['dustu'])})  EN_EKSIK={en_eksik}  "
      f"TR_EKSIK={tr_eksik if tr_eksik is not None else 'okunamadi'}{'' if ARGS.tr_zorunlu else ' (TR yalniz bilgi)'}")
kaldi = bool(en_eksik or _EN_HATA or _MANSET_HATA
             or (ARGS.tr_zorunlu and (tr_eksik is None or tr_eksik)))
if kaldi:
    print("SONUC: KALDI -- FOY atfi, foyde olmayan sayi ya da manset tasiyicisi sorunu var (ya da artefakt okunamadi).")
    sys.exit(1)
print("SONUC: GECTI -- FOY atiflari bloklarinda, bloklardaki sayilar foyde, manset tasiyicilari foyde ve metinde.")
sys.exit(0)
