import pytest
from pattern_kit.creational.factory import Factory, register_factory


class Car:
    def __init__(self, color):
        self.color = color


class Truck:
    def __init__(self, capacity):
        self.capacity = capacity


def setup_function():
    Factory.clear()


def test_register_and_create_car():
    Factory.register("car", Car)
    car = Factory.create("car", color="blue")
    assert isinstance(car, Car)
    assert car.color == "blue"


def test_register_and_create_truck():
    Factory.register("truck", Truck)
    truck = Factory.create("truck", 5000)
    assert isinstance(truck, Truck)
    assert truck.capacity == 5000

def test_decorator():
    @register_factory("logger")
    class Logger:
        pass

    logger = Factory.create("logger")
    assert logger is not None
    assert isinstance(logger, Logger)


def test_create_unregistered_raises():
    with pytest.raises(KeyError, match="No factory registered under key 'plane'"):
        Factory.create("plane")


def test_unregister_factory():
    Factory.register("car", Car)
    assert "car" in Factory._registry

    Factory.unregister("car")
    assert "car" not in Factory._registry


def test_clear_factories():
    Factory.register("car", Car)
    Factory.register("truck", Truck)
    Factory.clear()

    assert Factory._registry == {}
