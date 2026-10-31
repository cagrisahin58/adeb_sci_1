# Salt okur: bir JSON dosyasinin anahtar agacini (derinlik sinirli) ve kisa degerlerini basar.
# Kullanim: python3 -I _ek_rapor_anahtar.py <dosya> [derinlik=4] [kok.anahtar.yolu] [listeden_en_cok=8]
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")


def bas(o, yol, d, dmax, lmax):
    if isinstance(o, dict):
        if d >= dmax:
            print(f"{yol}: dict({len(o)}) anahtarlar={list(o)[:12]}")
            return
        for k, v in o.items():
            bas(v, f"{yol}.{k}" if yol else str(k), d + 1, dmax, lmax)
    elif isinstance(o, list):
        if all(not isinstance(x, (dict, list)) for x in o):
            s = json.dumps(o if len(o) <= lmax else o[:lmax], ensure_ascii=False)
            print(f"{yol}: list({len(o)}) {s[:400]}")
        else:
            if d >= dmax:
                print(f"{yol}: list({len(o)}) of {type(o[0]).__name__}")
                return
            for i, x in enumerate(o[:lmax]):
                bas(x, f"{yol}[{i}]", d + 1, dmax, lmax)
            if len(o) > lmax:
                print(f"{yol}: ... toplam {len(o)}")
    else:
        s = json.dumps(o, ensure_ascii=False)
        print(f"{yol}: {s[:300]}")


dosya = sys.argv[1]
dmax = int(sys.argv[2]) if len(sys.argv) > 2 else 4
kok = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "-" else ""
lmax = int(sys.argv[4]) if len(sys.argv) > 4 else 8
with open(dosya, encoding="utf-8") as f:
    o = json.load(f)
if kok:
    for p in kok.split("."):
        if isinstance(o, list):
            o = o[int(p)]
        else:
            o = o[p]
bas(o, kok, 0, dmax, lmax)
