.. _service_locator:

Service Locator
===============

The `ServiceLocator` pattern provides a globally accessible registry for managing shared services or dependencies.

It allows components to register and retrieve services without needing direct references or constructor-based injection.

This pattern is useful in small to mid-size applications, plugin-based systems, or when decoupling setup logic from core business logic.

Overview
--------

Services can be:

- Registered with `ServiceLocator.register("key", service)`
- Retrieved with either:

  - `ServiceLocator.get("key")`

  - `ServiceLocator["key"]`

- Unregistered with `ServiceLocator.unregister("key")`
- Checked with either:

  - `ServiceLocator.has("key")`

  - `"key" in ServiceLocator`

You can also inspect the currently registered services by printing the class:

.. code-block:: python

    class ConsoleLogger:
        def log(self, msg): print(msg)

    class FileLogger:
        def __init__(self, path): self.path = path

    class MySQLDatabase:
        def connect(self): ...

    ServiceLocator.register("Loggers", [ConsoleLogger(), FileLogger("logs.txt")])
    ServiceLocator.register("Database", MySQLDatabase())

    print(ServiceLocator)

    # Output:
    # Registered services:
    # Database: object of type MySQLDatabase
    # Loggers:
    #   - object of type ConsoleLogger
    #   - object of type FileLogger

.. note::

    This approach introduces a form of global state. While convenient, it should be used with care in larger systems, as it can obscure true dependencies.

Example Usage
-------------

.. code-block:: python

    from pattern_kit import ServiceLocator

    class Logger:
        def log(self, msg):
            print(f"[LOG] {msg}")

    ServiceLocator.register("logger", Logger())

    logger = ServiceLocator["logger"]
    logger.log("Ready to go!")

    if "logger" in ServiceLocator:
        ServiceLocator.unregister("logger")

API Reference
-------------

.. autoclass:: pattern_kit.architectural.service_locator.ServiceLocator
    :members:
    :undoc-members:
    :show-inheritance:
