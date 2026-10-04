#!/usr/bin/env python3
"""Mahmood ve ark. (ICCV 2021, arXiv 2104.02610) Tablo 1 / Tablo 2 / Ek Tablo 3
metinden PROGRAMLA ayristirilir ve ozdeslik (Denklem 11) altinda yeniden puanlanir.

Girdi : results/q1/dis_veri/mahmood2021_metin.txt  (PDF'den cikarilmis metin,
        sayfa ayiraci "===== SAYFA N =====", tablo hucreleri satir basina bir deger)
        results/q1/ozdeslik_kontrol.json            (p = P(cekismeli yanlis | temiz yanlis),
                                                     bizim C1/q1 yonlerimizde olculmus)
        results/c1_transfer/c1_transfer_summary.json (bizim CIFAR-10 cifti, dort protokol)
Cikti : results/q1/dis_veri/mahmood2021_tablolar.json
        results/q1/dis_veri/mahmood2021_ozdeslik.json

Hicbir sayi elle yazilmaz; tum hucreler regex ile metinden okunur. Elle verilen
tek sey model adlarinin aile etiketidir (ViT / hibrit / CNN) ve Tablo 2'deki
kisaltilmis adlarin Tablo 1 adlarina eslenmesidir (sira ile dogrulanir).

Calistirma (depo kokunden):
  docker exec -w /workspace adeb_eval python experiments/q1_mahmood2021_tablolar.py
"""
import datetime
import hashlib
import io
import json
import os
import re
import sys

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
os.chdir(ROOT)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

METIN = "results/q1/dis_veri/mahmood2021_metin.txt"
OZDES = "results/q1/ozdeslik_kontrol.json"
BIZIM = "results/c1_transfer/c1_transfer_summary.json"
OUT_TAB = "results/q1/dis_veri/mahmood2021_tablolar.json"
OUT_OZ = "results/q1/dis_veri/mahmood2021_ozdeslik.json"

KAYNAK = {}


def sha256(yol):
    h = hashlib.sha256()
    with open(yol, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def kaydet_kaynak(yol):
    KAYNAK[yol] = sha256(yol)


def yaz(yol, obj):
    with io.open(yol, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print("yazildi:", yol)


# ------------------------------------------------------------------ ayristirma
PCT = re.compile(r"^(\d+(?:\.\d+)?)%$")
SAYFA = re.compile(r"^===== SAYFA (\d+) =====$")


def sayfalar(metin):
    out, cur = {}, None
    for ln in metin.splitlines():
        m = SAYFA.match(ln.strip())
        if m:
            cur = int(m.group(1))
            out[cur] = []
            continue
        if cur is not None:
            out[cur].append(ln.strip())
    return out


def beyaz_kutu_blogu(satirlar, etiket):
    """'etiket' satirindan sonra 7 sutun basligi + (ad, 7 yuzde) satirlari."""
    i = satirlar.index(etiket)
    baslik = satirlar[i + 1:i + 8]
    assert baslik == ["FGSM", "PGD", "BPDA", "MIM", "C&W", "APGD", "Acc"], baslik
    j = i + 8
    satir = []
    while j + 7 < len(satirlar) + 1:
        ad = satirlar[j]
        degerler = satirlar[j + 1:j + 8]
        if PCT.match(ad) or not all(PCT.match(v) for v in degerler):
            break
        satir.append({"model": ad,
                      **{b: float(PCT.match(v).group(1)) for b, v in zip(baslik, degerler)}})
        j += 8
    return baslik, satir


def transfer_blogu(satirlar, etiket, baslangic=0):
    """'etiket' satirindan sonra sutun adlari (ilk ad tekrar edene kadar) ve
    her satirda ad + n yuzde ('+' -> None). Doner: sutunlar, satirlar, matris."""
    i = satirlar.index(etiket, baslangic)
    j = i + 1
    sutun = [satirlar[j]]
    j += 1
    while satirlar[j] != sutun[0]:
        sutun.append(satirlar[j])
        j += 1
    n = len(sutun)
    sat_ad, mat = [], []
    for _ in range(n):
        ad = satirlar[j]
        hucre = []
        for v in satirlar[j + 1:j + 1 + n]:
            if v == "+":
                hucre.append(None)
            else:
                m = PCT.match(v)
                assert m, (etiket, ad, v)
                hucre.append(float(m.group(1)))
        sat_ad.append(ad)
        mat.append(hucre)
        j += 1 + n
    assert sat_ad == sutun, (sat_ad, sutun)
    return sutun, mat, j


# Tablo 2'deki kisaltilmis adlar -> Tablo 1 adlari (yalniz ad eslemesi, sayi degil)
AD_ESLEME = {"R50-ViT": "ViT-R50", "BiT-50x1": "BiT-M-R50x1", "BiT-101x3": "BiT-M-R101x3"}
# Aile etiketleri (Mahmood'un "model genus" ayrimi; ViT-R50 hibrit ResNet-50 govdeli ViT)
AILE = {"ViT-B-32": "ViT", "ViT-B-16": "ViT", "ViT-L-16": "ViT", "ViT-R50": "hibrit",
        "BiT-M-R50x1": "CNN", "BiT-M-R101x3": "CNN", "ResNet-56": "CNN", "ResNet-164": "CNN"}


def main():
    kaydet_kaynak(METIN)
    with io.open(METIN, encoding="utf-8") as fh:
        metin = fh.read()
    S = sayfalar(metin)

    # ---- Tablo 1 (sayfa 4): CIFAR-10 beyaz kutu + temiz dogruluk
    s4 = S[4]
    t1_alinti = " ".join(s4[0:4])
    bas10, t1_c10 = beyaz_kutu_blogu(s4, "CIFAR-10")
    _, t1_in = beyaz_kutu_blogu(s4, "ImageNet")
    # ---- Ek Tablo 3 (sayfa 14): CIFAR-10 + CIFAR-100 + ImageNet
    s14 = S[14]
    t3_alinti = " ".join(s14[0:4])
    _, t3_c10 = beyaz_kutu_blogu(s14, "CIFAR-10")
    _, t3_c100 = beyaz_kutu_blogu(s14, "CIFAR-100")
    t3_t1_tutarli = t3_c10 == t1_c10

    # ---- Tablo 2 (sayfa 6): transfer matrisleri
    s6 = S[6]
    t2_alinti = " ".join(s6[0:3])
    sut10, M10, k = transfer_blogu(s6, "CIFAR-10")
    sut100, M100, k = transfer_blogu(s6, "CIFAR-100", k)
    sutIN, MIN, _ = transfer_blogu(s6, "ImageNet", k)

    t1_adlar = [r["model"] for r in t1_c10]
    t2_adlar = [AD_ESLEME.get(a, a) for a in sut10]
    assert t2_adlar == t1_adlar, (t2_adlar, t1_adlar)
    assert [AD_ESLEME.get(a, a) for a in sut100] == t1_adlar
    assert [r["model"] for r in t3_c100] == t1_adlar

    # ---- Yon dogrulamasi: baslik "ilk sutun = kaynak C_i" der; Bolum 4.2 metni
    # tersini der. Bolum 4.3 anlatisindaki sayilarla hangisinin dogru oldugu sinanir.
    s5 = " ".join(S[5])
    rx = re.compile(r"\((\d+\.\d)%, (\d+\.\d)% and (\d+\.\d)% for CIFAR-10,\s*CIFAR-100\s*and\s*ImageNet")
    anlati = [tuple(float(x) for x in m.groups()) for m in rx.finditer(s5)]
    assert len(anlati) >= 2, anlati
    bit_to_vitl, vitl_to_bit = anlati[0], anlati[1]
    a1 = re.search(r"Adversar-?\s*ial examples generated using BiT-50x1 are misclassi\S*\s*by ViT-L-16.*?respectively\)", s5)
    a2 = re.search(r"Likewise, less than half the time\s*BiT-M-50x1 is fooled by adversarial examples generated\s*using ViT-L-16[^)]*\)", s5)
    s7 = " ".join(S[6] + S[7])
    m7 = re.search(r"BiT-\s*M-152x4 only (\d+\.\d)% of the time", s7)
    iBit, iVl = sut10.index("BiT-50x1"), sut10.index("ViT-L-16")
    jBitIN, jVlIN, jB152 = sutIN.index("BiT-50x1"), sutIN.index("ViT-L-16 (512)"), sutIN.index("BiT-152x4")
    satir_kaynak = {
        "CIFAR-10 M[BiT-50x1][ViT-L-16] == anlati BiT->ViT-L-16": M10[iBit][iVl] == bit_to_vitl[0],
        "CIFAR-100 M[BiT-50x1][ViT-L-16] == anlati": M100[iBit][iVl] == bit_to_vitl[1],
        "ImageNet M[BiT-50x1][ViT-L-16 (512)] == anlati": MIN[jBitIN][jVlIN] == bit_to_vitl[2],
        "CIFAR-10 M[ViT-L-16][BiT-50x1] == anlati ViT-L-16->BiT": M10[iVl][iBit] == vitl_to_bit[0],
        "CIFAR-100 M[ViT-L-16][BiT-50x1] == anlati": M100[iVl][iBit] == vitl_to_bit[1],
        "ImageNet M[ViT-L-16 (512)][BiT-50x1] == anlati": MIN[jVlIN][jBitIN] == vitl_to_bit[2],
        "ImageNet M[ViT-L-16 (512)][BiT-152x4] == sayfa 7 (ViT-L-16 -> BiT-M-152x4)":
            (m7 is not None and MIN[jVlIN][jB152] == float(m7.group(1))),
    }
    yon_sonuc = all(satir_kaynak.values())
    s45 = " ".join(S[4] + S[5])
    celiski = re.search(r"The top row of the\s*table corresponds to the model which was used to generate\s*the adversarial examples", s45)
    kopya = re.search(r"In the special case\s*when i = j, we train an independent copy of model i[^.]*\.", s45)
    tum = " ".join(ln for k_ in sorted(S) for ln in S[k_])
    m21k = re.search(r"pre-training dataset\s*\(X\s*′,\s*Y\s*′\)\s*is ImageNet-21K[^.]*\.", tum)
    m1000 = re.search(r"we ﬁ?\S*nd a set\s*of m = 1000 examples that both classi\S*ers correctly iden-?\s*tify", s45)

    def mat_sozluk(sut, M):
        ad = [AD_ESLEME.get(a, a) for a in sut]
        return {ad[i]: {ad[j]: M[i][j] for j in range(len(ad))} for i in range(len(ad))}

    tab = {
        "uretildi_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "kaynaklar": dict(KAYNAK),
        "yontem": "PDF'den cikarilmis metin sayfa ayiraclarina bolunur; Tablo 1 (s.4), Ek Tablo 3 (s.14) ve "
                  "Tablo 2 (s.6) hucreleri satir basina tek deger bicimindedir ve regex ^(\\d+(\\.\\d+)?)%$ ile okunur. "
                  "Elle verilen yalniz aile etiketi ve Tablo 2 kisaltma -> Tablo 1 ad eslemesidir (sira ile assert).",
        "kunye": "Mahmood, Mahmood, van Dijk. On the Robustness of Vision Transformers to Adversarial Examples. "
                 "ICCV 2021, arXiv:2104.02610",
        "model_adlari": t1_adlar,
        "tablo2_kisa_adlar": sut10,
        "ad_esleme_tablo2_tablo1": AD_ESLEME,
        "aile": AILE,
        "temiz_dogruluk_yuzde": {
            "CIFAR-10": {r["model"]: r["Acc"] for r in t1_c10},
            "CIFAR-100": {r["model"]: r["Acc"] for r in t3_c100},
            "CIFAR-100_kaynak_notu": "Ana metin Tablo 1'de YOK; ek malzeme Tablo 3 (sayfa 14) iceriyor ve oradan okundu.",
        },
        "beyaz_kutu_saglam_dogruluk_yuzde": {
            "sutunlar": bas10,
            "CIFAR-10_tablo1": t1_c10,
            "CIFAR-100_ek_tablo3": t3_c100,
            "ImageNet_tablo1": t1_in,
            "ek_tablo3_CIFAR-10_ile_tablo1_ayni_mi": t3_t1_tutarli,
        },
        "transfer_matrisleri_yuzde": {
            "yorum": "satir = kaynak C_i (cekismeli ornegi ureten), sutun = hedef C_j (degerlendiren). "
                     "Hucre = FGSM/PGD/MIM'in en buyugu, m = 1000 HER IKISI DOGRU ornek (Denklem 3).",
            "CIFAR-10": mat_sozluk(sut10, M10),
            "CIFAR-100": mat_sozluk(sut100, M100),
            "ImageNet": {"sutunlar": sutIN, "matris_satir_kaynak": MIN,
                         "not": "'+' = olculmedi (i = j), None olarak yazildi"},
        },
        "yon_dogrulamasi": {
            "tablo2_basligi": "first column = model used to generate the adversarial examples, C_i; top row = model used to evaluate, C_j",
            "bolum_4_2_metni_celisiyor_mu": celiski is not None,
            "bolum_4_2_alinti": celiski.group(0) if celiski else None,
            "bolum_4_3_anlati_BiT_to_ViTL16": bit_to_vitl,
            "bolum_4_3_anlati_ViTL16_to_BiT": vitl_to_bit,
            "anlati_alinti_1": a1.group(0) if a1 else None,
            "anlati_alinti_2": a2.group(0) if a2 else None,
            "hucre_kontrolleri": satir_kaynak,
            "sonuc_satir_kaynak": yon_sonuc,
            "hukum": ("Bolum 4.3 anlatisi ve sayfa 7 orneginin yedi hucresi de 'satir = kaynak' okumasiyla birebir tutuyor; "
                      "Bolum 4.2'deki 'ust satir = kaynak' cumlesi baslik ve anlatiyla celisen bir yazim hatasidir."
                      if yon_sonuc else "YON BELIRSIZ: anlati hucreleri satir=kaynak okumasiyla tutmuyor."),
        },
        "kosegen_notu": {
            "alinti": kopya.group(0) if kopya else None,
            "hukum": "Kosegen beyaz kutu DEGILDIR: i = j icin bagimsiz egitilmis ikinci kopyaya transferdir. "
                     "Ayristirmalarda kosegen kullanilmaz.",
        },
        "protokol_alinti": m1000.group(0) if m1000 else None,
        "on_egitim_alinti": m21k.group(0) if m21k else None,
        "sayfalar": {"tablo1": 4, "tablo2": 6, "ek_tablo3": 14, "anlati": 5},
        "baslik_alintilari": {"tablo1": t1_alinti, "tablo2": t2_alinti, "ek_tablo3": t3_alinti},
    }
    yaz(OUT_TAB, tab)
    on_egitim_alinti = tab["on_egitim_alinti"]

    # ================================================================ ozdeslik
    kaydet_kaynak(OZDES)
    with io.open(OZDES, encoding="utf-8") as fh:
        oz = json.load(fh)
    p_min = oz["ozet"]["P_advyanlis_verili_temizyanlis"]["min"]
    p_ort = oz["ozet"]["P_advyanlis_verili_temizyanlis"]["ort"]
    P_DEGER = {"p=1 (ust sinir)": 1.0, f"p=p_min={p_min} (ozdeslik_kontrol min)": p_min}

    def ozdeslik_ham(r_tc, e_t, p):
        return e_t * p + r_tc * (1 - e_t)

    def yon_ongoru(r_bc, e_s, e_t, p):
        """bc oranindan ham orani ongorur. r_tc bilinmez; merkez r_tc = r_bc.
        Varsayimsiz sinir: q = P(kaynak temiz yanlis | hedef temiz dogru) <= min(1, e_s/(1-e_t));
        r_tc = (1-q) r_bc + q f, f in [0,1]  ->  r_tc in [r_bc(1-qmax), r_bc + qmax(1-r_bc)]."""
        qmax = min(1.0, e_s / (1 - e_t))
        tc_lo, tc_hi = r_bc * (1 - qmax), r_bc + qmax * (1 - r_bc)
        return {
            "ham_merkez": ozdeslik_ham(r_bc, e_t, p),
            "ham_alt": ozdeslik_ham(tc_lo, e_t, p),
            "ham_ust": ozdeslik_ham(tc_hi, e_t, p),
            "tc_aralik": [tc_lo, tc_hi],
            "qmax": qmax,
        }

    ozdeslik = {}
    for ds, M, acc in (("CIFAR-10", M10, {r["model"]: r["Acc"] for r in t1_c10}),
                       ("CIFAR-100", M100, {r["model"]: r["Acc"] for r in t3_c100})):
        adlar = t1_adlar
        yonler = []
        for i, s in enumerate(adlar):
            for j, t in enumerate(adlar):
                if i == j:
                    continue
                r_bc = M[i][j] / 100
                e_s, e_t = 1 - acc[s] / 100, 1 - acc[t] / 100
                kayit = {"kaynak": s, "hedef": t, "bc_yuzde": M[i][j],
                         "e_kaynak_yuzde": 100 * e_s, "e_hedef_yuzde": 100 * e_t}
                for etk, p in P_DEGER.items():
                    o = yon_ongoru(r_bc, e_s, e_t, p)
                    kayit[etk] = {"ham_ongoru_yuzde": 100 * o["ham_merkez"],
                                  "ham_ongoru_aralik_yuzde": [100 * o["ham_alt"], 100 * o["ham_ust"]],
                                  "ham_eksi_bc_puan": 100 * (o["ham_merkez"] - r_bc),
                                  "ham_eksi_bc_aralik_puan": [100 * (o["ham_alt"] - r_bc), 100 * (o["ham_ust"] - r_bc)]}
                yonler.append(kayit)
        Y = {(y["kaynak"], y["hedef"]): y for y in yonler}

        # --- ciftler: asimetri ve ongorulen protokol etkisi
        ciftler = []
        for i, a in enumerate(adlar):
            for j, b in enumerate(adlar):
                if j <= i:
                    continue
                fa, fb = AILE[a], AILE[b]
                # yon: aileler arasi ciftte CNN -> ViT eksi ViT -> CNN (makale konvansiyonu)
                if {fa, fb} in ({"CNN", "ViT"}, {"CNN", "hibrit"}):
                    c, v = (a, b) if fa == "CNN" else (b, a)
                    tur = "aileler_arasi" + ("_hibrit" if "hibrit" in (fa, fb) else "")
                else:
                    c, v = a, b
                    tur = "aile_ici"
                ileri, geri = Y[(c, v)], Y[(v, c)]
                kayit = {"cift": f"{c} vs {v}", "tur": tur,
                         "asimetri_tanimi": f"{c}->{v} eksi {v}->{c}",
                         "temiz_dogruluk_farki_puan": acc[c] - acc[v],
                         "temiz_hata_farki_mutlak_puan": abs(acc[c] - acc[v]),
                         "asimetri_bc_puan": ileri["bc_yuzde"] - geri["bc_yuzde"]}
                for etk in P_DEGER:
                    hi, hg = ileri[etk], geri[etk]
                    asim_ham = hi["ham_ongoru_yuzde"] - hg["ham_ongoru_yuzde"]
                    lo = hi["ham_ongoru_aralik_yuzde"][0] - hg["ham_ongoru_aralik_yuzde"][1]
                    up = hi["ham_ongoru_aralik_yuzde"][1] - hg["ham_ongoru_aralik_yuzde"][0]
                    kayit[etk] = {
                        "asimetri_ham_ongoru_puan": asim_ham,
                        "asimetri_ham_ongoru_aralik_puan": [lo, up],
                        "protokol_etkisi_ham_eksi_bc_puan": asim_ham - kayit["asimetri_bc_puan"],
                        "protokol_etkisi_aralik_puan": [lo - kayit["asimetri_bc_puan"], up - kayit["asimetri_bc_puan"]],
                        "isaret_degisir_mi_merkez": (asim_ham > 0) != (kayit["asimetri_bc_puan"] > 0),
                        "isaret_degisebilir_mi_aralik": (lo <= 0 <= up) or ((lo > 0) != (kayit["asimetri_bc_puan"] > 0)),
                    }
                ciftler.append(kayit)

        # --- aile ozeti: hangi aile guclu kaynak?
        def ort(xs):
            return sum(xs) / len(xs) if xs else None

        aile_ozet = {}
        for hibrit_vit_mi in (False, True):
            vitler = [m for m in adlar if AILE[m] == "ViT" or (hibrit_vit_mi and AILE[m] == "hibrit")]
            cnnler = [m for m in adlar if AILE[m] == "CNN"]
            c2v = [Y[(c, v)]["bc_yuzde"] for c in cnnler for v in vitler]
            v2c = [Y[(v, c)]["bc_yuzde"] for c in cnnler for v in vitler]
            n_vit_guclu = sum(Y[(v, c)]["bc_yuzde"] > Y[(c, v)]["bc_yuzde"] for c in cnnler for v in vitler)
            aile_ozet["hibrit_ViT_sayildi" if hibrit_vit_mi else "hibrit_haric"] = {
                "ViT_modelleri": vitler, "CNN_modelleri": cnnler,
                "CNN_to_ViT_bc_ortalama_yuzde": ort(c2v),
                "ViT_to_CNN_bc_ortalama_yuzde": ort(v2c),
                "aile_asimetrisi_CNNtoViT_eksi_ViTtoCNN_puan": ort(c2v) - ort(v2c),
                "ViT_daha_guclu_kaynak_oldugu_cift_sayisi": n_vit_guclu,
                "cift_sayisi": len(cnnler) * len(vitler),
                "guclu_kaynak_ailesi": "ViT" if ort(v2c) > ort(c2v) else "CNN",
            }

        # alt aile: on egitimli BiT-M ile sifirdan ResNet ayri (hibrit haric ViT'lere karsi)
        vitler = [m for m in adlar if AILE[m] == "ViT"]
        for alt_ad, alt in (("BiT-M", [m for m in adlar if m.startswith("BiT-M")]),
                            ("ResNet", [m for m in adlar if m.startswith("ResNet")])):
            c2v = [Y[(c, v)]["bc_yuzde"] for c in alt for v in vitler]
            v2c = [Y[(v, c)]["bc_yuzde"] for c in alt for v in vitler]
            aile_ozet[f"alt_aile_{alt_ad}_vs_ViT"] = {
                "CNN_modelleri": alt, "ViT_modelleri": vitler,
                "CNN_to_ViT_bc_ortalama_yuzde": ort(c2v),
                "ViT_to_CNN_bc_ortalama_yuzde": ort(v2c),
                "aile_asimetrisi_CNNtoViT_eksi_ViTtoCNN_puan": ort(c2v) - ort(v2c),
                "CNN_daha_guclu_kaynak_oldugu_cift_sayisi": sum(
                    Y[(c, v)]["bc_yuzde"] > Y[(v, c)]["bc_yuzde"] for c in alt for v in vitler),
                "cift_sayisi": len(alt) * len(vitler),
                "CNN_temiz_dogruluk_yuzde": {c: acc[c] for c in alt},
            }

        arasi = [c for c in ciftler if c["tur"] == "aileler_arasi"]
        etk1 = list(P_DEGER)[0]
        etkmin = list(P_DEGER)[1]
        en_buyuk = max(arasi, key=lambda c: abs(c[etk1]["protokol_etkisi_ham_eksi_bc_puan"]))
        ozdeslik[ds] = {
            "yonler": yonler,
            "ciftler": ciftler,
            "aile_ozeti": aile_ozet,
            "aileler_arasi_ozet": {
                "cift_sayisi": len(arasi),
                "temiz_hata_farki_max_puan": max(c["temiz_hata_farki_mutlak_puan"] for c in arasi),
                "abs_asimetri_bc_min_puan": min(abs(c["asimetri_bc_puan"]) for c in arasi),
                "abs_protokol_etkisi_max_puan_p1": abs(en_buyuk[etk1]["protokol_etkisi_ham_eksi_bc_puan"]),
                "abs_protokol_etkisi_max_cift": en_buyuk["cift"],
                "isaret_degisen_cift_sayisi_merkez_p1": sum(c[etk1]["isaret_degisir_mi_merkez"] for c in arasi),
                "isaret_degisen_cift_sayisi_merkez_pmin": sum(c[etkmin]["isaret_degisir_mi_merkez"] for c in arasi),
                "isaret_degisebilir_cift_sayisi_aralik_p1": sum(c[etk1]["isaret_degisebilir_mi_aralik"] for c in arasi),
                "protokol_etkisi_bolu_abs_asimetri_max_p1": max(
                    abs(c[etk1]["protokol_etkisi_ham_eksi_bc_puan"]) / abs(c["asimetri_bc_puan"])
                    for c in arasi if c["asimetri_bc_puan"] != 0),
            },
        }

    # --- (ii) anahtar cift: BiT-M-R50x1 <-> ViT-L-16
    anahtar = {}
    for ds in ("CIFAR-10", "CIFAR-100"):
        c = next(x for x in ozdeslik[ds]["ciftler"] if x["cift"] == "BiT-M-R50x1 vs ViT-L-16")
        anahtar[ds] = c

    # --- (iv) bizim CIFAR-10 ciftimiz (c1_transfer_summary, uc tohum ortalamasi)
    kaydet_kaynak(BIZIM)
    with io.open(BIZIM, encoding="utf-8") as fh:
        biz = json.load(fh)
    P = biz["protocols"]
    acc_vit = P["target_correct"]["n_cond_CNN_to_ViT"]["mean"] / P["raw"]["n_cond_CNN_to_ViT"]["mean"] * 100
    acc_cnn = P["target_correct"]["n_cond_ViT_to_CNN"]["mean"] / P["raw"]["n_cond_ViT_to_CNN"]["mean"] * 100
    asim = {k: P[k]["diff"]["mean"] for k in ("raw", "target_correct", "both_correct", "successful_source")}
    # Mahmood'a uyguladigimiz ayni yaklasimi (r_tc = r_bc) bizim veride sinayalim: bc'den ham ongoru
    e_v, e_c = 1 - acc_vit / 100, 1 - acc_cnn / 100
    bc_c2v, bc_v2c = P["both_correct"]["CNN_to_ViT"]["mean"] / 100, P["both_correct"]["ViT_to_CNN"]["mean"] / 100
    tc_c2v, tc_v2c = P["target_correct"]["CNN_to_ViT"]["mean"] / 100, P["target_correct"]["ViT_to_CNN"]["mean"] / 100
    biz_ongoru = {}
    for etk, p in P_DEGER.items():
        a_bc = 100 * ((ozdeslik_ham(bc_c2v, e_v, p)) - ozdeslik_ham(bc_v2c, e_c, p))
        a_tc = 100 * ((ozdeslik_ham(tc_c2v, e_v, p)) - ozdeslik_ham(tc_v2c, e_c, p))
        biz_ongoru[etk] = {
            "ham_asimetri_ongoru_bc_den_rtc_esit_rbc_varsayimi_puan": a_bc,
            "ham_asimetri_ongoru_tc_den_tam_ozdeslik_puan": a_tc,
            "gozlenen_ham_asimetri_puan": asim["raw"],
            "yaklasim_hatasi_bc_den_puan": a_bc - asim["raw"],
            "protokol_etkisi_ongoru_ham_eksi_bc_puan": a_bc - asim["both_correct"],
        }
    biz_k = {
        "kaynak": BIZIM,
        "temiz_dogruluk_ResNet18_AT_yuzde": acc_cnn,
        "temiz_dogruluk_ViT_Tiny_AT_yuzde": acc_vit,
        "temiz_dogruluk_farki_puan": acc_cnn - acc_vit,
        "asimetri_CNNtoViT_eksi_ViTtoCNN_puan": asim,
        "gozlenen_ham_eksi_tc_puan": asim["raw"] - asim["target_correct"],
        "gozlenen_ham_eksi_bc_puan": asim["raw"] - asim["both_correct"],
        "ozdeslik_sinamasi": biz_ongoru,
        "guclu_kaynak_ailesi_bizde": "CNN" if asim["both_correct"] > 0 else "ViT",
        "kaynak_temiz_hata_bizde_yuzde": {"ResNet18_AT": 100 - acc_cnn, "ViT_Tiny_AT": 100 - acc_vit},
        "kaynak_temiz_hata_max_Mahmood_CIFAR10_yuzde": max(100 - r["Acc"] for r in t1_c10),
        "kaynak_temiz_hata_max_Mahmood_CIFAR100_yuzde": max(100 - r["Acc"] for r in t3_c100),
        "not": "Mahmood'a r_tc = r_bc yaklasimiyla uygulanan ongoru bizim veride sinanir (yaklasim_hatasi alani); "
               "yaklasim hatasi kaynak temiz hatasiyla buyur, bu yuzden bizim ciftteki hata Mahmood CIFAR-10 icin "
               "ust sinir niteligindedir.",
    }

    k10 = anahtar["CIFAR-10"]
    etk1 = list(P_DEGER)[0]
    yorum = {
        "anahtar_cift_CIFAR10": (
            f"BiT-M-R50x1 vs ViT-L-16: temiz fark {k10['temiz_dogruluk_farki_puan']:+.2f} puan (CNN eksi ViT), "
            f"bc asimetrisi {k10['asimetri_bc_puan']:+.2f} puan, p=1 ile ongorulen ham asimetri "
            f"{k10[etk1]['asimetri_ham_ongoru_puan']:+.2f} puan; protokol etkisi "
            f"{k10[etk1]['protokol_etkisi_ham_eksi_bc_puan']:+.2f} puan."),
    }
    oz10 = ozdeslik["CIFAR-10"]["aileler_arasi_ozet"]
    guclu10 = ozdeslik["CIFAR-10"]["aile_ozeti"]["hibrit_haric"]["guclu_kaynak_ailesi"]
    if (oz10["isaret_degisen_cift_sayisi_merkez_p1"] == 0
            and oz10["isaret_degisebilir_cift_sayisi_aralik_p1"] == 0
            and guclu10 != biz_k["guclu_kaynak_ailesi_bizde"]):
        yorum["uzlasma"] = (
            f"Mahmood CIFAR-10'da guclu kaynak ailesi {guclu10}, bizde {biz_k['guclu_kaynak_ailesi_bizde']}. "
            f"Aileler arasi {oz10['cift_sayisi']} ciftin hicbirinde ozdeslikle ongorulen ham-bc protokol etkisi "
            f"asimetrinin isaretini cevirmiyor, varsayimsiz aralikta bile (en buyuk |etki| "
            f"{oz10['abs_protokol_etkisi_max_puan_p1']:.2f} puan, en kucuk |bc asimetrisi| "
            f"{oz10['abs_asimetri_bc_min_puan']:.2f} puan). "
            f"CIFAR-10'da protokol farki iki calismanin yon celiskisini aciklamaz.")
    else:
        yorum["uzlasma"] = ("CIFAR-10'da ozdeslik en az bir aileler arasi ciftte isareti cevirebiliyor ya da aile yonu "
                            "bizimkiyle ayni; ayrintilar aileler_arasi_ozet ve ciftler alanlarinda.")
    for ds in ("CIFAR-10", "CIFAR-100"):
        etk1 = list(P_DEGER)[0]
        don = [c for c in ozdeslik[ds]["ciftler"] if c["tur"] == "aileler_arasi" and c[etk1]["isaret_degisir_mi_merkez"]]
        cnn_guclu = [c for c in ozdeslik[ds]["ciftler"] if c["tur"] == "aileler_arasi" and c["asimetri_bc_puan"] > 0]
        yorum[f"isaret_donen_ciftler_{ds}"] = {
            "bc_de_CNN_guclu_kaynak_olan_ciftler": [c["cift"] for c in cnn_guclu],
            "ham_ongoruyle_isaret_donen_ciftler_p1_merkez": [c["cift"] for c in don],
            "not": "Merkez tahmin r_tc = r_bc; aralik alanlari varsayimsiz sinirlari verir. Aralik sifiri iceriyorsa "
                   "donus kesin degildir.",
        }

    out = {
        "uretildi_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "kaynaklar": dict(KAYNAK) | {OUT_TAB: sha256(OUT_TAB)},
        "yontem": ("Ozdeslik r_ham = e_t * p + r_tc * (1 - e_t). Mahmood yalniz bc (her ikisi dogru) verir; merkez "
                   "tahminde r_tc = r_bc alinir. Varsayimsiz aralik: q = P(kaynak temiz yanlis | hedef temiz dogru) "
                   "<= min(1, e_s / (1 - e_t)), r_tc in [r_bc(1-q), r_bc + q(1-r_bc)]. p iki degerle: 1 (ust sinir) "
                   "ve ozdeslik_kontrol.json'daki bizim yonlerimizin en kucuk p'si. Asimetri aileler arasi ciftte "
                   "CNN->ViT eksi ViT->CNN; protokol etkisi = ongorulen ham asimetri eksi bc asimetrisi. "
                   "Kosegen (bagimsiz kopya) kullanilmaz."),
        "p_degerleri": {"p_min": p_min, "p_ort": p_ort, "kaynak": OZDES,
                        "not": "p bizim cekismeli egitilmis (AT) yonlerimizde olculdu; Mahmood modelleri standart egitimli, "
                               "orada p olculmedi. p = 1 ust sinir olarak raporlanir."},
        "rejim_notlari": {
            "on_egitim": "ViT ve BiT-M modelleri ImageNet-21K on egitimli, CIFAR'a ince ayarli (alinti asagida); "
                         "ResNet-56/164 icin on egitim belirtilmiyor",
            "on_egitim_alinti": on_egitim_alinti,
            "egitim": "standart (cekismeli egitim YOK); Tablo 1'de PGD/C&W/APGD saglam dogrulugu ~%0 (tablolar.json)",
            "epsilon": "l_inf, eps = 0.031 (Tablo 1 basligi); bizimki 8/255",
            "saldiri": "hucre basina FGSM, PGD, MIM'in EN BUYUGU (Tablo 2 basligi); bizimki tek PGD-10",
            "protokol": "her ikisi dogru (Denklem 3), cift basina m = 1000 ornek; bizimki tam test kumesi, dort protokol",
            "kosegen": "i = j bagimsiz egitilmis kopya; beyaz kutu degil",
            "model_olcegi": "ViT-B/L ve BiT-M buyuk on egitimli modeller; bizimki ViT-Tiny / ResNet-18 / WRN-28-10, "
                            "CIFAR uzerinde sifirdan cekismeli egitim",
        },
        "ozdeslik": ozdeslik,
        "anahtar_cift_BiT-M-R50x1_ViT-L-16": anahtar,
        "bizim_CIFAR10_ciftimiz": biz_k,
        "yorum": yorum,
    }
    yaz(OUT_OZ, out)

    # --- konsol ozeti
    for ds in ("CIFAR-10", "CIFAR-100"):
        print(ds, json.dumps(ozdeslik[ds]["aile_ozeti"], ensure_ascii=False))
        print(ds, json.dumps(ozdeslik[ds]["aileler_arasi_ozet"], ensure_ascii=False))
        print(ds, "anahtar", json.dumps(anahtar[ds], ensure_ascii=False))
    print("yon dogrulamasi:", tab["yon_dogrulamasi"]["sonuc_satir_kaynak"], tab["yon_dogrulamasi"]["hucre_kontrolleri"])
    print("bizim:", json.dumps(biz_k, ensure_ascii=False))


if __name__ == "__main__":
    main()
