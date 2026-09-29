#!/usr/bin/env python3
"""PDF'in ILK SAYFASINDA ozet ve anahtar kelimeler var mi?
Kapilar .tex okuyor; bu, RENDER'i denetler."""
import fitz

d = fitz.open("/workspace/paper/manuscript/main.pdf")
s1 = d[0].get_text()
tum = "".join(p.get_text() for p in d)
for etiket, parca in (("ozet ilk cumlesi (s.1)", "Comparisons of adversarial robustness across architecture families"),
                      ("INDEX TERMS (s.1)", "INDEX TERMS"),
                      ("ABSTRACT basligi (s.1)", "ABSTRACT")):
    print(f"{etiket:28s}: {'VAR' if parca in s1 else 'YOK'}")
print(f"{'ozet TUM belgede':28s}: {'VAR' if 'Comparisons of adversarial robustness across' in tum else 'YOK'}")
print(f"{'INDEX TERMS TUM belgede':28s}: {'VAR' if 'INDEX TERMS' in tum else 'YOK'}")
print(f"{'VOLUME 11, 2023 altbilgi':28s}: {'VAR' if 'VOLUME 11, 2023' in s1 else 'YOK'}")
