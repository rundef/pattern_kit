from abc import ABC, abstractmethod
from typing import Any, Union
import inspect

class StopPipeline(Exception):
    """
    Raised by handlers to exit the pipeline early.
    Optionally carry a `result` to return from `run` or `run_async`.
    """
    def __init__(self, result: Any = None):
        super().__init__()
        self.result = result

class Handler(ABC):
    """
    Base handler class for use in a HandlerPipeline.
    Override `can_handle()` and `handle()` as needed.
    """

    def can_handle(self, data: Any, **kwargs) -> bool:
        """Override if you want filtering behavior. Default: always handle."""
        return True

    @abstractmethod
    def handle(self, data: Any, **kwargs) -> Any:
        """Perform processing on data and return result."""
        pass

class AsyncHandler(ABC):
    """
    Base handler class for use in a HandlerPipeline.
    Override `can_handle()` and `handle()` as needed.
    """

    def can_handle(self, data: Any, **kwargs) -> bool:
        """Override if you want filtering behavior. Default: always handle."""
        return True

    @abstractmethod
    async def handle(self, data: Any, **kwargs) -> Any:
        """Perform processing on data and return result."""
        pass


class HandlerPipeline:
    """
    A configurable pipeline of handlers.

    Args:
        pass_result (bool): If True, result of each handler is passed to the next handler.
    """

    def __init__(self, pass_result: bool = False):
        self._handlers: list[Union[Handler, AsyncHandler]] = []
        self._pass_result = pass_result

    def add_handler(self, handler: Union[Handler, AsyncHandler]) -> None:
        """
        Add an handler.
        """
        self._handlers.append(handler)

    def remove_handler(self, handler: Union[Handler, AsyncHandler]) -> None:
        """
        Remove an handler.
        """
        self._handlers.remove(handler)

    def __iadd__(self, handler: Union[Handler, AsyncHandler]):
        """Add handler using `+=` operator."""
        self.add_handler(handler)
        return self

    def __isub__(self, handler: Union[Handler, AsyncHandler]):
        """Remove handler using `-=` operator."""
        self.remove_handler(handler)
        return self

    def run(self, data: Any, **kwargs) -> Any:
        """
        Run the pipeline.
        """
        result = current = data
        try:
            for handler in self._handlers:
                if handler.can_handle(current, **kwargs):
                    result = handler.handle(current, **kwargs)

                    if self._pass_result:
                        current = result

        except StopPipeline as stop:
            return stop.result

        return result

    async def run_async(self, data: Any, **kwargs) -> Any:
        """
        Run the pipeline asynchronously.
        Supports both sync and async handlers transparently.
        """
        result = current = data

        try:
            for handler in self._handlers:
                if handler.can_handle(current, **kwargs):
                    method = getattr(handler, "handle", None)
                    if inspect.iscoroutinefunction(method):
                        result = await method(current, **kwargs)
                    else:
                        result = method(current, **kwargs)

                    if self._pass_result:
                        current = result

        except StopPipeline as stop:
            return stop.result

        return result
