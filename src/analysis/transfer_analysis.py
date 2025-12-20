"""Transfer attack analysis for cross-architecture vulnerability study."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Dict, List, Tuple, Union
import numpy as np
from pathlib import Path
import pandas as pd


class TransferAttackAnalyzer:
    """
    Analyze transferability of adversarial examples across architectures.

    Key research questions:
    1. Do adversarial examples transfer between CNNs and ViTs?
    2. Which architecture produces more transferable perturbations?
    3. How does perturbation magnitude affect transferability?
    """

    def __init__(
        self,
        source_model: nn.Module,
        target_models: Dict[str, nn.Module],
        device: Optional[torch.device] = None,
    ):
        """
        Initialize transfer attack analyzer.

        Args:
            source_model: Model used to generate adversarial examples
            target_models: Dictionary of target models to test transfer
            device: Device to run analysis on
        """
        self.source_model = source_model
        self.target_models = target_models
        self.device = device or next(source_model.parameters()).device
        self.loss_fn = nn.CrossEntropyLoss()

    def generate_adversarial_examples(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        attack_fn: callable,
    ) -> torch.Tensor:
        """
        Generate adversarial examples using source model.

        Args:
            images: Clean input images
            labels: True labels
            attack_fn: Attack function that takes (model, images, labels)

        Returns:
            Adversarial images
        """
        self.source_model.eval()
        images = images.to(self.device)
        labels = labels.to(self.device)

        adv_images = attack_fn(self.source_model, images, labels)
        return adv_images

    def evaluate_transfer(
        self,
        clean_images: torch.Tensor,
        adv_images: torch.Tensor,
        labels: torch.Tensor,
    ) -> Dict[str, Dict[str, float]]:
        """
        Evaluate transfer success to all target models.

        Args:
            clean_images: Original clean images
            adv_images: Adversarial images from source model
            labels: True labels

        Returns:
            Dictionary with transfer metrics for each target model
        """
        clean_images = clean_images.to(self.device)
        adv_images = adv_images.to(self.device)
        labels = labels.to(self.device)

        results = {}

        for name, model in self.target_models.items():
            model = model.to(self.device)
            model.eval()

            with torch.no_grad():
                # Clean accuracy on target
                clean_outputs = model(clean_images)
                clean_preds = clean_outputs.argmax(dim=1)
                clean_correct = (clean_preds == labels).float()
                clean_acc = clean_correct.mean().item()

                # Adversarial accuracy on target
                adv_outputs = model(adv_images)
                adv_preds = adv_outputs.argmax(dim=1)
                adv_correct = (adv_preds == labels).float()
                adv_acc = adv_correct.mean().item()

                # Transfer success rate (fooling rate)
                # Only count samples that were correctly classified originally
                correctly_classified_mask = clean_correct.bool()
                if correctly_classified_mask.sum() > 0:
                    transfer_success = (
                        (adv_preds[correctly_classified_mask] != labels[correctly_classified_mask])
                        .float().mean().item()
                    )
                else:
                    transfer_success = 0.0

                # Confidence drop
                clean_conf = F.softmax(clean_outputs, dim=1).max(dim=1)[0].mean().item()
                adv_conf = F.softmax(adv_outputs, dim=1).max(dim=1)[0].mean().item()
                conf_drop = clean_conf - adv_conf

                # Loss increase
                clean_loss = self.loss_fn(clean_outputs, labels).item()
                adv_loss = self.loss_fn(adv_outputs, labels).item()

            results[name] = {
                "clean_accuracy": clean_acc,
                "adversarial_accuracy": adv_acc,
                "accuracy_drop": clean_acc - adv_acc,
                "transfer_success_rate": transfer_success,
                "confidence_drop": conf_drop,
                "clean_loss": clean_loss,
                "adversarial_loss": adv_loss,
                "loss_increase": adv_loss - clean_loss,
            }

        return results

    def compute_transferability_matrix(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        attack_fn: callable,
        models: Dict[str, nn.Module],
    ) -> Tuple[np.ndarray, List[str]]:
        """
        Compute full transferability matrix between all model pairs.

        Args:
            images: Clean input images
            labels: True labels
            attack_fn: Attack function
            models: Dictionary of all models

        Returns:
            Transferability matrix (N x N) and model names
        """
        model_names = list(models.keys())
        n_models = len(model_names)
        transfer_matrix = np.zeros((n_models, n_models))

        images = images.to(self.device)
        labels = labels.to(self.device)

        for i, source_name in enumerate(model_names):
            source_model = models[source_name].to(self.device)
            source_model.eval()

            # Generate adversarial examples from source
            adv_images = attack_fn(source_model, images, labels)

            for j, target_name in enumerate(model_names):
                target_model = models[target_name].to(self.device)
                target_model.eval()

                with torch.no_grad():
                    # Get clean predictions for filtering
                    clean_outputs = target_model(images)
                    clean_preds = clean_outputs.argmax(dim=1)
                    correctly_classified = (clean_preds == labels)

                    # Evaluate on adversarial
                    adv_outputs = target_model(adv_images)
                    adv_preds = adv_outputs.argmax(dim=1)

                    # Transfer success rate
                    if correctly_classified.sum() > 0:
                        fooled = (adv_preds[correctly_classified] != labels[correctly_classified])
                        transfer_rate = fooled.float().mean().item()
                    else:
                        transfer_rate = 0.0

                transfer_matrix[i, j] = transfer_rate

        return transfer_matrix, model_names

    def analyze_perturbation_transferability(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        epsilon_range: List[float],
        attack_fn_factory: callable,
    ) -> Dict[str, Dict[float, float]]:
        """
        Analyze how perturbation magnitude affects transferability.

        Args:
            images: Clean input images
            labels: True labels
            epsilon_range: List of epsilon values to test
            attack_fn_factory: Function that takes epsilon and returns attack_fn

        Returns:
            Transfer rates for each target model at each epsilon
        """
        results = {name: {} for name in self.target_models.keys()}

        images = images.to(self.device)
        labels = labels.to(self.device)

        for eps in epsilon_range:
            attack_fn = attack_fn_factory(eps)
            adv_images = self.generate_adversarial_examples(images, labels, attack_fn)

            transfer_results = self.evaluate_transfer(images, adv_images, labels)

            for name, metrics in transfer_results.items():
                results[name][eps] = metrics["transfer_success_rate"]

        return results

    def compute_perturbation_similarity(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        attack_fn: callable,
        models: Dict[str, nn.Module],
    ) -> Dict[str, Dict[str, float]]:
        """
        Compute similarity between perturbations from different models.

        Args:
            images: Clean input images
            labels: True labels
            attack_fn: Attack function
            models: Dictionary of models

        Returns:
            Pairwise perturbation similarities
        """
        images = images.to(self.device)
        labels = labels.to(self.device)

        # Generate perturbations from each model
        perturbations = {}
        for name, model in models.items():
            model = model.to(self.device)
            model.eval()
            adv_images = attack_fn(model, images, labels)
            perturbations[name] = (adv_images - images).view(images.shape[0], -1)

        # Compute pairwise similarities
        model_names = list(models.keys())
        similarities = {}

        for i, name1 in enumerate(model_names):
            similarities[name1] = {}
            pert1 = perturbations[name1]
            pert1_norm = F.normalize(pert1, p=2, dim=1)

            for j, name2 in enumerate(model_names):
                pert2 = perturbations[name2]
                pert2_norm = F.normalize(pert2, p=2, dim=1)

                # Cosine similarity
                cosine_sim = (pert1_norm * pert2_norm).sum(dim=1).mean().item()

                # L2 distance
                l2_dist = torch.norm(pert1 - pert2, p=2, dim=1).mean().item()

                similarities[name1][name2] = {
                    "cosine_similarity": cosine_sim,
                    "l2_distance": l2_dist,
                }

        return similarities

    def analyze_gradient_alignment(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        models: Dict[str, nn.Module],
    ) -> Dict[str, Dict[str, float]]:
        """
        Analyze gradient alignment between models.

        Higher alignment suggests better transferability.

        Args:
            images: Clean input images
            labels: True labels
            models: Dictionary of models

        Returns:
            Pairwise gradient alignment scores
        """
        images = images.to(self.device)
        labels = labels.to(self.device)

        # Compute gradients from each model
        gradients = {}
        for name, model in models.items():
            model = model.to(self.device)
            model.eval()

            images_grad = images.clone().requires_grad_(True)
            outputs = model(images_grad)
            loss = self.loss_fn(outputs, labels)
            loss.backward()

            gradients[name] = images_grad.grad.view(images.shape[0], -1).detach()

        # Compute pairwise gradient alignment
        model_names = list(models.keys())
        alignments = {}

        for name1 in model_names:
            alignments[name1] = {}
            grad1 = gradients[name1]
            grad1_norm = F.normalize(grad1, p=2, dim=1)

            for name2 in model_names:
                grad2 = gradients[name2]
                grad2_norm = F.normalize(grad2, p=2, dim=1)

                # Cosine similarity (gradient alignment)
                alignment = (grad1_norm * grad2_norm).sum(dim=1).mean().item()
                alignments[name1][name2] = alignment

        return alignments

    def generate_ensemble_attack(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        models: Dict[str, nn.Module],
        weights: Optional[Dict[str, float]] = None,
        eps: float = 8/255,
        alpha: float = 2/255,
        steps: int = 10,
    ) -> torch.Tensor:
        """
        Generate adversarial examples using ensemble of models.

        Ensemble attacks often have better transferability.

        Args:
            images: Clean input images
            labels: True labels
            models: Dictionary of models to use in ensemble
            weights: Optional weights for each model (uniform if None)
            eps: Maximum perturbation
            alpha: Step size
            steps: Number of PGD steps

        Returns:
            Adversarial images
        """
        images = images.to(self.device)
        labels = labels.to(self.device)

        if weights is None:
            weights = {name: 1.0 / len(models) for name in models}

        # Initialize with random perturbation
        delta = torch.zeros_like(images).uniform_(-eps, eps)
        delta = delta.requires_grad_(True)

        for _ in range(steps):
            total_grad = torch.zeros_like(images)

            for name, model in models.items():
                model = model.to(self.device)
                model.eval()

                adv_images = images + delta
                outputs = model(adv_images)
                loss = self.loss_fn(outputs, labels)
                loss.backward()

                total_grad += weights[name] * delta.grad.data
                delta.grad.data.zero_()

            # Update perturbation
            delta.data = delta.data + alpha * total_grad.sign()
            delta.data = torch.clamp(delta.data, -eps, eps)
            delta.data = torch.clamp(images + delta.data, 0, 1) - images

        return (images + delta.detach()).clamp(0, 1)

    def full_transfer_analysis(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        attack_fn: callable,
        models: Dict[str, nn.Module],
    ) -> Dict[str, any]:
        """
        Perform comprehensive transfer attack analysis.

        Args:
            images: Clean input images
            labels: True labels
            attack_fn: Attack function
            models: Dictionary of all models

        Returns:
            Comprehensive analysis results
        """
        # Transferability matrix
        transfer_matrix, model_names = self.compute_transferability_matrix(
            images, labels, attack_fn, models
        )

        # Perturbation similarity
        pert_similarity = self.compute_perturbation_similarity(
            images, labels, attack_fn, models
        )

        # Gradient alignment
        grad_alignment = self.analyze_gradient_alignment(
            images, labels, models
        )

        # Summary statistics
        cnn_models = [n for n in model_names if "resnet" in n.lower() or "densenet" in n.lower()]
        vit_models = [n for n in model_names if "vit" in n.lower()]

        cnn_to_vit_transfer = []
        vit_to_cnn_transfer = []

        for i, src in enumerate(model_names):
            for j, tgt in enumerate(model_names):
                if src != tgt:
                    if src in cnn_models and tgt in vit_models:
                        cnn_to_vit_transfer.append(transfer_matrix[i, j])
                    elif src in vit_models and tgt in cnn_models:
                        vit_to_cnn_transfer.append(transfer_matrix[i, j])

        return {
            "transfer_matrix": transfer_matrix,
            "model_names": model_names,
            "perturbation_similarity": pert_similarity,
            "gradient_alignment": grad_alignment,
            "summary": {
                "cnn_to_vit_avg_transfer": np.mean(cnn_to_vit_transfer) if cnn_to_vit_transfer else 0,
                "vit_to_cnn_avg_transfer": np.mean(vit_to_cnn_transfer) if vit_to_cnn_transfer else 0,
                "intra_architecture_higher": (
                    np.mean([transfer_matrix[i, i] for i in range(len(model_names))])
                    if len(model_names) > 0 else 0
                ),
            }
        }

    def export_results_to_dataframe(
        self,
        transfer_matrix: np.ndarray,
        model_names: List[str],
    ) -> pd.DataFrame:
        """Convert transfer matrix to pandas DataFrame for easy export."""
        df = pd.DataFrame(
            transfer_matrix,
            index=model_names,
            columns=model_names,
        )
        df.index.name = "Source"
        df.columns.name = "Target"
        return df
