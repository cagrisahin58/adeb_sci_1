"""Model checkpointing utilities."""

import torch
from pathlib import Path
from typing import Optional, Dict, Any
import torch.nn as nn


def save_checkpoint(
    model: nn.Module,
    path: str,
    optimizer: Optional[torch.optim.Optimizer] = None,
    scheduler: Optional[Any] = None,
    epoch: Optional[int] = None,
    accuracy: Optional[float] = None,
    extra_info: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Save a model checkpoint.

    Args:
        model: The model to save
        path: Path to save the checkpoint
        optimizer: Optional optimizer state
        scheduler: Optional scheduler state
        epoch: Current epoch number
        accuracy: Current accuracy
        extra_info: Any additional information to save
    """
    save_path = Path(path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    checkpoint = {
        "model_state_dict": model.state_dict(),
    }

    if optimizer is not None:
        checkpoint["optimizer_state_dict"] = optimizer.state_dict()

    if scheduler is not None:
        checkpoint["scheduler_state_dict"] = scheduler.state_dict()

    if epoch is not None:
        checkpoint["epoch"] = epoch

    if accuracy is not None:
        checkpoint["accuracy"] = accuracy

    if extra_info is not None:
        checkpoint.update(extra_info)

    # Atomik yaz (Q1): best.pth dahil hicbir checkpoint yarim halde gorunmesin
    # (yazim sirasinda kesinti eski dosyayi bozmaz). Cagiranlarin kendi
    # .tmp+replace desenleri zararsiz bicimde ikinci kez rename yapar.
    tmp_path = save_path.with_name(save_path.name + ".tmp")
    torch.save(checkpoint, tmp_path)
    tmp_path.replace(save_path)


def load_checkpoint(
    path: str,
    model: Optional[nn.Module] = None,
    optimizer: Optional[torch.optim.Optimizer] = None,
    scheduler: Optional[Any] = None,
    device: Optional[torch.device] = None,
) -> Dict[str, Any]:
    """
    Load a model checkpoint.

    Args:
        path: Path to the checkpoint
        model: Optional model to load state into
        optimizer: Optional optimizer to load state into
        scheduler: Optional scheduler to load state into
        device: Device to map the checkpoint to

    Returns:
        Dict containing the checkpoint data
    """
    map_location = device if device is not None else "cpu"
    checkpoint = torch.load(path, map_location=map_location)

    if model is not None and "model_state_dict" in checkpoint:
        model.load_state_dict(checkpoint["model_state_dict"])

    if optimizer is not None and "optimizer_state_dict" in checkpoint:
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])

    if scheduler is not None and "scheduler_state_dict" in checkpoint:
        scheduler.load_state_dict(checkpoint["scheduler_state_dict"])

    return checkpoint


def load_model_weights(model: nn.Module, path: str, device: Optional[torch.device] = None) -> nn.Module:
    """
    Load only model weights from a checkpoint or state dict file.

    Args:
        model: The model to load weights into
        path: Path to the checkpoint or state dict
        device: Device to map the weights to

    Returns:
        The model with loaded weights
    """
    map_location = device if device is not None else "cpu"
    state = torch.load(path, map_location=map_location)

    # Handle both full checkpoints and plain state dicts
    if isinstance(state, dict) and "model_state_dict" in state:
        state = state["model_state_dict"]

    model.load_state_dict(state)
    return model
