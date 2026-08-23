# Built-in
from typing import Any, Optional
from collections.abc import Iterable

# stlib-ext
from moretyping.meta import Unknown
from morefunctools.notimplemented import notimplemented

# Relative
from .abstract import LogHandler
from .enums import LogLevel
from .log_stream import LogStream
from .log_handlers import SimpleLogHandler

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
    
    
    def critical(self, message: str | Unknown, *objects: Optional[Iterable[Any]]) -> None:
        self.log(LogLevel.CRITICAL, str(message) if isinstance(message, BaseException) else message, *objects,
                 exc_info=message if isinstance(message, BaseException) else None)
    