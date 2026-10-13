from dataclasses import dataclass
from typing import Any, Optional, Self
from abc import ABC

class Op(ABC):
    a: Any
    b: Any

@dataclass
class Add(Op):
    a: Any
    b: Any

    def __str__(self) -> str:
        return f"{self.a} + {self.b}"

@dataclass
class Substract(Op):
    a: Any
    b: Any

    def __str__(self) -> str:
        return f"{self.a} - {self.b}"

@dataclass
class Multiply(Op):
    a: Any
    b: Any

    def __str__(self) -> str:
        return f"({self.a}) * ({self.b})"

@dataclass
class Divide(Op):
    a: Any
    b: Any

    def __str__(self) -> str:
        return f"({self.a}) / ({self.b})"

@dataclass
class FloorDivide(Op):
    a: Any
    b: Any

    def __str__(self) -> str:
        return f"({self.a}) // ({self.b})"

class Equation:
    def __init__(self, value: Optional[Any] = None) -> None:
        self.eq = None
        if value is not None:
            self.eq = value

    def __add__(self, other) -> Self:
        n = self.copy()
        n.eq = Add(n.eq, other)
        return n

    def __sub__(self, other):
        n = self.copy()
        n.eq = Substract(n.eq, other)
        return n

    def __mul__(self, other):
        n = self.copy()
        n.eq = Multiply(n.eq, other)
        return n

    def __truediv__(self, other):
        n = self.copy()
        n.eq = Divide(n.eq, other)
        return n

    def __floordiv__(self, other):
        n = self.copy()
        n.eq = FloorDivide(n.eq, other)
        return n

    def __radd__(self, other) -> Self:
        n = self.copy()
        n.eq = Add(n.eq, other)
        return n

    def __rsub__(self, other):
        n = self.copy()
        n.eq = Substract(n.eq, other)
        return n

    def __rmul__(self, other):
        n = self.copy()
        n.eq = Multiply(n.eq, other)
        return n

    def __rtruediv__(self, other):
        n = self.copy()
        n.eq = Divide(n.eq, other)
        return n

    def __rfloordiv__(self, other):
        n = self.copy()
        n.eq = FloorDivide(n.eq, other)
        return n

    def resolve(self) -> Self:
        n = self.copy()

        def _resolve_it(op: Op) -> Op | int | float | Any:
            if not isinstance(op, Op):
                if isinstance(op, Equation):
                    raise TypeError()

                if hasattr(op, "_to_numeric"):
                    return op._to_numeric()
                
                return op  # Just a literal / already resolved

            ops = {
                Add: lambda a, b: a + b,
                Substract: lambda a, b: a - b,
                Multiply: lambda a, b: a * b,
                Divide: lambda a, b: a / b,
                FloorDivide: lambda a, b: a // b
            }

            try:
                a = _resolve_it(op.a)
                b = _resolve_it(op.b)

                if isinstance(op, Substract) and isinstance(a, Add):
                    if isinstance(a.b, (int, float)) and isinstance(b, (int, float)):
                        return _resolve_it(Add(a.a, a.b - b))

                if isinstance(op, Add) and isinstance(a, Add):
                    if isinstance(a.b, (int, float)) and isinstance(b, (int, float)):
                        return _resolve_it(Add(a.a, a.b + b))

                value = ops[type(op)](a, b)

                if isinstance(value, (Op, Equation)):
                    return op
                else:
                    return value
            except (TypeError, ValueError):
                return op

        n.eq = _resolve_it(n.eq)

        return n

    def copy(self) -> Self:
        n = Equation()
        n.eq = self.eq
        return n

    def __str__(self) -> str:
        eq_str = str(self.eq)
        return f"Equation({eq_str})"
