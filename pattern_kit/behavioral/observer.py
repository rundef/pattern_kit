from typing import Any, Union
from abc import ABC, abstractmethod
import inspect
import asyncio


class Observer(ABC):
    @abstractmethod
    def notify(self, event: str, data: Any = None) -> None:
        pass


class AsyncObserver(ABC):
    @abstractmethod
    async def notify(self, event: str, data: Any = None) -> None:
        pass


class Observable:
    """
    Observable class that supports both synchronous and asynchronous observers.

    Observers can be added via `add_observer()` or using `+=` operator,
    and removed via `remove_observer()` or `-=` operator.

    You can trigger notifications using either `notify()` (non-blocking)
    or `await notify_async()` (fully awaited).
    """

    def __init__(self) -> None:
        self._observers: list[Union[Observer, AsyncObserver]] = []

    def add_observer(self, observer: Union[Observer, AsyncObserver]) -> None:
        """
        Add an observer to the list of subscribers.
        """
        self._observers.append(observer)

    def remove_observer(self, observer: Union[Observer, AsyncObserver]) -> None:
        """
        Remove an observer from the list of subscribers.
        """
        self._observers.remove(observer)

    def __iadd__(self, observer: Union[Observer, AsyncObserver]):
        """Add observer using `+=` operator."""
        self.add_observer(observer)
        return self

    def __isub__(self, observer: Union[Observer, AsyncObserver]):
        """Remove observer using `-=` operator."""
        self.remove_observer(observer)
        return self


    def notify(self, event: str, data: Any = None) -> None:
        """
        Notify all observers.
        If an observer is asynchronous, it will be scheduled via `asyncio.create_task()` (non-blocking).
        """
        for observer in self._observers:
            method = getattr(observer, "notify", None)
            if inspect.iscoroutinefunction(method):
                asyncio.create_task(method(event, data))
            else:
                method(event, data)

    async def notify_async(self, event: str, data: Any = None) -> None:
        """
        Notify all observers and await any async ones. Sync observers will be called as normal.
        """
        for observer in self._observers:
            method = getattr(observer, "notify", None)
            if inspect.iscoroutinefunction(method):
                await method(event, data)
            else:
                method(event, data)
