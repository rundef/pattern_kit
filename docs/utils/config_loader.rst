Config-Based Instantiation
==========================

These utility functions allow you to dynamically instantiate classes from a configuration dictionary - especially useful when working with environments, plugins, or service registries.

This pattern complements :ref:`ServiceLocator <service_locator>`, enabling flexible, config-driven architecture.

It supports a variety of use cases:

- Creating a single object from config

- Creating multiple objects (e.g. a list of loggers)

- Mixing instantiated objects with raw config values

- Registering objects into the :ref:`ServiceLocator <service_locator>` automatically

Example
-------

This example demonstrates how to define a config dictionary that describes services and loggers,
then dynamically instantiate those classes using a class map. Each object is created and optionally
registered into the :ref:`ServiceLocator <service_locator>` for global access.

.. code-block:: python

    from pattern_kit import build_from_config
    # from .databases import PostgresDatabase, MongoDatabase
    # from .loggers import ConsoleLogger, SlackLogger

    config = {
        "Database": {"class": "PostgresDatabase", "args": {"url": "localhost"}},
        "Loggers": [
            {"class": "SlackLogger", "args": {"channel": "#general"}},
            {"class": "ConsoleLogger"}
        ]
    }

    class_map = {
        "PostgresDatabase": PostgresDatabase,
        "MongoDatabase": MongoDatabase,
        "SlackLogger": SlackLogger,
        "ConsoleLogger": ConsoleLogger,
    }

    components = build_from_config(config, class_map=class_map, register=True)

    # from pattern_kit import ServiceLocator
    # print(ServiceLocator)
    #
    # Registered services:
    # Database: object of type PostgresDatabase
    # Loggers:
    #  - object of type SlackLogger
    #  - object of type ConsoleLogger

Loading from YAML
-----------------

You can load configuration files using PyYAML and pass them directly to `build_from_config()`:

.. code-block:: python

    import yaml
    from pattern_kit import build_from_config

    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    components = build_from_config(config, class_map=my_class_map)

Supported Config Formats
------------------------

The `build_from_config()` function accepts any dictionary-style config.

You can load these from common file formats:

- **YAML** via `PyYAML` (`yaml.safe_load(...)`)

- **JSON** via the standard `json` module

- **TOML** via `tomli` or `tomllib` (Python 3.11+)

- **INI** via `configparser` (convert to dict manually)

- **XML** via `xmltodict` or custom parsing

After loading, simply pass the resulting dict to `build_from_config()`.

API Reference
-------------

.. autofunction:: pattern_kit.utils.config_loader.resolve_class

.. autofunction:: pattern_kit.utils.config_loader.build_object

.. autofunction:: pattern_kit.utils.config_loader.build_from_config

