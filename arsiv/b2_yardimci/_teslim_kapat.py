#!/usr/bin/env python3
"""TESLIM_DURUMU'nu B2 kapanisina gore gunceller."""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/results/q1_research/TESLIM_DURUMU.md")
t = p.read_text(encoding="utf-8")

if "ALTI KAPI" in t:
    print("zaten guncel")
    sys.exit(0)

CIFTLER = [
    # --- B2 artik acik degil ---
    ("**Makale şu anda kendi kapısından GEÇMİYOR** ve bu bilerek böyle: A kolu\n"
     "yeniden koşulana kadar H1/H2 muhafızları kırmızı kalır.",
     "**B2 KAPANDI (2026-08-25 akşamı).** A kolu 116/116 noktayla yeniden koşuldu,\n"
     "metin iki dilde işlendi, **altı kapının altısı da geçiyor**\n"
     "(`bash scripts/kapilar.sh`). Ayrıntı ve kapanış ölçümleri: `B2_DURUM.md`.\n"
     "\n"
     "Yol boyunca **altı kapı/sınama kusuru** daha bulundu ve kapatıldı; biri\n"
     "yeni bir kapı doğurdu (EN/TR ayna denetimi), o da hemen iki gerçek kusur\n"
     "buldu: Türkçe Yöntem'de eksik bir alt bölüm ve İngilizce Tartışma'da\n"
     "eksik bir paragraf (Mahmood karşıtlığı). İkisi de sayı taşımadığı için\n"
     "mevcut kapıların hiçbiri görmüyordu."),

    # --- paket listesi guncellemesi ---
    ("| `results/q1/KOKEN.json` | 23 artefaktın sha256 köken defteri |",
     "| `results/q1/KOKEN.json` | **44** artefaktın sha256 köken defteri |"),
    ("| Dört kapı betiği + çıktıları | sayıların denetlenebilir olduğunun kanıtı |",
     "| **Altı** kapı betiği + dört öz-sınama + `scripts/kapilar.sh` | sayıların "
     "*ve yapının* denetlenebilir olduğunun kanıtı |\n"
     "| `src/analysis/protokoller.py` | dört koşullama maskesinin TEK kaynağı "
     "(metin/kod ayrışmasını imkânsız kılar) |\n"
     "| `B2_DURUM.md` + `B2_KAPI_KUSURU.md` | protokol düzeltmesinin ve bulunan "
     "kapı kusurlarının kaydı |"),

    ("**Pakete girmeden önce kapatılması gereken tek teknik borç:** kapıların\n"
     "`paper/bildiri/` altını da taraması (2. bölümdeki boşluk).",
     "**Teknik borç kalmadı.** Bildiri kapısı yazıldı (ve 2026-08-25'te kör\n"
     "olduğu bulunup artefakt-okur hâle getirildi); EN/TR ayna kapısı eklendi."),
]

hata = []
for eski, yeni in CIFTLER:
    if t.count(eski) != 1:
        hata.append(f"{t.count(eski)} eslesme: {eski[:60]}")
        continue
    t = t.replace(eski, yeni, 1)

if hata:
    print("BASARISIZ -- yazilmadi:", *hata, sep="\n  ")
    sys.exit(1)
p.write_text(t, encoding="utf-8")
print("TESLIM_DURUMU guncellendi")
