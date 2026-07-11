"""Vision Transformer (ViT) models for CIFAR-10."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple
import math

try:
    import timm
    TIMM_AVAILABLE = True
except ImportError:
    TIMM_AVAILABLE = False

from .base import BaseModel
from .registry import register_model


# =============================================================================
# CIFAR-Native ViT (32x32 input, 4x4 patch - no resize needed)
# =============================================================================

class PatchEmbed(nn.Module):
    """Image to Patch Embedding for CIFAR-10 (32x32)."""

    def __init__(self, img_size=32, patch_size=4, in_chans=3, embed_dim=192):
        super().__init__()
        self.img_size = img_size
        self.patch_size = patch_size
        self.num_patches = (img_size // patch_size) ** 2  # 64 for 32x32 with 4x4 patches

        self.proj = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)

    def forward(self, x):
        # x: (B, C, H, W) -> (B, embed_dim, H/patch, W/patch) -> (B, num_patches, embed_dim)
        x = self.proj(x)  # (B, embed_dim, 8, 8)
        x = x.flatten(2).transpose(1, 2)  # (B, 64, embed_dim)
        return x


class Attention(nn.Module):
    """Multi-head self-attention."""

    def __init__(self, dim, num_heads=3, qkv_bias=True, attn_drop=0., proj_drop=0.):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        self.scale = self.head_dim ** -0.5

        self.qkv = nn.Linear(dim, dim * 3, bias=qkv_bias)
        self.attn_drop = nn.Dropout(attn_drop)
        self.proj = nn.Linear(dim, dim)
        self.proj_drop = nn.Dropout(proj_drop)

    def forward(self, x):
        B, N, C = x.shape
        qkv = self.qkv(x).reshape(B, N, 3, self.num_heads, self.head_dim).permute(2, 0, 3, 1, 4)
        q, k, v = qkv.unbind(0)

        attn = (q @ k.transpose(-2, -1)) * self.scale
        attn = attn.softmax(dim=-1)
        attn = self.attn_drop(attn)

        x = (attn @ v).transpose(1, 2).reshape(B, N, C)
        x = self.proj(x)
        x = self.proj_drop(x)
        return x, attn


class MLP(nn.Module):
    """MLP block."""

    def __init__(self, in_features, hidden_features=None, out_features=None, drop=0.):
        super().__init__()
        out_features = out_features or in_features
        hidden_features = hidden_features or in_features * 4

        self.fc1 = nn.Linear(in_features, hidden_features)
        self.act = nn.GELU()
        self.fc2 = nn.Linear(hidden_features, out_features)
        self.drop = nn.Dropout(drop)

    def forward(self, x):
        x = self.fc1(x)
        x = self.act(x)
        x = self.drop(x)
        x = self.fc2(x)
        x = self.drop(x)
        return x


class TransformerBlock(nn.Module):
    """Transformer encoder block."""

    def __init__(self, dim, num_heads, mlp_ratio=4., qkv_bias=True, drop=0., attn_drop=0.):
        super().__init__()
        self.norm1 = nn.LayerNorm(dim)
        self.attn = Attention(dim, num_heads=num_heads, qkv_bias=qkv_bias,
                             attn_drop=attn_drop, proj_drop=drop)
        self.norm2 = nn.LayerNorm(dim)
        self.mlp = MLP(in_features=dim, hidden_features=int(dim * mlp_ratio), drop=drop)

    def forward(self, x, return_attention=False):
        attn_out, attn_weights = self.attn(self.norm1(x))
        x = x + attn_out
        x = x + self.mlp(self.norm2(x))
        if return_attention:
            return x, attn_weights
        return x


class CIFARViT(nn.Module):
    """
    CIFAR-native Vision Transformer.

    Designed for 32x32 images with 4x4 patches (64 patches total).
    No resizing needed - efficient for CIFAR-10.
    """

    def __init__(self, img_size=32, patch_size=4, in_chans=3, num_classes=10,
                 embed_dim=192, depth=12, num_heads=3, mlp_ratio=4.,
                 qkv_bias=True, drop_rate=0., attn_drop_rate=0.):
        super().__init__()
        self.num_classes = num_classes
        self.embed_dim = embed_dim

        # Patch embedding
        self.patch_embed = PatchEmbed(img_size, patch_size, in_chans, embed_dim)
        num_patches = self.patch_embed.num_patches

        # Class token and position embedding
        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        self.pos_embed = nn.Parameter(torch.zeros(1, num_patches + 1, embed_dim))
        self.pos_drop = nn.Dropout(p=drop_rate)

        # Transformer blocks
        self.blocks = nn.ModuleList([
            TransformerBlock(embed_dim, num_heads, mlp_ratio, qkv_bias, drop_rate, attn_drop_rate)
            for _ in range(depth)
        ])

        # Final norm and head
        self.norm = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, num_classes)

        # Initialize weights
        self._init_weights()

    def _init_weights(self):
        nn.init.trunc_normal_(self.pos_embed, std=0.02)
        nn.init.trunc_normal_(self.cls_token, std=0.02)
        self.apply(self._init_weights_module)

    def _init_weights_module(self, m):
        if isinstance(m, nn.Linear):
            nn.init.trunc_normal_(m.weight, std=0.02)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.LayerNorm):
            nn.init.zeros_(m.bias)
            nn.init.ones_(m.weight)

    def forward_features(self, x):
        B = x.shape[0]
        x = self.patch_embed(x)

        cls_tokens = self.cls_token.expand(B, -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)
        x = x + self.pos_embed
        x = self.pos_drop(x)

        for blk in self.blocks:
            x = blk(x)

        x = self.norm(x)
        return x[:, 0]  # Return CLS token

    def forward(self, x):
        x = self.forward_features(x)
        x = self.head(x)
        return x

    def get_attention_maps(self, x):
        """Get attention maps from all layers."""
        B = x.shape[0]
        x = self.patch_embed(x)

        cls_tokens = self.cls_token.expand(B, -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)
        x = x + self.pos_embed
        x = self.pos_drop(x)

        attention_maps = []
        for blk in self.blocks:
            x, attn = blk(x, return_attention=True)
            attention_maps.append(attn)

        return attention_maps


@register_model("vit_cifar_tiny")
class CIFAR10ViTCIFARTiny(BaseModel):
    """
    CIFAR-native ViT-Tiny.

    Architecture: 32x32 input, 4x4 patch, 192 dim, 12 layers, 3 heads
    Parameters: ~5.5M (vs ~5.7M for timm vit_tiny with resize)
    """

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        super().__init__(num_classes=num_classes)

        self.model = CIFARViT(
            img_size=32,
            patch_size=4,
            num_classes=num_classes,
            embed_dim=192,
            depth=12,
            num_heads=3,
            mlp_ratio=4.,
            drop_rate=0.1,
            attn_drop_rate=0.0,
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        return self.model.forward_features(x)

    def get_attention_maps(self, x: torch.Tensor):
        """Get attention maps for analysis."""
        return self.model.get_attention_maps(x)

    @property
    def input_size(self) -> Tuple[int, int]:
        return (32, 32)


@register_model("vit_cifar_small")
class CIFAR10ViTCIFARSmall(BaseModel):
    """
    CIFAR-native ViT-Small.

    Architecture: 32x32 input, 4x4 patch, 384 dim, 12 layers, 6 heads
    Parameters: ~21.7M
    """

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        super().__init__(num_classes=num_classes)

        self.model = CIFARViT(
            img_size=32,
            patch_size=4,
            num_classes=num_classes,
            embed_dim=384,
            depth=12,
            num_heads=6,
            mlp_ratio=4.,
            drop_rate=0.1,
            attn_drop_rate=0.0,
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        return self.model.forward_features(x)

    def get_attention_maps(self, x: torch.Tensor):
        return self.model.get_attention_maps(x)

    @property
    def input_size(self) -> Tuple[int, int]:
        return (32, 32)


# =============================================================================
# Original timm-based ViT models (with 224x224 resize)
# =============================================================================


@register_model("vit_tiny")
class CIFAR10ViTTiny(BaseModel):
    """
    ViT-Tiny adapted for CIFAR-10.

    Uses timm library's vit_tiny_patch16_224 model.
    Input images are resized to 224x224 for patch-based processing.
    """

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        """
        Initialize ViT-Tiny for CIFAR-10.

        Args:
            num_classes: Number of output classes (default: 10)
            pretrained: Whether to use pretrained weights (default: False)
        """
        super().__init__(num_classes=num_classes)

        if not TIMM_AVAILABLE:
            raise ImportError(
                "timm library is required for ViT models. "
                "Install it with: pip install timm"
            )

        self.model = timm.create_model(
            "vit_tiny_patch16_224",
            pretrained=pretrained,
            num_classes=num_classes,
        )

        # Resize layer for CIFAR-10 (32x32 -> 224x224)
        self.resize = nn.Upsample(size=(224, 224), mode="bilinear", align_corners=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Resize input from 32x32 to 224x224
        x = self.resize(x)
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        """Get features before the final classification head."""
        x = self.resize(x)
        return self.model.forward_features(x)

    @torch.no_grad()
    def get_attention_maps(self, x: torch.Tensor):
        """
        Extract real post-softmax attention weights from every block.

        timm'in fused SDPA yolu attention matrisini hic olusturmaz; bu yuzden
        gecici olarak fused_attn=False yapilir ve attn_drop uzerine hook
        takilir (M1: onceki figur kodu torch.rand ile sahte attention uretiyordu).

        Args:
            x: Input images in [0,1], shape (B, 3, 32, 32)

        Returns:
            Dict with:
              'attention': list of L tensors (B, heads, N, N), post-softmax
              'cls_maps': tensor (B, L, 14, 14) - CLS-row attention over the
                  196 patches, averaged over heads
              'entropy': tensor (L,) - mean entropy of CLS-row attention
                  distributions per layer
        """
        blocks = self.model.blocks
        captured = []
        hooks = []
        old_fused = []

        def hook(module, inputs, output):
            # attn_drop input/output: (B, heads, N, N) post-softmax attention
            captured.append(output.detach())

        for blk in blocks:
            old_fused.append(getattr(blk.attn, "fused_attn", None))
            if hasattr(blk.attn, "fused_attn"):
                blk.attn.fused_attn = False
            hooks.append(blk.attn.attn_drop.register_forward_hook(hook))

        try:
            _ = self.model(self.resize(x))
        finally:
            for h in hooks:
                h.remove()
            for blk, flag in zip(blocks, old_fused):
                if flag is not None:
                    blk.attn.fused_attn = flag

        if len(captured) != len(blocks):
            raise RuntimeError(
                f"Expected {len(blocks)} attention tensors, captured {len(captured)}; "
                "timm Attention module layout may have changed."
            )

        # CLS-row attention: (B, heads, N, N) -> row 0, patch columns 1..N-1
        cls_rows = []
        entropies = []
        for attn in captured:
            cls_row = attn[:, :, 0, 1:]           # (B, heads, 196)
            cls_row = cls_row.mean(dim=1)          # (B, 196), head-averaged
            # Entropy of the (renormalized) CLS->patch distribution
            p = cls_row / (cls_row.sum(dim=-1, keepdim=True) + 1e-12)
            entropies.append(-(p * (p + 1e-12).log()).sum(dim=-1).mean())
            grid = int(cls_row.shape[-1] ** 0.5)   # 14 for 196 patches
            cls_rows.append(cls_row.reshape(-1, grid, grid))

        return {
            "attention": captured,
            "cls_maps": torch.stack(cls_rows, dim=1),   # (B, L, 14, 14)
            "entropy": torch.stack(entropies),           # (L,)
        }

    def freeze_backbone(self) -> None:
        """Freeze all layers except the classification head."""
        for name, param in self.model.named_parameters():
            if "head" not in name:
                param.requires_grad = False

    @property
    def input_size(self) -> Tuple[int, int]:
        return (32, 32)  # Native input, resized internally


@register_model("vit_small")
class CIFAR10ViTSmall(BaseModel):
    """ViT-Small adapted for CIFAR-10."""

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        super().__init__(num_classes=num_classes)

        if not TIMM_AVAILABLE:
            raise ImportError(
                "timm library is required for ViT models. "
                "Install it with: pip install timm"
            )

        self.model = timm.create_model(
            "vit_small_patch16_224",
            pretrained=pretrained,
            num_classes=num_classes,
        )

        self.resize = nn.Upsample(size=(224, 224), mode="bilinear", align_corners=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.resize(x)
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        x = self.resize(x)
        return self.model.forward_features(x)

    def freeze_backbone(self) -> None:
        for name, param in self.model.named_parameters():
            if "head" not in name:
                param.requires_grad = False


@register_model("vit_base")
class CIFAR10ViTBase(BaseModel):
    """ViT-Base adapted for CIFAR-10."""

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        super().__init__(num_classes=num_classes)

        if not TIMM_AVAILABLE:
            raise ImportError(
                "timm library is required for ViT models. "
                "Install it with: pip install timm"
            )

        self.model = timm.create_model(
            "vit_base_patch16_224",
            pretrained=pretrained,
            num_classes=num_classes,
        )

        self.resize = nn.Upsample(size=(224, 224), mode="bilinear", align_corners=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.resize(x)
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        x = self.resize(x)
        return self.model.forward_features(x)

    def freeze_backbone(self) -> None:
        for name, param in self.model.named_parameters():
            if "head" not in name:
                param.requires_grad = False
