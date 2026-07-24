from base import _TestSuite, register_test
import pytest

from morefunctools import notimplemented, NotImplemented
from morefunctools.notimplemented import NotImplementedWarning

class NotImplementedTests(_TestSuite):
    class TestErrorBehaviour(_TestSuite):
        @staticmethod
        def test_default():
            @notimplemented(NotImplemented.Default)
            def unfinished():
                return 42

            with pytest.raises(NotImplementedError):
                result = unfinished()

        @staticmethod
        def test_default_2():
            @notimplemented()
            def unfinished():
                return 42

            with pytest.raises(NotImplementedError):
                result = unfinished()

        @staticmethod
        def test_default_3():
            @notimplemented
            def unfinished():
                return 42

            with pytest.raises(NotImplementedError):
                result = unfinished()

        @staticmethod
        def test_abstract():
            @notimplemented(NotImplemented.Abstract)
            def unfinished():
                return 42

            with pytest.raises(NotImplementedError):
                result = unfinished()

        __targets__ = (test_default, test_default_2, test_default_3, test_abstract)

    class TestWarnBehaviour(_TestSuite):
        @staticmethod
        def test_dev():
            @notimplemented(NotImplemented.Development)
            def unfinished():
                return 42

            with pytest.warns(NotImplementedWarning):
                result = unfinished()

            assert result == 42

        @staticmethod
        def test_broken():
            @notimplemented(NotImplemented.Broken)
            def unfinished():
                return 42

            with pytest.warns(NotImplementedWarning):
                result = unfinished()

            assert result == 42

        __targets__ = (test_dev, test_broken)

    class TestUsage(_TestSuite):
        @staticmethod
        def test_normal():
            @notimplemented
            def func1():
                ...
            @notimplemented()
            def func2():
                ...
            @notimplemented(NotImplemented.Default)
            def func3():
                ...
            assert func1 is not None
            assert func2 is not None
            assert func3 is not None

        __targets__ = (test_normal,)

    __targets__ = (TestErrorBehaviour, TestWarnBehaviour, TestUsage)
