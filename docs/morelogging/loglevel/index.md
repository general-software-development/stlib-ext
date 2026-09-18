# morelogging.LogLevel

## Annotations
```python
from moretyping.data.mutable_enum import MutableEnum

class LogLevelItem:
    ...

class LogLevel(MutableEnum[LogLevelItem]):
    DEBUG = None
    INFO = None
    WARNING = None
    ERROR = None
    CRITICAL = None

def add_log_level(name: str, level: int) -> None:
    LogLevel.add(name, LogLevelItem(level = level, name = name))

add_log_level("DEBUG", 0)
add_log_level("INFO", 20)
add_log_level("WARNING", 40)
add_log_level("ERROR", 60)
add_log_level("CRITICAL", 80)
```

## Properties

* `DEBUG`: log level 0
* `INFO`: log level 20
* `WARNING`: log level 40
* `ERROR`: log level 60
* `CRITICAL`: log level 80

## Adding a log level

To add a log level, use the `add_log_level` function.
