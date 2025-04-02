from pattern_kit.utils.config_loader import build_from_config
from pattern_kit.architectural.service_locator import ServiceLocator

class DummyBroker:
    def __init__(self, api_key: str):
        self.api_key = api_key

class DummyLogger:
    def __init__(self, level: str = "info"):
        self.level = level

class DummyConsole:
    def __init__(self):
        pass

# Now define tests
def test_single_object_instantiation():
    cfg = {
        "Broker": {
            "class": "DummyBroker",
            "args": {"api_key": "123"}
        }
    }
    class_map = {"DummyBroker": DummyBroker}
    objs = build_from_config(cfg, class_map)

    assert isinstance(objs["Broker"], DummyBroker)
    assert objs["Broker"].api_key == "123"

def test_list_of_objects_instantiation():
    cfg = {
        "Loggers": [
            {"class": "DummyLogger", "args": {"level": "debug"}},
            {"class": "DummyLogger", "args": {"level": "warn"}}
        ]
    }
    class_map = {"DummyLogger": DummyLogger}
    objs = build_from_config(cfg, class_map)

    assert isinstance(objs["Loggers"], list)
    assert objs["Loggers"][0].level == "debug"
    assert objs["Loggers"][1].level == "warn"

def test_raw_config_passthrough():
    cfg = {
        "Settings": {
            "timezone": "UTC",
            "logging_enabled": True
        }
    }
    objs = build_from_config(cfg)

    assert objs["Settings"]["timezone"] == "UTC"
    assert objs["Settings"]["logging_enabled"] is True

def test_mixed_config_with_service_registration():
    ServiceLocator.clear()

    cfg = {
        "Broker": {
            "class": "DummyBroker",
            "args": {"api_key": "999"}
        },
        "Console": {
            "class": "DummyConsole"
        },
        "Loggers": [
            {"class": "DummyLogger", "args": {"level": "debug"}},
            {"class": "DummyLogger", "args": {"level": "warn"}}
        ],
        "Settings": {"env": "dev"}
    }
    class_map = {
        "DummyBroker": DummyBroker,
        "DummyConsole": DummyConsole,
        "DummyLogger": DummyLogger,
    }

    objs = build_from_config(cfg, class_map=class_map, register=True)

    assert "Broker" in ServiceLocator
    assert "Console" in ServiceLocator
    assert "Loggers" in ServiceLocator

    assert isinstance(ServiceLocator["Broker"], DummyBroker)

    assert ServiceLocator["Broker"].api_key == "999"
    assert isinstance(ServiceLocator["Console"], DummyConsole)

    assert ServiceLocator.has("Settings") is True
    assert ServiceLocator["Settings"]["env"] == "dev"

    assert isinstance(ServiceLocator["Loggers"], list)
    assert len(ServiceLocator["Loggers"]) == 2
    assert isinstance(ServiceLocator["Loggers"][0], DummyLogger)
    assert isinstance(ServiceLocator["Loggers"][1], DummyLogger)

    assert ServiceLocator["Loggers"][0].level == "debug"
    assert ServiceLocator["Loggers"][1].level == "warn"
