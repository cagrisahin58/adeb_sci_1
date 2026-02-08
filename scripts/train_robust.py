#!/usr/bin/env python3
"""
Robust Training Script with tmux Session Management

Features:
- Automatic tmux session creation and management
- Checkpoint recovery and training resumption
- Early stopping with configurable patience
- GPU memory monitoring and cleanup
- Training state persistence

Usage:
    python scripts/train_robust.py --config configs/experiments/cifar10_vit_native.yaml
    python scripts/train_robust.py --resume --session my_training
"""

import os
import sys
import json
import signal
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@dataclass
class TrainingState:
    """Persistent training state."""
    config_path: str
    session_name: str
    start_time: str
    current_epoch: int = 0
    best_accuracy: float = 0.0
    best_robust_accuracy: float = 0.0
    checkpoint_path: Optional[str] = None
    status: str = "initialized"  # initialized, running, paused, completed, failed

    def save(self, path: Path):
        """Save state to JSON file."""
        with open(path, 'w') as f:
            json.dump(asdict(self), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> 'TrainingState':
        """Load state from JSON file."""
        with open(path) as f:
            data = json.load(f)
        return cls(**data)


class CheckpointManager:
    """Manage training checkpoints with automatic cleanup."""

    def __init__(self, save_dir: Path, max_checkpoints: int = 3):
        self.save_dir = save_dir
        self.max_checkpoints = max_checkpoints
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def get_latest_checkpoint(self) -> Optional[Path]:
        """Get the most recent checkpoint."""
        checkpoints = sorted(self.save_dir.glob("checkpoint_epoch_*.pth"))
        if checkpoints:
            return checkpoints[-1]
        return None

    def get_best_checkpoint(self) -> Optional[Path]:
        """Get the best checkpoint."""
        best_path = self.save_dir / "best.pth"
        if best_path.exists():
            return best_path
        return None

    def cleanup_old_checkpoints(self):
        """Remove old checkpoints, keeping only the most recent ones."""
        checkpoints = sorted(self.save_dir.glob("checkpoint_epoch_*.pth"))
        if len(checkpoints) > self.max_checkpoints:
            for ckpt in checkpoints[:-self.max_checkpoints]:
                ckpt.unlink()
                print(f"Removed old checkpoint: {ckpt.name}")


class EarlyStopping:
    """Early stopping with patience."""

    def __init__(self, patience: int = 20, min_delta: float = 0.001):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_score = None
        self.should_stop = False

    def __call__(self, score: float) -> bool:
        """Check if training should stop."""
        if self.best_score is None:
            self.best_score = score
        elif score < self.best_score + self.min_delta:
            self.counter += 1
            if self.counter >= self.patience:
                self.should_stop = True
        else:
            self.best_score = score
            self.counter = 0
        return self.should_stop


def check_gpu_memory():
    """Check available GPU memory."""
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=memory.free,memory.total', '--format=csv,noheader,nounits'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            free, total = map(int, result.stdout.strip().split(','))
            print(f"GPU Memory: {free}MB free / {total}MB total ({100*free/total:.1f}% available)")
            return free, total
    except Exception as e:
        print(f"Could not check GPU memory: {e}")
    return None, None


def create_tmux_session(session_name: str) -> bool:
    """Create a new tmux session if it doesn't exist."""
    # Check if session exists
    result = subprocess.run(
        ['tmux', 'has-session', '-t', session_name],
        capture_output=True
    )
    if result.returncode == 0:
        print(f"tmux session '{session_name}' already exists")
        return True

    # Create new session
    result = subprocess.run(
        ['tmux', 'new-session', '-d', '-s', session_name],
        capture_output=True
    )
    if result.returncode == 0:
        print(f"Created tmux session: {session_name}")
        return True
    else:
        print(f"Failed to create tmux session: {result.stderr.decode()}")
        return False


def run_in_tmux(session_name: str, command: str):
    """Run a command in an existing tmux session."""
    subprocess.run([
        'tmux', 'send-keys', '-t', session_name, command, 'Enter'
    ])


def setup_signal_handlers(state: TrainingState, state_path: Path):
    """Setup graceful shutdown handlers."""
    def signal_handler(signum, frame):
        print(f"\nReceived signal {signum}, saving state...")
        state.status = "paused"
        state.save(state_path)
        print(f"State saved to {state_path}")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def main():
    parser = argparse.ArgumentParser(description='Robust Training Script')
    parser.add_argument('--config', type=str, required=False,
                       help='Path to configuration file')
    parser.add_argument('--session', type=str, default='training',
                       help='tmux session name')
    parser.add_argument('--resume', action='store_true',
                       help='Resume from last checkpoint')
    parser.add_argument('--no-tmux', action='store_true',
                       help='Run directly without tmux')
    parser.add_argument('--check-gpu', action='store_true',
                       help='Only check GPU status')
    args = parser.parse_args()

    # GPU check mode
    if args.check_gpu:
        check_gpu_memory()
        return

    # State management
    state_dir = PROJECT_ROOT / 'logs' / 'training_states'
    state_dir.mkdir(parents=True, exist_ok=True)
    state_path = state_dir / f'{args.session}_state.json'

    if args.resume and state_path.exists():
        state = TrainingState.load(state_path)
        print(f"Resuming from state: epoch {state.current_epoch}, best acc {state.best_accuracy:.2f}%")
        config_path = state.config_path
    else:
        if not args.config:
            print("Error: --config required for new training")
            sys.exit(1)
        config_path = args.config
        state = TrainingState(
            config_path=config_path,
            session_name=args.session,
            start_time=datetime.now().isoformat(),
        )

    # Check GPU
    free, total = check_gpu_memory()
    if free is not None and free < 4000:
        print(f"Warning: Low GPU memory ({free}MB). Training may fail.")

    # Build training command
    train_cmd = f"python -m cli.main train adversarial --config {config_path}"
    if args.resume and state.checkpoint_path:
        train_cmd += f" --resume {state.checkpoint_path}"

    if args.no_tmux:
        # Run directly
        state.status = "running"
        state.save(state_path)
        setup_signal_handlers(state, state_path)

        print(f"\nStarting training...")
        print(f"Command: {train_cmd}")
        os.system(train_cmd)
    else:
        # Run in tmux
        if create_tmux_session(args.session):
            state.status = "running"
            state.save(state_path)

            print(f"\nStarting training in tmux session '{args.session}'...")
            print(f"Command: {train_cmd}")
            print(f"\nTo attach: tmux attach -t {args.session}")
            print(f"To detach: Ctrl+B, then D")

            run_in_tmux(args.session, f"cd {PROJECT_ROOT}")
            run_in_tmux(args.session, train_cmd)


if __name__ == '__main__':
    main()
