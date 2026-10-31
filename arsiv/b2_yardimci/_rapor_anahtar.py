import json, sys
sys.stdout.reconfigure(encoding="utf-8")

def gez(o, yol, derinlik, maxd, maxliste=6):
    if derinlik > maxd:
        return
    if isinstance(o, dict):
        for k, v in o.items():
            p = f"{yol}.{k}" if yol else str(k)
            if isinstance(v, (dict, list)):
                tur = "dict" if isinstance(v, dict) else f"list[{len(v)}]"
                print(f"{'  '*derinlik}{p}  <{tur}>")
                gez(v, p, derinlik + 1, maxd, maxliste)
            else:
                s = repr(v)
                if len(s) > 120:
                    s = s[:120] + "..."
                print(f"{'  '*derinlik}{p} = {s}")
    elif isinstance(o, list):
        if all(not isinstance(x, (dict, list)) for x in o):
            s = repr(o)
            if len(s) > 160:
                s = s[:160] + "..."
            print(f"{'  '*derinlik}{yol} = {s}")
        else:
            for i, v in enumerate(o[:maxliste]):
                gez(v, f"{yol}[{i}]", derinlik + 1, maxd, maxliste)

dosya = sys.argv[1]
maxd = int(sys.argv[2]) if len(sys.argv) > 2 else 3
onek = sys.argv[3] if len(sys.argv) > 3 else ""
d = json.load(open(dosya, encoding="utf-8"))
if onek:
    for k in onek.split("."):
        if isinstance(d, list):
            d = d[int(k)]
        else:
            d = d[k]
gez(d, onek, 0, maxd)
