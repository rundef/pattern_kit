from pattern_kit import HandlerPipeline, Handler, AsyncHandler


# --- Dummy handlers for tests ---

class AddOneHandler(Handler):
    def handle(self, data):
        return data + 1


class MultiplyHandler(Handler):
    def handle(self, data):
        return data * 2


class StopIfEvenHandler(Handler):
    def handle(self, data):
        if data % 2 == 0:
            return None
        return data


class AlwaysSkipHandler(Handler):
    def can_handle(self, data) -> bool:
        return False

    def handle(self, data):
        return "should not happen"


class TrackingHandler(Handler):
    def __init__(self):
        self.calls = []

    def handle(self, data):
        self.calls.append(data)
        return data


def test_pipeline_pass_result_false_short_circuit_false():
    pipeline = HandlerPipeline(short_circuit=False, pass_result=False)
    pipeline.add_handler(AddOneHandler())
    pipeline.add_handler(MultiplyHandler())

    # Multiply will act on the original input (not AddOne's output)
    result = pipeline.run(3)
    assert result == 3 * 2  # Last handler defines result


def test_pipeline_pass_result_true_short_circuit_false():
    pipeline = HandlerPipeline(short_circuit=False, pass_result=True)
    pipeline.add_handler(AddOneHandler())
    pipeline.add_handler(MultiplyHandler())

    result = pipeline.run(3)
    assert result == (3 + 1) * 2


def test_pipeline_pass_result_true_short_circuit_true_shortcircuits():
    pipeline = HandlerPipeline(short_circuit=True, pass_result=True)
    pipeline.add_handler(AddOneHandler())
    pipeline.add_handler(StopIfEvenHandler())
    pipeline.add_handler(MultiplyHandler())

    result = pipeline.run(3)  # 3+1=4 → StopIfEvenHandler returns None → pipeline stops
    assert result is None


def test_pipeline_pass_result_true_short_circuit_true_no_short_circuit():
    pipeline = HandlerPipeline(short_circuit=True, pass_result=True)
    pipeline.add_handler(AddOneHandler())
    pipeline.add_handler(MultiplyHandler())

    result = pipeline.run(3)  # (3+1)*2 = 8
    assert result == 8


def test_pipeline_with_can_handle_filtering():
    pipeline = HandlerPipeline(short_circuit=False, pass_result=True)
    pipeline.add_handler(AlwaysSkipHandler())
    pipeline.add_handler(AddOneHandler())
    result = pipeline.run(3)
    assert result == 4  # AddOneHandler runs, SkipHandler ignored


def test_pipeline_execution_order():
    tracker = TrackingHandler()
    pipeline = HandlerPipeline(short_circuit=False, pass_result=False)
    pipeline.add_handler(AddOneHandler())
    pipeline.add_handler(tracker)
    pipeline.run(10)
    assert tracker.calls == [10]  # Not 11 — original input passed to tracker


def test_pipeline_result_when_last_handler_is_none_but_no_short_circuit():
    class NullHandler(Handler):
        def handle(self, data):
            return None

    pipeline = HandlerPipeline(short_circuit=False, pass_result=True)
    pipeline.add_handler(AddOneHandler())
    pipeline.add_handler(NullHandler())

    result = pipeline.run(5)
    assert result is None  # Last result is None, but pipeline ran fully


def test_pipeline_result_is_original_when_pass_result_false():
    pipeline = HandlerPipeline(short_circuit=False, pass_result=False)
    pipeline.add_handler(AddOneHandler())
    pipeline.add_handler(MultiplyHandler())
    result = pipeline.run(7)
    assert result == 14  # Multiply(7)



# ---------- async test cases ----------


class SyncAddOne(Handler):
    def handle(self, data):
        return data + 1


class AsyncMultiply(AsyncHandler):
    async def handle(self, data):
        return data * 2


class AsyncStopIfNegative(AsyncHandler):
    async def handle(self, data):
        if data < 0:
            return None
        return data

async def test_async_pipeline_pass_result_true_short_circuit_false():
    pipeline = HandlerPipeline(short_circuit=False, pass_result=True)
    pipeline += SyncAddOne()
    pipeline += AsyncMultiply()
    result = await pipeline.run_async(3)
    assert result == (3 + 1) * 2  # 8


async def test_async_pipeline_short_circuit_triggered():
    pipeline = HandlerPipeline(short_circuit=True, pass_result=True)
    pipeline += SyncAddOne()
    pipeline += AsyncStopIfNegative()
    pipeline += AsyncMultiply()
    result = await pipeline.run_async(-2)  # -2+1 = -1 -> short-circuited b/c negative
    assert result is None

    result = await pipeline.run_async(0)  # (0 + 1) * 2
    assert result == 2


async def test_async_pipeline_with_sync_only_handlers():
    pipeline = HandlerPipeline(short_circuit=False, pass_result=True)
    pipeline += SyncAddOne()
    pipeline += SyncAddOne()
    result = await pipeline.run_async(10)
    assert result == 12

