from __future__ import annotations
from ._complex import Complex
import math
from ._equation import Equation

class Root:
    def __new__(cls, value: int | float | Root, exp: int = 2):
        if value >= 0:
            if value ** (1/exp) % 1 == 0:
                return value ** (1/exp)
        elif exp % 2 != 0 and (value * -1) ** (1/exp) % 1 == 0:
            return -1 * (-1 * value) ** (1/exp)
        elif (value * -1) ** (1/exp) % 1 == 0:
            if exp == 2:
                return Complex(0, (value * -1) ** (1/exp))
            else:
                return Complex(0, 0, **{f"i{exp}": (value * -1) ** (1/exp)})

        if not isinstance(exp, int):
            raise TypeError("Root exponent needs to be an integer.")

        return super().__new__(cls)

    def __init__(self, value: int | float | Root, exp: int = 2):
        self.value = value
        self.exp = exp

        if isinstance(self.value, Root):
            self.exp = self.exp * self.value.exp
            self.value = self.value.value

    def __str__(self) -> str:
        return f"Root[{self.exp}]({self.value})"

    def __add__(self, other):
        return Equation(self) + other

    def __sub__(self, other):
        return Equation(self) - other

    def __mul__(self, other):
        return Equation(self) * other

    def __truediv__(self, other):
        return Equation(self) / other

    def __floordiv__(self, other):
        return Equation(self) // other

    def __radd__(self, other):
        return Equation(other) + self

    def __rsub__(self, other):
        return Equation(other) - self

    def __rmul__(self, other):
        return Equation(other) * self

    def __rtruediv__(self, other):
        return Equation(other) / self

    def __rfloordiv__(self, other):
        return Equation(other) // self

class SquareRoot(Root):
    def __new__(cls, value: int | float | Root):
        return super().__new__(cls, value, 2)
