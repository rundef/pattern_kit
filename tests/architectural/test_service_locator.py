import pytest
from pattern_kit import ServiceLocator


class DummyService:
    def __init__(self, name):
        self.name = name


def setup_function():
    # Ensure clean state before each test
    ServiceLocator.clear()


def test_register_and_get_service():
    service = DummyService("alpha")
    ServiceLocator.register("dummy", service)

    result = ServiceLocator.get("dummy")
    assert isinstance(result, DummyService)
    assert result.name == "alpha"

    result2 = ServiceLocator["dummy"]
    assert result2 is result


def test_missing_service_raises_error():
    with pytest.raises(RuntimeError, match="Unknown service: missing"):
        ServiceLocator.get("missing")



def test_unregister_service():
    ServiceLocator.register("temp", 123)
    assert ServiceLocator.has("temp")
    assert "temp" in ServiceLocator

    ServiceLocator.unregister("temp")
    assert not ServiceLocator.has("temp")
    assert "temp" not in ServiceLocator


def test_clear_all_services():
    ServiceLocator.register("a", 1)
    ServiceLocator.register("b", 2)

    ServiceLocator.clear()
    assert not ServiceLocator.has("a")
    assert not ServiceLocator.has("b")