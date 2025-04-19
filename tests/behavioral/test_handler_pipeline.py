import pytest
from pattern_kit import HandlerPipeline, Handler, AsyncHandler, StopPipeline


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
            raise StopPipeline()
        return data


class StopWithValueHandler(Handler):
    def __init__(self, value):
        self.value = value
    def handle(self, data):
        # Demonstrates carrying back a payload
        raise StopPipeline(self.value)


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


# --- sync tests ---

def test_pipeline_pass_result_false():
    pipeline = HandlerPipeline(pass_result=False)
    pipeline.add_handler(AddOneHandler())
    pipeline.add_handler(MultiplyHandler())

    # Multiply acts on the original input, not AddOne's output
    assert pipeline.run(3) == 3 * 2


def test_pipeline_pass_result_true():
    pipeline = HandlerPipeline(pass_result=True)
    pipeline.add_handler(AddOneHandler())
    pipeline.add_handler(MultiplyHandler())

    assert pipeline.run(3) == (3 + 1) * 2


def test_pipeline_can_be_stopped_on_even():
    pipeline = HandlerPipeline(pass_result=True)
    pipeline += AddOneHandler()
    pipeline += StopIfEvenHandler()
    pipeline += MultiplyHandler()

    # 3+1=4 -> StopIfEvenHandler raises StopPipeline -> pipeline.run returns None
    assert pipeline.run(3) is None

    # 2+1=3 -> no exception -> multiply -> 6
    assert pipeline.run(2) == (2 + 1) * 2


def test_pipeline_passes_original_when_pass_result_false():
    tracker = TrackingHandler()
    pipeline = HandlerPipeline(pass_result=False)
    pipeline += AddOneHandler()
    pipeline += tracker
    pipeline.run(10)
    # tracker saw the original 10, not 11
    assert tracker.calls == [10]


def test_pipeline_last_none_result_without_exception():
    class NullHandler(Handler):
        def handle(self, data):
            return None

    pipeline = HandlerPipeline(pass_result=True)
    pipeline += AddOneHandler()
    pipeline += NullHandler()

    # No StopPipeline raised, so last returned value—even if None—is returned
    assert pipeline.run(5) is None


def test_pipeline_stop_with_custom_value():
    pipeline = HandlerPipeline(pass_result=True)
    pipeline += StopWithValueHandler("boom")
    pipeline += AddOneHandler()  # should never run

    assert pipeline.run(123) == "boom"


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
            raise StopPipeline()
        return data


class AsyncStopWithValue(AsyncHandler):
    def __init__(self, value):
        self.value = value

    async def handle(self, data):
        raise StopPipeline(self.value)


async def test_async_pipeline_pass_result_true():
    pipeline = HandlerPipeline(pass_result=True)
    pipeline += SyncAddOne()
    pipeline += AsyncMultiply()
    result = await pipeline.run_async(3)
    assert result == 8  # (3+1)*2


async def test_async_pipeline_stops_on_negative():
    pipeline = HandlerPipeline(pass_result=True)
    pipeline += SyncAddOne()
    pipeline += AsyncStopIfNegative()
    pipeline += AsyncMultiply()

    # -2+1 = -1 -> StopPipeline -> None
    assert await pipeline.run_async(-2) is None
    # 0+1=1 -> continue -> 2
    assert await pipeline.run_async(0) == 2


async def test_async_pipeline_stop_with_value():
    pipeline = HandlerPipeline(pass_result=True)
    pipeline += AsyncStopWithValue("async")
    pipeline += AsyncMultiply()  # should never run

    assert await pipeline.run_async(999) == "async"


async def test_async_pipeline_with_sync_only():
    pipeline = HandlerPipeline(pass_result=True)
    pipeline += SyncAddOne()
    pipeline += SyncAddOne()
    assert await pipeline.run_async(10) == 12
