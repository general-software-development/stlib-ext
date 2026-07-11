# moretyping.data.Number

## Annotations

```python
type Numeric = float | int

class Number(metaclass=ProcessMeta, output_classes=(int, float)):
    def __new__(cls, value: Numeric | Any) -> Numeric:
        ...
```

## Parameters

`value: Numeric | Any`
: An integer or float, or any object convertible to a float.

## Return Value

Returns `Numeric` &mdash; the integer/float created from `value`

## Raises

`ValueError`

: If the value can't be cast to a numeric type.

## Details

If the value is an integer, return it unchanged.

Otherwise, return `float(value)`.

## Example usage

```python
from moretyping.data import Number

a = 8
b = "4"
c = "4.2"

print(Number(a))  # 8
print(Number(b))  # 4.0
print(Number(c))  # 4.2
```
