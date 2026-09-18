# morelogging.data_wrappers.LogStreamInfo

## Type Annotations

```python
# Built-in
from typing import Any, Optional
from collections.abc import Iterable
from pydantic import BaseModel, ConfigDict
from .enums import LogLevel

class LogStreamInfo:
    name: str
    logLevel: LogLevel = LogLevel.DEBUG

class Log(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    level: LogLevel
    message: str
    objects: Iterable[Any] = tuple()
    lsi: LogStreamInfo  # you can guess what this stands for
    exc_info: Optional[Exception] = None

    ...
```

## Properties

* `level: LogLevel`
: The log level associated with the Log

* `message: str`
: The log's message

* `objects: Iterable[any] = tuple()`
: Additional objects of any type attached to the log, if any

* `lsi: LogStreamInfo`

* `exc_info: Optional[Exception] = None`
: The exception associated with the log, if any
