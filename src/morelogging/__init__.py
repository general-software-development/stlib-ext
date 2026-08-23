# TODO: integration with logging.py

# built-in
import warnings
from typing import Any, Optional
from collections.abc import Iterable

# Relative
from .logger import Logger

class ExperimentalWarning(Warning):
    ...

warnings.warn("morelogging is experimental and incomplete. It is not ready to be used in production.", ExperimentalWarning)

if True:
    if not __debug__:
        warnings.warn("This is a debug script.")

    stream = Logger("TestLogger")
    stream.log(LogLevel.DEBUG, "Test", "abc", None, {'a': 'bc'})
    stream.log(LogLevel.INFO, "Test", "abc", None, {'a': 'bc'})
    stream.log(LogLevel.CRITICAL, "Test", "abc", None, {'a': 'bc'})
    try:
        def test():
            raise Exception("test")
        test()
    except Exception as e:
        stream.error(e)
