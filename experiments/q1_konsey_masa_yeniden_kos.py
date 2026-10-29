# -*- coding: utf-8 -*-
"""Konsey planinda sayi kaynagi olarak anilan masa betiklerini, ciktilarini results/q1/konsey_masa/ altina
yazacak bicimde yeniden kosar ve eski ciktilarla (raporlar/konsey_2026-10-29/*.json) karsilastirir.

Betiklerin kendisi DEGISTIRILMEZ: kaynak metin okunur, yalniz cikti (ve carpimsal betikte yorunge girdisi)
yolu metin ikamesiyle degistirilir, ikame sayisi denetlenir ve __file__ ozgun yol olarak verilerek exec edilir.
Planda anilanlar: _p3_carpimsal_yasa_masa (havuz_AT7.w_beyaz_kutu, log_tau_simetri_ihlali_rms, A_kolu) ve
_p3_potansiyel_masa (havuz_cifar10.ayar_testi). _p3_carpimsal_yasa_masa, A_kolu icin _p3_yorunge_gurbuzluk_masa
ciktisini okudugundan o da yeniden kosulur.
Cikti: results/q1/konsey_masa/_p3_*.json ve results/q1/konsey_masa/yeniden_kos_karsilastirma.json
"""
import hashlib
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
KL = KOK / "raporlar" / "konsey_2026-10-29"
YENI = KOK / "results" / "q1" / "konsey_masa"

ESKI_W = 'os.path.join(KOK, "raporlar", "konsey_2026-10-29", "{ad}.json")'
YENI_W = 'os.path.join(KOK, "results", "q1", "konsey_masa", "{ad}.json")'
ISLER = [
    ("_p3_yorunge_gurbuzluk_masa", [(ESKI_W, YENI_W)]),
    ("_p3_carpimsal_yasa_masa", [(ESKI_W, YENI_W),
                                 ('oku("raporlar/konsey_2026-10-29/_p3_yorunge_gurbuzluk_masa.json")',
                                  'oku("results/q1/konsey_masa/_p3_yorunge_gurbuzluk_masa.json")')]),
    ("_p3_potansiyel_masa", [(ESKI_W, YENI_W)]),
    # 29.10 dogrulayici duzeltmesi (madde 6): planda sayi kaynagi olarak anilmayan, ama raporlar/ altinda cikti
    # birakan masa betikleri de results/q1/konsey_masa/ altina yeniden kosulur.
    ("_p3_havuz_gurbuzluk_yasasi", [(ESKI_W, YENI_W)]),
    ("_P2_panel_masa", [('"raporlar/konsey_2026-10-29/{ad}.json"', '"results/q1/konsey_masa/{ad}.json"')]),
    ("_P2_panel_logit", [('"raporlar/konsey_2026-10-29/{ad}.json"', '"results/q1/konsey_masa/{ad}.json"')]),
    ("_P2_panel_logit_ayri", [('"raporlar/konsey_2026-10-29/{ad}.json"', '"results/q1/konsey_masa/{ad}.json"')]),
    ("_rb_liste", [("/workspace/raporlar/konsey_2026-10-29/{ad}.json", "/workspace/results/q1/konsey_masa/{ad}.json")]),
    ("_rb_imagenet_P2", [("/workspace/raporlar/konsey_2026-10-29/{ad}.json",
                          "/workspace/results/q1/konsey_masa/{ad}.json")]),
]
YOKSAY = {"uretildi_utc"}


def duz(x, on=""):
    out = {}
    if isinstance(x, dict):
        for k, v in x.items():
            if k in YOKSAY:
                continue
            out.update(duz(v, f"{on}.{k}" if on else k))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            out.update(duz(v, f"{on}[{i}]"))
    else:
        out[on] = x
    return out


def karsilastir(eski, yeni):
    e, y = duz(eski), duz(yeni)
    sayisal, farkli_metin, enb = 0, [], 0.0
    enb_anahtar = None
    for k in set(e) & set(y):
        a, b = e[k], y[k]
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
            sayisal += 1
            d = abs(float(a) - float(b))
            if d > enb:
                enb, enb_anahtar = d, k
        elif a != b:
            farkli_metin.append(k)
    return {"ortak_yaprak": len(set(e) & set(y)), "sayisal_yaprak": sayisal, "en_buyuk_mutlak_fark": enb,
            "en_buyuk_fark_anahtari": enb_anahtar, "farkli_sayisal_olmayan": sorted(farkli_metin)[:20],
            "yalniz_eskide": sorted(set(e) - set(y))[:20], "yalniz_yenide": sorted(set(y) - set(e))[:20],
            "ozdes": enb == 0.0 and not farkli_metin and set(e) == set(y)}


def main():
    YENI.mkdir(parents=True, exist_ok=True)
    rapor = {"betik": "experiments/q1_konsey_masa_yeniden_kos.py", "uretildi_utc": datetime.now(timezone.utc).isoformat(),
             "isler": {}}
    for ad, ikameler in ISLER:
        kaynak = KL / f"{ad}.py"
        src = kaynak.read_text(encoding="utf-8")
        for eski, yeni in ikameler:
            e, y = eski.format(ad=ad), yeni.format(ad=ad)
            n = src.count(e)
            if n != 1:
                raise SystemExit(f"{ad}: ikame '{e}' {n} kez bulundu (1 beklenir)")
            src = src.replace(e, y)
        g = {"__name__": "__main__", "__file__": str(kaynak)}
        exec(compile(src, str(kaynak), "exec"), g)
        eski_json = KL / f"{ad}.json"
        yeni_json = YENI / f"{ad}.json"
        kar = karsilastir(json.loads(eski_json.read_text(encoding="utf-8")),
                          json.loads(yeni_json.read_text(encoding="utf-8")))
        rapor["isler"][ad] = {"betik": str(kaynak.relative_to(KOK)),
                              "betik_sha256": hashlib.sha256(kaynak.read_bytes()).hexdigest(),
                              "ikameler": [[a.format(ad=ad), b.format(ad=ad)] for a, b in ikameler],
                              "eski_cikti": str(eski_json.relative_to(KOK)), "yeni_cikti": str(yeni_json.relative_to(KOK)),
                              "karsilastirma_uretildi_utc_haric": kar}
    with io.open(YENI / "yeniden_kos_karsilastirma.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(rapor, f, ensure_ascii=False, indent=1)
    for ad, v in rapor["isler"].items():
        k = v["karsilastirma_uretildi_utc_haric"]
        print(ad, "ozdes" if k["ozdes"] else "FARKLI", k["sayisal_yaprak"], k["en_buyuk_mutlak_fark"], k["farkli_sayisal_olmayan"][:3])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
