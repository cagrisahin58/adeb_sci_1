r"""Makaledeki tasiyici sayilarin referans foyu ve artefaktlarla tutarliligini denetler.

TASARIM (2026-10-31, konsey manseti; brif 12 §5.10, not 14; ayni gun ikinci surum: celisik
dogrulayicinin K1, K2, S1-S3, Y1-Y3 bulgulari; UCUNCU ve son surum: ikinci dogrulayicinin K1b,
S1b, T1, Y1-Y4 bulgulari, asagida [3] ile isaretli). Tasiyici kumesi elle tutulan bir liste
DEGIL, metnin kendi `% FOY:<bolum>:<satir>` ve `% KAYNAK:` yorumlarindan turetilir. Iki kapi
(A, B) ve bir bilgi kismi (C) vardir.

[3] GRUP TANIMI (K1b). Ardisik yorum satirlarindan olusan bir yorum blogu, icinde FOY atfi,
'% KAYNAK:' ya da '% YON:' yorumu varsa GRUPTUR. FOY atfi olmayan grup "KAYNAK-yalniz" gruptur
(atif bos, kaynak anahtarlari dolu): blogundaki her ondalik ve iki+ basamakli tamsayi KAYNAK
yorumunda yazili bir degerle ya da SABIT ile kapsanmiyorsa EKSIK (KAYNAK DEGER EKSIK; foyde
bulunsa bile, cunku blok foy satiri atfetmiyor). Grubun blogu bitince tarama blogun sonundan
surer (blok icindeki KAYNAK yorumu yeni grup acmaz, blogun grubuna eklenir).
[3] GRUPSUZ (K1b). Hicbir grubun blogunda olmayan, yorum disindaki her ondalik ve iki+ basamakli
tamsayi (ad parcalari, surumler ve baglamli SABIT haric) EKSIK (GRUPSUZ).
[3] KAYNAK BELGESI (Y2). KAYNAK yorumunda acikca yazili bir deger bir metin sayisini kapsiyorsa,
o metin sayisi yorumun ADINI VERDIGI belgede de bulunmalidir: ON_KAYIT ->
raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md (Dondurma eki dahil); EK ->
ON_KAYIT_EK_B8_B10_2026-10-30.md; CLAUDE.md; brif -> 12_makale_revizyon_brifi.md; R09/R11 ->
konsey dizininde 09_*/11_*; acik yol (raporlar/..., results/...) ya da raporlar/ ve results/
altinda tekil dosya adi (.md/.json/.txt). 'eski metin' bir belge degildir. Belge adi yoksa ya da
deger belgede yoksa EKSIK (KAYNAK BELGEDE YOK). Belge okunurken U+2212, Turkce ondalik virgul,
binlik ayraclari ve 10⁻⁴ ust simgeleri taninir. results/<yol>.json#anahtar ile adlandirilan JSON
yapraklari dosyadan okundugu icin ayrica aranmaz. Yorumdaki 'a-b' tamsayi araligi iki ucu da
yazili sayar (ic degerleri degil).
[3] TERS ARALIK (T1). Metindeki her [a, b], [a; b] ve a--b (en tire dahil) icin a > b ise EKSIK.
Metindeki aralik foyde ters yonde ([b, a]) bulunuyorsa DEMET EKSIK.
[3] YON (Y1). 'excludes/includes/contains/spans zero' iceren her cumle (grup ici ya da grupsuz)
denetlenebilir bir araliga baglanmalidir: ifadeden once gelen en yakin [a, b] ya da 'a to b'
araligi (yoksa sonraki ilk aralik); cumlede aralik yoksa grubun '% YON: [a; b] FOY:<b>:<s>'
yorumu (aralik o foy satirinda birlikte bulunmali). Hicbiri yoksa EKSIK (YON DENETLENEMEDI).
Sayisiz kural cumleleri (karar kurali tablosu gibi) icin grup '% YON: kural' yorumu tasir.
[3] KOPYA (S1b). Bir manset/ozet kaleminin iki anlamli rakami yer degistirmis hali (0.936 ->
0.963; 0.003 -> 0.030 gibi basamak kaymasi degil), kalemin AYNEN yazili oldugu foy satirini
atfeden bir blokta duruyorsa, deger blogun atif satirlarinda bulunsa bile EKSIK; kosul: (a) blok
ozette ve kalem blokta yok, ya da (b) blogun yorumu kalemi aniyor ve takasli degeri anmiyor.
Karar: kural metnin yalniz 'kalem blokta yoksa' kosuluyla uygulandiginda 04:228'deki mesru
jackknife degeri -0.346'yi (H1 -0.364 icin foy 1550'yi atfeden blok) yanlislikla yakaliyordu;
(a)/(b) kosulu blogun o kalemi tasimak uzere atfedildigini sart kosar. Yakinlik (en cok 3
birim) ve ters isaret icin eski KOPYA (i) kurali (atfedilen satirda yoksa EKSIK) aynen durur.
[3] OZ-SINAMA (Y3) her sinamada uygulanabilen BUTUN adaylari (en cok 5) bozar; her biri
yakalanmalidir. kapilar.sh oz-sinama KALDI verirse zinciri hemen durdurur (Y4).
[3] `--eksik-json <yol>` EKSIK kalemlerini tur, dosya, satir ve oneriyle (foy satirlari, belge
satirlari) JSON olarak yazar; arsiv/b2_yardimci/_kapi_eksik_rapor.py bundan yazar listesini kurar.

SAYI AYRISTIRMA (K2, isarete duyarli). Metin ve foy ayni kurallarla okunur: -0.364, $-0.364$,
\(-0.364\), U+2212, \textminus, \minus, \ensuremath{-}, $-$0.364 ve {-}0.364 hepsi NEGATIF
0.364'tur; \pm, U+00B1, +- ve +/- ayractir. 'ResNet-18', 'CIFAR-10', 'WRN-28-10' ad parcasidir;
'36--58' aralik tiresidir; surum dizgeleri (2.6.0, 1.26.4) sayi degildir. "Tasinmis" esleme:
esit, foy degeri metnin basamak sayisina yuvarlaninca esit, yuzde <-> oran (44.2 -> 0.442),
bilimsel gosterimde mantis yuvarlamasi; HER BIRINDE ISARET AYNI olmalidir (+ ile isaretsiz ayni
siniftir, negatif ayri; sifira yuvarlanan isaretsizdir). Tamsayilar yalniz esitlikle eslesir.

  A. FOY yorumlarindan turetilen tasiyicilar (KAPI). Her ardisik yorum grubundaki FOY atiflari
     (bolum etiketi, satir listesi ve araliklar; parantez icindeki aciklama atilir) okunur. Grubun
     BLOGU, gruptan sonraki metin satirlaridir; bir sonraki FOY yorumunda ya da bos satirda biter
     (acik table/figure ortami bos satirda bitmez). Bloktaki her ondalik sayi (bilimsel dahil) ve
     iki ve daha cok basamakli her tamsayi (tohum, n, epok; S3) denetlenir:
       A1  ondalik sayi tasiyan blok, atfettigi satirlarin hicbir sayisini (ondalik ya da uc+
           basamakli tamsayi) tasimiyorsa EKSIK. Sekil blogu yalniz bilgi.
       A2  foyun HICBIR satirinda isaretiyle tasinmis hali olmayan sayi EKSIK (FOYDE YOK); yalniz
           ters isaretlisi varsa ya da atfedilen satirda ters isaretli duruyorsa EKSIK (ISARET).
       A3  atfedilen satirlarda olmayip foyun baska satirinda bulunan iki+ ondalikli, bilimsel ya
           da tamsayi deger EKSIK (ATIF EKSIK). Tek ondalikli sayilar (asama.blok etiketi) bilgi.
       KAYNAK (K1). '% KAYNAK:' yorumu grubu MUAF TUTMAZ. Yalniz (i) yorumda acikca yazili
           degerleri ('delta = 0.10', 'n = 500'; Sec./satir/dosya:satir gostergeleri sayilmaz) ve
           (ii) 'results/<yol>.json#anahtar.alt' bicimiyle adlandirilan dosyadan OKUNAN sayisal
           yapraklari kapsar; okunamayan JSON atfi EKSIK. Grubun oteki sayilari A1-A3'e tabidir.
           [3] (i) kapsamindaki deger adlandirilan belgede de bulunmalidir (KAYNAK BELGESI); FOY
           atfi olmayan grupta KAYNAK ya da SABIT disi her sayi EKSIK (KAYNAK DEGER EKSIK).
       SABIT (S3). scripts icindeki SABITLER listesi (eps 8/255, PGD 10 adim, L2 eps 0.5, delta
           0.10, alfa 0.05, %90/%95, tohum 42, brif 12 §10 donanim/yazilim surumleri): her kalem
           baglam duzenli ifadesine baglidir, kaynagi yorumdadir.
       DEMET (S1, K2). 'kestirim [alt, ust]' ve 'ortalama ± SD' ayni foy satirinda BIRLIKTE
           bulunmali (kestirim ayri satirdaysa en cok iki satir yukarida, ara satirda baska ondalik
           yokken). Ogeleri foyde olup birlikte hicbir satirda olmayan demet EKSIK (DEMET: iki
           atfedilen satir arasinda deger takasi); birlikte yalniz atfedilmeyen satirda olan EKSIK
           (DEMET ATIF EKSIK). Aralik uclari isaretleriyle denetlenir.
       YON (K2, [3] Y1 ile genisletildi). 'excludes zero' yazan ifadenin baglandigi aralik sifiri
           dislamali, 'includes/contains/spans zero' yazanin icermeli; degilse EKSIK. Baglama kurali ve
           aralik bulunamayan cumle icin yukaridaki [3] YON maddesine bakin. 'negative/positive'
           yalniz sayilir (bilgi): isaret dogrulugu sayilarin kendi isaret denetimindedir.
       UST SINIR (Y2). 'p < B' bicimindeki sinir yuvarlamayla eslesmez. Gecer ancak (a) B atfedilen
           bir satirda AYNEN yaziliysa (or. p tabani 1.00e-04) ya da (b) atfedilen satirlarin foy
           paragrafinda 'metne girecek ... sinir' satiri B'yi veriyorsa ve B paragraftaki en buyuk
           p'den kucuk degilse. Aksi EKSIK (UST SINIR); metin degistirilmez, raporlanir.
     Foy disinda satir numarasi EKSIK. Hicbir sayisi blokta gecmeyen tek tek atiflar bilgi.

  B. Ana manset ve ozet tasiyicilari (KAPI).
     B-JSON: H1/H2/H3, K-a/K-b/K-c (CIFAR-10 B2, CIFAR-100 B9), korunma orani (B5),
       A^sigma_IN (B8) kestirim ve %90 araliklari; B6 en buyuk/en kucuk PGD-10 - AA farki; Liu
       cifti; alti Mantel r (B10). Degerler JSON artefaktlarindan ISARETIYLE hesaplanir; foyun
       M9-M10 bolumunde ve metinde gecmelidir.
     B-OZET (S2): main.tex'teki \begin{abstract} icindeki HER sayi (tasarim sabitleri haric)
       otomatik kalem olur: foyde (isaretiyle) ve GOVDEDE (ozet disi metin, ayni isaret) gecmelidir.
     KOPYA (S1): metindeki BUTUN kopyalar birebir olmalidir. (i) Bir manset/ozet kalemiyle ayni
       basamakli, en cok 3 birim farkli, rakamlari yer degistirmis ya da ters isaretli bir sayi,
       bulundugu FOY grubunun atfettigi satirlarda (grup disindaysa foyun herhangi bir satirinda)
       yoksa EKSIK (olasi bozuk kopya). (ii) 'kestirim [alt, ust]' demetinin uc ogesinden ikisi bir
       manset/ozet demetiyle ayni, biri farkliysa EKSIK (demet tutarsiz). Tek kopyanin bozulmasi
       da boylece KALDI verir.

  C. Eski artefakt kontrolleri (2026-08 .. 2026-10 listesi, 426 kalem, degistirilmedi): YALNIZ
     BILGI, kapi disi. Metinde kalan kalem "korunuyor", kalmayan "dustu (brif §5.10)" diye
     sayilir; metinde kalanlarin degeri A kismindaki FOY atiflariyla denetlenir. (Onceki
     docstring C'yi kosullu zorunlu anlatiyordu; kod hep bilgi olarak raporladi. Y1: belge koda
     uyduruldu.)

IKI DIL: EN (paper/manuscript) ve TR (paper/manuscript_tr) AYRI AYRI denetlenir. Dosya
listesi main.tex'teki \\input / \\InputIfFileExists satirlarindan okunur (Ek ve hesaplama
ayrintilari dahil). GRUPSUZ taramasi main.tex'te \begin{document}'ten baslar (DOI, cilt, yil, posta
kodu ust veridir); ay adindan ya da kisaltmadan sonra gelen 1990-2030 yili ('October 2026', 'ATEEC
2026') takvim/etkinlik adidir; \tfrac12 ve sayisal alt simge indisleri (\ell_{12}) sayi degildir.
TR aynasi henuz esitlenmedigi icin TR sonucu varsayilan olarak
YALNIZ BILGIDIR; `--tr-zorunlu` ile kapiya katilir.
DIKKAT -- `{,}` makrosu iki dilde FARKLI anlama gelir:
  EN : binlik ayraci   ->  10{,}000  = 10000   => "{,}" SILINIR
  TR : ondalik ayraci  ->  10{,}45   = 10.45   => "{,}" NOKTAYA cevrilir
Ayni normalleştirmeyi iki dile uygulamak sessiz "EKSIK" raporlari uretir.

OZ-SINAMA: scripts/test_verify_manuscript_numbers.py (gecici kopyada bozmalar; kapilar.sh'nin
ilk adimi). Cikis 0 = GECTI, 1 = KALDI. `--ayrinti` bilgi listelerini de basar; `--dokum
<json>` oz-sinamanin kullandigi grup/belirtec/manset dokumunu yazar.
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
_AP.add_argument("--ayristirma-sinami", action="store_true",
                 help="Yalniz isaret/sayi ayristirma vakalarini sina ve cik (oz-sinamanin ilk adimi).")
_AP.add_argument("--dokum", default=None,
                 help="Oz-sinama icin grup/belirtec/manset dokumunu bu JSON yoluna yaz.")
_AP.add_argument("--eksik-json", default=None,
                 help="EKSIK kalemlerini tur/dosya/satir/oneri ile bu JSON yoluna yaz (yazar listesi icin).")
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
# YENI RAPOR (2026-10-31, ikinci surum; dogrulayici bulgulari K1, K2, S1-S3, Y1-Y3).
# A FOY yorumlari, B ana manset + ozet, C eski kontroller (yalniz bilgi). Yukaridaki CHECKS
# listesi degistirilmeden hesaplanir; yalniz hukmu bilgidir (C kismi).
# ===========================================================================================
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

FOY_YOL = ROOT / "results/C1_REFERANS_FOYU.md"
FOY = FOY_YOL.read_text(encoding="utf-8").split("\n")   # FOY[i-1] = i. satir

# --- S3: tasarim sabitleri ------------------------------------------------------------------
# Foyde (sonuc sayisi olarak) bulunmayan ama metne girmesi gereken TASARIM sabitleri. Liste
# bilerek kucuk tutulur ve her kalem BAGLAMA baglidir (once/sonra duzenli ifadesi): '16' yalniz
# 'GB'den once, '42' yalniz 'seed' sozcugunden sonra sabit sayilir; baska yerde gecen ayni sayi
# normal A2/A3 denetimine girer. Kaynaklar yorumdadir; listeye sonuc sayisi EKLENMEZ.
SABITLER = [
    # (deger, once (satirda sayidan hemen once), sonra (hemen sonra), kaynak)
    ("255", r"/\s*$", None, "eps = 8/255, alpha = 2/255 paydasi (CLAUDE.md Adversarial Training Parametreleri)"),
    ("10", r"(?i)(PGD|steps?|iterations?|adim)\W{0,3}$", r"(?i)^\W{0,3}(steps?|iterations?|adim)", "PGD adim sayisi steps = 10 (CLAUDE.md)"),
    ("0.5", r"(?i)(epsilon|eps|\\epsilon|varepsilon|L_?2|ell_2|ell_ 2)[^0-9]{0,12}$", None, "L2 eps = 0.5 (ON_KAYIT; 07_appendix KAYNAK: tasarim sabiti)"),
    ("0.10", r"(\\delta|delta|±|\\pm)\s*=?\s*$", None, "esdegerlik siniri delta = 0.10 (ON_KAYIT Sec. 5)"),
    ("0.1", r"(\\delta|delta|±|\\pm)\s*=?\s*$", None, "esdegerlik siniri delta = 0.10 (ON_KAYIT Sec. 5)"),
    ("0.05", r"(?i)(\bp\s*(<|=|\\le|\\leq|≤)|alpha\s*=?|\\alpha\s*=?|level\s*(of)?)\s*$", None, "anlamlilik ve Holm alfa 0.05 (ON_KAYIT Sec. 6)"),
    ("90", None, r"^\s*\\?%", "%90 araliklar (ON_KAYIT Sec. 5 karar ilkesi)"),
    ("95", None, r"^\s*\\?%", "%95 araliklar (ON_KAYIT Sec. 5)"),
    ("42", r"(?i)seed\s*$", None, "deterministik cuDNN, tohum 42 (brif 12 §10; eski metin 04:638 ve 03:192)"),
    ("16", None, r"^\s*GB", "RTX 5060 Ti 16 GB (brif 12 §10; CLAUDE.md Donanim)"),
    ("32", None, r"^\s*GB", "RTX 5090 32 GB (brif 12 §10; CLAUDE.md Donanim)"),
    ("5060", r"(?i)RTX\s*$", None, "RTX 5060 Ti (brif 12 §10)"),
    ("5090", r"(?i)RTX\s*$", None, "RTX 5090 (brif 12 §10)"),
    ("12.8", r"(?i)CUDA\s*$", None, "CUDA 12.8 (brif 12 §10; CLAUDE.md)"),
    ("25.01", r"(?i)(nv|NVIDIA|container|release)[^0-9]{0,12}$", None, "NVIDIA PyTorch kapsayicisi nv25.01 (brif 12 §10; pip_freeze)"),
    ("32", r"\\times\s*$", r"(?i)^(\s*-\s*|\s+)pixel|^\s*\\times\s*32\b", "girdi cozunurlugu 32x32 (CIFAR; ON_KAYIT Sec. 3 hucre tanimlari, R32)"),
    ("224", r"\\times\s*$", r"(?i)^(\s*-\s*|\s+)pixel|^\s*\\times\s*224\b", "girdi cozunurlugu 224x224 (ON_KAYIT Sec. 3 hucre tanimlari, R224/V)"),
]
_SABIT_RE = [(d, re.compile(o) if o else None, re.compile(s) if s else None, k) for d, o, s, k in SABITLER]


def sabit_mi(tk, once, sonra):
    if tk.neg:
        return None
    for d, o, s, k in _SABIT_RE:
        if tk.k == d and ((o is None and s is None) or (o is not None and o.search(once))
                          or (s is not None and s.search(sonra))):
            return k
    return None


# --- K2: isarete duyarli sayi ayristirma -----------------------------------------------------
def _duz(t):
    """Isaret ve matematik kipi bicimlerini duzle: -0.364, $-0.364$, \\(-0.364\\), U+2212, \\textminus,
    \\minus, \\ensuremath{-}, $-$0.364, {-}0.364 hepsi '-0.364' olur; \\pm, U+00B1, +- ve +/- ' ± ' olur."""
    t = t.replace("\u2212", "-").replace("\u2013", "--").replace("\u00b1", " ± ")
    t = re.sub(r"\\(?:textminus|minus)(?![A-Za-z])\s*", "-", t)
    t = re.sub(r"\\ensuremath\{\s*([-+])\s*\}", r"\1", t)
    t = re.sub(r"\$\s*([-+])\s*\$", r"\1", t)
    t = re.sub(r"\{\s*([-+])\s*\}", r"\1", t)
    t = re.sub(r"\$?\\pm(?![A-Za-z])\$?|\+/-|\+-(?=\s*\d)", " ± ", t)
    t = re.sub(r"\\[()]", " ", t)
    t = t.replace("$", " ").replace("~", " ")
    t = re.sub(r"\\[,;:!]", " ", t)
    return re.sub(r"(\\[A-Za-z]+)(?=[-+\d.])", r"\1 ", t)


_NUM = re.compile(r"(?<![A-Za-z0-9_.])(\d+(?:\.\d+)?(?:e[-+]?\d+)?)(?![A-Za-z0-9_])")


class Tok:
    __slots__ = ("k", "neg", "nd", "tam", "sci", "a", "b")

    def __init__(self, k, neg, nd, tam, sci, a, b):
        self.k, self.neg, self.nd, self.tam, self.sci, self.a, self.b = k, neg, nd, tam, sci, a, b

    def goster(self):
        return ("-" if self.neg else "") + self.k


def tokenler(t, tam_en_az=10):
    """Duzlenmis metindeki sayilar (isaretli). Ondaliklarin hepsi; tamsayilar >= tam_en_az.
    Isaret: hemen onceki '-' ya da '+' sayinin isaretidir, ONCESINDE harf/rakam/nokta/kapanis yoksa.
    'ResNet-18', 'CIFAR-10', 'WRN-28-10', 'ViT-B/16' tamsayilari ad parcasidir, atlanir; '36--58'
    aralik tiresidir (58 isaretsiz). Surum dizgeleri (2.6.0, 1.26.4) sayi degildir."""
    out = []
    for m in _NUM.finditer(t):
        s, a, b = m.group(1), m.start(1), m.end(1)
        if t[b:b + 1] == "." and t[b + 1:b + 2].isdigit():
            continue
        neg = bitisik = False
        if a >= 1 and t[a - 1] in "-+":
            o = t[a - 2] if a >= 2 else " "
            if t[a - 1] == "-" and o == "-":
                pass
            elif o.isalnum() or o in "._)]}/'":
                bitisik = True
            else:
                neg = t[a - 1] == "-"
        sci = "e" in s
        tam = not sci and "." not in s
        if tam:
            if bitisik or int(s) < tam_en_az:
                continue
            if a >= 2 and t[a - 1] == "/" and t[a - 2].isalpha():
                continue
        k = sci_kanonik(s) if sci else s
        nd = len(k.split("e")[0].split(".")[1]) if "." in k.split("e")[0] else 0
        if Decimal(k) == 0:
            neg = False
        out.append(Tok(k, neg, nd, tam, sci, a, b))
    return out


_Q = {n: Decimal(1).scaleb(-n) for n in range(0, 10)}


def anahtar(tk, neg=None):
    """Metin sayisinin eslesme anahtari (isaretli). neg verilirse isaret onunla degistirilir."""
    neg = tk.neg if neg is None else neg
    v = Decimal(tk.k)
    if v == 0:
        neg = False
    if tk.tam:
        return ("i", neg, int(v))
    if tk.sci:
        mant = tk.k.split("e")[0]
        md = len(mant.split(".")[1]) if "." in mant else 0
        e = v.adjusted()
        return ("e", neg, e, md, v.scaleb(-e).quantize(_Q[md], ROUND_HALF_UP))
    return ("d", neg, tk.nd, v)


def ters(key):
    return (key[0], not key[1]) + key[2:]


def deger_anahtarlari(v, neg):
    """Bir foy (ya da KAYNAK) degerinin metinde TASINMIS hallerinin anahtarlari: esit, metnin basamak
    sayisina yuvarlanmis (1-9 ondalik), yuzde <-> oran (x100, /100); bilimsel gosterimde mantis 0-4
    basamaga yuvarlanmis; tamsayi YALNIZ esitlikle. Isaret korunur; sifira yuvarlanan isaretsizdir."""
    K = set()
    if v == v.to_integral_value():
        K.add(("i", neg and v != 0, int(v)))
    for w in (v, v * 100, v / 100):
        for nd in range(1, 10):
            q = w.quantize(_Q[nd], ROUND_HALF_UP)
            K.add(("d", neg and q != 0, nd, q))
    if v != 0:
        e = v.adjusted()
        m_ = v.scaleb(-e)
        for md in range(0, 5):
            K.add(("e", neg, e, md, m_.quantize(_Q[md], ROUND_HALF_UP)))
    return K


def _foy_virgul(s):
    """Foydeki alintilanmis on kayit esikleri Turkce yazilir ('q >= 0,75'): virgul -> nokta."""
    # Yalniz tek basamakli tam kisim ve bosluk/parantez/karsilastirma/isaretten sonra: '{1,2}' gibi
    # liste ve kume yazimlari ondalik sayilmaz.
    return re.sub(r"(?<=[\s(=<>~+-])(\d),(\d{1,3})(?![\d,])", r"\1.\2", s)


_ARALIK = re.compile(r"\[([^\[\]]{1,80})\]")


def araliklar(t):
    """'[a, b]' / '[a; b]' (duzlenmis) -> [(bas, son, Tok a, Tok b)]; en az bir uc ondalik olmali."""
    out = []
    for m in _ARALIK.finditer(t):
        ic = m.group(1)
        if re.search(r"[A-DF-Za-df-z]", ic):
            continue
        ts = tokenler(ic, tam_en_az=0)
        if len(ts) == 2 and not (ts[0].tam and ts[1].tam):
            out.append((m.start(), m.end(), ts[0], ts[1]))
    return out


# --- foy dizini --------------------------------------------------------------------------------
FOY_DUZ = {i + 1: _duz(_foy_virgul(s)) for i, s in enumerate(FOY)}
FOY_TOK = {i: tokenler(t, tam_en_az=0) for i, t in FOY_DUZ.items()}
FOY_KEYS, KEY_LINES = {}, defaultdict(set)
_TOK_KEYS = {}
for _i, _ts in FOY_TOK.items():
    _K = set()
    for _t in _ts:
        _tk = deger_anahtarlari(Decimal(_t.k), _t.neg)
        _TOK_KEYS[(_i, _t.a)] = _tk
        _K |= _tk
    FOY_KEYS[_i] = _K
    for _k in _K:
        KEY_LINES[_k].add(_i)
FOY_ARALIK = {}
for _i, _t in FOY_DUZ.items():
    _ar = []
    for _s0, _s1, _ta, _tb in araliklar(_t):
        _ar.append((deger_anahtarlari(Decimal(_ta.k), _ta.neg), deger_anahtarlari(Decimal(_tb.k), _tb.neg)))
    FOY_ARALIK[_i] = _ar
# satirda aralik uclari disinda ondalik var mi (kestirim ayri satirda mi)
FOY_ARALIK_DISI = {}
for _i, _t in FOY_DUZ.items():
    _ic = {(a + s0 + 1) for s0, s1, ta, tb in araliklar(_t) for a in (ta.a, tb.a)}
    FOY_ARALIK_DISI[_i] = sum(1 for x in FOY_TOK[_i] if not x.tam and x.a not in _ic)


def _ayristirma_sinami():
    """K2 isaret bicimleri: her bicim dogru isaretle okunmali (oz-sinamanin ilk adimi)."""
    vakalar = [  # (EN ham metin, beklenen [(deger, negatif mi)])
        (r"$-0.364$", [("0.364", True)]), (r"\(-0.364\)", [("0.364", True)]), ("−0.364", [("0.364", True)]),
        (r"\textminus 0.364", [("0.364", True)]), (r"\textminus0.364", [("0.364", True)]),
        (r"$\minus 0.364$", [("0.364", True)]), (r"\ensuremath{-}0.364", [("0.364", True)]),
        (r"$-$0.364", [("0.364", True)]), (r"${-}0.364$", [("0.364", True)]), (r"minus 0.364", [("0.364", False)]),
        (r"0.364", [("0.364", False)]), (r"$+0.364$", [("0.364", False)]), (r"q = -0.20", [("0.20", True)]),
        (r"ResNet-18 on CIFAR-100 with WRN-28-10 and ViT-B/16", []), (r"36--58 epochs", [("36", False), ("58", False)]),
        (r"0.893--0.944", [("0.893", False), ("0.944", False)]), (r"PyTorch 2.6.0a0, numpy 1.26.4", []),
        (r"$37.93\pm0.14$", [("37.93", False), ("0.14", False)]), (r"$7{,}061\pm68$", [("7061", False), ("68", False)]),
        (r"[$-0.415$, $-0.314$]", [("0.415", True), ("0.314", True)]), (r"$p < 2\times10^{-84}$", [("2e-84", False)]),
    ]
    hata = []
    for ham, bek in vakalar:
        got = [(t.k, t.neg) for t in tokenler(duz_satir(ham, norm_en))]
        if got != bek:
            hata.append(f"{ham!r}: beklenen {bek}, okunan {got}")
    if anahtar(Tok("0.364", True, 3, False, False, 0, 0)) == anahtar(Tok("0.364", False, 3, False, False, 0, 0)):
        hata.append("-0.364 ile 0.364 ayni anahtari aliyor")
    iv = araliklar(duz_satir(r"[$-0.415$, $-0.314$]", norm_en))
    if len(iv) != 1 or not (iv[0][2].neg and iv[0][3].neg):
        hata.append("aralik [$-0.415$, $-0.314$] isaretleriyle okunmadi")
    return hata


def foy_araligi_var(ka, kb):
    """Foyde bu uclardan biri bir ARALIGIN ilgili ucu olarak (ya da ters yonde: a ust uc, b alt uc) geciyor
    mu? Gecmiyorsa metindeki '[a, b]' foyden alinmis bir aralik degil, iki ayri degerden kurulmus bir
    betimlemedir ([en kucuk, en buyuk])."""
    for L in KEY_LINES.get(ka, set()) | KEY_LINES.get(kb, set()):
        if any(ka in A or kb in B or ka in B or kb in A for A, B in FOY_ARALIK[L]):
            return True
    return False


def foyde_ters_aralik(ka, kb):
    """Foy satirlari: metindeki [a, b] foyde [b, a] olarak (ters yonde) birlikte duruyor."""
    return sorted(L for L in KEY_LINES.get(ka, set()) & KEY_LINES.get(kb, set())
                  if any(kb in A and ka in B for A, B in FOY_ARALIK[L]))


def _isaretli(tk):
    return Decimal(tk.k) * (-1 if tk.neg else 1)


def _ara(fl, x, y):
    """x ile y belirtecleri arasindaki metin (y'nin isaret karakteri haric)."""
    son = y.a - 1 if (y.a >= 1 and fl[y.a - 1] in "-+" and (y.neg or fl[y.a - 1] == "+")) else y.a
    return fl[x.b:son]


def ters_araliklar(fl):
    """T1: satirdaki [a, b] / [a; b] ve a--b araliklarindan a > b olanlar: [(yazi, a, b)]."""
    out = []
    for m in _ARALIK.finditer(fl):
        ic = m.group(1)
        if re.search(r"[A-DF-Za-df-z]", ic):
            continue
        ts = tokenler(ic, tam_en_az=0)
        if len(ts) == 2 and re.fullmatch(r"\s*[,;]?\s*", _ara(ic, ts[0], ts[1])) and _isaretli(ts[0]) > _isaretli(ts[1]):
            out.append((f"[{ts[0].goster()}, {ts[1].goster()}]", ts[0], ts[1]))
    ts = tokenler(fl, tam_en_az=0)
    for x, y in zip(ts, ts[1:]):
        if re.fullmatch(r"\s*--\s*", _ara(fl, x, y)) and _isaretli(x) > _isaretli(y):
            out.append((f"{x.goster()}--{y.goster()}", x, y))
    return out


def to_araliklari(t):
    """'a to b' bicimindeki araliklar (Y1): [(bas, son, Tok a, Tok b)]."""
    ts = tokenler(t, tam_en_az=0)
    return [(x.a, y.b, x, y) for x, y in zip(ts, ts[1:]) if re.fullmatch(r"\s+to\s+", _ara(t, x, y))]


def yon_denetle(satirlar_, yon_yorum, R_, dosya):
    """Y1: 'excludes/includes ... zero' iceren her cumle bir araliga baglanmalidir (metindeki en yakin
    onceki aralik, yoksa sonraki ilk aralik; o da yoksa grubun '% YON: [a; b] FOY:...' yorumu). Hicbiri
    yoksa EKSIK (YON DENETLENEMEDI); grup '% YON: kural' tasiyorsa sayisiz kural cumlesi (bilgi)."""
    parca, ofs = [], []
    p = 0
    for ln, fl, _r in satirlar_:
        ofs.append((p, ln))
        parca.append(fl)
        p += len(fl) + 1
    metin = " ".join(parca)

    def satir_no(pos):
        ln = ofs[0][1] if ofs else 0
        for o, l_ in ofs:
            if o <= pos:
                ln = l_
        return ln
    kural = any(re.search(r"(?i)\bYON\s*:\s*kural", y) for _l, y in yon_yorum)
    yiv = []
    for yl, y in yon_yorum:
        ust = y.split("FOY:")[0]
        atif_s = {s for _b, s in foy_atiflari(y)}
        for m in _ARALIK.finditer(_duz(_foy_virgul(ust))):
            ts = tokenler(m.group(1), tam_en_az=0)
            if len(ts) != 2:
                continue
            ka, kb = anahtar(ts[0]), anahtar(ts[1])
            if not (demet_satirlari(ka, kb, None) & atif_s):
                R_["yon"].append((f"{dosya}:{yl}", f"% YON: [{ts[0].goster()}, {ts[1].goster()}]",
                                  "YON yorumundaki aralik atfettigi foy satirinda birlikte yok"))
            yiv.append((ts[0], ts[1]))
    bas = 0
    for cumle in re.split(r"(?<=[.!?])\s+(?=[A-Z\\])", metin):
        c0 = metin.find(cumle, bas)
        c0 = bas if c0 < 0 else c0
        bas = c0 + len(cumle)
        if _YON_SOZ.search(cumle):
            R_["yon_bilgi"].append(f"{dosya}:{satir_no(c0)}")
        ifade = sorted([(m.start(), "dis", m.group(0)) for m in _YON_DISLAR.finditer(cumle)]
                       + [(m.start(), "ic", m.group(0)) for m in _YON_ICERIR.finditer(cumle)])
        if not ifade:
            continue
        iv = sorted([(s0, ta, tb) for s0, _s1, ta, tb in araliklar(cumle)] + [(s0, ta, tb) for s0, _s1, ta, tb in to_araliklari(cumle)],
                    key=lambda x: x[0])
        for pos, tur, soz in ifade:
            yer = f"{dosya}:{satir_no(c0 + pos)}"
            once = [x for x in iv if x[0] < pos]
            sonra = [x for x in iv if x[0] > pos]
            hedef = once[-1] if once else (sonra[0] if sonra else None)
            nereden = ""
            if hedef is None:
                if yiv:
                    hedef, nereden = (None, yiv[0][0], yiv[0][1]), " (YON yorumundan)"
                elif kural:
                    R_["yon_kural"].append(yer)
                    continue
                else:
                    R_["yon_denetlenemedi"].append((yer, f"'{soz}'", "cumlede denetlenebilir aralik yok; araligi metne ya da "
                                                    "'% YON: [a; b] FOY:<bolum>:<satir>' yorumuna yazin (kural cumlesiyse '% YON: kural')"))
                    continue
            _p, ta, tb = hedef
            a, b = _isaretli(ta), _isaretli(tb)
            yazi = f"[{ta.goster()}, {tb.goster()}]{nereden}"
            if tur == "dis" and not (a > 0 or b < 0):
                R_["yon"].append((yer, yazi, f"metin '{soz}' diyor, aralik sifiri iceriyor"))
            if tur == "ic" and not (a <= 0 <= b):
                R_["yon"].append((yer, yazi, f"metin '{soz}' diyor, aralik sifiri dislar"))


def _bolum_basliklari():
    """Her foy satiri icin en yakin '##'/'###' basligi (yalniz rapor icin)."""
    bas, cur = {}, ""
    for i, s in enumerate(FOY, 1):
        if s.startswith("#"):
            cur = s.lstrip("#").strip()[:48]
        bas[i] = cur
    return bas


_FOY_BASLIK = _bolum_basliklari()


def foy_paragrafi(s):
    """Foy satirinin paragrafi: bos satir ya da basliga kadar yukari ve asagi."""
    a = b = s
    while a > 1 and FOY[a - 2].strip() and not FOY[a - 2].startswith("#"):
        a -= 1
    while b < len(FOY) and FOY[b].strip() and not FOY[b].startswith("#"):
        b += 1
    return range(a, b + 1)


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
    r"\\(?:ref|eqref|cite|label|cellname|url|href|authorrefmark|doi)\{[^}]*\}",
    # [3] \tfrac12 (= 1/2) ve sayisal alt simge indisleri (\ell_{12}, T_{21}) deger degildir
    r"\\[dt]?frac\s*\d\d",
    r"_\{\d+\}|_\d+",
    r"\\(?:multicolumn|multirow)\{[^}]*\}\{[^}]*\}",
    # model kimlikleri (Wong2020Fast, Gowal2020Uncovering_28_10_extra) ad parcasidir, sayi degildir
    r"\\texttt\{(?:[^{}]|\{[^{}]*\})*\}",
    # tarihler (on kayit dondurma gunleri): olgu, sonuc sayisi degil
    r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December"
    r"|Ocak|Subat|Şubat|Mart|Nisan|Mayis|Mayıs|Haziran|Temmuz|Agustos|Ağustos|Eylul|Eylül|Ekim|Kasim|Kasım|Aralik|Aralık)"
    r"\s+\d{4}\b",
    r"\b\d{4}-\d{2}-\d{2}\b",
)]


def _bicimsiz(t):
    for r_ in _BICIM_RE:
        t = r_.sub(" ", t)
    return t


def duz_satir(s, norm):
    """Bir .tex satirini denetime hazirla: yorumu at, bicim sayilarini at, dil normu, isaret duzlemesi."""
    return _duz(norm(_bicimsiz(re.sub(r"(?<!\\)%.*", "", s))))


# --- K1: KAYNAK yorumlari yalniz ACIKCA yazilan sayilari kapsar --------------------------------
_KAYNAK_BAS = re.compile(r"^\s*%\s*KAYNAK\b")
_ETIKET_BAS = re.compile(r"^\s*%\s*[A-Z_]{3,}\b\s*[:(]")
_JSON_REF = re.compile(r"(results/[\w./\-]+?\.json)#([\w.\-]+)")


def _sayisal_yapraklar(x):
    if isinstance(x, bool):
        return []
    if isinstance(x, (int, float)):
        return [x]
    if isinstance(x, dict):
        return [y for v in x.values() for y in _sayisal_yapraklar(v)]
    if isinstance(x, list):
        return [y for v in x for y in _sayisal_yapraklar(v)]
    return []


_KONSEY = ROOT / "raporlar/konsey_2026-10-29"
_BELGE_DIZIN = None
_DOSYA_ADI = re.compile(r"(?:[\w.\-]+/)+[\w.\-]+\.(?:md|json|txt|py|yaml|yml|sh)\b"
                        r"|(?<![\w/.\-])[\w\-][\w.\-]*\.(?:md|json|txt|py|yaml|yml|sh)\b")


def _belge_dizini():
    """raporlar/ altindaki .md/.json/.txt ve results/ altindaki .md dosyalari, ada gore."""
    global _BELGE_DIZIN
    if _BELGE_DIZIN is None:
        d = defaultdict(list)
        for kok, uz in (("raporlar", (".md", ".json", ".txt")), ("results", (".md",))):
            for p in sorted((ROOT / kok).rglob("*")):
                if p.suffix in uz and p.is_file():
                    d[p.name].append(p)
        _BELGE_DIZIN = d
    return _BELGE_DIZIN


def kaynak_belgeleri(y):
    """KAYNAK yorumunun ADINI VERDIGI belgeler: [(ad, Path ya da None)]. None = ad var, okunabilir belge yok."""
    out = []

    def ekle(ad, p):
        p = p if (p is not None and p.is_file()) else None
        if all(a != ad for a, _p in out):
            out.append((ad, p))
    y0 = re.sub(r"^\s*%\s*KAYNAK\b", " ", y)
    for m in _DOSYA_ADI.finditer(y0):
        s = m.group(0)
        if s == "CLAUDE.md":
            ekle(s, ROOT / "CLAUDE.md")
            continue
        p = ROOT / s if "/" in s else None
        if p is None or not p.is_file():
            c = _belge_dizini().get(Path(s).name, [])
            p = c[0] if c else None
        ekle(s, p)
    if re.search(r"\bON_KAYIT(?![A-Za-z_])", y0) or re.search(r"(?i)\bdondurma eki", y0):
        ekle("ON_KAYIT", _KONSEY / "ON_KAYIT_2026-10-29.md")
    if re.search(r"\bEK\b", y0) or re.search(r"(?i)\bek on kayit", y0):
        ekle("EK", _KONSEY / "ON_KAYIT_EK_B8_B10_2026-10-30.md")
    if re.search(r"(?i)\bbrif\b", y0):
        ekle("brif 12", _KONSEY / "12_makale_revizyon_brifi.md")
    for m in re.finditer(r"\bR(\d{2})\b", y0):
        c = sorted(_KONSEY.glob(f"{m.group(1)}_*.md"))
        ekle(f"R{m.group(1)}", c[0] if c else None)
    if re.search(r"(?i)\beski\s+(?:metin|0\d_)", y0):
        ekle("eski metin (belge degil)", None)
    return out


_UST = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")


def _belge_satir_varyantlari(s):
    """Bir belge satirinin okunuslari: nokta ondalik; EN binlik virgulu; TR ondalik virgulu; TR binlik
    noktasi + ondalik virgul. U+2212, en tire, 'x10^-4' ve 10⁻⁴ ust simgeleri duzlenir."""
    s = s.replace("−", "-").replace("–", "--").replace("×", r" \times ")
    s = re.sub(r"10([⁻⁺]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+)", lambda m: "10^{" + m.group(1).translate(_UST) + "}", s)
    s = re.sub(r"10\^(-?\d+)", r"10^{\1}", s)
    v = {s, re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "", s), re.sub(r"(?<=\d),(?=\d)", ".", s),
         re.sub(r"(?<=\d),(?=\d)", ".", re.sub(r"(?<=\d)\.(?=\d{3}(?!\d))", "", s))}
    return [_duz(norm_sci(x)) for x in v]


_BELGE_KEYS = {}


def belge_satir_anahtarlari(p):
    """Belgenin her satiri icin tasinmis deger anahtarlari (onbellekli): [(satir_no, set)]."""
    if p not in _BELGE_KEYS:
        out = []
        try:
            L_ = p.read_text(encoding="utf-8", errors="replace").split("\n")
        except OSError:
            L_ = []
        for i, s in enumerate(L_, 1):
            K, gor = set(), set()
            for v in _belge_satir_varyantlari(s):
                for tk in tokenler(v, tam_en_az=0):
                    if (tk.k, tk.neg) in gor:
                        continue
                    gor.add((tk.k, tk.neg))
                    K |= deger_anahtarlari(Decimal(tk.k), tk.neg)
            if K:
                out.append((i, K))
        _BELGE_KEYS[p] = out
    return _BELGE_KEYS[p]


def belgede_satirlar(p, key):
    return [i for i, K in belge_satir_anahtarlari(p) if key in K]


def _yorum_acik_metni(y):
    """KAYNAK yorumundan gosterge olmayan (acikca yazili deger olabilecek) kisim."""
    y2 = _JSON_REF.sub(" ", y)
    y2 = re.sub(r"FOY:[^\s;()]*", " ", y2)
    y2 = re.sub(r"(?i)(?:Sec\.?|§|satir(?:lar|i)?|line)\s*[\d.,\s\-]*\d", " ", y2)
    y2 = re.sub(r"[\w./\-]*:\d+(?:-\d+)?", " ", y2)
    y2 = _DOSYA_ADI.sub(" ", y2)
    y2 = re.sub(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}\.\d{1,2}\.\d{4}\b", " ", y2)
    # 'a-b' tamsayi/ondalik araligi: iki uc da yazili deger sayilir (ic degerler degil)
    y2 = re.sub(r"(?<![\w.])(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)(?![\w.])", r"\1 -- \2", y2)
    return y2


def kaynak_kapsami(yorumlar):
    """KAYNAK yorumlarinin kapsami: [{'json': keys, 'acik': keys, 'belgeler': [(ad, Path|None)]}], hatalar.

    (i) Yorumda ACIKCA yazili degerler ('delta = 0.10', 'n = 500', '11.2M'): bolum/satir/tarih
        gostergeleri (Sec. 5, satir 156, 04:638, FOY:..., dosya adlari) sayilmaz. Kapsadigi metin sayisi
        yorumun adini verdigi belgede de bulunmalidir (Y2; kaynak_durumu).
    (ii) 'results/<yol>.json#anahtar.alt_anahtar' bicimindeki atif: o dosyadan o anahtar OKUNUR,
        sayisal yapraklarinin tasinmis halleri kapsanir. Dosya ya da anahtar yoksa KAPI HATASI.
    Grubun oteki sayilari normal A2/A3 denetimine tabidir (eski surumdeki grup muafiyeti kalkti)."""
    KY, hata = [], []
    for y in yorumlar:
        J = set()
        for m in _JSON_REF.finditer(y):
            try:
                val = jl(m.group(1))
                for parca in m.group(2).split("."):
                    val = val[int(parca)] if isinstance(val, list) else val[parca]
                yap = _sayisal_yapraklar(val)
                if not yap:
                    raise KeyError("sayisal yaprak yok")
                for x in yap:
                    d = Decimal(repr(float(x)))
                    J |= deger_anahtarlari(abs(d), d < 0)
            except Exception as e:  # noqa: BLE001
                hata.append(f"{m.group(1)}#{m.group(2)}: {type(e).__name__}: {e}")
        A = set()
        for tk in tokenler(_duz(_foy_virgul(_yorum_acik_metni(y))), tam_en_az=0):
            A |= deger_anahtarlari(Decimal(tk.k), tk.neg)
        KY.append({"json": J, "acik": A, "belgeler": kaynak_belgeleri(y), "yorum": y.strip()})
    return KY, hata


def kaynak_durumu(key, KY):
    """('ok', '') KAYNAK kapsiyor ve (acik degerse) adlandirilan belgede var; ('belge', neden) yorumda
    yazili ama belge adi yok ya da deger belgede yok; (None, '') KAYNAK kapsamiyor."""
    if any(key in k["json"] for k in KY):
        return "ok", ""
    adaylar = [k for k in KY if key in k["acik"]]
    if not adaylar:
        return None, ""
    adlar = []
    for k in adaylar:
        for ad, p in k["belgeler"]:
            if p is not None and belgede_satirlar(p, key):
                return "ok", ""
            adlar.append(ad + ("" if p is not None else " [okunamadi]"))
    if not adlar:
        return "belge", "KAYNAK yorumunda belge adi yok"
    return "belge", "deger adlandirilan belgede yok (" + ", ".join(dict.fromkeys(adlar)) + ")"


_YON_BAS = re.compile(r"^\s*%\s*YON\b\s*:")


def gruplar(base, files, norm):
    """Her yorum grubu (FOY atfi, KAYNAK ya da YON yorumu tasiyan yorum blogu): dosya, satir, atiflar
    [(bolum, satir, nitel)], KAYNAK yorumlari, YON yorumlari, blok satirlari. FOY atfi olmayan grup
    KAYNAK-yalniz gruptur (K1b). Blok bittikten sonra tarama blogun SONUNDAN surer: blok icindeki KAYNAK
    yorumu yeni bir grup acmaz, blogun grubuna eklenir."""
    G = []
    for f in files:
        L_ = (ROOT / base / f).read_text(encoding="utf-8").split("\n")
        i, n = 0, len(L_)
        while i < n:
            if not L_[i].lstrip().startswith("%"):
                i += 1
                continue
            j, atif, kaynak, kay_acik, fyor, yon, kyor = i, [], [], False, [], [], []
            yorumlar = []
            while j < n and L_[j].lstrip().startswith("%"):
                s = L_[j]
                yorumlar.append(s)
                if "FOY:" in s:
                    fyor.append(j + 1)
                    nt = _nitel(s)
                    atif += [(b, sa, nt) for b, sa in foy_atiflari(s)]
                if _YON_BAS.match(s):
                    yon.append((j + 1, s))
                if _KAYNAK_BAS.match(s):
                    kaynak.append(s)
                    kyor.append(j + 1)
                    kay_acik = True
                elif kay_acik and "FOY:" not in s and not _ETIKET_BAS.match(s) and s.strip() != "%":
                    kaynak[-1] += " " + s.lstrip()[1:]
                else:
                    kay_acik = False
                j += 1
            if not (atif or kaynak or yon):
                i = j
                continue
            satirlar, k, ort, kay_acik = [], j, 0, False
            while k < n:
                s = L_[k]
                if s.lstrip().startswith("%"):
                    if "FOY:" in s:
                        break
                    yorumlar.append(s)
                    if _YON_BAS.match(s):
                        yon.append((k + 1, s))
                    if _KAYNAK_BAS.match(s):
                        kaynak.append(s)
                        kyor.append(k + 1)
                        kay_acik = True
                    elif kay_acik and not _ETIKET_BAS.match(s) and s.strip() != "%":
                        kaynak[-1] += " " + s.lstrip()[1:]
                    else:
                        kay_acik = False
                    k += 1
                    continue
                kay_acik = False
                if not s.strip() and ort <= 0:
                    break
                ort += len(re.findall(r"\\begin\{(?:table|figure)\*?\}", s)) - len(re.findall(r"\\end\{(?:table|figure)\*?\}", s))
                satirlar.append((k + 1, duz_satir(s, norm), s))
                k += 1
            G.append({"dosya": f, "satir": i + 1, "blok_bas": j + 1, "blok_son": k, "atif": atif, "kaynak": kaynak, "fyor": fyor,
                      "kyor": kyor, "yon": yon, "yorumlar": yorumlar, "satirlar": satirlar,
                      "sekil": any("\\includegraphics" in r for _l, _d, r in satirlar)})
            i = max(k, j)
    return G


# --- Y2: ust sinir ifadeleri (p < 2x10^-84) ---------------------------------------------------
_SINIR_ONCE = re.compile(r"\bp\s*(?:<|\\le(?:q)?|\\ll|≤)\s*$")
_P_ONCE = re.compile(r"\bp\s*=\s*$")


def sinir_denetimi(tk, atif_sat):
    """Ust sinir kurali. Metindeki 'p < B' ancak su durumda gecer: (a) B atfedilen bir foy satirinda
    AYNEN (yuvarlamasiz) geciyor (or. p tabani 1.00e-04), ya da (b) atfedilen satirlarin foy
    paragrafinda 'metne girecek ... sinir' satiri var, oradaki sinir B'ye esit ve B o paragraftaki
    en buyuk p'den kucuk degil. Yuvarlama ile eslesme (1.9e-120 -> 2e-120) SINIR SAYILMAZ."""
    v = Decimal(tk.k)
    for s in atif_sat:
        if any(Decimal(f.k) == v and f.neg == tk.neg for f in FOY_TOK[s]):
            return True, ""
    par = sorted({L for s in atif_sat for L in foy_paragrafi(s)})
    maxp = None
    for L in par:
        t = FOY_DUZ[L]
        for f in FOY_TOK[L]:
            if f.sci and _P_ONCE.search(t[max(0, f.a - 6):f.a]):
                d = Decimal(f.k)
                maxp = d if maxp is None or d > maxp else maxp
    satir_var = False
    for L in par:
        if re.search(r"(?i)metne girecek.*sinir", FOY[L - 1]):
            satir_var = True
            t = FOY_DUZ[L]
            mm = re.search(r"<\s*([-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?)", t)
            if mm and Decimal(mm.group(1)) == v:
                if maxp is None or v >= maxp:
                    return True, ""
                return False, f"foydeki ortak sinir {mm.group(1)} paragraftaki en buyuk p'nin ({maxp:.2e}) altinda"
    ek = f"; atfedilen paragraftaki en buyuk p = {maxp:.2e}" if maxp is not None else ""
    if satir_var:
        return False, "UST SINIR: foyun 'metne girecek ortak sinir' satiri baska bir sinir veriyor" + ek
    return False, ("UST SINIR: atfedilen foy paragraflarinda 'metne girecek ortak sinir' satiri yok; sinir foyden "
                   "turetilmis sayilmaz (yuvarlama ile eslesme kabul edilmez)" + ek)


def demet_satirlari(ka, kb, ke):
    """Aralik (ve varsa kestirim) BIRLIKTE hangi foy satirlarinda? Kestirim ayni satirda olmali;
    satirda aralik disinda ondalik yoksa (kestirim bir onceki satirda yazilmis) bir-iki satir yukari."""
    out = set()
    for L in KEY_LINES.get(ka, set()) & KEY_LINES.get(kb, set()):
        if not any(ka in A and kb in B for A, B in FOY_ARALIK[L]):
            continue
        if ke is None or ke in FOY_KEYS[L]:
            out.add(L)
        elif FOY_ARALIK_DISI[L] == 0 and any(ke in FOY_KEYS.get(L - d, set()) for d in (1, 2)):
            out.add(L)
    return out


_YON_DISLAR = re.compile(r"(?i)\bexclud\w*\s+(?:zero|0(?![.\d]))")
_YON_ICERIR = re.compile(r"(?i)\b(?:includ|contain|span|cross|straddl)\w*\s+(?:zero|0(?![.\d]))")
_YON_SOZ = re.compile(r"(?i)\b(negative|positive)\b")


def kisim_a(G):
    """A1, A2, A3 (isarete duyarli), KAYNAK-yalniz gruplar ve KAYNAK belgesi (K1b, Y2), aralik/demet ve
    yon denetimi (T1 foyde ters yon, Y1), ust sinir kurali."""
    R_ = defaultdict(list)
    R_["grup"], R_["atif"], R_["sekil_grubu"], R_["nitel_grup"] = len(G), 0, 0, 0
    R_["kaynak_yalniz_grup"] = sum(1 for g in G if not g["atif"])
    DURUM = {}
    for g in G:
        yer0 = f"{g['dosya']}:{g['satir']}"
        kaynak_yalniz = not g["atif"]
        gecerli = []
        for bolum, s, nt in g["atif"]:
            R_["atif"] += 1
            if not (1 <= s <= len(FOY)):
                R_["gecersiz_satir"].append((yer0, bolum, s))
                continue
            gecerli.append((bolum, s, nt))
        atif_sat = sorted({s for _b, s, _n in gecerli})
        atif_keys = set().union(*(FOY_KEYS[s] for s in atif_sat)) if atif_sat else set()
        KY, kay_hata = kaynak_kapsami(g["kaynak"])
        for h in kay_hata:
            R_["kaynak_hata"].append((yer0, h))

        def kapsar(key):
            return kaynak_durumu(key, KY)[0] == "ok"
        gorulen, dec_var, kapsanan = set(), False, False
        for ln, fl, _r in g["satirlar"]:
            yer = f"{g['dosya']}:{ln}"
            for tk in tokenler(fl):
                key = anahtar(tk)
                sonra = fl[tk.b:tk.b + 16]
                once = fl[max(0, tk.a - 30):tk.a - (1 if (tk.a and fl[tk.a - 1] in "-+") else 0)]
                neden = ""
                kd, kneden = kaynak_durumu(key, KY)
                if kd == "ok":
                    st = "kaynak"
                elif _SINIR_ONCE.search(once) and not tk.tam:
                    if sabit_mi(tk, once, sonra):
                        st = "sabit"
                    else:
                        ok, neden = sinir_denetimi(tk, atif_sat)
                        st = "sinir_ok" if ok else "sinir"
                elif key in atif_keys:
                    st = "ok"
                elif sabit_mi(tk, once, sonra):
                    st = "sabit"
                elif kd == "belge":
                    st, neden = "kaynak_belge", kneden
                elif kaynak_yalniz:
                    st, neden = "kaynak_eksik", ("FOY atfi olmayan grup: deger KAYNAK yorumunda yazili degil"
                                                 if g["kaynak"] else "grupta yalniz YON yorumu var: deger hicbir yorumla kapsanmiyor")
                elif ters(key) in atif_keys:
                    st, neden = "isaret", "atfedilen foy satirinda ters isaretli"
                elif KEY_LINES.get(key):
                    st = "atif_eksik" if (tk.tam or tk.sci or tk.nd >= 2) else "atif_disi"
                elif KEY_LINES.get(ters(key)):
                    st, neden = "isaret", "foyde yalniz ters isaretli"
                else:
                    st = "foyde_yok"
                DURUM[(g["dosya"], ln, tk.a)] = st
                sabit_baglam = bool(sabit_mi(tk, once, sonra))
                if not tk.tam and st not in ("kaynak", "sabit") and not sabit_baglam:
                    dec_var = True
                # [3] A1 kapsama kaniti: baglamli tasarim sabiti (or. '±0.10') bir foy degerinin yuvarlamasiyla
                # rastlantiyla eslesse de (10.08/100 -> 0.10) atfin kapsandigini gostermez.
                if st in ("ok", "sinir_ok") and (not tk.tam or int(tk.k) >= 100) and not sabit_baglam:
                    kapsanan = True
                if (st, yer, tk.goster()) in gorulen:
                    continue
                gorulen.add((st, yer, tk.goster()))
                if st in ("atif_eksik", "atif_disi", "foyde_yok", "isaret", "sinir", "kaynak", "kaynak_belge", "kaynak_eksik"):
                    R_[st].append((yer, tk.goster(), neden))
                if st == "sabit":
                    R_["sabit"].append((yer, tk.goster()))
            if kaynak_yalniz:
                continue  # sayilari tek tek KAYNAK DEGER EKSIK; demet atfi aranmaz
            # aralik ve demet (S1, K2): [a, b] ve 'kestirim [a, b]' birlikte ayni foy satirinda
            ts = tokenler(fl, tam_en_az=0)
            for s0, s1, ta, tb in araliklar(fl):
                ka, kb = anahtar(ta), anahtar(tb)
                if kapsar(ka) or kapsar(kb):
                    continue
                est = None
                for x in ts:
                    if x.b <= s0 and re.fullmatch(r"[\s(]*", fl[x.b:s0]) and not x.tam:
                        est = x
                ke = anahtar(est) if est is not None and not kapsar(anahtar(est)) else None
                ogeler = [ka, kb] + ([ke] if ke else [])
                if any(not KEY_LINES.get(o) for o in ogeler):
                    continue  # ogelerden biri tek basina foyde yok: A2/isaret zaten raporlar
                if not foy_araligi_var(ka, kb):
                    continue  # foyde aralik olarak gecmeyen [en kucuk, en buyuk] betimlemesi: uclar tek tek denetlendi
                yazi = (f"{est.goster()} " if ke else "") + f"[{ta.goster()}, {tb.goster()}]"
                L_ok = demet_satirlari(ka, kb, ke)
                if L_ok & set(atif_sat):
                    continue
                L_ters = foyde_ters_aralik(ka, kb)
                if L_ok:
                    R_["demet_atif"].append((yer, yazi, f"birlikte yalniz foy satiri {', '.join(map(str, sorted(L_ok)[:4]))}"))
                elif L_ters:
                    R_["demet"].append((yer, yazi, f"aralik foyde TERS YONDE (foy satiri {', '.join(map(str, L_ters[:4]))})"))
                else:
                    R_["demet"].append((yer, yazi, "ogeler foyde var ama hicbir satirda birlikte degil (takas ya da karisma)"))
            for i_, x in enumerate(ts[:-1]):
                y = ts[i_ + 1]
                if not re.fullmatch(r"\s*±\s*", fl[x.b:y.a]) or x.tam and y.tam:
                    continue
                kx, ky = anahtar(x), anahtar(y)
                if kapsar(kx) or kapsar(ky) or not KEY_LINES.get(kx) or not KEY_LINES.get(ky):
                    continue
                L_ok = KEY_LINES[kx] & KEY_LINES[ky]
                if L_ok & set(atif_sat):
                    continue
                yazi = f"{x.goster()} ± {y.goster()}"
                if L_ok:
                    R_["demet_atif"].append((yer, yazi, f"birlikte yalniz foy satiri {', '.join(map(str, sorted(L_ok)[:4]))}"))
                else:
                    R_["demet"].append((yer, yazi, "ortalama ve SD foyde var ama hicbir satirda birlikte degil"))
        # yon sozcukleri (Y1): her 'excludes/includes zero' cumlesi denetlenebilir bir araliga bagli olmali
        yon_denetle(g["satirlar"], g["yon"], R_, g["dosya"])
        # A1
        nitel_hepsi = bool(gecerli) and all(nt for _b, _s, nt in gecerli)
        degerler = any(FOY_TOK[s] for s in atif_sat)
        if not dec_var:
            R_["nitel_grup"] += 1
        elif degerler and not kapsanan and not nitel_hepsi:
            if g["sekil"]:
                R_["sekil_grubu"] += 1
            else:
                ornek = []
                for _l, fl, _r in g["satirlar"]:
                    ornek += [t.goster() for t in tokenler(fl) if not t.tam]
                R_["grup_eksik"].append((yer0, atif_sat, ornek[:8]))
        for bolum, s, nt in gecerli:
            if any(not f.tam for f in FOY_TOK[s]) and not any(
                    DURUM.get((g["dosya"], ln, t.a)) == "ok" and anahtar(t) in FOY_KEYS[s]
                    for ln, fl, _r in g["satirlar"] for t in tokenler(fl)):
                (R_["satir_nitel"] if nt else R_["satir_kapsanmayan"]).append((yer0, bolum, s))
    R_["_durum"] = DURUM
    return R_


_YIL_ONCE = re.compile(r"(?:\b(?:January|February|March|April|May|June|July|August|September|October|November|December)"
                       r"|\b[A-Z]{3,}[A-Za-z]*)\s*$")


def tum_metin_taramasi(base, files, norm, G, R_):
    """Gruplarin disina da bakan denetimler: GRUPSUZ (K1b), TERS ARALIK (T1, butun metin), grupsuz
    paragraflarda YON (Y1). Yorum satirlari atlanir."""
    bloklu = defaultdict(set)
    for g in G:
        for ln, _fl, _r in g["satirlar"]:
            bloklu[g["dosya"]].add(ln)
    R_["grupsuz_satir"] = []
    for f in files:
        L_ = (ROOT / base / f).read_text(encoding="utf-8").split("\n")
        par = []
        # Karar: main.tex'te \begin{document} oncesi (DOI, cilt, yil, posta kodu gibi ust veri) GRUPSUZ disi.
        govde = not any("\\begin{document}" in s for s in L_)

        def par_bitir():
            if par:
                yon_denetle(par, [], R_, f)
                par.clear()
        for i, s in enumerate(L_, 1):
            if s.lstrip().startswith("%"):
                continue
            fl = duz_satir(s, norm)
            for yazi, _x, _y in ters_araliklar(fl):
                R_["ters_aralik"].append((f"{f}:{i}", yazi, "alt uc ust uctan buyuk"))
            if "\\begin{document}" in s:
                govde = True
            if i in bloklu[f] or not govde:
                par_bitir()
                continue
            if not s.strip():
                par_bitir()
                continue
            par.append((i, fl, s))
            if s.strip():
                R_["grupsuz_satir"].append((f, i))
            gor = set()
            for tk in tokenler(fl):
                once = fl[max(0, tk.a - 30):tk.a - (1 if (tk.a and fl[tk.a - 1] in "-+") else 0)]
                if sabit_mi(tk, once, fl[tk.b:tk.b + 16]):
                    R_["grupsuz_sabit"].append((f"{f}:{i}", tk.goster()))
                    continue
                if tk.tam and not tk.neg and 1990 <= int(tk.k) <= 2030 and _YIL_ONCE.search(once):
                    R_["grupsuz_yil"].append((f"{f}:{i}", tk.goster()))
                    continue  # 'October 2026', 'ATEEC 2026': takvim yili ya da etkinlik adi (ad parcasi)
                if tk.goster() in gor:
                    continue
                gor.add(tk.goster())
                R_["grupsuz"].append((f"{f}:{i}", tk.goster(), "hicbir FOY/KAYNAK grubunun blogunda degil"))
        par_bitir()


A_KAPI = ("gecersiz_satir", "grup_eksik", "foyde_yok", "atif_eksik", "isaret", "sinir", "demet", "demet_atif",
          "yon", "kaynak_hata", "kaynak_eksik", "kaynak_belge", "grupsuz", "ters_aralik", "yon_denetlenemedi")


# --- B. ana manset tasiyicilari: JSON artefaktlarindan + ozetteki butun sayilar (S2) ----------------
MANSET, MANSET_UC, _MANSET_HATA = [], [], []


def _mk(etiket, deger, nd=3, kaynak="json"):
    d = float(deger)
    k = f"{abs(d):.{nd}f}"
    it = {"etiket": etiket, "k": k, "neg": d < 0 and Decimal(k) != 0, "nd": nd, "kaynak": kaynak}
    MANSET.append(it)
    return it


def _mk3(etiket, est, lo, hi, nd=3):
    MANSET_UC.append((etiket, _mk(etiket, est, nd), _mk(etiket + " %90 alt", lo, nd), _mk(etiket + " %90 ust", hi, nd)))


try:
    _b2 = jl("results/q1/konsey_ayrisim_b2.json")["b2"]["F_B2"]
    _b9 = jl("results/q1/konsey_b9_c100/b9_dondurulmus_b2.json")["b2"]["F_B2"]
    _b4 = jl("results/q1/konsey_ayrisim_b4.json")["b4"]["F_B4"]["karsitliklar"]
    _b5 = jl("results/q1/konsey_ayrisim_b5.json")["b5"]["birincil_C1-R32_V-scr"]
    _b6 = jl("results/q1/konsey_b6_maskeleme.json")["modeller"]
    _b8 = jl("results/q1/konsey_b8_imagenetv2/b8_betimsel.json")
    for _h in ("H1", "H2", "H3"):
        _mk3(f"{_h} kestirim (B4)", _b4[_h]["kestirim"], *_b4[_h]["ci90"])
    for _vk, _F in (("CIFAR-10 B2", _b2), ("CIFAR-100 B9", _b9)):
        _mk3(f"K-a ort q {_vk}", _F["K-a"]["sinama"]["ort"], *_F["K-a"]["sinama"]["ci90"])
        _mk3(f"K-b rho(V-scr) {_vk}", _F["K-b"]["ort"], *_F["K-b"]["ci90"])
        _mk3(f"K-c Delta_seed {_vk}", _F["K-c"]["Delta_w"], *_F["K-c"]["bootstrap"]["ci90"])
    _mk3("korunma orani G_best/G_PGD (B5)", _b5["oran"], *_b5["bootstrap"]["ci90"])
    _fk = [v["fark_puan"] for v in _b6.values()]
    _mk("B6 en buyuk PGD-10 - AA farki (puan)", max(_fk), 2)
    _mk("B6 en kucuk PGD-10 - AA farki (puan)", min(_fk), 2)
    _mk3("A^sigma_IN (B8)", _b8["A_sigma_IN"]["kestirim"], *_b8["A_sigma_IN"]["goruntu_bootstrap"]["ci90"])
    _mk("A^sigma_scr Liu (B8)", _b8["A_sigma_scr_Liu"]["kestirim"])
    for _vk in ("cifar10", "cifar100", "imagenetv2"):
        _ms_ = jl(f"results/q1/konsey_b10_gradyan/mantel_{_vk}.json")["sinamalar"]
        _mk(f"Mantel r ham {_vk} (B10)", _ms_["ham"]["istatistik"])
        _mk(f"Mantel r ana etki artik {_vk} (B10)", _ms_["ana_etki_artik"]["istatistik"])
except Exception as _e_:  # anahtar degisirse kapi SESSIZCE gecmesin
    _MANSET_HATA.append(f"{type(_e_).__name__}: {_e_}")

_M9_BAS = next((i for i, s in enumerate(FOY, 1) if s.startswith("## M9:")), None)
_M10_SON = next((i for i, s in enumerate(FOY, 1) if s.startswith("## Sabit dizgeler")), len(FOY) + 1)
if _M9_BAS is None:
    _MANSET_HATA.append("foyde '## M9:' basligi yok")
M9_M10_KEYS = set().union(*(FOY_KEYS[i] for i in range(_M9_BAS, _M10_SON))) if _M9_BAS else set()


def metin_toklari(base, files, norm):
    """Metnin butun (yorum disi) satirlarindaki sayilar: [(dosya, satir, Tok, duz_satir, ozet_mi)] ve
    ozetin demetleri (kestirim [alt, ust])."""
    out, demet = [], []
    for f in files:
        ozet = False
        for i, s in enumerate((ROOT / base / f).read_text(encoding="utf-8").split("\n"), 1):
            if s.lstrip().startswith("%"):
                continue
            if "\\begin{abstract}" in s:
                ozet = True
            fl = duz_satir(s, norm)
            ts = tokenler(fl)
            for tk in ts:
                out.append((f, i, tk, fl, ozet))
            t0 = tokenler(fl, tam_en_az=0)
            for s0, s1, ta, tb in araliklar(fl):
                est = None
                for x in t0:
                    if x.b <= s0 and re.fullmatch(r"[\s(]*", fl[x.b:s0]) and not x.tam:
                        est = x
                demet.append((f, i, est, ta, tb, ozet))
            if "\\end{abstract}" in s:
                ozet = False
    return out, demet


def _yakin(o, it):
    """o (metindeki sayi) manset degeri it'in olasi bozuk kopyasi mi? Ayni basamak sayisinda: en cok 3
    birim farkli, rakamlari yer degistirmis ya da ayni mutlak deger ters isaretli."""
    if o.tam or o.sci or o.nd != it["nd"]:
        return False
    if o.k == it["k"]:
        return o.neg != it["neg"]
    if o.neg != it["neg"]:
        return False
    fark = abs(Decimal(o.k) - Decimal(it["k"]))
    return fark <= 3 * _Q[it["nd"]] or sorted(o.k) == sorted(it["k"])


def _takas(o, it):
    """S1b: o, kalemin iki ANLAMLI rakaminin yer degistirmesi mi (0.936 <-> 0.963)? Ayni uzunluk ve isaret, tam
    iki konum farkli ve capraz esit; iki konum da iki dizgenin ilk sifir-disi rakaminda ya da sonrasinda (0.003 ile
    0.030 gibi basamak kaymasi takas sayilmaz)."""
    a, b = o.k, it["k"]
    if o.tam or o.sci or o.neg != it["neg"] or len(a) != len(b) or a == b:
        return False
    fark = [i for i in range(len(a)) if a[i] != b[i]]
    if len(fark) != 2 or a[fark[0]] != b[fark[1]] or a[fark[1]] != b[fark[0]] or "." in (a[fark[0]], a[fark[1]]):
        return False
    ilk = max(next((i for i, c in enumerate(s) if c not in "0."), len(s)) for s in (a, b))
    return fark[0] >= ilk


def kisim_b(base, files, norm, G, durum):
    toks, demetler = metin_toklari(base, files, norm)
    sat_grup = {}
    for gi, g in enumerate(G):
        for ln in range(g["blok_bas"], g["blok_son"] + 1):
            sat_grup[(g["dosya"], ln)] = gi
    tum = {(t.k, t.neg) for _f, _i, t, _fl, _o in toks}
    govde = {(t.k, t.neg) for _f, _i, t, _fl, oz in toks if not oz}
    tum_key = {anahtar(t) for _f, _i, t, _fl, _o in toks}

    # S2: ozetteki her sayi manset kalemi olur (foyde, govdede ve her kopyada birebir)
    items = list(MANSET)
    uclu = list(MANSET_UC)
    ozet_var = False
    for f, i, t, fl, oz in toks:
        if not oz:
            continue
        ozet_var = True
        once = fl[max(0, t.a - 30):t.a - (1 if (t.a and fl[t.a - 1] in "-+") else 0)]
        if sabit_mi(t, once, fl[t.b:t.b + 16]):
            continue
        if any(it["kaynak"] == "ozet" and it["k"] == t.k and it["neg"] == t.neg for it in items):
            continue
        items.append({"etiket": f"OZET {t.goster()}", "k": t.k, "neg": t.neg, "nd": t.nd, "kaynak": "ozet",
                      "tam": t.tam, "sci": t.sci})
    for f, i, est, ta, tb, oz in demetler:
        if oz and est is not None:
            mk = lambda x: {"k": x.k, "neg": x.neg, "nd": x.nd}  # noqa: E731
            uclu.append((f"OZET demet {est.goster()} [{ta.goster()}, {tb.goster()}]", mk(est), mk(ta), mk(tb)))

    def _key(it):
        return anahtar(Tok(it["k"], it["neg"], it["nd"], it.get("tam", False), it.get("sci", "e" in it["k"]), 0, 0))

    sat, eksik, kopya = [], 0, []
    for it in items:
        key = _key(it)
        if it["kaynak"] == "json":
            f_ok = key in M9_M10_KEYS
            t_ok = key in tum_key and (it["k"], it["neg"]) in tum
        else:
            f_ok = bool(KEY_LINES.get(key))
            t_ok = (it["k"], it["neg"]) in govde
        if not (f_ok and t_ok):
            eksik += 1
        sat.append((it, f_ok, t_ok))

    def mesru(f, i, t):
        gi = sat_grup.get((f, i))
        if gi is not None:
            return durum.get((f, i, t.a)) in ("ok", "kaynak", "sabit", "sinir_ok")
        return bool(KEY_LINES.get(anahtar(t)))

    # S1b: blok kalemin foy satirini atfediyor ama kalemi tasimiyorsa, rakamlari yer degistirmis deger atfedilen
    # satirlarda bulunsa bile mesru sayilmaz. Karar (yanlis alarm, 04:228 -0.346 jackknife): kural iki durumda
    # uygulanir: (a) blok OZETTE ve kalem blokta yok; (b) blogun yorumu kalemin degerini aynen aniyor (blok o kalemi
    # tasimak uzere atfedilmis) ve takasli degeri anmiyor -- (b) kalem blokta baska bir kopyada dursa da gecerlidir,
    # boylece blok icinde iki kopyadan birinin takasi da yakalanir. Takasli deger mesruysa yazar onu yoruma ekler.
    blok_deger, blok_ozet = defaultdict(set), defaultdict(bool)
    for f, i, t, fl, oz in toks:
        gi = sat_grup.get((f, i))
        if gi is not None:
            blok_deger[gi].add((t.k, t.neg))
            blok_ozet[gi] |= oz
    grup_atif = [{s for _b, s, _n in g["atif"]} for g in G]
    grup_yorum = [{(x.k, x.neg) for x in tokenler(_duz(_foy_virgul(" ".join(g.get("yorumlar", [])))), tam_en_az=0)} for g in G]
    gorulen = set()
    for it in items:
        if it.get("tam") or it.get("sci") or it["nd"] < 2:
            continue
        kalem_sat = {s for s in KEY_LINES.get(_key(it), set())
                     if any(x.k == it["k"] and x.neg == it["neg"] for x in FOY_TOK[s])}
        for f, i, t, fl, oz in toks:
            gi = sat_grup.get((f, i))
            s1b = (gi is not None and _takas(t, it) and bool(grup_atif[gi] & kalem_sat)
                   and (t.k, t.neg) not in grup_yorum[gi]
                   and ((blok_ozet[gi] and (it["k"], it["neg"]) not in blok_deger[gi])
                        or (it["k"], it["neg"]) in grup_yorum[gi]))
            if not (s1b or _yakin(t, it)):
                continue
            if s1b or not mesru(f, i, t):
                k_ = (f, i, t.goster())
                if k_ in gorulen:
                    continue
                gorulen.add(k_)
                neden = ("olasi bozuk kopya (rakam takasi): blok kalemin foy satirini (" + ", ".join(map(str, sorted(grup_atif[gi] & kalem_sat)[:3]))
                         + ") kalem icin atfediyor; takasli deger yorumda yok" if s1b else "olasi bozuk kopya: atfedilen foy satirinda yok")
                kopya.append((it, f"{f}:{i}", t.goster(), neden))
    for et, E, A, U in uclu:
        hedef = [(E["k"], E["neg"]), (A["k"], A["neg"]), (U["k"], U["neg"])]
        for f, i, est, ta, tb, oz in demetler:
            if est is None:
                continue
            gz = [(est.k, est.neg), (ta.k, ta.neg), (tb.k, tb.neg)]
            ortak = sum(1 for x, y in zip(gz, hedef) if x == y)
            if ortak == 2:
                k_ = (f, i, tuple(gz))
                if k_ in gorulen:
                    continue
                gorulen.add(k_)
                kopya.append(({"etiket": et, "k": E["k"], "neg": E["neg"]}, f"{f}:{i}",
                              f"{est.goster()} [{ta.goster()}, {tb.goster()}]",
                              f"demet tutarsiz: beklenen {('-' if E['neg'] else '') + E['k']} "
                              f"[{('-' if A['neg'] else '') + A['k']}, {('-' if U['neg'] else '') + U['k']}]"))
    if not ozet_var:
        _MANSET_HATA.append(f"{base}: ozet (\\begin{{abstract}}) okunamadi; S2 denetimi yapilamadi")
    return sat, eksik + len(kopya), kopya


# --- C. eski kontroller: yalniz bilgi ---------------------------------------------------------
def tam_eslesme(val, txt):
    return len(re.findall(r"(?<![\d.,])" + re.escape(val) + r"(?![\d])", txt))


def kisim_c(txt):
    """Eski listede metinde kalan 'korunuyor', kalmayan 'dustu (brif §5.10)'. YALNIZ BILGI: bu
    kalemlerin metinde kalanlari A kismindaki FOY atiflariyla (isarete duyarli) denetlenir."""
    sonuc = {"korunuyor": [], "dustu": []}
    for label, val in CHECKS:
        (sonuc["korunuyor"] if tam_eslesme(val, txt) > 0 else sonuc["dustu"]).append((label, val))
    return sonuc


def dil_denetimi(dil, base, files, norm):
    G = gruplar(base, files, norm) if files else []
    a = kisim_a(G)
    if files:
        tum_metin_taramasi(base, files, norm, G, a)
    b = kisim_b(base, files, norm, G, a["_durum"]) if files else ([], 0, [])
    return G, a, b, kisim_c(LANGS[dil])


_ETIKET = {
    "foyde_yok": "FOYDE YOK: foyun hicbir satirinda (isaretiyle) tasinmis hali yok",
    "atif_eksik": "ATIF EKSIK: atfedilen foy satirlarinda yok, foyde baska satirda var",
    "isaret": "ISARET",
    "sinir": "",
    "demet": "DEMET",
    "demet_atif": "DEMET ATIF EKSIK",
    "yon": "YON",
    "kaynak_eksik": "KAYNAK DEGER EKSIK",
    "kaynak_belge": "KAYNAK BELGEDE YOK",
    "grupsuz": "GRUPSUZ",
    "ters_aralik": "TERS ARALIK",
    "yon_denetlenemedi": "YON DENETLENEMEDI",
}


def yaz_dil(dil, G, a, b, c, tam):
    sat_b, eksik_b, kopya = b
    eksik_a = sum(len(a[k]) for k in A_KAPI)
    print("=" * 78)
    print(f"[{dil}] dosyalar: {', '.join(EN_FILES if dil == 'EN' else TR_FILES) or 'YOK'}")
    print(f"[{dil}] A. FOY/KAYNAK yorumlari: {a['grup']} grup ({a['kaynak_yalniz_grup']} KAYNAK-yalniz), {a['atif']} satir "
          f"atfi. EKSIK {eksik_a} "
          f"(A1 grup {len(a['grup_eksik'])}; A2 foyde yok {len(a['foyde_yok'])}; A3 atif eksik {len(a['atif_eksik'])}; "
          f"isaret {len(a['isaret'])}; ust sinir {len(a['sinir'])}; demet {len(a['demet'])}+{len(a['demet_atif'])}; "
          f"yon {len(a['yon'])}; yon denetlenemedi {len(a['yon_denetlenemedi'])}; ters aralik {len(a['ters_aralik'])}; "
          f"KAYNAK deger eksik {len(a['kaynak_eksik'])}; KAYNAK belgede yok {len(a['kaynak_belge'])}; "
          f"GRUPSUZ {len(a['grupsuz'])}; gecersiz satir no {len(a['gecersiz_satir'])}; "
          f"KAYNAK JSON hatasi {len(a['kaynak_hata'])})")
    for yer, bolum, s in a["gecersiz_satir"]:
        print(f"    EKSIK  {yer}  FOY:{bolum}:{s}  -- foy {len(FOY)} satir; satir numarasi disarida")
    for yer, sat, ornek in a["grup_eksik"]:
        print(f"    EKSIK  {yer}  FOY satirlari {', '.join(map(str, sat[:10]))}{' ...' if len(sat) > 10 else ''}  "
              f"-- blokta bu satirlarin hicbir sayisi yok; blok sayilari: {', '.join(ornek) or '-'}")
    for yer, h in a["kaynak_hata"]:
        print(f"    EKSIK  {yer}  KAYNAK JSON okunamadi: {h}")
    for k in ("foyde_yok", "atif_eksik", "isaret", "sinir", "demet", "demet_atif", "yon", "yon_denetlenemedi",
              "ters_aralik", "kaynak_eksik", "kaynak_belge", "grupsuz"):
        for yer, x, neden in a[k]:
            ek = ""
            if k in ("kaynak_eksik", "kaynak_belge", "grupsuz"):
                t_ = tokenler(_duz(x), tam_en_az=0)
                sat = sorted(KEY_LINES.get(anahtar(t_[0]), ())) if t_ else []
                ek = f"; foyde satir {', '.join(map(str, sat[:5]))}{' ...' if len(sat) > 5 else ''}" if sat else "; foyde yok"
            if k == "atif_eksik":
                t_ = tokenler(_duz(x), tam_en_az=0)
                sat = sorted(KEY_LINES.get(anahtar(t_[0]), ())) if t_ else []
                ek = f" ({', '.join(map(str, sat[:5]))}{' ...' if len(sat) > 5 else ''}); yanlis sayi ya da eksik FOY atfi"
            on = "p < " if k == "sinir" else ""
            bas = _ETIKET[k]
            print(f"    EKSIK  {yer}  {on}{x}  -- {bas}{': ' if bas and neden else ''}{neden}{ek}")
    print(f"    bilgi: atif disi (tek ondalikli, foyde baska satirda) {len(a['atif_disi'])}; KAYNAK yorumunda acikca "
          f"yazili ya da JSON'dan okunan {len(a['kaynak'])}; tasarim sabiti {len(a['sabit'])}; hicbir sayisi blokta "
          f"gecmeyen atfedilen satir {len(a['satir_kapsanmayan'])} (nitel isaretli {len(a['satir_nitel'])}); ondalik "
          f"sayisiz (nitel) grup {a['nitel_grup']}; sekil grubu (A1 disi) {a['sekil_grubu']}; yon sozcuklu cumle "
          f"(negative/positive, yalniz bilgi) {len(a['yon_bilgi'])}; '% YON: kural' ile muaf yon ifadesi "
          f"{len(a['yon_kural'])}; grupsuz satirda baglamli sabit {len(a['grupsuz_sabit'])}")
    if ARGS.ayrinti:
        for yer, x, _n in a["atif_disi"]:
            print(f"      atif disi  {yer}  {x}")
        for yer, x, _n in a["kaynak"]:
            print(f"      KAYNAK kapsadi  {yer}  {x}")
        for yer, x in a["sabit"]:
            print(f"      sabit  {yer}  {x}")
        for yer, bolum, s in a["satir_kapsanmayan"]:
            print(f"      kapsanmayan atif  {yer}  FOY:{bolum}:{s} [{_FOY_BASLIK.get(s, '-')}]")
    print(f"[{dil}] B. Ana manset ve ozet tasiyicilari: {len(sat_b)} kalem "
          f"({sum(1 for it, _f, _t in sat_b if it['kaynak'] == 'json')} JSON, "
          f"{sum(1 for it, _f, _t in sat_b if it['kaynak'] == 'ozet')} ozet), EKSIK {eksik_b} (kopya {len(kopya)})")
    if tam:
        for it, f_ok, t_ok in sat_b:
            v = ("-" if it["neg"] else "") + it["k"]
            fe, te = ("foy M9-M10", "metin") if it["kaynak"] == "json" else ("foy", "govde")
            print(f"    {'OK   ' if (f_ok and t_ok) else 'EKSIK'}  {it['etiket'][:46]:46s} {v:>8s}  {fe}: "
                  f"{'var' if f_ok else 'YOK'}  {te}: {'var' if t_ok else 'YOK'}")
        for it, yer, x, neden in kopya:
            v = ("-" if it["neg"] else "") + it["k"]
            print(f"    EKSIK  {it['etiket'][:46]:46s} {v:>8s}  KOPYA  {yer}  {x}  -- {neden}")
    print(f"[{dil}] C. Eski kontroller ({len(CHECKS)}, yalniz bilgi, kapi disi): metinde korunuyor "
          f"{len(c['korunuyor'])}; dustu (brif §5.10) {len(c['dustu'])}")
    if tam and ARGS.ayrinti:
        for label, val in c["dustu"]:
            print(f"      dustu (brif §5.10)  {label} = {val}")
    return eksik_a + eksik_b


def dokum_yaz(yol, G, a, b):
    """Oz-sinama icin grup, belirteç ve manset dokumu (JSON)."""
    durum = a["_durum"]
    out = {"gruplar": [], "manset": [], "foy_satir": len(FOY),
           "grupsuz_satirlar": [list(x) for x in a.get("grupsuz_satir", [])]}
    for g in G:
        gg = {"dosya": g["dosya"], "satir": g["satir"], "blok_bas": g["blok_bas"], "blok_son": g["blok_son"],
              "atif": sorted({s for _b, s, _n in g["atif"]}), "kaynak": bool(g["kaynak"]), "sekil": g["sekil"],
              "yorum_satirlari": g["fyor"], "kaynak_satirlari": g["kyor"], "yon_satirlari": [l_ for l_, _y in g["yon"]],
              "blok_satirlari": [ln for ln, _fl, _r in g["satirlar"]], "tok": []}
        for ln, fl, raw in g["satirlar"]:
            for t in tokenler(fl):
                gg["tok"].append({"satir": ln, "deger": t.goster(), "tam": t.tam, "nd": t.nd,
                                  "durum": durum.get((g["dosya"], ln, t.a))})
        out["gruplar"].append(gg)
    for it, f_ok, t_ok in b[0]:
        out["manset"].append({"etiket": it["etiket"], "deger": ("-" if it["neg"] else "") + it["k"],
                              "kaynak": it["kaynak"], "nd": it["nd"], "foy": f_ok, "metin": t_ok})
    Path(yol).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


# --- yazar listesi icin oneri aramasi (--eksik-json) ------------------------------------------------------
def _oneri_belgeleri():
    """Bir degerin aranacagi tasarim belgeleri: on kayit, ek on kayit, CLAUDE.md, brif ve konsey raporlari."""
    L_ = [_KONSEY / "ON_KAYIT_2026-10-29.md", _KONSEY / "ON_KAYIT_EK_B8_B10_2026-10-30.md", ROOT / "CLAUDE.md",
          _KONSEY / "12_makale_revizyon_brifi.md"]
    L_ += [p for p in sorted(_KONSEY.glob("[0-9][0-9]_*.md")) if p not in L_]
    return [p for p in L_ if p.is_file()]


def oneriler(deger):
    """Degerin (isaretiyle) foy satirlari ve tasarim belgesi satirlari."""
    t_ = tokenler(_duz(deger), tam_en_az=0)
    if not t_:
        return {"foy": [], "belge": []}
    key = anahtar(t_[0])
    foy = [{"satir": s, "baslik": _FOY_BASLIK.get(s, ""), "metin": FOY[s - 1].strip()[:160]}
           for s in sorted(KEY_LINES.get(key, ()))[:6]]
    belge = []
    for p in _oneri_belgeleri():
        sat = belgede_satirlar(p, key)
        if sat:
            belge.append({"belge": str(p.relative_to(ROOT)), "satirlar": sat[:6]})
    kod = []
    oncelikli = {"ON_KAYIT_2026-10-29.md", "ON_KAYIT_EK_B8_B10_2026-10-30.md", "CLAUDE.md", "12_makale_revizyon_brifi.md"}
    if not any(Path(b_["belge"]).name in oncelikli for b_ in belge) and key[0] == "i" and key[2] >= 100:
        # tasarim belgesinde yoksa kod/ayar dosyalarinda tamsayi olarak ara (or. bolme tohumu 777)
        for kok in ("experiments", "configs", "src", "scripts"):
            for p in sorted((ROOT / kok).rglob("*")):
                if p.suffix not in (".py", ".yaml", ".yml") or "verify_manuscript" in p.name or not p.is_file():
                    continue
                try:
                    L_ = p.read_text(encoding="utf-8", errors="replace").split("\n")
                except OSError:
                    continue
                sat = [i for i, s in enumerate(L_, 1) if re.search(rf"(?<![\w.]){key[2]}(?![\w.])", s)]
                if sat:
                    kod.append({"belge": str(p.relative_to(ROOT)), "satirlar": sat[:4]})
    return {"foy": foy, "belge": belge[:6], "kod": kod[:4]}


def eksik_json_yaz(yol, G, a, b):
    kayit = []

    def ekle(tur, yer, deger, neden, oneri=True):
        f, _, ln = yer.rpartition(":")
        kayit.append({"tur": tur, "dosya": f, "satir": int(ln) if ln.isdigit() else ln, "deger": deger, "neden": neden,
                      "oneri": oneriler(deger.replace("p < ", "")) if (oneri and deger) else {"foy": [], "belge": []}})
    TUR = {"foyde_yok": "FOYDE YOK", "atif_eksik": "ATIF EKSIK", "isaret": "ISARET", "sinir": "UST SINIR",
           "demet": "DEMET", "demet_atif": "DEMET ATIF EKSIK", "yon": "YON", "yon_denetlenemedi": "YON DENETLENEMEDI",
           "ters_aralik": "TERS ARALIK", "kaynak_eksik": "KAYNAK DEGER EKSIK", "kaynak_belge": "KAYNAK BELGEDE YOK",
           "grupsuz": "GRUPSUZ"}
    for k, tur in TUR.items():
        for yer, x, neden in a[k]:
            ekle(tur, yer, x, neden, oneri=k not in ("demet", "demet_atif", "yon", "yon_denetlenemedi", "ters_aralik"))
    for yer, bolum, s in a["gecersiz_satir"]:
        ekle("GECERSIZ SATIR", yer, "", f"FOY:{bolum}:{s} foy disinda", oneri=False)
    for yer, sat, ornek in a["grup_eksik"]:
        ekle("A1 GRUP", yer, "", f"blok atfettigi satirlarin ({', '.join(map(str, sat[:8]))}) hicbir sayisini tasimiyor; "
                                 f"blok sayilari {', '.join(ornek)}", oneri=False)
    for yer, h in a["kaynak_hata"]:
        ekle("KAYNAK JSON", yer, "", h, oneri=False)
    for it, f_ok, t_ok in b[0]:
        if not (f_ok and t_ok):
            kayit.append({"tur": "MANSET/OZET", "dosya": "", "satir": "", "deger": ("-" if it["neg"] else "") + it["k"],
                          "neden": f"{it['etiket']}: foy {'var' if f_ok else 'YOK'}, metin/govde {'var' if t_ok else 'YOK'}",
                          "oneri": {"foy": [], "belge": []}})
    for it, yer, x, neden in b[2]:
        f, _, ln = yer.rpartition(":")
        kayit.append({"tur": "KOPYA", "dosya": f, "satir": int(ln), "deger": x,
                      "neden": f"{it['etiket']} = {('-' if it['neg'] else '') + it['k']}: {neden}", "oneri": {"foy": [], "belge": []}})
    Path(yol).write_text(json.dumps({"foy_satir": len(FOY), "kayit": kayit}, ensure_ascii=False, indent=1), encoding="utf-8")


if ARGS.ayristirma_sinami:
    _h = _ayristirma_sinami()
    for _x in _h:
        print(f"  KALDI  {_x}")
    print(f"AYRISTIRMA: {'KALDI' if _h else 'GECTI'} ({len(_h)} hata)")
    sys.exit(1 if _h else 0)

print(f"Foy: {FOY_YOL.relative_to(ROOT)} ({len(FOY) - 1 if FOY and FOY[-1] == '' else len(FOY)} satir)")
G_en, a_en, b_en, c_en = dil_denetimi("EN", EN_BASE, EN_FILES, norm_en)
en_eksik = yaz_dil("EN", G_en, a_en, b_en, c_en, tam=True)
if ARGS.dokum:
    dokum_yaz(ARGS.dokum, G_en, a_en, b_en)
if ARGS.eksik_json:
    eksik_json_yaz(ARGS.eksik_json, G_en, a_en, b_en)
if TR_FILES and LANGS["TR"].strip():
    G_tr, a_tr, b_tr, c_tr = dil_denetimi("TR", TR_BASE, TR_FILES, norm_tr)
    tr_eksik = yaz_dil("TR", G_tr, a_tr, b_tr, c_tr, tam=ARGS.tr_zorunlu)
else:
    tr_eksik = None
    print("UYARI: TR metni okunamadi (dosya adlari degismis olabilir).")

print("=" * 78)
for _h in _EN_HATA + _MANSET_HATA:
    print(f"KAPI HATASI (artefakt okunamadi): {_h}")
print(f"TOPLAM: A grup={a_en['grup']} atif={a_en['atif']}  B manset+ozet={len(b_en[0])}  C eski={len(CHECKS)} "
      f"(dustu {len(c_en['dustu'])}, bilgi)  EN_EKSIK={en_eksik}  "
      f"TR_EKSIK={tr_eksik if tr_eksik is not None else 'okunamadi'}{'' if ARGS.tr_zorunlu else ' (TR yalniz bilgi)'}")
kaldi = bool(en_eksik or _EN_HATA or _MANSET_HATA
             or (ARGS.tr_zorunlu and (tr_eksik is None or tr_eksik)))
if kaldi:
    print("SONUC: KALDI -- FOY atfi, foyde olmayan ya da ters isaretli sayi, demet, ust sinir ya da manset/ozet "
          "tasiyicisi sorunu var (ya da artefakt okunamadi).")
    sys.exit(1)
print("SONUC: GECTI -- FOY atiflari bloklarinda, bloklardaki sayilar isaretleriyle foyde, demetler birlikte, "
      "manset ve ozet tasiyicilari foyde ve metnin her kopyasinda.")
sys.exit(0)
