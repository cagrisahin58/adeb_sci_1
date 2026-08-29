#!/usr/bin/env python3
"""TR aynasi - 3: sekil kaldirmalari, tekrar kesimleri, uslup kalintilari."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")
D = "04_deneyler.tex"
p4 = ROOT / D

# ---- Ingilizce tarafla AYNI uc sekil kaldirilir ----
t = p4.read_text(encoding="utf-8")
for ad in ("fig_tsne_features", "fig1_robustness_comparison",
           "fig_adversarial_examples"):
    t2, n = re.subn(
        r"\\begin\{figure\}\[!t\]\s*\\centering\s*"
        r"\\includegraphics\[[^\]]*\]\{[^}]*" + ad + r"\.pdf\}\s*"
        r"\\caption\{.*?\}\s*\\label\{fig:[a-z_0-9]*\}\s*\\end\{figure\}\s*",
        "", t, count=1, flags=re.DOTALL)
    if n:
        t = t2
        print(f"  [+] {ad} sekil blogu kaldirildi")
    elif ad not in t:
        print(f"  [=] {ad} zaten yok")
    else:
        sys.exit(f"BASARISIZ: {ad} desene uymadi")
p4.write_text(t, encoding="utf-8")

YAMALAR = [
    # ---- t-SNE paragrafi (sekle gonderme kalkar, sayilar kalir) ----
    (D,
     r"Şekil~\ref{fig:tsne_features}, sondan bir önceki katman öznitelik "
     r"uzaylarının gösterim amaçlı bir t-SNE gömmesini verir. t-SNE gömmeleri "
     r"hiperparametrelere duyarlı olduğundan ve nitel aşırı yorumu davet "
     r"ettiğinden, tüm iddiaları özgün öznitelik uzayında hesaplanan metriklere "
     r"dayandırıyoruz (koşu başına $n$=500; her model beyaz kutu saldırıya "
     r"uğratılmış; üç koşu üzerinden ortalama$\pm$std). Saldırı, sınıf yapısını en "
     r"güçlü biçimde \emph{CNN'de} çökertmektedir: temizde eğitilmiş 5-NN etiket "
     r"tutarlılığı $\%87{,}3\pm2{,}6$'dan $\%51{,}3\pm1{,}8$'e düşer, siluet "
     r"skoru $0{,}196\pm0{,}010$'dan $-0{,}032\pm0{,}004$'e iner, sınıf "
     r"içi/sınıflar arası uzaklık oranı $0{,}511\pm0{,}013$'ten "
     r"$0{,}847\pm0{,}003$'e çıkar ve göreli sınıf merkezi kayması "
     r"$0{,}238\pm0{,}012$'dir. ViT'in sondan bir önceki uzayı temiz girdilerde "
     r"bile zayıf sınıf ayrımı gösterir (siluet $-0{,}021\pm0{,}005$; 5-NN "
     r"tutarlılığı $\%61{,}1\pm1{,}4$, saldırıda $\%48{,}5\pm1{,}4$'e düşer) ve "
     r"merkezleri çok daha az kayar ($0{,}083\pm0{,}004$).",

     r"Sondan bir önceki katmanın geometrisi, düşük boyutlu bir gömmeden değil "
     r"özgün öznitelik uzayında ölçülmektedir; gömme nitel aşırı yorumu davet "
     r"ederdi (koşu başına $n$=500; beyaz kutu; üç koşu üzerinden "
     r"ortalama$\pm$std). Saldırı, sınıf yapısını en güçlü biçimde \emph{CNN'de} "
     r"çökertmektedir: temizde eğitilmiş 5-NN etiket tutarlılığı "
     r"$\%87{,}3\pm2{,}6$'dan $\%51{,}3\pm1{,}8$'e, siluet skoru "
     r"$0{,}196\pm0{,}010$'dan $-0{,}032\pm0{,}004$'e iner ve göreli sınıf merkezi "
     r"kayması $0{,}238\pm0{,}012$'ye karşı ViT'te $0{,}083\pm0{,}004$'tür; ViT'in "
     r"uzayı temiz girdilerde bile zayıf sınıf ayrımı gösterir (siluet "
     r"$-0{,}021\pm0{,}005$; 5-NN tutarlılığı $\%61{,}1\pm1{,}4$, saldırıda "
     r"$\%48{,}5\pm1{,}4$).",
     "TR t-SNE paragrafi"),

    # ---- C3: entropi sekil cumlesi (EN'de tamamen kaldirildi) ----
    (D,
     "\nŞekil~\\ref{fig:feature_degradation}, temsilî bir örneğin temiz ve "
     "çekişmeli CLS dikkatini katman başına entropi eğrileriyle birlikte "
     "gösterir; iki entropi eğrisi üst üste binmektedir; yukarıda raporlanan "
     "sıfır sonucun görsel biçimi budur.\n",
     "\n",
     "TR C3 entropi sekil cumlesi"),

    # ---- dikkat haritasi paragrafi sikistirma ----
    (D,
     r"Nicel ölçümleri tamamlayıcı olarak Şekil~\ref{fig:attention_layers}, "
     r"temsilî bir örnek için 1., 6.\ ve 12.\ katmanlardaki CLS dikkat "
     r"haritalarını görselleştirir. Görselleştirme yukarıdaki yer değiştirme "
     r"ölçümüyle tutarlıdır, çünkü geç katmanlar erken katmanlardan daha çok "
     r"hareket eder; ancak bu türden tek örnekli dikkat panellerinin kolayca fazla "
     r"yorumlandığına dikkat çekiyoruz:",
     r"Şekil~\ref{fig:attention_layers}, temsilî bir örnek için 1., 6.\ ve 12.\ "
     r"katmanlardaki CLS dikkat haritalarını görselleştirir. Yer değiştirme "
     r"ölçümüyle uyumludur, çünkü geç katmanlar daha çok hareket eder; ancak bu "
     r"türden tek örnekli paneller kolayca fazla yorumlanır:",
     "TR dikkat haritasi"),

    # ---- C13: "birincisi" AI kalintisi + dilbilgisi hatasi ----
    (D,
     r"Bundan çıkan iki sonuçtan birincisi, iki mimarinin hasarın "
     r"\emph{birikip birikmediğinde} değil \emph{nerede} biriktiğinde "
     r"ayrışmaktadır.",
     r"Bundan iki sonuç çıkar. Mimariler hasarın \emph{birikip birikmediğinde} "
     r"değil \emph{nerede} biriktiğinde ayrışmaktadır.",
     "TR C13 uslup"),

    # ---- token toplulastirma (03'te zaten var) ----
    (D,
     r"ve bir dönüştürücü bloğunu özetlemekte kullanılan jeton agregasyonu. ViT "
     r"için yalnız CLS jetonunu, 196 yama jetonunun ortalamasını ve tüm jetonların "
     r"düzleştirilmiş birleşimini; CNN için mekânsal boyutlar üzerinden "
     r"düzleştirilmiş her artık blok çıktısını raporluyoruz.",
     r"ve bir dönüştürücü bloğunu özetlemekte kullanılan jeton agregasyonu "
     r"(Bölüm~\ref{subsec:metrics}).",
     "TR token tekrari"),

    # ---- B6 devami: L2 tekrari ----
    (D,
     r"Eğim, özdeşliği örneklem dışında da doğrulamaktadır. "
     r"Denklem~\eqref{eq:raw_identity}, eğimin hedefler üzerinden ortalanmış "
     r"$1-r_{\text{koş}}$ değerine eşit olmasını öngörür. Koşullu oranlar",
     r"Bu sınama geçmektedir. Koşullu oranlar",
     "TR L2 tekrari"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
