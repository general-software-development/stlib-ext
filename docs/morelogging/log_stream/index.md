# morelogging.LogStream

## Annotations

```python
from functools import cached_property
import hashlib
import uuid as uuidlib
from typing import Any, Optional
from collections.abc import Iterable

from moretyping.meta import Unknown

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
        self.logLevel = LogLevel.DEBUG

    @property
    def lsi(self) -> LogStreamInfo:
        return LogStreamInfo(name=self.name, logLevel=self.logLevel)

    @cached_property
    def identifier(self) -> str:
        return hashlib.sha3_512(str((self.name, self.uuid)).encode('utf8')).hexdigest()

    def add_handler(self, handler: LogHandler) -> str:
        ...

        return handler.identifier

    def remove_handler(self, handler_id: str) -> LogHandler:
        if h := self.handlers.get(handler_id):
            ...
            return h  # same id
        else:
            raise KeyError(f"Attempted to remove handler with identifier {handler_id} from log stream {self.name} ({self.identifier}), meanwhile {handler_id} was not found.")

    def clear_handlers(self) -> list[LogHandler]:
        h = list(self.handlers.values())
        self.handlers.clear()
        return h

    def _add_item(self, item: Log) -> None:
        self.data.append(item)
        for handler in self.handlers.values():
            handler._push(item)

    def log(self, level: LogLevel, message: str, *objects: Optional[Iterable[Any]],
            exc_info: Optional[Exception] = None) -> None:
        self._add_item(
            Log(
                level = level,
                message = message,
                objects = objects or [],
                lsi = self.lsi,
                exc_info = exc_info
            )
        )

    ...
```

## Properties

`name: str`
: The name associated with the log stream

`stream: LogStream`
: The LogStream behind the log stream

`identifier: str`
: A unique identifier

## Methods

### add_handler

```python
def add_handler(self, handler: LogHandler) -> str:
    ...
```

Adds a log handler to the log stream, and returns its identifier.

### remove_handler

```python
def remove_handler(self, handler_id: str) -> LogHandler:
    ...
```

Removes a handler from the log stream, by its identifier, and returns the log handler instance. It is recommended not to keep the returned instance alive.

### clear_handlers

```python
def clear_handlers(self) -> list[LogHandler]:
    ...
```

Deletes all log handlers form the log stream, returning them in a list. It is recommended not to keep the returned instances alive.

### log

```python
def log(self, level: LogLevel, message: str | Unknown, *objects: Optional[Iterable[Any]],
        exc_info: Optional[Exception] = None) -> None:
    ...
```

Appends a log with log level `level`, message `message`, with the objects specified as positional arguments, and with the Exception passed to `exc_info`, if any.

Objects are concatenated at the end of the message.
