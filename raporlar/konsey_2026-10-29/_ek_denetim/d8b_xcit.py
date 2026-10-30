import inspect, timm, robustbench, robustbench.utils as U
import robustbench.model_zoo.imagenet
for n in ("debenedetti2022light_xcit_s12_imagenet_linf", "debenedetti2022light_xcit_s12_cifar100_linf", "debenedetti2022light_xcit_s12_cifar10_linf"):
    cfg = timm.models.get_pretrained_cfg(n)
    print(n, getattr(cfg, "url", None) or getattr(cfg, "hf_hub_id", None), getattr(cfg, "mean", None), getattr(cfg, "std", None))
src = inspect.getsource(U.load_model)
i = src.find("timm")
print(src[max(0, i-400): i+900])
