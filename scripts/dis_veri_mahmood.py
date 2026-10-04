"""Mahmood, Mahmood, van Dijk (ICCV 2021, arXiv 2104.02610) PDF'inden Tablo 1 (temiz dogruluk) ve
Tablo 2 (CIFAR-10 transfer matrisi) metnini cikarir; sayilar ELLE DEGIL bu metinden okunacak.
Konteynerde: docker exec -w /workspace adeb_eval python scripts/dis_veri_mahmood.py
Girdi: results/q1/dis_veri/mahmood2021.pdf (curl ile indirilir). Cikti: results/q1/dis_veri/mahmood2021_metin.txt
"""
import re
import sys

import fitz  # type: ignore

src = "results/q1/dis_veri/mahmood2021.pdf"
out = "results/q1/dis_veri/mahmood2021_metin.txt"
doc = fitz.open(src)
with open(out, "w", encoding="utf-8") as fh:
    for i, page in enumerate(doc, 1):
        t = page.get_text("text")
        fh.write(f"\n===== SAYFA {i} =====\n{t}")
        if re.search(r"Table\s*[12]\b", t):
            print(f"--- sayfa {i} (Table 1/2 gecen) ---")
            # tablo cevresini bas
            for m in re.finditer(r"Table\s*[12][.:]", t):
                s = max(0, m.start() - 1500)
                print(t[s:m.end() + 2500].replace("\n", " | ")[:4200])
                print("....")
print("yazildi:", out, "sayfa:", len(doc))
