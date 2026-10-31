import re, sys
sys.stdout.reconfigure(encoding="utf-8")
# kullanim: _mk_bt_baglam.py dosya satir1,satir2 desen
f, sat, desen = sys.argv[1], sys.argv[2], sys.argv[3]
ls = open(f, encoding="utf-8").read().split("\n")
for n in map(int, sat.split(",")):
    l = ls[n - 1]
    for m in re.finditer(desen, l):
        print(n, "...", l[max(0, m.start() - 90):m.end() + 50].replace("\n", " "))
