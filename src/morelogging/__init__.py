import uuid as uuidlib
from functools import cached_property
import hashlib
import warnings
from abc import ABC, abstractmethod
from typing import Any, Optional
from collections.abc import Iterable
from pydantic import BaseModel, field_validator, ValidationInfo
from enum import Enum
from morefunctools import NotImplemented, notimplemented
from moretyping.meta import Unknown
import sys
from copy import deepcopy
from moreshell import shell
from dataclasses import dataclass

# TODO: Switch to something that lets users add new log levels
class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ExperimentalWarning(Warning):
    ...

warnings.warn("morelogging is experimental and incomplete. It is not ready to be used in production.", ExperimentalWarning)

@dataclass
class LogStreamInfo:
    name: str

class Log(BaseModel):
    level: LogLevel
    message: str
    objects: Iterable[Any] = tuple()
    lsi: LogStreamInfo

    @field_validator("message")
    @classmethod
    def check_message(cls, value: str | Any, info: ValidationInfo) -> str:
        if not isinstance(value, str):
            if isinstance(value, (BaseException, Warning)) and info.data.get("level") in {LogLevel.ERROR, LogLevel.CRITICAL}:
                pass
            else:
                raise TypeError("Log message is an Exception/Warning, but the log level isnt LogLevel.ERROR or LogLevel.CRITICAL")
        else:
            if len(value) == 0:
                raise ValueError(f"Log message is an empty string ('{value}')")

        return str(value)

    @field_validator("objects")
    @classmethod
    def check_objects(cls, value: Iterable[Any]) -> tuple[Any, ...] | tuple:
        if not value:
            return tuple()
        return tuple(map(lambda x: deepcopy(x), value))

class LogHandler(ABC):
    name: str
    uuid: str

    def __init__(self) -> None:
        self.__dict__['name'] = f"<{self.__class__.__name__} instance at 0x{hex(id(self))}>"
        self.__dict__['uuid'] = uuidlib.uuid4().hex
        self._connect_hook: list[Any] | None = None
        self._position = 0

        self.auto_run = True

    @cached_property
    def identifier(self) -> str:
        return hashlib.sha3_512(str((self.name, self.uuid)).encode('utf8')).hexdigest()

    @abstractmethod
    @notimplemented(NotImplemented.Abstract)
    def format(self, log: Log, lsi: LogStreamInfo) -> str:
        ...

    @abstractmethod
    @notimplemented(NotImplemented.Abstract)
    def commit(self, log: str, lsi: LogStreamInfo) -> None:
        ...

    @abstractmethod
    @notimplemented(NotImplemented.Abstract)
    def open(self) -> None:
        ...

    @abstractmethod
    @notimplemented(NotImplemented.Abstract)
    def close(self) -> None:
        ...

    def __del__(self):
        self.close()

    def update(self) -> None:
        if self._connect_hook is None:
            warnings.warn("No hook connected (?). Error 0x1")
            return

        while self._position < len(self._connect_hook) - 1:
            # TODO: Move this and _push code into __internal_push
            self.commit(self.format(self._connect_hook[self._position]))
            self._position += 1

    def _push(self, log: Log) -> None:
        if not self.auto_run:
            return
        self.commit(self.format(log, log.lsi), log, log.lsi)
        self._position += 1

    def _connect(self, data: list[Log]) -> None:
        self._connect_hook = data

    def __setattr__(self, name: str, value: Unknown) -> None:
        if name in {'name', 'uuid'}:
            raise RuntimeError(f"Attempted to modify immutable property LogHandler.{name} to '{value}'.")
        self.__dict__[name] = value

class SimpleLogHandler(LogHandler):
    def __init__(self) -> None:
        self.colors = {
            LogLevel.DEBUG:     shell.color.FORE_WHITE  + shell.color.STYLE_DIM,
            LogLevel.INFO:      shell.color.FORE_GREEN  + shell.color.STYLE_NORMAL,
            LogLevel.WARNING:   shell.color.FORE_YELLOW + shell.color.STYLE_NORMAL,
            LogLevel.ERROR:     shell.color.FORE_RED    + shell.color.STYLE_NORMAL,
            LogLevel.CRITICAL:  shell.color.FORE_RED    + shell.color.STYLE_BRIGHT
        }

        self.lsi_name_color = shell.color.FORE_MAGENTA + shell.color.STYLE_BRIGHT

        super().__init__()

    # TODO: Custom handling for LogLevel.Error and LogLevel.Critical
    # TODO: Custom rendering for exceptions
    def format(self, log: Log, lsi: LogStreamInfo) -> str:
        return f"{shell.color.STYLE_RESET_ALL}{self.colors.get(log.level)}" \
                + f"[ {log.level.value.ljust(8, ":")} ]\t    " \
                + f"{shell.color.STYLE_RESET_ALL}{self.lsi_name_color}{lsi.name}    " \
                + shell.color.STYLE_RESET_ALL + self.colors.get(log.level) \
                + f"{log.message} " \
                + f"{' '.join(map(lambda x: str(x), log.objects))}{shell.color.STYLE_RESET_ALL}"

    def commit(self, log: str, logi: Log, lsi: LogStreamInfo) -> None:
        print(
            log,
            file=sys.stderr if logi.level in {LogLevel.ERROR, LogLevel.CRITICAL}
                else sys.stdout
        )

    def open(self) -> None:
        pass

    def close(self) -> None:
        sys.stdout.flush()

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

    def log(self, level: LogLevel, message: str, *objects: Optional[Iterable[Any]]) -> None:
        lsi = LogStreamInfo(name=self.name)
        self._add_item(Log(level=level, message=message, objects=objects or [], lsi=lsi))

class Logger:
    def __init__(self, name: str) -> None:
        self.name = name
        self.stream = LogStream(self.name)

        default_handler = SimpleLogHandler()
        self.add_handler(default_handler)

    @property
    def identifier(self) -> str:
        return self.stream.identifier

    def add_handler(self, handler: LogHandler) -> str:
        self.stream.add_handler(handler)

    def remove_handler(self, handler_id: str) -> LogHandler:
        self.stream.remove_handler(handler_id)

    def clear_handlers(self) -> list[LogHandler]:
        self.stream.clear_handlers()

    def log(self, level: LogLevel, message: str | Unknown, *objects: Optional[Iterable[Any]]) -> None:
        self.stream.log(level, message, *objects)

    def debug(self, message: str, *objects: Optional[Iterable[Any]]) -> None:
        self.log(LogLevel.DEBUG, message, *objects)

    def info(self, message: str, *objects: Optional[Iterable[Any]]) -> None:
        self.log(LogLevel.INFO, message, *objects)
    
    
    def warning(self, message: str, *objects: Optional[Iterable[Any]]) -> None:
        self.log(LogLevel.WARNING, message, *objects)
    
    
    def error(self, message: str | Unknown, *objects: Optional[Iterable[Any]]) -> None:
        self.log(LogLevel.ERROR, message, *objects)
    
    @notimplemented
    def critical(self, message: str | Unknown, *objects: Optional[Iterable[Any]]) -> None:
        ...

if __name__ == "__main__":
    if not __debug__:
        warnings.warn("This is a debug script.")

    stream = Logger("TestLogger")
    stream.log(LogLevel.DEBUG, "Test", "abc", None, {'a': 'bc'})
    stream.log(LogLevel.INFO, "Test", "abc", None, {'a': 'bc'})
    stream.log(LogLevel.CRITICAL, "Test", "abc", None, {'a': 'bc'})
