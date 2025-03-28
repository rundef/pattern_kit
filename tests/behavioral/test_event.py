import asyncio
from unittest.mock import MagicMock, AsyncMock
from pattern_kit.behavioral.event import Event


def test_event_add_and_remove_listeners():
    event = Event()
    listener = MagicMock()

    event += listener
    assert listener in event._listeners

    event -= listener
    assert listener not in event._listeners


def test_event_calls_sync_listeners():
    event = Event()
    listener = MagicMock()
    event += listener

    event("data", key="value")
    listener.assert_called_once_with("data", key="value")

# ---------- async tests ----------

async def test_event_calls_async_listeners_with_call_async():
    event = Event()
    listener = AsyncMock()
    event += listener

    await event.call_async("payload")
    listener.assert_awaited_once_with("payload")


async def test_event_calls_mixed_listeners_with_call_async():
    event = Event()
    sync_listener = MagicMock()
    async_listener = AsyncMock()

    event += sync_listener
    event += async_listener

    await event.call_async("mixed")
    sync_listener.assert_called_once_with("mixed")
    async_listener.assert_awaited_once_with("mixed")


async def test_event_call_schedules_async_listeners():
    event = Event()
    listener = AsyncMock()
    event += listener

    event("fire-and-forget")

    # Let the event loop run a bit to schedule the async listener
    await asyncio.sleep(0.05)
    listener.assert_awaited_once_with("fire-and-forget")
