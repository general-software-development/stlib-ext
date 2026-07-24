import uuid
from functools import cached_property
import hashlib
import warnings
from abc import ABC, abstractmethod
from typing import Any, Optional
from collections.abc import Iterable
from pydantic import BaseModel, field_validator, ValidationInfo
from enum import Enum

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ExperimentalWarning(Warning):
    ...

warnings.warn("morelogging is experimental and incomplete. It is not ready to be used in production.", ExperimentalWarning)

class Log(BaseModel):
    level: LogLevel
    message: str
    objects: Iterable[Any] = tuple()

    @field_validator("message")
    @classmethod
    def check_message(cls, value: str, info: ValidationInfo):
        if not isinstance(value, str):
            if isinstance(value, (BaseException, Warning)) and info.data.get("level") in {LogLevel.ERROR, LogLevel.CRITICAL}:
                pass
            else:
                raise TypeError("Log message is an Exception/Warning, but the log level isnt LogLevel.ERROR or LogLevel.CRITICAL")
        else:
            if len(value) == 0:
                raise ValueError(f"Log message is an empty string ('{value}')")

        return value

    @field_validator("objects")
    @classmethod
    def check_objects(cls, value: Iterable[Any]) -> tuple[Any]:
        if not value:
            return tuple()
        return tuple(value)

class LogHandler(ABC):
    def __init__(self) -> None:
        self.__dict__['name'] = f"<{self.__class__.__name__} instance at 0x{hex(id(self))}>"
        self.__dict__['uuid'] = uuid.uuid4().hex
        self._connect_hook: list[Any] | None = None
        self._position = 0

    @cached_property
    def identifier(self) -> str:
        return hashlib.sha3_512(str((self.name, self.uuid)).encode('utf8'))

    @abstractmethod
    def format(self, log: Log) -> str:
        raise NotImplementedError("LogHandler(ABC).format is an abstract method and not implemented.")

    @abstractmethod
    def commit(self, log: str) -> None:
        raise NotImplementedError("LogHandler(ABC).commit is an abstract method and not implemented.")

    @abstractmethod
    def open(self) -> None:
        raise NotImplementedError("LogHandler(ABC).open is an abstract method and not implemented.")

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError("LogHandler(ABC).close is an abstract method and not implemented.")

    def update(self) -> None:
        if self._connect_hook is None:
            warnings.warn("No hook connected (?). Error 0x1")
            return

        while self._position < len(self._connect_hook) - 1:
            self._push(self._connect_hook[self._position])

    def _push(self, log: Log) -> None:
        self.commit(self.format(log))
        self._position += 1

    def _connect(self, data) -> None:
        self._connect_hook = data

    def __setattr__(self, name, value):
        if name in {'name', 'uuid'}:
            raise RuntimeError(f"Attempted to modify immutable property LogHandler.{name} to '{value}'.")
        self.__dict__[name] = value

class SimpleLogHandler(LogHandler):
    def format(self, log: Log) -> str:
        return f"{log.level.value} {log.message} {' '.join(map(lambda x: str(x), log.objects))}"

    def commit(self, log: str) -> None:
        print(log)

class LogStream:
    def __init__(self, name: str) -> None:
        self.__dict__["name"] = name
        self.__dict__["uuid"] = uuid.uuid4().hex
        self.data = []
        self.handlers = {}

    @cached_property
    def identifier(self) -> str:
        return hashlib.sha3_512(str((self.name, self.uuid)))

    def add_handler(self, handler: LogHandler) -> str:
        handler._connect(self.data)
        self.handlers[handler.identifier] = handler
        return handler.identifier

    def remove_handler(self, handler_id: str) -> LogHandler:
        if h := self.handlers.get(handler_id):
            h._connect(None)
            self.handlers.pop(handler_id)
            return h  # same id
        else:
            raise KeyError(f"Attempted to remove handler with identifier {handler_id} form log stream {self.name} ({self.identifier}), meanwhile {handler_id} was not found.")

    def __setattr__(self, name, value):
        if name in {'name', 'uuid'}:
            raise RuntimeError(f"Attempted to modify immutable property {self.__class__.__name__}.{name} to '{value}'.")
        self.__dict__[name] = value

    def _add_item(self, item: list) -> None:
        self.data.append(item)
        for handler in self.handlers.values():
            handler._push(item)

    def log(self, level: LogLevel, message: str, *objects: Optional[Iterable[Any]]) -> None:
        self._add_item(Log(level=level, message=message, objects=objects or []))

if __name__ == "__main__":
    if not __debug__:
        warnings.warn("This is a debug script.")

    stream = LogStream("MyLogger")
    handler = SimpleLogHandler()
    stream.add_handler(handler)
    stream.log(LogLevel.DEBUG, "Test", "abc", None, {'a': 'bc'})
