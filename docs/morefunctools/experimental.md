# morefunctools.experimental

## Annotations

```python
@overload
def experimental(message: Optional[str] = None,
                 category: type[Warning] = ExperimentalWarning,
                 stacklevel: int = 2
                ) -> Callable[[Callable], Callable]:
    ...

@overload
def experimental(fn: Callable) -> Callable:
    ...
```

## Parameters

`message: Optional[str] = None`
: The warning message to display when the function is used.

`category: type[Warning] = ExperimentalWarning`
: Warning type/class

`stacklevel: int = 2`
: Stack level passed to `warnings.warn`

## Return Value

*N/A*

## Raises

*N/A*

## Example usage

```python
from morefunctools import experimental

@experimental
def test1() -> str:
    return "Hello, world!"

@experimental(message = "Hello, world!")
def test2() -> None:
    return

def main():
    test1()  # ExperimentalWarning('Function {test1} is experimental. Expect bugs or incomplete behaviour.')
    test2()  # ExperimentalWarning('Hello, world!')
```
