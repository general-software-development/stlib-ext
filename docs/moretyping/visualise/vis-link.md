# moretyping.vis.VisLink

## Annotations

```python
class VisLink(metaclass=VisualiseMeta):
    def __init__(self, data: list[Any]) -> None:
        ...

    @cached_property
    def strdata(self) -> Iterable[str]:
        ...

    @cached_property
    def string(self) -> str:
        ...
```

## Parameters

`data: list[Any]`
: A list of objects of any kind.

## Return Value

Returns a `VisLink` instance.

## Properties

`strdata: Iterable[str]`
: An iterable object (not list) containing a stringified version of each element in `data`.

`string: str`
: A stringified version of the data.

## Methods

```py
def __str__(self) -> str:
    ...
```
: Equivilant to the `string` property

```py
def __repr__(self) -> str:
    ...
```
: Class name + stringified data.

## Details

For a list such as `[1, 2, 3]`, it will return `[ 1 > 2 > 3 ]`.

## Example usage

```python
from moretyping.vis import VisLink

data = [1, 2, 3, 4]

view = VisLink(data)

print(view)        # [ 1 > 2 > 3 > 4 ]
print(repr(view))  # <VisLink object> [ 1 > 2 > 3 > 4 ]
```
