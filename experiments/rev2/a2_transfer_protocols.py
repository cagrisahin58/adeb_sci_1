"""A2: Transfer protokolleri ve istatistik (rev2 BLOK A).

Uc protokol: target-correct (mevcut), both-correct, successful-source.
Both-correct ortak kumede paired bootstrap + sign-flip permutation testi,
fark icin bootstrap CI, TOST +-1/+-2/+-3 duyarlilik tablosu.

Çalıştırma: docker exec adeb_eval python /workspace/experiments/rev2/a2_transfer_protocols.py
Çıktı: results/rev2_blockA/a2_transfer_protocols.json
"""
import json
import math
import os
import zlib

import sys

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
sys.path.insert(0, ROOT)
from src.analysis import protokoller as PROTO  # noqa: E402
OUT_DIR = os.path.join(ROOT, "results/rev2_blockA")
os.makedirs(OUT_DIR, exist_ok=True)

SEED = 42


def _akis(*etiket):
    """Tuketici adina baglanmis BAGIMSIZ rastgele akis.

    Tek bir paylasilan RNG kullanilirsa, yukarida fazladan bir bootstrap
    kosmak asagidaki permutasyon testinin sayilarini kaydirir. Ad-tabanli
    turetme bunu imkansiz kilar; her sayi tek basina yeniden uretilebilir.
    """
    anahtar = zlib.crc32("|".join(str(e) for e in etiket).encode())
    return np.random.default_rng([SEED, anahtar])
N_BOOT = 10000
N_PERM = 20000


# Girdi/cikti yolu ortam degiskeniyle degistirilebilir: ayni istatistik kodunu
# C1 (3 tohum, sizinti duzeltmeli) kontrol noktalarina da uygulayabilmek icin.
IN_DIR = os.environ.get("A2_IN_DIR", "results/transfer_analysis_run3")
OUT_FILE = os.environ.get("A2_OUT", os.path.join(OUT_DIR, "a2_transfer_protocols.json"))


def load_pair(src, tgt):
    fname = f"per_sample_{src}_to_{tgt}.npz"
    with np.load(os.path.join(ROOT, IN_DIR, fname)) as z:
        return {k: z[k].copy() for k in z.files}


cnn2vit = load_pair("ResNet18_AT", "ViT_Tiny_AT")
vit2cnn = load_pair("ViT_Tiny_AT", "ResNet18_AT")


def rate_ci(fool_mask, cond_mask, etiket):
    rng = _akis("rate_ci", etiket)
    idx = np.flatnonzero(cond_mask)
    vals = fool_mask[idx].astype(float)
    n = len(vals)
    boots = np.empty(N_BOOT)
    for b in range(N_BOOT):
        boots[b] = vals[rng.integers(0, n, n)].mean()
    return {
        "rate": round(float(vals.mean() * 100), 2),
        "n_conditioned": int(n),
        "ci95": [round(float(np.percentile(boots, 2.5) * 100), 2), round(float(np.percentile(boots, 97.5) * 100), 2)],
    }


def protocol_masks(pair, protocol):
    """Maskeler src/analysis/protokoller.py'den gelir (TEK KAYNAK).

    'successful_source' BEYAZ KUTU BASARISIDIR: kaynak temizde dogru VE
    cekismelide yanlis. 'successful_source_loose' terk edilmis gevsek
    varyanttir ve yalniz duyarlilik raporlamasi icin tasinir.
    """
    m = PROTO.maskeler(pair["target_clean_correct"], pair["source_clean_correct"],
                       pair["source_adv_wrong"], tani=True)
    if protocol not in m:
        raise ValueError(protocol)
    return pair["target_adv_wrong"], m[protocol]


report = {"seed": 42, "n_bootstrap": N_BOOT, "n_permutation": N_PERM,
          "ss_definition": "target_clean_correct & source_clean_correct & source_adv_wrong",
          "protocols": {}}

for protocol in PROTO.PROTOKOLLER + PROTO.TANI_PROTOKOLLERI:
    f_cv, c_cv = protocol_masks(cnn2vit, protocol)
    f_vc, c_vc = protocol_masks(vit2cnn, protocol)
    entry = {
        "CNN_to_ViT": rate_ci(f_cv, c_cv, f"{protocol}/CNN_to_ViT"),
        "ViT_to_CNN": rate_ci(f_vc, c_vc, f"{protocol}/ViT_to_CNN"),
    }
    entry["diff_CNNtoViT_minus_ViTtoCNN"] = round(entry["CNN_to_ViT"]["rate"] - entry["ViT_to_CNN"]["rate"], 2)
    report["protocols"][protocol] = entry

# --- Both-correct ortak kumede PAIRED analiz --------------------------------
# Ayni ortak kume: iki modelin de clean-dogru oldugu ornekler. Her ornek icin
# iki yonun fooling gostergesi ayni orneklem uzerinde tanimli -> paired.
B = cnn2vit["target_clean_correct"] & cnn2vit["source_clean_correct"]
B2 = vit2cnn["target_clean_correct"] & vit2cnn["source_clean_correct"]
assert (B == B2).all(), "ortak kume iki dosyada ayni olmali"
idx = np.flatnonzero(B)
x = cnn2vit["target_adv_wrong"][idx].astype(float)  # CNN->ViT fooling gostergesi
y = vit2cnn["target_adv_wrong"][idx].astype(float)  # ViT->CNN fooling gostergesi
d = x - y
n = len(d)
diff = d.mean()

# paired bootstrap CI -- KENDI akisi
_rng_boot = _akis("both_correct_paired", "bootstrap")
boots = np.empty(N_BOOT)
for b in range(N_BOOT):
    boots[b] = d[_rng_boot.integers(0, n, n)].mean()
ci = [float(np.percentile(boots, 2.5) * 100), float(np.percentile(boots, 97.5) * 100)]

# sign-flip permutation testi (H0: fark dagilimi 0 etrafinda simetrik)
_rng_perm = _akis("both_correct_paired", "permutation")
signs = _rng_perm.integers(0, 2, size=(N_PERM, n)) * 2 - 1
perm_means = (signs * d).mean(axis=1)
p_perm = float((np.abs(perm_means) >= abs(diff)).mean())

# TOST (paired normal yaklasik): H0 |delta| >= margin
se = d.std(ddof=1) / math.sqrt(n)
tost = {}
for margin_pp in [1, 2, 3]:
    m = margin_pp / 100.0
    z_low = (diff + m) / se
    z_up = (diff - m) / se
    p_low = 0.5 * math.erfc(z_low / math.sqrt(2))          # P(Z <= -z_low): delta <= -m tek tarafli
    p_up = 0.5 * math.erfc(-z_up / math.sqrt(2))           # P(Z >= z_up): delta >= +m tek tarafli
    tost[f"margin_{margin_pp}pp"] = {"p": float(f"{max(p_low, p_up):.3g}"), "equivalent_at_0.05": bool(max(p_low, p_up) < 0.05)}

report["both_correct_paired"] = {
    "n_common": int(n),
    "diff_pp": round(float(diff * 100), 2),
    "paired_bootstrap_ci95_pp": [round(ci[0], 2), round(ci[1], 2)],
    "signflip_permutation_p": p_perm,
    "paired_se_pp": round(float(se * 100), 3),
    "tost_sensitivity": tost,
    "tost_margin_rationale": "2pp marji, egitim-kosusu duzeyindeki gozlenen varyasyonun (~PGD birkac puan) "
    "altinda kalan farklari pratikte-esdeger sayma ilkesine dayanir; +-1/+-3 duyarlilik tablosu verilir.",
}

out = OUT_FILE
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as f:
    json.dump(report, f, indent=1)
print(json.dumps(report, indent=1))
print(f"\nkaydedildi: {out}")
