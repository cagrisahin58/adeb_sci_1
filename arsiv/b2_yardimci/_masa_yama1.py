# -*- coding: utf-8 -*-
"""Tek seferlik yama (31.10.2026): _masa_sapma_notu.py metin eklerini duzeltir ve bu oturumda ONKAYIT_SAPMALAR.md
sonuna eklenen iki basligi (henuz hicbir S10-3 kosusu yapilmadan) kaldirir; onekin ozgun sha256 ile ayni oldugunu denetler."""
import hashlib
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(__file__).resolve().parents[2]
p = KOK / "arsiv/b2_yardimci/_masa_sapma_notu.py"
s = io.open(p, encoding="utf-8").read()
rep = [
    ('''def pe(x):
    m, e = f"{float(x):.1e}".split("e")
    return f"{m.replace('.', ',')}×10^{int(e)}"''',
     '''def pe(x):
    if float(x) == 0.0:
        return "0"
    m, e = f"{float(x):.1e}".split("e")
    ust = str(int(e)).translate(str.maketrans("-0123456789", "\\u207b\\u2070\\u00b9\\u00b2\\u00b3\\u2074\\u2075\\u2076\\u2077\\u2078\\u2079"))
    return f"{m.replace('.', ',')}×10{ust}"


def kp(a, nd=3):
    return f"[{tr(a[0], nd)}; {tr(a[1], nd)}]"'''),
    ('''        return (f"{ad}'da ({j['meta']['blok']}) ortalama q'nun hiyerarşik bootstrap %90 aralığı {ar(ka['bootstrap']['ci90'])}, "
                f"%95 aralığı {ar(ka['bootstrap']['ci95'])}'tür (birincil t aralıkları %90 {ar(ka['t_ci90'])}, %95 "
                f"{ar(ka['t_ci95'])}); ortalama ρ(V-scr) için bootstrap %90 aralığı {ar(kb['bootstrap']['ci90'])}, %95 aralığı "
                f"{ar(kb['bootstrap']['ci95'])}'tür (birincil t aralıkları %90 {ar(kb['t_ci90'])}, %95 {ar(kb['t_ci95'])}); "
                f"bootstrap TOST p'si {pe(kb['bootstrap']['tost_p'])}, t TOST p'si {pe(kb['t_tost_p'])}'dir "''',
     '''        return (f"{ad} ({j['meta']['blok']}) ortalama q'nun hiyerarşik bootstrap aralıkları %90 {kp(ka['bootstrap']['ci90'])} "
                f"ve %95 {kp(ka['bootstrap']['ci95'])} olarak bulunmuştur (birincil t aralıkları %90 {kp(ka['t_ci90'])}, %95 "
                f"{kp(ka['t_ci95'])}); ortalama ρ(V-scr) için bootstrap aralıkları %90 {kp(kb['bootstrap']['ci90'])} ve %95 "
                f"{kp(kb['bootstrap']['ci95'])}, birincil t aralıkları %90 {kp(kb['t_ci90'])} ve %95 {kp(kb['t_ci95'])}, "
                f"bootstrap TOST p'si {pe(kb['bootstrap']['tost_p'])}, t TOST p'si ise {pe(kb['t_tost_p'])} olarak bulunmuştur "'''),
    ('''{blok('cifar10', 'CIFAR-10')} {blok('cifar100', 'CIFAR-100')}''',
     '''{blok('cifar10', "CIFAR-10'da")} {blok('cifar100', "CIFAR-100'de")}'''),
    ('''aynıdır, en büyük mutlak fark "
        f"{nf:.1e}'dir (`dogrulama''',
     '''aynıdır; en büyük mutlak fark "
        f"{pe(nf)} olarak hesaplanmıştır (`dogrulama'''),
    ('''(en büyük fark {kcf:.1e}; "''', '''(en büyük fark {pe(kcf)}; "'''),
    ('''        parca.append(f"{ad[v]}'da {tr(d['S10_3']['istatistik'])} (tek yönlü p''',
     '''        parca.append(f"{ad[v]} {tr(d['S10_3']['istatistik'])} (tek yönlü p'''),
    ('''    ad = {"cifar10": "CIFAR-10", "cifar100": "CIFAR-100", "imagenetv2": "ImageNetV2"}''',
     '''    ad = {"cifar10": "CIFAR-10'da", "cifar100": "CIFAR-100'de", "imagenetv2": "ImageNetV2'de"}'''),
    ('''(en büyük mutlak fark {mf:.1e}; `yeniden''', '''(en büyük mutlak fark {pe(mf)}; `yeniden'''),
    ('''{str(M['yeniden_uretim_hepsi_esit_1e-6']).lower()}). S10-3 istatistiği " + "; ".join(parca)
        + f"'dir (`veri.<veri>.S10_3`''',
     '''{str(M['yeniden_uretim_hepsi_esit_1e-6']).lower()}). S10-3 istatistiği " + ", ".join(parca)
        + f" olarak bulunmuştur (`veri.<veri>.S10_3`'''),
]
for o, n in rep:
    if s.count(o) != 1:
        raise SystemExit("yama bulunamadi: " + o[:90])
    s = s.replace(o, n)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
sp = KOK / "results/q1_research/ONKAYIT_SAPMALAR.md"
b = sp.read_bytes()
i = b.find("\n### 31.10.2026, ana ön kayıt §7: hiyerarşik bootstrap".encode("utf-8"))
on = b[:i]
h = hashlib.sha256(on).hexdigest()
print("onek sha256:", h)
if h != "06ac9ff351aaaec729d5cc5c5cbf6ae857078c169ecb1fce92d4fb705504fe3a":
    raise SystemExit("onek ozgun dosyayla ayni degil; dokunulmadi")
sp.write_bytes(on)
print("eklenen iki baslik kaldirildi; dosya ozgun haline dondu")
