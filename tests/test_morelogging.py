# This file is AI-generated.
# Don't even bother me about it.

from dataclasses import FrozenInstanceError
import logging

import pytest
from pydantic import ValidationError

from base import _TestSuite, static_mark_parametrize
from morelogging import compat
from morelogging.abstract import LogHandler
from morelogging.data_wrappers import Log, LogStreamInfo
from morelogging.enums import LogLevel
from morelogging.log_handlers import SimpleLogHandler
from morelogging.log_stream import LogStream
from morelogging.logger import Logger


class RecordingLogHandler(LogHandler):
    def __init__(self, *, use_default_format=False):
        self.commits = []
        self.use_default_format = use_default_format
        self.opened = False
        self.closed = False
        super().__init__()

    def format(self, log, lsi):
        if self.use_default_format:
            raise NotImplementedError
        return f"{lsi.name}:{log.level.value}:{log.message}"

    def commit(self, log, logdata, lsi):
        self.commits.append((log, logdata, lsi))

    def open(self):
        self.opened = True

    def close(self):
        self.closed = True


class DataWrapperTests(_TestSuite):
    class LogStreamInfoTests(_TestSuite):
        @staticmethod
        def test_fields():
            lsi = LogStreamInfo(name="test")
            assert lsi.name == "test"

        @staticmethod
        def test_frozen():
            lsi = LogStreamInfo(name="test")
            with pytest.raises(FrozenInstanceError):
                lsi.name = "other"

        __targets__ = (test_fields, test_frozen)

    class LogTests(_TestSuite):
        @staticmethod
        def test_basic():
            lsi = LogStreamInfo(name="test")
            log = Log(
                level=LogLevel.INFO,
                message="message",
                objects=(1, "two"),
                lsi=lsi
            )

            assert log.level is LogLevel.INFO
            assert log.message == "message"
            assert log.objects == (1, "two")
            assert log.lsi is lsi
            assert log.exc_info is None

        @staticmethod
        def test_empty_message():
            log = Log(
                level=LogLevel.INFO,
                message="",
                lsi=LogStreamInfo(name="test")
            )
            assert log.message == r"\[NUL]"

        @staticmethod
        def test_objects_are_copied():
            obj = {"values": [1, 2]}
            log = Log(
                level=LogLevel.INFO,
                message="message",
                objects=[obj],
                lsi=LogStreamInfo(name="test")
            )

            obj["values"].append(3)
            assert log.objects == ({"values": [1, 2]},)
            assert log.objects[0] is not obj

        @staticmethod
        def test_invalid_message():
            with pytest.raises(ValidationError):
                Log(
                    level=LogLevel.INFO,
                    message=123,
                    lsi=LogStreamInfo(name="test")
                )

        @staticmethod
        def test_exception_info():
            error = ValueError("bad value")
            log = Log(
                level=LogLevel.ERROR,
                message="failed",
                lsi=LogStreamInfo(name="test"),
                exc_info=error
            )
            assert log.exc_info is error

        @staticmethod
        def test_invalid_exception_info():
            with pytest.raises(ValidationError):
                Log(
                    level=LogLevel.ERROR,
                    message="failed",
                    lsi=LogStreamInfo(name="test"),
                    exc_info=KeyboardInterrupt()
                )

        __targets__ = (
            test_basic,
            test_empty_message,
            test_objects_are_copied,
            test_invalid_message,
            test_exception_info,
            test_invalid_exception_info
        )

    __targets__ = (LogStreamInfoTests, LogTests)


class LogHandlerTests(_TestSuite):
    @staticmethod
    def test_identifier():
        handler = RecordingLogHandler()
        identifier = handler.identifier

        assert len(identifier) == 128
        assert identifier == handler.identifier

    @static_mark_parametrize("attribute", ["name", "uuid"])
    def test_immutable_attributes(attribute):
        handler = RecordingLogHandler()
        with pytest.raises(RuntimeError):
            setattr(handler, attribute, "changed")

    @staticmethod
    def test_push():
        handler = RecordingLogHandler()
        lsi = LogStreamInfo(name="stream")
        log = Log(level=LogLevel.INFO, message="hello", lsi=lsi)

        handler._push(log)

        assert len(handler.commits) == 1
        formatted, logdata, commit_lsi = handler.commits[0]
        assert formatted == "stream:INFO:hello"
        assert logdata is log
        assert commit_lsi is lsi

    @staticmethod
    def test_push_falls_back_to_message():
        handler = RecordingLogHandler(use_default_format=True)
        log = Log(
            level=LogLevel.INFO,
            message="hello",
            lsi=LogStreamInfo(name="stream")
        )

        handler._push(log)

        assert handler.commits[0][0] == "hello"

    @staticmethod
    def test_auto_run_disabled():
        handler = RecordingLogHandler()
        handler.auto_run = False
        log = Log(
            level=LogLevel.INFO,
            message="hello",
            lsi=LogStreamInfo(name="stream")
        )

        handler._push(log)

        assert handler.commits == []

    __targets__ = (
        test_identifier,
        test_immutable_attributes,
        test_push,
        test_push_falls_back_to_message,
        test_auto_run_disabled
    )


class LogStreamTests(_TestSuite):
    @staticmethod
    def test_identifier():
        stream = LogStream("test")
        other = LogStream("test")

        assert len(stream.identifier) == 128
        assert stream.identifier == stream.identifier
        assert stream.identifier != other.identifier

    @static_mark_parametrize("attribute", ["name", "uuid"])
    def test_immutable_attributes(attribute):
        stream = LogStream("test")
        with pytest.raises(RuntimeError):
            setattr(stream, attribute, "changed")

    @staticmethod
    def test_add_handler():
        stream = LogStream("test")
        handler = RecordingLogHandler()

        handler_id = stream.add_handler(handler)

        assert handler_id == handler.identifier
        assert stream.handlers[handler_id] is handler
        assert handler._connect_hook[0] is stream.data

    @staticmethod
    def test_log():
        stream = LogStream("test")
        handler = RecordingLogHandler()
        stream.add_handler(handler)

        stream.log(LogLevel.WARNING, "message", 1, {"a": 2})

        assert len(stream.data) == 1
        log = stream.data[0]
        assert log.level is LogLevel.WARNING
        assert log.message == "message"
        assert log.objects == (1, {"a": 2})
        assert log.lsi == LogStreamInfo(name="test")
        assert handler.commits[0][1] is log

    @staticmethod
    def test_remove_handler():
        stream = LogStream("test")
        handler = RecordingLogHandler()
        handler_id = stream.add_handler(handler)

        removed = stream.remove_handler(handler_id)

        assert removed is handler
        assert handler_id not in stream.handlers
        assert handler._connect_hook == [None]

    @staticmethod
    def test_remove_unknown_handler():
        stream = LogStream("test")
        with pytest.raises(KeyError):
            stream.remove_handler("missing")

    @staticmethod
    def test_clear_handlers():
        stream = LogStream("test")
        handlers = [RecordingLogHandler(), RecordingLogHandler()]
        for handler in handlers:
            stream.add_handler(handler)

        removed = stream.clear_handlers()

        assert removed == handlers
        assert stream.handlers == {}

    @staticmethod
    def test_handler_auto_run_disabled():
        stream = LogStream("test")
        handler = RecordingLogHandler()
        handler.auto_run = False
        stream.add_handler(handler)

        stream.log(LogLevel.INFO, "message")

        assert len(stream.data) == 1
        assert handler.commits == []

    __targets__ = (
        test_identifier,
        test_immutable_attributes,
        test_add_handler,
        test_log,
        test_remove_handler,
        test_remove_unknown_handler,
        test_clear_handlers,
        test_handler_auto_run_disabled
    )


class SimpleLogHandlerTests(_TestSuite):
    @static_mark_parametrize("level", list(LogLevel))
    def test_format(level):
        handler = SimpleLogHandler()
        log = Log(
            level=level,
            message="hello",
            objects=("world", 3),
            lsi=LogStreamInfo(name="stream")
        )

        formatted = handler.format(log, log.lsi)

        assert level.value in formatted
        assert "stream" in formatted
        assert "hello" in formatted
        assert "world 3" in formatted

    @staticmethod
    def test_format_exception():
        handler = SimpleLogHandler()
        error = ValueError("bad value")
        log = Log(
            level=LogLevel.ERROR,
            message="failed",
            lsi=LogStreamInfo(name="stream"),
            exc_info=error
        )

        formatted = handler.format(log, log.lsi)

        assert "ValueError: bad value" in formatted

    @staticmethod
    def test_commit_stdout(capsys):
        handler = SimpleLogHandler()
        log = Log(
            level=LogLevel.INFO,
            message="message",
            lsi=LogStreamInfo(name="stream")
        )

        handler.commit("formatted", log, log.lsi)
        captured = capsys.readouterr()

        assert captured.out == "formatted\n"
        assert captured.err == ""

    @static_mark_parametrize("level", [LogLevel.ERROR, LogLevel.CRITICAL])
    def test_commit_stderr(level, capsys):
        handler = SimpleLogHandler()
        log = Log(
            level=level,
            message="message",
            lsi=LogStreamInfo(name="stream")
        )

        handler.commit("formatted", log, log.lsi)
        captured = capsys.readouterr()

        assert captured.out == ""
        assert captured.err == "formatted\n"

    __targets__ = (test_format, test_format_exception, test_commit_stdout, test_commit_stderr)


class LoggerTests(_TestSuite):
    @staticmethod
    def _make_logger():
        logger = Logger("test")
        logger.clear_handlers()
        handler = RecordingLogHandler()
        logger.add_handler(handler)
        return logger, handler

    @staticmethod
    def test_default_handler():
        logger = Logger("test")
        assert len(logger.stream.handlers) == 1
        assert isinstance(next(iter(logger.stream.handlers.values())), SimpleLogHandler)

    @staticmethod
    def test_identifier():
        logger = Logger("test")
        assert logger.identifier == logger.stream.identifier

    @static_mark_parametrize("method, level", [
        ("debug", LogLevel.DEBUG),
        ("info", LogLevel.INFO),
        ("warning", LogLevel.WARNING)
    ])
    def test_convenience_methods(method, level):
        logger, handler = LoggerTests._make_logger()

        getattr(logger, method)("message", "object")

        log = handler.commits[0][1]
        assert log.level is level
        assert log.message == "message"
        assert log.objects == ("object",)

    @staticmethod
    def test_error_message():
        logger, handler = LoggerTests._make_logger()

        logger.error("failed", 3)

        log = handler.commits[0][1]
        assert log.level is LogLevel.ERROR
        assert log.message == "failed"
        assert log.objects == (3,)
        assert log.exc_info is None

    @staticmethod
    def test_error_exception():
        logger, handler = LoggerTests._make_logger()
        error = ValueError("bad value")

        logger.error(error)

        log = handler.commits[0][1]
        assert log.level is LogLevel.ERROR
        assert log.message == "bad value"
        assert log.exc_info is error

    @staticmethod
    def test_critical_not_implemented():
        logger = Logger("test")
        with pytest.raises(NotImplementedError):
            logger.critical("message")

    @staticmethod
    def test_remove_handler():
        logger, handler = LoggerTests._make_logger()
        logger.remove_handler(handler.identifier)
        assert logger.stream.handlers == {}

    @staticmethod
    def test_clear_handlers():
        logger = Logger("test")
        logger.clear_handlers()
        assert logger.stream.handlers == {}

    __targets__ = (
        test_default_handler,
        test_identifier,
        test_convenience_methods,
        test_error_message,
        test_error_exception,
        test_critical_not_implemented,
        test_remove_handler,
        test_clear_handlers
    )


class CompatTests(_TestSuite):
    class LevelConversionTests(_TestSuite):
        @static_mark_parametrize("name, level", [
            ("NOTSET", LogLevel.DEBUG),
            ("DEBUG", LogLevel.DEBUG),
            ("INFO", LogLevel.INFO),
            ("WARNING", LogLevel.WARNING),
            ("ERROR", LogLevel.ERROR),
            ("CRITICAL", LogLevel.CRITICAL),
            ("CUSTOM", LogLevel.DEBUG)
        ])
        def test_stlib_to_morelogging(name, level):
            assert compat._stlib_logname_to_loglevel(name) is level

        @static_mark_parametrize("level, name", [
            (LogLevel.DEBUG, "DEBUG"),
            (LogLevel.INFO, "INFO"),
            (LogLevel.WARNING, "WARNING"),
            (LogLevel.ERROR, "ERROR"),
            (LogLevel.CRITICAL, "CRITICAL")
        ])
        def test_morelogging_to_stlib(level, name):
            assert compat._loglevel_to_stlib_levelname(level) == name

        __targets__ = (test_stlib_to_morelogging, test_morelogging_to_stlib)

    @staticmethod
    def test_handler_as_stlib_formatter():
        handler = RecordingLogHandler()
        lsi = LogStreamInfo(name="compat")
        formatter = compat.handler_as_stlib_formatter(handler, lsi)
        record = logging.LogRecord(
            name="stdlib",
            level=logging.WARNING,
            pathname=__file__,
            lineno=1,
            msg="hello %s",
            args=("world",),
            exc_info=None
        )

        formatted = formatter.format(record)

        assert formatted == "compat:WARNING:hello world"

    @staticmethod
    def test_handler_as_stlib_handler():
        handler = RecordingLogHandler()
        lsi = LogStreamInfo(name="compat")
        stdlib_handler = compat.handler_as_stlib_handler(handler, lsi)
        record = logging.LogRecord(
            name="stdlib",
            level=logging.ERROR,
            pathname=__file__,
            lineno=1,
            msg="failed",
            args=(),
            exc_info=None
        )

        stdlib_handler.handle(record)

        log = handler.commits[0][1]
        assert log.level is LogLevel.ERROR
        assert log.message == "failed"
        assert log.lsi is lsi

    @staticmethod
    def test_logger_as_stlib_handler():
        logger = Logger("compat")
        logger.clear_handlers()
        recording_handler = RecordingLogHandler()
        logger.add_handler(recording_handler)
        stdlib_handler = compat.logger_as_stlib_handler(logger)
        record = logging.LogRecord(
            name="stdlib",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="hello",
            args=(),
            exc_info=None
        )

        stdlib_handler.handle(record)

        log = recording_handler.commits[0][1]
        assert log.level is LogLevel.INFO
        assert log.message == "hello"

    @staticmethod
    def test_stlib_logger_as_logger():
        records = []

        class CaptureHandler(logging.Handler):
            def emit(self, record):
                records.append(record)

        stdlib_logger = logging.Logger("compat")
        stdlib_logger.setLevel(logging.DEBUG)
        stdlib_logger.addHandler(CaptureHandler())
        logger = compat.stlib_logger_as_logger(stdlib_logger)

        logger.warning("hello", "world")

        assert len(records) == 1
        assert records[0].levelno == logging.WARNING
        assert records[0].msg == "hello"
        assert records[0].args == ("world",)

    __targets__ = (
        LevelConversionTests,
        test_handler_as_stlib_formatter,
        test_handler_as_stlib_handler,
        test_logger_as_stlib_handler,
        test_stlib_logger_as_logger
    )
