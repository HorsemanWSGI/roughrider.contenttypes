from typing import Dict
from .meta import ContentType


class Registry:

    __slots__ = ('_types',)

    def __init__(self):
        self._types: Dict[str, ContentType] = {}

    def register(self, name, content_type: ContentType):
        if name in self._types:
            raise KeyError(f'Content type `{name}` already exists.')
        self._types[name] = content_type

    def unregister(self, name):
        if name not in self._types:
            raise KeyError(f'Content type `{name}` is unknown.')
        del self._types[name]

    def __getitem__(self, name) -> ContentType:
        return self._types[name]

    def __len__(self):
        return len(self._types)

    def __iter__(self):
        return iter(self._types)

    def items(self):
        return self._types.items()
