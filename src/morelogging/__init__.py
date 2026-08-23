# Relative
from .logger import Logger
from .enums import LogLevel
from .abstract import LogHandler
from .log_handlers import SimpleLogHandler
from .log_stream import LogStream
from . import data_wrappers
from . import compat

if True:
    import warnings

    if not __debug__:
        warnings.warn("This is a debug script.")

    stream = Logger("TestLogger")
    stream.log(LogLevel.DEBUG, "Test", "abc", None, {'a': 'bc'})
    stream.log(LogLevel.INFO, "Test", "abc", None, {'a': 'bc'})
    stream.log(LogLevel.CRITICAL, "Test", "abc", None, {'a': 'bc'})
    try:
        def test():
            raise Exception("test error")
        test()
    except Exception as e:
        stream.error(e)

    import logging
    logging_logger = logging.getLogger("testLogger-logging")
    logging_logger.propagate = False
    logging_logger.setLevel(logging.DEBUG)
    logging_logger.addHandler(compat.handler_as_stlib_handler(SimpleLogHandler(), data_wrappers.LogStreamInfo(name="FakeTestLogger")))
    logging_logger.info("stuff %s %s", "test", "stuff")

    reverse_logger = compat.stlib_logger_as_logger(logging.root)
    reverse_logger.error("logging.py test message")

    stream.info("done")
