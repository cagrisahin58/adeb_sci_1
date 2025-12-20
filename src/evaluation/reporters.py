"""Result reporters for various output formats."""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List, Any
import matplotlib.pyplot as plt
import numpy as np


class CSVReporter:
    """Reporter for CSV output format."""

    def __init__(self, output_dir: str = "./results", legacy_format: bool = True):
        """
        Initialize CSV reporter.

        Args:
            output_dir: Directory to save results
            legacy_format: Use legacy column names for backward compatibility
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.legacy_format = legacy_format

    def save(
        self,
        results: pd.DataFrame,
        filename: str,
        model_name: Optional[str] = None,
        training_type: Optional[str] = None,
    ) -> str:
        """
        Save results to CSV.

        Args:
            results: DataFrame with results
            filename: Output filename
            model_name: Model name to add as column
            training_type: Training type to add as column

        Returns:
            Path to saved file
        """
        df = results.copy()

        # Add model and training columns if provided
        if model_name is not None:
            df.insert(0, "Model", model_name)
        if training_type is not None:
            df.insert(1, "Training", training_type)

        # Legacy format column renaming
        if self.legacy_format:
            column_map = {
                "attack": "Attack",
                "eps": "Epsilon",
                "accuracy": "Accuracy",
                "defense": "Defense",
            }
            df = df.rename(columns=column_map)

        path = self.output_dir / filename
        df.to_csv(path, index=False)

        return str(path)


class LaTeXReporter:
    """Reporter for LaTeX table output."""

    def __init__(self, output_dir: str = "./paper"):
        """
        Initialize LaTeX reporter.

        Args:
            output_dir: Directory to save tables
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        results: pd.DataFrame,
        filename: str,
        caption: Optional[str] = None,
        label: Optional[str] = None,
    ) -> str:
        """
        Save results as LaTeX table.

        Args:
            results: DataFrame with results
            filename: Output filename
            caption: Table caption
            label: Table label for references

        Returns:
            Path to saved file
        """
        # Format accuracy columns
        df = results.copy()
        for col in df.columns:
            if "accuracy" in col.lower() or "acc" in col.lower():
                df[col] = df[col].apply(lambda x: f"{x:.2f}\\%")

        # Generate LaTeX
        latex = df.to_latex(
            index=False,
            escape=False,
            column_format="l" + "c" * (len(df.columns) - 1),
        )

        # Wrap in table environment
        if caption or label:
            latex_full = "\\begin{table}[htbp]\n\\centering\n"
            if caption:
                latex_full += f"\\caption{{{caption}}}\n"
            if label:
                latex_full += f"\\label{{{label}}}\n"
            latex_full += latex
            latex_full += "\\end{table}"
            latex = latex_full

        path = self.output_dir / filename
        with open(path, "w") as f:
            f.write(latex)

        return str(path)

    def create_comparison_table(
        self,
        results_dict: Dict[str, pd.DataFrame],
        filename: str,
        metric: str = "accuracy",
    ) -> str:
        """
        Create a comparison table across multiple models/methods.

        Args:
            results_dict: Dictionary mapping names to result DataFrames
            filename: Output filename
            metric: Metric column to compare

        Returns:
            Path to saved file
        """
        # Combine results
        combined = []
        for name, df in results_dict.items():
            df_copy = df.copy()
            df_copy["Method"] = name
            combined.append(df_copy)

        combined_df = pd.concat(combined, ignore_index=True)

        # Pivot for comparison
        pivot = combined_df.pivot_table(
            values=metric,
            index=["attack", "eps"],
            columns="Method",
            aggfunc="first",
        ).reset_index()

        return self.save(pivot, filename)


class PlotReporter:
    """Reporter for visualization plots."""

    def __init__(self, output_dir: str = "./results", figsize: tuple = (10, 6)):
        """
        Initialize plot reporter.

        Args:
            output_dir: Directory to save plots
            figsize: Default figure size
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.figsize = figsize

    def plot_accuracy_vs_epsilon(
        self,
        results: pd.DataFrame,
        filename: str,
        title: Optional[str] = None,
    ) -> str:
        """
        Plot accuracy vs epsilon for different attacks.

        Args:
            results: DataFrame with results
            filename: Output filename
            title: Plot title

        Returns:
            Path to saved file
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        attacks = results[results["attack"] != "clean"]["attack"].unique()

        for attack in attacks:
            attack_data = results[results["attack"] == attack]
            ax.plot(
                attack_data["eps"],
                attack_data["accuracy"],
                marker="o",
                label=attack.upper(),
            )

        ax.set_xlabel("Epsilon (ε)")
        ax.set_ylabel("Accuracy (%)")
        ax.set_title(title or "Robustness vs Perturbation Size")
        ax.legend()
        ax.grid(True, alpha=0.3)

        path = self.output_dir / filename
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)

        return str(path)

    def plot_attack_comparison(
        self,
        results_dict: Dict[str, pd.DataFrame],
        filename: str,
        eps: float = 8 / 255,
        title: Optional[str] = None,
    ) -> str:
        """
        Plot bar chart comparing different models/methods.

        Args:
            results_dict: Dictionary mapping names to result DataFrames
            filename: Output filename
            eps: Epsilon value to compare at
            title: Plot title

        Returns:
            Path to saved file
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        methods = list(results_dict.keys())
        attacks = ["clean", "fgsm", "pgd"]

        x = np.arange(len(attacks))
        width = 0.8 / len(methods)

        for i, (method, df) in enumerate(results_dict.items()):
            accuracies = []
            for attack in attacks:
                if attack == "clean":
                    acc = df[df["attack"] == "clean"]["accuracy"].values
                else:
                    acc = df[(df["attack"] == attack) & (df["eps"] == eps)]["accuracy"].values

                accuracies.append(acc[0] if len(acc) > 0 else 0)

            ax.bar(x + i * width, accuracies, width, label=method)

        ax.set_xlabel("Attack")
        ax.set_ylabel("Accuracy (%)")
        ax.set_title(title or f"Model Comparison (ε={eps:.4f})")
        ax.set_xticks(x + width * (len(methods) - 1) / 2)
        ax.set_xticklabels([a.upper() for a in attacks])
        ax.legend()
        ax.grid(True, alpha=0.3, axis="y")

        path = self.output_dir / filename
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)

        return str(path)

    def plot_defense_effectiveness(
        self,
        results: pd.DataFrame,
        filename: str,
        title: Optional[str] = None,
    ) -> str:
        """
        Plot defense effectiveness comparison.

        Args:
            results: DataFrame with normal and defense results
            filename: Output filename
            title: Plot title

        Returns:
            Path to saved file
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        if "defense" in results.columns:
            defenses = results["defense"].unique()

            for defense in defenses:
                defense_data = results[results["defense"] == defense]
                ax.bar(defense, defense_data["accuracy"].mean())
        else:
            attacks = results["attack"].unique()
            ax.bar(attacks, results.groupby("attack")["accuracy"].mean())

        ax.set_xlabel("Method")
        ax.set_ylabel("Accuracy (%)")
        ax.set_title(title or "Defense Effectiveness")
        ax.grid(True, alpha=0.3, axis="y")

        path = self.output_dir / filename
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)

        return str(path)
