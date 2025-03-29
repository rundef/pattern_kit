from typing import Any, Dict

class ServiceLocatorMeta(type):
    def __contains__(cls, key: str) -> bool:
        return cls.has(key)

    def __getitem__(cls, key: str) -> Any:
        return cls.get(key)

    def __str__(cls):
        lines = ["Registered services:"]
        for key, val in cls.registered.items():
            if isinstance(val, list):
                lines.append(f"{key}:")
                for item in val:
                    lines.append(f"  - object of type {type(item).__name__}")
            else:
                lines.append(f"{key}: object of type {type(val).__name__}")
        return "\n".join(lines)

    __repr__ = __str__

class ServiceLocator(metaclass=ServiceLocatorMeta):
    """
    A simple Service Locator pattern implementation.

    This class acts as a global registry for services or dependencies.
    It allows you to register, retrieve, and unregister services by key or type.
    """
    registered: Dict[str, Any] = {}

    @classmethod
    def register(cls, key: str, service: Any) -> None:
        """Register a service by name/key."""
        cls.registered[key] = service

    @classmethod
    def get(cls, key: str) -> Any:
        """Retrieve a service by name/key."""
        if key not in cls.registered:
            raise RuntimeError(f"Unknown service: {key}")
        return cls.registered.get(key)

    @classmethod
    def unregister(cls, key: str) -> None:
        """Unregister a service by name/key."""
        cls.registered.pop(key, None)

    @classmethod
    def has(cls, key: str) -> bool:
        """Check if a service is registered."""
        return key in cls.registered

    @classmethod
    def clear(cls) -> None:
        """Remove all registered services."""
        cls.registered.clear()
