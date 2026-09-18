# moretyping.data.Number

## Annotations

```python
from moretyping.meta import Unknown

class MutableEnumMeta(type):
    ...

class MutableEnum[T = Unknown](metaclass=MutableEnumMeta):
    def __init__(self, object: T) -> None:
        self.value = object

    def __init_subclass__(cls):
        cls._members = {}

    @classmethod
    def add(cls, name, value):
        if hasattr(cls, name) and getattr(cls, name) is not None:
            raise ValueError(f"{cls.__name__} already has an attribute named {name!r}")

        member = cls(value)
        cls._members[name] = member
        setattr(cls, name, member)
        return member

    def __getattribute__(self, name: str) -> T:
        return super().__getattribute__(name)
```

## Parameters

`SomeEnum.item.value: T`
: The value of the item. Identical API to the built-in `enum`

## Methods

`SomeEnum.add(name: str, value: T)`
: Add an enum item with the name `name`, and the value `value`.

## Example

This is an example from [`morelogging`](../../morelogging/loglevel/index.md):

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

```python
LogLevel.DEBUG  # LogLevel instance
LogLevel.DEBUG.value  # LogLevelItem(level = 0, name = "DEBUG")
```
