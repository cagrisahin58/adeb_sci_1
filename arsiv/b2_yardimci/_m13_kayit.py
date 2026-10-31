# -*- coding: utf-8 -*-
"""Y4 (fig:registry_map) icin makine okunur kayit haritasi: results/q1/konsey_kayit_kurallari.json.

Her on kayitli sinama icin ongoru, destek ve curutme esikleri, Holm ailesi, delta, karar kurali ve gerceklesen karar.
Esik degerleri dondurulmus betiklerin kaynak satirlarindan duzenli ifadeyle okunur (elle sayi yok) ve ayni satirin
on kayit metnindeki karsiligi (ondalik virgullu yazim) denetlenir. Gerceklesen karar iki yerden okunur: sonuc JSON'unun
karar anahtari ve foyun (results/C1_REFERANS_FOYU.md) ilgili tablo hucresi; ikisinin ayni oldugu yazilir. Sonuc
sayilari (kestirim, aralik, p) bu dosyaya kopyalanmaz; foy satir numarasi verilir.
Calistirma: depo kokunden `python3 arsiv/b2_yardimci/_m13_kayit.py` (31.10.2026, deney-takibi).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _m13_ortak as O  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
CIKTI = "results/q1/konsey_kayit_kurallari.json"
DB = "experiments/q1_konsey_ayrisim.py"
EB = "experiments/q1_ek_ayrisim.py"
GB = "experiments/q1_ek_gradyan_kosinus.py"
MB = "scripts/konsey_b6_maskeleme.py"
OK = "raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md"
EK = "raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md"
J2 = "results/q1/konsey_ayrisim_b2.json"
J4 = "results/q1/konsey_ayrisim_b4.json"
J5 = "results/q1/konsey_ayrisim_b5.json"
M6 = "results/q1/konsey_b6_maskeleme.json"
J9 = "results/q1/konsey_b9_c100/b9_dondurulmus_b2.json"
J8 = "results/q1/konsey_b8_imagenetv2/b8_betimsel.json"
J10 = "results/q1/konsey_b10_gradyan/b10_aile.json"
NUM = r"(-?[0-9]+(?:\.[0-9]+)?)"


def kk(o):
    return f"{o['dosya']}:{o['satir']}"


def esik(ad, rel, parca, desen, bas=None, son=None, ok_rel=None, ok_parca=None, sira=None):
    """Kaynak satirindan esik degeri; ok_rel/ok_parca verilirse on kayit satirinda ondalik virgullu yazimi aranir."""
    o = O.kanit(rel, parca, desen, sira=sira, bas=bas or 1, son=son)
    e = {"ad": ad, "deger": o["deger"], "kaynak": kk(o), "kaynak_metni": o["metin"]}
    if ok_rel:
        # 31.10.2026 bulgu 4: isaretli, sozcuk sinirli, yuvarlamasiz arama (kural: O.ON_KAYIT_ARAMA_KURALI)
        n = O.bul(ok_rel, ok_parca)
        es = O.on_kayit_ara(ok_rel, n, o["deger"])
        e["on_kayit"] = f"{ok_rel}:{n}"
        e["on_kayit_metninde_yazimi"] = sorted({x["yazim"] for x in es})
        e["on_kayit_eslesmeleri"] = es
        e["on_kayit_aranan_yazimlar"] = O.ondalik_yazimlari(o["deger"])
        if not es:
            raise SystemExit(f"{ok_rel}:{n}: {ad} degeri ({O.ondalik_yazimlari(o['deger'])}, isaretli) metinde yok")
    return e


def ok_alinti(rel, parca, desen):
    """On kayit satirindan tam alinti (duzenli ifadenin ilk grubu); satir ve alinti birlikte."""
    n = O.bul(rel, parca)
    m = re.search(desen, O.satirlar(rel)[n - 1])
    if not m:
        raise SystemExit(f"{rel}:{n}: alinti deseni {desen!r} eslesmedi")
    return {"kaynak": f"{rel}:{n}", "alinti": m.group(1)}


def kural(rel, parca, bas=None, son=None, sira=None):
    o = O.kanit(rel, parca, bas=bas or 1, son=son, sira=sira)
    return {"kaynak": kk(o), "metin": o["metin"]}


def jget(d, yol):
    x = d
    for p in yol:
        x = x[p]
    return x


def gercek(jrel, yol, bolum, satir_bas, sutun, sira=None):
    """JSON karari ile foy tablo hucresini birlikte okur; ayni mi denetler."""
    j = O.jyukle(jrel)
    v = jget(j, yol)
    f = O.foy_tablo_hucresi(bolum, satir_bas, sutun, sira=sira)
    return {"karar_json": v, "json": f"{jrel} " + ".".join(str(p) for p in yol), "foy_bolum": bolum.lstrip("# "),
            "foy_satiri": f["foy_satiri"], "foy_sutun": sutun, "foy_hucre": f["deger"],
            "foy_satir_metni_sha256": f["satir_metni_sha256"], "json_ile_foy_ayni": str(v) == f["deger"]}


def main():
    # fonksiyon sinirlari (ayni ifadeler b2_karar ve b4_karar'da tekrarlandigi icin)
    b2a, b2b = O.bul(DB, "def b2_karar("), O.bul(DB, "def b2_coz(")
    b4a, b4b = O.bul(DB, "def b4_karar("), O.bul(DB, "def b4_cekirdek(")
    sba, sbb = O.bul(DB, "def sonuc_bolgesi("), b4a

    sabit = {
        "DELTA": esik("delta (birincil esdegerlik siniri, log birimi)", DB, "DELTA = ", r"DELTA = " + NUM, sira=0,
                      ok_rel=OK, ok_parca="Eşdeğerlik sınırı bütün log ölçekli niceliklerde"),
        "DELTA_DUY": esik("delta duyarliligi", DB, "DELTA_DUY = ", r"DELTA_DUY = " + NUM,
                          ok_rel=OK, ok_parca="Eşdeğerlik sınırı bütün log ölçekli niceliklerde"),
        "ALFA": esik("Holm alfa", DB, "ALFA = ", r"ALFA = " + NUM, ok_rel=OK, ok_parca="### B2 (üç tohum"),
        "B5_ESIK": esik("B5 korunma orani esigi", DB, "B5_ESIK = ", r"B5_ESIK = " + NUM,
                        ok_rel=OK, ok_parca="S_k(m) = ort_{c∈P} log T_k(m→c)"),
        "BOOT_TOHUM": esik("bootstrap tohumu", DB, "BOOT_TOHUM = ", r"BOOT_TOHUM = " + NUM),
        "BOOTSTRAP_B": esik("bootstrap kopya sayisi (varsayilan)", DB, 'ap.add_argument("--bootstrap"', r"default=" + NUM,
                            ok_rel=OK, ok_parca="K-c, tür içi benzerlik"),
        "S5_BANT": esik("S5 bandi (puan)", DB, "S5_EGIM, S5_KESISIM, S5_BANT = ", r"= [^,]+, [^,]+, " + NUM,
                        ok_rel=OK, ok_parca="- S5, protokol katmanının"),
        # 31.10.2026 bulgu 2: S5 ongoru dogrusunun sabitleri (ongoru = S5_EGIM * temiz fark + S5_KESISIM)
        "S5_EGIM": esik("S5 ongoru dogrusu egimi", DB, "S5_EGIM, S5_KESISIM, S5_BANT = ", r"= " + NUM,
                        ok_rel=OK, ok_parca="- S5, protokol katmanının"),
        "S5_KESISIM": esik("S5 ongoru dogrusu kesisimi (puan)", DB, "S5_EGIM, S5_KESISIM, S5_BANT = ", r"= [^,]+, " + NUM,
                           ok_rel=OK, ok_parca="- S5, protokol katmanının"),
        "B6_ESIK_PUAN": esik("B6 maskeleme esigi (PGD-10 - AA, puan)", MB, '"--esik", type=float, default=', r"default=" + NUM,
                             ok_rel=OK, ok_parca="AutoAttack n = 1000; PGD-10"),
        "B8_BEKLENTI_A_SIGMA_IN": esik("B8 IN satiri beklenti esigi", EB, "BEKLENTI_A_SIGMA_IN = ", r"= " + NUM,
                                       ok_rel=EK, ok_parca="Beklenti dondurulmuş öngörülerden türetilmiştir"),
        "B10_PERM": esik("B10 Mantel permutasyon sayisi", EB, "PERM_ON_KAYIT = ", r"= " + NUM,
                         ok_rel=EK, ok_parca="Anlamlılık Mantel permütasyon sınamasıyla verilir"),
        "B10_PERM_TOHUM": esik("B10 permutasyon tohumu", GB, "TOHUM = ", r"TOHUM = " + NUM,
                               ok_rel=EK, ok_parca="Anlamlılık Mantel permütasyon sınamasıyla verilir"),
    }
    delta_tanim = kural(DB, "def tost_p(est, se, df, delta=DELTA)")

    # 31.10.2026 bulgu 1: TOST ve S1 esdegerlik sinirlari acik alan olarak (deger DELTA satirindan, on kayit satirinda aranir)
    def tost_siniri(ad, ok_parca):
        e = esik(ad, DB, "DELTA = ", r"DELTA = " + NUM, sira=0, ok_rel=OK, ok_parca=ok_parca)
        e["tur"] = "TOST +-DELTA: iki tek yonlu sinama (H0: mu <= -DELTA ve H0: mu >= +DELTA); buyuk p Holm'a girer"
        e["alt_sinir"], e["ust_sinir"] = -e["deger"], e["deger"]
        e["tost_tanimi"] = delta_tanim["kaynak"]
        return e

    def s1_siniri():
        e = esik("S1 esdegerlik siniri +-DELTA", DB, "DELTA = ", r"DELTA = " + NUM, sira=0, ok_rel=OK, ok_parca="- S1, köprü")
        e["tur"] = ("ham %90 t araligi (-DELTA; DELTA) icinde (iki ucta kesin esitsizlik); TOST degil, kesifsel, Holm yok")
        e["alt_sinir"], e["ust_sinir"] = -e["deger"], e["deger"]
        e["icinde_tanimi"] = kural(DB, "def icinde(ci, a=-DELTA, b=DELTA):")["kaynak"]
        e["uygulama"] = kural(DB, 'ik["S1"] = {"sigma": a, "rho": b, "ongoru_ikisi_de_esdeger"')["kaynak"]
        return e

    sinamalar = []
    # ---------------- B2: F_B2 (CIFAR-10) ve B9: F_B9 (CIFAR-100), ayni dondurulmus kurallar ----------------
    def b2_kurallari(blok, aile, jrel, bolum, sutun, ok_ref):
        out = []
        out.append({
            "kimlik": "K-a", "blok": blok, "aile": aile, "baglayici": True,
            "nicelik": "q_s = [sigma(R_s) - sigma(V_s)] / D_s, tohum basina; ort q",
            "ongoru": "her tohumda q_s >= esik",
            "ongorulen_buyukluk": esik("K-a ongoru", DB, 'all(q >= 0.75 for q in ka["q"])', r"q >= " + NUM,
                                       ok_rel=OK, ok_parca="K-a, kaynak açığının simetrik oranı"),
            "sinama": {"tur": "tek yonlu t, df 2", "H0_esik": esik("K-a H0: ort q <= esik", DB, 'pa = float(1 - stats.t.cdf((kat["ort"] - 0.5)',
                                                                   r'\(kat\["ort"\] - ' + NUM, b2b, None,
                                                                   OK, "K-a, kaynak açığının simetrik oranı", sira=0)},
            "destek": {"kural": "Holm sonrasi p < ALFA", **kural(DB, "elif adj[0] < ALFA:", b2a, b2b)},
            "curutme": {"kural": "ort q %90 araligi ust siniri < esik",
                        "esik": esik("K-a curutme", DB, 'elif kat["ci90"][1] < 0.5:', r"< " + NUM, b2a, b2b,
                                     OK, "K-a, kaynak açığının simetrik oranı")},
            "payda_kurali": {"kural": "bir tohumda D_s <= DELTA ise kararsiz, Holm'da p = 1",
                             **kural(DB, 'ka["payda_kucuk_tohumlar"] = [i for i, D in enumerate(ka["D"]) if not (D > DELTA)]')},
            "karar_sirasi": "payda kurali > curutme > destek > kararsiz",
            "karar_sirasi_kaynagi": kural(DB, "def b2_karar(")["kaynak"] + "-" + str(b2b - 1),
            "on_kayit": ok_ref("K-a"),
            "gerceklesen": gercek(jrel, ("b2", "F_B2", "karar", "K-a"), bolum, "| K-a, ", sutun)})
        out.append({
            "kimlik": "K-b", "blok": blok, "aile": aile, "baglayici": True,
            "nicelik": "rho(V-scr), tohum ortalamasi",
            "ongoru": "esdeger, |rho| < DELTA",
            "esdegerlik_siniri": tost_siniri("K-b TOST siniri +-DELTA", "K-b, ViT'nin yönlü terimi"),
            "sinama": {"tur": "TOST +-DELTA (iki tek yonlu p'nin buyugu Holm'a girer)", **delta_tanim},
            "destek": {"kural": "Holm sonrasi TOST p < ALFA", **kural(DB, "if adj[1] < ALFA:", b2a, b2b)},
            "curutme": {"kural": "%95 aralik sifiri disliyor ve |ort| > DELTA (iki yonde)",
                        **kural(DB, 'cur = (kb["ci95"][0] > 0 or kb["ci95"][1] < 0) and abs(kb["ort"]) > delta', b2a, b2b)},
            "karar_sirasi": "destek > curutme > kararsiz",
            "on_kayit": ok_ref("K-b"),
            "gerceklesen": gercek(jrel, ("b2", "F_B2", "karar", "K-b"), bolum, "| K-b, ", sutun)})
        out.append({
            "kimlik": "K-c", "blok": blok, "aile": aile, "baglayici": True,
            "nicelik": "Delta_w = ort log tau(V_s, V_s') - ort_s sigma(V_s)",
            "ongoru": "Delta_w >= esik",
            "ongorulen_buyukluk": esik("K-c ongoru", DB, 'kc["ongoru_Delta_ge_0.30"] = kc["Delta_w"] >= 0.30', r">= " + NUM,
                                       ok_rel=OK, ok_parca="K-c, tür içi benzerlik"),
            "sinama": {"tur": "tek yonlu, H0: Delta_w <= 0; hiyerarsik bootstrap p = (1 + #{Delta* <= 0})/(B + 1)",
                       **kural(DB, "p_kc = float((1 + (dist <= 0).sum()) / (args.bootstrap + 1))")},
            "destek": {"kural": "curutme tutmuyorsa Holm sonrasi p < ALFA", **kural(DB, "elif adj[2] < ALFA:", b2a, b2b)},
            "curutme": {"kural": "%90 bootstrap araligi ust siniri < DELTA (once denetlenir)",
                        **kural(DB, 'if kc["bootstrap"]["ci90"][1] < delta:', b2a, b2b)},
            "karar_sirasi": "curutme > destek > kararsiz",
            "on_kayit": ok_ref("K-c"),
            "gerceklesen": gercek(jrel, ("b2", "F_B2", "karar", "K-c"), bolum, "| K-c, ", sutun)})
        return out

    def ok_b2(x):
        return okatir_b2[x]
    okatir_b2 = {"K-a": okatir(OK, "K-a, kaynak açığının simetrik oranı"),
                 "K-b": okatir(OK, "K-b, ViT'nin yönlü terimi"),
                 "K-c": okatir(OK, "K-c, tür içi benzerlik")}
    ek42 = okatir(EK, "K-a(B9), K-b(B9) ve K-c(B9), dondurulmuş K-a")

    def ok_b9(x):
        return {"ek_on_kayit": ek42, "dondurulmus_tanim": okatir_b2[x]}

    sinamalar += b2_kurallari("B2", "F_B2", J2, "### M9.5", "Karar", ok_b2)
    sinamalar += b2_kurallari("B9", "F_B9", J9, "### M10.2", "CIFAR-100 karar", ok_b9)

    # ---------------- B4: F_B4 ----------------
    sinamalar.append({
        "kimlik": "H1", "blok": "B4", "aile": "F_B4", "baglayici": True,
        "nicelik": "A^sigma_scr = sigma(V-scr) - sigma(R224-scr)",
        "ongoru": "A^sigma_scr <= esik",
        "ongorulen_buyukluk": esik("H1 ongoru", DB, 'out["H1_ongoru_buyuklugu_tuttu (A <= -0,20)"] = bool(h1["kestirim"] <= -0.20)',
                                   r"<= " + NUM + r"\)$", b4a, b4b, OK, "H1, girdi hattı eşitlenmişken"),
        "sinama": {"tur": "tek yonlu t, H0: A >= 0; birlesik varyans df 5", **kural(DB, "def b4_pler(")},
        "kurallar_sirasiyla": [
            {"i": "ham %90 aralik (-DELTA; DELTA) icinde -> curutuldu (esdeger)",
             **kural(DB, 'elif icinde(h1["ci90"], -delta, delta):', b4a, b4b)},
            {"ii": "Holm sonrasi p < ALFA -> destek", **kural(DB, "elif adj[0] < ALFA:", b4a, b4b)},
            {"iii": "kestirim > 0 ve %95 alt sinir > 0 -> curutuldu (ters yon)",
             **kural(DB, 'elif h1["kestirim"] > 0 and h1["ci95"][0] > 0:', b4a, b4b)},
            {"iv": "kalan -> kararsiz"}],
        "on_kayit": okatir(OK, "H1, girdi hattı eşitlenmişken"),
        "gerceklesen": gercek(J4, ("b4", "F_B4", "karar", "H1"), "### M9.3", "| H1, ", "Karar")})
    sinamalar.append({
        "kimlik": "H2", "blok": "B4", "aile": "F_B4", "baglayici": True,
        "nicelik": "I^sigma = [sigma(V-IN) - sigma(V-scr)] - [sigma(R224-IN) - sigma(R224-scr)]",
        "ongoru": "I^sigma >= esik",
        "ongorulen_buyukluk": esik("H2 ongoru", DB, 'out["H2_ongoru_buyuklugu_tuttu (I >= +0,10)"] = bool(h2["kestirim"] >= 0.10)',
                                   r">= " + NUM + r"\)$", b4a, b4b, OK, "H2, başlatma ile mimarinin"),
        "sinama": {"tur": "iki yonlu t, H0: I = 0; df 5",
                   # 31.10.2026 bulgu 8: iki yonlu p'nin hesaplandigi ve Holm'a girdigi betik satirlari
                   "p_iki": kural(DB, '"p_iki": float(2 * min(stats.t.cdf(t, df), 1 - stats.t.cdf(t, df)))})'),
                   "holm_girdisi": kural(DB, 'return [k["H1"].get("p_tek_kucuk", float("nan")), k["H2"].get("p_iki", float("nan")), p3]')},
        "kurallar_sirasiyla": [
            {"i": "ham %90 aralik (-DELTA; DELTA) icinde -> curutuldu (esdeger)",
             **kural(DB, 'elif icinde(h2["ci90"], -delta, delta):', b4a, b4b)},
            {"ii": "Holm sonrasi p < ALFA, kestirim > 0 ve logit kestirim > 0 -> destek",
             **kural(DB, 'elif adj[1] < ALFA and h2["kestirim"] > 0 and k_logit["H2"]["kestirim"] > 0:', b4a, b4b)},
            {"iii": "kestirim < 0 ve ham iki yonlu p < ALFA -> curutuldu (ters yon)",
             **kural(DB, 'elif h2["kestirim"] < 0 and h2.get("p_iki", 1) < ALFA:', b4a, b4b)},
            {"iv": "kalan -> kararsiz (logit isaret donusu dahil)",
             **kural(DB, 'out["H2"] = "kararsiz (logit olceginde isaret tersine donuyor)"', b4a, b4b)}],
        "on_kayit": okatir(OK, "H2, başlatma ile mimarinin"),
        "gerceklesen": gercek(J4, ("b4", "F_B4", "karar", "H2"), "### M9.3", "| H2, ", "Karar")})
    sinamalar.append({
        "kimlik": "H3", "blok": "B4", "aile": "F_B4", "baglayici": True,
        "nicelik": "A^rho = 1/2 {[rho(V-scr) - rho(R224-scr)] + [rho(V-IN) - rho(R224-IN)]}",
        "ongoru": "esdeger, |A^rho| < DELTA",
        "esdegerlik_siniri": tost_siniri("H3 TOST siniri +-DELTA", "H3, yönlü terimin mimariye ait olmaması"),
        "sinama": {"tur": "TOST +-DELTA", **delta_tanim},
        "destek": {"kural": "Holm sonrasi TOST p < ALFA", **kural(DB, "elif adj[2] < ALFA:", b4a, b4b)},
        "curutme": {"kural": "%95 aralik sifiri disliyor ve |kestirim| > DELTA",
                    **kural(DB, 'elif (h3["ci95"][0] > 0 or h3["ci95"][1] < 0) and abs(h3["kestirim"]) > delta:', b4a, b4b)},
        "karar_sirasi": "destek > curutme > kararsiz",
        "on_kayit": okatir(OK, "H3, yönlü terimin mimariye ait olmaması"),
        "gerceklesen": gercek(J4, ("b4", "F_B4", "karar", "H3"), "### M9.3", "| H3, ", "Karar")})

    # ---------------- B4 ikincil S1-S7 (kesifsel) ----------------
    s_satirlari = (("S1-sigma", "| S1, kopru sigma"), ("S1-rho", "| S1, kopru rho"), ("S2", "| S2, "),
                   ("S3-ViT", "| S3, omega baslatma etkisi ViT"), ("S3-ResNet", "| S3, omega baslatma etkisi ResNet"),
                   ("S3-etkilesim", "| S3, omega etkilesimi"), ("S5", "| S5, "), ("S6", "| S6, "), ("S7", "| S7, "))
    s_ok = {"S1": "- S1, köprü", "S2": "- S2, başlatmanın", "S3": "- S3, ω karşıtlıkları", "S4": "- S4, tohum indeksiyle",
            "S5": "- S5, protokol katmanının", "S6": "- S6, ikincil panel", "S7": "- S7, r matrisinde"}
    s_kod = {"S1": 'ik["S1"] = {"sigma": a, "rho": b, "ongoru_ikisi_de_esdeger"', "S2": 'ik["S2"]["ongoru_negatif"] = ',
             "S3": 'ik["S3"]["ongoru_omega_VIN_lt_Vscr"] = ', "S5": 's5o["ongoru_ort_sapma_bant_icinde"] = abs(s5o["ort"]) <= S5_BANT',
             "S6": 'ik["S6"] = {"panel": P2, "A_sigma_scr"', "S7": 'ik["S7"] = hodge_r('}
    # 31.10.2026 bulgu 2: S1-S7 ongoruleri (ON_KAYIT satir 78-84 tam alinti) ve bulgu 5: karsilastirilacak JSON anahtarlari
    _a1 = ok_alinti(OK, s_ok["S1"], r"(öngörü ikisi de ±0,10 içinde)")
    _a3 = ok_alinti(OK, s_ok["S3"], r"(öngörü ω\(V-IN\) < ω\(V-scr\))")
    s_ongoru = {
        "S1-sigma": ("sigma koprusu ve rho koprusu ikisi de esdeger: ham %90 araligi (-DELTA; DELTA) icinde", _a1),
        "S1-rho": ("sigma koprusu ve rho koprusu ikisi de esdeger: ham %90 araligi (-DELTA; DELTA) icinde", _a1),
        "S2": ("rho(V-IN) - rho(V-scr) < 0 (negatif)", ok_alinti(OK, s_ok["S2"], r"(öngörü negatif)")),
        "S3-ViT": ("omega(V-IN) < omega(V-scr), yani ViT baslatma etkisi < 0", _a3),
        "S3-ResNet": ("yok (betimsel; on kayitta S3 ongorusu yalniz ViT baslatma etkisi icindir)", _a3),
        "S3-etkilesim": ("yok (betimsel; on kayitta S3 ongorusu yalniz ViT baslatma etkisi icindir)", _a3),
        "S5": ("cift sapmalarinin ortalamasi +-S5_BANT puan icinde",
               ok_alinti(OK, s_ok["S5"], r"(Öngörü: ortalama sapma ±1,5 puan içinde)")),
        "S6": ("A^sigma_scr ve I^sigma'nin isareti ikincil panelde birincil panelle ayni",
               ok_alinti(OK, s_ok["S6"], r"(A\^σ_scr ve I\^σ.nın işareti birincil panelle aynı)")),
        "S7": ("yok (betimsel; on kayit satirinda ongoru ifadesi yok)", ok_alinti(OK, s_ok["S7"], r"^- (S7, .*)$")),
        "S4": ("yok (betimsel)", ok_alinti(OK, s_ok["S4"], r"(betimsel)")),
    }
    s_json = {"S1-sigma": [("S1", "ongoru_ikisi_de_esdeger")], "S1-rho": [("S1", "ongoru_ikisi_de_esdeger")],
              "S2": [("S2", "ongoru_negatif")], "S3-ViT": [("S3", "ongoru_omega_VIN_lt_Vscr")],
              "S5": [("S5", "ozet", "ongoru_ort_sapma_bant_icinde"), ("S5", "ozet", "curutme_ci90_bant_disinda")],
              "S6": [("S6", "isaret_ayni_A"), ("S6", "isaret_ayni_I")]}
    j4s = O.jyukle(J4)
    for kim, bas in s_satirlari:
        s = kim.split("-")[0]
        o = {"kimlik": kim, "blok": "B4 ikincil", "aile": "yok (kesifsel, coklu duzeltme yok)", "baglayici": False,
             "on_kayit": okatir(OK, s_ok[s]), "betik": kural(DB, s_kod[s]) if s in s_kod else None,
             "gerceklesen": {**{x: y for x, y in O.foy_tablo_hucresi("### M9.4", bas, "Ongoru").items()},
                             "foy_bolum": "M9.4", "kaynak_json": f"{J4} b4.ikincil.{s}"}}
        if s == "S5":
            o["curutme"] = kural(DB, 's5o["curutme_ci90_bant_disinda"] = ')
            o["bant"] = sabit["S5_BANT"]
            # 31.10.2026 bulgu 8 ve 2: curutme kurali metni (on kayit tam alinti) ve ongoru dogrusunun sabitleri
            o["curutme"]["kural"] = ("ortalama sapmanin %90 araligi [-S5_BANT; S5_BANT] bandinin tumuyle disinda -> "
                                     "mekanizma cumlesi daraltilir, manset etkilenmez")
            o["curutme"]["on_kayit"] = ok_alinti(OK, s_ok["S5"], r"(Çürütme: [^.]*\.)")
            o["ongoru_dogrusu"] = {"tanim": "ongorulen yayilim (puan) = S5_EGIM * temiz fark (puan) + S5_KESISIM; sapma = "
                                            "gozlenen - ongorulen; ongoru: cift sapmalarinin ortalamasi +-S5_BANT icinde",
                                   "egim": sabit["S5_EGIM"], "kesisim": sabit["S5_KESISIM"], "bant": sabit["S5_BANT"],
                                   "betik": kural(DB, "ong = S5_EGIM * temiz + S5_KESISIM"),
                                   "on_kayit": ok_alinti(OK, s_ok["S5"], r"(mevcut 60 noktalık ilişkinin \(eğim [^)]*\))")}
        if s == "S1":
            o["esdegerlik_siniri"] = s1_siniri()
        # 31.10.2026 bulgu 2: yapilandirilmis ongoru ve on kayit tam alintisi
        o["ongoru"], o["ongoru_on_kayit"] = s_ongoru[kim]
        o["ongoru_turu"] = "kesifsel; karar degil, coklu duzeltme yok"
        # 31.10.2026 bulgu 5: foy 'Ongoru' hucresindeki evet/hayir degerleri b4.ikincil mantiksal anahtarlariyla
        g = o["gerceklesen"]
        if kim in s_json:
            vals = [bool(jget(j4s, ("b4", "ikincil") + y)) for y in s_json[kim]]
            foy_b = [x == "evet" for x in re.findall(r":\s*(evet|hayir)\b", g["deger"])]
            g["karar_json"] = {".".join(y): v for y, v in zip(s_json[kim], vals)}
            g["json"] = f"{J4} " + "; ".join("b4.ikincil." + ".".join(y) for y in s_json[kim])
            g["foy_hucre"] = g["deger"]
            g["json_ile_foy_ayni"] = len(foy_b) == len(vals) and foy_b == vals
            g["karsilastirma_kurali"] = "foy hucresindeki 'etiket: evet|hayir' degerleri sirayla JSON mantiksal anahtarlariyla"
        else:
            g["json_ile_foy_karsilastirma"] = "yok: betimsel satir (foy hucresi 'betimsel'), JSON'da karar anahtari yok"
        sinamalar.append(o)
    sinamalar.append({"kimlik": "S4", "blok": "B4 ikincil", "aile": "yok (betimsel)", "baglayici": False,
                      "on_kayit": okatir(OK, s_ok["S4"]),
                      "ongoru": s_ongoru["S4"][0], "ongoru_on_kayit": s_ongoru["S4"][1], "ongoru_turu": "betimsel",
                      "gerceklesen": {**O.foy_satiri("### M9.4", "S4, tohum indeksiyle eslesmis ciftler"), "foy_bolum": "M9.4",
                                      "not": "betimsel tablo; karar yok",
                                      "json_ile_foy_karsilastirma": "yok: betimsel tablo, karar yok"}})

    # ---------------- B5 ----------------
    b5a = O.bul(DB, 'if not (Gp > DELTA):')
    sinamalar.append({
        "kimlik": "B5", "blok": "B5", "aile": "tek sinamali ayri aile (Holm yok)", "baglayici": True,
        "nicelik": "korunma orani G_best / G_PGD (C1-R32 ve V-scr; capraz uydurmali secim)",
        "ongoru": "oran >= B5_ESIK", "esik": sabit["B5_ESIK"],
        "kurallar_sirasiyla": [
            {"i": "G_PGD <= DELTA -> kararsiz (payda kucuk)", **kural(DB, "if not (Gp > DELTA):")},
            {"ii": "%90 bootstrap ust siniri < B5_ESIK -> curutuldu (manset PGD ailesiyle sinirlanir)",
             **kural(DB, 'elif o["bootstrap"]["ci90"][1] < B5_ESIK:', b5a, b5a + 6)},
            {"iii": "%90 bootstrap alt siniri >= B5_ESIK -> destek",
             **kural(DB, 'elif o["bootstrap"]["ci90"][0] >= B5_ESIK:', b5a, b5a + 6)},
            {"iv": "kalan -> kararsiz"}],
        "izinli_saldirilar": kural(DB, "B5_IZINLI = "),
        "on_kayit": okatir(OK, "S_k(m) = ort_{c∈P} log T_k(m→c)"),
        "gerceklesen": gercek(J5, ("b5", "birincil_C1-R32_V-scr", "karar"), "### M9.6", "| Karar |", "Deger")})

    # ---------------- B6 maskeleme kurali ----------------
    m6 = O.jyukle(M6)
    b6_satir = {m: O.foy_tablo_hucresi("### M9.7", f"| {m} |", "Isaretli") for m in m6["modeller"]}
    sinamalar.append({
        "kimlik": "B6", "blok": "B6", "aile": "karar kurali (sinama degil; B4 bolgesini duzenler)", "baglayici": True,
        "nicelik": "PGD-10 dogrulugu - AutoAttack dogrulugu (ilk 1000 test goruntusu, puan)",
        "kural": "fark > B6_ESIK_PUAN olan model isaretlenir; isaretli varsa H1-H3 isaretliler cikarilarak yeniden "
                 "hesaplanir, karar degisirse ilgili manset kararsiz sayilir",
        "esik": sabit["B6_ESIK_PUAN"], "betik": kural(MB, '"isaretli": bool(fark > a.esik)'),
        "b4_uygulamasi": kural(DB, 'isaretli = [m for m in (getattr(args, "maskeleme_isaretli", None) or []) if m in mevcut]'),
        "on_kayit": okatir(OK, "AutoAttack n = 1000; PGD-10"),
        "gerceklesen": {"isaretli_json": m6["isaretli"], "json": f"{M6} isaretli",
                        "foy_bolum": "M9.7", "foy_satirlari": {m: x["foy_satiri"] for m, x in b6_satir.items()},
                        "foy_hucreleri": {m: x["deger"] for m, x in b6_satir.items()},
                        "foy_satir_metni_sha256": {m: x["satir_metni_sha256"] for m, x in b6_satir.items()},
                        "json_ile_foy_ayni": all((m in m6["isaretli"]) == (x["deger"] == "evet") for m, x in b6_satir.items()),
                        "bolgeye_uygulama": {**O.foy_satiri("### M9.3", "B6 maskeleme kuralindan sonra uygulanan bolge"),
                                             "foy_bolum": "M9.3"}}})

    # ---------------- B8 (betimsel, aile yok) ----------------
    e8a, e8b = O.bul(EB, "def b8_etiket("), O.bul(EB, "def b8(a):")
    for kim, ana, sat, esk, okp in (
            ("B8-A_sigma_IN", "A_sigma_IN", "| A_sigma_IN (", sabit["B8_BEKLENTI_A_SIGMA_IN"],
             "Beklenti dondurulmuş öngörülerden türetilmiştir"),
            ("B8-A_sigma_scr_Liu", "A_sigma_scr_Liu", "| A_sigma_scr_Liu (",
             esik("B8 Liu satiri beklenti esigi", EB, '**ozetle(satirlar.get("scr", []), -0.20)}', r", " + NUM + r"\)\}",
                  ok_rel=EK, ok_parca="Liu çifti için aynı nicelik"), "Liu çifti için aynı nicelik")):
        sinamalar.append({
            "kimlik": kim, "blok": "B8", "aile": "yok (betimsel, kesifsel; Holm yok)", "baglayici": False,
            "nicelik": "A^sigma = sigma(donusturucu) - sigma(CNN), P8, bolunmus yari, log; goruntu bootstrap'i",
            "beklenti_esigi": esk,
            "etiketler_sirasiyla": [
                {"i": "%90 aralik (-DELTA; DELTA) icinde -> ihmal edilebilir", **kural(EB, "if ci90[0] > -delta and ci90[1] < delta:", e8a, e8b)},
                {"ii": "kestirim <= esik, ciftlerin hepsi negatif ve %90 ust sinir < 0 -> beklentiyle uyumlu",
                 **kural(EB, "if est <= esik and all(v < 0 for v in cift_degerleri) and ci90[1] < 0:", e8a, e8b)},
                {"iii": "kestirim > 0 ve %95 alt sinir > 0 -> ters yon", **kural(EB, "if est > 0 and ci95[0] > 0:", e8a, e8b)},
                {"iv": "kalan -> belirsiz"}],
            "on_kayit": okatir(EK, okp),
            "gerceklesen": gercek(J8, (ana, "betimsel_etiket"), "### M10.4", sat, "Betimsel etiket")})
    sinamalar.append({"kimlik": "B8-K-abc", "blok": "B8", "aile": "yok (dondurulmus betik ciktisi yalniz betimsel)",
                      "baglayici": False, "on_kayit": okatir(EK, "Bu çıktıdaki F_B2 p değerleri, Holm sonuçları ve karar etiketleri"),
                      "gerceklesen": {**O.foy_satiri("### M10.4", "Dondurulmus betigin B8 ciktisi"), "foy_bolum": "M10.4",
                                      "not": "etiketler B8'de karar degildir",
                                      "json_ile_foy_karsilastirma": "yok: dondurulmus betik ciktisi B8'de karar degildir"}})

    # ---------------- B10: F_B10, alti sinama ----------------
    j10 = O.jyukle(J10)
    ham_ong = esik("H10 ongorulen buyukluk", EB, '("ham", "H10", 0.50)', r'"H10", ' + NUM,
                   ok_rel=EK, ok_parca="Ham sınama H10-d için öngörü")
    kis_ong = esik("H10k ongorulen buyukluk", EB, '("ana_etki_artik", "H10k", 0.30)', r'"H10k", ' + NUM,
                   ok_rel=EK, ok_parca="Ham sınama H10-d için öngörü")
    cur10 = esik("B10 curutme: kestirim esigi (kestirim <= esik)", EB, "elif r <= 0.20 and p >= 0.20:", r"r <= " + NUM,
                 ok_rel=EK, ok_parca="Ham sınama H10-d için öngörü")
    cur10p = esik("B10 curutme: ham Mantel p esigi (p >= esik)", EB, "elif r <= 0.20 and p >= 0.20:", r"p >= " + NUM,
                  ok_rel=EK, ok_parca="Ham sınama H10-d için öngörü")
    for i, x in enumerate(j10["F_B10"]["sinamalar"]):
        ad = x["sinama"]
        sinamalar.append({
            "kimlik": ad, "blok": "B10", "aile": "F_B10", "baglayici": True,
            "nicelik": ("Spearman(c_ij, log tau_ij), Mantel" if ad.startswith("H10-") else
                        "Spearman(c artigi, log tau artigi), model ana etkileri cikarilmis, Mantel"),
            "ongoru": "Spearman > 0", "ongorulen_buyukluk": ham_ong if ad.startswith("H10-") else kis_ong,
            "kurallar_sirasiyla": [
                {"i": "kestirim <= esik ve ham Mantel p >= p esigi -> curutuldu", "esik": cur10, "p_esigi": cur10p},
                {"ii": "Holm sonrasi p < ALFA -> destek", **kural(EB, "elif ph < dm.ALFA:")},
                {"iii": "kalan -> kararsiz"}],
            "on_kayit": okatir(EK, "Ham sınama H10-d için öngörü"),
            "gerceklesen": gercek(J10, ("F_B10", "sinamalar", i, "karar"), "### M10.5", f"| {ad} |", "Karar")})

    # ---------------- aileler ----------------
    j2, j4, j9 = O.jyukle(J2), O.jyukle(J4), O.jyukle(J9)
    aileler = {
        "F_B2": {"blok": "B2", "veri": "CIFAR-10", "sinamalar": ["K-a", "K-b", "K-c"], "holm": True,
                 "aile_buyuklugu_json": len(j2["b2"]["F_B2"]["p_holm"]), "json": f"{J2} b2.F_B2.p_holm",
                 "on_kayit": okatir(OK, "### B2 (üç tohum")},
        "F_B4": {"blok": "B4", "veri": "CIFAR-10", "sinamalar": ["H1", "H2", "H3"], "holm": True,
                 "aile_buyuklugu_json": len(j4["b4"]["F_B4"]["p_holm"]), "json": f"{J4} b4.F_B4.p_holm",
                 "on_kayit": okatir(OK, "### B4 (2x2; birincil aile F_B4")},
        "F_B9": {"blok": "B9", "veri": "CIFAR-100", "sinamalar": ["K-a", "K-b", "K-c"], "holm": True,
                 "aile_buyuklugu_json": len(j9["b2"]["F_B2"]["p_holm"]), "json": f"{J9} b2.F_B2.p_holm",
                 "on_kayit": okatir(EK, "### 4.2 Öngörüler, sınamalar ve karar")},
        "F_B10": {"blok": "B10", "veri": "CIFAR-10, CIFAR-100, ImageNetV2", "sinamalar": [x["sinama"] for x in j10["F_B10"]["sinamalar"]],
                  "holm": True, "aile_buyuklugu_json": j10["F_B10"]["aile_buyuklugu"], "json": f"{J10} F_B10.aile_buyuklugu",
                  "on_kayit": okatir(EK, "Aile F_B10 altı sınamadır")},
        "B5": {"blok": "B5", "holm": False, "not": "tek sinamali ayri aile", "on_kayit": okatir(OK, "B5 tek sınamalı ayrı bir ailedir")},
        "B8": {"blok": "B8", "holm": False, "not": "karar ailesi yok, betimsel", "on_kayit": okatir(EK, "B8'de Holm'lu bir karar ailesi yoktur")},
        "S1-S7": {"blok": "B4 ikincil", "holm": False, "not": "kesifsel, coklu duzeltme yok",
                  "on_kayit": okatir(OK, "İkincil çözümlemeler (keşifsel olarak etiketlenir")},
    }
    karar_ilkesi = {"birincil": okatir(OK, "Karar ilkesi (bütün birincil sınamalar için)"),
                    "ek": okatir(EK, "δ = 0,10, duyarlılık δ = 0,06, α = 0,05, karar ilkesi"),
                    "hesaplanamayan_p_1": kural(DB, "def holm_aile(")}
    bolge = {"sira": kural(DB, '"kural": "sira: O2 > O5 > O1 > O3 > O3-varyant > O5a; O4 ek niteleme"}', sba, sbb),
             "on_kayit_tablosu": okatir(OK, "| Bölge | Koşul | Manşet |"),
             "on_kayit_sira": okatir(OK, "Bölgeler şu sırayla denetlenir"),
             "gerceklesen": {"bolge_json": j4["b4"]["F_B4"]["karar"]["sonuc_bolgesi"],
                             "O4_niteleme_json": j4["b4"]["F_B4"]["karar"]["O4_niteleme"],
                             "json": f"{J4} b4.F_B4.karar.sonuc_bolgesi, .O4_niteleme",
                             **O.foy_satiri("### M9.3", "Sonuc bolgesi: "), "foy_bolum": "M9.3"}}
    bolge["gerceklesen"]["foy_satirinda_bolge_var"] = f"**{bolge['gerceklesen']['bolge_json']}**" in \
        O.satirlar(O.FOY)[bolge["gerceklesen"]["foy_satiri"] - 1]
    den = {"json_ile_foy_ayni_hepsi": all(s["gerceklesen"].get("json_ile_foy_ayni", True) for s in sinamalar),
           "json_ile_foy_ayni_olmayan": [s["kimlik"] + "/" + s["blok"] for s in sinamalar
                                         if s["gerceklesen"].get("json_ile_foy_ayni") is False],
           "sinama_sayisi": len(sinamalar),
           "dondurulmus_betik_sha256": O.sha(DB), "ek_ayrisim_sha256": O.sha(EB),
           "dondurulmus_betik_on_kayitla_ayni": O.sha(DB) in "\n".join(O.satirlar(OK)),
           "foy_sha256": O.sha(O.FOY)}
    # 31.10.2026 duzeltme turu: denetim alanlari (yalniz ekleme)
    kars = [s for s in sinamalar if "json_ile_foy_ayni" in s["gerceklesen"]]
    den["json_ile_foy_karsilastirilan_sayisi"] = len(kars)
    den["json_ile_foy_ayni_sayisi"] = sum(1 for s in kars if s["gerceklesen"]["json_ile_foy_ayni"])
    den["json_ile_foy_karsilastirilmayan"] = [
        {"kimlik": s["kimlik"], "blok": s["blok"],
         "neden": s["gerceklesen"].get("json_ile_foy_karsilastirma") or s["gerceklesen"].get("not", "-")}
        for s in sinamalar if "json_ile_foy_ayni" not in s["gerceklesen"]]
    den["json_ile_foy_ozet"] = (f"{den['json_ile_foy_ayni_sayisi']}/{len(kars)} karsilastirilan sinamada JSON karari foy "
                                f"hucresiyle ayni; {len(sinamalar)} sinamanin {len(sinamalar) - len(kars)} tanesi "
                                f"karsilastirilmadi (betimsel ya da karar degil)")
    den["foy_sha256_tanimi"] = O.FOY_OZETI_TANIMI

    def _say(o):
        if isinstance(o, dict):
            return ("on_kayit_eslesmeleri" in o) + sum(_say(v) for v in o.values())
        if isinstance(o, list):
            return sum(_say(v) for v in o)
        return 0
    den["on_kayit_deger_aramasi"] = {"kural": O.ON_KAYIT_ARAMA_KURALI,
                                     "denetlenen_deger_sayisi": _say(sabit) + _say(sinamalar)}
    govde = {"sabitler": sabit, "delta_tost_tanimi": delta_tanim, "karar_ilkesi": karar_ilkesi, "aileler": aileler,
             "sinamalar": sinamalar, "sonuc_bolgesi": bolge, "denetimler": den}
    O.yaz(CIKTI, govde, __file__, "Y4 fig:registry_map kaynagi: on kayitli sinamalarin kayit haritasi",
          "Her sinama icin ongoru, esikler (dondurulmus betik satirindan), Holm ailesi, delta, karar kurali ve gerceklesen "
          "karar (sonuc JSON'u ve foy tablo hucresi; sonuc sayilari kopyalanmaz, foy satiri verilir).")


def okatir(rel, parca):
    """On kayit metninde `parca`nin gectigi tekil satir."""
    n = O.bul(rel, parca)
    return {"kaynak": f"{rel}:{n}", "metin_basi": O.satirlar(rel)[n - 1].strip()[:200]}


if __name__ == "__main__":
    main()
