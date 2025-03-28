EventEmitter
============

The `EventEmitter` class provides a simple and flexible way to implement an **event-driven architecture** in Python.

It allows you to register event listeners and emit events to notify those listeners. The emitter supports both **synchronous and asynchronous** listeners.

Overview
--------

Listeners can be registered using `.on(event, listener)` and removed using `.off(event, listener)`.  
To emit events, you can use `.emit()` (non-blocking) or `await .emit_async()` (fully awaited).

This pattern is well suited for applications such as:

- Decoupled service layers

- Message/event bus systems

- Plugin architectures

- Real-time user interfaces

Example Usage
-------------

.. code-block:: python

    from pattern_kit import EventEmitter

    def on_data_received(data):
        print(f"[Sync] Got data: {data}")

    async def on_data_async(data):
        print(f"[Async] Got data: {data}")

    emitter = EventEmitter()
    emitter.on("data", on_data_received)
    emitter.on("data", on_data_async)

    emitter.emit("data", {"value": 42})         # Non-blocking
    await emitter.emit_async("data", {"value": 42})  # Awaited

    emitter.off("data", on_data_received)

API Reference
-------------

.. autoclass:: pattern_kit.behavioral.event_emitter.EventEmitter
    :members:
    :undoc-members:
    :show-inheritance:

