"""turkce-yazi denetimi (30.09.2026) sonrasi hedefli TR yamalari + bir EN capraz atif duzeltmesi.
1) Duzeltme isareti (â î û) TR bolumlerinde ve TR main.tex'te karakter duzeyinde kaldirilir.
2) 01_giris ve 06_sonuc'ta rapor sesi (-maktadir) genis zamana / ulaca cekilir; icerik ayni.
3) Betiklerin isaretledigi tekil cumleler.
4) EN 04:421 'subsec:attacks' -> 'subsec:attack_methods' (TR ile ayni; butce §3'te tanimli).
Her eski dize TAM BIR kez gecmeli; aksi halde durur, o dosya yazilmaz.
Kullanim (depo kokunden): python3 arsiv/b2_yardimci/_tr_uslup_yama.py
"""
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
TR = ROOT / "paper" / "manuscript_tr"
EN = ROOT / "paper" / "manuscript" / "sections"

SAPKA = {"â": "a", "î": "i", "û": "u", "Â": "A", "Î": "İ", "Û": "U"}

PATCHES = {
    TR / "sections" / "01_giris.tex": [
        (
            "Literatür bu soruya tutarsız yanıtlar vermektedir: Bai vd.~\\cite{bai2021transformers} eşleşmiş eğitim "
            "tarifleri altında dönüştürücülerin CNN'leri geçmediğini, Benz vd.~\\cite{benz2021adversarial} ise standart "
            "eğitilmiş modellerde ViT'lerin daha gürbüz olduğunu bildirmektedir. Transfer çalışmaları buna kendi "
            "uyuşmazlıklarını eklemektedir: birçoğu saldırıların ViT'den CNN'e, tersine göre daha kolay taşındığını "
            "bildirmekte~\\cite{mahmood2021robustness, benz2021adversarial, shao2022adversarial}, Naseer "
            "vd.~\\cite{naseer2022improving} ise ViT üzerinde üretilen pertürbasyonların geleneksel saldırılar altında "
            "zayıf transfer ettiğini bulmaktadır; bu makalede ölçülen yön ilk grubunkinin tersidir ve "
            "Bölüm~\\ref{sec:discussion} bu noktaya geri dönmektedir.",
            "Literatür bu soruya tutarsız yanıtlar verir: Bai vd.~\\cite{bai2021transformers} eşleşmiş eğitim "
            "tarifleri altında dönüştürücülerin CNN'leri geçmediğini, Benz vd.~\\cite{benz2021adversarial} ise standart "
            "eğitilmiş modellerde ViT'lerin daha gürbüz olduğunu bildirir. Transfer çalışmaları buna kendi "
            "uyuşmazlıklarını ekler: birçoğu saldırıların ViT'den CNN'e, tersine göre daha kolay taşındığını "
            "bildirir~\\cite{mahmood2021robustness, benz2021adversarial, shao2022adversarial}, Naseer "
            "vd.~\\cite{naseer2022improving} ise ViT üzerinde üretilen pertürbasyonların geleneksel saldırılar altında "
            "zayıf transfer ettiğini bulur; bu makalede ölçülen yön ilk grubunkinin tersidir ve "
            "Bölüm~\\ref{sec:discussion} bu noktaya geri döner.",
        ),
        (
            "mimari başına üç bağımsız eğitim koşusu yapılmakta ve \\emph{her} eğitim aşamasından önce ayrılan sabit bir "
            "doğrulama bölmesi kullanılmaktadır, dolayısıyla hiçbir model gördüğü veriyle seçilmemektedir. Tüm "
            "değerlendirmeler, örnek bazında sonuç kaydıyla tam test kümesinde koşmaktadır; bu, eşleştirilmiş "
            "istatistikleri mümkün kılar: aynı örnekler, saldırıyı yeniden koşmadan farklı protokoller altında yeniden "
            "ağırlıklandırılabilir. Modeller sabitken yalnızca protokol değiştirilmekte ve sonucun ne kadar kaydığını "
            "ölçmekteyiz.",
            "mimari başına üç bağımsız eğitim koşusu yapıyoruz; \\emph{her} eğitim aşamasından önce ayrılan sabit bir "
            "doğrulama bölmesi kullandığımız için hiçbir model gördüğü veriyle seçilmiyor. Tüm değerlendirmeler tam test "
            "kümesinde, örnek bazında sonuç kaydıyla koşar; bu kayıt eşleştirilmiş istatistikleri mümkün kılar: aynı "
            "örnekler, saldırıyı yeniden koşmadan farklı protokoller altında yeniden ağırlıklandırılabilir. Modeller "
            "sabitken yalnızca protokolü değiştiriyor ve sonucun ne kadar kaydığını ölçüyoruz.",
        ),
        (
            "Her biri, amaca özel bir ölçümle doğrudan test edilmektedir.",
            "Her birini amaca özel bir ölçümle doğrudan sınıyoruz.",
        ),
        (
            "puan arasında değişmekte, buna karşılık her iki mimariyi sıfırdan yeniden eğitmek aynı niceliği $1{,}5$ "
            "puandan az oynatmaktadır. Yayılım şöyle ayrışır. Koşulsuz kestirimi hedef doğru kestirimden ayıran $9{,}21$ "
            "puanı türettiğimiz bir özdeşlik kapalı formda kaldırmakta, $5{,}79$ puan ise farklı bir niceliği kestiren "
            "bir protokolden gelmektedir.",
            "puan arasında değişirken her iki mimariyi sıfırdan yeniden eğitmek aynı niceliği $1{,}5$ puandan az "
            "oynatır. Yayılım şöyle ayrışır. Koşulsuz kestirimi hedef doğru kestirimden ayıran $9{,}21$ puanı "
            "türettiğimiz bir özdeşlik kapalı formda kaldırır, $5{,}79$ puan ise farklı bir niceliği kestiren bir "
            "protokolden gelir.",
        ),
        (
            "Bir eşdeğerlik testinin kabul mü ret mi edileceğine de protokol karar vermektedir.",
            "Bir eşdeğerlik testinin kabul mü ret mi edileceğine de protokol karar verir.",
        ),
        (
            "eşitlendiklerinde dört protokolün ikisi yönü tersine çevirmektedir.",
            "eşitlendiklerinde dört protokolün ikisi yönü tersine çevirir.",
        ),
        (
            "yayılımı CIFAR-10'daki büyüklüğüne yakın tutmakta ve işaretini korumaktadır; sabit bir eğitim yörüngesi "
            "üzerinde değiştirilen çevrimdışı kontrol noktası seçim kuralı da makalelerin nadiren raporladığı bir "
            "varyans kaynağı olarak ortaya çıkmaktadır.",
            "yayılımı CIFAR-10'daki büyüklüğüne yakın tutar ve işaretini korur; sabit bir eğitim yörüngesi üzerinde "
            "değiştirilen çevrimdışı kontrol noktası seçim kuralı da makalelerin nadiren raporladığı bir varyans "
            "kaynağı olarak ortaya çıkar.",
        ),
        (
            "Gelen transfer de hedefin kendi kırılganlığını izlemekte (üç hedef üzerinde $r=0{,}986$) ve asimetriyi daha "
            "zayıf hedefin bir özelliği olarak yeniden çerçevelemektedir.",
            "Gelen transfer de hedefin kendi kırılganlığını izler (üç hedef üzerinde $r=0{,}986$) ve asimetriyi daha "
            "zayıf hedefin bir özelliği olarak yeniden çerçeveler.",
        ),
        (
            "ölçekten bağımsız seyreklik farkları mekansal lokalite farkına karşılık gelmemektedir; dört mekansal "
            "ölçütün dördü de sıfır sonuç vermiştir. CLS dikkat entropisi $n=1000$'de saldırı altında ölçülebilir "
            "biçimde değişmemektedir. ViT'e özgü bir transfer saldırısı olan Jeton Gradyanı Düzenlileştirme "
            "(TGR)~\\cite{zhang2023tgr} bu rejimde transfer kazancı sağlamamakta, eşleşmiş bütçede düz MI-FGSM'ye "
            "yenilmektedir. İki davranışsal fark ise ayakta kalmaktadır. Gradyan seyrekliği farkları bağımsız kontrol "
            "noktası kümelerinde tekrarlanmakta, çekişmeli eğitimle ortaya çıkmakta ve yalnızca mutlak kosinüste var "
            "olan bir hizalanma farkıyla birlikte gelmektedir. Çekişmeli hasar iki mimaride nitel olarak farklı "
            "derinliklerde birikmektedir ve ölçülen kayma profili",
            "ölçekten bağımsız seyreklik farkları mekansal lokalite farkına karşılık gelmez; dört mekansal ölçütün "
            "dördü de sıfır sonuç vermiştir. CLS dikkat entropisi $n=1000$'de saldırı altında ölçülebilir biçimde "
            "değişmez. ViT'e özgü bir transfer saldırısı olan Jeton Gradyanı Düzenlileştirme (TGR)~\\cite{zhang2023tgr} "
            "bu rejimde transfer kazancı sağlamaz, eşleşmiş bütçede düz MI-FGSM'ye yenilir. İki davranışsal fark ise "
            "ayakta kalır. Gradyan seyrekliği farkları bağımsız kontrol noktası kümelerinde tekrarlanır, çekişmeli "
            "eğitimle ortaya çıkar ve yalnızca mutlak kosinüste var olan bir hizalanma farkıyla birlikte gelir. "
            "Çekişmeli hasar iki mimaride nitel olarak farklı derinliklerde birikir ve ölçülen kayma profili",
        ),
        (
            "somut raporlama gerekliliklerine dönüşmektedir; bu gereklilikler",
            "somut raporlama gerekliliklerine dönüşür; bu gereklilikler",
        ),
        (
            "Bölüm~\\ref{sec:related_work} çekişmeli değerlendirme pratiğini ve mimari karşılaştırma çalışmalarını gözden "
            "geçirdikten sonra Bölüm~\\ref{sec:methodology} eğitim protokolünü, koşullama protokollerini ve ölçümleri "
            "tanımlamakta, Bölüm~\\ref{sec:experiments} ise sonuçları raporlamaktadır. Çıkarımları ve sınırlılıkları "
            "Bölüm~\\ref{sec:discussion} ele almakta, Bölüm~\\ref{sec:conclusion} çalışmayı sonuçlandırmaktadır.",
            "Bölüm~\\ref{sec:related_work} çekişmeli değerlendirme pratiğini ve mimari karşılaştırma çalışmalarını gözden "
            "geçirir; Bölüm~\\ref{sec:methodology} eğitim protokolünü, koşullama protokollerini ve ölçümleri tanımlar; "
            "Bölüm~\\ref{sec:experiments} sonuçları verir. Çıkarımlar ve sınırlılıklar Bölüm~\\ref{sec:discussion}'te, "
            "sonuç Bölüm~\\ref{sec:conclusion}'da yer alır.",
        ),
    ],
    TR / "sections" / "06_sonuc.tex": [
        (
            "puan arasında değişmekte, buna karşılık her iki mimariyi sıfırdan yeniden eğitmek aynı niceliği $1{,}5$ "
            "puandan az oynatmaktadır. Bu $15{,}01$ puanlık yayılım, türettiğimiz bir özdeşliğin kapalı formda "
            "kaldırdığı $9{,}21$ puan ile farklı bir niceliği kestiren bir protokolden gelen $5{,}79$ puana "
            "ayrılmaktadır.",
            "puan arasında değişirken her iki mimariyi sıfırdan yeniden eğitmek aynı niceliği $1{,}5$ puandan az "
            "oynatır. Bu $15{,}01$ puanlık yayılım, türettiğimiz bir özdeşliğin kapalı formda kaldırdığı $9{,}21$ puan "
            "ile farklı bir niceliği kestiren bir protokolden gelen $5{,}79$ puana ayrılır.",
        ),
        (
            "ölçeklenmiş haline cebirsel olarak eşittir; bu özdeşlik $36$ ölçülen yönde $0{,}41$ puandan küçük bir "
            "hatayla tutmakta ve ölçülen öncülü sağlayan yayımlanmış herhangi bir ham orana uygulanabilmektedir. "
            "CIFAR-100 yinelemesi ile kontrol noktası seçimi ablasyonu aynı yönü göstermektedir:",
            "ölçeklenmiş haline cebirsel olarak eşittir; bu özdeşlik $36$ ölçülen yönde $0{,}41$ puandan küçük bir "
            "hatayla tutar ve ölçülen öncülü sağlayan yayımlanmış herhangi bir ham orana uygulanabilir. CIFAR-100 "
            "yinelemesi ile kontrol noktası seçimi ablasyonu aynı yönü gösterir:",
        ),
        (
            "dört protokolün ikisi işareti tersine çevirmekte ve birincil protokol eşdeğerliği kabul etmektedir. Başka "
            "bir deyişle yön, modeller eşitlenmemişken geçerlidir ve üç hedefli analizimiz onu hedefin kendi "
            "kırılganlığıyla ($r = 0{,}986$) ilişkilendirmektedir.",
            "dört protokolün ikisi işareti tersine çevirir ve birincil protokol eşdeğerliği kabul eder. Başka bir "
            "deyişle yön, modeller eşitlenmemişken geçerlidir ve üç hedefli analizimiz onu hedefin kendi "
            "kırılganlığıyla ($r = 0{,}986$) ilişkilendirir.",
        ),
        (
            "$L_\\infty$ saldırısı altında değişmemektedir; dönüştürücüye özgü bir transfer saldırısı bu rejimde transfer "
            "kazancı sağlamamaktadır.",
            "$L_\\infty$ saldırısı altında değişmez; dönüştürücüye özgü bir transfer saldırısı bu rejimde transfer "
            "kazancı sağlamaz.",
        ),
        (
            "gradyan seyrekliği sıralaması ile CNN'de geç katmanlarda",
            "gradyan seyrekliği sıralaması ve CNN'de geç katmanlarda",
        ),
        (
            "Çalışmamız üç veri kümesini ve tek bir model çiftini kapsamaktadır; dolayısıyla protokol etkisinin başka "
            "mimari çiftlerindeki boyutu kalibre edilmeyi beklemektedir.",
            "Çalışmamız üç veri kümesini ve tek bir model çiftini kapsadığından protokol etkisinin başka mimari "
            "çiftlerindeki boyutu kalibre edilmeyi bekler.",
        ),
    ],
    TR / "sections" / "02_ilgili_calismalar.tex": [
        (
            "Atıf yapılan çalışmalarda yalnız üçüncüsü iddia edilmektedir; ilk ikisi yorumdur.",
            "Anılan çalışmalar yalnız üçüncüsünü ileri sürer; ilk ikisi yorumdur.",
        ),
    ],
    TR / "sections" / "03_yontem.tex": [
        (
            "Bu, mutlak bir doğruluk için doğru ölçek, transfer asimetrisi için yanlış ölçektir:",
            "Bu marj mutlak doğruluk için doğru, transfer asimetrisi için yanlış ölçektir:",
        ),
    ],
    TR / "sections" / "04_deneyler.tex": [
        # EN 04:121'deki MI-FGSM adim notu ve Tablo tgr gondermesi TR'de eksikti (HEAD'de de yoktu).
        (
            "momentum tabanlı MI-FGSM~\\cite{dong2018boosting} altında da ($19{,}07\\pm0{,}33$'e karşı "
            "$\\%15{,}42\\pm0{,}52$, hedef doğru) tersinden daha iyi transfer olmaktadır; dolayısıyla etki PGD "
            "saldırısının bir artefaktı değildir.",
            "momentum tabanlı MI-FGSM~\\cite{dong2018boosting} altında da ($19{,}07\\pm0{,}33$'e karşı "
            "$\\%15{,}42\\pm0{,}52$, hedef doğru; bu iki yönlü kontrol başka yerde kullanılan $\\alpha=2/255$'i değil "
            "saldırının kendi varsayılan adımı $\\alpha=\\eps/10$'u kullanır, ViT$\\rightarrow$CNN değerinin "
            "Tablo~\\ref{tab:tgr}'deki eşleşmiş bütçeli değerden hafifçe ayrılmasının nedeni budur) tersinden daha iyi "
            "transfer olur; dolayısıyla etki PGD saldırısının bir artefaktı değildir.",
        ),
    ],
    TR / "sections" / "05_tartisma.tex": [
        (
            "Ablasyonun sağladığı şey ise Bölüm~\\ref{subsec:statistics_results}'te raporlanan seçim protokolü "
            "yayılımıdır.",
            "Ablasyonun verdiği ise Bölüm~\\ref{subsec:statistics_results}'te raporlanan seçim protokolü yayılımıdır.",
        ),
        (
            "bu, ayakta kalan davranışsal farkların, yani seyreklik sıralaması ile derinlik profillerinin, ailelerin mi "
            "yoksa bu küçük modellerin mi özelliği olduğunu test edecektir.",
            "böyle bir çift, ayakta kalan davranışsal farkların, yani seyreklik sıralamasıyla derinlik profillerinin, "
            "ailelerin mi yoksa bu küçük modellerin mi özelliği olduğunu sınayacaktır.",
        ),
    ],
    EN / "04_experiments.tex": [
        (
            "at the budget used throughout this paper (Section~\\ref{subsec:attacks}),",
            "at the budget used throughout this paper (Section~\\ref{subsec:attack_methods}),",
        ),
    ],
}


def main():
    hata = 0
    # 1) sapka: TR bolumleri + TR main.tex
    n_sapka = 0
    for p in sorted((TR / "sections").glob("0?_*.tex")) + [TR / "main.tex"]:
        t = io.open(p, encoding="utf-8").read()
        t2 = t
        for a, b in SAPKA.items():
            t2 = t2.replace(a, b)
        if t2 != t:
            n_sapka += sum(t.count(a) for a in SAPKA)
            io.open(p, "w", encoding="utf-8", newline="\n").write(t2)
    print(f"sapka kaldirildi: {n_sapka} karakter")

    # 2-4) cumle yamalari
    for path, pairs in PATCHES.items():
        text = io.open(path, encoding="utf-8").read()
        new_text = text
        for i, (old, new) in enumerate(pairs, 1):
            n_old = new_text.count(old)
            if n_old == 1:
                new_text = new_text.replace(old, new)
                print(f"OK    {path.name} #{i}")
            elif n_old == 0 and new_text.count(new) == 1:
                print(f"ZATEN {path.name} #{i}")
            else:
                print(f"HATA  {path.name} #{i}: eski dize {n_old} kez gecti")
                hata += 1
        if new_text != text and not hata:
            io.open(path, "w", encoding="utf-8", newline="\n").write(new_text)
    if hata:
        print(f"\n{hata} yama uygulanamadi; hatali dosya(lar) yazilmadi.")
        sys.exit(1)
    print("\nTum uslup yamalari tamam.")


if __name__ == "__main__":
    main()
