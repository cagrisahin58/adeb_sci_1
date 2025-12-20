"""Attack registry for managing attack methods."""

from typing import Dict, Type, Optional, Any, List
import torch.nn as nn
from .base import BaseAttack


class AttackRegistry:
    """
    Registry for attack methods.

    Provides a factory pattern for creating attack instances by name.
    """

    _attacks: Dict[str, Type[BaseAttack]] = {}

    @classmethod
    def register(cls, name: str):
        """
        Decorator to register an attack class.

        Args:
            name: Name to register the attack under

        Returns:
            Decorator function
        """
        def decorator(attack_cls: Type[BaseAttack]) -> Type[BaseAttack]:
            if name in cls._attacks:
                raise ValueError(f"Attack '{name}' is already registered")
            cls._attacks[name] = attack_cls
            return attack_cls

        return decorator

    @classmethod
    def get(cls, name: str, model: nn.Module, **kwargs) -> BaseAttack:
        """
        Get an attack instance by name.

        Args:
            name: Name of the registered attack
            model: Model to attack
            **kwargs: Arguments to pass to the attack constructor

        Returns:
            Attack instance

        Raises:
            ValueError: If the attack name is not registered
        """
        if name not in cls._attacks:
            available = ", ".join(cls._attacks.keys())
            raise ValueError(f"Attack '{name}' not found. Available attacks: {available}")

        return cls._attacks[name](model=model, **kwargs)

    @classmethod
    def get_class(cls, name: str) -> Type[BaseAttack]:
        """
        Get an attack class by name.

        Args:
            name: Name of the registered attack

        Returns:
            Attack class
        """
        if name not in cls._attacks:
            available = ", ".join(cls._attacks.keys())
            raise ValueError(f"Attack '{name}' not found. Available attacks: {available}")

        return cls._attacks[name]

    @classmethod
    def list_attacks(cls) -> List[str]:
        """
        List all registered attack names.

        Returns:
            List of attack names
        """
        return list(cls._attacks.keys())

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """
        Check if an attack is registered.

        Args:
            name: Attack name to check

        Returns:
            True if registered, False otherwise
        """
        return name in cls._attacks


def register_attack(name: str):
    """
    Decorator to register an attack class.

    This is a convenience wrapper around AttackRegistry.register.

    Args:
        name: Name to register the attack under

    Returns:
        Decorator function
    """
    return AttackRegistry.register(name)
