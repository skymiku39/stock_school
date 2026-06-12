"""In-process Publish/Subscribe event bus."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import TypeVar

from stock_school.core.events import Event
from stock_school.core.protocols import EventSubscriber

E = TypeVar("E", bound=Event)
Handler = Callable[[Event], None]


class EventBus:
    """Publish events to typed subscribers (Pub/Sub)."""

    def __init__(self) -> None:
        self._handlers: dict[type[Event], list[Handler]] = defaultdict(list)

    def subscribe(self, event_type: type[E], handler: Handler) -> None:
        self._handlers[event_type].append(handler)

    def subscribe_subscriber(self, subscriber: EventSubscriber) -> None:
        """Register a subscriber that dispatches via on_event (all event types)."""
        self.subscribe(Event, subscriber.on_event)

    def publish(self, event: Event) -> None:
        for event_type in type(event).__mro__:
            if not issubclass(event_type, Event):
                continue
            for handler in self._handlers.get(event_type, ()):
                handler(event)
