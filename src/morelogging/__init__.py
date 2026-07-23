import uuid
from functools import cached_property
import hashlib
import warnings
from abc import ABC, abstractmethod
from typing import Any
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

class LogHandler(ABC):
    def __init__(self) -> None:
        self.name = f"<{self.__class__.__name__}> {self.__qualname__}"
        self.uuid = uuid.uuid4().hex
        self._connect_hook: list[Any] | None = None
        self._position = 0

    @cached_property
    def identifier(self) -> str:
        return hashlib.sha3_512(str((self.name, self.uuid)))

    @abstractmethod
    def format(self, log) -> str:
        raise NotImplementedError("LogHandler(ABC).format is an abstract method and not implemented.")

    @abstractmethod
    def commit(self, log) -> None:
        raise NotImplementedError("LogHandler(ABC).commit is an abstract method and not implemented.")

    def update(self) -> None:
        if self._connect_hook is None:
            warnings.warn("No hook connected (?). Error 0x1")
            return

        while self._position < len(self._connect_hook) - 1:
            self._push(self._connect_hook[self._position])

    def _push(self, log) -> None:
        self.commit(self.format(log))
        self._position += 1

    def _connect(self, data) -> None:
        self._connect_hook = data

    def __setattr__(self, name, value):
        if name in {'name', 'uuid'}:
            raise RuntimeError(f"Attempted to modify immutable property {LogStream.name} to '{value}'.")
        self.__dict__[name] = value

class LogStream:
    def __init__(self, name: str) -> None:
        self.name = name
        self.uuid = uuid.uuid4().hex
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
            raise RuntimeError(f"Attempted to modify immutable property {LogStream.name} to '{value}'.")
        self.__dict__[name] = value

    def _add_item(self, item: list) -> None:
        self.data.append(item)
        for handler in self.handlers.values():
            handler.push(item)

    def log(self, level: LogLevel, message: str) -> None:
        self._add_item([level, message])
