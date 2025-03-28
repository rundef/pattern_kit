HandlerPipeline
===============

The `HandlerPipeline` class provides a flexible processing pipeline, supporting both
synchronous and asynchronous handlers.

It can be configured to behave like a Pipe and Filter, Chain of Responsibility, or
a short-circuiting processing pipeline.

Overview
--------

Each handler can decide whether to handle a given input using `can_handle()`, and either
process it or pass it to the next handler in the chain.

You can control pipeline behavior via configuration flags:

- **short_circuit (bool)**:
    If enabled, the pipeline stops immediately when a handler returns `None`.

- **pass_result (bool)**:
    If enabled, the result from one handler is passed as input to the next handler.

The pipeline supports both synchronous and asynchronous processing via `.run()` and `.run_async()` methods.

Example Usage
-------------

.. code-block:: python

    from pattern_kit import HandlerPipeline, Handler, AsyncHandler

    class Multiply(Handler):
        def handle(self, data):
            return data * 2

    class AsyncAdd(AsyncHandler):
        async def handle(self, data):
            return data + 3

    pipeline = HandlerPipeline(short_circuit=True, pass_result=True)
    pipeline += Multiply()
    pipeline += AsyncAdd()

    result = await pipeline.run_async(5)  # Result is (5 * 2) + 3 = 13

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

