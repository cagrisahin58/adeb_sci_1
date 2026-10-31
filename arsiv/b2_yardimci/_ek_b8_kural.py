"""Ek on kayit §5.5 kuralini onisleme_denetimi.json'a bagimsiz uygular (31.10.2026, salt okur).
RB temiz dogruluklari raporlar/konsey_2026-10-29/_ek_denetim/dis/rb/in_<ad>.json (clean_acc) kopyalarindan okunur."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path("/home/firat/projects/adeb_sci_1")
DEN = KOK / "results/q1/konsey_b8_imagenetv2/denetim/onisleme_denetimi.json"
MAN = KOK / "results/q1/konsey_b8_imagenetv2/denetim/imagenetv2_manifest.json"
RB = KOK / "raporlar/konsey_2026-10-29/_ek_denetim/dis/rb"

d = json.loads(DEN.read_text())
m = json.loads(MAN.read_text())
print(f"manifest n={m.get('n')} liste_sha256={m.get('liste_sha256')}")
print(f"denetim ortak_onisleme={d['ortak_onisleme']} n={d['n']} kalan={d['kalan']} isaretli={d['isaretli']}")
print("takma_ad|rb_adi|rb_temiz(json)|esik_i|kendi|ortak|fark(ortak-kendi)|abs|i|ii|isaret|karar_bagimsiz|karar_betik|uyum")
uyumsuz = 0
for ad, r in d["modeller"].items():
    rb_adi = r["model"]
    rbj = json.loads((RB / f"in_{rb_adi}.json").read_text())
    rb = float(rbj["clean_acc"])
    rb = rb * 100 if rb <= 1 else rb
    kendi, ortak = r["temiz_dogruluk_kendi"], r["temiz_dogruluk_ortak"]
    esik = max(25.0, 0.6 * rb)
    i_ok = kendi >= 25.0 and kendi >= 0.6 * rb
    fark = ortak - kendi
    ii_ok = abs(fark) <= 5.0
    isaret = ii_ok and abs(fark) > 3.0
    karar = "kaldi" if not (i_ok and ii_ok) else ("gecti_isaretli" if isaret else "gecti")
    kb = r["esik"]["karar"]
    uy = (karar == kb) and abs(r["esik"]["rb_temiz"] - rb) < 1e-9
    uyumsuz += (not uy)
    print(f"{ad}|{rb_adi}|{rb:.2f}|{esik:.3f}|{kendi:.2f}|{ortak:.2f}|{fark:+.2f}|{abs(fark):.2f}|{i_ok}|{ii_ok}|{isaret}|{karar}|{kb}|{'UYUMLU' if uy else 'UYUMSUZ'}")
    print(f"   kendi_onisleme={r.get('kendi_onisleme')}")
print(f"uyumsuz={uyumsuz}")
