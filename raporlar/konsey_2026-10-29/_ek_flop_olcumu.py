"""06_ek_deney_tasarim.md icin: CPU'da rastgele agirlikli mimarilerde tek goruntu ileri gecis FLOP'u
(torch.utils.flop_counter; carpma-toplama 2 FLOP sayilir) ve parametre sayisi. Indirme yapmaz.
Konteynerde: docker exec -e CUDA_VISIBLE_DEVICES= -w /workspace adeb_eval python raporlar/konsey_2026-10-29/_ek_flop_olcumu.py"""
import io, json, sys, warnings
from datetime import datetime, timezone
warnings.filterwarnings("ignore")
sys.path.insert(0, "/workspace")
import torch, timm
import torchvision.models as tvm
from torch.utils.flop_counter import FlopCounterMode

out = {"uretildi_utc": datetime.now(timezone.utc).isoformat(), "torch": torch.__version__, "timm": timm.__version__,
       "birim": "GFLOP/goruntu (ileri gecis, 1 goruntu), param_M milyon parametre, fp32_MB = 4 bayt x parametre", "modeller": {}}

def say(ad, fn, b):
    try:
        m = fn().eval()
        x = torch.rand(1, 3, b, b)
        with FlopCounterMode(display=False) as fc, torch.no_grad():
            m(x)
        p = sum(t.numel() for t in m.parameters())
        out["modeller"][ad] = {"girdi": b, "gflop": round(fc.get_total_flops() / 1e9, 3),
                               "param_M": round(p / 1e6, 2), "fp32_MB": round(4 * p / 1e6, 1)}
    except Exception as e:
        out["modeller"][ad] = {"hata": repr(e)}
    print(ad, out["modeller"][ad], flush=True)

from src.models import ModelRegistry
from robustbench.model_zoo.architectures.wide_resnet import WideResNet
from robustbench.model_zoo.architectures.dm_wide_resnet import DMWideResNet, Swish
from robustbench.model_zoo.architectures.resnet import PreActResNet, PreActBlock, ResNet50
from robustbench.model_zoo.architectures import xcit as _rbx  # noqa: F401 (timm kaydi)
from robustbench.model_zoo.architectures.robustarch_wide_resnet import get_model as ra_get
from robustbench.model_zoo.architectures.convstem_models import get_convstem_models

# CIFAR (32 girdi)
say("c1_resnet18", lambda: ModelRegistry.get("resnet18", num_classes=10), 32)
say("c1_vit_tiny", lambda: ModelRegistry.get("vit_tiny", num_classes=10), 32)
say("c1_resnet18_224", lambda: ModelRegistry.get("resnet18_224", num_classes=10), 32)
say("rb_prn18", lambda: PreActResNet(PreActBlock, [2, 2, 2, 2]), 32)
say("rb_resnet50_cifar", lambda: ResNet50(), 32)
say("rb_wrn28_10", lambda: WideResNet(depth=28, widen_factor=10, num_classes=10), 32)
say("rb_dmwrn28_10_c100", lambda: DMWideResNet(num_classes=100, depth=28, width=10, activation_fn=Swish), 32)
say("rb_wrn34_10_c100", lambda: WideResNet(depth=34, widen_factor=10, num_classes=100), 32)
say("rb_xcit_s12_cifar10", lambda: timm.create_model("debenedetti2022light_xcit_s12_cifar10_linf", pretrained=False), 32)
# ImageNet (224 girdi)
say("tv_resnet18", tvm.resnet18, 224)
say("tv_resnet50", tvm.resnet50, 224)
say("tv_wide_resnet50_2", tvm.wide_resnet50_2, 224)
say("ra_wrn101_2", lambda: ra_get("ra_wrn101_2"), 224)
say("convnext_t_cvst", lambda: get_convstem_models("convnext_t_cvst"), 224)
say("convnext_b_cvst", lambda: get_convstem_models("convnext_b_cvst"), 224)
say("vit_s_cvst", lambda: get_convstem_models("vit_s_cvst"), 224)
say("vit_b_cvst", lambda: get_convstem_models("vit_b_cvst"), 224)
say("timm_convnext_base", lambda: timm.create_model("convnext_base"), 224)
say("timm_swin_base_patch4_window7_224", lambda: timm.create_model("swin_base_patch4_window7_224"), 224)
say("timm_vit_base_patch16_224", lambda: timm.create_model("vit_base_patch16_224"), 224)
say("timm_xcit_small_12_p16_224", lambda: timm.create_model("xcit_small_12_p16_224"), 224)

with io.open("/workspace/raporlar/konsey_2026-10-29/_ek_flop_olcumu.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("yazildi")
