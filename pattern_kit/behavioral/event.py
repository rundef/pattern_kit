from typing import Callable, Any
import asyncio
import inspect


class Event:
    """
    A lightweight event object that acts like a multicast delegate.

    Listeners can be added with `+=`, removed with `-=`, and all will be called
    when the event is triggered like a function: `event(args...)`.

    Supports both synchronous and asynchronous listeners.
    """

    def __init__(self):
        self._listeners: list[Callable[..., Any]] = []

    def __iadd__(self, listener: Callable[..., Any]) -> "Event":
        """Add a listener to the event."""
        self._listeners.append(listener)
        return self

    def __isub__(self, listener: Callable[..., Any]) -> "Event":
        """Remove a listener from the event."""
        self._listeners.remove(listener)
        return self

    def __call__(self, *args, **kwargs) -> None:
        """
        Call the event and notify all listeners.

        Async listeners are scheduled using `asyncio.create_task()` (non-blocking).
        """
        for listener in self._listeners:
            if inspect.iscoroutinefunction(listener):
                asyncio.create_task(listener(*args, **kwargs))
            else:
                listener(*args, **kwargs)

    async def call_async(self, *args, **kwargs) -> None:
        """
        Await all async listeners. Sync ones are called immediately.
        """
        for listener in self._listeners:
            if inspect.iscoroutinefunction(listener):
                await listener(*args, **kwargs)
            else:
                listener(*args, **kwargs)
