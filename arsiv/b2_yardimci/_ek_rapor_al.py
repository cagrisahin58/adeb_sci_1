# Salt okur: bir JSON dosyasindan verilen anahtar yollarinin degerlerini basar.
# Kullanim: python3 -I _ek_rapor_al.py <dosya> <yol1> [yol2 ...]   (yol: a.b.c, liste indeksi sayi)
# Anahtar adinda nokta varsa yol parcasi ~ ile ayrilabilir: a~b.c~d (bu durumda ~ ayirici olur).
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
with open(sys.argv[1], encoding="utf-8") as f:
    kok = json.load(f)
for yol in sys.argv[2:]:
    parcalar = yol.split("~") if "~" in yol else yol.split(".")
    o = kok
    try:
        for p in parcalar:
            if isinstance(o, list):
                o = o[int(p)]
            else:
                o = o[p]
        print(f"{yol} = {json.dumps(o, ensure_ascii=False)[:600]}")
    except (KeyError, IndexError, ValueError, TypeError) as e:
        print(f"{yol} = BULUNAMADI ({type(e).__name__}: {e})")
