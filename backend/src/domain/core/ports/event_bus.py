import abc
from collections import defaultdict
from typing import Any, Dict, List
from typing import Union, Callable

from flask import current_app

from domain.core import commands, events
from domain.core.events import EventCallback
from domain.core.topics import Topic
from service_layer.unit_of_work import AbstractUnitOfWork

Message = Union[commands.Command, events.Event]


class AbstractEventBus(abc.ABC):
    @abc.abstractmethod
    def subscribe(self, topic: Topic, callback: EventCallback) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def publish(self, event: Message, uow: AbstractUnitOfWork = None) -> List[Any]:
        raise NotImplementedError


class InMemoryEventBus(AbstractEventBus):
    def __init__(self) -> None:
        super().__init__()
        self._subscriptions: Dict[Topic, List[EventCallback]] = defaultdict(lambda: [])

    def subscribe(self, topic: Topic, callback: EventCallback) -> None:
        print(f"Subscribes to {topic} with {callback}")
        self._subscriptions[topic].append(callback)

    def publish(self, message: Message, uow: AbstractUnitOfWork = None) -> List[Any]:
        results = []
        for callback in set(self._subscriptions[message.topic]):
            if isinstance(message, events.Event):
                self._handle_event(message, callback=callback, uow=uow)
            elif isinstance(message, commands.Command):
                result = self._handle_command(message, callback=callback, uow=uow)
                results.append(result)
            else:
                raise Exception(f'{message} was not an Event or Command')
        return results

    @staticmethod
    def _handle_event(event: events.Event, callback: Callable, uow: AbstractUnitOfWork):
        try:
            callback(event, uow=uow)
        except Exception:
            current_app.logger.exception('Exception handling event %s', event)

    @staticmethod
    def _handle_command(command: commands.Command, callback: Callable, uow: AbstractUnitOfWork):
        current_app.logger.debug('handling command %s', command)
        try:
            result = callback(command, uow=uow)
            return result  # (3)
        except Exception:
            current_app.logger.exception('Exception handling command %s', command)
            raise  # (2)
