from dataclasses import dataclass
from typing import Any, Optional
from collections.abc import Iterable
from pydantic import BaseModel, ConfigDict, field_validator, ValidationInfo
from .enums import LogLevel
from copy import deepcopy

@dataclass
class LogStreamInfo:
    name: str

class Log(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    level: LogLevel
    message: str
    objects: Iterable[Any] = tuple()
    lsi: LogStreamInfo
    exc_info: Optional[Exception] = None

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
