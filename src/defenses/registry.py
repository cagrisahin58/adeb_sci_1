"""Defense registry for managing defense mechanisms."""

from typing import Dict, Type, Optional, Any, List
import torch.nn as nn
from .base import BaseDefense


class DefenseRegistry:
    """
    Registry for defense mechanisms.

    Provides a factory pattern for creating defense instances by name.
    """

    _defenses: Dict[str, Type[BaseDefense]] = {}

    @classmethod
    def register(cls, name: str):
        """
        Decorator to register a defense class.

        Args:
            name: Name to register the defense under

        Returns:
            Decorator function
        """
        def decorator(defense_cls: Type[BaseDefense]) -> Type[BaseDefense]:
            if name in cls._defenses:
                raise ValueError(f"Defense '{name}' is already registered")
            cls._defenses[name] = defense_cls
            return defense_cls

        return decorator

    @classmethod
    def get(cls, name: str, model: nn.Module, **kwargs) -> BaseDefense:
        """
        Get a defense instance by name.

        Args:
            name: Name of the registered defense
            model: Model to defend
            **kwargs: Arguments to pass to the defense constructor

        Returns:
            Defense instance

        Raises:
            ValueError: If the defense name is not registered
        """
        if name not in cls._defenses:
            available = ", ".join(cls._defenses.keys())
            raise ValueError(f"Defense '{name}' not found. Available defenses: {available}")

        return cls._defenses[name](model=model, **kwargs)

    @classmethod
    def get_class(cls, name: str) -> Type[BaseDefense]:
        """
        Get a defense class by name.

        Args:
            name: Name of the registered defense

        Returns:
            Defense class
        """
        if name not in cls._defenses:
            available = ", ".join(cls._defenses.keys())
            raise ValueError(f"Defense '{name}' not found. Available defenses: {available}")

        return cls._defenses[name]

    @classmethod
    def list_defenses(cls) -> List[str]:
        """
        List all registered defense names.

        Returns:
            List of defense names
        """
        return list(cls._defenses.keys())

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """
        Check if a defense is registered.

        Args:
            name: Defense name to check

        Returns:
            True if registered, False otherwise
        """
        return name in cls._defenses


def register_defense(name: str):
    """
    Decorator to register a defense class.

    This is a convenience wrapper around DefenseRegistry.register.

    Args:
        name: Name to register the defense under

    Returns:
        Decorator function
    """
    return DefenseRegistry.register(name)
