# Salt okur: B10 Mantel ciktilari ve kosinus ozetlerinden rapor icin degerleri basar (stdlib).
# c_ij betimsel ozetleri (aile ici / aileler arasi ortalama) ayni dosyadaki c_tum matrisinden turetilir;
# aile atamasi hucre tablolarindan (CIFAR-10: hucre_tablosu.json, CIFAR-100: _b9, ImageNetV2: _b8) okunur.
import json
import statistics as st
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = "results/q1/konsey_b10_gradyan/"
HT = {"cifar10": "raporlar/konsey_2026-10-29/hucre_tablosu.json",
      "cifar100": "raporlar/konsey_2026-10-29/hucre_tablosu_b9.json",
      "imagenetv2": "raporlar/konsey_2026-10-29/hucre_tablosu_b8.json"}


def kisa(o, n=300):
    return json.dumps(o, ensure_ascii=False)[:n]


for d in ["cifar10", "cifar100", "imagenetv2"]:
    m = json.load(open(f"{R}mantel_{d}.json", encoding="utf-8"))
    print(f"\n==== mantel_{d}.json ust anahtarlar: {list(m.keys())}")
    for k, v in m.items():
        if isinstance(v, dict):
            print(f"  {k}: alt anahtarlar {list(v.keys())[:20]}")
            for kk, vv in v.items():
                if not isinstance(vv, (list, dict)):
                    print(f"     {k}.{kk} = {kisa(vv)}")
                elif isinstance(vv, list) and len(vv) <= 25 and all(not isinstance(x, (list, dict)) for x in vv):
                    print(f"     {k}.{kk} = {kisa(vv, 500)}")
                else:
                    print(f"     {k}.{kk} = <{type(vv).__name__} {len(vv)}>")
        elif isinstance(v, list):
            print(f"  {k}: list {len(v)} {kisa(v[:20], 400)}")
        else:
            print(f"  {k} = {kisa(v)}")

    k = json.load(open(f"{R}{d}/kosinus_ozet.json", encoding="utf-8"))
    print(f"---- {d}/kosinus_ozet.json: n={k.get('n')} K={len(k['modeller'])} nan={k.get('nan_kosinus_sayisi')} "
          f"sha={k.get('betik_sha256')} uretildi={k.get('uretildi_utc')} anahtarlar={list(k.keys())}")
    ht = json.load(open(HT[d], encoding="utf-8"))["modeller"]
    mod = k["modeller"]
    aile = {}
    for x in mod:
        e = ht.get(x)
        aile[x] = e["aile"] if e else "TABLODA_YOK"
    print("  aileler:", {x: aile[x] for x in mod})
    C = k["c_tum"]
    gr = {"CNN-CNN": [], "ViT-ViT": [], "karma": []}  # ViT-ViT: donusturucu-donusturucu (ViT, Swin, XCiT)
    for i in range(len(mod)):
        for j in range(i + 1, len(mod)):
            a, b = aile[mod[i]], aile[mod[j]]
            a = "CNN" if a == "CNN" else "DON"; b = "CNN" if b == "CNN" else "DON"
            g = "karma" if a != b else ("CNN-CNN" if a == "CNN" else "ViT-ViT")
            gr[g].append(C[i][j])
    tum = [C[i][j] for i in range(len(mod)) for j in range(i + 1, len(mod))]
    print(f"  tum ciftler: n={len(tum)} ort={st.mean(tum):.4f} min={min(tum):.4f} max={max(tum):.4f} medyan={st.median(tum):.4f}")
    for g, v in gr.items():
        if v:
            print(f"  {g}: n={len(v)} ort={st.mean(v):.4f} min={min(v):.4f} max={max(v):.4f}")
    # en kucuk ve en buyuk ciftler
    ciftler = sorted(((C[i][j], mod[i], mod[j]) for i in range(len(mod)) for j in range(i + 1, len(mod))))
    print("  en kucuk 3:", [(round(c, 4), a, b) for c, a, b in ciftler[:3]])
    print("  en buyuk 3:", [(round(c, 4), a, b) for c, a, b in ciftler[-3:]])
    if "log_gradyan_normu_ort" in k:
        print("  log_gradyan_normu_ort:", {x: round(v, 3) for x, v in k["log_gradyan_normu_ort"].items()})

print("\n==== Mantel sinamalari (tam)")
for d in ["cifar10", "cifar100", "imagenetv2"]:
    m = json.load(open(f"{R}mantel_{d}.json", encoding="utf-8"))
    for s, v in m["sinamalar"].items():
        print(f"  {d}.sinamalar.{s} = {kisa(v, 800)}")
