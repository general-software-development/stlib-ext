from typing import Any
from ._meta_process import ProcessMeta

type Numeric = int | float

class Number(metaclass=ProcessMeta, output_classes=(int, float)):
    """
    Convert an object of unknown type to a Numeric (`int|float`) value.

    Args:
        value: Numeric | Any &mdash; The value to cast to a Numeric type.

    Returns:
        Numeric &mdash; The value cast to a Numeric type.

    Raises:
        ValueError: If the value can't be cast to a numeric type.

    Details:
        If the value is an integer, return it unchanged.

        Otherwise, return `float(value)`
    """
    def __new__(cls, value: Numeric | Any) -> int | float:  # type: ignore[misc]
        if isinstance(value, int):
            return value
        return float(value)
