# -*- coding: utf-8 -*-
"""Ek cozumleme sarmalayicisinin GERCEK hucre tablolariyla kuru ayristirmasi (30.10.2026, CPU).

Dondurulmus hucre tablolarinin (hucre_tablosu_b9.json, hucre_tablosu_b8.json) takma adlariyla SAHTE
transfer matrisleri kurar (gecici klasorde) ve experiments/q1_ek_ayrisim.py'yi --sinama kipinde
--mod b9 ve --mod b8 ile cagirir. Amac yalniz kod yolunun gercek tablolarla uctan uca calistigini,
dondurulmus betigin sha256 denetimiyle yuklendigini ve B8'de IN satirina yalniz Singh ciftlerinin,
scr satirina Liu ciftinin girdigini gostermektir. Sayilar SAHTEDIR ve hicbir yerde kullanilmaz.

Konteynerde, depo kokunden, GPU'ya dokunmadan:
  docker exec -w /workspace -e CUDA_VISIBLE_DEVICES= adeb_eval python -B scripts/ek_kuru_ayristirma.py
Cikti: results/q1/ek_regresyon/kuru_ayristirma/{b9_kuru.json, b9_kuru.json.sarmalayici.json, b8_kuru.json, ozet.json}
"""
import hashlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

KOK = Path(__file__).resolve().parents[1]
TABLO9 = KOK / "raporlar/konsey_2026-10-29/hucre_tablosu_b9.json"
TABLO8 = KOK / "raporlar/konsey_2026-10-29/hucre_tablosu_b8.json"
OUT = KOK / "results/q1/ek_regresyon/kuru_ayristirma"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sahte_matris(dizin, adlar, n, tohum):
    """Ozgun npz semasinda sahte per_sample dosyalari (target/source clean correct, adv wrong)."""
    rng = np.random.default_rng(tohum)
    dizin.mkdir(parents=True, exist_ok=True)
    tc = {m: rng.random(n) < 0.7 for m in adlar}
    guc = {m: 0.3 + 0.4 * rng.random() for m in adlar}
    sa = {s: rng.random(n) < guc[s] for s in adlar}
    for s in adlar:
        for t in adlar:
            aw = sa[s] if s == t else rng.random(n) < 0.5 * guc[s] * (0.5 + guc[t])
            np.savez(dizin / f"per_sample_{s}_to_{t}.npz", target_clean_correct=tc[t], target_adv_wrong=aw,
                     source_clean_correct=tc[s], source_adv_wrong=sa[s])
    (dizin / "transfer_matrix.json").write_text(json.dumps({"models": adlar, "SAHTE": True}))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    spec = importlib.util.spec_from_file_location("q1_ek_ayrisim", KOK / "experiments/q1_ek_ayrisim.py")
    EK = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(EK)
    dm = EK.dondurulmus()  # sha256 denetimi burada; uyusmazlikta SystemExit
    OUT.mkdir(parents=True, exist_ok=True)
    gec = Path(tempfile.mkdtemp(prefix="ek_kuru_"))
    ozet = {"SAHTE_VERI_SONUC_DEGIL": True,
            "dondurulmus_betik_sha256": EK.sha256(EK.DONDURULMUS),
            "dondurulmus_betik_sha256_beklenen": EK.DONDURULMUS_SHA,
            "hucre_tablosu_b9_sha256": sha(TABLO9), "hucre_tablosu_b8_sha256": sha(TABLO8)}
    try:
        t9 = json.loads(TABLO9.read_text(encoding="utf-8"))
        a9 = list(t9["modeller"])
        sahte_matris(gec / "b9", a9, n=400, tohum=91)
        yan = EK.main(["--mod", "b9", "--matris-dizini", str(gec / "b9"), "--hucre-tablosu", str(TABLO9),
                       "--cikti", str(OUT / "b9_kuru.json"), "--bootstrap", "200", "--sinama"])
        r9 = json.loads((OUT / "b9_kuru.json").read_text(encoding="utf-8"))
        ozet["b9"] = {"model_sayisi": len(a9), "panel_birincil": len((r9.get("panel") or {}).get("birincil", [])),
                      "panel_ikincil": len((r9.get("panel") or {}).get("ikincil", [])),
                      "hata": r9.get("hata"), "F_B2_var": "F_B2" in (r9.get("b2") or {}),
                      "F_B2_aile_buyuklugu": len(((r9.get("b2") or {}).get("F_B2") or {}).get("p_holm", [])),
                      "dondurulmus_cikti_meta_sha": r9.get("meta", {}).get("betik_sha256"),
                      "sarmalayici_temiz_dogruluk_model_sayisi": len(yan["temiz_dogruluk_yuzde"])}

        t8 = json.loads(TABLO8.read_text(encoding="utf-8"))
        a8 = list(t8["modeller"])
        sahte_matris(gec / "b8", a8, n=400, tohum=81)
        r8 = EK.main(["--mod", "b8", "--matris-dizini", str(gec / "b8"), "--hucre-tablosu", str(TABLO8),
                      "--cikti", str(OUT / "b8_kuru.json"), "--bootstrap", "200", "--sinama"])
        ozet["b8"] = {"model_sayisi": len(a8), "panel_birincil": len(r8["panel"]["birincil"]),
                      "hata": r8.get("hata"),
                      "ciftler": [{k: c[k] for k in ("cift", "cnn", "donusturucu", "satir", "durum")}
                                  for c in r8.get("ciftler", [])],
                      "IN_satiri_ciftleri": r8.get("A_sigma_IN", {}).get("ciftler"),
                      "scr_satiri_ciftleri": r8.get("A_sigma_scr_Liu", {}).get("ciftler"),
                      "IN_beklenti_esigi": r8.get("A_sigma_IN", {}).get("beklenti_esigi"),
                      "scr_beklenti_esigi": r8.get("A_sigma_scr_Liu", {}).get("beklenti_esigi"),
                      "IN_bootstrap_tohum": r8.get("A_sigma_IN", {}).get("goruntu_bootstrap", {}).get("tohum")}
        # dondurulmus betigin B8 tablosuyla --mod b2 cagrisi da (ek on kayit §5.6) kuru kosulur
        dm.main(["--mod", "b2", "--matris-dizini", str(gec / "b8"), "--hucre-tablosu", str(TABLO8),
                 "--cikti", str(OUT / "b8_dondurulmus_b2_kuru.json"), "--bootstrap", "200", "--sinama"])
        r8b = json.loads((OUT / "b8_dondurulmus_b2_kuru.json").read_text(encoding="utf-8"))
        ozet["b8_dondurulmus_b2"] = {"hata": r8b.get("hata"), "F_B2_var": "F_B2" in (r8b.get("b2") or {})}
    finally:
        shutil.rmtree(gec, ignore_errors=True)
    ok = (ozet["dondurulmus_betik_sha256"] == ozet["dondurulmus_betik_sha256_beklenen"]
          and not ozet["b9"]["hata"] and ozet["b9"]["F_B2_var"]
          and not ozet["b8"]["hata"] and ozet["b8"]["IN_satiri_ciftleri"] == [1, 2]
          and ozet["b8"]["scr_satiri_ciftleri"] == [3] and ozet["b8_dondurulmus_b2"]["F_B2_var"])
    ozet["GECTI"] = bool(ok)
    with io.open(OUT / "ozet.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(ozet, f, ensure_ascii=False, indent=1)
    print(json.dumps(ozet, ensure_ascii=False, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
