import asyncio
import pytest
from pattern_kit.creational.object_pool import ObjectPool, AsyncObjectPool


class MyObject:
    def __init__(self):
        self.value = 0


def test_acquire_and_release():
    pool = ObjectPool(factory=MyObject, max_size=2)

    obj1 = pool.acquire()
    assert isinstance(obj1, MyObject)

    pool.release(obj1)
    assert len(pool) == 1

    obj2 = pool.acquire()
    assert obj1 is obj2  # Reused


def test_create_new_if_pool_empty():
    pool = ObjectPool(factory=MyObject, max_size=1)

    obj1 = pool.acquire()
    obj2 = pool.acquire()

    assert obj1 is not obj2
    assert len(pool) == 0  # Nothing idle


def test_release_discards_if_full():
    pool = ObjectPool(factory=MyObject, max_size=1)

    obj1 = MyObject()
    obj2 = MyObject()

    pool.release(obj1)
    pool.release(obj2)  # Should be discarded silently

    assert len(pool) == 1

def test_sync_context_manager():
    pool = ObjectPool(factory=MyObject)

    with pool.borrow() as obj:
        obj.value = 42

    assert len(pool) == 1

# ---------- async tests ----------

async def test_async_pool_acquire_and_release():
    pool = AsyncObjectPool(factory=MyObject, max_size=2)

    obj1 = await pool.acquire()
    await pool.release(obj1)

    assert len(pool) == 1

    obj2 = await pool.acquire()
    assert obj1 is obj2  # Reused


async def test_async_pool_discard_if_full():
    pool = AsyncObjectPool(factory=MyObject, max_size=1)

    await pool.release(MyObject())
    await pool.release(MyObject())  # Should be silently dropped

    assert len(pool) == 1

async def test_async_context_manager():
    pool = AsyncObjectPool(factory=MyObject)

    async with pool.borrow() as obj:
        obj.value = 99

    assert len(pool) == 1
