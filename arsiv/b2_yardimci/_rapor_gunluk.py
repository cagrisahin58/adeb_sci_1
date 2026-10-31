"""09_sonuc_b2_b6 raporu icin salt okur yardimci: B3 AT ve temiz gunluklerinden satir numarali ozet."""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
yeni = ["V_IN_s2101", "V_IN_s2102", "R224_IN_s1301", "R224_IN_s1302", "R224_scr_s1201", "R224_scr_s1202"]
for m in yeni:
    f = f"logs/konsey_b3/{m}_AT.log"
    sat = open(f, encoding="utf-8", errors="replace").read().splitlines()
    ep = [(i + 1, s) for i, s in enumerate(sat) if re.match(r"^Epoch \d+/100 - ", s)]
    best = [(i + 1, sat[i - 1]) for i, s in enumerate(sat) if "Best model saved" in s]
    print(f"== {m} AT: epok satiri {len(ep)}")
    for no, s in ep:
        e = int(re.match(r"^Epoch (\d+)/", s).group(1))
        if e in (1, 5):
            print(f"   satir {no}: {s}")
    if best:
        print(f"   son 'Best model saved' oncesi satir {best[-1][0] - 1}: {best[-1][1]}")
    print(f"   son epok satir {ep[-1][0]}: {ep[-1][1]}")
    for i, s in enumerate(sat):
        if s.startswith("Early stopping") or s.startswith("Training completed") or s.startswith("Best adversarial accuracy"):
            print(f"   satir {i + 1}: {s}")
            if s.startswith("Best adversarial accuracy"):
                break
    # ilk egitim kaybi satiri
    for i, s in enumerate(sat):
        if "train_loss" in s.lower():
            print(f"   ilk train_loss satiri {i + 1}: {s[:160]}")
            break
    ft = f"logs/konsey_b3/{m}_temiz.log"
    st = open(ft, encoding="utf-8", errors="replace").read().splitlines()
    ept = [(i + 1, s) for i, s in enumerate(st) if re.match(r"^Epoch \d+/\d+", s)]
    print(f"   temiz gunluk: epok satiri {len(ept)}; ilk: {ept[0] if ept else None}")
    if ept:
        print(f"   temiz son: {ept[-1]}")
    for i, s in enumerate(st):
        if "Best" in s and ("acc" in s.lower()):
            pass
    bt = [(i + 1, s) for i, s in enumerate(st) if re.search(r"(?i)best (val|test|clean)?.*acc", s)]
    if bt:
        print(f"   temiz 'best' son satir {bt[-1][0]}: {bt[-1][1][:160]}")
