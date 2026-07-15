# moretyping.vis.ViewJSON

## Annotations

```python
class ViewJSON(metaclass=VisualiseMeta):
    def __init__(self, data: Optional[Any] = {}) -> None:
        ...

    @cached_property
    def string(self) -> str:
        ...
```

## Parameters

`data: Optional[Any]`
: Any JSON-compatible object.

## Return Value

Returns a `ViewJSON` instance.

## Properties

`string: str`
: A JSON-serialised verison of the data.

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

For any object, returns the JSON conversion of it.

## Example usage

```python
from moretyping.vis import ViewJSON

data = {
    "users": [
        {
            "name": "User123",
            "age": 24,
        }
    ]
}

view = ViewJSON(data)

print(view)
#{
#   "users": [
#       {
#           "name": "User123",
#           "age": 24
#       }
#   ]
#}
```
