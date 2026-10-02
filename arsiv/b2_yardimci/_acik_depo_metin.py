"""Acik depo karari (2026-10-02): 'upon acceptance' dili kalkar, URL girer; fon 'no specific grant'.
Dokunulan yerler: EN/TR main.tex veri-kod bolumu, EN/TR §6 son cumle, declarations.txt (§2, §4, tarih),
cover_letter.tex, pre_submission_checklist.md. Her eski dize TAM BIR kez gecmeli.
Kullanim (depo kokunden): python3 arsiv/b2_yardimci/_acik_depo_metin.py
"""
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
URL = "https://github.com/cagrisahin58/cnn-vit-robustness-protocols"

PATCHES = {
    ROOT / "paper/manuscript/main.tex": [
        (
            "% TODO(submission): repo URL — kabul sonrasi (veya gonderimde anonim depo ile)\n"
            "% asagidaki cumleye gercek URL eklenecek.\n"
            "% 2026-08-25: vaat KAPSAMLANDI. Yayimlanacak kume makaledeki her sayiyi\n"
            "% yeniden uretmeye yeter (analiz kodu + ornek bazinda kayitlar + bolme\n"
            "% indeksleri + tohumlar); kontrol noktalari (~36 GB) istek uzerine.\n"
            "% Uc yerdeki dil ayni: gelecek zaman, ayni kapsam.\n",
            "% 2026-10-02: depo HERKESE ACIK (cnn-vit-robustness-protocols; kurucu betik\n"
            "% scripts/acik_depo_kur.sh). Kapsam vaatle ayni: analiz kodu + ornek bazinda\n"
            "% kayitlar + bolme indeksleri + tohumlar; kontrol noktalari (40 GB) istek\n"
            "% uzerine. Uc yerdeki dil ayni: simdiki zaman, ayni kapsam (burasi, §6, TR).\n",
        ),
        (
            "Upon acceptance we will publish the analysis pipeline, the scripts that generate every table and figure "
            "in this paper, the per-sample evaluation records, the fixed validation-split indices and the seed lists, "
            "which together reproduce every number reported here; the four conditioning protocols are all computed "
            "from the per-sample records, so the protocol comparison can be repeated without retraining. An "
            "anonymized copy of that archive is available to reviewers during review at "
            "\\texttt{[ANONYMOUS-ARCHIVE-URL]}, so the protocol comparison can be checked before acceptance rather "
            "than after it. Trained checkpoints total about $40$~GB and are available from the authors on request.",
            "The analysis pipeline, the scripts that generate every table and figure in this paper, the per-sample "
            "evaluation records, the fixed validation-split indices and the seed lists are publicly available at "
            "\\texttt{" + URL + "}; together they reproduce every number reported here, and because the four "
            "conditioning protocols are all computed from the per-sample records, the protocol comparison can be "
            "repeated without retraining. Trained checkpoints total about $40$~GB and are available from the "
            "authors on request.",
        ),
    ],
    ROOT / "paper/manuscript_tr/main.tex": [
        (
            "Kabul sonrasında analiz hattını, bu makaledeki her tabloyu ve şekli üreten betikleri, örnek bazında "
            "değerlendirme kayıtlarını, sabit doğrulama bölmesi indekslerini ve tohum listelerini yayımlayacağız; "
            "bunlar burada raporlanan her sayıyı yeniden üretmeye yetmektedir, çünkü dört koşullama protokolünün "
            "tamamı örnek bazındaki kayıtlardan hesaplanmaktadır ve protokol karşılaştırması yeniden eğitim "
            "gerektirmeden tekrarlanabilmektedir. Bu arşivin anonimleştirilmiş bir kopyası, inceleme sırasında "
            "hakemlerin erişimine \\texttt{[ANONYMOUS-ARCHIVE-URL]} adresinde açıktır; böylece protokol "
            "karşılaştırması kabulden sonra değil, kabulden önce denetlenebilir. Eğitilmiş kontrol noktaları "
            "yaklaşık $40$~GB tutmaktadır ve yazarlardan istek üzerine sağlanmaktadır.",
            "Analiz hattı, bu makaledeki her tabloyu ve şekli üreten betikler, örnek bazında değerlendirme "
            "kayıtları, sabit doğrulama bölmesi indeksleri ve tohum listeleri \\texttt{" + URL + "} adresinde "
            "herkese açıktır; bunlar burada raporlanan her sayıyı yeniden üretmeye yeter, çünkü dört koşullama "
            "protokolünün tamamı örnek bazındaki kayıtlardan hesaplanır ve protokol karşılaştırması yeniden eğitim "
            "gerektirmeden tekrarlanabilir. Eğitilmiş kontrol noktaları yaklaşık $40$~GB tutar ve yazarlardan "
            "istek üzerine sağlanır.",
        ),
    ],
    ROOT / "paper/manuscript/sections/06_conclusion.tex": [
        (
            "The pipeline, the per-sample logs and the analysis scripts will be released on acceptance so that the "
            "protocol comparison can be reproduced and extended.",
            "The pipeline, the per-sample logs and the analysis scripts are publicly available, so the protocol "
            "comparison can be reproduced and extended.",
        ),
    ],
    ROOT / "paper/manuscript_tr/sections/06_sonuc.tex": [
        (
            "Protokol karşılaştırmasının yeniden üretilip genişletilebilmesi için tam boru hattı, örnek bazında "
            "kayıtlar ve analiz betikleri kabul sonrasında yayımlanacaktır.",
            "Tam boru hattı, örnek bazında kayıtlar ve analiz betikleri herkese açık olduğundan protokol "
            "karşılaştırması yeniden üretilebilir ve genişletilebilir.",
        ),
    ],
    ROOT / "paper/submission/declarations.txt": [
        ("Date: 2026-08-25 (revised)", "Date: 2026-10-02 (revised)"),
        (
            "Upon acceptance we will publish the analysis pipeline, the scripts that\n"
            "generate every table and figure in the manuscript, the per-sample evaluation\n"
            "records, the fixed validation-split indices and the seed lists. These\n"
            "together reproduce every number reported in the paper: all four conditioning\n"
            "protocols are computed from the per-sample records, so the protocol\n"
            "comparison can be repeated without retraining. Trained checkpoints total\n"
            "about 40 GB and are available from the authors on reasonable request.",
            "The analysis pipeline, the scripts that generate every table and figure in\n"
            "the manuscript, the per-sample evaluation records, the fixed\n"
            "validation-split indices and the seed lists are publicly available at\n"
            + URL + "\n"
            "(MIT license for the code, CC BY 4.0 for the records). Together they\n"
            "reproduce every number reported in the paper: all four conditioning\n"
            "protocols are computed from the per-sample records, so the protocol\n"
            "comparison can be repeated without retraining. Trained checkpoints total\n"
            "about 40 GB and are available from the authors on reasonable request.",
        ),
        (
            "[TO BE CONFIRMED BY AUTHORS]\n"
            "Option A: \"This research received no specific grant from any funding agency\n"
            "in the public, commercial, or not-for-profit sectors.\"\n"
            "Option B: \"This work was supported by [Agency] under Grant [Number].\"",
            "This research received no specific grant from any funding agency in the\n"
            "public, commercial, or not-for-profit sectors.",
        ),
    ],
    ROOT / "paper/submission/cover_letter.tex": [
        (
            "\\item Upon acceptance we will publish the analysis pipeline, the scripts that generate every table and "
            "figure, the per-sample evaluation records, the fixed validation-split indices, and the seed lists. "
            "Trained checkpoints total about $36$~GB and are available from the authors on request.",
            "\\item The analysis pipeline, the scripts that generate every table and figure, the per-sample "
            "evaluation records, the fixed validation-split indices, and the seed lists are publicly available at "
            "\\texttt{" + URL + "}. Trained checkpoints total about $40$~GB and are available from the authors on "
            "request.",
        ),
    ],
    ROOT / "paper/submission/pre_submission_checklist.md": [
        (
            "### Code Availability Statement\n"
            "**Status:** Needs to be added\n"
            "**Recommended text:**\n"
            "> The source code and trained models used in this study will be made publicly available upon "
            "acceptance of the manuscript.",
            "### Code Availability Statement\n"
            "**Status:** Done (2026-10-02). Public repository " + URL + " (analysis pipeline, per-sample records, "
            "split indices, seed lists, verification scripts; checkpoints on request). Built by "
            "`scripts/acik_depo_kur.sh`; reference sheet regenerates byte-identically from the records.\n"
            "**Text in the manuscript:** present tense and the same scope in main.tex (Data and Code "
            "Availability), Section 6, the Turkish mirror, declarations.txt and the cover letter.",
        ),
    ],
}


def main():
    hata = 0
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
    print("\nAcik depo metin yamalari tamam.")


if __name__ == "__main__":
    main()
