from tests.base import _TestSuite
from src import moretyping
import pytest

class DataTests(_TestSuite):
    class Number(_TestSuite):
        class Conversions(_TestSuite):
            @pytest.mark.parametrize("inputData, expected",
                [
                    (2, 2),
                    (4, 4),
                    (5, 5),
                    (-100, -100),
                    (12083, 12083)
                ])
            @staticmethod
            def int_to_int(inputData, expected):
                out = moretyping.data.Number(inputData)
                assert out == expected

            @pytest.mark.parametrize("inputData, expected",
                [
                    (0.0, 0.0),
                    (2.3, 2.3),
                    (-100.2, -100.2),
                    (0.1, 0.1)
                ])
            def float_to_float(self, inputData, expected):
                out = moretyping.data.Number(inputData)
                assert out == expected

            @pytest.mark.parametrize("inputData, expected",
                [
                    ("0", 0.0),
                    ("-1.3", -1.3),
                    ("1", 1),
                    ("2.3", 2.3)
                ])
            def str_to_float(self, inputData, expected):
                out = moretyping.data.Number(inputData)
                assert out == expected

            @pytest.mark.parametrize("invalidInputData", ["s", "avc", "0x2", "1823f"])
            def invalid_str(self, invalidInputData):
                with pytest.raises(ValueError):
                    moretyping.data.Number(invalidInputData)

            def invalid_type(self):
                with pytest.raises(TypeError):
                    moretyping.data.Number(None)

            def test_something(self):
                ...

            __targets__ = (int_to_int, float_to_float, str_to_float, invalid_str, invalid_type)
            
        __targets__ = (Conversions,)
    
    __targets__ = (Number,)
