#!/usr/bin/env python3
"""E3 sekli: iki kol AYRI panel + x eksenindeki DELIKLER gorunur.

BAGLAYICI SARTLAR (E3_YENIDEN_TASARIM EK A.3 ve B.3):
  · EK A'nin olctugu iki delik SEKILDE GORUNUR KILINACAK. O bantlarda egim
    hicbir noktayla desteklenmiyor; deger INTERPOLASYONDUR.
  · Kollar AYRI panelde; HAVUZLANMIS tek bir uydurma CIZILMEZ.
  · Serbestlik derecesini KUME sayisi belirler -> altyazida n=<nokta> degil
    "<k> kume" yazilir.
  · Basarili-kaynak AYRI bir surucudur (EK C) -> dort-protokol ve uc-protokol
    yayilimlari AYNI panelde iki seri olarak cizilir.

Girdi : results/q1/e3_iki_kol_fit.json  (+ nokta dosyalari)
Cikti : paper/figures/raw/fig_e3_kalibrasyon.pdf  (+ .png onizleme)
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import numpy as np                       # noqa: E402

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
P4 = ["raw", "target_correct", "both_correct", "successful_source"]
P3 = ["raw", "target_correct", "both_correct"]

# DELIKLER, SEKLIN KENDI EKSENINDEN hesaplanir.
#
# DIKKAT -- bir kez yanlis yapildi: EK A'nin olctugu iki delik
# (%17,68-23,28 ve %42,28-56,40) HEDEFIN TEMIZ HATASI eksenindedir; bu sekil
# ise CIFTIN HATA FARKI eksenini kullanir. Ayni BIRIM (puan) oldugu icin gri
# bantlar makul GORUNUYOR ama BASKA BIR NICELIGIN bosluklarini isaretliyordu.
# EK A'nin baglayici sarti "olculmemis bolgeler gorunur olsun"dur ve o sart
# KULLANILAN eksende saglanmalidir.
def delikleri_bul(x_degerleri, esik=2.0):
    """x ekseninde gozlenmemis araliklar (esik puandan genis kopukluklar)."""
    xs = sorted(set(round(float(v), 3) for v in x_degerleri))
    return [(xs[i], xs[i + 1]) for i in range(len(xs) - 1)
            if xs[i + 1] - xs[i] > esik]


def kayitlar(kol):
    if kol == "A":
        d = ROOT / "results/q1/e3_akolu"
        return [json.loads(f.read_text(encoding="utf-8")) for f in sorted(d.glob("*.json"))] if d.is_dir() else []
    bf = ROOT / "results/q1/e3_asimetri_fit.json"
    if not bf.exists():
        return []
    return json.loads(bf.read_text(encoding="utf-8"))["ciftler"]


fit = json.loads((ROOT / "results/q1/e3_iki_kol_fit.json").read_text(encoding="utf-8"))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True)
BASLIK = {"A": "A kolu — kontrollü (yörünge içi)",
          "B": "B kolu — gözlemsel (final modeller)"}

for ax, kol in zip(axes, ("A", "B")):
    ks = kayitlar(kol)
    bilgi = fit["kollar"].get(kol, {})
    if not ks or "dort_protokol" not in bilgi:
        ax.text(0.5, 0.5, f"{kol} kolu: veri yok", ha="center", va="center",
                transform=ax.transAxes, fontsize=11)
        ax.set_title(BASLIK[kol], fontsize=11)
        continue

    x = np.array([k["x_temiz_hata_farki"] for k in ks])
    y4 = np.array([max(k["asimetri"][p] for p in P4) - min(k["asimetri"][p] for p in P4) for k in ks])
    y3 = np.array([max(k["asimetri"][p] for p in P3) - min(k["asimetri"][p] for p in P3) for k in ks])

    ax.scatter(x, y4, s=26, alpha=0.75, label="4 protokol", color="#1f77b4", zorder=3)
    ax.scatter(x, y3, s=26, alpha=0.75, marker="^",
               label="3 protokol (başarılı-kaynak hariç)", color="#d62728", zorder=3)

    xs = np.linspace(x.min(), x.max(), 100)
    for ad, renk, seri in (("dort_protokol", "#1f77b4", y4),
                           ("uc_protokol_bas_kaynak_haric", "#d62728", y3)):
        b1, b0 = np.polyfit(x, seri, 1)
        ax.plot(xs, b1 * xs + b0, color=renk, lw=1.6, zorder=2)
        ga = bilgi[ad]["egim_GA95"]
        ax.plot([], [], " ", label=f"eğim {b1:+.3f}  GA [{ga[0]:+.2f}, {ga[1]:+.2f}]")

    # --- DELIKLER: EK A sarti, BU KOLUN KENDI x ekseninde ---
    delikler = delikleri_bul(x)
    for lo, hi in delikler:
        ax.axvspan(lo, hi, color="0.85", zorder=1)
    if delikler:
        genis = ", ".join(f"{lo:.1f}-{hi:.1f}" for lo, hi in delikler)
        ax.plot([], [], " ", label=f"gri: x'te ÖLÇÜLMEMİŞ ({genis})")
    else:
        ax.plot([], [], " ", label="x'te 2 puandan geniş delik yok")

    ax.set_xlabel("çiftin temiz hata farkı (puan)")
    ax.set_title(f"{BASLIK[kol]}\n{bilgi['n_kume']} küme", fontsize=11)
    # gosterge NOKTALARI ORTMESIN: eksenin ustunde yer ac ve alt-sag'a al
    ax.set_ylim(top=max(y4.max(), y3.max()) * 1.32)
    ax.legend(fontsize=7.5, loc="lower right", framealpha=0.92)
    ax.grid(alpha=0.25, zorder=0)

axes[0].set_ylabel("asimetrinin protokoller arası yayılımı (puan)")
fig.suptitle("E3 — protokol yayılımının kalibrasyonu (kollar AYRI; havuzlanmış uydurma YOK)",
             fontsize=12)
fig.tight_layout(rect=(0, 0, 1, 0.95))

out_dir = ROOT / "paper/figures/raw"
out_dir.mkdir(parents=True, exist_ok=True)
for ext in ("pdf", "png"):
    fig.savefig(out_dir / f"fig_e3_kalibrasyon.{ext}", dpi=160, bbox_inches="tight")
print(f"yazildi: {out_dir}/fig_e3_kalibrasyon.pdf (+.png)")
for _kol in ("A", "B"):
    _ks = kayitlar(_kol)
    if _ks:
        _d = delikleri_bul([k["x_temiz_hata_farki"] for k in _ks])
        print(f"  kol {_kol} x-ekseni delikleri: {_d or 'yok'}")
print("NOT: EK A'nin %17,68-23,28 ve %42,28-56,40 delikleri HEDEFIN TEMIZ HATASI")
print("     eksenindedir; bu sekil CIFTIN HATA FARKI eksenini kullanir. Farkli")
print("     nicelik oldugu icin o bantlar burada CIZILMEZ.")
for kol in ("A", "B"):
    b = fit["kollar"].get(kol, {})
    print(f"  kol {kol}: " + (f"{b.get('n_nokta')} nokta / {b.get('n_kume')} kume"
                              if "n_kume" in b else b.get("DURUM", "yok")))
