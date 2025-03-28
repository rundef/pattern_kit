Event
=====

The `Event` class is a lightweight multicast delegate that supports both synchronous and asynchronous listeners.

This pattern is useful when you want to notify multiple callbacks of a single event, such as in plugin systems, GUI toolkits, or loosely coupled applications. It provides an elegant alternative to more verbose observer implementations or string-based event emitters.

Overview
--------

- Add a listener with ``+=`` (function, method, or coroutine)
- Remove a listener with ``-=``
- Trigger the event with ``event(args...)`` (non-blocking)
- Use ``await event.call_async(...)`` to await all listeners

Example Usage
-------------

.. code-block:: python

    from pattern_kit import Event

    def on_document_loaded(doc):
        print("Sync listener:", doc)

    async def on_document_async(doc):
        print("Async listener:", doc)

    on_new_document = Event()
    on_new_document += on_document_loaded
    on_new_document += on_document_async

    # Fire-and-forget (async listeners will run in background)
    on_new_document("report.pdf")

    # Fully awaited (awaits async listeners)
    await on_new_document.call_async("report.pdf")

API Reference
-------------

.. autoclass:: pattern_kit.behavioral.event.Event
    :members:
    :undoc-members:
    :show-inheritance:
