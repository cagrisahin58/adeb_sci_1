"""Configuration management utilities."""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from pathlib import Path
import yaml
from omegaconf import OmegaConf, DictConfig


@dataclass
class DataConfig:
    """Data configuration."""
    dataset: str = "cifar10"
    data_dir: str = "./data"
    batch_size: int = 128
    test_batch_size: int = 100
    num_workers: int = 2


@dataclass
class TrainingConfig:
    """Training configuration."""
    epochs: int = 50
    optimizer: str = "sgd"
    lr: float = 0.1
    momentum: float = 0.9
    weight_decay: float = 5e-4
    scheduler: str = "cosine"
    scheduler_t_max: Optional[int] = None  # Defaults to epochs


@dataclass
class AttackConfig:
    """Attack configuration."""
    name: str = "pgd"
    eps: float = 0.031373  # 8/255
    alpha: float = 0.007843  # 2/255
    steps: int = 10
    random_start: bool = True


@dataclass
class DefenseConfig:
    """Defense configuration."""
    name: str = "adversarial_training"
    attack: AttackConfig = field(default_factory=AttackConfig)
    beta: float = 6.0  # TRADES/MART parameter


@dataclass
class EvaluationConfig:
    """Evaluation configuration."""
    batch_size: int = 100
    subset_size: Optional[int] = None
    attacks: List[str] = field(default_factory=lambda: ["fgsm", "pgd"])
    epsilons: List[float] = field(default_factory=lambda: [0.007843, 0.015686, 0.031373])


@dataclass
class LoggingConfig:
    """Logging configuration."""
    log_dir: str = "./logs"
    save_freq: int = 5
    verbose: bool = True


@dataclass
class CheckpointConfig:
    """Checkpoint configuration."""
    checkpoint_dir: str = "./models"
    save_best: bool = True
    save_last: bool = True


@dataclass
class ExperimentConfig:
    """Main experiment configuration."""
    name: str = "experiment"
    seed: int = 42
    device: str = "auto"
    model: str = "resnet18"
    model_args: Dict[str, Any] = field(default_factory=dict)
    data: DataConfig = field(default_factory=DataConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    defense: Optional[DefenseConfig] = None
    evaluation: EvaluationConfig = field(default_factory=EvaluationConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    checkpoint: CheckpointConfig = field(default_factory=CheckpointConfig)


def load_config(config_path: str) -> ExperimentConfig:
    """
    Load configuration from a YAML file.

    Args:
        config_path: Path to the configuration file

    Returns:
        ExperimentConfig: Loaded configuration
    """
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(path, "r") as f:
        config_dict = yaml.safe_load(f)

    # Use OmegaConf for merging with defaults
    schema = OmegaConf.structured(ExperimentConfig)
    config = OmegaConf.create(config_dict)
    merged = OmegaConf.merge(schema, config)

    # Convert back to dataclass
    return OmegaConf.to_object(merged)


def save_config(config: ExperimentConfig, save_path: str) -> None:
    """
    Save configuration to a YAML file.

    Args:
        config: Configuration to save
        save_path: Path to save the configuration
    """
    path = Path(save_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    config_dict = OmegaConf.to_container(OmegaConf.structured(config))

    with open(path, "w") as f:
        yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)


def create_default_config() -> ExperimentConfig:
    """Create a default experiment configuration."""
    return ExperimentConfig()
