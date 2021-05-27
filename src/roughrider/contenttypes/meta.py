from abc import ABCMeta
from datetime import datetime
from collections import UserDict, OrderedDict
from typing import Dict, NamedTuple, Type, Optional, Callable, ClassVar


class Action(NamedTuple):
    name: str
    title: str
    css: str
    resolve: Callable


class Actions(OrderedDict):

    def register(self, id: str, title: str = None, css: str = ''):
        def register_resolver(func):
            self[id] = Action(name=id, title=title, css=css, resolve=func)
            return func
        return register_resolver


class ActionRegistry(ABCMeta):

    def __new__(mcls, name, bases, namespace):
        if namespace.get('actions') is None:
            namespace['actions'] = Actions()
        return super().__new__(mcls, name, bases, namespace)


class Content(UserDict, metaclass=ActionRegistry):
    id: str
    title: str
    date: datetime
    state: str
    actions: ClassVar[Actions]

    @property
    def date(self):
        return self['creation_date']

    @classmethod
    def create(cls, data: Dict):
        data['creation_date'] = datetime.now()
        return cls(data)


class ContentType:

    __slots__ = ('factory',)

    factory: Type[Content]

    def __init__(self, factory):
        self.factory = factory
