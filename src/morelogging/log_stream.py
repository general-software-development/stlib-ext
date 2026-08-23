# Built-in
from functools import cached_property
import hashlib
import uuid as uuidlib
from typing import Any, Optional
from collections.abc import Iterable

# stlib-ext
from moretyping.meta import Unknown

# Relative
from .abstract import LogHandler
from .data_wrappers import Log, LogStreamInfo
from .enums import LogLevel

class LogStream:
    name: str
    uuid: str

    def __init__(self, name: str) -> None:
        self.__dict__["name"] = name
        self.__dict__["uuid"] = uuidlib.uuid4().hex
        self.data: list[Log] = []
        self.handlers: dict[str, LogHandler] = {}

    @cached_property
    def identifier(self) -> str:
        return hashlib.sha3_512(str((self.name, self.uuid)).encode('utf8')).hexdigest()

    def add_handler(self, handler: LogHandler) -> str:
        handler._connect([self.data])
        self.handlers[handler.identifier] = handler
        return handler.identifier

    def remove_handler(self, handler_id: str) -> LogHandler:
        if h := self.handlers.get(handler_id):
            h._connect([None])
            self.handlers.pop(handler_id)
            return h  # same id
        else:
            raise KeyError(f"Attempted to remove handler with identifier {handler_id} from log stream {self.name} ({self.identifier}), meanwhile {handler_id} was not found.")

    def clear_handlers(self) -> list[LogHandler]:
        h = list(self.handlers.values())
        self.handlers.clear()
        return h

    def __setattr__(self, name: str, value: Unknown) -> None:
        if name in {'name', 'uuid'}:
            raise RuntimeError(f"Attempted to modify immutable property {self.__class__.__name__}.{name} to '{value}'.")
        self.__dict__[name] = value

    def _add_item(self, item: Log) -> None:
        self.data.append(item)
        for handler in self.handlers.values():
            handler._push(item)

    def log(self, level: LogLevel, message: str, *objects: Optional[Iterable[Any]],
            exc_info: Optional[Exception] = None) -> None:
        lsi = LogStreamInfo(name=self.name)
        self._add_item(Log(level=level, message=message, objects=objects or [], lsi=lsi, exc_info=exc_info))
    