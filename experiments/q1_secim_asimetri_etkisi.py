#!/usr/bin/env python3
"""Gorev 1.3: secim kuralinin asimetriye etkisi, SAKLI yorungelerden (GPU yok).

Girdiler
  results/q1/e3_akolu_v2/A_*_ep*.json  KANONIK A kolu (siki successful_source; e3_iki_kol_fit.json
                                       'A_kolu_kaynak_dizin' alani bu dizini gosterir)
  results/q1/e3_akolu/A_*_ep*.json     B2 oncesi ilk kosum (successful_source GEVSEK maskeyle);
                                       yalniz karsilastirma icin
  results/q1/e2/e2_grid.json           CIFAR-10 18 hucrelik secim izgarasi (bolme x patience x yumusatma)
  results/q1/e2/select_*_val{A,B,C}.json  CIFAR-10 tek kural (patience 20) secimleri
  results/q1/b8_secim_bandi.json       CIFAR-100 9 hucrelik secim izgarasi
Cikti
  results/q1/secim_asimetri_etkisi.json

A kolu kaydi: bir model M (taranan yorunge, epok c) ile SABIT es P arasinda iki yon.
Kayittaki 'asimetri' = (P -> M) eksi (M -> P). Makale konvansiyonu CNN->ViT eksi ViT->CNN
oldugu icin ResNet yorungelerinde isaret CEVRILIR (asimetri_makale alani). Yayilim isaretten
bagimsizdir. CIFAR-10 yorungeleri E2 yeniden egitimleridir (models/q1/e2), es model C1 best.pth;
CIFAR-100 ve SVHN yorungeleri E1/E7 egitimlerinin kendisidir.

Calistirma (depo kokunden):
  docker exec -w /workspace adeb_eval python experiments/q1_secim_asimetri_etkisi.py
"""
import datetime
import glob
import hashlib
import io
import json
import os
import re
import sys

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
os.chdir(ROOT)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OUT = "results/q1/secim_asimetri_etkisi.json"
DIZINLER = {"e3_akolu_v2": "results/q1/e3_akolu_v2", "e3_akolu": "results/q1/e3_akolu"}
KANONIK = "e3_akolu_v2"
E2_GRID = "results/q1/e2/e2_grid.json"
B8 = "results/q1/b8_secim_bandi.json"
PROT = ["raw", "target_correct", "both_correct", "successful_source"]
KAYNAK = {}


def sha256(yol):
    h = hashlib.sha256()
    with open(yol, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def oku_json(yol):
    KAYNAK[yol] = sha256(yol)
    with io.open(yol, encoding="utf-8") as fh:
        return json.load(fh)


def yorunge_serileri(dizin):
    kayitlar = {}
    for f in sorted(glob.glob(f"{dizin}/A_*_ep*.json")):
        d = oku_json(f)
        kayitlar.setdefault(d["trajectory_id"], []).append(d)
    out = {}
    for tid, lst in kayitlar.items():
        lst.sort(key=lambda d: d["epoch"])
        cnn_yorunge = "_rn18_" in tid
        isaret = -1.0 if cnn_yorunge else 1.0   # makale konvansiyonu: CNN->ViT eksi ViT->CNN
        seri = []
        for d in lst:
            a = {p: isaret * d["asimetri"][p] for p in PROT}
            uc = [a["raw"], a["target_correct"], a["both_correct"]]
            # temiz hata: ileri yonun hedefi M, geri yonun hedefi P
            e_M, e_P = d["e_hedef_ileri"], d["e_hedef_geri"]
            e_vit, e_cnn = (e_P, e_M) if cnn_yorunge else (e_M, e_P)
            seri.append({
                "epoch": d["epoch"],
                "asimetri_makale": a,
                "yayilim_dort": max(a.values()) - min(a.values()),
                "yayilim_dort_kayittaki": d["y_asimetri_yayilimi"],
                "yayilim_uc_ss_haric": max(uc) - min(uc),
                "e_ViT": e_vit, "e_CNN": e_cnn,
                "temiz_hata_farki_ViT_eksi_CNN": e_vit - e_cnn,
                "x_temiz_hata_farki_mutlak": d["x_temiz_hata_farki"],
                "ozdeslik_artik_ileri": d.get("ozdeslik_artik_ileri"),
                "ozdeslik_artik_geri": d.get("ozdeslik_artik_geri"),
            })
        out[tid] = {
            "dataset": lst[0]["dataset"], "kume": lst[0]["kume"],
            "taranan_model": "ResNet-18" if cnn_yorunge else "ViT-Tiny",
            "yon_ileri_ornek": lst[0]["yon_ileri"],
            "seri": seri,
        }
    return out


def yorunge_ozeti(y):
    s = y["seri"]
    ilk, son = s[0], s[-1]

    def aralik(f):
        v = [f(r) for r in s]
        return {"min": min(v), "max": max(v), "max_eksi_min": max(v) - min(v)}

    x = np.array([r["temiz_hata_farki_ViT_eksi_CNN"] for r in s])
    xa = np.array([r["x_temiz_hata_farki_mutlak"] for r in s])
    ozet = {
        "epoklar": [r["epoch"] for r in s],
        "ilk_epok": ilk["epoch"], "son_epok": son["epoch"],
        "ilk": {"asimetri": ilk["asimetri_makale"], "yayilim_dort": ilk["yayilim_dort"],
                "yayilim_uc": ilk["yayilim_uc_ss_haric"], "temiz_hata_farki_ViT_eksi_CNN": ilk["temiz_hata_farki_ViT_eksi_CNN"]},
        "son": {"asimetri": son["asimetri_makale"], "yayilim_dort": son["yayilim_dort"],
                "yayilim_uc": son["yayilim_uc_ss_haric"], "temiz_hata_farki_ViT_eksi_CNN": son["temiz_hata_farki_ViT_eksi_CNN"]},
        "aralik_asimetri": {p: aralik(lambda r, p=p: r["asimetri_makale"][p]) for p in PROT},
        "aralik_yayilim_dort": aralik(lambda r: r["yayilim_dort"]),
        "aralik_yayilim_uc": aralik(lambda r: r["yayilim_uc_ss_haric"]),
        "aralik_temiz_hata_farki": aralik(lambda r: r["temiz_hata_farki_ViT_eksi_CNN"]),
    }
    if len(s) >= 3 and np.ptp(xa) > 0:
        for ad, key in (("yayilim_dort", "yayilim_dort"), ("yayilim_uc", "yayilim_uc_ss_haric")):
            yv = np.array([r[key] for r in s])
            b1, b0 = np.polyfit(xa, yv, 1)
            ozet[f"yorunge_ici_{ad}_vs_x_mutlak"] = {"egim": float(b1), "kesisim": float(b0),
                                                    "pearson_r": float(np.corrcoef(xa, yv)[0, 1]), "n": len(s)}
        for p in PROT:
            yv = np.array([r["asimetri_makale"][p] for r in s])
            ozet.setdefault("yorunge_ici_asimetri_vs_isaretli_fark", {})[p] = {
                "egim": float(np.polyfit(x, yv, 1)[0]), "pearson_r": float(np.corrcoef(x, yv)[0, 1])}
    return ozet


def secim_baglantisi(y, epoklar_secim):
    """Secilen epok -> saklanan en yakin A kolu epogu (stride ~10, ara deger yok)."""
    s = y["seri"]
    ep = np.array([r["epoch"] for r in s])
    out = []
    for etiket, e in epoklar_secim:
        i = int(np.argmin(np.abs(ep - e)))
        alt = [r for r in s if r["epoch"] <= e]
        ust = [r for r in s if r["epoch"] >= e]
        out.append({
            "hucre": etiket, "secilen_epok": e,
            "en_yakin_sakli_epok": int(ep[i]), "uzaklik_epok": int(abs(ep[i] - e)),
            "en_yakin_asimetri": s[i]["asimetri_makale"],
            "en_yakin_yayilim_dort": s[i]["yayilim_dort"],
            "en_yakin_yayilim_uc": s[i]["yayilim_uc_ss_haric"],
            "en_yakin_temiz_hata_farki_ViT_eksi_CNN": s[i]["temiz_hata_farki_ViT_eksi_CNN"],
            "alt_komsu_epok": alt[-1]["epoch"] if alt else None,
            "ust_komsu_epok": ust[0]["epoch"] if ust else None,
        })
    return out


def main():
    seriler = {ad: yorunge_serileri(d) for ad, d in DIZINLER.items()}
    e2 = oku_json(E2_GRID)
    b8 = oku_json(B8)
    sel_files = sorted(glob.glob("results/q1/e2/select_*_val*.json"))
    tek_kural = {}
    for f in sel_files:
        d = oku_json(f)
        m = re.search(r"select_(resnet18|vit_tiny)_s(\d+)_val([ABC])\.json", f)
        tek_kural.setdefault((m.group(1), m.group(2)), []).append(
            (f"val{m.group(3)} (patience {d['selection_rule']['patience']}, k=1)", d["selected_epoch"],
             d["test"]["clean_acc"], d["test"]["adv_acc"]))

    def secimler(tid, ds):
        """yorunge -> [(etiket, epok)] secim hucreleri; yoksa []"""
        m = re.match(r"A_(c10|c100|svhn)_(rn18|vit)_s(\d+)", tid)
        mim = "resnet18" if m.group(2) == "rn18" else "vit_tiny"
        tohum = m.group(3)
        if m.group(1) == "c10":
            hucre = e2["mimariler"][mim]["per_seed"][tohum]["hucreler"]
            ref = e2["referans_protokol"]
            lst = [(f"E2 bolme {h['split']} patience {h['patience']} k {h['k']}"
                    + (" [REFERANS]" if (h['split'], h['patience'], h['k']) == (ref['bolme'], ref['patience'], ref['k']) else ""),
                    h["secilen_epok"]) for h in hucre]
            lst += [(f"E2 tek kural {et}", e) for et, e, _, _ in tek_kural.get((mim, tohum), [])]
            return lst
        if m.group(1) == "c100":
            yor = b8["veri_kumeleri"]["cifar100"]["yorungeler"].get(f"{mim}_s{tohum}")
            if not yor:
                return []
            # E1 egitim kurali patience 20, yumusatmasiz (k=1): best.pth bu hucreye karsilik gelir
            return [(f"B8 patience {h['patience']} k {h['k']}"
                     + (" [REFERANS]" if (h['patience'], h['k']) == (20, 1) else ""), h["secilen_epok"])
                    for h in yor["hucreler"]]
        return []

    sonuc = {}
    for ad, ser in seriler.items():
        blok = {}
        for tid, y in sorted(ser.items()):
            oz = yorunge_ozeti(y)
            sec = secimler(tid, y["dataset"])
            bag = secim_baglantisi(y, sec) if sec else "yok (bu veri kumesi icin secim izgarasi yok)"
            if sec:
                vals = {p: [b["en_yakin_asimetri"][p] for b in bag] for p in PROT}
                yay = [b["en_yakin_yayilim_dort"] for b in bag]
                yay3 = [b["en_yakin_yayilim_uc"] for b in bag]
                eps = sorted({b["en_yakin_sakli_epok"] for b in bag})
                ref = [b for b in bag if "REFERANS" in b["hucre"]]
                sec_ozet = {
                    "secilen_epoklar": sorted({b["secilen_epok"] for b in bag}),
                    "eslesen_sakli_epoklar": eps,
                    "max_uzaklik_epok": max(b["uzaklik_epok"] for b in bag),
                    "secim_hucreleri_arasi_asimetri_araligi": {p: [min(v), max(v)] for p, v in vals.items()},
                    "secim_hucreleri_arasi_yayilim_dort_araligi": [min(yay), max(yay)],
                    "secim_hucreleri_arasi_yayilim_uc_araligi": [min(yay3), max(yay3)],
                    "referans_hucre": ref[0] if ref else None,
                    "son_epok_eksi_referans": ({
                        "asimetri": {p: y["seri"][-1]["asimetri_makale"][p] - ref[0]["en_yakin_asimetri"][p] for p in PROT},
                        "yayilim_dort": y["seri"][-1]["yayilim_dort"] - ref[0]["en_yakin_yayilim_dort"],
                        "yayilim_uc": y["seri"][-1]["yayilim_uc_ss_haric"] - ref[0]["en_yakin_yayilim_uc"],
                    } if ref else None),
                    "UYARI": "A kolu stride ~10 epok; secilen epok saklanan noktaya denk gelmeyebilir. Deger EN YAKIN "
                             "saklanan epoktandir, ara deger kestirimi yapilmadi.",
                }
            else:
                sec_ozet = "yok"
            blok[tid] = {"bilgi": {k: y[k] for k in ("dataset", "kume", "taranan_model", "yon_ileri_ornek")},
                         "ozet": oz, "secim_hucreleri": bag, "secim_ozeti": sec_ozet, "seri": y["seri"]}
        sonuc[ad] = blok

    # --- veri kumesi duzeyi: tum yorungelerde ilk/son ve max-min
    duzey = {}
    for tid, b in sonuc[KANONIK].items():
        ds = b["bilgi"]["dataset"]
        d = duzey.setdefault(ds, {"yorunge_sayisi": 0, "son_eksi_ilk_yayilim_dort": [], "yayilim_dort_max_eksi_min": [],
                                  "asimetri_tc_max_eksi_min": [], "asimetri_bc_max_eksi_min": [],
                                  "yorunge_ici_r_yayilim_uc_vs_x": [], "yorunge_ici_r_yayilim_dort_vs_x": []})
        d["yorunge_sayisi"] += 1
        oz = b["ozet"]
        d["son_eksi_ilk_yayilim_dort"].append(oz["son"]["yayilim_dort"] - oz["ilk"]["yayilim_dort"])
        d["yayilim_dort_max_eksi_min"].append(oz["aralik_yayilim_dort"]["max_eksi_min"])
        d["asimetri_tc_max_eksi_min"].append(oz["aralik_asimetri"]["target_correct"]["max_eksi_min"])
        d["asimetri_bc_max_eksi_min"].append(oz["aralik_asimetri"]["both_correct"]["max_eksi_min"])
        if "yorunge_ici_yayilim_uc_vs_x_mutlak" in oz:
            d["yorunge_ici_r_yayilim_uc_vs_x"].append(oz["yorunge_ici_yayilim_uc_vs_x_mutlak"]["pearson_r"])
            d["yorunge_ici_r_yayilim_dort_vs_x"].append(oz["yorunge_ici_yayilim_dort_vs_x_mutlak"]["pearson_r"])

    # --- v1 / v2 karsilastirmasi (ayni epoklar)
    karsi = {}
    for tid, b in sonuc[KANONIK].items():
        if tid not in sonuc["e3_akolu"]:
            continue
        s2 = {r["epoch"]: r for r in b["seri"]}
        s1 = {r["epoch"]: r for r in sonuc["e3_akolu"][tid]["seri"]}
        ort = sorted(set(s1) & set(s2))
        karsi[tid] = {
            "ortak_epok": len(ort),
            "max_abs_fark_raw": max(abs(s2[e]["asimetri_makale"]["raw"] - s1[e]["asimetri_makale"]["raw"]) for e in ort),
            "max_abs_fark_tc": max(abs(s2[e]["asimetri_makale"]["target_correct"] - s1[e]["asimetri_makale"]["target_correct"]) for e in ort),
            "max_abs_fark_ss": max(abs(s2[e]["asimetri_makale"]["successful_source"] - s1[e]["asimetri_makale"]["successful_source"]) for e in ort),
        }

    out = {
        "uretildi_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "kaynaklar": dict(KAYNAK),
        "yontem": ("A kolu kayitlari trajectory_id basina epok sirasina dizilir. Asimetri makale konvansiyonuna "
                   "(CNN->ViT eksi ViT->CNN) cevrilir: ResNet yorungelerinde kayittaki (P->M) - (M->P) isaret "
                   "degistirir. Yayilim dort protokolde ve uc protokolde (successful_source haric) max-min. "
                   "Yorunge ici iliski: yayilimin |temiz hata farki|'na EKK egimi ve Pearson r (epok noktalari, "
                   "cikarim amacli degil, betimsel). Secim baglantisi: E2 (CIFAR-10, 18 hucre + valA/B/C tek kural) ve "
                   "B8 (CIFAR-100, 9 hucre) izgaralarindaki secilen epok, saklanan en yakin A kolu epoguna eslenir."),
        "kanonik_dizin": DIZINLER[KANONIK],
        "dizin_notu": ("e3_akolu (ilk kosum) successful_source'u GEVSEK maskeyle (tc & sa) yazar ve PGD tohumu "
                       "(yorunge, epok)'a bagli degildir; e3_akolu_v2 siki maske ve ck_tohum tasir ve "
                       "e3_iki_kol_fit.json'un kullandigi dizindir. Ana sonuclar v2'den."),
        "yon_notu": ("CIFAR-10 yorungeleri E2 yeniden egitimleridir (C1 modelleri DEGIL); es model C1 best.pth. "
                     "Bu nedenle CIFAR-10'da 'son epok' C1 ciftinin son kontrol noktasi degil, ayni tohumlu E2 "
                     "kosusunun 100. epogudur. CIFAR-100'de yorunge E1 egitiminin kendisidir ve erken durdurmayla "
                     "biter; son epok = durus epogu."),
        "veri_kumesi_duzeyi": {ds: {k: (ozet if not isinstance(ozet, list) else
                                        {"degerler": ozet, "min": min(ozet) if ozet else None,
                                         "max": max(ozet) if ozet else None})
                                    for k, ozet in v.items()} for ds, v in duzey.items()},
        "v1_v2_karsilastirma": karsi,
        "yorungeler": sonuc,
        "eksikler": {
            "SVHN_secim_izgarasi": "yok (E7 icin secim izgarasi dosyasi yok)",
            "C1_ViT_2002_epok18_secimi": ("C1 modellerinin epok yorungesi A kolunda yok; CIFAR-10 A kolu E2 yeniden "
                                         "egitimlerini tarar. C1 secim epoku logs/ altindadir, burada kullanilmadi."),
            "ara_epoklar": "A kolu stride ~10; secilen epoklarin tam degeri yok, en yakin saklanan epok kullanildi.",
        },
    }
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print("yazildi:", OUT)

    for tid, b in sonuc[KANONIK].items():
        oz = b["ozet"]
        so = b["secim_ozeti"]
        print(f"{tid:20s} ep {oz['ilk_epok']:>3}->{oz['son_epok']:>3} | asim tc {oz['ilk']['asimetri']['target_correct']:+6.2f}->{oz['son']['asimetri']['target_correct']:+6.2f}"
              f" bc {oz['ilk']['asimetri']['both_correct']:+6.2f}->{oz['son']['asimetri']['both_correct']:+6.2f}"
              f" raw {oz['ilk']['asimetri']['raw']:+6.2f}->{oz['son']['asimetri']['raw']:+6.2f}"
              f" | yay4 {oz['ilk']['yayilim_dort']:5.2f}->{oz['son']['yayilim_dort']:5.2f} yay3 {oz['ilk']['yayilim_uc']:5.2f}->{oz['son']['yayilim_uc']:5.2f}"
              f" | dx {oz['ilk']['temiz_hata_farki_ViT_eksi_CNN']:+6.2f}->{oz['son']['temiz_hata_farki_ViT_eksi_CNN']:+6.2f}"
              f" | r3 {oz.get('yorunge_ici_yayilim_uc_vs_x_mutlak', {}).get('pearson_r', float('nan')):+.3f}"
              f" r4 {oz.get('yorunge_ici_yayilim_dort_vs_x_mutlak', {}).get('pearson_r', float('nan')):+.3f}")
        if isinstance(so, dict):
            print("      secim epok", so["secilen_epoklar"], "-> sakli", so["eslesen_sakli_epoklar"],
                  "| tc", [round(v, 2) for v in so["secim_hucreleri_arasi_asimetri_araligi"]["target_correct"]],
                  "bc", [round(v, 2) for v in so["secim_hucreleri_arasi_asimetri_araligi"]["both_correct"]],
                  "yay4", [round(v, 2) for v in so["secim_hucreleri_arasi_yayilim_dort_araligi"]],
                  "| ref", None if not so["referans_hucre"] else (so["referans_hucre"]["secilen_epok"], so["referans_hucre"]["en_yakin_sakli_epok"],
                  {p: round(v, 2) for p, v in so["referans_hucre"]["en_yakin_asimetri"].items()},
                  round(so["referans_hucre"]["en_yakin_yayilim_dort"], 2), round(so["referans_hucre"]["en_yakin_yayilim_uc"], 2),
                  round(so["referans_hucre"]["en_yakin_temiz_hata_farki_ViT_eksi_CNN"], 2)),
                  "| son-ref", None if not so["son_epok_eksi_referans"] else
                  {k: (round(v, 2) if not isinstance(v, dict) else {a: round(c, 2) for a, c in v.items()})
                   for k, v in so["son_epok_eksi_referans"].items()})
    print(json.dumps(out["veri_kumesi_duzeyi"], indent=0)[:3000])
    print(karsi)


if __name__ == "__main__":
    main()
