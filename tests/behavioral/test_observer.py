import asyncio
from typing import Any
from unittest.mock import MagicMock, patch

from pattern_kit import Observable, Observer, AsyncObserver


class SyncObserver(Observer):
    def __init__(self):
        self.last_event = None
        self.last_data = None

    def notify(self, event: str, data: Any = None) -> None:
        self.last_event = event
        self.last_data = data


class CustomAsyncObserver(AsyncObserver):
    def __init__(self):
        self.last_event = None
        self.last_data = None

    async def notify(self, event: str, data: Any = None) -> None:
        await asyncio.sleep(0.01)  # simulate async work
        self.last_event = event
        self.last_data = data


def test_add_and_remove_observer():
    obs = Observable()
    sync_observer = SyncObserver()

    obs += sync_observer
    assert sync_observer in obs._observers

    obs -= sync_observer
    assert sync_observer not in obs._observers


def test_sync_observer_notification():
    obs = Observable()
    sync_observer = SyncObserver()
    obs += sync_observer

    obs.notify("on_update", {"data": 42})

    assert sync_observer.last_event == "on_update"
    assert sync_observer.last_data == {"data": 42}


async def test_async_observer_notification_with_notify_async():
    obs = Observable()
    async_observer = CustomAsyncObserver()
    obs += async_observer

    await obs.notify_async("on_async_update", {"key": "value"})

    assert async_observer.last_event == "on_async_update"
    assert async_observer.last_data == {"key": "value"}


async def test_mixed_observers_notify_async():
    obs = Observable()
    sync_observer = SyncObserver()
    async_observer = CustomAsyncObserver()

    obs += sync_observer
    obs += async_observer

    await obs.notify_async("on_mixed_event", 123)

    assert sync_observer.last_event == "on_mixed_event"
    assert sync_observer.last_data == 123
    assert async_observer.last_event == "on_mixed_event"
    assert async_observer.last_data == 123


async def test_async_observer_called_via_notify(monkeypatch):
    obs = Observable()
    async_observer = CustomAsyncObserver()
    obs += async_observer

    with patch("asyncio.create_task", new_callable=MagicMock) as mock_create_task:
        obs.notify("on_event", {"hello": "world"})

        assert mock_create_task.called

        called_coro = mock_create_task.call_args[0][0]
        assert asyncio.iscoroutine(called_coro)

        # Manually close the coroutine to suppress any warning
        called_coro.close()
