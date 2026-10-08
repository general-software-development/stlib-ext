# morelogging.compat

## `handler_as_stlib_formatter()`

### Signature

```python
def handler_as_stlib_formatter(handler: LogHandler, lsi: LogStreamInfo) -> logging.Formatter:
    ...
```

### Arguments

`handler: LogHandler`
: A morelogging log handler

`lsi: LogStreamInfo`
: A morelogging LSI object ([`LogStreamInfo`](../data_wrappers/lsi.md), obtained from [`LogStream.lsi`](../log_stream/index.md))

### Return Value

Returns an instance of a custom subclass of `logging.Formatter`, that redirects all logs to a morelogging log handler's formatter.

## `handler_as_stlib_handler()`  <!-- Documenting this stuff is eating me alive -->

### Signature

```python
def handler_as_stlib_handler(handler: LogHandler, lsi: LogStreamInfo) -> logging.Handler:
    ...
```

### Arguments

`handler: LogHandler`
: A morelogging log handler

`lsi: LogStreamInfo`
: A morelogging LSI object ([`LogStreamInfo`](../data_wrappers/lsi.md), obtained from [`LogStream.lsi`](../log_stream/index.md))

### Return Value

Returns an instance of a custom subclass of `logging.Handler`, that redirects all logs to a morelogging log handler.

## `logger_as_stlib_handler()`

### Signature

```python
def logger_as_stlib_handler(logger: Logger) -> logging.Handler:
    ...
```

### Arguments

`logger: Logger`
: A morelogging logger object

### Return Value

Returns a logging Handler that redirects all logs to the morelogging Logger `logger`.

## `stlib_logger_as_logger()`

### Signature

```python
def stlib_logger_as_logger(logger: logging.Logger) -> Logger:
    ...
```

### Arguments

`logger: logging.Logger`
: A logging.Logger object

### Return Value

Returns a `morelogging.Logger` instance that redirects all logs to the `logging.Logger` instance passed via `logger`.
