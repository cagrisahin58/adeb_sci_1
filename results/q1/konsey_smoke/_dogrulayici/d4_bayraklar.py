"""Celisik dogrulayici, D4: kuyruk --dry-run ciktisindaki ve runbook'taki her
komutun bayraklarini, komutu CALISTIRMADAN gercek ayristiricilarla ayristirir.

  cli.main train clean/adversarial : click make_context (secenek ve secim denetimi)
  argparse betikleri               : parse_args yakalanir, main() parse sonrasi kesilir
  konsey_b3_kuyruk.sh              : betigin case blogundaki bayraklarla karsilastirma
Ayrica takma adlarin K5 ve hucre_tablosu.json ile uyumu denetlenir.
Kullanim: python d4_bayraklar.py DRY_RUN_TXT CIKTI_JSON
"""
import argparse
import json
import re
import runpy
import shlex
import sys
from pathlib import Path

sys.path.insert(0, "/workspace")
import click  # noqa: E402

from cli.main import cli  # noqa: E402

dry_txt, cikti = Path(sys.argv[1]), Path(sys.argv[2])
sonuc = {"kuyruk": [], "runbook": [], "takma_ad": {}}


class Ayristirildi(Exception):
    pass


_orig = argparse.ArgumentParser.parse_args


def _yakala(self, args=None, namespace=None):
    ns = _orig(self, args, namespace)
    raise Ayristirildi(vars(ns))


def argparse_ayristir(betik, argv):
    argparse.ArgumentParser.parse_args = _yakala
    eski = sys.argv
    sys.argv = [betik] + argv
    try:
        runpy.run_path(betik, run_name="__main__")
        return {"durum": "AYRISTIRILAMADI (parse_args cagrilmadi)"}
    except Ayristirildi as e:
        return {"durum": "OK", "ns": {k: v for k, v in e.args[0].items()}}
    except SystemExit as e:
        return {"durum": f"HATA SystemExit {e.code}"}
    finally:
        sys.argv = eski
        argparse.ArgumentParser.parse_args = _orig


def click_ayristir(argv):
    # argv: ["train", "clean", ...]
    grp = cli.commands[argv[0]]
    cmd = grp.commands[argv[1]]
    try:
        ctx = cmd.make_context(argv[1], list(argv[2:]), resilient_parsing=False)
        return {"durum": "OK", "ns": {k: v for k, v in ctx.params.items()}}
    except click.exceptions.ClickException as e:
        return {"durum": f"HATA {type(e).__name__}: {e.format_message()}"}
    except click.exceptions.Exit as e:
        return {"durum": f"HATA Exit {e.exit_code}"}


def komut_ayristir(argv):
    if argv[:3] == ["python", "-m", "cli.main"]:
        return click_ayristir(argv[3:])
    if argv[0] == "python" and argv[1].endswith(".py"):
        return argparse_ayristir(argv[1], argv[2:])
    if argv[0] == "bash" and argv[1].endswith("konsey_b3_kuyruk.sh"):
        txt = Path(argv[1]).read_text()
        bilinen = set(re.findall(r"^\s+(--[a-z-]+)\)", txt, flags=re.M))
        bayr = [a for a in argv[2:] if a.startswith("--")]
        bil = [b for b in bayr if b not in bilinen]
        return {"durum": "OK" if not bil else f"HATA bilinmeyen {bil}", "bilinen": sorted(bilinen)}
    return {"durum": "ATLANDI (tanimsiz)"}


# --- 1) kuyruk --dry-run komutlari ------------------------------------------
for satir in dry_txt.read_text().splitlines():
    m = re.match(r"^\[(temiz|AT|denetim|izleme|ozet)\]\s+(.*)$", satir)
    if not m:
        continue
    govde = m.group(2).split("#")[0].strip()
    govde = govde.replace("her 5 dk: ", "")
    if not govde.startswith("python"):
        continue
    argv = shlex.split(govde)
    r = komut_ayristir(argv)
    kayit = {"etiket": m.group(1), "komut": govde, "durum": r["durum"]}
    if m.group(1) in ("temiz", "AT") and r["durum"] == "OK":
        ns = r["ns"]
        kayit["ozet"] = {k: ns.get(k) for k in (
            "model", "init_weights", "optimizer_name", "lr_schedule", "epochs", "lr", "batch_size",
            "seed", "val_indices", "output_dir", "resume", "stop_epoch", "patience", "save_every",
            "pretrained", "defense", "grad_clip", "vit_lr_cap", "eps", "alpha", "steps",
            "lr_warmup", "eps_warmup") if k in ns}
    sonuc["kuyruk"].append(kayit)

# --- 2) runbook komutlari ----------------------------------------------------
rb = Path("raporlar/konsey_2026-10-29/KONSEY_RUNBOOK.md").read_text()
bloklar = re.findall(r"```bash\n(.*?)```", rb, flags=re.S)
# metin icindeki satir ici komutlar (`docker exec ... python ...`)
satir_ici = [m for m in re.findall(r"`(docker exec[^`]*python[^`]*)`", re.sub(r"```.*?```", "", rb, flags=re.S))]
bloklar = bloklar + satir_ici
sonuc["runbook_satir_ici_komut_sayisi"] = len(satir_ici)
degisken = {}
for blok in bloklar:
    blok = blok.replace("\\\n", " ")
    for ad, deger in re.findall(r'^([A-Z0-9]+)="(.*?)"\s*$', blok, flags=re.M):
        degisken[ad] = deger
for blok in bloklar:
    blok = blok.replace("\\\n", " ")
    for ad, deger in degisken.items():
        blok = blok.replace("$" + ad, deger)
    for pm in re.finditer(r"(python [^\s]+\.py|python -m cli\.main|bash scripts/[^\s]+\.sh)(.*?)(?=\s>\s|\s&&\s|\"|\||$)",
                          blok, flags=re.M):
        govde = (pm.group(1) + pm.group(2)).strip()
        argv = shlex.split(govde)
        r = komut_ayristir(argv)
        kayit = {"komut_basi": " ".join(argv[:2]), "arguman_sayisi": len(argv), "durum": r["durum"]}
        if r["durum"] == "OK" and "ns" in r:
            ns = r["ns"]
            kayit["ozet"] = {k: ns[k] for k in ("model", "rb_model", "sources", "attack", "cache_adv",
                                                  "skip_existing", "out_dir", "output_dir", "n_samples",
                                                  "mod", "matris_dizini", "hucre_tablosu", "cikti",
                                                  "seed", "dataset") if k in ns}
        sonuc["runbook"].append(kayit)

# --- 3) takma adlar: K5, hucre_tablosu, runbook, kuyruk ---------------------
K5 = (["ResNet18_AT_s1001", "ResNet18_AT_s1002", "ResNet18_AT_s1003",
       "ViT_Tiny_AT_s2001", "ViT_Tiny_AT_s2002", "ViT_Tiny_AT_s2003"]
      + ["Wong2020Fast", "Engstrom2019Robustness", "Carmon2019Unlabeled",
         "Gowal2020Uncovering_28_10_extra", "Sehwag2021Proxy_R18", "Addepalli2022Efficient_RN18",
         "Rade2021Helper_R18_ddpm", "Debenedetti2022Light_XCiT-S12"]
      + ["V_IN_s2101", "V_IN_s2102", "R224_IN_s1301", "R224_IN_s1302", "R224_scr_s1201", "R224_scr_s1202"])
K5_YOL = {}
for s in (1001, 1002, 1003):
    K5_YOL[f"ResNet18_AT_s{s}"] = f"models/c1/resnet18_s{s}/resnet18/adv/adversarial_training/best.pth"
for s in (2001, 2002, 2003):
    K5_YOL[f"ViT_Tiny_AT_s{s}"] = f"models/c1/vit_tiny_s{s}/vit_tiny/adv/adversarial_training/best.pth"
ht = json.loads(Path("raporlar/konsey_2026-10-29/hucre_tablosu.json").read_text())
ht_ad = list(ht["modeller"])
sonuc["takma_ad"]["k5_eksik_tabloda"] = [a for a in K5 if a not in ht_ad]
sonuc["takma_ad"]["tabloda_fazla"] = [a for a in ht_ad if a not in K5]
sonuc["takma_ad"]["c1_yol_uyusmazligi"] = {a: ht["modeller"][a]["kontrol_noktasi"] for a in K5_YOL
                                           if ht["modeller"][a]["kontrol_noktasi"] != K5_YOL[a]}
sonuc["takma_ad"]["c1_yol_diskte_var"] = {a: Path(p).exists() for a, p in K5_YOL.items()}
yeni = [a for a in K5 if "_s21" in a or "_s12" in a or "_s13" in a]
sonuc["takma_ad"]["yeni_tablo_yolu_k5_kalibi"] = {
    a: ht["modeller"][a]["kontrol_noktasi"] == f"models/q1/konsey/{a}/" for a in yeni}
# runbook'ta --model AD:TIP:YOL ve --rb-model AD
rb_tek = rb.replace("\\\n", " ")
rb_model = re.findall(r"--model ([A-Za-z0-9_\-]+):([a-z0-9_]+):([^\s\"]+)", rb_tek)
rb_rb = re.findall(r"--rb-model ([A-Za-z0-9_\-]+)", rb_tek)
sonuc["takma_ad"]["runbook_model_k5_disi"] = sorted({a for a, _, _ in rb_model if a not in K5})
sonuc["takma_ad"]["runbook_rb_k5_disi"] = sorted({a for a in rb_rb if a not in K5})
yol_uyusmaz = []
for a, tip, yol in rb_model:
    if a in K5_YOL and yol != K5_YOL[a]:
        yol_uyusmaz.append([a, yol])
    if a in yeni:
        bek = f"models/q1/konsey/{a}/{tip}/adv/adversarial_training/best.pth"
        if yol != bek:
            yol_uyusmaz.append([a, yol])
        tip_bek = {"V_IN": "vit_tiny_in1k", "R224_IN": "resnet18_224_in1k", "R224_scr": "resnet18_224"}[a.rsplit("_s", 1)[0]]
        if tip != tip_bek:
            yol_uyusmaz.append([a, "tip " + tip])
sonuc["takma_ad"]["runbook_yol_tip_uyusmazligi"] = yol_uyusmaz
kuyruk_ad = re.findall(r"^## (\S+)$", dry_txt.read_text(), flags=re.M)
sonuc["takma_ad"]["kuyruk_sirasi"] = kuyruk_ad
sonuc["takma_ad"]["kuyruk_k5_disi"] = [a for a in kuyruk_ad if a not in K5]
sonuc["takma_ad"]["s4_ciftleri_k5_ici"] = all(a in K5 for c in ht["s4_ciftleri"] for a in c)
sonuc["takma_ad"]["b2_ciftleri_k5_ici"] = all(a in K5 for c in ht["b2_tohum_ciftleri"] for a in c)

ozet = {"kuyruk_komut": len(sonuc["kuyruk"]),
        "kuyruk_hata": [k for k in sonuc["kuyruk"] if k["durum"] != "OK"],
        "runbook_komut": len(sonuc["runbook"]),
        "runbook_hata": [k for k in sonuc["runbook"] if k["durum"] != "OK"]}
sonuc["OZET"] = ozet
cikti.write_text(json.dumps(sonuc, indent=1, ensure_ascii=False, default=str))
print(json.dumps(ozet, indent=1, ensure_ascii=False, default=str))
print(json.dumps(sonuc["takma_ad"], indent=1, ensure_ascii=False, default=str))
