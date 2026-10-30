import json
from pathlib import Path
K = Path("/home/firat/projects/adeb_sci_1")
T = K / "raporlar/konsey_2026-10-29"
d = json.loads((T / "hucre_tablosu.json").read_text(encoding="utf-8"))
for ad in ("hucre_tablosu_b8.json", "hucre_tablosu_b9.json"):
    e = json.loads((T / ad).read_text(encoding="utf-8"))
    print(ad, "ust anahtar ayni:", sorted(d) == sorted(e), "hucre anahtar ayni:", sorted(d["hucreler"]) == sorted(e["hucreler"]))
    alan = {tuple(sorted(v)) for v in d["modeller"].values()}
    alan_e = {tuple(sorted(v)) for v in e["modeller"].values()}
    print("  model alanlari ayni:", alan == alan_e, "hucre degerleri:", sorted({v["hucre"] for v in e["modeller"].values()}),
          "aile:", sorted({v["aile"] for v in e["modeller"].values()}), "model sayisi:", len(e["modeller"]),
          "birincil:", sum(v["birincil_panel"] for v in e["modeller"].values()), "ikincil:", sum(v["ikincil_panel"] for v in e["modeller"].values()))
    for c in e["b2_tohum_ciftleri"]:
        assert all(x in e["modeller"] for x in c), c
    for m, v in e["modeller"].items():
        kn = v["kontrol_noktasi"]
        if kn.startswith("models/"):
            p = K / kn
            print("  ", m, "var" if p.exists() else "YOK", "bag" if p.is_symlink() else "", p.stat().st_size if p.exists() else "")
