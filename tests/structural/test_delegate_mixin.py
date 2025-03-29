import asyncio
from pattern_kit.structural.delegate_mixin import DelegateMixin

class FakeComponent:
    def foo(self): return "foo"
    def bar(self): return "bar"
    def _private(self): return "should not appear"
    def common(self): return "component"

    async def async_method(self):
        await asyncio.sleep(0)
        return "async_result"


def test_basic_delegation():
    class Wrapper(DelegateMixin):
        def __init__(self, component):
            self._delegate_methods(component)

    w = Wrapper(FakeComponent())
    assert w.foo() == "foo"
    assert w.bar() == "bar"
    assert not hasattr(w, "_private")

def test_namespaced_delegation():
    class Wrapper(DelegateMixin):
        def __init__(self, component):
            self._delegate_methods(component, namespace="comp")

    w = Wrapper(FakeComponent())
    assert w.comp_foo() == "foo"
    assert w.comp_bar() == "bar"
    assert not hasattr(w, "foo")

def test_include_filter():
    class Wrapper(DelegateMixin):
        def __init__(self, component):
            self._delegate_methods(component, include=["foo"])

    w = Wrapper(FakeComponent())
    assert hasattr(w, "foo")
    assert not hasattr(w, "bar")

def test_exclude_filter():
    class Wrapper(DelegateMixin):
        def __init__(self, component):
            self._delegate_methods(component, exclude=["bar"])

    w = Wrapper(FakeComponent())
    assert hasattr(w, "foo")
    assert not hasattr(w, "bar")

def test_include_vs_exclude_precedence():
    class Wrapper(DelegateMixin):
        def __init__(self, component):
            self._delegate_methods(component, exclude=[".*"], include=["foo"])

    w = Wrapper(FakeComponent())
    # Exclude runs first, so foo should be excluded
    assert not hasattr(w, "foo")

def test_conflict_with_existing_method_default():
    class Wrapper(DelegateMixin):
        def __init__(self, component):
            self._delegate_methods(component)

        def common(self):
            return "wrapper"

    w = Wrapper(FakeComponent())
    assert w.common() == "wrapper"

def test_conflict_with_existing_method_overwrite():
    class Wrapper(DelegateMixin):
        def __init__(self, component):
            self._delegate_methods(component, overwrite=True)

        def common(self):
            return "wrapper"

    w = Wrapper(FakeComponent())
    assert w.common() == "component"

async def test_async_method_delegation():
    class Wrapper(DelegateMixin):
        def __init__(self, component):
            self._delegate_methods(component)

    w = Wrapper(FakeComponent())
    result = await w.async_method()
    assert result == "async_result"