# morelogging.LogHandler

## Type Annotation

```python
from functools import cached_property
from abc import ABC, abstractmethod
import hashlib
from typing import Any
import uuid as uuidlib
import warnings

from moretyping.meta import Unknown
from morefunctools import NotImplemented, notimplemented

from .data_wrappers import LogStreamInfo, Log

class LogHandler(ABC):
    name: str
    uuid: str

    def __init__(self) -> None:
        self.__dict__['name'] = f"<{self.__class__.__name__} instance at 0x{hex(id(self))}>"
        self.__dict__['uuid'] = uuidlib.uuid4().hex
        self._connect_hook: list[list[Any]] | None = None
        self._position = 0

        self.auto_run = True

    @cached_property
    def identifier(self) -> str:
        return hashlib.sha3_512(str((self.name, self.uuid)).encode('utf8')).hexdigest()

    @abstractmethod
    def format(self, log: Log, lsi: LogStreamInfo) -> str:
        raise NotImplementedError("format() is not implemented.")

    @abstractmethod
    @notimplemented(NotImplemented.Abstract)
    def commit(self, log: str, logdata: Log, lsi: LogStreamInfo) -> None:
        ...

    def open(self) -> None:
        ...

    @abstractmethod
    @notimplemented(NotImplemented.Abstract)
    def close(self) -> None:
        ...

    def filter(self, log: Log, lsi: LogStreamInfo) -> bool:
        return log.level.value.level < lsi.logLevel.value.level

    def __del__(self):
        self.close()

    def update(self) -> None:
        ...

    def _push(self, log: Log) -> None:
        ...

    ...
```

## Properties

* `name: str`
: A name associated with the Log Handler instance

* `uuid: str`
: An UUID attached to the Log Handler instance

* `auto_run: bool = True`
: Whether the Log Handler should automatically process logs the second they are made.
: If this is disabled, the log handler instance will only process new logs when calling `.update()`

* `identifier: str`
: A unique identifier for this log handler

## Methods

* `filter(self, log: Log, lsi: LogStreamInfo) -> bool`
: A pre-made implementation for the filter() function. If this returns `True`, the log is dropped/ignored and won't be processed by `format()` and `commit()`.

* `update(self) -> None`
: If `auto_run` is disabled, this will make the log handler process any new log entries.
: If `auto_run` is enabled, this will do nothing.

## Abstract Methods

* `format(self, log: Log, lsi: LogStreamInfo) -> str`
: The function that handles formatting the log

* `commit(self, log: str, logdata: Log, lsi: LogStreamInfo) -> None`
: The function that handles committing/saving the log (ex. printing it, saving it to a file)

* `open(self) -> None`
: The function to allocate/prepare resources for the log handler (ex. opening a file). This is currently unused, and **does not require to be implemented.**

* `close(self) -> None`
: The function to close/deallocate the resources for the log handler (ex. closing a file, flushing stdout). Unlike `open()`, this **does** need to be implemented.

* `filter(self, log: Log, lsi: LogStreamInfo) -> bool`
: Determines whether or not a log should be processed/saved. If this returns `True`, the log is dropped, ignored, and not processed. If it returns `False`, that means the log should be kept.

## Pre-made Subclasses

* [`SimpleLogHandler`](./simple_log_handler.md)
