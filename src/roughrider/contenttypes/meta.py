from abc import ABCMeta, abstractmethod
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


class Metadata(NamedTuple):
    id: str
    title: str
    date: datetime
    state: str


class Content(UserDict, metaclass=ActionRegistry):
    metadata: Metadata
    actions: ClassVar[Actions]

    def __init__(self, data):
        self.metadata = self.get_metadata(data)
        super().__init__(data)

    @staticmethod
    @abstractmethod
    def get_metadata(data: Dict) -> Metadata:
        raise NotImplementedError('Override in your class.')

    @classmethod
    def create(cls, data: Dict):
        data['creation_date'] = datetime.now()
        return cls(data)


class ContentType:

    __slots__ = ('factory',)

    factory: Type[Content]

    def __init__(self, factory):
        self.factory = factory
