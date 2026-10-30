# -*- coding: utf-8 -*-
"""Ek bloklar (B8 ImageNetV2 paneli, B9 CIFAR-100 paneli) icin indirme betigi (30.10.2026).

YALNIZ WSL tarafinda, standart kutuphaneyle (python3 -I, numpy/requests/gdown gerekmez) calisir;
konteyner /mnt/d'yi zincir bitip yeniden kurulana kadar gormez (07_disk_D_plani.md §4).

Ne yapar:
  1. Her oge icin HTTP HEAD ile boyutu olcer (--olc yalniz bunu yapar).
  2. Ogeyi /mnt/d/adeb_sci_1_veri/<goreli yol> altina .part adiyla indirir, boyutu HEAD ile karsilastirir,
     sha256'sini hesaplar, /mnt/d/adeb_sci_1_veri/indirme_sha256.txt dosyasina ekler
     (sha256sum -c uyumlu, yollar D kokune goreli) ve kaydi _indirme/indirmeler.json'a yazar.
  3. Depoda ayni goreli yola mutlak sembolik bag koyar (models/robustbench_zoo/<ds>/Linf/<ad>.pt,
     data/imagenetv2). Depoda ayni adla gercek dosya varsa dokunmaz, raporlar.
  4. ImageNetV2 arsivini once Hugging Face'in X-Linked-Etag (LFS sha256) degeriyle dogrular, sonra
     kendi bos klasorune (data/imagenetv2) guvenli suzgecle acar ve sinif klasoru sayimini
     _indirme/imagenetv2_sayim.json'a yazar.

Google Drive: drive.usercontent.google.com/download?id=..&export=download&confirm=t (RobustBench'in
gdown ile kullandigi kimlikler; kimlikler konteynerdeki robustbench.model_zoo.model_dicts'ten okunmustur).
HTML (kota ya da onay sayfasi) donerse sayfadaki gizli alanlarla bir kez daha, sonra drive.google.com/uc
yedek adresiyle denenir; hepsi basarisizsa oge 'BASARISIZ' olarak elle indirme baglantisiyla listelenir.

Kullanim (WSL, depo kokunden; uzun surer, arka planda):
  python3 -I scripts/ek_indir.py --olc
  setsid nohup python3 -I scripts/ek_indir.py --grup hepsi > /mnt/d/adeb_sci_1_veri/_indirme/calisma.log 2>&1 &
  python3 -I scripts/ek_indir.py --durum
"""
import argparse
import hashlib
import html.parser
import json
import os
import sys
import tarfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

D_KOK = Path("/mnt/d/adeb_sci_1_veri")
DEPO = Path(__file__).resolve().parents[1]
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0 Safari/537.36")

HF_V2 = ("https://huggingface.co/datasets/vaishaal/ImageNetV2/resolve/main/"
         "imagenetv2-matched-frequency.tar.gz")
GH_REL = "https://github.com/RobustBench/robustbench/releases/download/v1.1/"

# (grup, ad, kaynak turu, kimlik/url, D'ye goreli hedef, depoda bag yolu (goreli) ya da None, rol)
# gdrive kimlikleri: robustbench.model_zoo.model_dicts (adeb_eval konteyneri, 30.10.2026 okumasi)
IN = "models/robustbench_zoo/imagenet/Linf/"
C100 = "models/robustbench_zoo/cifar100/Linf/"
OGELER = [
    ("imagenetv2", "ImageNetV2-MatchedFrequency", "url", HF_V2,
     "_indirme/arsiv/imagenetv2-matched-frequency.tar.gz", None, "B8 verisi"),
    # B8: once ayni tarifli ciftler, sonra panel, sonra yedek
    ("in", "Singh2023Revisiting_ConvNeXt-T-ConvStem", "gdrive", "1-FjtOF6LJ3-bf4VezsmWwncCxYSx-USP", IN + "Singh2023Revisiting_ConvNeXt-T-ConvStem.pt", IN + "Singh2023Revisiting_ConvNeXt-T-ConvStem.pt", "cift 1 CNN"),
    ("in", "Singh2023Revisiting_ViT-S-ConvStem", "gdrive", "1-1sUYXnj6bDXacIKI3KKqn4rlkmL-ZI2", IN + "Singh2023Revisiting_ViT-S-ConvStem.pt", IN + "Singh2023Revisiting_ViT-S-ConvStem.pt", "cift 1 ViT"),
    ("in", "Singh2023Revisiting_ConvNeXt-B-ConvStem", "gdrive", "1-lE-waaVvfL7lgBrydmZIM9UJimmHnVe", IN + "Singh2023Revisiting_ConvNeXt-B-ConvStem.pt", IN + "Singh2023Revisiting_ConvNeXt-B-ConvStem.pt", "cift 2 CNN"),
    ("in", "Singh2023Revisiting_ViT-B-ConvStem", "gdrive", "1-JBbfi_eH3tKMXObvPPHprrZae0RiQGT", IN + "Singh2023Revisiting_ViT-B-ConvStem.pt", IN + "Singh2023Revisiting_ViT-B-ConvStem.pt", "cift 2 ViT"),
    ("in", "Liu2023Comprehensive_ConvNeXt-B", "gdrive", "10-nSm-qUftvfKXHeOAakBQl8rxm-jCbk", IN + "Liu2023Comprehensive_ConvNeXt-B.pt", IN + "Liu2023Comprehensive_ConvNeXt-B.pt", "cift 3 CNN"),
    ("in", "Liu2023Comprehensive_Swin-B", "gdrive", "1-4mtxQCkThJUVdS3wvQ6NnmMZuySqR3c", IN + "Liu2023Comprehensive_Swin-B.pt", IN + "Liu2023Comprehensive_Swin-B.pt", "cift 3 donusturucu"),
    ("in", "Mo2022When_ViT-B", "gdrive", "1-dUFdvDBflqMsMLjZv3wlPJTm-Jm7net", IN + "Mo2022When_ViT-B.pt", IN + "Mo2022When_ViT-B.pt", "ciftsiz duz ViT"),
    ("in", "Salman2020Do_R18", "gdrive", "1OThCOQCOxY6lAgxZxgiK3YuZDD7PPfPx", IN + "Salman2020Do_R18.pt", IN + "Salman2020Do_R18.pt", "panel P8"),
    ("in", "Salman2020Do_R50", "gdrive", "1TmT5oGa1UvVjM3d-XeSj_XmKqBNRUg8r", IN + "Salman2020Do_R50.pt", IN + "Salman2020Do_R50.pt", "panel P8"),
    ("in", "Salman2020Do_50_2", "gdrive", "1OT7xaQYljrTr3vGbM37xK9SPoPJvbSKB", IN + "Salman2020Do_50_2.pt", IN + "Salman2020Do_50_2.pt", "panel P8"),
    ("in", "Engstrom2019Robustness", "gdrive", "1T2Fvi1eCJTeAOEzrH_4TAIwO8HTOYVyn", IN + "Engstrom2019Robustness.pt", IN + "Engstrom2019Robustness.pt", "panel P8"),
    ("in", "Chen2024Data_WRN_50_2", "gdrive", "1-PBlZVILAKFQ7mF8srKjdkTKJZAr61Uf", IN + "Chen2024Data_WRN_50_2.pt", IN + "Chen2024Data_WRN_50_2.pt", "panel P8"),
    ("in", "Peng2023Robust", "gdrive", "1-GpZ9Du83mBTN61Ytx9z_ZQSyIc1kYop", IN + "Peng2023Robust.pt", IN + "Peng2023Robust.pt", "panel P8"),
    ("in", "Debenedetti2022Light_XCiT-S12", "url", GH_REL + "debenedetti2022light-xcit-s-imagenet-linf.pth.tar", IN + "Debenedetti2022Light_XCiT-S12.pth.tar", IN + "Debenedetti2022Light_XCiT-S12.pth.tar", "ikincil panel (timm/GitHub)"),
    ("in", "Wong2020Fast", "gdrive", "1deM2ZNS5tf3S_-eRURJi-IlvUL8WJQ_w", IN + "Wong2020Fast.pt", IN + "Wong2020Fast.pt", "yedek P8 uyesi"),
    # B9: CIFAR-100 paneli (Pang2022Robustness_WRN28_10 depoda zaten var)
    ("c100", "Rice2020Overfitting", "gdrive", "1XXNZn3fZBOkD1aqNL1cvcD8zZDccyAZ6", C100 + "Rice2020Overfitting.pt", C100 + "Rice2020Overfitting.pt", "panel P9"),
    ("c100", "Rade2021Helper_R18_ddpm", "gdrive", "1-qUvfOjq6x4I8mZynfGtzzCH_nvqS_VQ", C100 + "Rade2021Helper_R18_ddpm.pt", C100 + "Rade2021Helper_R18_ddpm.pt", "panel P9"),
    ("c100", "Addepalli2022Efficient_RN18", "gdrive", "1-2hnxC7lZOQDqQbum4yPbtRtTND86I5N", C100 + "Addepalli2022Efficient_RN18.pt", C100 + "Addepalli2022Efficient_RN18.pt", "panel P9"),
    ("c100", "Sehwag2021Proxy", "gdrive", "1ejMNF2O4xkSdrjtZt2UXUeim-y9F7Req", C100 + "Sehwag2021Proxy.pt", C100 + "Sehwag2021Proxy.pt", "panel P9"),
    ("c100", "Wang2023Better_WRN-28-10", "gdrive", "1-jOu3wKWyw0XnBCXDGR32xn8Bw9GTJgh", C100 + "Wang2023Better_WRN-28-10.pt", C100 + "Wang2023Better_WRN-28-10.pt", "panel P9"),
    ("c100", "Jia2022LAS-AT_34_10", "gdrive", "1-338K2PUf5FTwk4cbUUeTNz247GrXaMG", C100 + "Jia2022LAS-AT_34_10.pt", C100 + "Jia2022LAS-AT_34_10.pt", "panel P9"),
    ("c100", "Debenedetti2022Light_XCiT-S12", "url", GH_REL + "debenedetti2022light-xcit-s-cifar100-linf.pth.tar", C100 + "Debenedetti2022Light_XCiT-S12.pth.tar", C100 + "Debenedetti2022Light_XCiT-S12.pth.tar", "ikincil panel (timm/GitHub)"),
    ("c100", "Hendrycks2019Using", "gdrive", "1If3tppQsCe5dN8Vbo9ff0tjlKQTTrShd", C100 + "Hendrycks2019Using.pt", C100 + "Hendrycks2019Using.pt", "ikincil panel"),
    ("c100", "Chen2021LTD_WRN34_10", "gdrive", "1-I4NZyULdEWH46b4EaCTxuuRo4eFXsg_", C100 + "Chen2021LTD_WRN34_10.pt", C100 + "Chen2021LTD_WRN34_10.pt", "yedek P9 uyesi 1"),
    ("c100", "Cui2023Decoupled_WRN-28-10", "gdrive", "15BwWdWbNfoarTEWWugicOVkTjh3nXH36", C100 + "Cui2023Decoupled_WRN-28-10.pt", C100 + "Cui2023Decoupled_WRN-28-10.pt", "yedek P9 uyesi 2"),
]


def simdi():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def gdrive_urls(gid):
    return [f"https://drive.usercontent.google.com/download?id={gid}&export=download&confirm=t",
            f"https://drive.google.com/uc?export=download&id={gid}&confirm=t"]


def ac(url, method="GET", timeout=60):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout)


def head_boyut(url):
    """HEAD (yonlendirmeleri izler). (boyut, icerik turu, ek basliklar) doner."""
    try:
        with ac(url, "HEAD") as r:
            h = {k.lower(): v for k, v in r.headers.items()}
            return int(h.get("content-length", -1)), h.get("content-type", ""), h
    except urllib.error.HTTPError as e:
        return -1, f"HTTP {e.code}", {}
    except Exception as e:  # noqa: BLE001
        return -1, f"HATA {e!r}", {}


def hf_lfs_sha256(url):
    """Hugging Face resolve adresi yonlendirmeden once X-Linked-Etag ile LFS sha256'sini verir."""

    class Dur(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    op = urllib.request.build_opener(Dur)
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        r = op.open(req, timeout=60)
        h = r.headers
    except urllib.error.HTTPError as e:
        h = e.headers
    et = (h.get("X-Linked-Etag") or "").strip('"')
    return et if len(et) == 64 else None


class GizliAlanlar(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.alan, self.eylem = {}, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "form" and a.get("action"):
            self.eylem = a["action"]
        if tag == "input" and a.get("type") == "hidden" and a.get("name"):
            self.alan[a["name"]] = a.get("value", "")


def sha256_dosya(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def indir_url(url, hedef, beklenen, ilerleme):
    """url -> hedef (.part ile). (bayt, icerik turu) doner; HTML donerse ValueError(html)."""
    part = hedef.with_name(hedef.name + ".part")
    t0, son = time.time(), 0.0
    with ac(url, timeout=120) as r:
        ct = r.headers.get("Content-Type", "")
        if ct.startswith("text/html"):
            raise ValueError(r.read(200000).decode("utf-8", "replace"))
        n = 0
        with open(part, "wb") as f:
            while True:
                b = r.read(1 << 20)
                if not b:
                    break
                f.write(b)
                n += len(b)
                if time.time() - son > 15:
                    son = time.time()
                    hiz = n / max(1e-6, son - t0) / 1e6
                    ilerleme(f"{hedef.name}: {n / 1e6:.1f}/{beklenen / 1e6:.1f} MB, {hiz:.1f} MB/s")
    if beklenen > 0 and n != beklenen:
        part.unlink(missing_ok=True)
        raise IOError(f"boyut uyusmuyor: {n} != HEAD {beklenen}")
    part.replace(hedef)
    return n, ct


def indir_oge(tur, kimlik, hedef, beklenen, ilerleme, deneme=3):
    urls = gdrive_urls(kimlik) if tur == "gdrive" else [kimlik]
    hatalar = []
    for url in urls:
        for k in range(deneme):
            try:
                return indir_url(url, hedef, beklenen, ilerleme) + (url,)
            except ValueError as e:  # HTML: onay/kota sayfasi
                p = GizliAlanlar()
                p.feed(str(e))
                kota = "quota" in str(e).lower() or "too many users" in str(e).lower()
                if p.eylem and p.alan and not kota:
                    url2 = p.eylem + "?" + urllib.parse.urlencode(p.alan)
                    try:
                        return indir_url(url2, hedef, beklenen, ilerleme) + (url2,)
                    except Exception as e2:  # noqa: BLE001
                        hatalar.append(f"{url2[:80]}: {e2!r}"[:300])
                else:
                    hatalar.append(f"{url[:80]}: HTML ({'kota' if kota else 'onay sayfasi'})")
                break  # ayni adreste HTML tekrar denenmez
            except Exception as e:  # noqa: BLE001
                hatalar.append(f"{url[:80]} deneme {k + 1}: {e!r}"[:300])
                time.sleep(10 * (k + 1))
    raise RuntimeError(" | ".join(hatalar))


def bag_kur(hedef_D, bag_goreli):
    if bag_goreli is None:
        return "bag yok"
    bag = DEPO / bag_goreli
    bag.parent.mkdir(parents=True, exist_ok=True)
    if bag.is_symlink():
        if os.readlink(bag) == str(hedef_D):
            return "bag zaten var"
        return f"FARKLI BAG VAR: {os.readlink(bag)} (dokunulmadi)"
    if bag.exists():
        return "depoda gercek dosya var (dokunulmadi)"
    os.symlink(str(hedef_D), bag)
    return "bag kuruldu"


def guvenli_ac(arsiv, hedef_dizin):
    """Arsivi yalniz bos (ya da yeni) klasore acar; 'data' suzgeci (yol kacisi, bag, aygit engellenir)."""
    hedef_dizin.mkdir(parents=True, exist_ok=True)
    if any(hedef_dizin.iterdir()):
        raise SystemExit(f"{hedef_dizin} bos degil; acma atlandi")
    with tarfile.open(arsiv, "r:*") as tf:  # HF dosyasi .tar.gz adli ama sikistirilmamis tar olabilir
        if hasattr(tarfile, "data_filter"):
            tf.extractall(hedef_dizin, filter="data")
        else:
            for m in tf.getmembers():
                p = (hedef_dizin / m.name).resolve()
                if not str(p).startswith(str(hedef_dizin.resolve())) or not (m.isfile() or m.isdir()):
                    raise SystemExit(f"guvensiz uye: {m.name}")
            tf.extractall(hedef_dizin)


def v2_sayim(kok):
    """Acilmis ImageNetV2 klasorunde sinif klasoru (0-999) ve dosya sayimi."""
    alt = [p for p in kok.iterdir() if p.is_dir()]
    if len(alt) == 1 and not alt[0].name.isdigit():
        kok = alt[0]
    siniflar = sorted([p for p in kok.iterdir() if p.is_dir()], key=lambda p: int(p.name) if p.name.isdigit() else -1)
    say = {p.name: len([f for f in p.iterdir() if f.is_file()]) for p in siniflar}
    adlar = sorted(say)
    return {"goruntu_koku": str(kok), "sinif_klasoru": len(say),
            "sayisal_adlar_0_999": adlar == sorted(str(i) for i in range(1000)),
            "toplam_dosya": sum(say.values()), "sinif_basina_min": min(say.values()) if say else 0,
            "sinif_basina_max": max(say.values()) if say else 0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grup", choices=["hepsi", "imagenetv2", "in", "c100"], default="hepsi")
    ap.add_argument("--olc", action="store_true", help="yalniz HEAD ile boyut olc")
    ap.add_argument("--durum", action="store_true", help="kayit defterini ozetle")
    ap.add_argument("--sadece", nargs="*", default=None, help="yalniz bu adlar")
    a = ap.parse_args()
    idir = D_KOK / "_indirme"
    idir.mkdir(parents=True, exist_ok=True)
    kayit_yol = idir / "indirmeler.json"
    kayit = json.loads(kayit_yol.read_text()) if kayit_yol.exists() else {}
    sha_yol = D_KOK / "indirme_sha256.txt"
    ilerleme_yol = idir / "ilerleme.log"

    def ilerleme(s):
        with open(ilerleme_yol, "a") as f:
            f.write(f"{simdi()} {s}\n")
        print(s, flush=True)

    sec = [o for o in OGELER if a.grup in ("hepsi", o[0]) and (a.sadece is None or o[1] in a.sadece)]
    if a.durum:
        for g, ad, *_ in sec:
            k = kayit.get(f"{g}/{ad}", {})
            print(f"{g:10s} {ad:45s} {k.get('durum', '-'):12s} {k.get('bayt', '')} {k.get('sha256', '')[:16]}")
        return
    if a.olc:
        top = 0
        olc = {}
        for g, ad, tur, kim, hedef, bag, rol in sec:
            url = gdrive_urls(kim)[0] if tur == "gdrive" else kim
            n, ct, _ = head_boyut(url)
            olc[f"{g}/{ad}"] = {"bayt": n, "icerik_turu": ct, "url": url, "rol": rol}
            top += max(n, 0)
            print(f"{g:10s} {ad:45s} {n:>14,d} {ct}")
        print(f"toplam {top / 1e9:.3f} GB")
        (idir / "boyutlar_head.json").write_text(json.dumps({"tarih": simdi(), "ogeler": olc,
                                                            "toplam_bayt": top}, indent=1))
        return

    ilerleme(f"BASLADI grup={a.grup} oge={len(sec)}")
    for g, ad, tur, kim, hedef_g, bag, rol in sec:
        anahtar = f"{g}/{ad}"
        hedef = D_KOK / hedef_g
        hedef.parent.mkdir(parents=True, exist_ok=True)
        url0 = gdrive_urls(kim)[0] if tur == "gdrive" else kim
        n_head, ct, _ = head_boyut(url0)
        k = {"grup": g, "rol": rol, "kaynak": tur, "kimlik_ya_da_url": kim, "hedef": str(hedef),
             "head_bayt": n_head, "head_icerik_turu": ct}
        t0 = time.time()
        try:
            if hedef.exists() and n_head > 0 and hedef.stat().st_size == n_head:
                k["durum"] = "VARDI"
                k["bayt"] = hedef.stat().st_size
            else:
                if n_head <= 0 and tur == "gdrive":
                    ilerleme(f"{ad}: HEAD boyut vermedi ({ct}); yine de deneniyor")
                bayt, ict, kullanilan = indir_oge(tur, kim, hedef, n_head, ilerleme)
                k.update({"durum": "OK", "bayt": bayt, "indirme_icerik_turu": ict,
                          "kullanilan_url": kullanilan[:200]})
            k["sha256"] = sha256_dosya(hedef)
            if ad == "ImageNetV2-MatchedFrequency":
                beklenen = hf_lfs_sha256(HF_V2)
                k["hf_lfs_sha256"] = beklenen
                k["hf_sha256_esit"] = (beklenen == k["sha256"]) if beklenen else None
                if beklenen and beklenen != k["sha256"]:
                    raise RuntimeError(f"sha256 HF LFS degeriyle uyusmuyor: {k['sha256']} != {beklenen}")
            onceki = sha_yol.read_text().splitlines() if sha_yol.exists() else []
            satir = f"{k['sha256']}  {hedef_g}"
            onceki = [s for s in onceki if not s.endswith("  " + hedef_g)] + [satir]
            sha_yol.write_text("\n".join(onceki) + "\n")
            if ad == "ImageNetV2-MatchedFrequency":
                vdir = D_KOK / "data" / "imagenetv2"
                if not (vdir.exists() and any(vdir.iterdir())):
                    ilerleme("ImageNetV2 aciliyor -> " + str(vdir))
                    guvenli_ac(hedef, vdir)
                say = v2_sayim(vdir)
                (idir / "imagenetv2_sayim.json").write_text(json.dumps(say, indent=1))
                k["acilmis"] = say
                k["bag"] = bag_kur(vdir, "data/imagenetv2")
            else:
                k["bag"] = bag_kur(hedef, bag)
        except Exception as e:  # noqa: BLE001
            k["durum"] = "BASARISIZ"
            k["hata"] = str(e)[:1500]
            if tur == "gdrive":
                k["elle_indirme"] = {"url": gdrive_urls(kim)[0], "hedef": str(hedef), "depo_bagi": bag}
        k["sure_s"] = round(time.time() - t0, 1)
        k["tarih"] = simdi()
        kayit[anahtar] = k
        kayit_yol.write_text(json.dumps(kayit, indent=1, ensure_ascii=False))
        ilerleme(f"{anahtar}: {k['durum']} {k.get('bayt', '')} sha={k.get('sha256', '')[:16]} {k.get('bag', '')}"
                 + (f" HATA {k.get('hata', '')[:200]}" if k["durum"] == "BASARISIZ" else ""))
    bas = [x for x, v in kayit.items() if v.get("durum") == "BASARISIZ"]
    ilerleme(f"BITTI; basarisiz: {bas if bas else 'yok'}")


if __name__ == "__main__":
    main()
