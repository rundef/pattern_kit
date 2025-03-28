import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from pattern_kit import EventEmitter


def test_add_and_remove_listener():
    emitter = EventEmitter()
    listener = MagicMock()

    emitter.on("test_event", listener)
    assert listener in emitter._listeners["test_event"]

    emitter.off("test_event", listener)
    assert listener not in emitter._listeners["test_event"]


def test_emit_sync_listener():
    emitter = EventEmitter()
    listener = MagicMock()

    emitter.on("greeting", listener)
    emitter.emit("greeting", {"msg": "hello"})

    listener.assert_called_once_with({"msg": "hello"})


async def test_emit_async_listener():
    emitter = EventEmitter()
    listener = AsyncMock()

    emitter.on("greeting", listener)
    await emitter.emit_async("greeting", {"msg": "hello"})

    listener.assert_awaited_once_with({"msg": "hello"})

async def test_mixed_sync_and_async_emit_async():
    emitter = EventEmitter()
    sync_listener = MagicMock()
    async_listener = AsyncMock()

    emitter.on("event", sync_listener)
    emitter.on("event", async_listener)

    await emitter.emit_async("event", 42)

    sync_listener.assert_called_once_with(42)
    async_listener.assert_awaited_once_with(42)


def test_emit_schedules_async_listeners():
    emitter = EventEmitter()

    async def async_listener(data):
        pass

    emitter.on("event", async_listener)

    with patch("asyncio.create_task", new_callable=MagicMock) as mock_create_task:
        emitter.emit("event", 123)

        assert mock_create_task.called

        called_coro = mock_create_task.call_args[0][0]
        assert asyncio.iscoroutine(called_coro)

        # Manually close the coroutine to suppress any warning
        called_coro.close()
