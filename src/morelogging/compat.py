# Built-in
import logging

# Relative
from .data_wrappers import Log, LogStreamInfo
from .enums import LogLevel
from .log_handlers import LogHandler
from .logger import Logger

def _stlib_logname_to_loglevel(name: str) -> LogLevel:
    match name:
        case 'NOTSET':
            return LogLevel.DEBUG
        case 'DEBUG':
            return LogLevel.DEBUG
        case 'INFO':
            return LogLevel.INFO
        case 'WARNING':
            return LogLevel.WARNING
        case 'ERROR':
            return LogLevel.ERROR
        case 'CRITICAL':
            return LogLevel.CRITICAL
        case _:
            return LogLevel.DEBUG

def _loglevel_to_stlib_levelname(level: LogLevel) -> str:
    match level:
        case LogLevel.DEBUG:    return 'DEBUG'
        case LogLevel.INFO:     return 'INFO'
        case LogLevel.WARNING:  return 'WARNING'
        case LogLevel.ERROR:    return 'ERROR'
        case LogLevel.CRITICAL: return 'CRITICAL'
        case _: return str(_)

def handler_as_stlib_formatter(handler: LogHandler, lsi: LogStreamInfo) -> logging.Formatter:
    class CompatFormatter(logging.Formatter):
        def format(self, record):
            log = Log(
                level=_stlib_logname_to_loglevel(record.levelname),
                message=record.getMessage(),
                objects=record.args,
                lsi=lsi,
                exc_info=record.exc_info[1] if record.exc_info else None
            )
            return handler.format(log, lsi)

    return CompatFormatter()

def handler_as_stlib_handler(handler: LogHandler, lsi: LogStreamInfo) -> logging.Handler:
    class CompatHandler(logging.Handler):
        def emit(self, record):
            log = Log(
                level=_stlib_logname_to_loglevel(record.levelname),
                message=record.getMessage(),
                objects=record.args,
                lsi=lsi,
                exc_info=record.exc_info[1] if record.exc_info else None
            )
            return handler._push(log)  # Formatting is applied automatically by the LogHandler

    h = CompatHandler()
    return h

def logger_as_stlib_handler(logger: Logger) -> logging.Handler:
    class CompatHandler(logging.Handler):
        def emit(self, record):
            logger.log(
                level = _stlib_logname_to_loglevel(record.levelname),
                message=record.getMessage(),
                *record.args,
                exc_info = record.exc_info[1] if record.exc_info else None
            )

    return CompatHandler()

def stlib_logger_as_logger(logger: logging.Logger) -> Logger:
    l = Logger(logger.name)
    l.clear_handlers()

    class CompatHandler(LogHandler):
        def commit(self, log, logdata, lsi):
            logger.log(
                logging.getLevelName(_loglevel_to_stlib_levelname(logdata.level)),
                logdata.message,
                *logdata.objects,
                exc_info=(
                    type(logdata.exc_info), logdata.exc_info, logdata.exc_info.__traceback__
                ) if logdata.exc_info else None
            )

        def format(self, log, lsi):
            return super().format(log, lsi)

        def close(self):
            pass

        def open(self):
            pass

    l.add_handler(CompatHandler())
    return l
