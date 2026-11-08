#!/usr/bin/env python
"""Dump the real structure of the two 2x2 architectures as the project builds them.

    python paper/figures/onizleme_v2/pv_b_yapi.py      (from the repository root)

Builds src/models/vit.py CIFAR10ViTTiny (V-scr wrapper, timm vit_tiny_patch16_224) and
src/models/r224.py CIFAR10ResNet18R224 (R224-scr wrapper, timm resnet18) with random
weights (no download), runs one 1 x 3 x 32 x 32 zero tensor through each with forward
hooks and writes every number the exploded-model preview prints to
paper/figures/onizleme_v2/pv_b_model_yapisi.txt (one "key = value" per line, so the
evidence file can cite file:line) and pv_b_model_yapisi.json (same keys).
Nothing is trained, nothing is read from results/.
"""
from __future__ import annotations

import io
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
OUT = Path("paper/figures/onizleme_v2")

import torch  # noqa: E402
import timm  # noqa: E402
from src.models.vit import CIFAR10ViTTiny  # noqa: E402
from src.models.r224 import CIFAR10ResNet18R224  # noqa: E402


def nparam(m):
    return int(sum(p.numel() for p in m.parameters()))


def main():
    torch.manual_seed(0)
    rows = []          # (key, value, note)

    def put(k, v, note=""):
        rows.append((k, v, note))

    put("torch.version", torch.__version__)
    put("timm.version", timm.__version__)
    # ------------------------------------------------------------- ViT-Tiny (V-scr wrapper)
    vit = CIFAR10ViTTiny(num_classes=10, pretrained=False).eval()
    vm = vit.model
    put("vit.wrapper", "src/models/vit.py:361 CIFAR10ViTTiny")
    put("vit.timm_name", "vit_tiny_patch16_224", "src/models/vit.py:386")
    pe = vm.patch_embed
    put("vit.input_hw", list(pe.img_size), "patch_embed.img_size (model-internal resize 32->224)")
    put("vit.patch", list(pe.patch_size), "patch_embed.patch_size")
    put("vit.grid", list(pe.grid_size), "patch_embed.grid_size")
    put("vit.num_patches", int(pe.num_patches))
    put("vit.embed_dim", int(vm.embed_dim))
    put("vit.cls_token", int(vm.cls_token.shape[1]) if vm.cls_token is not None else 0)
    put("vit.tokens", int(pe.num_patches) + (int(vm.cls_token.shape[1]) if vm.cls_token is not None else 0))
    put("vit.depth", len(vm.blocks))
    b0 = vm.blocks[0]
    put("vit.heads", int(b0.attn.num_heads))
    put("vit.head_dim", int(b0.attn.head_dim))
    put("vit.mlp_hidden", int(b0.mlp.fc1.out_features))
    put("vit.qkv_out", int(b0.attn.qkv.out_features), "attn.qkv: one linear map to Q, K and V (3 x embed_dim)")
    put("vit.mlp_act", type(b0.mlp.act).__name__)
    put("vit.norm", type(b0.norm1).__name__)
    put("vit.head_out", int(vm.head.out_features))
    put("vit.global_pool", str(vm.global_pool), "timm VisionTransformer.global_pool; 'token' = the CLS token feeds the head")
    put("vit.params", nparam(vit))
    put("vit.params_blocks", nparam(vm.blocks))
    put("vit.params_one_block", nparam(b0))
    put("vit.params_patch_embed", nparam(pe))
    shapes = {}
    hooks = [pe.register_forward_hook(lambda m, i, o: shapes.__setitem__("patch_embed", list(o.shape))),
             vm.blocks[0].register_forward_hook(lambda m, i, o: shapes.__setitem__("block0", list(o.shape))),
             vm.blocks[-1].register_forward_hook(lambda m, i, o: shapes.__setitem__("block_last", list(o.shape))),
             vm.head.register_forward_hook(lambda m, i, o: shapes.__setitem__("head", list(o.shape)))]
    with torch.no_grad():
        vit(torch.zeros(1, 3, 32, 32))
    for h in hooks:
        h.remove()
    put("vit.shape.patch_embed", shapes["patch_embed"], "forward hook, input 1x3x32x32")
    put("vit.shape.block0", shapes["block0"])
    put("vit.shape.block_last", shapes["block_last"])
    put("vit.shape.head", shapes["head"])
    # ------------------------------------------------------------- ResNet-18 (R224-scr wrapper)
    res = CIFAR10ResNet18R224(num_classes=10, pretrained=False).eval()
    rm = res.model
    from src.models import r224 as _r224
    put("vit.in_init_timm_name", _r224.INIT_WEIGHTS["deit_tiny_in1k"][0] if hasattr(_r224, "INIT_WEIGHTS") else
        "deit_tiny_patch16_224.fb_in1k", "src/models/r224.py:48 (V-IN initialisation weights)")
    put("res.wrapper", "src/models/r224.py:139 CIFAR10ResNet18R224")
    put("res.timm_name", "resnet18", "src/models/r224.py:114")
    put("res.stem_kernel", list(rm.conv1.kernel_size))
    put("res.stem_stride", list(rm.conv1.stride))
    put("res.stem_out", int(rm.conv1.out_channels))
    put("res.maxpool_kernel", int(rm.maxpool.kernel_size) if isinstance(rm.maxpool.kernel_size, int)
        else list(rm.maxpool.kernel_size))
    put("res.maxpool_stride", int(rm.maxpool.stride) if isinstance(rm.maxpool.stride, int)
        else list(rm.maxpool.stride))
    stages = [rm.layer1, rm.layer2, rm.layer3, rm.layer4]
    put("res.stages", len(stages))
    shp = {}
    hk = [rm.conv1.register_forward_hook(lambda m, i, o: shp.__setitem__("stem", list(o.shape))),
          rm.maxpool.register_forward_hook(lambda m, i, o: shp.__setitem__("maxpool", list(o.shape))),
          rm.global_pool.register_forward_hook(lambda m, i, o: shp.__setitem__("pool", list(o.shape))),
          rm.fc.register_forward_hook(lambda m, i, o: shp.__setitem__("fc", list(o.shape)))]
    for si, st in enumerate(stages, 1):
        hk.append(st.register_forward_hook(lambda m, i, o, si=si: shp.__setitem__(f"layer{si}", list(o.shape))))
    with torch.no_grad():
        res(torch.zeros(1, 3, 32, 32))
    for h in hk:
        h.remove()
    put("res.shape.stem", shp["stem"], "forward hook, input 1x3x32x32 (resized to 224 inside)")
    put("res.shape.maxpool", shp["maxpool"])
    for si, st in enumerate(stages, 1):
        put(f"res.layer{si}.blocks", len(st))
        put(f"res.layer{si}.block_type", type(st[0]).__name__)
        put(f"res.layer{si}.convs_per_block", sum(1 for n, _ in st[0].named_children() if n.startswith("conv")))
        put(f"res.layer{si}.kernel", list(st[0].conv1.kernel_size))
        put(f"res.layer{si}.channels", int(st[0].conv2.out_channels))
        put(f"res.layer{si}.shape", shp[f"layer{si}"])
        put(f"res.layer{si}.params", nparam(st))
        put(f"res.layer{si}.block_children", [f"{n}:{type(m).__name__}" for n, m in st[0].named_children()
                                              if m is not None])
        put(f"res.layer{si}.block_last_children", [f"{n}:{type(m).__name__}" for n, m in st[-1].named_children()
                                                   if m is not None], "the stage's last BasicBlock")
    put("res.shape.pool", shp["pool"])
    put("res.shape.fc", shp["fc"])
    put("res.fc_out", int(rm.fc.out_features))
    put("res.params", nparam(res))
    convs = sum(1 for m in rm.modules() if isinstance(m, torch.nn.Conv2d))
    put("res.conv_layers_total", convs, "includes the three 1x1 downsample convs")
    put("res.conv_layers_main_path", 1 + sum(len(st) * 2 for st in stages), "stem + 2 per BasicBlock")
    put("res.weighted_layers_main_path", 1 + sum(len(st) * 2 for st in stages) + 1, "the '18': convs + fc")
    lines = ["# pv_b_model_yapisi.txt: written by paper/figures/onizleme_v2/pv_b_yapi.py",
             "# key = value   (note); line numbers are cited by pv_b_model_exploded.kanit.json"]
    for k, v, note in rows:
        lines.append(f"{k} = {json.dumps(v)}" + (f"   ({note})" if note else ""))
    with io.open(OUT / "pv_b_model_yapisi.txt", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with io.open(OUT / "pv_b_model_yapisi.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump({k: v for k, v, _ in rows}, fh, indent=1)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
