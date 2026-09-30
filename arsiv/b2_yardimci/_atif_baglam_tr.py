"""Atif-baglam duzeltmeleri (raporlar/atif_2026-09-30/rapor.md, Bolum 4.1: A1-A13, O1), TR aynasi.
EN karsiligi: _atif_baglam_en.py. Her eski dize TAM BIR kez gecmeli; aksi halde durur, dosya yazilmaz.
Kullanim (depo kokunden): python3 arsiv/b2_yardimci/_atif_baglam_tr.py
"""
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
SEC = ROOT / "paper" / "manuscript_tr" / "sections"

PATCHES = {
    "01_giris.tex": [
        # A1
        (
            "Benz vd.~\\cite{benz2021adversarial} ise standart eğitilmiş modellerde ViT'lerin daha gürbüz olduğunu "
            "bildirmektedir; mimariler arası transfer çalışmaları da saldırıların CNN'den ViT'e mi yoksa tersine mi "
            "daha kolay taşındığı konusunda uyuşmamaktadır~\\cite{mahmood2021robustness, ravikumar2023trend, "
            "naseer2022improving}. ",
            "Benz vd.~\\cite{benz2021adversarial} ise standart eğitilmiş modellerde ViT'lerin daha gürbüz olduğunu "
            "bildirmektedir. Transfer çalışmaları buna kendi uyuşmazlıklarını eklemektedir: birçoğu saldırıların "
            "ViT'den CNN'e, tersine göre daha kolay taşındığını bildirmekte~\\cite{mahmood2021robustness, "
            "benz2021adversarial, shao2022adversarial}, Naseer vd.~\\cite{naseer2022improving} ise ViT üzerinde "
            "üretilen pertürbasyonların geleneksel saldırılar altında zayıf transfer ettiğini bulmaktadır; bu makalede "
            "ölçülen yön ilk grubunkinin tersidir ve Bölüm~\\ref{sec:discussion} bu noktaya geri dönmektedir. ",
        ),
    ],
    "02_ilgili_calismalar.tex": [
        # A8
        (
            "Sertifikalı gürbüzlükteki güncel gelişmeler arasında, çok adımlı savunmalarla sertifika yarıçaplarını "
            "iyileştiren Uyarlanabilir Rastgeleleştirilmiş Yumuşatma~\\cite{lyu2024adaptive} sayılabilir.",
            "Sertifikalı gürbüzlükteki güncel gelişmeler arasında, rastgeleleştirilmiş yumuşatmayı test zamanında "
            "uyarlanan çok adımlı modelleri sertifikalandıracak biçimde genişleten Uyarlanabilir Rastgeleleştirilmiş "
            "Yumuşatma~\\cite{lyu2024adaptive} sayılabilir.",
        ),
        # A12
        (
            "RobustBench lider tablosu~\\cite{croce2021robustbench} en güncel CNN gürbüzlüğünü izlemektedir; "
            "CIFAR-10'da en yüksek gürbüz doğruluğa WideResNet türevleri ulaşmaktadır.",
            "RobustBench lider tablosu~\\cite{croce2021robustbench} gürbüz doğruluğu mimariden bağımsız olarak "
            "izlemektedir; CIFAR-10 sıralamasının tepesini WideResNet türevleri tutmaktadır.",
        ),
        # A7
        (
            "daha algısal hizalı~\\cite{tsipras2019robustness} ve daha seyrek~\\cite{chalasani2020concise} gradyanlar "
            "ürettiği bilinmektedir.",
            "daha algısal hizalı gradyanlar~\\cite{tsipras2019robustness} ve daha seyrek öznitelik "
            "atıfları~\\cite{chalasani2020concise} ürettiği bilinmektedir.",
        ),
        # A3
        (
            "İlk çalışmalar, küresel alıcı alan sayesinde ViT'lerin bazı içkin gürbüzlük özellikleri sergilediğini "
            "öne sürmüştür~\\cite{bhojanapalli2021understanding}.",
            "Bhojanapalli vd.~\\cite{bhojanapalli2021understanding}, yeterli veriyle ön eğitildiklerinde ViT'lerin "
            "geniş bir pertürbasyon yelpazesinde en az ResNet'ler kadar gürbüz olduğunu bulmuştur.",
        ),
        # A2
        (
            "Shao vd.~\\cite{shao2022adversarial}, çekişmeli eğitimin ViT gürbüzlüğünü artırabildiğini ve ViT "
            "özniteliklerinin yüksek frekanslı içeriğe daha az dayandığını göstermiştir; eğitim kararsızlığı kaynaklı "
            "güçlükler ise sürmektedir.",
            "Shao vd.~\\cite{shao2022adversarial}, ViT'leri beyaz kutu ve transfer ayarlarında CNN'lerden ve "
            "MLP-Mixer'lardan daha gürbüz bulmuş, özniteliklerinin daha az yüksek frekanslı içerik taşıdığını "
            "göstermiş ve çekişmeli eğitimin ViT'lere uygulanabildiğini ortaya koymuştur; ancak ön niteliğindeki "
            "CIFAR-10 koşusunda çekişmeli eğitilmiş ViT büyük bir CNN'i geçememiştir.",
        ),
        # A4
        (
            "Daha yakın zamanda Jain vd.~\\cite{jain2024towards}, ViT'e özgü eğitim güçlüklerini ele alan AAS-AT "
            "yöntemini önermiş; difüzyonla",
            "Daha yakın zamanda Jain vd.~\\cite{jain2024towards}, ViT'lerdeki bir gradyan maskeleme biçimini dikkatteki "
            "softmax alt taşmasına (underflow) bağlamış ve PGD türü saldırıların bu yüzden ViT'lerde eksik kaldığını "
            "göstermiştir; yalnız PGD'ye dayanan ViT değerlendirmeleri için bir uyarı olan bu bulguya karşı AutoAttack, "
            "gradyansız Square bileşeniyle kısmi bir güvence sağlar. Düzeltilmiş saldırı üzerine kurdukları çekişmeli "
            "eğitim tarifi CIFAR-10 ve ImageNet-100'de mevcut ViT tariflerini geçmektedir; difüzyonla",
        ),
        # A6
        (
            "Transfer edilebilirlik; model mimarisi, eğitim verisi ve saldırı yöntemi gibi etkenlere "
            "bağlıdır~\\cite{demontis2019adversarial}.",
            "Demontis vd.~\\cite{demontis2019adversarial} transfer edilebilirliği iki etkene, hedef modelin içkin "
            "kırılganlığına ve vekil modelin karmaşıklığına bağlamakta ve onu iki modelin girdi gradyanlarının "
            "hizalanmasıyla ilişkilendirmektedir.",
        ),
        # A10
        (
            "güncel değerlendirme kılavuzları bu tür protokol seçimlerini açık hâle getirmektedir~\\cite{zhao2025revisiting}.",
            "transfer saldırılarının sistematik yeniden değerlendirmeleri de havuzu her modelin doğru sınıflandırdığı "
            "örneklerle sınırlamaktadır~\\cite{zhao2025revisiting}.",
        ),
        # A5
        (
            "Chen vd.~\\cite{chen2023understanding}, mimariler arası transferi etkileyen etkenleri sistematik olarak "
            "incelemekte ve mimari tümevarım önyargılarının (CNN'lerin yüksek, ViT'lerin düşük frekanslı bilgiyi tercih "
            "etmesi) transfer başarısını önemli ölçüde etkilediğini bulmaktadır.",
            "Chen vd.~\\cite{chen2023understanding}, CNN'ler ile ViT'lerin farklı tümevarım önyargılarından yararlanan "
            "bir transfer saldırısı önermektedir; bu farkın ardındaki frekans tercihleri, CNN'lerin yüksek, ViT'lerin "
            "düşük frekanslı içeriğe yaslanması, Benz vd.~\\cite{benz2021adversarial} ve Shao "
            "vd.~\\cite{shao2022adversarial} tarafından belgelenmiştir.",
        ),
        # A9 (02:74)
        (
            "Transfer değerlendirmesini doğru sınıflandırılan örneklerle koşullamak yerleşik "
            "pratiktir~\\cite{liu2017delving, dong2018boosting, mahmood2021robustness, ravikumar2023trend} ve tekil "
            "makaleler bir protokol seçip devam etmektedir.",
            "Transfer değerlendirmesini modellerin doğru sınıflandırdığı örneklerle koşullamak yerleşik "
            "pratiktir~\\cite{liu2017delving, dong2018boosting, mahmood2021robustness, ravikumar2023trend} ve tekil "
            "makaleler bir koşullama kümesi seçip devam etmektedir.",
        ),
    ],
    "03_yontem.tex": [
        # A11
        (
            "tutarlı parti-normalizasyonu istatistikleri görür ve standart çekişmeli eğitim gerçeklemeleri "
            "izlenir~\\cite{rice2020overfitting}.",
            "tutarlı parti-normalizasyonu istatistikleri görür; bu, Rice vd.'nin~\\cite{rice2020overfitting} referans "
            "gerçeklemesindeki uygulamadır.",
        ),
        # A9 (03:116)
        (
            "Transfer değerlendirmesini doğru sınıflandırılan örneklerle koşullamak yerleşik "
            "pratiktir~\\cite{liu2017delving, dong2018boosting, mahmood2021robustness, ravikumar2023trend, "
            "zhao2025revisiting} ve en çok mimariler arası karşılaştırmalarda önem taşır:",
            "Transfer değerlendirmesini doğru sınıflandırılan örneklerle koşullamak yerleşik pratiktir ve genellikle "
            "çalışmadaki her modelin doğru sınıflandırdığı örnekler üzerinde yapılır~\\cite{liu2017delving, "
            "dong2018boosting, mahmood2021robustness, ravikumar2023trend, zhao2025revisiting}; hedef-doğru oran bu "
            "havuzun tek yanlı gevşetmesidir ve koşullama en çok mimariler arası karşılaştırmalarda önem taşır:",
        ),
    ],
    "04_deneyler.tex": [
        # A7 (04:299)
        (
            "yani çekişmeli eğitim CNN gradyanlarını çok daha güçlü seyrekleştirmektedir~\\cite{chalasani2020concise} "
            "ile tutarlı olarak.",
            "yani çekişmeli eğitim CNN gradyanlarını çok daha güçlü seyrekleştirmektedir; bu, Chalasani "
            "vd.'nin~\\cite{chalasani2020concise} çekişmeli eğitilmiş modeller için bildirdiği daha seyrek öznitelik "
            "atıflarıyla uyumludur.",
        ),
    ],
    "05_tartisma.tex": [
        # O1 + A6
        (
            "Mahmood ve ark.~\\cite{mahmood2021robustness} farklı bir mimari çiftinde ters yönü raporlamakta; "
            "dönüştürücüye doğru transferi ondan dışarı olan transferden zayıf bulmaktadır. Mekanizmamız bununla "
            "uyumludur: asimetriyi, CNN'de üretilen pertürbasyonların özel bir gücüyle değil hedefin kendi "
            "kırılganlığıyla ilişkilendiriyoruz ve onların çiftinde zayıf hedef olan taraf bizimkinden farklıdır.",
            "Mahmood ve ark.~\\cite{mahmood2021robustness} farklı bir mimari çiftinde ters yönü raporlamakta, "
            "dönüştürücüye doğru transferi ondan dışarı olan transferden zayıf bulmaktadır; Benz "
            "vd.~\\cite{benz2021adversarial} ile Shao vd.~\\cite{shao2022adversarial} de kendi model kümelerinde aynı "
            "sıralamayı bildirmektedir. Mekanizmamız bu sonuçlarla uyumludur: asimetriyi, CNN'de üretilen "
            "pertürbasyonların özel bir gücüyle değil hedefin kendi kırılganlığıyla ilişkilendiriyoruz, ki bu Demontis "
            "vd.'nin~\\cite{demontis2019adversarial} saptadığı iki etkenden ilkidir, ve Mahmood ve ark.'nın çiftinde "
            "zayıf hedef olan taraf bizimkinden farklıdır.",
        ),
        # A13
        (
            "ve difüzyonla üretilmiş sentetik veriyle ViT'lerin CIFAR-10'da WideResNet'leri geçtiği "
            "bildirilmiştir~\\cite{wang2023better, wu2025vision}.",
            "ve Wang vd.'nin~\\cite{wang2023better} difüzyonla üretilmiş veri tarifiyle eğitilen bir ViT'in CIFAR-10'da "
            "WideResNet'leri geçtiği bildirilmiştir~\\cite{wu2025vision}.",
        ),
    ],
}


def main():
    hata = 0
    for fname, pairs in PATCHES.items():
        path = SEC / fname
        text = io.open(path, encoding="utf-8").read()
        new_text = text
        for i, (old, new) in enumerate(pairs, 1):
            n_old = new_text.count(old)
            if n_old == 1:
                new_text = new_text.replace(old, new)
                print(f"OK    {fname} #{i}")
            elif n_old == 0 and new_text.count(new) == 1:
                print(f"ZATEN {fname} #{i} (yeni dize mevcut)")
            else:
                print(f"HATA  {fname} #{i}: eski dize {n_old} kez gecti")
                hata += 1
        if new_text != text and not hata:
            io.open(path, "w", encoding="utf-8", newline="\n").write(new_text)
    if hata:
        print(f"\n{hata} yama uygulanamadi; HICBIR dosya yazilmadi (hatali dosyalar).")
        sys.exit(1)
    print("\nTum TR atif-baglam yamalari tamam.")


if __name__ == "__main__":
    main()
