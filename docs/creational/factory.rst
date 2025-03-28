Factory
=======

The `Factory` pattern provides a centralized registry for dynamically creating objects by name.

It allows you to register classes (or any callable) and instantiate them using a string identifier. This pattern is useful in plugin systems, strategy selectors, configuration-driven object creation, and more.

Overview
--------

The factory maintains a registry of constructors (classes or callables). Once registered under a key, the object can be created with optional keyword arguments.

You can also use the `@register_factory("name")` decorator to register classes automatically.

Example Usage
-------------

.. code-block:: python

    from pattern_kit import Factory

    class Car:
        def __init__(self, color):
            self.color = color

    class Truck:
        def __init__(self, capacity):
            self.capacity = capacity

    Factory.register("car", Car)
    Factory.register("truck", Truck)

    car = Factory.create("car", color="blue")
    truck = Factory.create("truck", capacity=5000)

    print(type(car), car.color)
    print(type(truck), truck.capacity)

Decorator Usage
---------------

.. code-block:: python

    from pattern_kit import register_factory, Factory

    @register_factory("car")
    class Car:
        def __init__(self, color):
            self.color = color

    log = Factory.create("car", color="blue")

API Reference
-------------

.. autoclass:: pattern_kit.creational.factory.Factory
    :members:
    :undoc-members:
    :show-inheritance:

.. autofunction:: pattern_kit.creational.factory.register_factory
