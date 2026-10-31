"""09_sonuc_b2_b6 raporu icin salt okur yardimci: B4 kosegeni, 46,40 cakismasi, cokus dosyalari.
Hicbir dosya yazmaz. Depo kokunden: python3 -I arsiv/b2_yardimci/_rapor_kosegen.py
"""
import glob
import hashlib
import json
import os
import re
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
M = "results/q1/konsey_b4_matris"


def yukle(src, tgt):
    return np.load(f"{M}/per_sample_{src}_to_{tgt}.npz")


z = yukle("R224_IN_s1301", "R224_IN_s1301")
print("npz anahtarlari:", list(z.keys()))
for k in z.keys():
    print("  ", k, z[k].shape, z[k].dtype)

yeni = ["V_IN_s2101", "V_IN_s2102", "R224_IN_s1301", "R224_IN_s1302", "R224_scr_s1201", "R224_scr_s1202"]
c1 = ["ResNet18_AT_s1001", "ResNet18_AT_s1002", "ResNet18_AT_s1003", "ViT_Tiny_AT_s2001", "ViT_Tiny_AT_s2002", "ViT_Tiny_AT_s2003"]

tm = json.load(open(f"{M}/transfer_matrix.json"))
print("transfer_matrix.json anahtarlari:", list(tm.keys())[:20])

print("\n== Kosegen (beyaz kutu), n=10000 ve ilk 1000")
kos = {}
for m in yeni + c1:
    d = yukle(m, m)
    cc = d["target_clean_correct"].astype(bool) if "target_clean_correct" in d else None
    aw = d["target_adv_wrong"].astype(bool)
    n = aw.shape[0]
    temiz = cc.mean() * 100
    pgd_dogru = (cc & ~aw).mean() * 100
    w = (aw & cc).sum() / cc.sum() * 100
    cc1, aw1 = cc[:1000], aw[:1000]
    pgd1 = (cc1 & ~aw1).mean() * 100
    kos[m] = dict(n=n, temiz=temiz, pgd_dogru=pgd_dogru, w=w, pgd1=pgd1, dogru_say=int((cc & ~aw).sum()))
    print(f"{m}: n={n} temiz={temiz:.2f} pgd10_dogru={pgd_dogru:.2f} ({int((cc & ~aw).sum())}/{n}) w(hedef-dogru)={w:.4f} ilk1000_pgd10_dogru={pgd1:.1f}")

print("\n== 46,40 cakismasi: R224_IN_s1301 ile R224_scr_s1201")
a = yukle("R224_IN_s1301", "R224_IN_s1301")
b = yukle("R224_scr_s1201", "R224_scr_s1201")
ra = a["target_clean_correct"].astype(bool) & ~a["target_adv_wrong"].astype(bool)
rb = b["target_clean_correct"].astype(bool) & ~b["target_adv_wrong"].astype(bool)
print("test kumesinde PGD-10 dogru sayisi:", int(ra.sum()), int(rb.sum()))
print("ikisinde de dogru:", int((ra & rb).sum()), "yalniz IN:", int((ra & ~rb).sum()), "yalniz scr:", int((~ra & rb).sum()))
print("ornek bazinda uyusma orani:", float((ra == rb).mean()))
ca = a["target_clean_correct"].astype(bool)
cb = b["target_clean_correct"].astype(bool)
print("temiz dogru sayisi:", int(ca.sum()), int(cb.sum()), "temiz uyusma:", float((ca == cb).mean()))
# capraz transfer
for s, t in [("R224_IN_s1301", "R224_scr_s1201"), ("R224_scr_s1201", "R224_IN_s1301")]:
    d = yukle(s, t)
    cc = d["target_clean_correct"].astype(bool)
    aw = d["target_adv_wrong"].astype(bool)
    print(f"T({s}->{t}) hedef-dogru = {(aw & cc).sum() / cc.sum() * 100:.4f}")

print("\n== Kontrol noktasi ozetleri")
for m, alt in [("R224_IN_s1301", "resnet18_224_in1k"), ("R224_scr_s1201", "resnet18_224"), ("R224_IN_s1302", "resnet18_224_in1k"), ("R224_scr_s1202", "resnet18_224")]:
    p = f"models/q1/konsey/{m}/{alt}/adv/adversarial_training/best.pth"
    if os.path.exists(p):
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        print(m, p, os.path.getsize(p), h[:16])
    else:
        print(m, "YOK", p)

print("\n== AT gunlukleri: val PGD satirlari (son 6 ve en iyi)")
for m in yeni:
    f = f"logs/konsey_b3/{m}_AT.log"
    if not os.path.exists(f):
        print(m, "gunluk yok"); continue
    satirlar = open(f, encoding="utf-8", errors="replace").read().splitlines()
    eslesen = [s for s in satirlar if re.search(r"(?i)val.*pgd|pgd.*val|robust", s)]
    print(f"-- {m}: {len(satirlar)} satir, val/pgd iceren {len(eslesen)}")
    for s in eslesen[:3]:
        print("   ", s[:220])
    print("   ...")
    for s in eslesen[-4:]:
        print("   ", s[:220])

print("\n== Cokus dosyalari")
for f in sorted(glob.glob("logs/konsey_b3/*cokus.txt")):
    print("--", f)
    print(open(f, encoding="utf-8", errors="replace").read()[:600])
