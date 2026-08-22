# Built-in
from functools import cached_property
from abc import ABC, abstractmethod
import hashlib
from typing import Any
import uuid as uuidlib
import warnings

# stlib-ext
from moretyping.meta import Unknown
from morefunctools import NotImplemented, notimplemented

# Relative
from .data_wrappers import LogStreamInfo, Log

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
            # ^ Note from same person: i forgot why
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
