#!/usr/bin/env python3
"""B2 metin -- 4/n: ozet, giris, ilgili calismalar, tartisma, sonuc ve
CIFAR-100 ON-KESTIRIM paragrafi. Iki dil."""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
hata, yazilan = [], []


def yama(rel, ciftler):
    p = ROOT / rel
    t = orig = p.read_text(encoding="utf-8")
    for eski, yeni, ad in ciftler:
        if eski not in t and yeni in t:
            continue
        n = t.count(eski)
        if n != 1:
            hata.append(f"{rel} :: {ad}: {n} eslesme")
            return
        t = t.replace(eski, yeni, 1)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        yazilan.append(rel)


# ------------------------------------------------------------------ EN ozet
yama("paper/manuscript/main.tex", [
    ("transfer asymmetry ranges from 4.4 to 14.6 points on CIFAR-10",
     "transfer asymmetry ranges from 4.4 to 19.4 points on CIFAR-10", "EN ozet aralik"),
    ("Replicating the design on CIFAR-100 widens the spread and preserves the sign "
     "in all twelve measurements.",
     "Replicating the design on CIFAR-100 leaves the spread in the same range and "
     "preserves the sign in all twelve measurements.", "EN ozet C100"),
])

# ----------------------------------------------------------------- TR ozet
yama("paper/manuscript_tr/main.tex", [
    ("CIFAR-10'da $4{,}4$ ile $14{,}6$ puan arasında değişmekte",
     "CIFAR-10'da $4{,}4$ ile $19{,}4$ puan arasında değişmekte", "TR ozet aralik"),
    ("Aynı tasarımın CIFAR-100'de yinelenmesi yayılımı genişletmekte ve on iki "
     "ölçümün tamamında işareti korumaktadır",
     "Aynı tasarımın CIFAR-100'de yinelenmesi yayılımı aynı aralıkta bırakmakta ve "
     "on iki ölçümün tamamında işareti korumaktadır", "TR ozet C100"),
])

# ----------------------------------------------------------------- EN giris
yama("paper/manuscript/sections/01_introduction.tex", [
    ("ranges from $+4.4$ to $+14.6$ points across four established conditioning "
     "protocols, a 3.3-fold spread",
     "ranges from $+4.4$ to $+19.4$ points across four established conditioning "
     "protocols, a 4.4-fold spread", "EN giris aralik"),
    ("Repeating the full design on CIFAR-100 widens the mean per-seed protocol "
     "spread to $13.58\\pm1.71$ points and preserves the sign in all twelve "
     "measurements.",
     "Repeating the full design on CIFAR-100 leaves the mean per-seed protocol "
     "spread at $13.83\\pm1.30$ points, close to the CIFAR-10 value, and preserves "
     "the sign in all twelve measurements.", "EN giris C100"),
])

# ----------------------------------------------------------------- TR giris
yama("paper/manuscript_tr/sections/01_giris.tex", [
    ("$+4{,}4$ ile $+14{,}6$ puan arasında değişmektedir; bu 3,3 katlık bir "
     "yayılımdır",
     "$+4{,}4$ ile $+19{,}4$ puan arasında değişmektedir; bu 4,4 katlık bir "
     "yayılımdır", "TR giris aralik"),
    ("Tasarımın tamamı CIFAR-100 üzerinde tekrarlandığında tohum başına ortalama "
     "protokol yayılımı $13{,}58\\pm1{,}71$ puana çıkmakta ve işaret on iki ölçümün "
     "tamamında korunmaktadır.",
     "Tasarımın tamamı CIFAR-100 üzerinde tekrarlandığında tohum başına ortalama "
     "protokol yayılımı $13{,}83\\pm1{,}30$ puan olmakta, yani CIFAR-10 değerine "
     "yakın kalmakta ve işaret on iki ölçümün tamamında korunmaktadır.",
     "TR giris C100"),
])

# ------------------------------------------------------- EN ilgili calismalar
yama("paper/manuscript/sections/02_related_work.tex", [
    ("the measured asymmetry moves by $10.45\\pm0.76$ points across the four "
     "protocols, a 3.3-fold spread",
     "the measured asymmetry moves by $15.01\\pm0.84$ points across the four "
     "protocols, a 4.4-fold spread", "EN rw"),
])
yama("paper/manuscript_tr/sections/02_ilgili_calismalar.tex", [
    ("ölçülen asimetrinin dört protokol boyunca $10{,}45\\pm0{,}76$ puan oynadığını "
     "buluyoruz; bu, 3,3 katlık bir yayılımdır.",
     "ölçülen asimetrinin dört protokol boyunca $15{,}01\\pm0{,}84$ puan oynadığını "
     "buluyoruz; bu, 4,4 katlık bir yayılımdır.", "TR rw"),
])

# --------------------------------------------------------------- EN tartisma
yama("paper/manuscript/sections/05_discussion.tex", [
    ("whereas changing only the conditioning protocol moves it by $10.45\\pm0.76$ "
     "points",
     "whereas changing only the conditioning protocol moves it by $15.01\\pm0.84$ "
     "points", "EN disc yayilim"),
    ("A quantity that the measurement choice moves by ten points while retraining "
     "moves it by one",
     "A quantity that the measurement choice moves by fifteen points while "
     "retraining moves it by one", "EN disc olcek"),
    ("On CIFAR-100 the spread is larger than on CIFAR-10 ($13.58\\pm1.71$ against "
     "$10.45\\pm0.76$ points) and the sign is preserved in all twelve measurements",
     "On CIFAR-100 the spread is close to the CIFAR-10 value ($13.83\\pm1.30$ "
     "against $15.01\\pm0.84$ points) and the sign is preserved in all twelve "
     "measurements", "EN disc C100"),
])
yama("paper/manuscript_tr/sections/05_tartisma.tex", [
    ("yalnızca koşullama protokolünü değiştirmek $10{,}45\\pm0{,}76$ puan "
     "oynatmaktadır",
     "yalnızca koşullama protokolünü değiştirmek $15{,}01\\pm0{,}84$ puan "
     "oynatmaktadır", "TR disc yayilim"),
    ("Ölçüm seçiminin on puan oynattığı, yeniden eğitmenin ise bir puan oynattığı",
     "Ölçüm seçiminin on beş puan oynattığı, yeniden eğitmenin ise bir puan "
     "oynattığı", "TR disc olcek"),
    ("CIFAR-100'de yayılım CIFAR-10'dakinden büyüktür ($13{,}58\\pm1{,}71$'e karşı "
     "$10{,}45\\pm0{,}76$ puan) ve işaret on iki ölçümün tamamında korunmaktadır",
     "CIFAR-100'de yayılım CIFAR-10 değerine yakındır ($13{,}83\\pm1{,}30$'a karşı "
     "$15{,}01\\pm0{,}84$ puan) ve işaret on iki ölçümün tamamında korunmaktadır",
     "TR disc C100"),
])

# ------------------------------------------------------------------ EN sonuc
yama("paper/manuscript/sections/06_conclusion.tex", [
    ("ranges from $+4.4$ to $+14.6$ points across four established conditioning "
     "protocols, a 3.3-fold spread",
     "ranges from $+4.4$ to $+19.4$ points across four established conditioning "
     "protocols, a 4.4-fold spread", "EN sonuc aralik"),
    ("The same design run on CIFAR-100 widens the spread to $13.58\\pm1.71$ points "
     "rather than shrinking it",
     "The same design run on CIFAR-100 leaves the spread at $13.83\\pm1.30$ points, "
     "close to the CIFAR-10 value", "EN sonuc C100"),
])
yama("paper/manuscript_tr/sections/06_sonuc.tex", [
    ("$+4{,}4$ ile $+14{,}6$ puan arasında değişmektedir; bu, 3,3 katlık bir "
     "yayılımdır. buna karşılık",
     "$+4{,}4$ ile $+19{,}4$ puan arasında değişmektedir; bu, 4,4 katlık bir "
     "yayılımdır. Buna karşılık", "TR sonuc aralik"),
    ("Aynı tasarım CIFAR-100 üzerinde koşulduğunda yayılım daralmak yerine "
     "$13{,}58\\pm1{,}71$ puana genişlemekte",
     "Aynı tasarım CIFAR-100 üzerinde koşulduğunda yayılım CIFAR-10 değerine yakın "
     "kalmakta ($13{,}83\\pm1{,}30$ puan)", "TR sonuc C100"),
])

# ================= CIFAR-100 ON-KESTIRIM: K8 ile YUZLESME =================
EN_OK_E = ("Two of the three registered predictions are confirmed, and the third is "
           "not testable in this design. The prediction that the protocol spread "
           "would be larger on the harder dataset is confirmed ($13.58 > 10.45$), as "
           "is the prediction that the sign would be preserved ($12/12$).")
EN_OK_Y = (
    "One of the three registered predictions is confirmed, one fails under the "
    "reading we treat as binding, and the third is not testable in this design. The "
    "prediction that the sign would be preserved is confirmed ($12/12$). The "
    "prediction that the protocol spread would be larger on the harder dataset was "
    "registered as a comparison against the CIFAR-10 spread, quoted at the time as "
    "$10.45$ points. Against that literal threshold it holds ($13.83 > 10.45$); "
    "against the CIFAR-10 spread as it now stands under the successful-source "
    "definition of Section~\\ref{subsec:transfer} it does not ($13.83 < 15.01$). We "
    "report the failure rather than the reading that would rescue it, because the "
    "registration named the CIFAR-10 spread and not the number. The two datasets "
    "place the protocol effect in the same range instead of ordering it by "
    "difficulty, so the mechanism we propose predicts the size of the effect but "
    "not its ordering between these two datasets.")
yama("paper/manuscript/sections/04_experiments.tex", [(EN_OK_E, EN_OK_Y, "EN onkestirim")])

TR_OK_E = ("Üç ön kestirimin ikisi doğrulanmış, üçüncüsü ise bu tasarımda sınanamadı. "
           "Protokol yayılımının daha zor veri kümesinde büyüyeceği ön kestirimi "
           "doğrulanmıştır ($13{,}58 > 10{,}45$); işaretin korunacağı ön kestirimi de "
           "doğrulanmıştır ($12/12$).")
TR_OK_Y = (
    "Üç ön kestirimin biri doğrulanmış, biri bağlayıcı saydığımız okumada "
    "tutmamış, üçüncüsü ise bu tasarımda sınanamamıştır. İşaretin korunacağı ön "
    "kestirimi doğrulanmıştır ($12/12$). Protokol yayılımının daha zor veri "
    "kümesinde büyüyeceği ön kestirimi, CIFAR-10 yayılımına karşı bir "
    "karşılaştırma olarak kaydedilmiş ve o tarihte bu değer $10{,}45$ puan diye "
    "anılmıştı. Bu sayısal eşiğe karşı kestirim tutmaktadır ($13{,}83 > 10{,}45$); "
    "Bölüm~\\ref{subsec:transfer}'in başarılı kaynak tanımı altında CIFAR-10 "
    "yayılımının bugünkü değerine karşı ise tutmamaktadır ($13{,}83 < 15{,}01$). "
    "Kestirimi kurtaracak okumayı değil, tutmadığını raporluyoruz; çünkü kayıt "
    "sayıyı değil CIFAR-10 yayılımını adlandırmıştı. İki veri kümesi protokol "
    "etkisini zorluğa göre sıralamak yerine aynı aralığa yerleştirmektedir; yani "
    "önerdiğimiz mekanizma etkinin büyüklüğünü öngörmekte, bu iki veri kümesi "
    "arasındaki sıralamasını öngörmemektedir.")
yama("paper/manuscript_tr/sections/04_deneyler.tex", [(TR_OK_E, TR_OK_Y, "TR onkestirim")])

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("yazilan:", *yazilan, sep="\n  ")
