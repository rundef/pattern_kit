HandlerPipeline
===============

The `HandlerPipeline` class provides a flexible processing pipeline, supporting both synchronous and asynchronous handlers.

It uses a single early‑exit mechanism (`StopPipeline`) and an optional data‑flow control flag (`pass_result`).


Overview
--------

Each handler can decide whether to handle a given input using `can_handle()`, and either process it or pass it to the next handler in the chain.

The pipeline supports both synchronous and asynchronous processing via `.run()` and `.run_async()` methods.

You can control pipeline behavior via:

- **Early Exit (StopPipeline)**

  Handlers may terminate the pipeline immediately by raising: `raise StopPipeline(result)`

  When raised, `result` is returned by `.run()` / `.run_async()` (even if result is None).

- **pass_result (bool)**

  - **pass_result=False** (default): every handler receives the original input.

  - **pass_result=True**: each handler receives the previous handler's output as its input.


Example Usage
-------------

.. code-block:: python

    from pattern_kit import HandlerPipeline, Handler, AsyncHandler, StopPipeline

    class Multiply(Handler):
        def handle(self, data):
            if data % 2 == 0:
                # Stop the pipeline if input is an even number
                raise StopPipeline(99)
            return data * 2

    class AsyncAdd(AsyncHandler):
        async def handle(self, data):
            return data + 3

    pipeline = HandlerPipeline(pass_result=True)
    pipeline += Multiply()
    pipeline += AsyncAdd()

    result = await pipeline.run_async(5)  # Result is (5 * 2) + 3 = 13
    result = await pipeline.run_async(6)  # Result is 99

API Reference
-------------

.. autoclass:: pattern_kit.behavioral.handler_pipeline.HandlerPipeline
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: pattern_kit.behavioral.handler_pipeline.Handler
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: pattern_kit.behavioral.handler_pipeline.AsyncHandler
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: pattern_kit.behavioral.handler_pipeline.StopPipeline
    :members:
    :undoc-members:
    :show-inheritance:
