"""Butunlestirici yazar: tam eslesmeli metin degisiklikleri. Kullanim:
python3 _mk_bt_duzelt.py <degisiklik_dosyasi.py>
Degisiklik dosyasi DEGISIKLIKLER = [(dosya, eski, yeni), ...] tanimlar.
Her eski dizge dosyada tam bir kez gecmelidir; yoksa hicbir sey yazilmaz."""
import io, sys, runpy
sys.stdout.reconfigure(encoding="utf-8")
kok = "/home/firat/projects/adeb_sci_1/paper/manuscript/"
d = runpy.run_path(sys.argv[1])["DEGISIKLIKLER"]
icerik = {}
hata = False
for f, eski, yeni in d:
    if f not in icerik:
        icerik[f] = io.open(kok + f, encoding="utf-8").read()
    n = icerik[f].count(eski)
    if n != 1:
        print("HATA", f, n, repr(eski[:80]))
        hata = True
        continue
    icerik[f] = icerik[f].replace(eski, yeni)
if hata:
    sys.exit(1)
for f, t in icerik.items():
    io.open(kok + f, "w", encoding="utf-8", newline="\n").write(t)
    print("yazildi", f)
