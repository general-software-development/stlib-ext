from functools import wraps
from collections.abc import Callable
from typing import Any, Optional, overload
import warnings

class ExperimentalWarning(Warning):
    def __init__(self, message: str) -> None:
        self.msg = message
        super().__init__(message)

@overload
def experimental(message: Optional[str] = None, category: type[Warning] = ExperimentalWarning, stacklevel: int = 2) -> Callable[[Callable], Callable]:
    ...

@overload
def experimental(fn: Callable) -> Callable:
    ...

# TODO: Clean up a little
def experimental(message: Optional[str] | Callable = None, category: type[Warning] = ExperimentalWarning, stacklevel: int = 2) -> Callable:
    newMessage = None if callable(message) else message
    if callable(message):
        fn = message
        message = None
        
        @wraps(fn)
        def wrapper(*args, **kwargs) -> Any:
            warnings.warn(newMessage or f"Function {'{'}{fn.__name__}{'}'} is experimental. Expect bugs or incomplete behaviour.", category = category, stacklevel = stacklevel)
            return fn(*args, **kwargs)
        
        return wrapper

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs) -> Any:
            warnings.warn(newMessage or f"Function {'{'}{fn.__name__}{'}'} is experimental. Expect bugs or incomplete behaviour.", category = category, stacklevel = stacklevel)
            return fn(*args, **kwargs)
        return wrapper

    return decorator

@experimental
def test():
    ...

__defaults__ = (
    experimental,
)
