# TODO: integration with logging.py

import uuid as uuidlib
from functools import cached_property
import hashlib
import warnings
from typing import Any, Optional
from collections.abc import Iterable
from morefunctools import notimplemented
from moretyping.meta import Unknown
import sys
from moreshell import shell
import traceback
from .abstract import LogHandler
from .enums import LogLevel
from .data_wrappers import LogStreamInfo, Log

class ExperimentalWarning(Warning):
    ...

warnings.warn("morelogging is experimental and incomplete. It is not ready to be used in production.", ExperimentalWarning)

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

    # TODO: Custom handling for LogLevel.Error and LogLevel.Critical when no message
    def format(self, log: Log, lsi: LogStreamInfo) -> str:
        text = f"{shell.color.STYLE_RESET_ALL}{self.colors.get(log.level)}" \
                + f"[ {log.level.value.ljust(8, ":")} ]\t    " \
                + f"{shell.color.STYLE_RESET_ALL}{self.lsi_name_color}{lsi.name}    " \
                + shell.color.STYLE_RESET_ALL + self.colors.get(log.level) \
                + f"{log.message} " \
                + f"{' '.join(map(lambda x: str(x), log.objects))}{shell.color.STYLE_RESET_ALL}"

        err_color = shell.color.STYLE_DIM
        tb = traceback.format_exception(log.exc_info, limit=6)
        if tb and log.exc_info:
            err = err_color + f"\n    {err_color}# " + '\n'.join(tb).replace("\n", f"\n    {err_color}# ")
        else:
            err = ""
        return text + err + shell.color.STYLE_RESET_ALL

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

    def log(self, level: LogLevel, message: str | Unknown, *objects: Optional[Iterable[Any]],
            exc_info: Optional[Exception] = None) -> None:
        self.stream.log(level, message, *objects, exc_info=exc_info)

    def debug(self, message: str, *objects: Optional[Iterable[Any]]) -> None:
        self.log(LogLevel.DEBUG, message, *objects)

    def info(self, message: str, *objects: Optional[Iterable[Any]]) -> None:
        self.log(LogLevel.INFO, message, *objects)
    
    
    def warning(self, message: str, *objects: Optional[Iterable[Any]]) -> None:
        self.log(LogLevel.WARNING, message, *objects)
    
    
    def error(self, message: str | Unknown, *objects: Optional[Iterable[Any]]) -> None:
        self.log(LogLevel.ERROR, str(message) if isinstance(message, BaseException) else message, *objects,
                 exc_info=message if isinstance(message, BaseException) else None)
    
    @notimplemented
    def critical(self, message: str | Unknown, *objects: Optional[Iterable[Any]]) -> None:
        ...

if True:
    if not __debug__:
        warnings.warn("This is a debug script.")

    stream = Logger("TestLogger")
    stream.log(LogLevel.DEBUG, "Test", "abc", None, {'a': 'bc'})
    stream.log(LogLevel.INFO, "Test", "abc", None, {'a': 'bc'})
    stream.log(LogLevel.CRITICAL, "Test", "abc", None, {'a': 'bc'})
    try:
        def test():
            raise Exception("test")
        test()
    except Exception as e:
        stream.error(e)
