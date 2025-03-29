.. _delegate_mixin:

DelegateMixin
=============

The `DelegateMixin` is a structural design pattern that dynamically binds public methods from a target object onto the current instance. It simplifies method delegation and supports namespacing, filtering, and conflict resolution.

Use this when you want to:

- Expose another object's methods on your own interface.
- Build adapters, facades, or proxies dynamically.
- Avoid repetitive boilerplate code for delegation.

Example usage:

.. code-block:: python

    class Engine:
        def start(self): return "engine started"
        def stop(self): return "engine stopped"

    class Car(DelegateMixin):
        def __init__(self, engine):
            self._delegate_methods(engine, namespace="engine")

    car = Car(Engine())
    assert car.engine_start() == "engine started"

API
---

.. autoclass:: pattern_kit.structural.delegate_mixin.DelegateMixin
    :members:
    :undoc-members:
    :show-inheritance:

Parameters
~~~~~~~~~~
- **target** (*object*): The object to delegate methods from.
- **namespace** (*str*, optional): A prefix to avoid name collisions.
- **exclude** (*list[str]*, optional): Regex patterns for method names to exclude (default: `['_.*']`).
- **include** (*list[str]*, optional): Regex patterns to selectively include certain method names.
- **overwrite** (*bool*, optional): Whether to overwrite methods if they already exist on `self` (default: `False`).

Behavior
~~~~~~~~
- Only public, callable attributes are considered.
- `exclude` is applied before `include`.
- If `overwrite=False`, existing attributes are preserved.
