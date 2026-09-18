# morelogging.data_wrappers.LogStreamInfo

## Type Annotations
```python
from dataclasses import dataclass
from .enums import LogLevel

@dataclass(frozen=True, slots=True)
class LogStreamInfo:
    name: str
    logLevel: LogLevel = LogLevel.DEBUG
```

## Properties

* `name: str`
: The Log Stream's name

* `logLevel: LogLevel`
: The minimum log level to output (interpreted by log handlers)
