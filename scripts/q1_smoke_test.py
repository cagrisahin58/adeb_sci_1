"""Q1 altyapisi duman testi: hicbir tam egitim baslatmadan tum yollari dogrular.

Kontroller:
  1. Veri: CIFAR-100 + SVHN indir, 1'er parti yukle, [0,1] araligi ve
     etiket araligini dogrula; SVHN flip'in kapali oldugunu dogrula.
  2. Modeller: resnet50/vit_small (nc=10) + resnet18/vit_tiny (nc=100)
     kur, ileri+geri gecis, parametre sayilari rapor beklentisiyle karsilastir.
  3. load_model_auto: nc=100'luk gecici checkpoint'ten sinif sayisini cikar.
  4. get_attention_maps: vit_small mixin'i calisiyor mu (grid 14x14).
  5. AdversarialTrainer: 2 mini epoch (kucuk subset), save_every=1 ->
     epochs/epoch_00{1,2}.pth + metrics.jsonl + TRAINING_COMPLETE olusuyor mu;
     eps-warmup degerlendirmeyi etkilemiyor mu (base_eps korunuyor mu).
  6. Cevrimdisi secim: uretilen epoch dizisine q1_offline_select simulasyonu.
  7. Clean Trainer resume: 1 epoch egit, last.pth'tan 2. epoch'a devam et.
Cikti: results/q1/smoke_report.json (her kontrol PASS/FAIL)
"""
import json
import shutil
import sys
import tempfile
import traceback
from pathlib import Path

import torch
from torch.utils.data import DataLoader, Subset

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT))
import os
os.chdir(ROOT)

report = {}


def check(name):
    def deco(fn):
        def run():
            try:
                detail = fn()
                report[name] = {"status": "PASS", "detail": detail}
                print(f"PASS  {name}: {detail}")
            except Exception as e:
                report[name] = {"status": "FAIL", "detail": f"{type(e).__name__}: {e}"}
                print(f"FAIL  {name}: {e}")
                traceback.print_exc()
        return run
    return deco


@check("veri_cifar100")
def t_cifar100():
    from src.data import get_loaders
    tr, te = get_loaders("cifar100", data_dir="./data", batch_size=64)
    x, y = next(iter(tr))
    assert x.shape[1:] == (3, 32, 32) and 0.0 <= x.min() and x.max() <= 1.0
    assert int(y.max()) <= 99 and int(y.min()) >= 0
    return f"train={len(tr.dataset)}, test={len(te.dataset)}, y_max={int(y.max())}"


@check("veri_svhn")
def t_svhn():
    from src.data import get_loaders, DATASETS
    tr, te = get_loaders("svhn", data_dir="./data", batch_size=64)
    x, y = next(iter(tr))
    assert x.shape[1:] == (3, 32, 32) and x.max() <= 1.0
    assert len(tr.dataset) == DATASETS["svhn"]["n_train"] == 73257
    # flip kapali mi: transform zincirinde RandomHorizontalFlip olmamali
    tfs = str(tr.dataset.transform)
    assert "RandomHorizontalFlip" not in tfs, f"SVHN'de flip acik! {tfs}"
    return f"train={len(tr.dataset)}, test={len(te.dataset)}, flip=KAPALI"


@check("veri_svhn_val_split")
def t_svhn_val():
    import subprocess
    r = subprocess.run([sys.executable, "experiments/rev2/make_val_split.py",
                        "--dataset", "svhn"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-300:]
    payload = json.load(open("data/val_split_indices_svhn.json"))
    assert payload["dataset"] == "svhn" and payload["n_train_total"] == 73257
    assert max(payload["val_indices"]) < 73257
    return f"svhn val bolmesi: {len(payload['val_indices'])} indeks, n_train=73257"


@check("modeller")
def t_models():
    from src.models import ModelRegistry
    out = []
    for name, nc in [("resnet50", 10), ("vit_small", 10),
                     ("resnet18", 100), ("vit_tiny", 100)]:
        m = ModelRegistry.get(name, num_classes=nc)
        n_par = sum(p.numel() for p in m.parameters())
        x = torch.randn(2, 3, 32, 32).clamp(0, 1)
        logits = m(x)
        assert logits.shape == (2, nc), f"{name}: {logits.shape}"
        logits.sum().backward()
        out.append(f"{name}(nc={nc})={n_par/1e6:.2f}M")
    return "; ".join(out)


@check("load_model_auto")
def t_auto():
    from src.models import ModelRegistry
    from src.utils.load_model_auto import load_model_auto, infer_num_classes
    m = ModelRegistry.get("resnet18", num_classes=100)
    tmp = Path(tempfile.mkdtemp()) / "ck.pth"
    torch.save({"model_state_dict": m.state_dict()}, tmp)
    nc = infer_num_classes(torch.load(tmp, weights_only=False)["model_state_dict"])
    assert nc == 100, nc
    m2 = load_model_auto("resnet18", str(tmp), torch.device("cpu"))
    assert m2.model.fc.out_features == 100
    shutil.rmtree(tmp.parent)
    return "nc=100 checkpoint'ten dogru cikarildi"


@check("vit_small_attention")
def t_attn():
    from src.models import ModelRegistry
    m = ModelRegistry.get("vit_small", num_classes=10).eval()
    x = torch.rand(2, 3, 32, 32)
    d = m.get_attention_maps(x)
    assert d["cls_maps"].shape[0] == 2 and d["cls_maps"].shape[2:] == (14, 14)
    assert d["entropy"].shape[0] == len(m.model.blocks)
    return f"cls_maps {tuple(d['cls_maps'].shape)}, {len(d['attention'])} blok"


@check("adv_trainer_save_every")
def t_trainer():
    from src.data import get_loaders
    from src.models import ModelRegistry
    from src.training import AdversarialTrainer
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tr, te = get_loaders("cifar10", data_dir="./data", batch_size=64)
    small_tr = DataLoader(Subset(tr.dataset, list(range(256))), batch_size=64, shuffle=True)
    small_te = DataLoader(Subset(te.dataset, list(range(200))), batch_size=100)
    ckdir = Path(tempfile.mkdtemp())
    model = ModelRegistry.get("resnet18", num_classes=10)
    t = AdversarialTrainer(model=model, train_loader=small_tr, test_loader=small_te,
                           device=device, epochs=2, lr=0.01, checkpoint_dir=str(ckdir),
                           save_every=1, grad_clip=1.0, eps_warmup_epochs=2,
                           patience=0, verbose=False)
    t.train()
    eps_ok = abs(t.defense.eps - t.base_eps) < 1e-9  # degerlendirme tam eps'te birakildi
    files = sorted(p.name for p in (ckdir / "epochs").glob("*.pth"))
    metrics = (ckdir / "epochs" / "metrics.jsonl").read_text().strip().splitlines()
    complete = (ckdir / "TRAINING_COMPLETE").exists()
    assert files == ["epoch_001.pth", "epoch_002.pth"], files
    assert len(metrics) == 2 and complete and eps_ok
    ck = torch.load(ckdir / "epochs" / "epoch_001.pth", weights_only=False)
    assert "model_state_dict" in ck and "clean_acc" in ck
    # 6. kontrol: cevrimdisi secim simulasyonu ayni dizin uzerinde
    import subprocess
    outj = ckdir / "select.json"
    r = subprocess.run([sys.executable, "scripts/q1_offline_select.py",
                        "--epochs-dir", str(ckdir / "epochs"),
                        "--model-type", "resnet18", "--dataset", "cifar10",
                        "--val-indices", "data/val_split_indices.json",
                        "--out", str(outj), "--steps", "2",
                        "--test-eval", "--test-n", "200"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-400:]
    sel = json.load(open(outj))
    # test-eval sozlesmesi: secim None ise test de None; degilse npz + acc var
    assert "test" in sel
    if sel["selected_epoch"] is None:
        assert sel["test"] is None
    else:
        assert sel["test"] is not None and 0.0 <= sel["test"]["adv_acc"] <= 100.0
        assert Path(sel["test"]["per_sample_npz"]).exists()
    # SOZLESME testi: aracin sectigi epoch, ayni kayitlara C1 kuralinin
    # bagimsiz uygulanmasiyla ayni olmali (mini model %0 adv alabilir ve
    # secim mesru olarak None kalabilir - trainer'in best.pth kurali gibi)
    sys.path.insert(0, str(ROOT / "scripts"))
    from q1_offline_select import simulate_selection
    recs = [(d["epoch"], d["clean"], d["adv"]) for d in sel["records"]]
    exp_epoch, exp_adv, _ = simulate_selection(recs, patience=20, min_delta=0.1)
    assert len(recs) == 2, recs
    assert sel["selected_epoch"] == exp_epoch and sel["selected_adv_acc"] == exp_adv
    shutil.rmtree(ckdir)
    return (f"epochs/={files}, metrics={len(metrics)} satir, COMPLETE={complete}, "
            f"eps_restore={eps_ok}, offline_select={sel['selected_epoch']} "
            f"(bagimsiz simulasyonla ozdes)")


@check("clean_trainer_resume")
def t_clean_resume():
    from src.data import get_loaders
    from src.models import ModelRegistry
    from src.training import Trainer
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tr, te = get_loaders("cifar10", data_dir="./data", batch_size=64)
    small_tr = DataLoader(Subset(tr.dataset, list(range(256))), batch_size=64, shuffle=True)
    small_te = DataLoader(Subset(te.dataset, list(range(200))), batch_size=100)
    ckdir = Path(tempfile.mkdtemp())
    m = ModelRegistry.get("resnet18", num_classes=10)
    t1 = Trainer(model=m, train_loader=small_tr, test_loader=small_te, device=device,
                 epochs=1, lr=0.01, checkpoint_dir=str(ckdir), verbose=False)
    t1.train()
    assert (ckdir / "last.pth").exists() and (ckdir / "TRAINING_COMPLETE").exists()
    m2 = ModelRegistry.get("resnet18", num_classes=10)
    t2 = Trainer(model=m2, train_loader=small_tr, test_loader=small_te, device=device,
                 epochs=2, lr=0.01, checkpoint_dir=str(ckdir), verbose=False)
    t2.train(resume=True)
    hist_len = len(t2.history["train_loss"])
    assert hist_len == 2, f"resume sonrasi history {hist_len} epoch (2 bekleniyordu)"
    shutil.rmtree(ckdir)
    return f"1 epoch + resume ile 2.: history={hist_len} epoch, COMPLETE var"


if __name__ == "__main__":
    for fn_name in ["t_cifar100", "t_svhn", "t_svhn_val", "t_models", "t_auto",
                    "t_attn", "t_trainer", "t_clean_resume"]:
        globals()[fn_name]()
    out = ROOT / "results/q1/smoke_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(report, f, indent=2)
    n_fail = sum(1 for r in report.values() if r["status"] == "FAIL")
    print(f"\nTOPLAM: {len(report)} kontrol, {n_fail} FAIL -> {out}")
    sys.exit(1 if n_fail else 0)
