"""Device handling utilities for GPU/CPU management."""

import torch
from typing import Optional


def get_device(device: Optional[str] = None) -> torch.device:
    """
    Get the appropriate device for training/inference.

    Args:
        device: Device specification ('cuda', 'cpu', 'mps', or None for auto-detect)

    Returns:
        torch.device: The selected device
    """
    if device is None or device == "auto":
        if torch.cuda.is_available():
            return torch.device("cuda")
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return torch.device("mps")
        else:
            return torch.device("cpu")

    return torch.device(device)


def get_device_info(device: torch.device) -> dict:
    """
    Get information about the specified device.

    Args:
        device: The device to get info for

    Returns:
        dict: Device information
    """
    info = {
        "device": str(device),
        "type": device.type,
    }

    if device.type == "cuda":
        info["name"] = torch.cuda.get_device_name(device)
        info["memory_total"] = torch.cuda.get_device_properties(device).total_memory
        info["memory_allocated"] = torch.cuda.memory_allocated(device)
        info["cuda_version"] = torch.version.cuda

    return info


def print_device_info(device: torch.device) -> None:
    """Print device information to console."""
    info = get_device_info(device)
    print(f"Device: {info['device']}")

    if info["type"] == "cuda":
        print(f"  GPU: {info['name']}")
        print(f"  Memory: {info['memory_total'] / 1e9:.2f} GB")
        print(f"  CUDA Version: {info['cuda_version']}")
