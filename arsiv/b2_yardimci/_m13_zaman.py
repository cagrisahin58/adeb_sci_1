# -*- coding: utf-8 -*-
"""Y5 (fig:prereg_chain) icin makine okunur zaman cizelgesi: results/q1/konsey_zaman_cizelgesi.json.

Olaylar ve kaynaklari (31.10.2026, deney-takibi):
  - on kayit ve ek on kayit dondurma anlari: git commit zamani (`git log -1 --format=%H|%cI`); dondurma commit'inin
    dosyayi ekleyen ilk commit oldugu `git log --diff-filter=A` ile denetlenir (git yalniz okunur);
  - B2 matrisi: gunlukte zaman damgasi yok; dosya degistirilme zamanlari (cells_meta.json kosu basinda, transfer_matrix.json
    sonunda yazilir; experiments/c1_c3_transfer_matrix.py satiri kanit olarak verilir) ve cozumleme JSON'unun uretildi_utc alani;
  - konsey zinciri (B2 cozumleme, B3, B4, B6, B5): results/q1/konsey_zincir_durum.tsv ve logs/konsey_zincir.log (salt okunur);
    B3'un alti kosusunun temiz ve AT asamalari zincir gunlugunun BASLA/BITTI satirlarindan, defterle capraz denetimli;
  - ek zincir (regresyon, B8-0, B9, B8, B10, cozumleme): results/q1/ek_loglar/ek_zincir_1.log ve ek_zincir_2.log;
  - hakem paneli sonrasi masa cozumlemeleri: results/q1/konsey_ek_masa/*.json uretildi_utc;
  - saat dilimi: her gunluk icin, gunlukteki bir adimin zamani ayni adimin yazdigi JSON'un uretildi_utc alaniyla
    karsilastirilarak saat farki hesaplanir (elle varsayim yok);
  - GPU adi ve bellegi: zincir gunlugundeki nvidia-smi dokumu; toplam egitim suresi: B3 defteri (foy M9.1 satiri verilir).
Calistirma: depo kokunden WSL'de `python3 arsiv/b2_yardimci/_m13_zaman.py` (git gerekir; yalniz standart kutuphane).
"""
import csv
import datetime as dt
import io
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _m13_ortak as O  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
CIKTI = "results/q1/konsey_zaman_cizelgesi.json"
OK = "raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md"
EK = "raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md"
ZD = "results/q1/konsey_zincir_durum.tsv"
ZL = "logs/konsey_zincir.log"
DF = "results/q1/konsey_b3_defter.tsv"
E1 = "results/q1/ek_loglar/ek_zincir_1.log"
E2 = "results/q1/ek_loglar/ek_zincir_2.log"
MD = "results/q1/konsey_ek_masa"
SP = "results/q1_research/ONKAYIT_SAPMALAR.md"
MX = "experiments/c1_c3_transfer_matrix.py"
J2 = "results/q1/konsey_ayrisim_b2.json"
J4 = "results/q1/konsey_ayrisim_b4.json"
J5 = "results/q1/konsey_ayrisim_b5.json"
J9 = "results/q1/konsey_b9_c100/b9_dondurulmus_b2.json"
J10 = "results/q1/konsey_b10_gradyan/b10_aile.json"
UTC = dt.timezone.utc
YEREL = None  # gosterim dilimi; main() basinda on kayit dondurma commit'inin saat diliminden alinir (elle deger yok)


def iso(t):
    return t.astimezone(UTC).isoformat()


def yerel(t):
    return t.astimezone(YEREL).strftime("%Y-%m-%d %H:%M:%S %z")


def git(*a):
    return subprocess.run(["git", "-C", str(O.KOK), *a], capture_output=True, text=True, check=True).stdout.strip()


def commit(kisa, dosya):
    h, ci = git("log", "-1", "--format=%H|%cI", kisa).split("|")
    ekleyen = git("log", "--format=%H", "--diff-filter=A", "--", dosya).split("\n")[-1]
    return {"commit": h, "commit_zamani": ci, "utc": iso(dt.datetime.fromisoformat(ci)),
            "yerel": yerel(dt.datetime.fromisoformat(ci)),
            "kaynak": f"git log -1 --format=%H|%cI {kisa}",
            "dosyayi_ekleyen_ilk_commit": ekleyen, "dondurma_commiti_dosyayi_ekleyen_ilk_commit": ekleyen == h}


def mtime(rel):
    O._OKUNAN.add(rel)
    return dt.datetime.fromtimestamp((O.KOK / rel).stat().st_mtime, UTC)


def jutc(rel, yol=("meta", "uretildi_utc")):
    d = O.jyukle(rel)
    x = d
    for p in yol:
        x = x[p]
    return dt.datetime.fromisoformat(x), ".".join(yol)


def utc_bul(d):
    """JSON icinde ilk 'uretildi_utc' alani (anahtar yoluyla)."""
    if isinstance(d, dict):
        if "uretildi_utc" in d:
            return d["uretildi_utc"], "uretildi_utc"
        for k_, v in d.items():
            r = utc_bul(v)
            if r:
                return r[0], f"{k_}.{r[1]}"
    return None


def saat(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def ofset(gunluk_zamani, utc_zamani, etiket):
    """Gunluk saati (dilimsiz) ile ayni olayin UTC zamani arasindaki saat farki (tam saate yuvarlanir) ve artik."""
    fark = (gunluk_zamani.replace(tzinfo=UTC) - utc_zamani).total_seconds()
    h = round(fark / 3600)
    return {"etiket": etiket, "saat_farki": h, "artik_s": round(fark - 3600 * h, 3)}


def main():
    global YEREL
    YEREL = dt.datetime.fromisoformat(git("log", "-1", "--format=%cI", "e32f2ce")).tzinfo
    # ---------------- dondurma anlari ----------------
    don = {"on_kayit": {**commit("e32f2ce", OK), "dosya": OK,
                        "metin_kaniti": f"{EK}:{O.bul(EK, 'dosyasına eklenen ayrı bir ön kayıttır')} (commit e32f2ce)"},
           "ek_on_kayit": {**commit("7325419", EK), "dosya": EK}}

    # ---------------- saat dilimi denetimi ----------------
    zd = list(csv.DictReader(io.StringIO("\n".join(O.satirlar(ZD))), delimiter="\t"))
    zrow = {r["adim"]: r for r in zd if r["adim"] != "zincir"}
    zof = []
    for adim, jrel in (("B2_cozumleme", J2), ("B4_cozumleme", J4), ("B5_cozumleme", J5)):
        u, _ = jutc(jrel)
        a, b = saat(zrow[adim]["baslangic"]), saat(zrow[adim]["bitis"])
        o = ofset(a, u, f"{ZD} {adim}.baslangic ile {jrel} meta.uretildi_utc")
        o["json_zamani_adim_icinde"] = a.replace(tzinfo=UTC) - dt.timedelta(hours=o["saat_farki"]) <= u <= \
            b.replace(tzinfo=UTC) - dt.timedelta(hours=o["saat_farki"])
        zof.append(o)
    E2L = O.satirlar(E2)
    n_coz = O.bul(E2, "adim cozumleme basliyor")
    n_bit = O.bul(E2, " bitti", bas=n_coz)
    t_coz = saat(E2L[n_coz - 1][:19])
    t_bit = saat(E2L[n_bit - 1][:19])
    eof = []
    for jrel in (J9, J10):
        u, _ = jutc(jrel)
        o = ofset(t_coz, u, f"{E2}:{n_coz} cozumleme baslangici ile {jrel} meta.uretildi_utc")
        o["json_zamani_adim_icinde"] = t_coz.replace(tzinfo=UTC) - dt.timedelta(hours=o["saat_farki"]) <= u <= \
            t_bit.replace(tzinfo=UTC) - dt.timedelta(hours=o["saat_farki"])
        eof.append(o)
    z_h = {o["saat_farki"] for o in zof}
    e_h = {o["saat_farki"] for o in eof}
    if len(z_h) != 1 or len(e_h) != 1:
        raise SystemExit(f"saat dilimi tutarsiz: zincir {z_h}, ek {e_h}")
    ZH, EH = z_h.pop(), e_h.pop()
    dilim = {"konsey_zinciri_saat_farki_utc_gore": ZH, "ek_zincir_saat_farki_utc_gore": EH, "konsey_zinciri_kanit": zof,
             "ek_zincir_kanit": eof,
             "not": "konteyner saati (zincir gunlugu, durum TSV'si, B3 defteri) ve ek zincir gunlukleri bu farkla UTC'ye cevrilir"}

    def z2u(s, h):
        return (saat(s) - dt.timedelta(hours=h)).replace(tzinfo=UTC)

    def olay(ad, bas, bit, kaynak, h, **ek):
        o = {"olay": ad, "baslangic_utc": iso(z2u(bas, h)) if bas else None, "bitis_utc": iso(z2u(bit, h)) if bit else None,
             "baslangic_yerel": yerel(z2u(bas, h)) if bas else None, "bitis_yerel": yerel(z2u(bit, h)) if bit else None,
             "gunluk_saati": {"baslangic": bas, "bitis": bit, "saat_farki_utc_gore": h}, "kaynak": kaynak}
        if bas and bit:
            o["sure_s"] = int((saat(bit) - saat(bas)).total_seconds())
        o.update(ek)
        return o

    # ---------------- B2 (gunluk damgasiz; dosya zamanlari) ----------------
    cm = mtime("results/q1/konsey_b2_panel/cells_meta.json")
    tm = mtime("results/q1/konsey_b2_panel/transfer_matrix.json")
    b2 = {"olay": "B2 matrisi (dosya zamanlari)", "baslangic_utc": iso(cm), "bitis_utc": iso(tm),
          "baslangic_yerel": yerel(cm), "bitis_yerel": yerel(tm), "sure_s": int((tm - cm).total_seconds()),
          "kaynak": "os.stat st_mtime: results/q1/konsey_b2_panel/cells_meta.json (baslangic vekili; "
                    f"{MX}:{O.bul(MX, 'meta_path.write_text(json.dumps(cell_cfg, indent=2))')} hucre hesabindan once yazar) ve "
                    "results/q1/konsey_b2_panel/transfer_matrix.json (bitis)",
          "kanit_turu": "dosya degistirilme zamani (gunluk degil)"}

    # ---------------- konsey zinciri ----------------
    zincir = []
    for r in zd:
        zincir.append(olay(r["adim"], r["baslangic"] or None, r["bitis"] or None,
                           f"{ZD}:{1 + zd.index(r) + 1}", ZH, durum=r["durum"], cikis_kodu=r["cikis_kodu"], **{"not": r["not"]}))
    # B3 asamalari (zincir gunlugu), defterle capraz
    ZLL = O.satirlar(ZL)
    bas_, bit_ = {}, {}
    for n, s in enumerate(ZLL, 1):
        m = re.match(r"\[([0-9: -]+)\] (BASLA|BITTI) (\S+_s\d+) (temiz|AT)[ :(]", s)
        if m:
            (bas_ if m.group(2) == "BASLA" else bit_)[(m.group(3), m.group(4))] = (m.group(1), n)
    df = list(csv.DictReader(io.StringIO("\n".join(O.satirlar(DF))), delimiter="\t"))
    dfi = {(r["takma_ad"], r["asama"]): (r, i + 2) for i, r in enumerate(df) if r["asama"] in ("temiz", "AT")}
    b3 = []
    for key in sorted(bas_, key=lambda x: bas_[x][1]):
        (b, nb), (e, ne) = bas_[key], bit_[key]
        r, nd = dfi[key]
        b3.append(olay(f"B3 {key[0]} {key[1]}", b, e, f"{ZL}:{nb}, {ZL}:{ne}", ZH, takma_ad=key[0], asama=key[1],
                       defter_satiri=f"{DF}:{nd}", defterle_ayni_baslangic=r["baslangic"] == b,
                       defter_bitis_farki_s=int((saat(r["bitis"]) - saat(e)).total_seconds()),
                       defter_sure_s=int(r["sure_s"])))
    # GPU
    n_gpu = O.bul(ZL, "NVIDIA GeForce", sira=0)
    g = ZLL[n_gpu - 1]
    gpu_adi = re.search(r"(NVIDIA GeForce [^|]+?)\s{2,}", g).group(1).strip()
    bel = re.search(r"(\d+)MiB /\s*(\d+)MiB", ZLL[n_gpu]).groups()
    E1L = O.satirlar(E1)
    n_e1 = O.bul(E1, " MiB, ")
    e1m = re.search(r"(\d+) MiB, (\d+) MiB", E1L[n_e1 - 1]).groups()
    n_kt = O.bul(ZL, "KUYRUK TAMAM; toplam egitim")
    tsa = sum(int(r["sure_s"]) for r in df if r["asama"] in ("temiz", "AT") and r["sure_s"])
    egitim = {"defter_toplam_sure_s": tsa, "defter_toplam_sure_sa": tsa / 3600,
              "kaynak": f"{DF} sure_s (asama temiz ve AT satirlari toplami)",
              "zincir_gunlugu_satiri": f"{ZL}:{n_kt}", "zincir_gunlugu_metni": ZLL[n_kt - 1].strip(),
              "foy": O.foy_satiri("### M9.1", "Defterdeki temiz ve AT asama surelerinin toplami"),
              "egitim_payi_on_kayit": f"{OK}:{O.bul(OK, '(e) Toplam GPU bütçesi')}"}
    donanim = {"gpu": gpu_adi, "gpu_bellek_toplam_mib": int(bel[1]), "gpu_bellek_kullanilan_mib_zincir_basi": int(bel[0]),
               "kaynak": f"{ZL}:{n_gpu}-{n_gpu + 1} (nvidia-smi dokumu, B3 on denetimi)",
               "ek_zincir_bellek": {"kullanilan_mib": int(e1m[0]), "toplam_mib": int(e1m[1]), "kaynak": f"{E1}:{n_e1}"}}

    # ---------------- ek zincir ----------------
    ek = []
    for rel in (E1, E2):
        L = O.satirlar(rel)
        adim = [(n, s[:19], re.match(r".{19} adim (\S+) basliyor", s).group(1)) for n, s in enumerate(L, 1)
                if re.match(r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d adim \S+ basliyor", s)]
        bit = [(n, s[:19]) for n, s in enumerate(L, 1) if re.match(r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d bitti$", s)]
        for i, (n, t, ad) in enumerate(adim):
            if i + 1 < len(adim):
                nb, tb, tur = adim[i + 1][0], adim[i + 1][1], "sonraki adimin baslangici"
            else:
                nb, tb = bit[-1]
                tur = "gunlugun 'bitti' satiri"
            rc = [s.strip() for s in L[n:nb - 1] if re.search(r"rc=\d+", s)]
            ek.append(olay(f"ek zincir: {ad}", t, tb, f"{rel}:{n}, {rel}:{nb}", EH, bitis_tanimi=tur, donus_kodlari=rc))

    # ---------------- B9/B8/B10 cozumleme JSON'lari ----------------
    coz = {}
    for rel in (J2, J4, J5, J9, "results/q1/konsey_b9_c100/b9_sarmalayici_b2.json",
                "results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json", "results/q1/konsey_b8_imagenetv2/b8_betimsel.json", J10):
        v, yol = utc_bul(O.jyukle(rel))
        coz[rel] = {"uretildi_utc": v, "anahtar": yol}

    # ---------------- masa cozumlemeleri (31.10) ----------------
    masa = {}
    for p in sorted((O.KOK / MD).glob("*.json")):
        rel = str(p.relative_to(O.KOK))
        r = utc_bul(O.jyukle(rel))
        if r:
            masa[rel] = {"uretildi_utc": r[0], "anahtar": r[1], "yerel": yerel(dt.datetime.fromisoformat(r[0]))}

    # ---------------- matris boyutlari ----------------
    matris = {}
    for blok, rel in (("B2", "results/q1/konsey_b2_panel/transfer_matrix.json"), ("B4", "results/q1/konsey_b4_matris/transfer_matrix.json"),
                      ("B5-MI", "results/q1/konsey_b5_saldiri/mi/transfer_matrix.json"),
                      ("B5-TGR", "results/q1/konsey_b5_saldiri/tgr/transfer_matrix.json"),
                      ("B9", "results/q1/konsey_b9_c100/matris/transfer_matrix.json"),
                      ("B8", "results/q1/konsey_b8_imagenetv2/matris/transfer_matrix.json")):
        d = O.jyukle(rel)
        matris[blok] = {"saldiri": d.get("attack"), "n_goruntu": d["n_samples"], "model_sayisi": len(d["models"]),
                        "hucre_sayisi": len(d["results"]), "kaynak_sayisi": len(d.get("sources") or []),
                        "eps_x255": d["eps"] * 255, "kaynak": f"{rel} attack, n_samples, models, results, sources, eps"}
    m6 = O.jyukle("results/q1/konsey_b6_maskeleme.json")
    matris["B6-AA"] = {"n_goruntu": m6["n"], "model_sayisi": len(m6["modeller"]),
                       "kaynak": "results/q1/konsey_b6_maskeleme.json n, modeller"}
    for v in ("cifar10", "cifar100", "imagenetv2"):
        rel = f"results/q1/konsey_b10_gradyan/mantel_{v}.json"
        d = O.jyukle(rel)
        matris[f"B10-{v}"] = {"model_sayisi": d["sinamalar"]["ham"]["K"], "cift_sayisi": d["sinamalar"]["ham"]["cift_sayisi"],
                              "kaynak": f"{rel} sinamalar.ham.K, .cift_sayisi"}

    # ---------------- kayit oncesi gorulen veri bolumleri ve sapma kayitlari ----------------
    ka, kb = O.bolum_araligi(OK, "## 1. Kayıt öncesinde görülmüş veriler")
    ea, eb = O.bolum_araligi(EK, "## 1. Kayıt öncesinde görülmüş veriler")
    sap = []
    for n, s in enumerate(O.satirlar(SP), 1):
        m = re.match(r"### (\d\d)\.(\d\d)\.(\d{4}), (.*)$", s)
        if m:
            sap.append({"tarih": f"{m.group(3)}-{m.group(2)}-{m.group(1)}", "baslik": m.group(4), "kaynak": f"{SP}:{n}",
                        "sapma_degil_ibaresi": "sapma değil" in s})

    govde = {"saat_dilimi": dilim, "dondurma": don, "B2": b2, "konsey_zinciri": zincir, "B3_asamalari": b3,
             "ek_zincir": ek, "cozumleme_jsonlari": coz, "masa_cozumlemeleri": masa, "matrisler": matris,
             "donanim": donanim, "egitim_suresi": egitim,
             "kayit_oncesi_gorulen_veriler": {"ana": f"{OK}:{ka}-{kb}", "ek": f"{EK}:{ea}-{eb}"},
             "sapma_kaydi_basliklari": sap,
             "denetimler": {
                 "B3_defter_baslangiclari_zincir_gunluguyle_ayni": all(x["defterle_ayni_baslangic"] for x in b3),
                 "B3_defter_bitis_farki_s_en_buyuk_mutlak": max(abs(x["defter_bitis_farki_s"]) for x in b3),
                 "B3_asama_sayisi": len(b3),
                 "ek_dondurma_konsey_zinciri_icinde": z2u(zrow["B3_kuyruk"]["baslangic"], ZH)
                 <= dt.datetime.fromisoformat(don["ek_on_kayit"]["commit_zamani"]) <= z2u(zrow["B3_kuyruk"]["bitis"], ZH),
                 "on_kayit_dondurmasi_B2_matrisinden_once": dt.datetime.fromisoformat(don["on_kayit"]["commit_zamani"]) < cm,
                 "ek_dondurma_ek_zincirden_once": dt.datetime.fromisoformat(don["ek_on_kayit"]["commit_zamani"])
                 < z2u(ek[0]["gunluk_saati"]["baslangic"], EH)}}
    O.yaz(CIKTI, govde, __file__, "Y5 fig:prereg_chain kaynagi: on kayit ve deney zinciri zaman cizelgesi",
          "Dondurma commit'leri, B2-B6 konsey zinciri, B3'un alti kosusunun asamalari, B8-B10 ek zinciri ve masa "
          "cozumlemeleri; her zaman UTC ve +03 olarak, gunluk saati ve saat dilimi kanitiyla.")


if __name__ == "__main__":
    main()
