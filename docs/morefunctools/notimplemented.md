# morefunctools.notimplemented

## Annotations

```python
@overload
def notimplemented(enumtype: NotImplemented = NotImplemented.Default, message: Optional[str] = None) -> Callable[[Callable], Callable]:
    ...

@overload
def notimplemented(fn: Callable) -> Callable:
    ...
```

## Notes

Denotes that a function is not implemented and, depending on the value of `enumtype` if specified, throw a warning or an error.

## Parameters

`enumtype: NotImplemented = NotImplemented.Default`
: Describes what should happen when the function is called.
: `NotImplemented.Default` uses your message if any, or `f"{fn.__qualname__} is not implemented."`
: `NotImplemented.Abstract` uses `f"{fn.__qualname__} is an abstract method, and therefore not implemented."`
: `NotImplemented.Development` uses `f"{fn.__qualname__} is in development, and not yet finished. Expect unfinished or broken behaviour."`
: `NotImplemented.Broken` uses `f"{fn.__qualname__} is broken and may not function properly."`

`message: Optional[str] = None`
: The warning message to display when the function is used. Only applied if `enumtype` is `NotImplemented.Default`

## Return Value

*N/A*

## Raises

*N/A*

## Example usage

```python
from morefunctools import notimplemented, NotImplemented

@notimplemented(NotImplemented.Development)
def test():
    a = 1
    b = 2
    ... # unfinished behaviour

def main():
    test()  # NotImplementedWarning: test is in development, and not yet finished. Expect unfinished or broken behaviour.
```
