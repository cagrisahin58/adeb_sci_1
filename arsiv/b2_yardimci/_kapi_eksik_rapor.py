#!/usr/bin/env python3
"""Sayi kapisinin (scripts/verify_manuscript_numbers.py) EKSIK listesini yazar icin Markdown'a cevirir.

Kapiyi metnin ANLIK haliyle `--eksik-json` ile kosar, kalemleri turlerine gore ayirir (KAYNAK deger eksik,
ATIF EKSIK, ust sinir, GRUPSUZ, YON denetlenemedi, diger) ve her kalem icin onerilen cozumu yazar:
hangi foy satiri atfedilmeli ya da KAYNAK yorumuna hangi deger ve belge yazilmali.

Konteynerde: docker exec -w /workspace adeb_eval python -B arsiv/b2_yardimci/_kapi_eksik_rapor.py
Cikti: raporlar/hakem_konsey_2026-10-31/sayi_kapisi_eksikler.md (sayi kapisi ucuncu tur, 2026-10-31).
"""
import json
import re
import subprocess
import sys
import tempfile
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
KAPI = ROOT / "scripts/verify_manuscript_numbers.py"
CIKTI = ROOT / "raporlar/hakem_konsey_2026-10-31/sayi_kapisi_eksikler.md"
EN = ROOT / "paper/manuscript"

ONCELIK = ["ON_KAYIT_2026-10-29.md", "ON_KAYIT_EK_B8_B10_2026-10-30.md", "CLAUDE.md", "12_makale_revizyon_brifi.md"]
BELGE_ADI = {"ON_KAYIT_2026-10-29.md": "ON_KAYIT", "ON_KAYIT_EK_B8_B10_2026-10-30.md": "EK", "CLAUDE.md": "CLAUDE.md",
             "12_makale_revizyon_brifi.md": "brif 12"}


def bolum_etiketi(baslik):
    m = re.match(r"\s*(M\d+(?:\.\d+)*)", baslik or "")
    if m:
        return m.group(1)
    w = re.sub(r"[^\w\s-]", " ", baslik or "Foy").split()
    return " ".join(w[:3]) or "Foy"


def belge_onerisi(o):
    b = sorted(o.get("belge", []), key=lambda x: next((i for i, a in enumerate(ONCELIK) if x["belge"].endswith(a)), 99))
    if not b:
        return None
    x = b[0]
    ad = BELGE_ADI.get(Path(x["belge"]).name, x["belge"])
    return f"{ad} (`{x['belge']}` satir {', '.join(map(str, x['satirlar'][:3]))})"


def foy_onerisi(o, n=3):
    f = o.get("foy", [])[:n]
    if not f:
        return None
    return "; ".join(f"`FOY:{bolum_etiketi(x['baslik'])}:{x['satir']}` ({x['baslik'][:40]})" for x in f)


def kod_onerisi(o):
    k = o.get("kod", [])
    if not k:
        return None
    return "; ".join(f"`{x['belge']}` satir {', '.join(map(str, x['satirlar'][:2]))}" for x in k[:2])


def cozum(k):
    tur, o, v = k["tur"], k["oneri"], k["deger"]
    b, f, c = belge_onerisi(o), foy_onerisi(o), kod_onerisi(o)
    if tur in ("KAYNAK DEGER EKSIK", "GRUPSUZ"):
        yer = "grubun KAYNAK yorumuna" if tur == "KAYNAK DEGER EKSIK" else "paragrafin ustune bir `% KAYNAK:` yorumu acip"
        oncelikli = bool(b) and any(Path(x["belge"]).name in ONCELIK for x in o.get("belge", []))
        parca = []
        if c and not oncelikli:
            parca.append(f"Kod/ayar sabitiyse {yer} acik yolla yazin, or. `% KAYNAK: {c.split('`')[1]} ({v})` ({c}).")
        if b:
            parca.append(f"Tasarim sabitiyse {yer} `{v}` degerini ve belgeyi yazin: {b}.")
        if f:
            parca.append(f"Olcum sayisiysa {('paragrafin ustune ' if tur == 'GRUPSUZ' else '')}FOY atfi ekleyin: {f}.")
        return " ".join(parca) or ("Deger ne foyde ne tasarim belgelerinde ne de kodda bulundu: kaynagi yazar belirlemeli ya da "
                                   "sayi metinden cikmali.")
    if tur == "KAYNAK BELGEDE YOK":
        if b:
            return f"KAYNAK yorumundaki belge adini degeri tasiyan belgeyle degistirin ya da ekleyin: {b}."
        if c:
            return f"Degeri tasiyan dosyayi acik yolla adlandirin: {c}."
        if f:
            return f"Deger foyde var: KAYNAK yerine FOY atfi kullanin: {f}."
        return "Deger hicbir belgede bulunmadi; 'eski metin' bir belge degildir, kaynagi yazar belirlemeli."
    if tur == "ATIF EKSIK":
        s = f"Grubun FOY yorumuna atfedilmesi gereken satir (ilk adaylar): {f}." if f else "Foy satiri bulunamadi."
        if b:
            s += f" Tasarim sabitiyse FOY yerine KAYNAK yorumuna yazin: {b}."
        return s
    if tur == "UST SINIR":
        return ("Atfedilen foy paragrafina (foy yazari) 'metne girecek ortak sinir: p < B' satiri eklenmeli; B o paragraftaki "
                "en buyuk p'den kucuk olmamali. Ya da metin foyde AYNEN yazili bir p degerini kullanmali.")
    if tur == "YON DENETLENEMEDI":
        return k.get("yon_onerisi") or ("Cumledeki araligi metne yazin ya da paragrafin ustune `% YON: [a; b] FOY:<bolum>:<satir>` "
                                        "ekleyin; sayisiz kural cumlesiyse `% YON: kural`.")
    if tur == "DEMET ATIF EKSIK":
        m = re.search(r"foy satiri ([\d, ]+)", k["neden"])
        return f"Demet birlikte yalniz foy satiri {m.group(1).strip() if m else '?'} icinde: bu satiri grubun FOY yorumuna ekleyin."
    if tur == "KOPYA":
        return "Kalemin dogru degerini yazin (ya da takasli deger mesruysa blogun FOY yorumuna ekleyin)."
    return "Ayrintiya gore duzeltin."


def yon_onerisi(k, L_tex, FOY):
    """YON DENETLENEMEDI icin somut oneri: tablo icindeyse '% YON: kural'; degilse ifadeden onceki kestirimi foyde arar."""
    i = k["satir"] - 1
    acik = sum(1 for s in L_tex[:i + 1] if re.search(r"\\begin\{table", s)) - sum(1 for s in L_tex[:i] if re.search(r"\\end\{table", s))
    if acik > 0:
        return "Karar kurali tablosu (sayisiz kural cumlesi): tablonun KAYNAK yorumunun yanina `% YON: kural` ekleyin."
    s = L_tex[i]
    m = re.search(r"\b(exclud|includ|contain|span)\w*\s+(zero|0)", s)
    once = s[:m.start()] if m else s
    say = re.findall(r"(-?\$?-?\d+\.\d+)", once.replace("$", ""))
    if not say:
        return None
    v = say[-1].replace("$", "")
    duzey = "95" if re.search(r"95\s*\\?%", s[max(0, (m.start() if m else 0) - 60):(m.start() if m else len(s))]) else "90"
    for n, f in enumerate(FOY, 1):
        if re.search(r"(?<![\d.])" + re.escape(v) + r"(?![\d])", f):
            br = list(re.finditer(r"\[\s*([+-]?\d+[.,]\d+)\s*;\s*([+-]?\d+[.,]\d+)\s*\]", f[f.find(v):]))
            if not br:
                continue
            x = br[1] if (duzey == "95" and len(br) > 1) else br[0]
            a, b = x.groups()
            return (f"Kestirim {v} foy satiri {n}'de; cumle %{duzey} araligina dayaniyor: paragrafin ustune "
                    f"`% YON: [{a}; {b}] FOY:<bolum>:{n}` ekleyin (foy satirinda kestirimden sonraki "
                    f"{'ikinci' if x is not br[0] else 'ilk'} aralik; satir: `{f.strip()[:140]}`).")
    return None


def main():
    with tempfile.TemporaryDirectory() as t:
        js = Path(t) / "eksik.json"
        r = subprocess.run([sys.executable, "-B", str(KAPI), "--eksik-json", str(js)], capture_output=True, text=True, cwd=str(ROOT))
        D = json.loads(js.read_text(encoding="utf-8"))
    m = re.search(r"EN_EKSIK=(\d+)", r.stdout)
    en_eksik = int(m.group(1)) if m else None
    ozet_satir = next((s for s in r.stdout.splitlines() if s.startswith("[EN] A.")), "")
    FOY = (ROOT / "results/C1_REFERANS_FOYU.md").read_text(encoding="utf-8").split("\n")
    tex = {}
    for k in D["kayit"]:
        if k["tur"] == "YON DENETLENEMEDI":
            L_ = tex.setdefault(k["dosya"], (EN / k["dosya"]).read_text(encoding="utf-8").split("\n"))
            k["yon_onerisi"] = yon_onerisi(k, L_, FOY)
    BOL = OrderedDict([
        ("KAYNAK deger eksik", ("KAYNAK DEGER EKSIK", "KAYNAK BELGEDE YOK")),
        ("ATIF EKSIK", ("ATIF EKSIK",)),
        ("Ust sinir", ("UST SINIR",)),
        ("GRUPSUZ", ("GRUPSUZ",)),
        ("YON denetlenemedi", ("YON DENETLENEMEDI",)),
    ])
    kume = defaultdict(list)
    for k in D["kayit"]:
        b = next((ad for ad, turler in BOL.items() if k["tur"] in turler), "Diger")
        kume[b].append(k)
    sayac = {ad: len(kume.get(ad, [])) for ad in list(BOL) + ["Diger"]}
    out = []
    out.append("# Sayi kapisi: metnin anlik halinde EKSIK listesi (2026-10-31)")
    out.append("")
    out.append("Bu liste `arsiv/b2_yardimci/_kapi_eksik_rapor.py` ile uretildi; kapinin ucuncu ve son duzeltme turundan "
               "(K1b, S1b, T1, Y1-Y4) sonra `scripts/verify_manuscript_numbers.py` makalenin o anki haliyle kosuldu. "
               "Makale baska bir ajan tarafindan duzenlendigi icin satir numaralari kayabilir; listeyi yeniden uretmek icin "
               "`docker exec -w /workspace adeb_eval python -B arsiv/b2_yardimci/_kapi_eksik_rapor.py` yeterlidir.")
    out.append("")
    out.append(f"Kapinin hukmu: EN_EKSIK = {en_eksik}. Kapi ozeti: `{ozet_satir.strip()}`")
    out.append("")
    out.append("| Tur | Kalem |")
    out.append("|---|---|")
    for ad, n in sayac.items():
        out.append(f"| {ad} | {n} |")
    out.append("")
    out.append("Onerilerin okunusu: 'Tasarim sabitiyse' onerisi degeri iceren tasarim belgesini (on kayit, ek on kayit, "
               "CLAUDE.md, brif) satiriyla verir; KAYNAK yorumuna degerin kendisi ve belgenin adi birlikte yazilmalidir "
               "(or. `% KAYNAK: ON_KAYIT Sec. 5 (H1 esigi -0.20; K-a esigi 0.75)`), cunku kapi yalniz yorumda ACIKCA "
               "yazili degeri kabul eder ve onu adlandirilan belgede arar. 'Olcum sayisiysa' onerisi degerin gectigi ilk foy "
               "satirlarini verir; dogru satiri baglama gore yazar secer. `FOY:<bolum>:<satir>` icindeki bolum etiketi "
               "kapi icin bilgi amaclidir, denetlenen satir numarasidir. 'eski metin' bir belge sayilmaz.")
    out.append("")
    out.append("## Yazar icin yazim kurallari (kapinin ucuncu surumu)")
    out.append("")
    out.append("1. Her sayili paragraf ya da tablo ustunde bir yorum grubu tasir: olcum sayilari icin `% FOY:<bolum>:<satir>`, "
               "tasarim sabitleri icin `% KAYNAK: <belge> (<deger>; <deger>)`. Bos satir grubu bitirir; bos satirla ayrilan "
               "ikinci paragraf kendi yorumunu ister (03_methodology.tex:77, 199, 265 bu yuzden GRUPSUZ).")
    out.append("2. KAYNAK yorumu belgeyi adiyla anar: `ON_KAYIT` (on kayit), `EK` (ek on kayit), `CLAUDE.md`, `brif`, "
               "`R09`/`R11` ya da acik yol (`raporlar/...md`, `experiments/rev2/make_val_split.py`). Yazilan her deger o "
               "belgede bulunmalidir. 'eski metin 03:78-100' bir belge sayilmaz. 'a-b' tamsayi araligi iki ucu kapsar "
               "(`tohumlar 1001-1003` 1001 ve 1003'u kapsar).")
    out.append("3. 'excludes/includes zero' diyen cumle ya araligi kendisi tasir ya da grubun ustunde `% YON: [a; b] "
               "FOY:<bolum>:<satir>` bulunur; sayisiz karar kurali cumleleri icin `% YON: kural`.")
    out.append("4. Ozet ve degerleri yorumda anilan bloklarda bir manset degerinin iki anlamli rakami yer degistirirse "
               "(0.936 -> 0.963) kapi KOPYA EKSIK verir; takasli deger mesruysa blogun yorumuna yazilir.")
    out.append("")
    for ad in list(BOL) + ["Diger"]:
        L_ = kume.get(ad, [])
        out.append(f"## {ad} ({len(L_)})")
        out.append("")
        if not L_:
            out.append("Kalem yok.")
            out.append("")
            continue
        out.append("| Yer | Deger | Tur ve neden | Onerilen cozum |")
        out.append("|---|---|---|---|")
        for k in sorted(L_, key=lambda k: (k["dosya"], k["satir"] if isinstance(k["satir"], int) else 0, k["deger"])):
            yer = f"{k['dosya']}:{k['satir']}" if k["dosya"] else "-"
            nd = k["neden"] or ""
            neden = (nd if nd.startswith(k["tur"]) else k["tur"] + (": " + nd if nd else "")).replace("|", "/")
            out.append(f"| `{yer}` | `{k['deger'] or '-'}` | {neden[:220]} | {cozum(k).replace('|', '/')} |")
        out.append("")
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    with open(CIKTI, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"yazildi: {CIKTI.relative_to(ROOT)}  EN_EKSIK={en_eksik}  " + "  ".join(f"{a}={n}" for a, n in sayac.items()))


if __name__ == "__main__":
    main()
