import re, sys
from pathlib import Path
K = Path("/home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29")
for ad in ("ON_KAYIT_EK_B8_B10_2026-10-30.md", "08_ek_kod_raporu.md"):
    t = (K / ad).read_text(encoding="utf-8")
    sat = t.splitlines()
    print("==", ad, len(sat), "satir")
    print(" uzun tire U+2014:", t.count("\u2014"), " en tire U+2013:", t.count("\u2013"), " ' - ' tire-bosluk:", len(re.findall(r"\S - \S", t)))
    kalin_bas = [i + 1 for i, l in enumerate(sat) if re.match(r"^\s*(\*\*|__)[^*_]{1,40}(\*\*|__)", l)]
    ital_bas = [i + 1 for i, l in enumerate(sat) if re.match(r"^\s*\*[^*\s][^*]{0,30}\*[\s.:]", l)]
    print(" paragraf basi koyu:", kalin_bas[:10], " italik:", ital_bas[:10])
    print(" toplam ** sayisi:", t.count("**"))
    # birinci tekil/cogul kisi
    kisi = re.findall(r"\b\w+(?:dım|dim|dum|düm|tım|tim|tum|tüm|ıyorum|iyorum|uyorum|üyorum|acağım|eceğim|ırım|irim|urum|ürüm|arım|erim)\b", t)
    kisi2 = re.findall(r"\b(?:ben|bence|benim|bana|biz|bizim|bize|bizce)\b", t, flags=re.I)
    kisi3 = re.findall(r"\b\w+(?:dık|dik|duk|dük|tık|tik|tuk|tük|ıyoruz|iyoruz|uyoruz|üyoruz|acağız|eceğiz|alım|elim)\b", t)
    print(" 1. tekil adaylar:", sorted(set(kisi))[:30])
    print(" zamir:", sorted(set(kisi2)))
    print(" 1. cogul adaylar:", sorted(set(kisi3))[:30])
    madde = sum(1 for l in sat if re.match(r"^\s*[-*] ", l))
    print(" madde satiri:", madde, " 'Etiket:' maddesi:", sum(1 for l in sat if re.match(r"^\s*[-*] [^:]{1,30}: ", l)))
