from pattern_kit import Singleton, singleton


class MySingleton(Singleton):
    def __init__(self, value: int = 0):
        self.value = value


def test_create_and_instance_are_same():
    instance1 = MySingleton.create(value=42)
    instance2 = MySingleton.instance()

    assert instance1 is instance2
    assert instance2.value == 42


def test_instance_auto_creation():
    # Reset state
    MySingleton.instances.clear()

    # instance() should auto-create if not already existing
    instance = MySingleton.instance(value=99)
    assert isinstance(instance, MySingleton)
    assert instance.value == 99


def test_create_overwrites_previous_instance():
    MySingleton.create(value=1)
    first = MySingleton.instance()
    assert first.value == 1

    MySingleton.create(value=999)
    second = MySingleton.instance()
    assert second.value == 999
    assert first is not second


def test_instance_doesnt_overwrite():
    # Reset state
    MySingleton.instances.clear()

    instance = MySingleton.instance(value=99)

    instance2 = MySingleton.instance(value=100)
    assert instance2.value == 99
    assert instance2 is instance

# ---------- Decorator-based Singleton ----------

@singleton
class DecoratedSingleton:
    def __init__(self):
        self.counter = 0


def test_decorator_singleton_identity():
    a = DecoratedSingleton()
    b = DecoratedSingleton()
    assert a is b


def test_decorator_singleton_state_persistence():
    inst = DecoratedSingleton()
    inst.counter += 1

    again = DecoratedSingleton()
    assert again.counter == 1