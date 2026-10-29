# -*- coding: utf-8 -*-
"""K-c hiyerarsik bootstrap yolunun UC tohumlu kod sinamasi (SAHTE). SONUC DEGILDIR.

Dondurma oncesi (29.10.2026) acik kalan "K-c'nin uc tohumlu davranisi" bosluguna yonelik yalniz kod sinamasidir.
Havuz klasoru (results/q1/havuz_cifar10; ON_KAYIT §1'de gorulmus veri olarak beyanli) sekiz modeli tam caprazlar.
Uc farkli model SAHTE olarak ayni "V-scr" hucresinin uc tohumu sayilir; panel dort IN on egitimsiz CNN'dir.
Sayilar hicbir hipotez icin kanit degildir; amac (i) uc tohumla bootstrap'in calismasi, (ii) yeniden cekim
sayisinin beklenen buyuklukte olmasi (yerine koyarak uc cekimde tek farkli tohum olasiligi 3/27 = 1/9;
B = 2000 kopyada beklenen yeniden cekim yaklasik 2000 x (1/9)/(8/9) = 250),
(iii) ayni tohumun kendisiyle eslesen ciftlerin dislanmasidir.
Cikti: results/q1/_konsey_sahte/sahte_b2_kc3.json
Calistirma (konteynerde, depo kokunden): python results/q1/_konsey_sahte/kc3_sinama.py
"""
import io
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK / "experiments"))
sys.path.insert(0, str(KOK))
import q1_konsey_ayrisim as A  # noqa: E402

ARA = KOK / "results" / "q1" / "_konsey_sahte"


def m(hucre, tohum, gercek, panel=False):
    return {"hucre": hucre, "tohum": tohum, "aile": "SAHTE", "birincil_panel": panel,
            "ikincil_panel": False, "gercek_kimlik": gercek}


t = {"SINAMA_SONUC_DEGIL": True,
     "aciklama": "K-c uc tohumlu kod yolu sinamasi; SAHTE (havuz modelleri sahte V-scr tohumu sayildi)",
     "modeller": {
         "SAHTE_Va": m("V-scr", 1, "havuz ViT_Tiny_AT (C1 s2001)"),
         "SAHTE_Vb": m("V-scr", 2, "havuz ResNet18_AT (C1 s1001)"),
         "SAHTE_Vc": m("V-scr", 3, "havuz Debenedetti2022_XCiT_S12"),
         "Wong2020Fast": m("panel", None, "havuz Wong2020_PRN18", panel=True),
         "Engstrom2019Robustness": m("panel", None, "havuz Engstrom2019_RN50", panel=True),
         "Carmon2019Unlabeled": m("panel", None, "havuz Carmon2019_WRN28_10", panel=True),
         "Gowal2020Uncovering_28_10_extra": m("panel", None, "havuz Gowal2020_WRN28_10", panel=True),
     },
     "b2_tohum_ciftleri": [],
     "dizin_takma_ad_esleme": {"results/q1/havuz_cifar10": {
         "ViT_Tiny_AT": "SAHTE_Va", "ResNet18_AT": "SAHTE_Vb", "Debenedetti2022_XCiT_S12": "SAHTE_Vc",
         "Wong2020_PRN18": "Wong2020Fast", "Engstrom2019_RN50": "Engstrom2019Robustness",
         "Carmon2019_WRN28_10": "Carmon2019Unlabeled", "Gowal2020_WRN28_10": "Gowal2020Uncovering_28_10_extra"}}}

ty = ARA / "sahte_hucre_tablosu_kc3.json"
with io.open(ty, "w", encoding="utf-8", newline="\n") as f:
    json.dump(t, f, ensure_ascii=False, indent=1)
c = ARA / "sahte_b2_kc3.json"
A.main(["--mod", "b2", "--matris-dizini", "results/q1/havuz_cifar10", "--hucre-tablosu", str(ty),
        "--cikti", str(c), "--panel-en-az", "4", "--sinama"])
d = json.loads(c.read_text(encoding="utf-8"))
kc = d["b2"]["F_B2"]["K-c"]
sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps(kc, ensure_ascii=False, indent=1)[:4000])
