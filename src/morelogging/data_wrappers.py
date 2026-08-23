# Built-in
from dataclasses import dataclass
from typing import Any, Optional
from collections.abc import Iterable
from copy import deepcopy

# External
from pydantic import BaseModel, ConfigDict, field_validator, ValidationInfo

# Relative
from .enums import LogLevel

@dataclass(frozen=True, slots=True)
class LogStreamInfo:
    name: str

class Log(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    level: LogLevel
    message: str
    objects: Iterable[Any] = tuple()
    lsi: LogStreamInfo  # you can guess what this stands for
    exc_info: Optional[Exception] = None

    @field_validator("message")
    @classmethod
    def check_message(cls, value: str | Any, info: ValidationInfo) -> str:
        # Is it not a string?
        if not isinstance(value, str):
            raise TypeError("Log message is an Exception/Warning, but the log level isnt LogLevel.ERROR or LogLevel.CRITICAL")
        # It is a string
        else:
            if len(value) == 0:
                value = '\\[NUL]'

        return value

    @field_validator("objects")
    @classmethod
    def check_objects(cls, value: Iterable[Any]) -> tuple[Any, ...] | tuple:
        if not value:
            return tuple()
        return tuple(map(lambda x: deepcopy(x), value))

    @field_validator("exc_info")
    @classmethod
    def check_exc_info(cls, value: Optional[Exception]) -> Exception | None:
        if value is None:
            return value
        if not isinstance(value, BaseException):
            raise TypeError("exc_info is not of type `Exception`.")
        if not isinstance(value, Exception):
            raise TypeError("exc_info cannot be of type `BaseException` (has to be Exception).")
        return value
