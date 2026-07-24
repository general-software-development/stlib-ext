from enum import Enum, auto
from typing import Any, Callable, Optional, overload
from functools import wraps
from warnings import warn

class NotImplementedWarning(Warning):
    ...

class NotImplemented(Enum):
    Abstract = auto()
    Development = auto()
    Broken = auto()
    Default = auto()

@overload
def notimplemented(enumtype: NotImplemented = NotImplemented.Default, message: Optional[str] = None) -> Callable[[Callable], Callable]:
    ...

@overload
def notimplemented(fn: Callable) -> Callable:
    ...

def notimplemented(function_or_enumtype: NotImplemented | Callable = NotImplemented.Default, message: Optional[str] = None):
    function = None
    enumtype = None
    if callable(function_or_enumtype):
        function = function_or_enumtype
        enumtype = NotImplemented.Default
    else:
        enumtype = function_or_enumtype
        function = None

    def runBehaviour(fn: Callable, *args, **kwargs) -> Any:
        if enumtype is NotImplemented.Abstract:
            raise NotImplementedError(f"{fn.__qualname__} is an abstract method, and therefore not implemented.")
        elif enumtype is NotImplemented.Development:
            warn(f"{fn.__qualname__} is in development, and not yet finished. Expect unfinished or broken behaviour.", NotImplementedWarning)
        elif enumtype is NotImplemented.Broken:
            warn(f"{fn.__qualname__} is broken and may not function properly.", NotImplementedWarning)
        elif enumtype is NotImplemented.Default:
            raise NotImplementedError(message or f"{fn.__qualname__} is not implemented.")
        else:
            raise ValueError()

        return fn(*args, **kwargs)

    if function is None:
        def decorator(fn: Callable) -> Callable:
            @wraps(fn)
            def wrapper(*args, **kwargs) -> Any:
                return runBehaviour(fn, *args, **kwargs)

            return wrapper
        return decorator
    else:
        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:
            return runBehaviour(function, *args, **kwargs)
        return wrapper
    