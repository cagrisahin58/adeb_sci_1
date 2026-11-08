# -*- coding: utf-8 -*-
"""Curutme zinciri denetimleri (08.11.2026). Konteynerde, depo kokunden.

Alt komutlar (her biri tek satir JSON basar; cikis kodu 0 = GECTI/TAMAM, 3 = KALDI, 2 = hesaplanamadi):
  esik      C1 V-scr temiz asamasinin en iyi dogrulama dogruluklarindan (logs/C1_clean_vit_200{1,2,3}.log,
            'Best accuracy: X%' satiri) ortalama + 5 puan esigini hesaplar (B manipulasyon denetimi).
  manip     --temiz-dir DIR [--esik E]: temiz asamanin TRAINING_COMPLETE best_acc'i (dogrulama bolmesi) >= esik mi.
  init      --log LOG --ad TIMM_ADI: temiz gunlugundeki INIT_WEIGHTS_RAPORU satirinda source_sha256, indirme
            denetimindeki (results/q1/curutme_2026-11-08/indirme_denetimi.json) HF LFS ozetiyle ayni mi ve
            norm_matches_cfg dogru mu (C1/C2 manipulasyon denetimi).
  kirpilma  --at-dir DIR --takma T --sinir-s S: AT duvar saati siniriyla kesildiyse best.pth ve last.pth
            epoklarindan 'kirpilmis olabilir' isaretini (secilen epok son biten epogun 5 epok yakininda)
            hesaplar ve DIR/SURE_SINIRI dosyasina yazar. best.pth yoksa kod 3.
  epok      --log PILOT_LOG [--pilot-epok 2] [--pilot-s P] [--tavan-s 6300] [--en-cok 200]:
            E_temiz = min(en_cok, floor(tavan / t)). t baslatma suresini (veri ve model kurulumu) TASIMAZ:
            t = son pilot epogunun egitim dongusu suresi (tqdm cubugunun son 'N/N [MM:SS<' degeri) +
            epok basina dogrulama payi ((egitim suresi - cubuk sureleri toplami) / epok sayisi; egitim suresi
            Trainer'in 'Training completed in X minutes' satiri). Cubuk okunamazsa t = egitim suresi / epok.
            --pilot-s (duvar suresi) yalniz bilgi olarak yazilir. Curutme fable karari 08.11.2026 (curutucu tur 2),
            t = P / N (02_deney_adaylari.json B.durdurma_kurali).
"""
import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]


def yaz(d, kod):
    print(json.dumps(d, ensure_ascii=False))
    sys.exit(kod)


def c1_esik():
    vals, kaynak = [], []
    for s in (2001, 2002, 2003):
        p = KOK / f"logs/C1_clean_vit_{s}.log"
        son = None
        # satir numarasi standart sayimla ('\n'); read_text ve splitlines tqdm'in '\r'lerini de satir sayar
        for i, l in enumerate(p.read_bytes().decode("utf-8", errors="replace").split("\n"), 1):
            m = re.search(r"Best accuracy: ([0-9.]+)%", l)
            if m:
                son = (float(m.group(1)), i)
        if son is None:
            return None, kaynak
        vals.append(son[0])
        kaynak.append(f"logs/C1_clean_vit_{s}.log:{son[1]}")
    return vals, kaynak


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="komut", required=True)
    sp.add_parser("esik")
    m = sp.add_parser("manip")
    m.add_argument("--temiz-dir", required=True)
    m.add_argument("--esik", type=float, default=None)
    i = sp.add_parser("init")
    i.add_argument("--log", required=True)
    i.add_argument("--ad", required=True)
    k = sp.add_parser("kirpilma")
    k.add_argument("--at-dir", required=True)
    k.add_argument("--takma", required=True)
    k.add_argument("--sinir-s", type=float, required=True)
    e = sp.add_parser("epok")
    e.add_argument("--log", required=True, help="pilot temiz kosusunun logu")
    e.add_argument("--pilot-s", type=float, default=None, help="pilot duvar suresi (yalniz bilgi)")
    e.add_argument("--pilot-epok", type=int, default=2)
    e.add_argument("--tavan-s", type=float, default=1.75 * 3600)
    e.add_argument("--en-cok", type=int, default=200)
    a = ap.parse_args()

    if a.komut == "esik":
        vals, kaynak = c1_esik()
        if not vals:
            yaz({"durum": "HESAPLANAMADI", "kaynak": kaynak}, 2)
        ort = sum(vals) / len(vals)
        yaz({"durum": "TAMAM", "c1_vscr_temiz_dogrulama": vals, "ortalama": round(ort, 4),
             "esik": round(ort + 5.0, 4), "kaynak": kaynak}, 0)

    if a.komut == "manip":
        esik = a.esik
        if esik is None:
            vals, _ = c1_esik()
            if not vals:
                yaz({"durum": "HESAPLANAMADI"}, 2)
            esik = sum(vals) / len(vals) + 5.0
        tc = Path(a.temiz_dir) / "TRAINING_COMPLETE"
        if not tc.exists():
            yaz({"durum": "HESAPLANAMADI", "neden": f"{tc} yok"}, 2)
        d = dict(l.split("=", 1) for l in tc.read_text().split() if "=" in l)
        best = float(d["best_acc"])
        yaz({"durum": "GECTI" if best >= esik else "KALDI", "temiz_dogrulama_en_iyi": best,
             "esik": round(esik, 4), "epochs_run": int(d.get("epochs_run", -1)), "kaynak": str(tc)},
            0 if best >= esik else 3)

    if a.komut == "init":
        den = json.loads((KOK / "results/q1/curutme_2026-11-08/indirme_denetimi.json").read_text(encoding="utf-8"))
        bek = den["timm"].get(a.ad, {})
        satir = None
        for n, l in enumerate(Path(a.log).read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if l.startswith("INIT_WEIGHTS_RAPORU "):
                satir = (json.loads(l[len("INIT_WEIGHTS_RAPORU "):]), n)
        if satir is None:
            yaz({"durum": "HESAPLANAMADI", "neden": "INIT_WEIGHTS_RAPORU satiri yok", "log": a.log}, 2)
        r, n = satir
        hf = bek.get("hf_lfs_sha256") or bek.get("sha256")
        ok = (r.get("source_sha256") == hf and r.get("norm_matches_cfg") is True
              and (bek.get("fark_normu") or 0) > 0 and not r.get("missing_nonhead") and not r.get("shape_mismatch"))
        yaz({"durum": "GECTI" if ok else "KALDI", "log_satiri": f"{a.log}:{n}", "source_sha256": r.get("source_sha256"),
             "beklenen_sha256": hf, "hf_lfs_ile_dogrulandi": bek.get("sha256_hf_ile_ayni"),
             "norm_matches_cfg": r.get("norm_matches_cfg"), "pretrained_cfg_mean": r.get("pretrained_cfg_mean"),
             "pretrained_cfg_std": r.get("pretrained_cfg_std"), "in1k_agirligindan_fark_normu": bek.get("fark_normu")},
            0 if ok else 3)

    if a.komut == "kirpilma":
        import torch
        d = Path(a.at_dir)
        if not (d / "best.pth").exists():
            yaz({"durum": "KALDI", "neden": "best.pth yok"}, 3)
        be = torch.load(d / "best.pth", map_location="cpu", weights_only=False).get("epoch")
        le = None
        if (d / "last.pth").exists():
            le = torch.load(d / "last.pth", map_location="cpu", weights_only=False).get("epoch")
        kirp = (be is not None and le is not None and be >= le - 4)
        rec = {"takma": a.takma, "durum": "SURE_SINIRI", "sinir_s": a.sinir_s,
               "secilen_epok": (be + 1) if be is not None else None,
               "son_biten_epok": (le + 1) if le is not None else None, "kirpilmis_olabilir": kirp,
               "zaman_utc": datetime.now(timezone.utc).isoformat()}
        (d / "SURE_SINIRI").write_text(json.dumps(rec, ensure_ascii=False) + "\n")
        yaz(rec, 0)

    if a.komut == "epok":
        metin = Path(a.log).read_text(encoding="utf-8", errors="replace")
        parcalar = re.split(r"[\r\n]", metin)

        def sn(z):
            v = [int(x) for x in z.split(":")]
            return v[0] * 3600 + v[1] * 60 + v[2] if len(v) == 3 else v[0] * 60 + v[1]

        cubuk = {}
        for k in range(1, a.pilot_epok + 1):
            desen = re.compile(rf"Epoch {k}/\d+: 100%\|.*?\| (\d+)/\1 \[((?:\d+:)?\d+:\d+)<")
            bul = [m for m in (desen.search(x) for x in parcalar) if m]
            if bul:
                cubuk[k] = sn(bul[-1].group(2))
        tm = re.findall(r"Training completed in ([0-9.]+) minutes", metin)
        T = float(tm[-1]) * 60.0 if tm else None
        if T is None:
            yaz({"durum": "HESAPLANAMADI", "neden": "'Training completed in' satiri yok", "log": a.log}, 2)
        n_ozet = len(re.findall(r"Epoch \d+/\d+ - Train Loss", metin))
        if n_ozet != a.pilot_epok:
            yaz({"durum": "HESAPLANAMADI", "neden": f"logda {n_ozet} epok ozeti var, pilot {a.pilot_epok} epok olmali "
                 "(egitim suresi pilot disi epoklari tasir)", "log": a.log}, 2)
        if len(cubuk) == a.pilot_epok:
            dogrulama = max(0.0, (T - sum(cubuk.values())) / a.pilot_epok)
            t = cubuk[a.pilot_epok] + dogrulama
            yontem = "son_epok_cubugu_arti_dogrulama_payi"
        else:
            dogrulama = None
            t = T / a.pilot_epok
            yontem = "egitim_suresi_bolu_epok (cubuk okunamadi)"
        E = min(a.en_cok, int(math.floor(a.tavan_s / t)))
        yaz({"durum": "TAMAM", "yontem": yontem, "log": a.log, "pilot_epok": a.pilot_epok,
             "cubuk_suresi_s": cubuk, "egitim_suresi_s": round(T, 2),
             "dogrulama_payi_s": None if dogrulama is None else round(dogrulama, 2),
             "pilot_duvar_s_bilgi": a.pilot_s, "epok_suresi_s": round(t, 2),
             "tavan_s": a.tavan_s, "E_temiz": E}, 0)


if __name__ == "__main__":
    main()
