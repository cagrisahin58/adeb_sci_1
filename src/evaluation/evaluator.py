"""Evaluator class for comprehensive model evaluation."""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Optional, Dict, List, Any
from pathlib import Path
from tqdm import tqdm
import pandas as pd

from .metrics import compute_accuracy, compute_robustness
from ..attacks import AttackRegistry


class Evaluator:
    """
    Comprehensive evaluator for model robustness.

    Evaluates models against multiple attacks and defense settings.
    """

    def __init__(
        self,
        model: nn.Module,
        test_loader: DataLoader,
        device: Optional[torch.device] = None,
        verbose: bool = True,
    ):
        """
        Initialize the evaluator.

        Args:
            model: Model to evaluate
            test_loader: Test data loader
            device: Device to run on
            verbose: Whether to print progress
        """
        self.model = model
        self.test_loader = test_loader
        self.verbose = verbose

        self.device = device or (
            torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        )
        self.model = self.model.to(self.device)

        self.results: List[Dict[str, Any]] = []

    def evaluate_clean(self) -> float:
        """
        Evaluate clean accuracy.

        Returns:
            Clean accuracy percentage
        """
        acc = compute_accuracy(
            self.model,
            self.test_loader,
            device=self.device,
            verbose=self.verbose,
        )

        self.results.append({
            "attack": "clean",
            "eps": 0.0,
            "accuracy": acc,
        })

        if self.verbose:
            print(f"Clean accuracy: {acc:.2f}%")

        return acc

    def evaluate_attack(
        self,
        attack_name: str,
        eps: float = 8 / 255,
        **attack_kwargs,
    ) -> float:
        """
        Evaluate against a specific attack.

        Args:
            attack_name: Name of the attack
            eps: Perturbation size
            **attack_kwargs: Additional attack parameters

        Returns:
            Robust accuracy percentage
        """
        # Create attack
        attack = AttackRegistry.get(
            attack_name,
            model=self.model,
            eps=eps,
            device=self.device,
            **attack_kwargs,
        )

        acc = compute_robustness(
            self.model,
            attack,
            self.test_loader,
            device=self.device,
            verbose=self.verbose,
        )

        self.results.append({
            "attack": attack_name,
            "eps": eps,
            "accuracy": acc,
        })

        if self.verbose:
            print(f"{attack_name} (eps={eps:.4f}) accuracy: {acc:.2f}%")

        return acc

    def evaluate_multiple_attacks(
        self,
        attacks: List[str] = ["fgsm", "pgd"],
        epsilons: List[float] = [2 / 255, 4 / 255, 8 / 255],
        **attack_kwargs,
    ) -> pd.DataFrame:
        """
        Evaluate against multiple attacks and epsilon values.

        Args:
            attacks: List of attack names
            epsilons: List of epsilon values
            **attack_kwargs: Additional attack parameters

        Returns:
            DataFrame with results
        """
        if self.verbose:
            print("=" * 50)
            print("Robustness Evaluation")
            print("=" * 50)

        # Clean accuracy first
        self.evaluate_clean()

        # Each attack and epsilon
        for attack_name in attacks:
            for eps in epsilons:
                self.evaluate_attack(attack_name, eps, **attack_kwargs)

        return self.get_results_dataframe()

    def evaluate_defense(
        self,
        defense,
        attack_name: str = "pgd",
        eps: float = 8 / 255,
        **attack_kwargs,
    ) -> float:
        """
        Evaluate a defense mechanism against an attack.

        Args:
            defense: Defense object
            attack_name: Attack name
            eps: Perturbation size
            **attack_kwargs: Additional attack parameters

        Returns:
            Defended accuracy percentage
        """
        attack = AttackRegistry.get(
            attack_name,
            model=self.model,
            eps=eps,
            device=self.device,
            **attack_kwargs,
        )

        self.model.eval()
        correct = 0
        total = 0

        iterator = self.test_loader
        if self.verbose:
            iterator = tqdm(iterator, desc=f"Defense eval ({defense.name})")

        for inputs, labels in iterator:
            inputs, labels = inputs.to(self.device), labels.to(self.device)

            # Generate adversarial examples
            adv_inputs = attack(inputs, labels)

            # Apply defense
            outputs = defense(adv_inputs, labels)

            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        acc = 100.0 * correct / total

        self.results.append({
            "attack": attack_name,
            "eps": eps,
            "defense": defense.name,
            "accuracy": acc,
        })

        if self.verbose:
            print(f"{defense.name} + {attack_name} (eps={eps:.4f}) accuracy: {acc:.2f}%")

        return acc

    def get_results_dataframe(self) -> pd.DataFrame:
        """
        Get results as a pandas DataFrame.

        Returns:
            DataFrame with all evaluation results
        """
        return pd.DataFrame(self.results)

    def save_results(self, path: str) -> None:
        """
        Save results to a CSV file.

        Args:
            path: Path to save the results
        """
        df = self.get_results_dataframe()
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)

        if self.verbose:
            print(f"Results saved to {path}")

    def clear_results(self) -> None:
        """Clear all stored results."""
        self.results = []
