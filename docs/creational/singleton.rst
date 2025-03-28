Singleton
=========

The Singleton pattern ensures that only one instance of a class exists during the lifetime of a program.

`pattern_kit` offers **two clean approaches** for implementing singletons, depending on your style and needs.

Class-based Singleton
---------------------

Inherit from `Singleton` and use `.instance()` to retrieve or create the singleton instance:

.. code-block:: python

    from pattern_kit import Singleton

    class Logger(Singleton):
        def __init__(self, level="info"):
            self.level = level

    log1 = Logger.instance()
    log2 = Logger.instance()

    assert log1 is log2

You can also overwrite the singleton with `.create()`:

.. code-block:: python

    Logger.create(level="debug")

Decorator-based Singleton
--------------------------

Use the `@singleton` decorator to make a class a singleton without needing inheritance:

.. code-block:: python

    from pattern_kit import singleton

    @singleton
    class Tracker:
        def __init__(self):
            self.count = 0

    t1 = Tracker()
    t2 = Tracker()

    assert t1 is t2
    t1.count += 1
    assert t2.count == 1

Choosing Your Style
-------------------

- Use the **class-based `Singleton`** if you want explicit lifecycle control and `.instance()` semantics.
- Use the **`@singleton` decorator** for simplicity and a more functional style.

API Reference
-------------

.. autoclass:: pattern_kit.creational.singleton.Singleton
    :members:
    :undoc-members:
    :show-inheritance:

.. autofunction:: pattern_kit.creational.singleton.singleton
