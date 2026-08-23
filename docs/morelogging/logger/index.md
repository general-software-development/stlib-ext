# morelogging.Logger

## Annotations
```python
class Logger:
    def __init__(self, name: str) -> None:
        self.name = name
        self.stream = LogStream(self.name)

        ...
    
    @property
    def identifier(self) -> str:
        ...

    def add_handler(self, handler: LogHandler) -> str:
        ...

    def remove_handler(self, handler_id: str) -> LogHandler:
        ...

    def clear_handlers(self) -> list[LogHandler]:
        ...

    def log(self, level: LogLevel, message: str | Unknown, *objects: Optional[Iterable[Any]],
            exc_info: Optional[Exception] = None) -> None:
        ...

    def debug(self, message: str, *objects: Optional[Iterable[Any]]) -> None:
        ...

    def info(self, message: str, *objects: Optional[Iterable[Any]]) -> None:
        ...

    def warning(self, message: str, *objects: Optional[Iterable[Any]]) -> None:
        ...
    
    def error(self, message: str | Unknown, *objects: Optional[Iterable[Any]]) -> None:
        ...
    
    def critical(self, message: str | Unknown, *objects: Optional[Iterable[Any]]) -> None:
        ...
```

## Properties
`name: str`
: The name associated with the logger

`stream: LogStream`
: The LogStream behind the logger

`identifier: str`
: A unique identifier

## Methods

### add_handler
```python
def add_handler(self, handler: LogHandler) -> str:
    ...
```

Same as [`LogStream.add_handler`](./missing).

### remove_handler
```python
def remove_handler(self, handler_id: str) -> LogHandler:
    ...
```

Same as [`LogStream.remove_handler`](./missing).

### clear_handlers
```python
def clear_handlers(self) -> list[LogHandler]:
    ...
```

Same as [`LogStream.clear_handlers`](./missing).

### log
```python
def log(self, level: LogLevel, message: str | Unknown, *objects: Optional[Iterable[Any]],
        exc_info: Optional[Exception] = None) -> None:
    ...
```

Same as [`LogStream.log`](./missing).

### debug
```python
def debug(self, message: str, *objects: Optional[Iterable[Any]]) -> None:
    ...
```

Prints a `debug` level log. Objects are concatenated at the end of the message.

### info
```python
def info(self, message: str, *objects: Optional[Iterable[Any]]) -> None:
    ...
```

Prints a `info` level log. Objects are concatenated at the end of the message.

### warning
```python
def warning(self, message: str, *objects: Optional[Iterable[Any]]) -> None:
    ...
```

Prints a `warning` level log. Objects are concatenated at the end of the message.

### error
```python
def error(self, message: str | Exception | Unknown, *objects: Optional[Iterable[Any]]) -> None:
    ...
```

Prints a `error` level log. Objects are concatenated at the end of the message.

### critical
```python
def critical(self, message: str | Exception | Unknown, *objects: Optional[Iterable[Any]]) -> None:
    ...
```

Prints a `critical` level log. Objects are concatenated at the end of the message.