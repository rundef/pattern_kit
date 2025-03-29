from .architectural.service_locator import ServiceLocator

from .behavioral.event import Event
from .behavioral.event_emitter import EventEmitter
from .behavioral.handler_pipeline import Handler, AsyncHandler, HandlerPipeline
from .behavioral.observer import Observer, AsyncObserver, Observable

from .creational.factory import Factory, register_factory
from .creational.singleton import Singleton, singleton
from .creational.object_pool import ObjectPool, AsyncObjectPool

from .structural.delegate_mixin import DelegateMixin

__all__ = [
    # Architectural patterns
    "ServiceLocator",

    # Behavioral patterns
    "Event",
    "EventEmitter",
    "Handler", "AsyncHandler", "HandlerPipeline",
    "Observable", "Observer", "AsyncObserver",

    # Creational patterns
    "Factory", "register_factory",
    "Singleton", "singleton",
    "ObjectPool", "AsyncObjectPool",

    # Structural patterns
    "DelegateMixin",
]

__version__ = '1.2.0'
