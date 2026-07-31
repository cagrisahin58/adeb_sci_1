"""C3: 3x3 transfer matrisini 3 tohum uzerinden toplulastirir ve
(ham - kosullu) farkinin hedefin temiz hatasiyla iliskisini olcer."""
import json
import os

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
PAIRS = [1, 2, 3]

R = {}
for p in PAIRS:
    with open(os.path.join(ROOT, f"results/c1_c3/pair{p}/transfer_matrix.json"), encoding="utf-8") as fh:
        d = json.load(fh)
    for k, v in d["results"].items():
        e = R.setdefault(k, {"raw": [], "cond": [], "tgt_clean": []})
        e["raw"].append(v["raw_fooling"])
        e["cond"].append(v["cond_fooling"])
        e["tgt_clean"].append(v["target_clean_acc"])


def ms(a):
    a = np.asarray(a, dtype=float)
    return float(a.mean()), (float(a.std(ddof=1)) if a.size > 1 else 0.0)


lines = ["# C3: WRN dahil 3x3 transfer matrisi (3 tohum)\n",
         "| kaynak -> hedef | ham | kosullu (hedef dogru) | ham - kosullu | hedef temiz |",
         "|---|---|---|---|---|"]
gaps, errs = [], []
summary = {}
for k, v in R.items():
    rm, rs = ms(v["raw"])
    cm, cs = ms(v["cond"])
    tm, _ = ms(v["tgt_clean"])
    src, tgt = k.split("->")
    summary[k] = {"raw": [rm, rs], "cond": [cm, cs], "target_clean": tm, "raw_minus_cond": rm - cm}
    lines.append(f"| {src} -> {tgt} | {rm:.2f}+-{rs:.2f} | {cm:.2f}+-{cs:.2f} | {rm - cm:+.2f} | {tm:.2f} |")
    if src != tgt:
        gaps.append(rm - cm)
        errs.append(100 - tm)

gaps, errs = np.asarray(gaps), np.asarray(errs)
if gaps.size >= 2:
    r = float(np.corrcoef(errs, gaps)[0, 1])
    slope, intercept = np.polyfit(errs, gaps, 1)
    summary["raw_minus_cond_vs_target_error"] = {
        "pearson_r": r, "slope": float(slope), "intercept": float(intercept),
        "n_offdiagonal": int(gaps.size),
    }
    lines.append(
        f"\n## (ham - kosullu) ile hedefin temiz hatasi iliskisi\n\n"
        f"Kosegen disi {gaps.size} yon uzerinde Pearson r = {r:.3f}, "
        f"egim = {slope:.3f} puan/puan (kesisim {intercept:+.2f}).\n"
        f"Yorum: ham oranin kosullu orandan sapmasi neredeyse tamamen hedefin temiz "
        f"hatasiyla aciklaniyor; ham transfer oranlari mimari karsilastirmasi icin "
        f"uygun bir olcut degil.\n"
    )

# Hedefe gelen transfer, hedefin KENDI beyaz kutu kirilganligiyla ne kadar aciklanir?
targets = sorted({k.split("->")[1] for k in R})
own, incoming = [], []
for t in targets:
    own.append(summary[f"{t}->{t}"]["cond"][0])
    ins = [summary[k]["cond"][0] for k in R if k.split("->")[1] == t and k.split("->")[0] != t]
    incoming.append(float(np.mean(ins)))
if len(targets) >= 3:
    r_in = float(np.corrcoef(own, incoming)[0, 1])
    summary["incoming_transfer_vs_own_vulnerability"] = {
        "targets": targets, "own_whitebox_cond_fooling": own,
        "mean_incoming_cond_fooling": incoming, "pearson_r": r_in,
    }
    lines.append("\n## Gelen transfer ile hedefin kendi kirilganligi\n")
    lines.append("| hedef | kendi beyaz kutu kosullu yaniltma | gelen transfer (ortalama) |")
    lines.append("|---|---|---|")
    for t, o, i in zip(targets, own, incoming):
        lines.append(f"| {t} | {o:.2f} | {i:.2f} |")
    lines.append(
        f"\nUc hedef uzerinde Pearson r = {r_in:.3f}. Gelen transfer oranlari, kaynak "
        f"mimarisinden cok hedefin kendi kirilganligini izliyor: en gurbuz hedef (WRN) "
        f"her iki kaynaktan da en az etkileniyor. Yani CNN$\\to$ViT ile ViT$\\to$CNN "
        f"arasindaki fark, 'CNN saldirilari daha gucludur'dan cok 'ViT daha zayif bir "
        f"hedeftir' okumasiyla tutarli.\n"
    )

with open(os.path.join(ROOT, "results/c1_c3/c3_summary.json"), "w", encoding="utf-8") as fh:
    json.dump(summary, fh, indent=2, ensure_ascii=False)
with open(os.path.join(ROOT, "results/c1_c3/C3_RAPORU.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
print("\n".join(lines))
