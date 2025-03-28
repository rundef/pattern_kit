from typing import Type, Any, Dict


class Factory:
    """
    A simple, extensible Factory pattern implementation.

    Allows registering classes or callables by name,
    then instantiating them via `.create("name", **kwargs)`.
    """

    _registry: Dict[str, Type] = {}

    @classmethod
    def register(cls, key: str, constructor: Type) -> None:
        """Register a class or callable under a name."""
        cls._registry[key] = constructor

    @classmethod
    def create(cls, key: str, *args, **kwargs) -> Any:
        """
        Create an instance of the registered class or factory function.
        """
        if key not in cls._registry:
            raise KeyError(f"No factory registered under key '{key}'")
        return cls._registry[key](*args, **kwargs)

    @classmethod
    def unregister(cls, key: str) -> None:
        """Remove a registered factory."""
        cls._registry.pop(key, None)

    @classmethod
    def clear(cls) -> None:
        """Clear all registered factories."""
        cls._registry.clear()

def register_factory(key: str):
    """
    Decorator that registers a class or callable into the Factory registry.
    """
    def decorator(cls_or_func):
        Factory.register(key, cls_or_func)
        return cls_or_func
    return decorator
