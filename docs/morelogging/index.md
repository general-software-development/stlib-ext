# MoreLogging
> Both a replacement and extension of the standard logging library

## Summary
1. [`Logger`](./logger/index.md)
: The user-facing API intended to be used for logging.

2. `LogStream`
: A lower-level but still easily usable logging class, standing as the backend for `Logger`

3. `LogHandler`
: The abstract class for log handlers

4. `LogLevel`
: The enum class for log levels

5. `SimpleLogHandler`
: The default log handler for all `Logger` instances &mdash; a premade implementation of a handler and formatter, featuring automatic log colouring and nice formatting

6. `data_wrappers`
: The internal classes used purely to hold or organise data

7. `compat`
: A compatibility module, for integration with the standard library `logging` library
