"""Tests for analysis module."""

import pytest
import torch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestGradientAnalyzer:
    """Tests for GradientAnalyzer."""

    def test_compute_input_gradients(self, resnet_model, sample_batch):
        from src.analysis import GradientAnalyzer

        model = resnet_model.eval()
        analyzer = GradientAnalyzer(model)

        images, labels = sample_batch
        grads = analyzer.compute_input_gradients(images, labels)

        assert grads.shape == images.shape

    def test_compute_gradient_statistics(self, resnet_model, sample_batch):
        from src.analysis import GradientAnalyzer

        model = resnet_model.eval()
        analyzer = GradientAnalyzer(model)

        images, labels = sample_batch
        stats = analyzer.compute_gradient_statistics(images, labels)

        assert "l2_norm_mean" in stats
        assert "linf_norm_mean" in stats
        assert "sparsity" in stats
        assert "spatial_variance" in stats

    def test_compare_gradient_landscapes(self, resnet_model, sample_batch):
        from src.analysis import GradientAnalyzer

        model = resnet_model.eval()
        analyzer = GradientAnalyzer(model)

        images, labels = sample_batch
        results = analyzer.compare_gradient_landscapes(
            images, labels,
            epsilon_range=[0.001, 0.01]
        )

        assert "epsilons" in results
        assert "loss_random" in results
        assert "loss_gradient" in results

    def test_compute_gradient_alignment(self, resnet_model, sample_batch):
        from src.analysis import GradientAnalyzer

        model = resnet_model.eval()
        analyzer = GradientAnalyzer(model)

        images, labels = sample_batch
        alignment = analyzer.compute_gradient_alignment(images, labels)

        assert isinstance(alignment, float)
        assert 0 <= alignment <= 1


class TestTransferAttackAnalyzer:
    """Tests for TransferAttackAnalyzer."""

    def test_evaluate_transfer(self, resnet_model, sample_batch):
        from src.analysis import TransferAttackAnalyzer

        model = resnet_model.eval()
        # Use same model as source and target for testing
        analyzer = TransferAttackAnalyzer(
            source_model=model,
            target_models={"resnet": model}
        )

        images, labels = sample_batch
        # Simple identity "attack" for testing
        adv_images = images + 0.01 * torch.randn_like(images)
        adv_images = adv_images.clamp(0, 1)

        results = analyzer.evaluate_transfer(images, adv_images, labels)

        assert "resnet" in results
        assert "clean_accuracy" in results["resnet"]
        assert "adversarial_accuracy" in results["resnet"]
        assert "transfer_success_rate" in results["resnet"]

    def test_compute_perturbation_similarity(self, resnet_model, sample_batch):
        from src.analysis import TransferAttackAnalyzer

        model = resnet_model.eval()
        models = {"resnet1": model, "resnet2": model}

        analyzer = TransferAttackAnalyzer(
            source_model=model,
            target_models=models
        )

        images, labels = sample_batch

        # Simple attack function
        def simple_attack(m, x, y):
            x = x.clone().requires_grad_(True)
            loss = torch.nn.CrossEntropyLoss()(m(x), y)
            loss.backward()
            return (x + 0.01 * x.grad.sign()).clamp(0, 1)

        similarities = analyzer.compute_perturbation_similarity(
            images, labels, simple_attack, models
        )

        assert "resnet1" in similarities
        assert "resnet2" in similarities["resnet1"]

    def test_analyze_gradient_alignment(self, resnet_model, sample_batch):
        from src.analysis import TransferAttackAnalyzer

        model = resnet_model.eval()
        models = {"resnet": model}

        analyzer = TransferAttackAnalyzer(
            source_model=model,
            target_models=models
        )

        images, labels = sample_batch
        alignments = analyzer.analyze_gradient_alignment(images, labels, models)

        assert "resnet" in alignments
        # Self-alignment should be 1.0
        assert abs(alignments["resnet"]["resnet"] - 1.0) < 0.01


class TestAdversarialVisualizer:
    """Tests for AdversarialVisualizer."""

    def test_init(self):
        from src.analysis import AdversarialVisualizer

        viz = AdversarialVisualizer()
        assert viz.figsize == (12, 8)
        assert viz.dpi == 150

    def test_plot_robustness_comparison(self):
        from src.analysis import AdversarialVisualizer
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend

        viz = AdversarialVisualizer()

        results = {
            "resnet": {"adversarial_accuracy": 0.75},
            "vit": {"adversarial_accuracy": 0.55}
        }

        fig = viz.plot_robustness_comparison(results)
        assert fig is not None

    def test_plot_transfer_matrix(self):
        from src.analysis import AdversarialVisualizer
        import matplotlib
        import numpy as np
        matplotlib.use('Agg')

        viz = AdversarialVisualizer()

        transfer_matrix = np.array([[1.0, 0.3], [0.4, 1.0]])
        model_names = ["ResNet", "ViT"]

        fig = viz.plot_transfer_matrix(transfer_matrix, model_names)
        assert fig is not None

    def test_plot_epsilon_sweep(self):
        from src.analysis import AdversarialVisualizer
        import matplotlib
        matplotlib.use('Agg')

        viz = AdversarialVisualizer()

        epsilon_results = {
            "ResNet": {0.01: 0.9, 0.02: 0.7, 0.03: 0.5},
            "ViT": {0.01: 0.8, 0.02: 0.5, 0.03: 0.3}
        }

        fig = viz.plot_epsilon_sweep(epsilon_results)
        assert fig is not None


class TestAttentionAnalyzer:
    """Tests for AttentionAnalyzer (requires ViT)."""

    @pytest.mark.skipif(
        not pytest.importorskip("timm", reason="timm not installed"),
        reason="timm not installed"
    )
    def test_compute_attention_entropy(self):
        from src.analysis import AttentionAnalyzer
        import torch

        # Create dummy attention map
        attention_map = torch.softmax(torch.randn(1, 8, 49, 49), dim=-1)

        # Test entropy computation without a model
        analyzer = AttentionAnalyzer.__new__(AttentionAnalyzer)
        entropy = analyzer.compute_attention_entropy(attention_map)

        assert entropy.shape == (1, 8, 49)
        assert (entropy >= 0).all()
