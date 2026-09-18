# morelogging.LogHandler

## Type Annotation

```python
import traceback
import sys

import moreshell as shell

from .abstract import LogHandler
from .data_wrappers import Log, LogStreamInfo
from .enums import LogLevel

class SimpleLogHandler(LogHandler):
    def __init__(self) -> None:
        self.colors = {
            LogLevel.DEBUG:     shell.color.FORE_WHITE  + shell.color.STYLE_DIM,
            LogLevel.INFO:      shell.color.FORE_GREEN  + shell.color.STYLE_NORMAL,
            LogLevel.WARNING:   shell.color.FORE_YELLOW + shell.color.STYLE_NORMAL,
            LogLevel.ERROR:     shell.color.FORE_RED    + shell.color.STYLE_NORMAL,
            LogLevel.CRITICAL:  shell.color.FORE_RED    + shell.color.STYLE_BRIGHT
        }

        self.lsi_name_color = shell.color.FORE_MAGENTA + shell.color.STYLE_BRIGHT

        super().__init__()

    def format(self, log: Log, lsi: LogStreamInfo) -> str:
        text = f"{shell.color.STYLE_RESET_ALL}{self.colors.get(log.level)}" \
                + f"[ {log.level.value.name.ljust(8, ":")} ]\t    " \
                + f"{shell.color.STYLE_RESET_ALL}{self.lsi_name_color}{lsi.name}    " \
                + shell.color.STYLE_RESET_ALL + self.colors.get(log.level) \
                + f"{log.message} " \
                + f"{' '.join(map(lambda x: str(x), log.objects))}{shell.color.STYLE_RESET_ALL}"

        err_color = shell.color.STYLE_DIM
        tb = traceback.format_exception(log.exc_info, limit=6)
        if tb and log.exc_info:
            err = err_color + f"\n    {err_color}# " + '\n'.join(tb).replace("\n", f"\n    {err_color}# ")
        else:
            err = ""
        return text + err + shell.color.STYLE_RESET_ALL

    def commit(self, log: str, logi: Log, lsi: LogStreamInfo) -> None:
        print(
            log,
            file=sys.stderr if logi.level in {LogLevel.ERROR, LogLevel.CRITICAL}
                else sys.stdout
        )

    def open(self) -> None:
        pass

    def close(self) -> None:
        sys.stdout.flush()
```

## Properties

* `name: str` (Inherited from [LogHandler](./index.md))
: A name associated with the Log Handler instance

* `uuid: str` (Inherited from [LogHandler](./index.md))
: An UUID attached to the Log Handler instance

* `auto_run: bool = True` (Inherited from [LogHandler](./index.md))
: Whether the Log Handler should automatically process logs the second they are made.
: If this is disabled, the log handler instance will only process new logs when calling `.update()`

* `identifier: str` (Inherited from [LogHandler](./index.md))
: A unique identifier for this log handler

## Notes

The source code was attached here to be used as an example for custom log handlers. This log handler prints logs to the console, automatically nicely formatting Exceptions when printing them, and applying various coloring schemes.
