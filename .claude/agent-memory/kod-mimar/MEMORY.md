# kod-mimar bellegi (adeb_sci_1)

## Ortam tuzaklari
- Git Bash'ten `wsl.exe -d Ubuntu-22.04 -- bash -lc "..."`: komut once WSL varsayilan kabugundan (zsh) gecer,
  `$DEGISKEN` erken genisler ve bos kalir; yollar da MSYS donusumune ugrar. Calisan yol: betigi Write ile
  scratchpad'e yaz, `MSYS_NO_PATHCONV=1 wsl.exe -d Ubuntu-22.04 -- bash /mnt/c/.../betik.sh`.
- Konteyner `adeb_eval` root yazar: konteynerde uretilen sekil/kanit dosyalari icin
  `docker exec adeb_eval chown 1000:1000 <yol>`. Ustune yazilan mevcut dosya sahipligini korur (foy firat kaldi).
- WSL host python3'te numpy yok; kapi betikleri konteynerde kosar.

## Foy (results/C1_REFERANS_FOYU.md)
- `build_reference_sheet.py` deterministik: degistirmeden kosunca sha ayni (57e9659e... 31.10 sabah).
- Yeni bolum 'Sabit dizgeler'den once eklenirse onceki satir numaralari kaymaz; 'Sabit dizgeler'
  tablosundaki betik satir no'lari `_satir()` ile ilk eslesmeden bulunur, yeni kod sonra geldigi icin degismez.
- 31.10.2026: M10.7 eklendi (saldiri tohumu SD'si c1_statval; CIFAR-100 C3 hedef hatalari c3_precision).
  Yeni sha 21b2597a...; M10.7 (satir 2042-2067) cikarilinca 57e9659e geri gelir.

## Kapi tasarimi (verify_manuscript_numbers.py, 31.10.2026)
- Tasiyicilar metnin `% FOY:<bolum>:<satir>` yorumlarindan turetilir (A1 grup kapsamasi, A2 foyde yok,
  A3 atif eksik), B = JSON'dan ana manset, C = eski liste yalniz bilgi. Oz-sinama:
  `scripts/test_verify_manuscript_numbers.py` (bes bozma; `--en-dizin` ile gecici kopya).
- kapilar.sh ozet satirinda `grep -m1 'SONUC\|KALDI'` kullanir: bilgi satirlarina "KALDI" kelimesi yazma.
