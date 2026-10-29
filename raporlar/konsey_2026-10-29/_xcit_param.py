"""XCiT CIFAR varyantlarinin parametre sayisi (agirlik indirmeden, pretrained=False)."""
import os
import timm
import robustbench.model_zoo.architectures.xcit  # noqa: F401  (timm'e kayit)
for n in ["debenedetti2020light_xcit_s_cifar10_linf", "debenedetti2020light_xcit_m_cifar10_linf",
          "debenedetti2020light_xcit_l_cifar10_linf"]:
    try:
        m = timm.create_model(n, pretrained=False)
        print(n, round(sum(p.numel() for p in m.parameters()) / 1e6, 2), "M")
    except Exception as e:
        print(n, "HATA", repr(e)[:200])
p = "/root/.cache/torch/hub/checkpoints/debenedetti2022light-xcit-s-cifar10-linf.pth.tar"
print("onbellek", p, os.path.getsize(p) if os.path.exists(p) else "yok")
