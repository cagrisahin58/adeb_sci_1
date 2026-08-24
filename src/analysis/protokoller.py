"""Transfer olcum protokollerinin TEK KAYNAGI.

Bu makalenin tezi, transfer asimetrisinin hangi ornekler paydaya alindigina
gore degistigidir. O yuzden protokol tanimi bir gerceklestirme ayrintisi
degil, RAPORLANAN SONUCUN PARCASIDIR ve tek bir yerde durmalidir.

2026-08-25'e kadar tanim SEKIZ ayri dosyada kopyalanmisti ve `successful_source`
protokolu makale metninden AYRISMISTI:

    metin (Bolum 3.5): "saldirinin kaynakta BEYAZ KUTU ANLAMINDA basarili
                        oldugu hedef-dogru ornekler"
    kod (8 dosyada)  : target_clean_correct & source_adv_wrong

Gevsek kod, kaynagin TEMIZDE ZATEN YANILDIGI ornekleri de iceri aliyordu;
orada "basarili olmus bir saldiri" yoktur, yalnizca onceden var olan bir
hata vardir. Makalenin kendi Tartisma bolumu bu protokolu "zaten ise
yaramis bir saldirinin ne kadar tasindigi" diye tanimladigi icin gevsek
maske makalenin sordugu soruyu yanitlamiyordu. Kanonik tanim SIKI olandir.

Gevsek varyant silinmedi: makale onu OLCULMUS bir duyarlilik olarak
raporluyor (tek bir protokol adinin altindaki yazilmamis bir alt secim,
CIFAR-10 asimetrisini 4,77 puan oynatiyor -- makalenin kendi tezinin
ikinci dereceden bir orneginin, kendi boru hattimizda bulunmus hali).
"""
import numpy as np

# Kanonik sira: tablolarda ve yayilim hesaplarinda HER YERDE bu kullanilir.
PROTOKOLLER = ["raw", "target_correct", "both_correct", "successful_source"]

# Duyarlilik icin tasinan, kanonik OLMAYAN varyant.
TANI_PROTOKOLLERI = ["successful_source_loose"]

ETIKETLER = {
    "raw": "Kosulsuz (ham)",
    "target_correct": "Hedef dogru",
    "both_correct": "Her ikisi dogru",
    "successful_source": "Basarili kaynak",
    "successful_source_loose": "Basarili kaynak (gevsek varyant)",
}


def maskeler(target_clean_correct, source_clean_correct, source_adv_wrong,
             tani=True):
    """Protokol adi -> kosullama maskesi.

    target_clean_correct : hedef, TEMIZ girdide dogru mu
    source_clean_correct : kaynak, TEMIZ girdide dogru mu
    source_adv_wrong     : kaynak, KENDI cekismeli ornegini yanlis mi
                           siniflandiriyor (beyaz kutu)

    tani=True ise gevsek varyant da dondurulur (yalniz duyarlilik icin).
    """
    tc = np.asarray(target_clean_correct, dtype=bool)
    sc = np.asarray(source_clean_correct, dtype=bool)
    sa = np.asarray(source_adv_wrong, dtype=bool)

    m = {
        "raw": np.ones_like(tc, dtype=bool),
        "target_correct": tc,
        "both_correct": tc & sc,
        # BEYAZ KUTU BASARISI = temizde dogru VE cekismelide yanlis.
        "successful_source": tc & sc & sa,
    }
    if tani:
        # Kaynagin temiz hatasini iceri alan, terk edilmis varyant.
        m["successful_source_loose"] = tc & sa
    return m


def oranlar(target_adv_wrong, maske_sozlugu, basamak=None):
    """Maske adi -> yanıltma orani (yuzde). Bos maske icin nan."""
    fool = np.asarray(target_adv_wrong, dtype=bool)
    cikti = {}
    for ad, m in maske_sozlugu.items():
        if m.sum() == 0:
            cikti[ad] = float("nan")
            continue
        v = float(100 * fool[m].mean())
        cikti[ad] = round(v, basamak) if basamak is not None else v
    return cikti


def protokol_oranlari(target_clean_correct, target_adv_wrong,
                      source_clean_correct, source_adv_wrong,
                      basamak=None, tani=True):
    """Tek adimda: dort kanonik oran (+ istege bagli gevsek tani orani)."""
    m = maskeler(target_clean_correct, source_clean_correct, source_adv_wrong,
                 tani=tani)
    return oranlar(target_adv_wrong, m, basamak=basamak)


def yayilim(oran_sozlugu):
    """Dort KANONIK protokolun urettigi aciklik. Tani varyanti KATILMAZ."""
    v = [oran_sozlugu[p] for p in PROTOKOLLER]
    return max(v) - min(v)
