# Bagimsiz kuru deneme (denetci): sahte matrislerle dondurulmus betigi b8/b9 tablolariyla dogrudan cagirir.
import json, sys, subprocess, hashlib
from pathlib import Path
import numpy as np
KOK = Path("/workspace")
OUT = KOK / "raporlar/konsey_2026-10-29/_ek_denetim/kuru"
OUT.mkdir(parents=True, exist_ok=True)
def sahte(dizin, adlar, n, tohum):
    rng = np.random.default_rng(tohum)
    dizin.mkdir(parents=True, exist_ok=True)
    tc = {m: rng.random(n) < 0.6 for m in adlar}
    guc = {m: 0.3 + 0.5 * rng.random() for m in adlar}
    sa = {s: rng.random(n) < guc[s] for s in adlar}
    for s in adlar:
        for t in adlar:
            aw = sa[s] if s == t else rng.random(n) < 0.6 * guc[s] * (0.4 + guc[t])
            np.savez(dizin / f"per_sample_{s}_to_{t}.npz", target_clean_correct=tc[t], target_adv_wrong=aw,
                     source_clean_correct=tc[s], source_adv_wrong=sa[s])
    (dizin / "transfer_matrix.json").write_text(json.dumps({"models": adlar, "SAHTE": True}))
sonuc = {}
for ad in ("b8", "b9"):
    tablo_yol = KOK / f"raporlar/konsey_2026-10-29/hucre_tablosu_{ad}.json"
    t = json.loads(tablo_yol.read_text(encoding="utf-8"))
    adlar = list(t["modeller"])
    d = OUT / f"sahte_{ad}"
    sahte(d, adlar, 400, 7 if ad == "b8" else 9)
    cikti = OUT / f"dondurulmus_{ad}.json"
    r = subprocess.run([sys.executable, "-B", "experiments/q1_konsey_ayrisim.py", "--mod", "b2", "--matris-dizini", str(d),
                        "--hucre-tablosu", str(tablo_yol), "--cikti", str(cikti), "--bootstrap", "200", "--sinama"],
                       cwd=KOK, capture_output=True, text=True)
    rec = {"rc": r.returncode, "stderr_son": r.stderr[-1500:], "stdout_son": r.stdout[-600:]}
    if cikti.exists():
        o = json.loads(cikti.read_text(encoding="utf-8"))
        b2 = o.get("b2", {})
        rec["panel"] = o.get("panel")
        rec["hata"] = o.get("hata")
        rec["hucreler"] = b2.get("hucreler")
        rec["tohum_ciftleri"] = b2.get("tohum_ciftleri")
        F = b2.get("F_B2", {})
        rec["F_B2_anahtarlar"] = sorted(F.keys()) if isinstance(F, dict) else str(type(F))
        rec["Ka_q"] = (F.get("K-a") or {}).get("q") if isinstance(F, dict) else None
        rec["Kb_degerler"] = (F.get("K-b") or {}).get("degerler") if isinstance(F, dict) else None
        rec["model_tablosu_eksik"] = {m: v for m, v in b2.get("model_tablosu", {}).items() if "eksik_hucreler" in v}
        rec["ust_anahtarlar"] = sorted(o.keys())
    # ek sarmalayici b8
    if ad == "b8":
        c2 = OUT / "ek_b8.json"
        r2 = subprocess.run([sys.executable, "-B", "experiments/q1_ek_ayrisim.py", "--mod", "b8", "--matris-dizini", str(d),
                             "--hucre-tablosu", str(tablo_yol), "--cikti", str(c2), "--bootstrap", "200", "--sinama"],
                            cwd=KOK, capture_output=True, text=True)
        rec["ek_b8_rc"] = r2.returncode
        rec["ek_b8_stderr"] = r2.stderr[-1500:]
        if c2.exists():
            o2 = json.loads(c2.read_text(encoding="utf-8"))
            rec["ek_b8_IN"] = {k: o2["A_sigma_IN"].get(k) for k in ("ciftler", "kestirim", "betimsel_etiket", "beklenti_esigi")}
            rec["ek_b8_scr"] = {k: o2["A_sigma_scr_Liu"].get(k) for k in ("ciftler", "kestirim", "betimsel_etiket", "beklenti_esigi")}
            rec["ek_b8_cift_satir"] = [(c["cift"], c["cnn"], c["donusturucu"], c["satir"]) for c in o2["ciftler"]]
    sonuc[ad] = rec
(OUT / "ozet.json").write_text(json.dumps(sonuc, indent=1, ensure_ascii=False))
print(json.dumps(sonuc, indent=1, ensure_ascii=False)[:6000])
