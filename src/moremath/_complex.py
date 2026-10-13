from builtins import NotImplemented
from typing import Any

class Complex:
    def __init__(self, real: int | float | Any, imag: int | float | Any, **other_imag: int | float | Any):
        self.real = real
        self.imags = {"i": imag}
        for basis, multiplier in other_imag.items():
            self.imags[basis] = multiplier

    def __add__(self, other: "Complex") -> "Complex":
        if not isinstance(other, Complex):
            return NotImplemented

        real = self.real + other.real

        imags = self.imags.copy()

        for basis, coefficient in other.imags.items():
            imags[basis] = imags.get(basis, 0) + coefficient

        return Complex(
            real,
            **imags
        )

    def __repr__(self) -> str:
        terms = [str(self.real)]

        for basis, coefficient in self.imags.items():
            if coefficient != 0:
                terms.append(f"{coefficient}{basis}")

        return "Complex(" + " + ".join(terms) + ")"
