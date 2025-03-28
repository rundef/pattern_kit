from collections import defaultdict
from typing import Callable, Any
import inspect
import asyncio


class EventEmitter:
    """
    A lightweight event emitter that supports both synchronous and asynchronous listeners.
    """

    def __init__(self):
        self._listeners: dict[str, list[Callable[[Any], Any]]] = defaultdict(list)

    def on(self, event: str, listener: Callable[[Any], Any]) -> None:
        """
        Register a listener for a given event name.
        """
        self._listeners[event].append(listener)

    def off(self, event: str, listener: Callable[[Any], Any]) -> None:
        """
        Unregister a listener from a given event name.
        """
        self._listeners[event].remove(listener)

    def emit(self, event: str, data: Any = None) -> None:
        """
        Emit an event and notify all registered listeners.

        Async listeners are scheduled using `asyncio.create_task()` (non-blocking).
        """
        for listener in self._listeners.get(event, []):
            if inspect.iscoroutinefunction(listener):
                asyncio.create_task(listener(data))
            else:
                listener(data)

    async def emit_async(self, event: str, data: Any = None) -> None:
        """
        Emit an event and await all async listeners (sync ones are called normally).
        """
        for listener in self._listeners.get(event, []):
            if inspect.iscoroutinefunction(listener):
                await listener(data)
            else:
                listener(data)
