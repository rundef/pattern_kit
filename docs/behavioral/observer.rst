Observable / Observer
=====================

The Observer pattern defines a **one-to-many dependency** between objects so that when one object changes state,
all its dependents (observers) are notified and updated automatically.

This module provides a flexible implementation of the pattern, supporting both **synchronous and asynchronous observers**.

Overview
--------

- The `Observable` class maintains a list of observers.
- Observers can be added using `.add_observer()` or the `+=` operator.
- Observers are notified via `.notify()` (non-blocking) or `await .notify_async()` (fully awaited).
- Observers can be either:
  - `Observer`: synchronous, implements `.notify(event, data)`
  - `AsyncObserver`: asynchronous, implements `async def notify(event, data)`

This design is suitable for both event-driven systems and real-time notification use cases.

Example Usage
-------------

.. code-block:: python

    from pattern_kit import Observable, Observer, AsyncObserver

    class SyncListener(Observer):
        def notify(self, event, data=None):
            print(f"[Sync] Event: {event}, Data: {data}")

    class AsyncListener(AsyncObserver):
        async def notify(self, event, data=None):
            print(f"[Async] Event: {event}, Data: {data}")

    obs = Observable()
    obs += SyncListener()
    obs += AsyncListener()

    obs.notify("on_event", {"foo": "bar"})         # Non-blocking notify
    await obs.notify_async("on_event", {"foo": "bar"})  # Awaited notify_async

API Reference
-------------

.. autoclass:: pattern_kit.behavioral.observer.Observable
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: pattern_kit.behavioral.observer.Observer
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: pattern_kit.behavioral.observer.AsyncObserver
    :members:
    :undoc-members:
    :show-inheritance:

