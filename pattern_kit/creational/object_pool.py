from queue import Queue, Empty
from typing import Callable, TypeVar, Generic
from contextlib import contextmanager, asynccontextmanager

import asyncio

T = TypeVar("T")


class ObjectPool(Generic[T]):
    """
    A simple thread-safe object pool for synchronous use.

    This pool reuses objects to avoid repeated construction.
    It does not strictly enforce a maximum number of active objects—
    `max_size` only limits how many can be stored for reuse.
    """

    def __init__(self, factory: Callable[[], T], max_size: int = 10):
        self._factory = factory
        self._pool = Queue(maxsize=max_size)

    def acquire(self) -> T:
        """
        Acquire an object from the pool. If none are available, creates a new one.
        """
        try:
            return self._pool.get_nowait()
        except Empty:
            return self._factory()

    def release(self, obj: T) -> None:
        """
        Return an object to the pool for reuse. If the pool is full, the object is discarded.
        """
        try:
            self._pool.put_nowait(obj)
        except:
            pass

    @contextmanager
    def borrow(self):
        """
        Context manager version of `acquire()` + `release()`.
        """
        obj = self.acquire()
        try:
            yield obj
        finally:
            self.release(obj)

    def clear(self) -> None:
        """Remove all idle objects from the pool."""
        while not self._pool.empty():
            self._pool.get_nowait()

    def __len__(self) -> int:
        """Return the number of idle objects in the pool."""
        return self._pool.qsize()


class AsyncObjectPool(Generic[T]):
    """
    An asyncio-compatible object pool.

    This pool reuses objects to avoid repeated construction.
    It does not strictly enforce a maximum number of active objects—
    `max_size` only limits how many can be stored for reuse.
    """

    def __init__(self, factory: Callable[[], T], max_size: int = 10):
        self._factory = factory
        self._pool = asyncio.Queue(maxsize=max_size)

    async def acquire(self) -> T:
        """
        Acquire an object from the async pool.
        Returns a new one if no reusable objects are available.
        """
        if self._pool.empty():
            return self._factory()
        return await self._pool.get()

    async def release(self, obj: T) -> None:
        """
        Return an object to the pool. If the pool is full, the object is discarded.
        """
        if self._pool.full():
            return
        await self._pool.put(obj)

    @asynccontextmanager
    async def borrow(self):
        """
        Async context manager version of `acquire()` + `release()`.
        """
        obj = await self.acquire()
        try:
            yield obj
        finally:
            await self.release(obj)

    async def clear(self) -> None:
        """Remove all idle objects from the pool."""
        while not self._pool.empty():
            await self._pool.get()

    def __len__(self) -> int:
        """Return the number of idle objects in the pool."""
        return self._pool.qsize()
