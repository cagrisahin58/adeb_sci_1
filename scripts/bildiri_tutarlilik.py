#!/usr/bin/env python3
"""Bildirinin tasiyici sayilari ARTEFAKTLARLA tutuyor mu?

NEDEN VAR: bildiri (paper/bildiri/) dort makale kapisinin HICBIRI tarafindan
taranmiyor ve main ile q1 dallarinda BAYT AYNI, yani Q1 kampanyasi ona hic
dokunmadi. Kampanya bazi anlatilari degistirdi; bildiride eskimis sayi ya da
curutulmus iddia kalmis olabilir. Bu betik onu OLCER.

TASARIM -- neden dize degil SAYI karsilastiriliyor: bildiri 3 anlamli
basamak, makale 4 basamak yaziyor (0,493 ile 0,4928). Duz dize aramasi
iki yonde de yanilir:
  - dize ararsan yuvarlama farkini SAHTE UYUSMAZLIK sayarsin;
  - "dize varsa kontrol et" dersen sayi baska bir degere donustugunde
    kontrol SESSIZCE ATLANIR (oz-sinamanin 1. adimi tam bunu yakaladi:
    37,93 -> 36,00 karantina degeri gorunmez kaliyordu).
Bu yuzden her buyukluk BAGLAM DESENIYLE bildiriden cekilir ve otoriter
degerle SAYISAL olarak karsilastirilir. Bildirinin yazdigi basamak sayisi
tolerans olur.

2026-08-25 DUZELTMESI -- KAPI KORDU. Otoriter degerler betige SABIT
YAZILMISTI, yani kapi korumaya calistigi sayinin bir KOPYASINI tasiyordu ve
artefakt degistiginde kaymayi GOREMIYORDU. Olculdu: B2 protokol duzeltmesi
ust siniri 14,60'tan 19,37'ye tasidi, kapi yine "GECTI" dedi. Artik her
otoriter deger ARTEFAKTTAN hesaplaniyor. Kapinin kendi oz-sinamasina da
ucuncu bir kol eklendi: ARTEFAKTI bozup kapinin KALDIGI dogrulanir.

2026-10-31 -- MAKALE O1 SURUMUNE GECTI, BILDIRI DEGISMEDI. Bildiri ATEEC
2026'da degerlendirmede ve dokunulmaz; makalenin onceki surumuyle tutarli
yazilmistir. Yeni surumde degisen tek tasiyici bicim "4.4-fold" ifadesidir:
makale onu birakti ve uclari (+4.36 / +19.37) yaziyor. Kapi artik kat iddiasini
bu iki uca ESLER (KAT ESLEMESI) ve bildiri ile makale arasindaki bilerek
yapilmis farklari, makalede onlari beyan eden dizelerle birlikte
BILINEN_FARKLAR listesinde tutar. Sayisal denetim (bildiri <-> artefakt)
degismedi.

Cikis kodu: uyusmazlik varsa 1, yoksa 0.
"""
import json
import os
import re
import sys
from pathlib import Path

# GATE_ROOT     : hem paper/ hem results/ iceren KIRIK bir kopyayi denetler
#                 (oz-sinamanin artefakt kolu bunu kullanir).
# MANUSCRIPT_ROOT: yalniz paper/ kopyasini denetler (eski oz-sinama kollari).
_gkok = os.environ.get("GATE_ROOT")
_kok = os.environ.get("MANUSCRIPT_ROOT")
_VARSAYILAN = (Path("/workspace") if Path("/workspace/results").is_dir()
               else Path(__file__).resolve().parents[1])
ROOT = Path(_gkok) if _gkok else _VARSAYILAN          # artefakt koku
PAPER_ROOT = Path(_kok) if _kok else ROOT             # metin koku

R = PAPER_ROOT / "paper"
b = (R / "bildiri/bildiri.tex").read_text(encoding="utf-8")
en = "\n".join(p.read_text(encoding="utf-8")
               for p in sorted((R / "manuscript").rglob("*.tex")))
if not b.strip() or not en.strip():
    sys.exit("KAPI HATASI: bildiri ya da makale okunamadi; denetim yapilmadi.")


def jl(p):
    f = ROOT / p
    if not f.exists():
        sys.exit(f"KAPI HATASI: artefakt yok: {f}")
    return json.loads(f.read_text(encoding="utf-8"))


# --- OTORITER DEGERLER: hepsi artefakttan, hicbiri elle yazilmis degil ---
seed = jl("results/c1_seeds/c1_seed_summary.json")["aggregate"]
trs = jl("results/c1_transfer/c1_transfer_summary.json")
beh = jl("results/c1_behavior_summary.json")["gradient"]

PROTOKOLLER = ["raw", "target_correct", "both_correct", "successful_source"]
_farklar = [trs["protocols"][p]["diff"]["mean"] for p in PROTOKOLLER]
_mutlak = [abs(v) for v in _farklar]
ALT, UST = min(_farklar), max(_farklar)
KAT = max(_mutlak) / min(_mutlak)

# (etiket, bildirideki baglam deseni [tek yakalama grubu], otoriter deger)
SAYILAR = [
    ("AA ResNet",            r"\((\d+\.\d+)\$\\pm\$0\.14\\% vs",
     seed["resnet"]["aa"]["mean"]),
    ("AA ViT",               r"vs (\d+\.\d+)\$\\pm\$0\.40\\%",
     seed["vit"]["aa"]["mean"]),
    ("temiz fark",           r"a (\d+\.\d+)-point clean accuracy",
     seed["resnet"]["clean"]["mean"] - seed["vit"]["clean"]["mean"]),
    ("kosullu yaniltma CNN", r"\((\d+\.\d+)\\% vs \d+\.\d+\\% under PGD",
     seed["resnet"]["cond_fooling_pgd"]["mean"]),
    ("kosullu yaniltma ViT", r"\(\d+\.\d+\\% vs (\d+\.\d+)\\% under PGD",
     seed["vit"]["cond_fooling_pgd"]["mean"]),
    ("protokol alt sinir",   r"\$\+\$(\d+\.\d+) to \$\+\$\d+\.\d+ points", ALT),
    ("protokol ust sinir",   r"\$\+\$\d+\.\d+ to \$\+\$(\d+\.\d+) points", UST),
    ("protokol kat",         r"(\d+\.\d+)-fold", KAT),
    ("Hoyer CNN",            r"Hoyer (\d+\.\d+) vs \d+\.\d+",
     beh["ResNet18_AT"]["sparsity_hoyer"]["mean"]),
    ("Hoyer ViT",            r"Hoyer \d+\.\d+ vs (\d+\.\d+)",
     beh["ViT_Tiny_AT"]["sparsity_hoyer"]["mean"]),
    ("hizalanma ViT",        r"absolute cosine \((\d+\.\d+) vs \d+\.\d+",
     beh["ViT_Tiny_AT"]["gradient_alignment"]["mean"]),
    ("hizalanma CNN",        r"absolute cosine \(\d+\.\d+ vs (\d+\.\d+)",
     beh["ResNet18_AT"]["gradient_alignment"]["mean"]),
]

print(f"{'BUYUKLUK':22s} {'BILDIRIDE':>10s} {'OTORITER':>10s}  DURUM")
print("-" * 60)
uyusmaz = []
for ad, desen, otoriter in SAYILAR:
    m = re.search(desen, b)
    if not m or not m.group(m.lastindex or 1):
        print(f"{ad:22s} {'BULUNAMADI':>10s} {otoriter:>10.4f} KALDI")
        uyusmaz.append(f"{ad}: baglam bildiride bulunamadi "
                       f"(cumle yeniden yazilmis olabilir, elle bakin)")
        continue
    yazilan = m.group(m.lastindex or 1)
    basamak = len(yazilan.split(".")[1])
    tutuyor = round(otoriter, basamak) == float(yazilan)
    print(f"{ad:22s} {yazilan:>10s} {otoriter:>10.4f} "
          f"{'tutuyor' if tutuyor else 'KALDI'}")
    if not tutuyor:
        uyusmaz.append(f"{ad}: bildiri {yazilan}, otoriter deger {otoriter:.4f} "
                       f"({basamak} basamaga yuvarlanmisi "
                       f"{round(otoriter, basamak)})")

# Oransal iddia MAKALEDE de ayni sayiyla anilmali (K2 -- kat iddiasi tek
# basina gezmez). Artik dize varligi degil, SAYI karsilastiriliyor: ikisi
# birlikte eskirse eski kod sessiz kaliyordu.
print()
_bk = re.search(r"(\d+\.\d+)-fold", b)
_mk = re.search(r"(\d+\.\d+)-fold", en)
print(f"  bildiride kat: {_bk.group(1) if _bk else 'YOK'}   "
      f"makalede kat: {_mk.group(1) if _mk else 'YOK'}   "
      f"otoriter: {KAT:.4f}")
# 2026-10-31 KAT ESLEMESI (makalenin O1 surumu; bildiri DOKUNULMAZ, ATEEC'te
# degerlendirmede). Makalenin 31.10 surumu "N-fold" ifadesini birakti: protokol
# calismasi dorduncu katkiya indi ve uclari iki ondalikla yazar ("+4.36 to
# +19.37", giris katki 4, IV-I, Tablo III). Bildirinin kat iddiasi bu iki
# uctan TURETILIR (KAT = |ust| / |alt|). K2 kurali, yani "kat iddiasi tek
# basina gezmez", bu durumda dayanaginin makalede durmasiyla saglanir: makale
# iki ucu artefaktin iki ondalikli degerleriyle tasimali. Uclardan biri yoksa
# ya da artefaktla tutmuyorsa kapi yine KALIR. Bildiri ile makalenin yeni
# surumu arasindaki oteki bilinen farklar BILINEN_FARKLAR listesindedir.
_uc_alt = f"{ALT:.2f}"
_uc_ust = f"{UST:.2f}"
_uc_desen = lambda v: r"(?<![\d.])" + re.escape(v) + r"(?!\d)"
if _bk and not _mk:
    _alt_var = re.search(_uc_desen(_uc_alt), en) is not None
    _ust_var = re.search(_uc_desen(_uc_ust), en) is not None
    print(f"  KAT ESLEMESI: makalede kat ifadesi yok; dayanak uclar "
          f"{_uc_alt} {'VAR' if _alt_var else 'YOK'}, "
          f"{_uc_ust} {'VAR' if _ust_var else 'YOK'} "
          f"(|{_uc_ust}| / |{_uc_alt}| = {KAT:.4f})")
    if not (_alt_var and _ust_var):
        uyusmaz.append(f"bildiri {_bk.group(1)} kat diyor; makalede kat iddiasi "
                       f"YOK ve dayanak uclar ({_uc_alt}, {_uc_ust}) da eksik")
elif _bk and _mk and _bk.group(1) != _mk.group(1):
    uyusmaz.append(f"kat iddiasi iki belgede FARKLI: bildiri {_bk.group(1)}, "
                   f"makale {_mk.group(1)}")
if _mk:
    _b = len(_mk.group(1).split(".")[1])
    if round(KAT, _b) != float(_mk.group(1)):
        uyusmaz.append(f"makaledeki kat {_mk.group(1)}, artefakt {round(KAT, _b)}")

print()
print("=== Q1 KAMPANYASININ DEGISTIRDIGI IDDIALAR ===")
# Bildiri CIFAR-10 ile sinirli; SVHN'deki isaret cevrilmesi onu CURUTMEZ.
# Ama bunu ANCAK acik sinirlama cumlesi ayakta oldugu surece soyleyebiliriz.
YON = ("The direction, CNN$\\rightarrow$ViT stronger, "
       "is stable across protocols and seeds.")
SINIR = "preliminary results on one dataset and one model pair"
print(f"  {'VAR' if YON in b else 'YOK':4s}  yon protokoller/tohumlar boyunca kararli (CIFAR-10)")
print(f"  {'VAR' if SINIR in b else 'YOK':4s}  tek veri kumesi sinirlamasi ACIK YAZILI")
if YON in b and SINIR not in b:
    uyusmaz.append("yon iddiasi var ama tek-veri-kumesi sinirlamasi YOK; "
                   "SVHN'deki isaret cevrilmesi karsisinda savunulamaz")

# Yon iddiasi ARTEFAKTLA da tutmali: dort protokolun dordu de ayni isaretli mi?
_isaretler = [1 if v > 0 else -1 for v in _farklar]
print(f"  {'VAR' if len(set(_isaretler)) == 1 else 'YOK':4s}  "
      f"artefakt: dort protokolun dordu de ayni isaretli "
      f"({sum(1 for s in _isaretler if s > 0)}/4 pozitif)")
if YON in b and len(set(_isaretler)) != 1:
    uyusmaz.append("bildiri 'yon protokoller boyunca kararli' diyor ama "
                   "CIFAR-10 artefaktinda protokoller ISARET DEGISTIRIYOR")

print()
print("=== Q1'DE OLUP BILDIRIDE OLMAYAN KONULAR (genisletme payi) ===")
for konu, anahtar in [("SVHN", "SVHN"), ("CIFAR-100", "CIFAR-100"),
                      ("L2 tehdit modeli", "L_2"), ("ozdeslik", "identity"),
                      ("on kayit", "pre-registration"), ("TGR", "TGR")]:
    print(f"  bildiri={'VAR' if anahtar in b else 'YOK':4s} "
          f"makale={'VAR' if anahtar in en else 'YOK':4s}  {konu}")

# 2026-10-31 BILINEN FARKLAR: bildiri (ATEEC 2026, degerlendirmede, DOKUNULMAZ)
# makalenin ONCEKI surumuyle yazildi; makalenin 31.10 O1 surumu onunla su
# noktalarda bilerek ayrilir. Her fark, makalede onu beyan eden dizeyle
# eslenir; dize makaleden duserse fark beyansiz kalir ve kapi KALIR.
#   (fark, makalede aranan dize, gerekce)
BILINEN_FARKLAR = [
    ("onsurum beyani", "submitted to ATEEC 2026",
     "makale bildiriyi onsurum olarak anar (giris son paragraf)"),
    ("atif", "sahin2026behavioral",
     "makale bildiriye atif yapar"),
    ("yon kararliligi duzeltmesi", "corrects one claim",
     "bildiri 'yon protokoller ve tohumlar boyunca kararli' der (tek veri "
     "kumesi sinirlamasiyla); makale temiz dogruluk eslesince yonun kararli "
     "olmadigini yazar ve bunu bildirinin duzeltilen iddiasi olarak beyan eder"),
    ("baslik ve okuma cercevesi", "Less a Weak Source than a Different One",
     "bildiri basligi davranissal karsilastirmadir; makale O1 manseti: ViT'nin "
     "zayif kaynak gorunumu buyuk olcude simetrik benzemezliktir (bildiride "
     "olmayan panel ve ayrisim; sayi catismasi yok, yukaridaki sayilar tutuyor)"),
    ("kat ifadesi", f"{_uc_ust}",
     "bildiri 'N-fold' der, makale uclari yazar (yukarida KAT ESLEMESI)"),
]
print()
print("=== BILDIRI ILE MAKALENIN 31.10 SURUMU ARASINDA BILINEN FARKLAR ===")
for fark, dize, gerekce in BILINEN_FARKLAR:
    var = dize in en
    print(f"  makalede beyan {'VAR' if var else 'YOK':4s} {fark}")
    if not var:
        uyusmaz.append(f"bilinen fark '{fark}' makalede beyansiz kaldi "
                       f"(aranan: '{dize}'; {gerekce})")

print()
print(f"Bildiri: {len(b.splitlines())} satir, "
      f"{len(re.findall(chr(92) + chr(92) + 'cite', b))} atif cagrisi")
if uyusmaz:
    print("\nSONUC: KALDI")
    for u in uyusmaz:
        print("  -", u)
    sys.exit(1)
print("\nSONUC: GECTI -- bildirinin tasiyici sayilari ARTEFAKTLARLA SAYISAL "
      "olarak tutuyor, curutulmus iddia yok.")
