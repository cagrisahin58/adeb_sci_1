"""Model registry for managing model architectures."""

from typing import Dict, Type, Optional, Any, List
from .base import BaseModel


class ModelRegistry:
    """
    Registry for model architectures.

    Provides a factory pattern for creating model instances by name.
    """

    _models: Dict[str, Type[BaseModel]] = {}

    @classmethod
    def register(cls, name: str):
        """
        Decorator to register a model class.

        Args:
            name: Name to register the model under

        Returns:
            Decorator function
        """
        def decorator(model_cls: Type[BaseModel]) -> Type[BaseModel]:
            if name in cls._models:
                raise ValueError(f"Model '{name}' is already registered")
            cls._models[name] = model_cls
            return model_cls

        return decorator

    @classmethod
    def get(cls, name: str, **kwargs) -> BaseModel:
        """
        Get a model instance by name.

        Args:
            name: Name of the registered model
            **kwargs: Arguments to pass to the model constructor

        Returns:
            Model instance

        Raises:
            ValueError: If the model name is not registered
        """
        if name not in cls._models:
            available = ", ".join(cls._models.keys())
            raise ValueError(f"Model '{name}' not found. Available models: {available}")

        return cls._models[name](**kwargs)

    @classmethod
    def get_class(cls, name: str) -> Type[BaseModel]:
        """
        Get a model class by name.

        Args:
            name: Name of the registered model

        Returns:
            Model class
        """
        if name not in cls._models:
            available = ", ".join(cls._models.keys())
            raise ValueError(f"Model '{name}' not found. Available models: {available}")

        return cls._models[name]

    @classmethod
    def list_models(cls) -> List[str]:
        """
        List all registered model names.

        Returns:
            List of model names
        """
        return list(cls._models.keys())

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """
        Check if a model is registered.

        Args:
            name: Model name to check

        Returns:
            True if registered, False otherwise
        """
        return name in cls._models


def register_model(name: str):
    """
    Decorator to register a model class.

    This is a convenience wrapper around ModelRegistry.register.

    Args:
        name: Name to register the model under

    Returns:
        Decorator function
    """
    return ModelRegistry.register(name)
