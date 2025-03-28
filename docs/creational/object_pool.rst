Object Pool
===========

The Object Pool pattern allows for the reuse of expensive-to-create objects by keeping a pool of idle instances available for reuse.

This is useful in performance-sensitive or resource-constrained applications, such as:

- Database connections

- Network clients

- Simulation/game objects

- Pre-warmed service workers

`pattern_kit` provides two versions:

- **ObjectPool**: For synchronous usage
- **AsyncObjectPool**: For `asyncio` applications

Overview
--------

When you `acquire()` an object, it is temporarily removed from the pool. When you're done, you `release()` it back for future reuse.

If the pool is empty, a new object is created using the provided `factory`. The pool only limits how many **idle** objects it stores, not how many can be active at once.

Context manager support is available to automatically release objects:

.. code-block:: python

    with pool.borrow() as obj:
        obj.do_something()

    async with async_pool.borrow() as obj:
        await obj.do_something()

Example Usage
-------------

.. code-block:: python

    from pattern_kit import ObjectPool

    class Connection:
        def __init__(self):
            print("Opening connection")

    pool = ObjectPool(factory=Connection, max_size=2)

    conn1 = pool.acquire()
    pool.release(conn1)

    conn2 = pool.acquire()  # Reused connection
    assert conn1 is conn2

Async Usage
-----------

.. code-block:: python

    from pattern_kit import AsyncObjectPool

    class Worker:
        def __init__(self):
            self.jobs = []

    pool = AsyncObjectPool(factory=Worker, max_size=5)

    async def handle():
        async with pool.borrow() as worker:
            worker.jobs.append("job-123")

API Reference
-------------

.. autoclass:: pattern_kit.creational.object_pool.ObjectPool
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: pattern_kit.creational.object_pool.AsyncObjectPool
    :members:
    :undoc-members:
    :show-inheritance:
