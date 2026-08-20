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
chk("C3 hedef-duzeyi r (n=3)",
    c3p["veri_kumeleri"]["cifar10"]["HEDEF_DUZEYI_n3"]["pearson_r"], 4)
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

# --- rapor ---
rows = []
for label, val in CHECKS:
    found = {lang: (val in txt) for lang, txt in LANGS.items()}
    rows.append((label, val, found))

missing = 0
print(f"{'KONTROL':36s} {'DEGER':>9s}  EN   TR")
print("-" * 60)
for label, val, found in rows:
    en = "OK " if found["EN"] else "YOK"
    trk = "OK " if found["TR"] else "YOK"
    if not (found["EN"] and found["TR"]):
        missing += 1
    print(f"{label:36s} {val:>9s}  {en}  {trk}")

print("-" * 60)
en_missing = sum(1 for _, _, f in rows if not f["EN"])
tr_missing = sum(1 for _, _, f in rows if not f["TR"])
print(f"TOPLAM={len(rows)}  EN_EKSIK={en_missing}  TR_EKSIK={tr_missing}")
if not LANGS["TR"].strip():
    print("UYARI: TR metni okunamadi (dosya adlari degismis olabilir).")
