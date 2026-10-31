# -*- coding: utf-8 -*-
"""ONKAYIT_SAPMALAR.md sonuna 31.10.2026 masa cozumlemesi notlarini ekler (yalniz sona ekleme).

Sayilar elle yazilmaz: hepsi results/q1/konsey_ek_masa/*.json dosyalarindan okunur ve bicimlenir.
Asamalar: bootstrap (hiyerarsik bootstrap notu, sonuclarla), s103_on (S10-3 kod ve belirtim kaydi, koşudan once),
s103_sonuc (S10-3 kosusundan sonra sonuc paragrafi). Kullanim: python3 _masa_sapma_notu.py <asama>
"""
import hashlib
import io
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(__file__).resolve().parents[2]
SP = KOK / "results/q1_research/ONKAYIT_SAPMALAR.md"
BETIK = "experiments/q1_ek_masa.py"
D = "results/q1/konsey_ek_masa"
B_BASLIK = "### 31.10.2026, ana ön kayıt §7: hiyerarşik bootstrap duyarlılığı sonradan üretildi"
S_BASLIK = "### 31.10.2026, ek ön kayıt §12: S10-3 sonradan üretildi"
AD10, AD100 = "CIFAR-10'da", "CIFAR-100'de"


def sha(rel):
    return hashlib.sha256((KOK / rel).read_bytes()).hexdigest()


def oku(rel):
    return json.loads((KOK / rel).read_text(encoding="utf-8"))


def tr(x, nd=3):
    s = f"{float(x):.{nd}f}".replace(".", ",")
    return s.replace("-", "−")


def ar(a, nd=3):
    return f"{tr(a[0], nd)} ile {tr(a[1], nd)}"


def pe(x):
    if float(x) == 0.0:
        return "0"
    m, e = f"{float(x):.1e}".split("e")
    ust = str(int(e)).translate(str.maketrans("-0123456789", "\u207b\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079"))
    return f"{m.replace('.', ',')}×10{ust}"


def kp(a, nd=3):
    return f"[{tr(a[0], nd)}; {tr(a[1], nd)}]"


def ekle(metin, baslik):
    eski = SP.read_text(encoding="utf-8")
    if baslik and baslik in eski:
        raise SystemExit(f"baslik zaten var: {baslik}")
    if not eski.endswith("\n"):
        raise SystemExit("dosya satir sonuyla bitmiyor")
    with io.open(SP, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(metin)
    print(metin)


def bootstrap():
    J = {v: oku(f"{D}/bootstrap_{v}.json") for v in ("cifar10", "cifar100")}
    s_ = {J[v]["meta"]["betik_sha256"] for v in J}
    if len(s_) != 1 or s_ != {sha(BETIK)}:
        raise SystemExit(f"betik ozeti JSON'lardakiyle ayni degil: {s_} / {sha(BETIK)}")
    h = s_.pop()
    j10, j100 = J["cifar10"], J["cifar100"]
    tohum = j10["meta"]["bootstrap_tohum"]
    B = j10["meta"]["B"]
    nf = max(max(J[v]["dogrulama"]["nokta_kestirimleri_dondurulmus_json_ile_maks_fark"].values()) for v in J)
    kcf = max(max(abs(x) for x in J[v]["dogrulama"]["K-c_yeniden_uretim_maks_fark"].values()) for v in J)

    def blok(v, ad):
        j = J[v]
        ka, kb = j["K-a"], j["K-b"]
        k = j["karar"]["karsilastirma"]
        return (f"{ad} ({j['meta']['blok']}) ortalama q'nun hiyerarşik bootstrap aralıkları %90 {kp(ka['bootstrap']['ci90'])} "
                f"ve %95 {kp(ka['bootstrap']['ci95'])} olarak bulunmuştur (birincil t aralıkları %90 {kp(ka['t_ci90'])}, %95 "
                f"{kp(ka['t_ci95'])}); ortalama ρ(V-scr) için bootstrap aralıkları %90 {kp(kb['bootstrap']['ci90'])} ve %95 "
                f"{kp(kb['bootstrap']['ci95'])}, birincil t aralıkları %90 {kp(kb['t_ci90'])} ve %95 {kp(kb['t_ci95'])}, "
                f"bootstrap TOST p'si {pe(kb['bootstrap']['tost_p'])}, t TOST p'si ise {pe(kb['t_tost_p'])} olarak bulunmuştur "
                f"(`{D}/bootstrap_{v}.json`, `K-a.bootstrap`, `K-a.t_ci90`, `K-b.bootstrap`, `K-b.t_ci90`, `K-b.t_tost_p`). "
                f"Dondurulmuş karar kuralları bootstrap aralıkları ve p'leriyle yeniden uygulandığında K-a kararı "
                f"`{k['K-a']['dondurulmus']}` iken `{k['K-a']['bootstrap_araligiyla']}`, K-b kararı `{k['K-b']['dondurulmus']}` "
                f"iken `{k['K-b']['bootstrap_araligiyla']}` olmaktadır (`karar.karsilastirma`; değişen sınama listesi "
                f"`karar.degisen` = {j['karar']['degisen'] or 'boş'}, δ = 0,06 duyarlılığında `karar.delta_0.06.degisen` = "
                f"{j['karar']['delta_0.06']['degisen'] or 'boş'}).")

    degisen = sorted({s for v in J for s in J[v]["karar"]["degisen"] + J[v]["karar"]["delta_0.06"]["degisen"]})
    metin = (
        f"\n{B_BASLIK}\n\n"
        "Ana ön kaydın (ÖK) §5 duyarlılık listesinde yer alan hiyerarşik bootstrap (hücre içinde koşular, görüntüler ortak, "
        f"B = {B}) K-a ve K-b için B2'de (CIFAR-10) ve B9'da (CIFAR-100) 31.10.2026'da, hakem paneli raporlarından "
        "(`raporlar/hakem_konsey_2026-10-31/birlesik.md`, `mercek_istatistik.md`) sonra üretilmiştir. Dondurulmuş betik bu "
        "duyarlılığı B2'de yalnız K-c'nin birincil aralığı olarak üretmiş, K-a ve K-b için kod içermemişti; eksiklik bu "
        "dosyanın \"31.10.2026, ana ön kayıt §7 kayıtları\" başlığının 3. maddesinde uyumsuzluk notu olarak yazılmıştı. "
        "B9 dondurulmuş betikle aynı çağrıyla koşulduğundan aynı eksiklik orada da bulunmaktaydı.\n\n"
        "Kayıt ÖK §7'ye göre uygulama düzeyinde bir sapma olarak sınıflanmıştır. Hesap dondurulmuş betikle değil, onun "
        f"işlevlerini SHA-256 denetimiyle ve değiştirmeden yükleyen yeni bir betikle (`{BETIK}`, SHA-256 `{h}`, "
        "`--mod bootstrap`) ve B2 ile B9 sonuçları görüldükten sonra yapılmıştır. ÖK tanımı üç ayrıntıyı açık bırakmaktadır "
        "ve bunlar sonuçlar bilinirken belirlenmiştir: K-a'da iki hücrenin koşuları birbirinden bağımsız biçimde hücre "
        "içinde çekilmiş ve k'inci çekimler eşlenmiştir, koşu çiftlerini birim alan çekim ise ayrı bir duyarlılık olarak "
        f"verilmiştir (`cift_duzeyi_varyant`); ÖK bootstrap tohumu belirtmediğinden dondurulmuş betiğin BOOT_TOHUM sabiti "
        f"({tohum}) kullanılmış, K-c bu tohumla dondurulmuş RNG akışı izlenerek yeniden üretilmiş ve K-a ile K-b'nin koşu "
        "çekimleri aynı akıştan devam etmiştir; karar karşılaştırması için K-a'da (1 + #{ort q* ≤ 0,50})/(B + 1), K-b'de "
        "iki tek yönlü bootstrap p'sinin büyüğü tanımlanmıştır. Tam tanım JSON'ların `tanim` alanındadır. ÖK §5'e göre "
        "duyarlılıklar karar değiştirmez; aşağıdaki karşılaştırma yalnız raporlama içindir.\n\n"
        "Nokta kestirimleri dondurulmuş çıktılarla (`results/q1/konsey_ayrisim_b2.json`, "
        "`results/q1/konsey_b9_c100/b9_dondurulmus_b2.json`) aynıdır; en büyük mutlak fark "
        f"{pe(nf)} olarak hesaplanmıştır (`dogrulama.nokta_kestirimleri_dondurulmus_json_ile_maks_fark`). K-c'nin aralıkları, p'si ve yeniden "
        f"çekim sayısı iki veri kümesinde de dondurulmuş değerlerle birebir yeniden üretilmiştir (en büyük fark {pe(kcf)}; "
        f"`dogrulama.K-c_esit`). {blok('cifar10', AD10)} {blok('cifar100', AD100)} "
        + ("Böylece iki veri kümesinde de K-a, K-b ve K-c kararlarından hiçbiri bootstrap aralığıyla değişmemektedir. "
           if not degisen else f"Bootstrap aralığıyla değişen kararlar: {degisen}. ")
        + "Sayılar föyün M11.1 alt bölümüne betikle taşınmıştır.\n")
    ekle(metin, B_BASLIK)


def s103_on():
    h = sha(BETIK)
    J = oku(f"{D}/bootstrap_cifar10.json")
    if J["meta"]["betik_sha256"] != h:
        raise SystemExit("betik bootstrap kosusundan sonra degismis")
    metin = (
        f"\n{S_BASLIK}\n\n"
        "Ek ön kaydın (EK) §6.4'ündeki S10-3, yani aynı aileden olma göstergesini (CNN-CNN, dönüştürücü-dönüştürücü, karma) "
        "ek ortak değişken alan kısmi Mantel, dondurma anında kodsuzdu; EK §6.4 kod yazılırsa özetinin ilk koşudan önce "
        "kod eki olarak bu dosyaya yazılmasını ister. Kod 31.10.2026'da hakem paneli isteği üzerine "
        f"`{BETIK}` içinde `--mod mantel_aile` olarak yazılmış ve yalnız yapay matrislerle sınanmıştır "
        "(`arsiv/b2_yardimci/_masa_sinama_null.py`, `arsiv/b2_yardimci/_masa_sinama/`). Aşağıdaki özet gerçek veriyle ilk "
        "S10-3 koşusundan önce hesaplanmıştır; aynı dosyanın `--mod bootstrap` kipi bu özetle daha önce koşulmuştur.\n\n"
        f"```text\n{h}  {BETIK}\n```\n\n"
        "Belirtim şöyledir. Sırasız model çiftlerinde c ve log τ̄ matrislerinin her biri X_ij = μ + a_i + a_j + β_CC·CC_ij + "
        "β_TT·TT_ij + e_ij modeliyle değer ölçeğinde en küçük kareler ile kestirilir; karma çiftler referanstır, aile hücre "
        "tablolarındaki `aile` alanından alınır (CNN ayrı, ViT, XCiT ve Swin dönüştürücü). İstatistik iki artık vektörü "
        "arasındaki Spearman korelasyonudur. Permütasyon EK §6.2'nin kısmi istatistik kuralıyla aynıdır: c artık matrisinin "
        "satır ve sütunları ortak permüte edilir, log τ̄ artığı sabit tutulur; 9999 permütasyon, tohum 20261030, tek yönlü "
        "p = (1 + #{r* ≥ r})/(perm + 1). Duyarlılık olarak ham c matrisi permüte edilip sabit tasarıma göre yeniden "
        "artıklanır. Aynı koşu EK §6.2'nin ham ve ana etki artıklı istatistiklerini bağımsız kodla yeniden üretir ve "
        "`results/q1/konsey_b10_gradyan/mantel_<veri>.json` ile 1e-6 içinde karşılaştırır.\n\n"
        "Kayıt EK §12'ye göre kod eki niteliğinde olduğundan sapma sayılmaz, ancak beyan gerektirir. EK §6.4'teki tanım tek "
        "cümledir; tahmin denkleminin biçimi, permütasyon şeması ve aile gruplaması bu kayıtta, B10 sonuçları ve S10-3'e "
        "yakın bir hesabın nokta kestirimleri (`raporlar/konsey_2026-10-29/11_sonuc_b8_b10.md` §7, sıra ölçeğinde aile "
        "ayıklamalı artık Spearman) görüldükten sonra belirlenmiştir. Bu yüzden S10-3 önceden belirtilmiş bir sınama "
        "sayılmaz; EK §6.4'teki keşifsel statüsü değişmez, F_B10 ailesine girmez ve Holm hesabına katılmaz.\n")
    ekle(metin, S_BASLIK)


def s103_sonuc():
    M = oku(f"{D}/mantel_aile.json")
    K = oku(f"{D}/kesifsel.json")
    eski = SP.read_text(encoding="utf-8")
    i = eski.find(S_BASLIK)
    if i < 0 or "```text\n" + M["meta"]["betik_sha256"] + "  " + BETIK not in eski[i:]:
        raise SystemExit("S10-3 kaydi yok ya da kayitli ozet kosudaki betik ozetiyle ayni degil")
    if M["meta"]["uretildi_utc"] < "2026-10-31":
        raise SystemExit("tarih")
    ad = {"cifar10": "CIFAR-10'da", "cifar100": "CIFAR-100'de", "imagenetv2": "ImageNetV2'de"}
    parca = []
    for v in ("cifar10", "cifar100", "imagenetv2"):
        d = M["veri"][v]
        parca.append(f"{ad[v]} {tr(d['S10_3']['istatistik'])} (tek yönlü p {pe(d['S10_3']['p_tek'])}; ham c "
                     f"permütasyonlu duyarlılıkta p {pe(d['S10_3_duyarlilik_ham_c_permutasyonu']['p_tek'])})")
    mf = max(c["maks_fark"] for d in M["veri"].values() for c in d["mantel_json_karsilastirma"].values())
    metin = (
        "\n"
        f"Koşu {M['meta']['uretildi_utc'][:10]} tarihinde kayıtlı özetle yapılmıştır (`{D}/mantel_aile.json`, "
        f"`meta.betik_sha256`). EK §6.2'nin ham ve ana etki artıklı istatistikleri ve p'leri üç veri kümesinde 1e-6 içinde "
        f"yeniden üretilmiştir (en büyük mutlak fark {pe(mf)}; `yeniden_uretim_hepsi_esit_1e-6` = "
        f"{str(M['yeniden_uretim_hepsi_esit_1e-6']).lower()}). S10-3 istatistiği " + ", ".join(parca)
        + f" olarak bulunmuştur (`veri.<veri>.S10_3`, `S10_3_duyarlilik_ham_c_permutasyonu`; {M['meta']['perm']} permütasyon). S10-3 "
        "F_B10 ailesinde olmadığından ailenin kararlarını değiştirmez. Aynı gün üretilen keşifsel çözümlemeler "
        f"(aile içi kısıtlı permütasyon, sıra ölçeğinde aile ayıklamalı artık Spearman, yalnız CNN-CNN çiftleri, R18-R50 "
        f"çifti) `{D}/kesifsel.json` dosyasındadır (betik özeti aynı: "
        f"{'evet' if K['meta']['betik_sha256'] == M['meta']['betik_sha256'] else 'HAYIR'}) ve ön kayıt dışıdır. Sayılar "
        "föyün M11.2 ve M11.3 alt bölümlerine betikle taşınmıştır.\n")
    ekle(metin, None)


if __name__ == "__main__":
    {"bootstrap": bootstrap, "s103_on": s103_on, "s103_sonuc": s103_sonuc}[sys.argv[1]]()
